import React, { useState } from 'react';
import { connectFlatFile } from '../api';

function FlatFileForm({ onColumnsFetched }) {
  const [delimiter, setDelimiter] = useState(',');
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!file) {
      setError('Please select a file.');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('delimiter', delimiter);
    try {
      const response = await connectFlatFile(formData);
      onColumnsFetched(response.data.columns);
    } catch (err) {
      console.error(err);
      setError('Failed to connect to Flat File.');
    }
  };

  return (
    <div>
      <h3>Flat File Connection</h3>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".csv" onChange={handleFileChange} required />
        <input type="text" placeholder="Delimiter" value={delimiter} onChange={(e) => setDelimiter(e.target.value)} required />
        <button type="submit">Load File</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default FlatFileForm;

