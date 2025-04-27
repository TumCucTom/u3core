import os
import pytest
from unittest.mock import patch, MagicMock

# Set fake environment variables
os.environ["DB_HOST"] = "localhost"
os.environ["DB_USER"] = "test"
os.environ["DB_PASSWORD"] = "test"
os.environ["DB_NAME"] = "test_db"
os.environ["DB_PORT"] = "3306"
os.environ["POSTMARK_API"] = "dummy_postmark_api"

from python_server.app import create_app

@pytest.fixture
def client():
    with patch('python_server.app.pymysql.connect') as mock_connect, \
            patch('python_server.app.initialise_database') as mock_init_db, \
            patch('python_server.email_utils.send_email') as mock_send_email:

        # Mock DB connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        mock_connect.return_value = mock_conn
        mock_init_db.return_value = None
        mock_send_email.return_value = None

        app, _ = create_app()
        app.config['TESTING'] = True
        client = app.test_client()
        yield client
