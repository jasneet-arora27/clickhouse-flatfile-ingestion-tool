import React, { useState } from 'react';
import { connectClickHouse, fetchClickHouseColumns } from '../api';
import ColumnSelector from './ColumnSelector';

function ClickHouseForm({ onTablesFetched, onColumnsFetched, columns, onColumnSelect }) {
  const [host, setHost] = useState('');
  const [port, setPort] = useState(9440);
  const [database, setDatabase] = useState('');
  const [user, setUser] = useState('');
  const [jwt, setJwt] = useState('');
  const [error, setError] = useState('');
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');
  const [tableColumns, setTableColumns] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await connectClickHouse({
        host,
        port,
        database,
        user,
        jwt_token: jwt,
      });
      setTables(response.data.tables);
      onTablesFetched(response.data.tables);
    } catch (err) {
      console.error(err);
      setError('Failed to connect to ClickHouse.');
    }
  };

  const handleTableSelect = async (e) => {
    setSelectedTable(e.target.value);
    try {
      const response = await fetchClickHouseColumns({
        host,
        port,
        database,
        user,
        jwt_token: jwt,
        table: e.target.value,
      });
      setTableColumns(response.data.columns);
      onColumnsFetched(response.data.columns);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch columns from ClickHouse.');
    }
  };

  return (
    <div>
      <h3>ClickHouse Connection</h3>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Host" value={host} onChange={(e) => setHost(e.target.value)} required />
        <input type="number" placeholder="Port" value={port} onChange={(e) => setPort(e.target.value)} required />
        <input type="text" placeholder="Database" value={database} onChange={(e) => setDatabase(e.target.value)} required />
        <input type="text" placeholder="User" value={user} onChange={(e) => setUser(e.target.value)} required />
        <input type="password" placeholder="JWT Token" value={jwt} onChange={(e) => setJwt(e.target.value)} />
        <button type="submit">Connect</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {tables.length > 0 && (
        <div>
          <label>Select Table:</label>
          <select value={selectedTable} onChange={handleTableSelect}>
            <option value="">-- Select Table --</option>
            {tables.map((table) => (
              <option key={table} value={table}>{table}</option>
            ))}
          </select>
        </div>
      )}
      {selectedTable && <ColumnSelector columns={tableColumns} onColumnSelect={onColumnSelect} />}
    </div>
  );
}

export default ClickHouseForm;
