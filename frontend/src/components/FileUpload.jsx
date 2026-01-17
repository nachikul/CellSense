import React, { useCallback, useState } from 'react';
import './FileUpload.css';

function FileUpload({ onFileUpload, loading, error }) {
  const [customKeywords, setCustomKeywords] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && (file.name.endsWith('.xlsx') || file.name.endsWith('.xls'))) {
      onFileUpload(file, customKeywords);
    } else {
      alert('Please upload an Excel file (.xlsx or .xls)');
    }
  }, [onFileUpload, customKeywords]);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
  }, []);

  const handleFileChange = useCallback((e) => {
    const file = e.target.files[0];
    if (file) {
      onFileUpload(file, customKeywords);
    }
  }, [onFileUpload, customKeywords]);

  return (
    <div className="file-upload">
      <div 
        className="upload-area"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        {loading ? (
          <div className="loading">
            <div className="spinner"></div>
            <p>Processing your file...</p>
          </div>
        ) : (
          <>
            <div className="upload-icon">📁</div>
            <h3>Upload Your Financial Excel Sheet</h3>
            <p>Drag and drop your Excel file here, or click to browse</p>
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileChange}
              className="file-input"
              id="file-input"
            />
            <label htmlFor="file-input" className="btn-primary">
              Choose File
            </label>
            <p className="file-hint">Supported formats: .xlsx, .xls</p>
          </>
        )}
      </div>
      
      {error && (
        <div className="error-message">
          <p>❌ {error}</p>
        </div>
      )}

      <div className="advanced-options">
        <button 
          className="toggle-advanced"
          onClick={() => setShowAdvanced(!showAdvanced)}
        >
          {showAdvanced ? '▼' : '▶'} Advanced Options
        </button>
        
        {showAdvanced && (
          <div className="keywords-section">
            <label htmlFor="custom-keywords">
              <strong>Custom Financial Keywords</strong> (optional)
            </label>
            <input
              type="text"
              id="custom-keywords"
              className="keywords-input"
              placeholder="e.g., Mutual Funds, Savings, Loans, Fixed Deposits, Stocks, ESOPS"
              value={customKeywords}
              onChange={(e) => setCustomKeywords(e.target.value)}
            />
            <p className="keywords-hint">
              💡 Enter comma-separated keywords to detect in your financial data. 
              Default keywords include: income, expense, savings, investments, etc.
            </p>
          </div>
        )}
      </div>

      <div className="info-section">
        <h4>📋 Sample Excel Format</h4>
        <p>Your Excel sheet should contain financial data with columns like:</p>
        <ul>
          <li><strong>Date</strong> - Transaction date</li>
          <li><strong>Category</strong> - Expense/Income category</li>
          <li><strong>Description</strong> - Transaction description</li>
          <li><strong>Amount</strong> - Transaction amount</li>
          <li><strong>Type</strong> - Income or Expense</li>
        </ul>
        <p className="supported-keywords">
          <strong>Supported Financial Terms:</strong> Mutual Funds, Savings, Loans, Liabilities, 
          Provident Fund, Debt, Fixed Deposits, Recurring Deposits, Stocks, ESOPS, Insurance, 
          EMI, Credit Card, Mortgage, Salary, Bonus, Dividends, and more.
        </p>
      </div>
    </div>
  );
}

export default FileUpload;
