import React, { useState, useCallback } from 'react';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import FileUpload from './components/FileUpload';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = useCallback(async (file, customKeywords = '') => {
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);
    if (customKeywords) {
      formData.append('custom_keywords', customKeywords);
    }

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setData(response.data);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error uploading file');
      setLoading(false);
    }
  }, []);

  const handleReset = () => {
    setData(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>📊 CellSense</h1>
        <p>Your Personal Financial Dashboard</p>
      </header>

      {!data ? (
        <div className="upload-section">
          <FileUpload 
            onFileUpload={handleFileUpload} 
            loading={loading}
            error={error}
          />
        </div>
      ) : (
        <div className="dashboard-section">
          <div className="dashboard-header">
            <div>
              <h2>{data.filename}</h2>
              <p>{data.row_count} records loaded</p>
            </div>
            <button onClick={handleReset} className="btn-secondary">
              Upload New File
            </button>
          </div>
          <Dashboard data={data} />
        </div>
      )}
    </div>
  );
}

export default App;
