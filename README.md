# Bidirectional ClickHouse & Flat File Data Ingestion Tool

## Overview

This web application facilitates seamless data ingestion between ClickHouse and Flat Files, providing a user-friendly interface for configuring and executing bidirectional data transfers. It supports JWT token-based authentication for ClickHouse, allows users to select specific columns for ingestion, and reports the total number of records processed upon completion.

## Features

- **Bidirectional Data Flow:** Enables data transfer from ClickHouse to Flat Files and vice versa.
- **Source Selection:** Allows users to choose between ClickHouse and Flat File as the data source.
- **ClickHouse Connection:**
  - Provides a UI for configuring connection parameters such as Host, Port, Database, User, and JWT Token.
  - Authenticates using the provided JWT token via a compatible ClickHouse client library (e.g., Python).
- **Flat File Integration:**
  - Offers a UI for specifying the local Flat File name and delimiters.
  - Utilizes standard IO libraries for file handling.
- **Schema Discovery & Column Selection:**
  - Connects to the data source and fetches the list of available tables (ClickHouse) or the schema of the Flat File data.
  - Displays column names in the UI with selection controls (e.g., checkboxes) for column selection.
- **Efficient Ingestion Process:**
  - Executes data transfer based on user selections.
  - Implements efficient data handling techniques such as batching or streaming.
- **Completion Reporting:** Displays the total count of ingested records upon success.
- **Error Handling:** Implements robust error handling for connection, authentication, query, and ingestion, providing user-friendly messages.

## User Interface

The UI provides the following elements:

- Clear source/target selection.
- Input fields for all necessary connection parameters (ClickHouse source/target, Flat File).
- Mechanism to list tables (ClickHouse) or identify Flat File data source.
- Column list display with selection controls.
- Action buttons (e.g., "Connect", "Load Columns", "Preview", "Start Ingestion").
- Status display area (Connecting, Fetching, Ingesting, Completed, Error).
- Result display area (record count or error message).

## Enhancements

- Multi-Table Join (ClickHouse Source):

  - Allows selection of multiple ClickHouse tables.
  - Provides a UI element to input JOIN key(s)/conditions.
  - Constructs and executes the JOIN query for ingestion in the backend.

- Progress Bar: Visual indicator of ingestion progress (can be approximate).
- Data Preview: Button to display the first 100 records of the selected source data (with selected columns) in the UI before full ingestion.

## Technical Details

- **Backend:** Implemented in Python.
- **Frontend:** Implemented using React.
- **ClickHouse Instance:** Utilizes a local (Docker) ClickHouse instance.
- **JWT Handling:** Uses libraries to manage JWTs, primarily passing the token to the ClickHouse client.
