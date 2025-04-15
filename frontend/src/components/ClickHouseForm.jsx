import React, { useState } from 'react';
import { connectClickHouse } from '../api';

function ClickHouseForm({ onTablesFetched }) {
  const [host, setHost] = useState('');
  const [port, setPort] = useState(9440);
  const [database, setDatabase] = useState('');
  const [user, setUser] = useState('');
  const [jwt, setJwt] = useState('');
  const [error, setError] = useState('');
  
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
      onTablesFetched(response.data.tables);
    } catch (err) {
      console.error(err);
      setError('Failed to connect to ClickHouse.');
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
        <input type="password" placeholder="JWT Token" value={jwt} onChange={(e) => setJwt(e.target.value)} required />
        <button type="submit">Connect</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default ClickHouseForm;
