import cv2 
import os
import numpy as np

FACE_DATA_DIR = "face_data"
MODEL_PATH = "face_model.yml"

def train_model():
    face_files = [f for f in os.listdir(FACE_DATA_DIR) if f.endswith(".jpg")]

    if not face_files:
        print("no face data found. Run face_enroll.py first.")
        return

    faces = []
    labels = []

    for filename in face_files:
        img_path = os.path.join(FACE_DATA_DIR, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        faces.append(img)
        labels.append(1)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    recognizer.save(MODEL_PATH)

    print(f"model trained on {len(faces)} samples and saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()