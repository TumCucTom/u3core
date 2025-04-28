import pytest
from unittest.mock import patch, MagicMock

import python_server.fire_detection_script as fire_script

@pytest.fixture
def dummy_frame():
    # Create a dummy image frame (black frame)
    import numpy as np
    return np.zeros((480, 640, 3), dtype=np.uint8)

def test_detect_fire_with_yolo_fire_detected(dummy_frame):
    mock_model = MagicMock()
    mock_box = MagicMock()
    mock_box.cls = [MagicMock(item=lambda: 0)]  # class 0
    mock_box.conf = [MagicMock(item=lambda: 0.95)]  # high confidence
    mock_model.return_value = [MagicMock(boxes=[mock_box])]

    fire_detected, alert_type = fire_script.detect_fire_with_yolo(dummy_frame, mock_model)

    assert fire_detected is True
    assert alert_type == "fire"

def test_detect_fire_with_yolo_no_fire(dummy_frame):
    mock_model = MagicMock()
    mock_model.return_value = [MagicMock(boxes=[])]  # No boxes detected

    fire_detected, alert_type = fire_script.detect_fire_with_yolo(dummy_frame, mock_model)

    assert fire_detected is False
    assert alert_type == "none"

def test_run_yolov8_inference_quick_exit(dummy_frame):
    with patch('python_server.fire_detection_script.YOLO') as mock_yolo, \
            patch('python_server.fire_detection_script.cv2.VideoCapture') as mock_video, \
            patch('python_server.fire_detection_script.send_whatsapp_via_twilio') as mock_whatsapp, \
            patch('python_server.fire_detection_script.send_hazard_log') as mock_hazard_log, \
            patch('python_server.fire_detection_script.cv2.destroyAllWindows'):

        mock_model_instance = MagicMock()
        mock_result = MagicMock()
        mock_result.boxes.data = []  # No fire boxes
        mock_model_instance.return_value = [mock_result]
        mock_model_instance.names = {0: "fire"}
        mock_yolo.return_value = mock_model_instance

        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True  # <<< Always True for test
        mock_cap.read.side_effect = [(True, dummy_frame), (False, dummy_frame)]  # <<< Read success then stop
        mock_video.return_value = mock_cap

        fire_script.run_yolov8_inference(
            rtsp_url="dummy_rtsp_url",
            number="+1234567890",
            conf=0.6,
            iou=0.5,
            alert_class="fire",
            alert_interval=10,
            model_path="dummy_model_path.pt"
        )

        # Now this will pass
        assert mock_cap.read.call_count >= 1
        mock_whatsapp.assert_not_called()
        mock_hazard_log.assert_not_called()

