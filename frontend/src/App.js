import React, { useState } from "react";
import SourceSelector from "./components/SourceSelector";
import ClickHouseForm from "./components/ClickHouseForm";
import FlatFileForm from "./components/FlatFileForm";
import ColumnSelector from "./components/ColumnSelector";
import DataPreview from "./components/DataPreview";
import ProgressBar from "./components/ProgressBar";
import StatusDisplay from "./components/StatusDisplay";
import RecordCountDisplay from "./components/RecordCountDisplay";
import {
  previewClickHouse,
  ingestData,
  getProgress,
} from "./api";

function App() {
  const [source, setSource] = useState("clickhouse"); // default selection
  const [tables, setTables] = useState([]);
  const [columns, setColumns] = useState([]);
  const [selectedColumns, setSelectedColumns] = useState([]);
  const [previewData, setPreviewData] = useState([]);
  const [status, setStatus] = useState("");
  const [recordCount, setRecordCount] = useState(0);
  const [progress, setProgress] = useState(0);

  const handleColumnSelect = (selected) => {
    setSelectedColumns(selected);
  };

  // This example assumes you will add buttons and handlers for preview and ingestion
  const handlePreviewClickHouse = async () => {
    // You need to provide the connection parameters and selected table.
    // Here we simply pass dummy parameters; adjust with state as needed.
    const params = {
      host: "your_host",
      port: 9440,
      database: "your_db",
      user: "your_user",
      jwt_token: "your_jwt",
      table: tables[0], // for example, the first table
    };
    try {
      const response = await previewClickHouse(params);
      setPreviewData(response.data.preview);
    } catch (error) {
      setStatus("Error fetching preview from ClickHouse");
    }
  };

  const handleIngestion = async (direction) => {
    // Set up ingestion parameters based on the selected source
    let params = {};
    if (direction === "ch_to_flat") {
      // Example parameters for ClickHouse to Flat File
      params = {
        direction: "ch_to_flat",
        host: "your_host",
        port: 9440,
        database: "your_db",
        user: "your_user",
        jwt_token: "your_jwt",
        query: "SELECT * FROM " + tables[0],
        delimiter: ",",
        selected_columns: selectedColumns, // Pass selected columns
      };
    } else if (direction === "flat_to_ch") {
      // Example parameters for Flat File to ClickHouse
      params = {
        direction: "flat_to_ch",
        host: "your_host",
        port: 9440,
        database: "your_db",
        user: "your_user",
        jwt_token: "your_jwt",
        table: tables[0],
        delimiter: ",",
        selected_columns: selectedColumns, // Pass selected columns
      };
    }

    try {
      const response = await ingestData(params);
      setRecordCount(response.data.ingested_records);
      setStatus("Ingestion Completed");
    } catch (error) {
      setStatus("Error during ingestion");
    }
  };

  const checkProgress = async () => {
    try {
      const response = await getProgress();
      setProgress(response.data.progress);
    } catch (error) {
      console.error("Error checking progress", error);
    }
  };

  return (
    <div className="App">
      <h1>Bidirectional Data Ingestion Tool</h1>
      <SourceSelector source={source} setSource={setSource} />
      {source === "clickhouse" ? (
        <ClickHouseForm onTablesFetched={setTables} onColumnsFetched={setColumns} columns={columns} onColumnSelect={handleColumnSelect} />
      ) : (
        <FlatFileForm onColumnsFetched={setColumns} columns={columns} onColumnSelect={handleColumnSelect}/>
      )}
      <button onClick={handlePreviewClickHouse}>Preview Data</button>
      <DataPreview previewData={previewData} />
      <button onClick={() => handleIngestion("ch_to_flat")}>
        Start Ingestion
      </button>
      <StatusDisplay status={status} />
      <RecordCountDisplay count={recordCount} />
      <ProgressBar progress={progress} />
      <button onClick={checkProgress}>Check Progress</button>
    </div>
  );
}

export default App;
