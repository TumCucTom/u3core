import pytest
from unittest.mock import patch, MagicMock

import python_server.fire_detection_script as fire_script

@pytest.fixture
def dummy_frame():
    # Create a dummy image frame (e.g., black image)
    import numpy as np
    return np.zeros((480, 640, 3), dtype=np.uint8)

def test_detect_fire_with_roboflow_fire_detected(dummy_frame):
    with patch('python_server.fire_detection_script.requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "predictions": [
                {"class": "fire", "confidence": 0.9}
            ]
        }

        fire_detected, alert_type = fire_script.detect_fire_with_roboflow(dummy_frame)

        assert fire_detected is True
        assert alert_type == "fire"

def test_detect_fire_with_roboflow_no_fire(dummy_frame):
    with patch('python_server.fire_detection_script.requests.post') as mock_post:
        mock_post.return_value.json.return_value = {"predictions": []}

        fire_detected, alert_type = fire_script.detect_fire_with_roboflow(dummy_frame)

        assert fire_detected is False
        assert alert_type == "none"

def test_process_rtsp_stream_with_url_quick_exit(dummy_frame):
    # Mock everything heavy
    with patch('python_server.fire_detection_script.cv2.VideoCapture') as mock_video, \
            patch('python_server.fire_detection_script.detect_fire_with_roboflow') as mock_detect, \
            patch('python_server.fire_detection_script.cv2.imshow'), \
            patch('python_server.fire_detection_script.cv2.waitKey', return_value=ord('q')), \
            patch('python_server.fire_detection_script.send_sms_via_sns'), \
            patch('python_server.fire_detection_script.send_whatsapp_via_twilio'), \
            patch('python_server.fire_detection_script.send_hazard_log'):

        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.side_effect = [(True, dummy_frame), (False, None)]  # read() once then fail
        mock_video.return_value = mock_cap

        mock_detect.return_value = (False, "none")  # No fire detected

        fire_script.process_rtsp_stream_with_url("dummy_rtsp_url")

        # Verify that read was called (meaning we entered the loop at least once)
        assert mock_cap.read.call_count >= 1
