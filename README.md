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

## Setup Instructions

1.  Clone the repository.
2.  Install the backend dependencies: `cd backend && pip install -r requirements.txt`
3.  Install the frontend dependencies: `cd frontend && npm install`

## Configuration

1.  Configure the ClickHouse connection parameters in the frontend UI.
2.  Configure the Flat File source parameters in the frontend UI.

## Run Instructions

1.  Start the backend: `cd backend && python main.py`
2.  Start the frontend: `cd frontend && npm start`
3.  Open the application in your browser.

## Technical Details

- **Backend:** Implemented in Python.
- **Frontend:** Implemented using React.
- **ClickHouse Instance:** Utilizes a local (Docker) ClickHouse instance.
- **JWT Handling:** Uses libraries to manage JWTs, primarily passing the token to the ClickHouse client.
