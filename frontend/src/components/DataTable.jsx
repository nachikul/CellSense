import React, { useState, useEffect } from 'react';
import './DataTable.css';

function DataTable({ data, columns }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [editingCell, setEditingCell] = useState(null);
  const [tableData, setTableData] = useState(data);
  const itemsPerPage = 10;

  useEffect(() => {
    setTableData(data);
  }, [data]);

  // Filter data based on search
  const filteredData = (tableData || []).filter(row =>
    Object.values(row).some(value =>
      String(value).toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  // Pagination
  const totalPages = Math.ceil(filteredData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedData = filteredData.slice(startIndex, startIndex + itemsPerPage);

  const handleCellEdit = (rowIndex, column, value) => {
    const actualIndex = startIndex + rowIndex;
    const newData = [...tableData];
    newData[actualIndex] = { ...newData[actualIndex], [column]: value };
    setTableData(newData);
    setEditingCell(null);
  };

  const handleCellDoubleClick = (rowIndex, column) => {
    setEditingCell({ row: rowIndex, column });
  };

  return (
    <div className="data-table">
      <div className="table-controls">
        <input
          type="text"
          placeholder="🔍 Search transactions..."
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setCurrentPage(1);
          }}
          className="search-input"
        />
        <span className="record-count">
          {filteredData.length} records
        </span>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              {columns.map((column, idx) => (
                <th key={idx}>{column}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((row, rowIdx) => (
              <tr key={rowIdx}>
                {columns.map((column, colIdx) => {
                  const isEditing = editingCell?.row === rowIdx && editingCell?.column === column;
                  return (
                    <td
                      key={colIdx}
                      onDoubleClick={() => handleCellDoubleClick(rowIdx, column)}
                      className={isEditing ? 'editing' : ''}
                    >
                      {isEditing ? (
                        <input
                          type="text"
                          defaultValue={row[column] || ''}
                          autoFocus
                          onBlur={(e) => handleCellEdit(rowIdx, column, e.target.value)}
                          onKeyPress={(e) => {
                            if (e.key === 'Enter') {
                              handleCellEdit(rowIdx, column, e.target.value);
                            }
                          }}
                          className="cell-input"
                        />
                      ) : (
                        <span>{row[column] !== null && row[column] !== undefined ? String(row[column]) : '-'}</span>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className="page-btn"
          >
            ← Previous
          </button>
          <span className="page-info">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className="page-btn"
          >
            Next →
          </button>
        </div>
      )}

      <div className="table-hint">
        💡 Double-click any cell to edit its value
      </div>
    </div>
  );
}

export default DataTable;
