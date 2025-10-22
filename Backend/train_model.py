"""
Daily SBI Stock Price Prediction Model Training Script
Fetches 10 years of data ending yesterday, trains LSTM model, and saves model + scaler
"""

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import pickle
import os
from datetime import datetime, timedelta

# Configuration
TICKER = "SBIN.NS"
TIME_STEP = 60
EPOCHS = 50
BATCH_SIZE = 32

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'sbi_model.h5')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

# Ensure model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

def fetch_training_data():
    """Fetch 10 years of data ending yesterday"""
    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365*10)).strftime('%Y-%m-%d')
    
    print(f"Fetching {TICKER} data from {start_date} to {end_date}...")
    df = yf.download(TICKER, start=start_date, end=end_date, progress=True, auto_adjust=False)
    
    # Select OHLCV columns
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    print(f"Downloaded {len(df)} rows")
    return df

def engineer_features(df):
    """Add technical indicators"""
    print("Engineering features...")
    df['MA50'] = df['Close'].rolling(50).mean()
    df['MA200'] = df['Close'].rolling(200).mean()
    df['Return'] = df['Close'].pct_change()
    df = df.dropna()
    
    print(f"After feature engineering and dropna: {len(df)} rows")
    return df

def scale_data(df):
    """Scale features and save scaler"""
    print("Scaling data...")
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df)
    
    # Save the scaler for inference
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Scaler saved to {SCALER_PATH}")
    
    return scaled_data, scaler

def create_sequences(data, time_step=60):
    """Create LSTM input sequences"""
    X, y = [], []
    for i in range(time_step, len(data)):
        X.append(data[i-time_step:i])
        y.append(data[i])  # Predict all features
    return np.array(X), np.array(y)

def build_model(input_shape, output_features):
    """Build multi-output LSTM model"""
    print("Building LSTM model...")
    model = Sequential([
        LSTM(100, return_sequences=True, input_shape=input_shape),
        Dropout(0.3),
        LSTM(100),
        Dropout(0.3),
        Dense(output_features)
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.summary()
    return model

def train_and_save_model():
    """Main training pipeline"""
    print("\n" + "="*60)
    print(f"Starting training at {datetime.now()}")
    print("="*60 + "\n")
    
    # 1. Fetch data
    df = fetch_training_data()
    
    # 2. Engineer features
    df = engineer_features(df)
    
    # 3. Scale data and save scaler
    scaled_data, scaler = scale_data(df)
    
    # 4. Create sequences
    print(f"Creating sequences with TIME_STEP={TIME_STEP}...")
    X, y = create_sequences(scaled_data, TIME_STEP)
    print(f"X shape: {X.shape}, y shape: {y.shape}")
    
    # 5. Build model
    model = build_model(input_shape=(X.shape[1], X.shape[2]), output_features=y.shape[1])
    
    # 6. Train model
    print(f"\nTraining model for {EPOCHS} epochs...")
    history = model.fit(X, y, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1, validation_split=0.1)
    
    # 7. Save model
    model.save(MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")
    
    # 8. Training summary
    print("\n" + "="*60)
    print("Training completed successfully!")
    print(f"Final training loss: {history.history['loss'][-1]:.6f}")
    print(f"Final validation loss: {history.history['val_loss'][-1]:.6f}")
    print(f"Model file: {MODEL_PATH}")
    print(f"Scaler file: {SCALER_PATH}")
    print(f"Completed at: {datetime.now()}")
    print("="*60 + "\n")

if __name__ == "__main__":
    import argparse, time
    parser = argparse.ArgumentParser(description="Train SBI model and optionally auto-train on an interval")
    parser.add_argument("--interval", type=float, default=None, help="Auto-train interval in hours (e.g., 24 for daily). If omitted, trains once and exits.")
    args = parser.parse_args()

    try:
        if args.interval and args.interval > 0:
            hours = args.interval
            print(f"\nAuto-training enabled: will retrain every {hours} hour(s). Press Ctrl+C to stop.\n")
            while True:
                start_ts = datetime.now()
                train_and_save_model()
                elapsed = (datetime.now() - start_ts).total_seconds()
                sleep_s = max(0, hours * 3600 - elapsed)
                print(f"\nSleeping for {sleep_s/3600:.2f} hour(s) until next run...\n")
                time.sleep(sleep_s)
        else:
            train_and_save_model()
    except KeyboardInterrupt:
        print("\nAuto-training stopped by user.")
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
