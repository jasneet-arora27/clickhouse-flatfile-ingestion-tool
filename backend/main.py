from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os

# Import helper modules
from clickhouse_client import create_clickhouse_client, get_tables
from flatfile_handler import read_flatfile_schema, preview_data
from ingestion_engine import ingest_clickhouse_to_flatfile, ingest_flatfile_to_clickhouse
from preview_utils import preview_clickhouse_table
from progress_tracker import get_progress

app = FastAPI(
    title="ClickHouse-FlatFile Ingestion Tool",
    description="Backend API for Bidirectional Data Ingestion",
    version="1.0.0"
)

# Allow CORS for the frontend
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve a favicon if available
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

@app.get("/favicon.ico")
def favicon():
    file_path = os.path.join(static_dir, "favicon.ico")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Favicon not found")

# Global exception handler to catch unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )

# Health-check endpoint
@app.get("/")
async def root():
    return {"message": "Backend is running!"}

# ----------------------------
# ClickHouse Connection Endpoint
# ----------------------------
class ClickHouseConnectionParams(BaseModel):
    host: str
    port: int
    database: str
    user: str
    jwt_token: str

@app.post("/connect/clickhouse")
async def connect_clickhouse(params: ClickHouseConnectionParams):
    try:
        client = create_clickhouse_client(
            host=params.host,
            port=params.port,
            database=params.database,
            user=params.user,
            jwt_token=params.jwt_token
        )
        if client is None:
            raise ValueError("ClickHouse client creation failed")
        tables = get_tables(client)
        return {"tables": tables}
    except Exception as e:
        print(f"Error in /connect/clickhouse: {e}")
        raise HTTPException(status_code=400, detail=f"Error connecting to ClickHouse: {str(e)}")

# ----------------------------
# Flat File Connection Endpoint
# ----------------------------
@app.post("/connect/flatfile")
async def connect_flatfile(file: UploadFile = File(...), delimiter: str = Form(',')):
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        schema = read_flatfile_schema(temp_file_path, delimiter)
        os.remove(temp_file_path)
        if not schema:
            raise ValueError("Failed to read flat file schema")
        return {"columns": schema}
    except Exception as e:
        print(f"Error in /connect/flatfile: {e}")
        raise HTTPException(status_code=400, detail=f"Error connecting to flat file: {str(e)}")

# ----------------------------
# Fetch ClickHouse Columns Endpoint
# ----------------------------
class FetchColumnsClickHouseParams(BaseModel):
    host: str
    port: int
    database: str
    user: str
    jwt_token: str
    table: str

@app.post("/fetch-columns/clickhouse")
async def fetch_clickhouse_columns(params: FetchColumnsClickHouseParams):
    try:
        client = create_clickhouse_client(
            host=params.host,
            port=params.port,
            database=params.database,
            user=params.user,
            jwt_token=params.jwt_token
        )
        if client is None:
            raise ValueError("Failed to create ClickHouse client")
        query = f"DESCRIBE TABLE {params.table}"
        result = client.query(query)
        columns = [row[0] for row in result.result_set]
        return {"columns": columns}
    except Exception as e:
        print(f"Error in /fetch-columns/clickhouse: {e}")
        raise HTTPException(status_code=400, detail=f"Error fetching columns: {str(e)}")

# ----------------------------
# Preview Endpoints
# ----------------------------
class PreviewClickHouseParams(BaseModel):
    host: str
    port: int
    database: str
    user: str
    jwt_token: str
    table: str

@app.post("/preview/clickhouse")
async def preview_clickhouse(params: PreviewClickHouseParams):
    try:
        client = create_clickhouse_client(
            host=params.host,
            port=params.port,
            database=params.database,
            user=params.user,
            jwt_token=params.jwt_token
        )
        if client is None:
            raise ValueError("Failed to create ClickHouse client")
        preview = preview_clickhouse_table(client, params.table, limit=100)
        return {"preview": preview}
    except Exception as e:
        print(f"Error in /preview/clickhouse: {e}")
        raise HTTPException(status_code=400, detail=f"Error previewing ClickHouse table: {str(e)}")

@app.post("/preview/flatfile")
async def preview_flatfile(file: UploadFile = File(...), delimiter: str = Form(',')):
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        preview = preview_data(temp_file_path, delimiter, rows=100)
        os.remove(temp_file_path)
        if not preview:
            raise ValueError("Failed to preview flat file data")
        return {"preview": preview}
    except Exception as e:
        print(f"Error in /preview/flatfile: {e}")
        raise HTTPException(status_code=400, detail=f"Error previewing flat file data: {str(e)}")

# ----------------------------
# Data Ingestion Endpoint
# ----------------------------
class IngestParams(BaseModel):
    direction: str  # "ch_to_flat" or "flat_to_ch"
    # ClickHouse connection parameters (for both directions)
    host: str = None
    port: int = None
    database: str = None
    user: str = None
    jwt_token: str = None
    # For ClickHouse → Flat File
    query: str = None
    # For Flat File → ClickHouse
    table: str = None
    file_path: str = None  # local CSV path (for simplicity)
    delimiter: str = ','

@app.post("/ingest")
async def ingest_data(params: IngestParams):
    try:
        if params.direction == "ch_to_flat":
            required = [params.host, params.port, params.database, params.user, params.jwt_token, params.query]
            if not all(required):
                raise ValueError("Missing parameters for ClickHouse to Flat File ingestion")
            client = create_clickhouse_client(params.host, params.port, params.database, params.user, params.jwt_token)
            if client is None:
                raise ValueError("Failed to connect to ClickHouse")
            output_file = "output.csv"
            count = ingest_clickhouse_to_flatfile(client, params.query, output_file, params.delimiter)
            return {"ingested_records": count, "output_file": output_file}
        elif params.direction == "flat_to_ch":
            required = [params.host, params.port, params.database, params.user, params.jwt_token, params.table, params.file_path]
            if not all(required):
                raise ValueError("Missing parameters for Flat File to ClickHouse ingestion")
            client = create_clickhouse_client(params.host, params.port, params.database, params.user, params.jwt_token)
            if client is None:
                raise ValueError("Failed to connect to ClickHouse")
            count = ingest_flatfile_to_clickhouse(client, params.file_path, params.table, params.delimiter)
            return {"ingested_records": count}
        else:
            raise ValueError("Invalid ingestion direction. Use 'ch_to_flat' or 'flat_to_ch'.")
    except Exception as e:
        print(f"Error in /ingest: {e}")
        raise HTTPException(status_code=400, detail=f"Error during ingestion: {str(e)}")

# ----------------------------
# Progress Tracking Endpoint
# ----------------------------
@app.get("/progress")
async def progress():
    try:
        progress_value = get_progress()
        return {"progress": progress_value}
    except Exception as e:
        print(f"Error in /progress: {e}")
        raise HTTPException(status_code=400, detail=f"Error retrieving progress: {str(e)}")
