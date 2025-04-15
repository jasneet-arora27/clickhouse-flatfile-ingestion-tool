import React from 'react';

function DataPreview({ previewData }) {
  if (!previewData || previewData.length === 0) {
    return <p>No preview data available.</p>;
  }
  return (
    <table border="1">
      <thead>
        <tr>
          {Object.keys(previewData[0]).map((col, index) => (
            <th key={index}>{col}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {previewData.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {Object.values(row).map((value, i) => (
              <td key={i}>{value}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default DataPreview;

