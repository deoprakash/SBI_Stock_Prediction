import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import StockChart from './components/StockChart';
import './App.css';

function App() {
  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="container">
          <div className="row align-items-center py-4">
            <div className="col-md-8">
              <h1 className="mb-2 fw-bold d-flex align-items-center">
                <img src="src/assets/GKV1_State Bank of India (SBI)-logobase.net.png" alt="SBI Logo" style={{width: '40px', height: '40px', marginRight: '12px'}} />
                SBI Stock Price Prediction
              </h1>
              <p className="text-muted mb-0">
                Real-time SBI stock price forecasting
              </p>
            </div>
            <div className="col-md-4 text-md-end">
              <div className="stock-info">
                <span className="badge bg-primary fs-6 px-3 py-2">
                  <i className="bi bi-building me-2"></i>
                  SBIN.NS
                </span>
                <small className="d-block mt-2 text-muted">
                  State Bank of India - NSE
                </small>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container my-4">
        <StockChart />
      </main>

      {/* Footer */}
      <footer className="app-footer mt-5 py-4 bg-light">
        <div className="container text-center">
          <p className="text-muted mb-2">
            Made by DEO PRAKASH
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
