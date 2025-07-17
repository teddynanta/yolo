# utils.py
from ultralytics import YOLO
import numpy as np

model = YOLO("D:\\sandbox\\yolo\\best.pt")  # Load your trained YOLO model

def detect_faces_yolo_image(image: np.ndarray, conf_threshold=0.6):
    """
    Detect faces from an image using YOLO.
    Returns list of face bounding boxes [(x1, y1, x2, y2), ...]
    """
    results = model(image)
    boxes = results[0].boxes
    if boxes is None or len(boxes) == 0:
        return []

    detected_faces = []
    for box in boxes.data:
        x1, y1, x2, y2, conf, cls = box
        if conf >= conf_threshold:
            detected_faces.append((int(x1), int(y1), int(x2), int(y2)))

    return detected_faces
