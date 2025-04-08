"""Training from a given dataset"""
from ultralytics import YOLO

def train_yolo_model(
        dataset_yaml: str,
        epochs: int = 50,
        img_size: int = 640,
        model_weights: str = "yolov8n.pt"):
    """
    Trains a YOLOv8 model on a specified dataset.
    """
    # Load the YOLO model
    model = YOLO(model_weights)

    # Train the model
    model.train(data=dataset_yaml, epochs=epochs, imgsz=img_size)

if __name__ == "__main__":
    # Example usage: Modify or call from another script
    import sys

    if len(sys.argv) > 1:
        DATASET_PATH = sys.argv[1]
    else:
        DATASET_PATH = "datasets/default/data.yaml"  # Default path if no argument is provided

    train_yolo_model(DATASET_PATH)
