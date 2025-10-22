"""
Simple SBI Stock Price Prediction Test Script
Uses sbi_model.h5 to predict next day's stock price
"""

import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import pandas as pd
import os

# Configuration
TICKER = "SBIN.NS"
TIME_STEP = 60

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'sbi_model.h5')

print("Loading model...")
model = load_model(MODEL_PATH)
print(f"✓ Model loaded from: {MODEL_PATH}")

# Fetch recent data (5 years to ensure enough after dropna)
print(f"\nFetching {TICKER} data...")
df = yf.download(TICKER, period="5y", interval="1d", progress=False, auto_adjust=False)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

# Feature engineering
print("Engineering features...")
df['MA50'] = df['Close'].rolling(50).mean()
df['MA200'] = df['Close'].rolling(200).mean()
df['Return'] = df['Close'].pct_change()
df = df.dropna()

print(f"Data shape: {df.shape}")
print(f"Date range: {df.index[0]} to {df.index[-1]}")

# Check if we have enough data
if len(df) < TIME_STEP:
    print(f"\n❌ Error: Not enough data. Need {TIME_STEP} rows, got {len(df)}")
    print("Try fetching more historical data (period='5y' or '10y')")
    exit(1)

# Scale data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df)

# Prepare input sequence (last 60 days)
last_sequence = scaled_data[-TIME_STEP:]
X_input = last_sequence.reshape(1, TIME_STEP, df.shape[1])

print(f"\nInput shape: {X_input.shape}")

# Make prediction
print("Making prediction...")
predicted_scaled = model.predict(X_input, verbose=0)

# Inverse transform to get actual price
# The model predicts all 8 features, we need the Close price (index 3)
predicted_values = scaler.inverse_transform(predicted_scaled)

# Extract predicted values
pred_open = predicted_values[0, 0]
pred_high = predicted_values[0, 1]
pred_low = predicted_values[0, 2]
pred_close = predicted_values[0, 3]
pred_volume = predicted_values[0, 4]

# Current values (handle MultiIndex if present)
current_close = float(df.iloc[-1, 3])  # Close is at index 3
current_date = df.index[-1]

# Calculate next trading day
next_date = current_date + pd.Timedelta(days=1)
while next_date.weekday() >= 5:  # Skip weekends
    next_date += pd.Timedelta(days=1)

# Display results
print("\n" + "="*60)
print("PREDICTION RESULTS")
print("="*60)
print(f"\nCurrent Date:  {current_date.strftime('%Y-%m-%d')}")
print(f"Current Close: ₹{current_close:.2f}")
print(f"\nPredicted Date: {next_date.strftime('%Y-%m-%d')}")
print("-" * 60)
print(f"Predicted Open:   ₹{pred_open:.2f}")
print(f"Predicted High:   ₹{pred_high:.2f}")
print(f"Predicted Low:    ₹{pred_low:.2f}")
print(f"Predicted Close:  ₹{pred_close:.2f}")
print(f"Predicted Volume: {pred_volume:,.0f}")
print("-" * 60)

# Calculate expected change
change = pred_close - current_close
change_percent = (change / current_close) * 100

if change >= 0:
    print(f"\nExpected Change: +₹{change:.2f} (+{change_percent:.2f}%) ▲")
    print("Signal: BULLISH 🟢")
else:
    print(f"\nExpected Change: ₹{change:.2f} ({change_percent:.2f}%) ▼")
    print("Signal: BEARISH 🔴")

print("="*60)

# Show last 5 days for context
print("\nLast 5 Days Historical Data:")
print("-" * 60)
print(df[['Open', 'High', 'Low', 'Close', 'Volume']].tail())
print("="*60)
