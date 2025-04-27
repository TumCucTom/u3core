import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from python_server.endpoints.site_endpoints import register_site_endpoints

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True

    dummy_db_config = {"host": "localhost", "user": "test", "password": "test", "database": "test_db"}

    fire_detection_processes = {}

    with patch('python_server.endpoints.site_endpoints.get_db_connection') as mock_get_conn, \
            patch('python_server.endpoints.site_endpoints.get_count_from_table', return_value=("mock_count", 200)):

        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        mock_get_conn.return_value = mock_conn

        register_site_endpoints(app, dummy_db_config, fire_detection_processes)

        yield app.test_client(), mock_cursor, fire_detection_processes

def test_add_site_success(client):
    client, mock_cursor, _ = client

    payload = {
        "name": "New Site",
        "latitude": "51.5074",
        "longitude": "0.1278"
    }

    response = client.post('/api/add-site', json=payload)

    assert response.status_code == 201
    assert "message" in response.get_json()

def test_add_site_missing_fields(client):
    client, mock_cursor, _ = client

    payload = {
        "name": "New Site"
    }  # missing latitude and longitude

    response = client.post('/api/add-site', json=payload)

    assert response.status_code == 400
    assert "error" in response.get_json()

def test_fetch_sites_success(client):
    client, mock_cursor, _ = client

    # Simulate a site and its cameras
    mock_cursor.fetchall.side_effect = [
        [(1, "Site A")],  # Sites
        [(1, "Camera A1"), (2, "Camera A2")]  # Cameras for site 1
    ]

    response = client.get('/api/sites')

    assert response.status_code == 200
    data = response.get_json()
    assert "sites" in data
    assert isinstance(data["sites"], list)
    assert data["sites"][0]["name"] == "Site A"

def test_delete_site_success(client):
    client, mock_cursor, _ = client

    # Simulate site delete affecting 1 row
    mock_cursor.rowcount = 1

    response = client.delete('/api/delete-site/1?delete_cameras=true')

    assert response.status_code == 200
    assert "message" in response.get_json()

def test_delete_site_not_found(client):
    client, mock_cursor, _ = client

    # Simulate site not found (0 rows deleted)
    mock_cursor.rowcount = 0

    response = client.delete('/api/delete-site/999')

    assert response.status_code == 404
    assert "error" in response.get_json()

def test_update_site_success(client):
    client, mock_cursor, _ = client

    # Simulate site exists
    mock_cursor.fetchone.return_value = (1,)
    mock_cursor.rowcount = 1

    payload = {
        "name": "Updated Site",
        "latitude": "40.7128",
        "longitude": "-74.0060"
    }

    response = client.put('/api/update-site/1', json=payload)

    assert response.status_code == 200
    assert "message" in response.get_json()

def test_update_site_no_fields(client):
    client, mock_cursor, _ = client

    payload = {}

    response = client.put('/api/update-site/1', json=payload)

    assert response.status_code == 400
    assert "error" in response.get_json()

def test_update_site_not_found(client):
    client, mock_cursor, _ = client

    # Simulate site not found
    mock_cursor.fetchone.return_value = None

    payload = {
        "name": "Updated Site"
    }

    response = client.put('/api/update-site/999', json=payload)

    assert response.status_code == 404
    assert "error" in response.get_json()

def test_get_site_count(client):
    client, _, _ = client

    response = client.get('/api/get-site-count')

    assert response.status_code == 200
    assert response.get_data()  # mock returns "mock_count"
