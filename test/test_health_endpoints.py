import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import pymysql

from python_server.endpoints.health_endpoints import register_health_endpoints

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True

    dummy_db_config = {"host": "localhost", "user": "test", "password": "test", "database": "test_db"}

    register_health_endpoints(app, dummy_db_config)

    yield app.test_client()

def test_db_health_check_success(client):
    with patch('python_server.endpoints.health_endpoints.pymysql.connect') as mock_connect:
        # Simulate successful database connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        response = client.get('/api/health/db')

        assert response.status_code == 200
        assert response.get_json() == {"status": "healthy", "database_connection": True}

def test_db_health_check_failure(client):
    with patch('python_server.endpoints.health_endpoints.pymysql.connect') as mock_connect, \
            patch('time.sleep', return_value=None):  # Speed up test by skipping real sleep
        # Simulate database OperationalError every time
        mock_connect.side_effect = pymysql.err.OperationalError

        response = client.get('/api/health/db')

        assert response.status_code == 503
        assert response.get_json() == {"status": "unhealthy", "database_connection": False}
