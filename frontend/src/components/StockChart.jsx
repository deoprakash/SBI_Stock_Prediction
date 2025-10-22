import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, Title, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Filler } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Filler);

const StockChart = () => {
  const [chartData, setChartData] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);
  // Store the first predicted high and date
  const initialPredHigh = useRef(null);
  const initialPredDate = useRef(null);

  // Use environment variable for API URL
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const res = await axios.get(`${API_URL}/predict`);
      
      if (res.data.error) {
        setError(res.data.error);
        setLoading(false);
        return;
      }

      const historicalDates = res.data.historical.dates;
      const historicalPrices = res.data.historical.prices;
  const predDate = res.data.predicted.date;
  const predPrice = res.data.predicted.price;
  const predOpen = res.data.predicted.open;
  const predHigh = res.data.predicted.high;
  const predLow  = res.data.predicted.low;
  const predClose = res.data.predicted.close;
  const predVolume = res.data.predicted.volume;

      // Calculate price change
      const lastPrice = historicalPrices[historicalPrices.length - 1];
      const priceChange = predPrice - lastPrice;
      const priceChangePercent = ((priceChange / lastPrice) * 100).toFixed(2);

      setPrediction({
        date: predDate,
        price: predPrice,
        lastPrice: lastPrice,
        change: priceChange.toFixed(2),
        changePercent: priceChangePercent,
        open: predOpen,
        high: predHigh,
        low: predLow,
        close: predClose,
        volume: predVolume
      });

      // Store the first predicted high and date only once
      if (initialPredHigh.current === null && initialPredDate.current === null) {
        initialPredHigh.current = predHigh;
        initialPredDate.current = predDate;
      }

      setChartData({
        labels: [...historicalDates, predDate],
        datasets: [
          {
            label: 'Historical Price (₹)',
            // End historical series at last available date; null for tomorrow
            data: [...historicalPrices, null],
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 0,
            pointHoverRadius: 5,
            borderWidth: 2
          },
          {
            label: 'Predicted Price (₹)',
            // Only show predicted price for tomorrow's date
            data: [...Array(historicalPrices.length).fill(null), predPrice],
            borderColor: priceChange >= 0 ? '#10b981' : '#ef4444',
            backgroundColor: priceChange >= 0 ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
            borderDash: [5, 5],
            pointBackgroundColor: priceChange >= 0 ? '#10b981' : '#ef4444',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            fill: false,
            pointRadius: [...Array(historicalPrices.length).fill(0), 8], // static circle for predicted point
            pointStyle: [...Array(historicalPrices.length).fill('circle'), 'circle'],
            showLine: false,
            tension: 0.4,
            borderWidth: 3
          }
        ]
      });

      setLastUpdate(new Date().toLocaleString());
      setLoading(false);
    } catch (err) {
      console.error('Error fetching data:', err);
      const errorMsg = err.response?.data?.error || err.message || 'Unknown error';
      setError(`Failed to fetch data from ${API_URL}: ${errorMsg}`);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3600000); // Refresh every 1 hour
    return () => clearInterval(interval);
  }, []);

  // Chart.js annotation plugin config
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            size: 12,
            weight: 500
          }
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#ddd',
        borderWidth: 1,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += '₹' + context.parsed.y.toFixed(2);
            }
            return label;
          }
        }
      },
      annotation: {
        annotations: initialPredHigh.current && initialPredDate.current ? {
          predHighMarker: {
            type: 'point',
            xValue: initialPredDate.current,
            yValue: initialPredHigh.current,
            backgroundColor: '#f59e42',
            radius: 7,
            borderColor: '#f59e42',
            borderWidth: 2,
            label: {
              display: true,
              content: ['Predicted High'],
              position: 'top',
              color: '#f59e42',
              font: { weight: 'bold' }
            }
          },
          predHighLine: {
            type: 'line',
            xMin: initialPredDate.current,
            xMax: initialPredDate.current,
            yMin: 0,
            yMax: initialPredHigh.current,
            borderColor: '#f59e42',
            borderWidth: 2,
            borderDash: [4, 4],
            label: {
              display: false
            }
          }
        } : {}
      }
    },
    scales: {
      x: {
        display: true,
        grid: {
          display: false
        },
        ticks: {
          maxTicksLimit: 10,
          font: {
            size: 11
          }
        }
      },
      y: {
        display: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        },
        ticks: {
          callback: function(value) {
            return '₹' + value.toFixed(0);
          },
          font: {
            size: 11
          }
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3 text-muted">Fetching latest stock data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        <h5 className="alert-heading">Error</h5>
        <p>{error}</p>
        <hr />
        <button className="btn btn-outline-danger btn-sm" onClick={fetchData}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div>
      {/* Prediction Card */}
      {prediction && (
        <div className="row mb-4">
          <div className="col-md-12">
            <div className="card shadow-sm border-0">
              <div className="card-body">
                <div className="row align-items-center">
                  <div className="col-md-4 text-center border-end">
                    <small className="text-muted d-block mb-2">Current Price</small>
                    <h2 className="mb-0 fw-bold">₹{prediction.lastPrice.toFixed(2)}</h2>
                  </div>
                  <div className="col-md-4 text-center border-end">
                    <small className="text-muted d-block mb-2">Predicted Price ({prediction.date})</small>
                    <h2 className={`mb-0 fw-bold ${parseFloat(prediction.change) >= 0 ? 'text-success' : 'text-danger'}`}>
                      ₹{prediction.price.toFixed(2)}
                    </h2>
                    <div className="d-flex justify-content-center gap-3 mt-2 small text-muted">
                      <span>O: ₹{prediction.open?.toFixed(2)}</span>
                      <span>H: ₹{prediction.high?.toFixed(2)}</span>
                      <span>L: ₹{prediction.low?.toFixed(2)}</span>
                      <span>C: ₹{prediction.close?.toFixed(2)}</span>
                    </div>
                  </div>
                  <div className="col-md-4 text-center">
                    <small className="text-muted d-block mb-2">Expected Change</small>
                    <h3 className={`mb-1 fw-bold ${parseFloat(prediction.change) >= 0 ? 'text-success' : 'text-danger'}`}>
                      {parseFloat(prediction.change) >= 0 ? '+' : ''}₹{prediction.change}
                    </h3>
                    <span className={`badge ${parseFloat(prediction.change) >= 0 ? 'bg-success' : 'bg-danger'}`}>
                      {parseFloat(prediction.change) >= 0 ? '▲' : '▼'} {Math.abs(prediction.changePercent)}%
                    </span>
                    {prediction.volume && (
                      <div className="mt-2 text-muted small">Vol: {prediction.volume.toLocaleString()}</div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Chart */}
      <div className="card shadow-sm border-0">
        <div className="card-header bg-white border-0 pt-3">
          <div className="d-flex justify-content-between align-items-center">
            <h5 className="mb-0 fw-bold">Price Chart (Last 100 Days)</h5>
            <div>
              <small className="text-muted me-3">Last updated: {lastUpdate}</small>
              <button className="btn btn-sm btn-outline-primary" onClick={fetchData}>
                <i className="bi bi-arrow-clockwise"></i> Refresh
              </button>
            </div>
          </div>
        </div>
        <div className="card-body" style={{ height: '450px' }}>
          {chartData ? (
            <Line data={chartData} options={chartOptions} />
          ) : (
            <p className="text-center text-muted">No data available</p>
          )}
        </div>
      </div>

      {/* Info Footer */}
      <div className="mt-3 text-center">
        <small className="text-muted">
          This is a predictive model and may not reflect actual market conditions.  
        </small>
      </div>
    </div>
  );
};

export default StockChart;
