def preview_clickhouse_table(client, table, limit=100):
    """
    Retrieves the first 'limit' rows from the specified ClickHouse table.
    """
    try:
        query = f"SELECT * FROM {table} LIMIT {limit}"
        result = client.query(query)
        columns = result.column_names
        data = result.result_set
        preview = [dict(zip(columns, row)) for row in data]
        return preview
    except Exception as e:
        print(f"Error previewing ClickHouse table: {e}")
        return []
