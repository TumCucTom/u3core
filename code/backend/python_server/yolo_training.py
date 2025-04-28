"""Training from a given dataset"""
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments
import os
import sys
from ultralytics import YOLO

def train_yolo_model(
        dataset_yaml: str,
        epochs: int = 50,
        img_size: int = 640,
        model_weights: str = "yolov8n.pt",
        save_dir: str = "model/default/",
        save_name: str = "default.pt"):
    """
    Trains a YOLOv8 model on a specified dataset and saves the trained model.
    """

    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Load the YOLO model
    model = YOLO(model_weights)

    # Train the model
    _ = model.train(data=dataset_yaml, epochs=epochs, imgsz=img_size)

    # Save the trained model
    save_path = os.path.join(save_dir, save_name)
    model.export(format="torchscript", path=save_path)  # Export the model

    print(f"Trained model saved at: {save_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        DATASET_PATH = sys.argv[1]
    else:
        DATASET_PATH = "datasets/default/data.yaml"  # Default path if no argument is provided

    train_yolo_model(DATASET_PATH)
