import React from 'react';

function SourceSelector({ source, setSource }) {
  return (
    <div>
      <h3>Select Data Source</h3>
      <label>
        <input
          type="radio"
          name="dataSource"
          value="clickhouse"
          checked={source === 'clickhouse'}
          onChange={() => setSource('clickhouse')}
        />
        ClickHouse
      </label>
      <label>
        <input
          type="radio"
          name="dataSource"
          value="flatfile"
          checked={source === 'flatfile'}
          onChange={() => setSource('flatfile')}
        />
        Flat File
      </label>
    </div>
  );
}

export default SourceSelector;
