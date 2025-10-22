from flask import Flask, jsonify
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from flask_cors import CORS
import os
import pickle

app = Flask(__name__)

# Configure CORS for production
if os.environ.get('AZURE_DEPLOYMENT'):
    # In production, only allow your frontend domain
    CORS(app, resources={r"/*": {"origins": os.environ.get('FRONTEND_URL', '*')}})
else:
    # In development, allow all origins
    CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'sbi_model.h5')
SCALER_PATH = os.path.join(BASE_DIR, 'model', 'scaler.pkl')

# Load trained model and scaler
model = load_model(MODEL_PATH)

# Load the scaler that was fitted during training
try:
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    print(f"✓ Loaded scaler from {SCALER_PATH}")
except FileNotFoundError:
    print(f"⚠ Scaler not found at {SCALER_PATH}. Run train_model.py first!")
    scaler = None

TIME_STEP = 60

def fetch_data_and_predict():
    # Fetch enough history for MA200 + 60-step sequence (use 5y to be safe)
    # Explicitly set auto_adjust to False to match typical training defaults
    df = yf.download("SBIN.NS", period="10y", interval="1d", auto_adjust=False, progress=False)
    df = df[['Open','High','Low','Close','Volume']]
    
    # Feature engineering
    df['MA50'] = df['Close'].rolling(50).mean()
    df['MA200'] = df['Close'].rolling(200).mean()
    df['Return'] = df['Close'].pct_change()
    df = df.dropna()
    
    # Guard: ensure we have enough rows after dropna for the sequence length
    if len(df) < TIME_STEP:
        return {
            'error': f'Insufficient data after feature engineering. Need at least {TIME_STEP} rows, got {len(df)}.',
            'historical': { 'dates': [], 'prices': [] },
            'predicted': { 'date': None, 'price': None }
        }

    # Guard: ensure scaler was loaded
    if scaler is None:
        return {
            'error': 'Scaler not loaded. Please run train_model.py to train the model first.',
            'historical': { 'dates': [], 'prices': [] },
            'predicted': { 'date': None, 'price': None }
        }

    # Scale using the pre-fitted scaler from training (DO NOT re-fit)
    scaled_data = scaler.transform(df)

    # Last 60 days for prediction
    last_seq = scaled_data[-TIME_STEP:]
    # Guard: last_seq must be exactly TIME_STEP rows
    if last_seq.shape[0] != TIME_STEP:
        return {
            'error': f'Not enough sequence length for prediction. Expected {TIME_STEP}, got {last_seq.shape[0]}',
            'historical': { 'dates': [], 'prices': [] },
            'predicted': { 'date': None, 'price': None }
        }

    X_input = last_seq.reshape(1, TIME_STEP, df.shape[1])
    pred_scaled = model.predict(X_input, verbose=0)
    # Model outputs all features scaled (Open, High, Low, Close, Volume, MA50, MA200, Return)
    pred_values = scaler.inverse_transform(pred_scaled)
    pred_open = float(pred_values[0, 0])
    pred_high = float(pred_values[0, 1])
    pred_low  = float(pred_values[0, 2])
    pred_close = float(pred_values[0, 3])
    pred_volume = float(pred_values[0, 4])

    # Historical data
    # Get closes by position to avoid MultiIndex column name issues
    history_prices = df.iloc[:, 3].tail(100).to_list()
    history_dates = df.index[-100:].tolist()

    # Predicted next day
    # Move to next trading day (skip weekends)
    pred_date = history_dates[-1] + pd.Timedelta(days=1)
    while pred_date.weekday() >= 5:  # 5=Sat, 6=Sun
        pred_date += pd.Timedelta(days=1)

    return {
        'historical': {
            'dates': [d.strftime('%Y-%m-%d') for d in history_dates],
            'prices': [round(p,2) for p in history_prices]
        },
        'predicted': {
            'date': pred_date.strftime('%Y-%m-%d'),
            'price': round(pred_close, 2),
            'open': round(pred_open, 2),
            'high': round(pred_high, 2),
            'low': round(pred_low, 2),
            'close': round(pred_close, 2),
            'volume': int(pred_volume)
        }
    }

@app.route('/predict')
def predict():
    data = fetch_data_and_predict()
    return jsonify(data)

if __name__ == "__main__":
    # Only run with debug in local development
    port = int(os.environ.get("PORT", 5000))
    debug_mode = not os.environ.get('AZURE_DEPLOYMENT')
    app.run(host='0.0.0.0', port=port, debug=debug_mode)


#893.26
