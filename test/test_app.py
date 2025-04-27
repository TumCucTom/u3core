# test/test_app.py
import pytest
from python_server.app import create_app

@pytest.fixture
def client():
    app, _ = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_health_check(client):
    """Basic test to ensure the app runs and health endpoint works."""
    response = client.get('/health')
    assert response.status_code == 200
