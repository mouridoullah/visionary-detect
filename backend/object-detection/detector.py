import torch
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import requests

# Charger le modèle YOLO
def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    return model

# Détection des objets
def detect_objects(image_bytes):
    model = load_model()
    # Charger l'image en mémoire
    image = Image.open(BytesIO(image_bytes))
    results = model(image)
    # Retourner les résultats sous forme de liste
    return results.pandas().xyxy[0].to_dict(orient="records")

# Exemple d'utilisation
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python detector.py <image_url>")
        sys.exit(1)

    image_url = sys.argv[1]
    response = requests.get(image_url)
    if response.status_code == 200:
        detections = detect_objects(response.content)
        print(detections)
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
