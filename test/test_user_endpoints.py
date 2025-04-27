import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from python_server.endpoints.user_endpoints import register_user_endpoints

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True

    dummy_db_config = {"host": "localhost", "user": "test", "password": "test", "database": "test_db"}
    dummy_postmark_api = "dummy-api-key"

    with patch('python_server.endpoints.user_endpoints.get_db_connection') as mock_get_conn, \
            patch('python_server.endpoints.user_endpoints.send_email', return_value=True):

        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        mock_get_conn.return_value = mock_conn

        register_user_endpoints(app, dummy_db_config, dummy_postmark_api)

        yield app.test_client(), mock_cursor

def test_get_emails_success(client):
    client, mock_cursor = client

    mock_cursor.fetchall.return_value = [("test@example.com",)]

    response = client.get('/api/emails')

    assert response.status_code == 200
    assert "test@example.com" in response.get_json()

def test_get_name_success(client):
    client, mock_cursor = client

    mock_cursor.fetchone.return_value = ("John",)

    response = client.get('/api/getName?email=test@example.com')

    assert response.status_code == 200
    assert response.data == b'John'

def test_get_name_missing_email(client):
    client, _ = client

    response = client.get('/api/getName')

    assert response.status_code == 400

def test_get_name_not_found(client):
    client, mock_cursor = client

    mock_cursor.fetchone.return_value = None

    response = client.get('/api/getName?email=missing@example.com')

    assert response.status_code == 404

def test_login_success(client):
    client, mock_cursor = client

    mock_cursor.fetchone.return_value = ("hashed_password",)

    response = client.get('/api/login?emailVar=test@example.com')

    assert response.status_code == 200
    assert response.data == b'hashed_password'

def test_login_missing_email(client):
    client, _ = client

    response = client.get('/api/login')

    assert response.status_code == 400

def test_login_not_found(client):
    client, mock_cursor = client

    mock_cursor.fetchone.return_value = None

    response = client.get('/api/login?emailVar=missing@example.com')

    assert response.status_code == 404

def test_add_to_customer_success(client):
    client, mock_cursor = client

    payload = {
        "items": ["John", "Doe", "john@example.com", "password123"]
    }

    response = client.post('/api/addToCustomer', json=payload)

    assert response.status_code == 200
    assert "message" in response.get_json()

def test_add_to_customer_invalid_input(client):
    client, _ = client

    payload = {
        "items": ["John", "Doe"]  # Missing email/password
    }

    response = client.post('/api/addToCustomer', json=payload)

    assert response.status_code == 400

def test_send_reset_email_success(client):
    client, mock_cursor = client

    mock_cursor.fetchone.return_value = ("email",)

    payload = {"email": "john@example.com"}

    response = client.post('/api/sendResetEmail', json=payload)

    assert response.status_code == 200
    assert "message" in response.get_json()

def test_send_reset_email_not_found(client):
    client, mock_cursor = client

    mock_cursor.fetchone.return_value = None

    payload = {"email": "missing@example.com"}

    response = client.post('/api/sendResetEmail', json=payload)

    assert response.status_code == 404

def test_send_verify_email_success(client):
    client, mock_cursor = client

    mock_cursor.fetchone.return_value = ("email",)

    payload = {"email": "john@example.com"}

    response = client.post('/api/sendVerifyEmail', json=payload)

    assert response.status_code == 200
    assert "message" in response.get_json()

def test_send_verify_email_not_found(client):
    client, mock_cursor = client

    mock_cursor.fetchone.return_value = None

    payload = {"email": "missing@example.com"}

    response = client.post('/api/sendVerifyEmail', json=payload)

    assert response.status_code == 404
