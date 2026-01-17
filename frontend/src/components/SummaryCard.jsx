import React from 'react';
import './SummaryCard.css';

function SummaryCard({ analysis }) {
  if (!analysis) {
    return <div className="summary-empty">No analysis data available</div>;
  }

  const { financial_summary, numeric_columns } = analysis;

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  return (
    <div className="summary-card">
      {financial_summary && (
        <div className="summary-grid">
          <div className="summary-item income">
            <div className="summary-icon">💰</div>
            <div className="summary-details">
              <span className="summary-label">Total Income</span>
              <span className="summary-value">
                {formatCurrency(financial_summary.total_income)}
              </span>
            </div>
          </div>

          <div className="summary-item expense">
            <div className="summary-icon">💸</div>
            <div className="summary-details">
              <span className="summary-label">Total Expenses</span>
              <span className="summary-value">
                {formatCurrency(financial_summary.total_expenses)}
              </span>
            </div>
          </div>

          <div className={`summary-item balance ${financial_summary.net_balance >= 0 ? 'positive' : 'negative'}`}>
            <div className="summary-icon">{financial_summary.net_balance >= 0 ? '📈' : '📉'}</div>
            <div className="summary-details">
              <span className="summary-label">Net Balance</span>
              <span className="summary-value">
                {formatCurrency(financial_summary.net_balance)}
              </span>
            </div>
          </div>
        </div>
      )}

      {numeric_columns && numeric_columns.length > 0 && (
        <div className="stats-grid">
          {numeric_columns.slice(0, 4).map((col, idx) => (
            <div key={idx} className="stat-item">
              <span className="stat-label">{col.column}</span>
              <div className="stat-values">
                <div className="stat-row">
                  <span className="stat-key">Sum:</span>
                  <span className="stat-val">{formatCurrency(col.sum)}</span>
                </div>
                <div className="stat-row">
                  <span className="stat-key">Avg:</span>
                  <span className="stat-val">{formatCurrency(col.mean)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SummaryCard;
