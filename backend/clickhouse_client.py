import requests
from clickhouse_connect import get_client

def create_clickhouse_client(host: str, port: int, database: str, user: str, jwt_token: str):
    """
    Creates and returns a ClickHouse client connection.
    """
    try:
        headers = {'Authorization': f'Bearer {jwt_token}'}
        client = get_client(
            host=host,
            port=port,
            database=database,
            username=user,
            headers=headers
        )
        return client
    except Exception as e:
        print(f"Error creating ClickHouse client: {e}")
        return None

def get_tables(client):
    """
    Fetch all tables from the connected ClickHouse database.
    """
    try:
        query = "SHOW TABLES"
        result = client.query(query)
        tables = [row[0] for row in result.result_set]
        return tables
    except Exception as e:
        print(f"Error fetching tables: {e}")
        return []
