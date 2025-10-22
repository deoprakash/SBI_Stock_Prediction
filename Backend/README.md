# SBI Stock Price Prediction - Backend

Flask API for predicting SBI stock prices using LSTM neural network with automated daily training.

## Architecture

```
┌─────────────────┐      Daily 2 AM      ┌──────────────────┐
│ train_model.py  │ ──────────────────▶  │   model.h5       │
│ (Training)      │                       │   scaler.pkl     │
└─────────────────┘                       └──────────────────┘
                                                   │
                                                   │ Load
                                                   ▼
                                          ┌──────────────────┐
                                          │     app.py       │
                                          │  (Inference)     │
                                          └──────────────────┘
                                                   │
                                                   │ HTTP
                                                   ▼
                                          ┌──────────────────┐
                                          │   Frontend       │
                                          │   (React)        │
                                          └──────────────────┘
```

## Files Overview

| File | Purpose |
|------|---------|
| `train_model.py` | Training script - Fetches 10y data, trains LSTM, saves model+scaler |
| `app.py` | Flask API - Loads saved model+scaler, serves predictions |
| `run_training.bat` | Windows batch script to run training with venv |
| `TRAINING_SETUP.md` | Complete guide for automated training setup |
| `requirements.txt` | Python dependencies |

## Quick Start

### 1. Activate Virtual Environment
```powershell
cd Backend
.\myenv\Scripts\activate
```

### 2. Install Dependencies (if needed)
```powershell
pip install -r requirements.txt
```

### 3. Train Model (First Time)
```powershell
python train_model.py
```
This takes ~2-3 minutes and creates:
- `model/sbi_model.h5` (1.5 MB)
- `model/scaler.pkl` (800 bytes)

### 4. Start API Server
```powershell
python app.py
```
Server runs on: `http://127.0.0.1:5000`

### 5. Test API
```powershell
curl http://127.0.0.1:5000/predict
```

## API Endpoints

### GET `/predict`
Returns SBI stock price prediction for next trading day.

**Response:**
```json
{
  "historical": {
    "dates": ["2025-07-01", "2025-07-02", ...],
    "prices": [850.25, 852.50, ...]
  },
  "predicted": {
    "date": "2025-10-21",
    "price": 887.13,
    "open": 885.10,
    "high": 892.50,
    "low": 880.75,
    "close": 887.13,
    "volume": 5367969
  }
}
```

**Error Response:**
```json
{
  "error": "Scaler not loaded. Please run train_model.py first.",
  "historical": { "dates": [], "prices": [] },
  "predicted": { "date": null, "price": null }
}
```

## Model Details

- **Architecture:** LSTM (100→Dropout→100→Dropout→Dense)
- **Input:** 60-day sequences with 8 features
- **Features:** Open, High, Low, Close, Volume, MA50, MA200, Return
- **Output:** Multi-output prediction (all 8 features)
- **Training:** 50 epochs, batch size 32, 10% validation split
- **Data:** 10 years of SBIN.NS (NSE) daily OHLCV data

## Training vs Inference

| Aspect | Training (`train_model.py`) | Inference (`app.py`) |
|--------|----------------------------|---------------------|
| **Data** | 10 years ending yesterday | Latest 5 years for features |
| **Scaler** | `fit_transform()` - creates scaler | `transform()` - uses saved scaler |
| **Output** | Saves model.h5 + scaler.pkl | Loads model.h5 + scaler.pkl |
| **Frequency** | Daily at 2 AM (automated) | On-demand via API |
| **Duration** | ~2-3 minutes | <1 second |

## Why Separate Training?

✅ **Consistent Predictions** - Scaler stays fixed between training runs  
✅ **No Re-fitting** - API doesn't re-fit scaler on every request  
✅ **Fast Inference** - API just transforms and predicts  
✅ **Production Ready** - Training downtime doesn't affect API  
✅ **Automated Updates** - Model retrains daily with fresh data  

## Automated Daily Training

See `TRAINING_SETUP.md` for complete instructions on:
- Windows Task Scheduler setup
- Monitoring training runs
- Troubleshooting

**Quick Setup:**
1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Create Basic Task → Daily at 2:00 AM
3. Action → Run `run_training.bat`

## Troubleshooting

### Scaler Not Found
```
⚠ Scaler not found. Run train_model.py first!
```
**Fix:** `python train_model.py`

### Import Errors
```
ModuleNotFoundError: No module named 'tensorflow'
```
**Fix:** Activate venv and install dependencies:
```powershell
.\myenv\Scripts\activate
pip install -r requirements.txt
```

### Shape Mismatch
```
ValueError: cannot reshape array
```
**Fix:** Ensure you ran `train_model.py` to generate the correct model

## Development

### Run in Debug Mode
```powershell
$env:FLASK_ENV="development"; python app.py
```

### Check Logs
API prints scaler load status:
```
✓ Loaded scaler from C:\...\model\scaler.pkl
```

### Manual Training Test
```powershell
python train_model.py
```

## Production Deployment

For production deployment:

1. **Use Gunicorn/Waitress** instead of Flask dev server
2. **Set up monitoring** for training failures
3. **Add model versioning** (timestamp-based filenames)
4. **Implement rollback** to previous model if new one underperforms
5. **Add health check endpoint** (`/health`)

## License

MIT

## Contact

For issues or questions, please open a GitHub issue.
