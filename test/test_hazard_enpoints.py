import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from python_server.endpoints.hazard_endpoints import register_hazard_endpoints

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True

    dummy_db_config = {"host": "localhost", "user": "test", "password": "test", "database": "test_db"}

    with patch('python_server.endpoints.hazard_endpoints.get_db_connection') as mock_get_conn, \
            patch('python_server.endpoints.hazard_endpoints.get_count_from_table', return_value=("mock_count", 200)):

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        mock_get_conn.return_value = mock_conn

        register_hazard_endpoints(app, dummy_db_config)

        yield app.test_client(), mock_cursor

def test_add_hazard_success(client):
    client, mock_cursor = client

    # Simulate camera exists
    mock_cursor.fetchone.side_effect = [
        ("Test Camera",),  # Camera name fetch
        None  # No existing log
    ]

    payload = {
        "timestamp": "2024-04-27 15:30:00",
        "type": "fire",
        "cameraAddress": "rtsp://example.com/stream"
    }

    response = client.post('/api/add-hazard', json=payload)

    assert response.status_code == 201
    assert "message" in response.get_json()

def test_add_hazard_missing_fields(client):
    client, mock_cursor = client

    payload = {
        "timestamp": "2024-04-27 15:30:00",
        "cameraAddress": "rtsp://example.com/stream"
    }  # missing hazard 'type'

    response = client.post('/api/add-hazard', json=payload)

    assert response.status_code == 400
    assert "error" in response.get_json()

def test_add_hazard_camera_not_found(client):
    client, mock_cursor = client

    # Simulate camera not found
    mock_cursor.fetchone.return_value = None

    payload = {
        "timestamp": "2024-04-27 15:30:00",
        "type": "fire",
        "cameraAddress": "rtsp://example.com/stream"
    }

    response = client.post('/api/add-hazard', json=payload)

    assert response.status_code == 404
    assert "error" in response.get_json()

def test_get_logs_success(client):
    client, mock_cursor = client

    # Simulate existing logs
    mock_cursor.fetchall.return_value = [
        (1, "rtsp://example.com/stream", "Test Camera", "2024-04-27 15", "fire", 1, False)
    ]

    response = client.get('/api/get-logs')

    assert response.status_code == 200
    logs = response.get_json()
    assert isinstance(logs, list)
    assert logs[0]["cameraName"] == "Test Camera"

def test_get_hazard_count(client):
    client, _ = client

    response = client.get('/api/get-hazard-count')

    assert response.status_code == 200
    assert response.get_data()  # mock_count returns ("mock_count", 200)
