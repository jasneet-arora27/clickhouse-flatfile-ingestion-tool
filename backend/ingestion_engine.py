import pandas as pd
from progress_tracker import update_progress, reset_progress

def ingest_clickhouse_to_flatfile(client, query: str, output_file: str, delimiter: str = ',', selected_columns: list = None):
    """
    Fetches data from ClickHouse and writes it to a CSV file.
    """
    try:
        reset_progress()
        result = client.query(query)
        data = result.result_set
        columns = result.column_names
        df = pd.DataFrame(data, columns=columns)
        if selected_columns:
            df = df[selected_columns]
        try:
            df.to_csv(output_file, sep=delimiter, index=False)
            update_progress(len(df))
            return len(df)
        except Exception as e:
            print(f"Error writing to flat file: {e}")
            return 0
    except Exception as e:
        print(f"Error during ingestion (ClickHouse to FlatFile): {e}")
        return 0

def ingest_flatfile_to_clickhouse(client, file_path: str, table: str, delimiter: str = ',', selected_columns: list = None):
    """
    Reads data from a CSV file and inserts it into a ClickHouse table.
    """
    try:
        df = pd.read_csv(file_path, delimiter=delimiter)
        if selected_columns:
            df = df[selected_columns]
        data = [tuple(x) for x in df.values]
        columns = ", ".join(df.columns)
        insert_query = f"INSERT INTO {table} ({columns}) VALUES"
        # Adjust client.insert to match your client library's API
        try:
            client.insert(insert_query, data)
            update_progress(len(df))
            return len(df)
        except Exception as e:
            print(f"Error inserting data into ClickHouse: {e}")
            return 0
    except Exception as e:
        print(f"Error during ingestion (FlatFile to ClickHouse): {e}")
        return 0
