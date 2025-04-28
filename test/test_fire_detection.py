import pytest
from unittest.mock import MagicMock, patch
import python_server.fire_detection as fire_detection

@pytest.fixture
def mock_connection():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.cursor.return_value.__exit__.return_value = None

    return mock_conn, mock_cursor

def test_start_fire_detection_for_all_cameras_starts_processes(mock_connection):
    mock_conn, mock_cursor = mock_connection
    mock_cursor.fetchall.return_value = [
        ("rtsp://camera1", "+1234567890", "default"),
        ("rtsp://camera2", "+1234567891", "special")
    ]

    with patch('python_server.fire_detection.multiprocessing.Process') as mock_process_class:
        mock_process_instance = MagicMock()
        mock_process_class.return_value = mock_process_instance

        processes = {}
        fire_detection.start_fire_detection_for_all_cameras(
            connection=mock_conn,
            processes=processes,
            detection_func=fire_detection.run_fire_detection
        )

        # Should start two processes
        assert len(processes) == 2
        assert "rtsp://camera1" in processes
        assert "rtsp://camera2" in processes
        assert mock_process_instance.start.call_count == 2

        # Check that each process was started with correct arguments
        expected_calls = [
            (("rtsp://camera1", "+1234567890", 0.6, 0.5, "fire", 10, "models/default/best.pt"),),
            (("rtsp://camera2", "+1234567891", 0.6, 0.5, "fire", 10, "models/special/best.pt"),)
        ]
        actual_args = [call_args.args for call_args in mock_process_class.call_args_list]
        assert actual_args == expected_calls

def test_run_fire_detection_logs_rtsp_url(caplog):
    with patch('python_server.fire_detection.run_yolov8_inference') as mock_inference:
        with caplog.at_level('INFO'):
            fire_detection.run_fire_detection("rtsp://dummy_camera", "+1234567890")

    assert any("Running fire detection on" in record.message for record in caplog.records)
    mock_inference.assert_called_once()
