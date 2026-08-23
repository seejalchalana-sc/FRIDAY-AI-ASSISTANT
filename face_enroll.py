import cv2
import os

FACE_DATA_DIR = "face_data"
CASCADE_path = "haarcascade_frontalface_default.xml"
NUM_SAMPLES = 30

def enroll_face():
    if not os.path.exists(FACE_DATA_DIR):
        os.makedirs(FACE_DATA_DIR)

    face_cascade = cv2.CascadeClassifier(CASCADE_path)
    cam = cv2.VideoCapture(0)

    print("look at the camera. capturing face samples...")
    count = 0

    while count < NUM_SAMPLES:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y + h, x:x + w]
            face_img = cv2.resize(face_img, (200, 200))
            filename = os.path.join(FACE_DATA_DIR, f"face_{count}.jpg")
            cv2.imwrite(filename, face_img)
            cv2.rectangle(frame, (x, y), (x + w, y+ h), (0, 255, 0), 2)
            print(f"captured sample {count}/{NUM_SAMPLES}")

        cv2.imshow("enrollung - press q to quit early", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    if count > 0:
        print(f"enrollment complete. {count} samples saved.")
    else:
        print("no face samples captures. try again with better lightinng.")

if __name__ == "__main__":
    enroll_face()