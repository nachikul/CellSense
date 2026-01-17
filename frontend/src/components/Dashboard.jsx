import React, { useState, useMemo } from 'react';
import GridLayout from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import SummaryCard from './SummaryCard';
import ChartWidget from './ChartWidget';
import DataTable from './DataTable';
import './Dashboard.css';

function Dashboard({ data }) {
  const [layouts, setLayouts] = useState([
    { i: 'summary', x: 0, y: 0, w: 12, h: 2, minW: 6, minH: 2 },
    { i: 'chart1', x: 0, y: 2, w: 6, h: 4, minW: 3, minH: 3 },
    { i: 'chart2', x: 6, y: 2, w: 6, h: 4, minW: 3, minH: 3 },
    { i: 'table', x: 0, y: 6, w: 12, h: 5, minW: 6, minH: 4 },
  ]);

  const [editMode, setEditMode] = useState(false);

  const analysis = useMemo(() => {
    if (!data?.analysis) return null;
    return data.analysis;
  }, [data]);

  const handleLayoutChange = (newLayout) => {
    setLayouts(newLayout);
  };

  // Prepare chart data
  const prepareChartData = () => {
    if (!data?.data || data.data.length === 0) return [];
    
    // Try to find numeric columns for visualization
    const numericData = [];
    const firstRow = data.data[0];
    const keys = Object.keys(firstRow);
    
    // Group by category if available
    const categoryKey = keys.find(k => k.toLowerCase().includes('category'));
    const amountKey = keys.find(k => 
      k.toLowerCase().includes('amount') || 
      k.toLowerCase().includes('expense') ||
      k.toLowerCase().includes('income')
    );

    if (categoryKey && amountKey) {
      const grouped = {};
      data.data.forEach(row => {
        const category = row[categoryKey] || 'Other';
        const amount = parseFloat(row[amountKey]) || 0;
        grouped[category] = (grouped[category] || 0) + amount;
      });

      return Object.entries(grouped).map(([name, value]) => ({
        name,
        value: Math.abs(value)
      }));
    }

    return [];
  };

  const chartData = useMemo(() => prepareChartData(), [data]);

  return (
    <div className="dashboard">
      <div className="dashboard-controls">
        <button 
          className={`btn-control ${editMode ? 'active' : ''}`}
          onClick={() => setEditMode(!editMode)}
        >
          {editMode ? '🔒 Lock Layout' : '✏️ Edit Layout'}
        </button>
        <span className="help-text">
          {editMode ? 'Drag and resize widgets to customize your dashboard' : 'Click Edit Layout to customize'}
        </span>
      </div>

      <GridLayout
        className="grid-layout"
        layout={layouts}
        cols={12}
        rowHeight={60}
        width={typeof window !== 'undefined' ? Math.min(window.innerWidth - 100, 1360) : 1360}
        onLayoutChange={handleLayoutChange}
        isDraggable={editMode}
        isResizable={editMode}
        draggableHandle=".widget-header"
      >
        <div key="summary" className="widget">
          <div className="widget-header">
            <h3>📊 Financial Summary</h3>
          </div>
          <div className="widget-content">
            <SummaryCard analysis={analysis} />
          </div>
        </div>

        <div key="chart1" className="widget">
          <div className="widget-header">
            <h3>📈 Expenses by Category</h3>
          </div>
          <div className="widget-content">
            <ChartWidget data={chartData} type="pie" />
          </div>
        </div>

        <div key="chart2" className="widget">
          <div className="widget-header">
            <h3>📊 Category Breakdown</h3>
          </div>
          <div className="widget-content">
            <ChartWidget data={chartData} type="bar" />
          </div>
        </div>

        <div key="table" className="widget">
          <div className="widget-header">
            <h3>📋 Transaction Details</h3>
          </div>
          <div className="widget-content">
            <DataTable data={data.data} columns={data.columns} />
          </div>
        </div>
      </GridLayout>
    </div>
  );
}

export default Dashboard;
