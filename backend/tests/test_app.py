from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Backend is running!"}

# Example error handling test for ClickHouse connection with missing parameters.
def test_connect_clickhouse_error():
    response = client.post(
        "/connect/clickhouse",
        json={"host": "", "port": 9440, "database": "test", "user": "test"}
    )
    assert response.status_code == 400
    assert "Error connecting to ClickHouse" in response.json()["detail"]
