import cv2
import os

CASCADE_path = "haarcascade_frontalface_default.xml"
MODEL_PATH = "face_model.yml"
CONFIDENCE_THRESHOLD = 70  # lower = stricter match; tune after testing


def recognize_face(timeout_frames=50):
    """Runs a live face-check challenge, used by 'wake check'."""
    if not os.path.exists(MODEL_PATH):
        return False, "Face model not found. Run enrollment first."

    face_cascade = cv2.CascadeClassifier(CASCADE_path)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)

    cam = cv2.VideoCapture(0)
    frames_checked = 0
    recognized = False

    while frames_checked < timeout_frames:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_img = gray[y:y + h, x:x + w]
            face_img = cv2.resize(face_img, (200, 200))
            label, confidence = recognizer.predict(face_img)

            if confidence < CONFIDENCE_THRESHOLD:
                recognized = True
                break

        if recognized:
            break

        frames_checked += 1

    cam.release()
    cv2.destroyAllWindows()

    if recognized:
        return True, "Face recognized."
    return False, "Face not recognized."


def check_face_once():
    """Single-frame check, used by the background auto-relock monitor."""
    if not os.path.exists(MODEL_PATH):
        return False

    face_cascade = cv2.CascadeClassifier(CASCADE_path)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)

    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if not ret:
        return False

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y + h, x:x + w]
        face_img = cv2.resize(face_img, (200, 200))
        label, confidence = recognizer.predict(face_img)
        if confidence < CONFIDENCE_THRESHOLD:
            return True

    return False


if __name__ == "__main__":
    success, message = recognize_face()
    print(success, message)