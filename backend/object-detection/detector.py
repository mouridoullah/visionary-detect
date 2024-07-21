import torch
import cv2
import json
import os

# Chemins des fichiers
MODEL_PATH = 'backend/object-detection/model/yolov5s.pt'
LABELS_PATH = 'backend/object-detection/model/coco_labels.json'

# Télécharger le modèle YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, trust_repo=True)

def detect_objects(image):
    # Effectuer la détection d'objets
    results = model(image)
    # Post-traitement des résultats
    detections = results.xyxy[0].cpu().numpy()
    return detections

def draw_boxes(image, detections, labels):
    for detection in detections:
        x1, y1, x2, y2, confidence, class_id = detection
        label = labels[int(class_id)]
        color = (0, 255, 0)  # green

        # Dessiner le rectangle englobant
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        # Ajouter l'étiquette de classe et la confiance
        cv2.putText(image, f'{label} {confidence:.2f}', (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    return image

def process_image(image_path, labels):
    # Charger l'image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Détecter les objets
    detections = detect_objects(img_rgb)
    # Dessiner les boîtes englobantes
    img_with_boxes = draw_boxes(img, detections, labels)

    # Afficher l'image
    cv2.imshow("Detections", img_with_boxes)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def process_video(video_path, labels):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = detect_objects(frame_rgb)
        frame_with_boxes = draw_boxes(frame, detections, labels)

        # Afficher la frame
        cv2.imshow('Detections', frame_with_boxes)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Charger les labels des classes depuis le fichier JSON
with open(LABELS_PATH) as f:
    labels = json.load(f)

# Exemple d'utilisation
if __name__ == "__main__":
    media_path = input("Veuillez entrer le chemin de l'image ou de la vidéo: ").strip()

    if not media_path:
        print("Chemin non valide.")
    elif os.path.isfile(media_path):
        if media_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            process_image(media_path, labels)
        elif media_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            process_video(media_path, labels)
        else:
            print("Format de fichier non supporté.")
    else:
        print("Le fichier spécifié n'existe pas.")
