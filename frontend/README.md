# SBI Stock Price Prediction - Frontend Dashboard

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

## 📄 License

MIT

---

**Built with React + Vite for optimal performance and developer experience** ⚡
