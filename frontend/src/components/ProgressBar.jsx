import React from 'react';

function ProgressBar({ progress }) {
  return (
    <div style={{ border: '1px solid #000', width: '100%', marginTop: '10px' }}>
      <div style={{ width: `${progress}%`, background: 'lightblue', height: '20px' }}>
        {progress}%
      </div>
    </div>
  );
}

export default ProgressBar;

