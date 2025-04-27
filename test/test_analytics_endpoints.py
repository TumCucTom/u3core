import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from python_server.endpoints.analytics_endpoints import register_analytics_endpoints

@pytest.fixture
def client():
    app = Flask(__name__)
    dummy_db_config = {"host": "localhost", "user": "test", "password": "test", "database": "test_db"}

    with patch('python_server.endpoints.analytics_endpoints.get_db_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        mock_get_conn.return_value = mock_conn

        register_analytics_endpoints(app, dummy_db_config)

        app.config['TESTING'] = True
        yield app.test_client(), mock_cursor  # Yield both client and mock_cursor to control results

def test_get_anomalies_by_month(client):
    client, mock_cursor = client

    # Simulate database returning two months with anomalies
    mock_cursor.fetchall.return_value = [
        ("01", 5),  # January
        ("03", 7),  # March
    ]

    response = client.get('/api/anomalies-by-month')
    assert response.status_code == 200

    data = response.get_json()
    # Expect list of 12 months
    assert len(data) == 12
    assert data[0] == 5   # January
    assert data[2] == 7   # March
    assert data[1] == 0   # February
    assert data[11] == 0  # December

def test_get_anomalies_by_type(client):
    client, mock_cursor = client

    # Simulate database returning hazard types
    mock_cursor.fetchall.return_value = [
        ("fire", 10),
        ("smoke", 4),
    ]

    response = client.get('/api/anomalies-by-type')
    assert response.status_code == 200

    data = response.get_json()
    assert data["types"] == ["fire", "smoke"]
    assert data["counts"] == [10, 4]
