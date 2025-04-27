import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import pymysql

import python_server.endpoints.endpoint_utils as utils

@pytest.fixture
def mock_db():
    with patch('python_server.endpoints.endpoint_utils.get_db_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        mock_get_conn.return_value = mock_conn
        yield mock_conn, mock_cursor

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

def test_get_count_from_table_existing_table(mock_db, app):
    mock_conn, mock_cursor = mock_db

    mock_cursor.fetchone.side_effect = [
        (1,),  # Table exists check
        (42,)  # 42 rows in table
    ]

    dummy_config = {}

    with app.app_context():
        response, status_code = utils.get_count_from_table('Logs', dummy_config)

    assert status_code == 200
    assert response.json == 42

def test_get_count_from_table_non_existing_table(mock_db, app):
    mock_conn, mock_cursor = mock_db

    mock_cursor.fetchone.return_value = (0,)

    dummy_config = {}

    with app.app_context():
        response, status_code = utils.get_count_from_table('NonexistentTable', dummy_config)

    assert status_code == 200
    assert response.json == 0

def test_get_count_from_table_error(mock_db, app):
    mock_conn, mock_cursor = mock_db

    mock_cursor.execute.side_effect = pymysql.Error("DB failure!")

    dummy_config = {}

    with app.app_context():
        response, status_code = utils.get_count_from_table('AnyTable', dummy_config)

    assert status_code == 500
    assert "error" in response.json

