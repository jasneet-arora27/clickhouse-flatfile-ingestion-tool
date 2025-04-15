import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // adjust if needed

export const connectClickHouse = (params) =>
  axios.post(`${API_BASE_URL}/connect/clickhouse`, params);

export const connectFlatFile = (formData) =>
  axios.post(`${API_BASE_URL}/connect/flatfile`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

export const fetchClickHouseColumns = (params) =>
  axios.post(`${API_BASE_URL}/fetch-columns/clickhouse`, params);

export const previewClickHouse = (params) =>
  axios.post(`${API_BASE_URL}/preview/clickhouse`, params);

export const previewFlatFile = (formData) =>
  axios.post(`${API_BASE_URL}/preview/flatfile`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

export const ingestData = (params) =>
  axios.post(`${API_BASE_URL}/ingest`, params);

export const getProgress = () => axios.get(`${API_BASE_URL}/progress`);
