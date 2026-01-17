import React, { useCallback } from 'react';
import './FileUpload.css';

function FileUpload({ onFileUpload, loading, error }) {
  const handleDrop = useCallback((e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && (file.name.endsWith('.xlsx') || file.name.endsWith('.xls'))) {
      onFileUpload(file);
    } else {
      alert('Please upload an Excel file (.xlsx or .xls)');
    }
  }, [onFileUpload]);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
  }, []);

  const handleFileChange = useCallback((e) => {
    const file = e.target.files[0];
    if (file) {
      onFileUpload(file);
    }
  }, [onFileUpload]);

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
      </div>
    </div>
  );
}

export default FileUpload;
