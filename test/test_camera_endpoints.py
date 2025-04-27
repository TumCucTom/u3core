import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from python_server.endpoints.camera_endpoints import register_camera_endpoints

# TOP-LEVEL dummy detection function (outside fixture!)
def run_fire_detection(url):
    pass

@pytest.fixture
def client():
    app = Flask(__name__)
    fire_detection_processes = {}

    dummy_db_config = {"host": "localhost", "user": "test", "password": "test", "database": "test_db"}

    with patch('python_server.endpoints.camera_endpoints.get_db_connection') as mock_get_conn, \
            patch('python_server.endpoints.camera_endpoints.get_count_from_table', return_value=("mock_count", 200)):

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        mock_get_conn.return_value = mock_conn

        register_camera_endpoints(app, dummy_db_config, fire_detection_processes, run_fire_detection)

        app.config['TESTING'] = True
        yield app.test_client(), mock_cursor, fire_detection_processes


def test_add_camera(client):
    client, mock_cursor, fire_detection_processes = client

    mock_cursor.fetchall.return_value = []

    payload = {
        "name": "Test Camera",
        "rtsp_url": "tcp://192.168.1.10/stream",
        "site_id": 1
    }

    response = client.post('/api/add-camera', json=payload)
    assert response.status_code == 201
    assert "message" in response.get_json()
    assert "rtsp://" in list(fire_detection_processes.keys())[0]

def test_delete_camera_success(client):
    client, mock_cursor, fire_detection_processes = client

    # Simulate camera found in DB
    mock_cursor.fetchone.return_value = ("rtsp://192.168.1.10/stream",)
    mock_cursor.rowcount = 1

    fire_detection_processes["rtsp://192.168.1.10/stream"] = MagicMock()

    response = client.delete('/api/delete-camera/1')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Camera deleted successfully"

def test_update_camera_change_rtsp(client):
    client, mock_cursor, fire_detection_processes = client

    # Existing RTSP URL
    mock_cursor.fetchone.return_value = ("rtsp://192.168.1.10/stream",)
    mock_cursor.rowcount = 1

    old_url = "rtsp://192.168.1.10/stream"
    fire_detection_processes[old_url] = MagicMock()

    payload = {
        "rtsp_url": "tcp://192.168.1.11/stream"
    }

    response = client.put('/api/update-camera/1', json=payload)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Camera updated successfully"

def test_get_camera_count(client):
    client, mock_cursor, _ = client

    response = client.get('/api/get-camera-count')
    assert response.status_code == 200
    assert response.get_data()
