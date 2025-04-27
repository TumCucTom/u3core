import pytest
from unittest.mock import patch, MagicMock

import python_server.database as db_module  # adjust if needed

def test_get_db_connection_calls_pymysql_connect():
    with patch('python_server.database.pymysql.connect') as mock_connect:
        dummy_config = {"host": "localhost", "user": "test", "password": "test", "database": "test_db"}

        db_module.get_db_connection(dummy_config)

        mock_connect.assert_called_once_with(**dummy_config)

def test_initialise_database_creates_tables():
    with patch('python_server.database.get_db_connection') as mock_get_conn:
        # Fake database connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        # Setup context manager behavior
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        mock_get_conn.return_value = mock_conn

        dummy_config = {"host": "localhost", "user": "test", "password": "test", "database": "test_db"}

        db_module.initialise_database(dummy_config)

        # Check that execute was called multiple times (for all CREATE TABLE statements)
        assert mock_cursor.execute.call_count >= 5  # At least 5 CREATE TABLEs

        # Check that commit was called
        mock_conn.commit.assert_called_once()

        # Check that connection was closed
        mock_conn.close.assert_called_once()
