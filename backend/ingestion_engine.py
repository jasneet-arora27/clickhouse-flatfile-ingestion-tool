import pandas as pd

def ingest_clickhouse_to_flatfile(client, query: str, output_file: str, delimiter: str = ','):
    """
    Fetches data from ClickHouse and writes it to a CSV file.
    """
    try:
        result = client.query(query)
        data = result.result_set
        columns = result.column_names
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(output_file, sep=delimiter, index=False)
        return len(df)
    except Exception as e:
        print(f"Error during ingestion (ClickHouse to FlatFile): {e}")
        return 0

def ingest_flatfile_to_clickhouse(client, file_path: str, table: str, delimiter: str = ','):
    """
    Reads data from a CSV file and inserts it into a ClickHouse table.
    """
    try:
        df = pd.read_csv(file_path, delimiter=delimiter)
        data = [tuple(x) for x in df.values]
        columns = ", ".join(df.columns)
        insert_query = f"INSERT INTO {table} ({columns}) VALUES"
        # Adjust client.insert to match your client library's API
        client.insert(insert_query, data)
        return len(df)
    except Exception as e:
        print(f"Error during ingestion (FlatFile to ClickHouse): {e}")
        return 0
