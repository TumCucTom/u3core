import pytest
from unittest.mock import patch, MagicMock

import python_server.train_yolo as trainer  # correct!

def test_train_yolo_model_calls_train():
    with patch('python_server.train_yolo.YOLO') as mock_yolo_class:  # <<< PATCH CORRECT MODULE!
        # Mock instance returned by YOLO(model_weights)
        mock_model_instance = MagicMock()
        mock_yolo_class.return_value = mock_model_instance

        # Call the function under test
        trainer.train_yolo_model(
            dataset_yaml="path/to/data.yaml",
            epochs=10,
            img_size=320,
            model_weights="yolov8n.pt"
        )

        # Check that YOLO model was loaded with correct weights
        mock_yolo_class.assert_called_once_with("yolov8n.pt")

        # Check that train was called with correct arguments
        mock_model_instance.train.assert_called_once_with(
            data="path/to/data.yaml",
            epochs=10,
            imgsz=320
        )
