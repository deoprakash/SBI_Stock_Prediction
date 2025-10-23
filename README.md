# SBI Stock Prediction

**A Deep Learning-based Stock Price Forecasting System for the State Bank of India (SBI)**

---


## SBI Stock Price Prediction - Frontend Dashboard

Professional React-based dashboard for visualizing SBI stock predictions powered by LSTM neural networks.

## 🚀 Features

- **Real-time Predictions**: Displays next-day stock price forecast
- **Interactive Chart**: Last 100 days of historical data with smooth animations
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Auto-refresh**: Updates every hour automatically
- **Professional UI**: Modern card-based layout with gradient headers
- **Color-coded Predictions**: Green for positive, red for negative changes
- **Loading States**: Smooth loading spinners and error handling

## 📦 Tech Stack

- **React 19** - UI framework
- **Vite** - Build tool and dev server
- **Chart.js** - Chart visualization
- **Bootstrap 5** - UI components and styling
- **Axios** - HTTP client
- **Bootstrap Icons** - Icon library

## 🛠️ Setup

### Install Dependencies
```bash
npm install
```

### Start Development Server
```bash
npm run dev
```
Opens at `http://localhost:5173`

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## 📊 Dashboard Components

### 1. Header Section
- Stock ticker badge (SBIN.NS)
- Professional gradient background
- Descriptive subtitle

### 2. Prediction Stats Card
- **Current Price**: Last closing price from historical data
- **Predicted Price**: Next trading day forecast
- **Expected Change**: Absolute and percentage change with arrows

### 3. Interactive Price Chart
- 100-day historical price trend (solid blue line)
- Next-day prediction (dashed line, color-coded)
- Hover tooltips with exact prices
- Responsive scaling

### 4. Footer
- Model information
- Disclaimer
- Last update timestamp

## 🎨 Visual Features

### Color Scheme
- Primary Blue: `#2563eb` (historical data)
- Success Green: `#10b981` (positive predictions)
- Danger Red: `#ef4444` (negative predictions)
- Background: Gradient `#f5f7fa` to `#c3cfe2`
- Header: Purple gradient `#667eea` to `#764ba2`

### Responsive Design
- **Desktop**: Full three-column stat layout
- **Tablet**: Adjusted spacing
- **Mobile**: Stacked layout, optimized chart height

## 🔌 API Integration

Backend endpoint: `http://127.0.0.1:5000/predict`

**Expected Response:**
```json
{
  "historical": {
    "dates": ["2025-07-01", "2025-07-02", ...],
    "prices": [850.25, 852.50, ...]
  },
  "predicted": {
    "date": "2025-10-21",
    "price": 887.13
  }
}
```

## 📱 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS/Android)

## 🧪 Development

### File Structure
```
src/
├── components/
│   └── StockChart.jsx    # Main chart component
├── App.jsx               # Main app layout
├── App.css               # Custom styles
├── index.css             # Global styles
└── main.jsx              # Entry point
```

### Key Dependencies
```json
{
  "axios": "^1.12.2",
  "bootstrap": "^5.3.8",
  "bootstrap-icons": "^1.11.3",
  "chart.js": "^4.5.1",
  "react-chartjs-2": "^5.3.0"
}
```

## 🐛 Troubleshooting

### Backend Connection Issues
Ensure Flask backend is running:
```bash
cd ../Backend
python app.py
```

### CORS Errors
Backend should have CORS enabled:
```python
from flask_cors import CORS
CORS(app)
```

### Icons Not Displaying
Verify bootstrap-icons import in `App.jsx`:
```javascript
import 'bootstrap-icons/font/bootstrap-icons.css';
```

## 🔮 Future Enhancements

- Dark mode toggle
- Multiple stock tickers
- Date range selector
- Historical predictions comparison
- Export chart as image
- Real-time WebSocket updates
- Technical indicators overlay


## SBI Stock Price Prediction - Backend

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

## ⚙️ CI/CD Pipeline

- Tools Used: GitHub Actions, Azure DevOps, Netlify CI
- Workflow:
  - Code commits trigger automated tests and deployment
  - Backend updates deployed to Azure
  - Frontend updates deployed to Netlify
  - Zero downtime updates

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/deoprakash/SBI_Stock_Prediction.git
cd SBI_Stock_Prediction
```

2. Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

4. Set up frontend:

```bash
cd frontend
npm install
```

5. Run the backend locally:

```bash
cd backend
python app.py
```

6. Run the frontend locally:

```bash
cd frontend
npm start
```

---

## 🚀 Usage

- Access the live application:
  - Frontend: [SBI Stock Prediction](https://sbi-stock-prediction.netlify.app/)
  - Backend API: [Azure-hosted Flask API](https://sbi-stock-prediction-hwfsbfh0hscwc2b6.centralindia-01.azurewebsites.net/predict)

- API Endpoints:
  - `GET /predict` - Retrieve the latest stock predictions
  - `GET /history` - Access historical prediction data

---

## 📈 Model Retraining

- Frequency: Daily
- Process:
  - Fetch latest stock data
  - Preprocess data
  - Retrain LSTM model
  - Update model weights

---

## 🛠️ Deployment

### Backend (Azure)
1. Set up Azure App Service
2. Deploy the Flask application

### Frontend (Netlify)
1. Set up Netlify
2. Deploy the React application

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Commit your changes
5. Push to your fork
6. Create a Pull Request

---

## 📄 License

This project is licensed under the Apache License 2.0. See [LICENSE](https://github.com/deoprakash/SBI_Stock_Prediction/blob/main/LICENSE).

---

## 📬 Contact

- Author: [@deoprakash](https://github.com/deoprakash)
- Email: deoprakash364@gmail.com

