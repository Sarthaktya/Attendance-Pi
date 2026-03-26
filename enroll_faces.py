import os
import cv2
import numpy as np

from camera.webcam_stream import PiCameraStream
from detection.face_detector import FaceDetector
from recognition.embedder import FaceEmbedder


# ---------------- CONFIG ----------------
NAME = "Sarthak"          # change for each person
NUM_SAMPLES = 4
SAVE_PATH = "known_embeddings.npy"

# ----------------------------------------
detector = FaceDetector(confidence_threshold=0.4)
embedder = FaceEmbedder(
    "models/face_recognition_sface_2021dec.onnx"
)

cap = PiCameraStream()
embeddings = []

print(f"[INFO] Enrolling: {NAME}")
print("[INFO] Press 'c' to capture, 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Frame not received")
        break

    faces = detector.detect(frame)

    # Draw face boxes
    for (x1, y1, x2, y2) in faces:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.putText(
        frame,
        f"Samples: {len(embeddings)}/{NUM_SAMPLES}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )
    cv2.imshow("Attendance System", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("c") and len(faces) == 1:
        x1, y1, x2, y2 = faces[0]
        face = frame[y1:y2, x1:x2]

        if face.size > 0:
            emb = embedder.embed(face)
            embeddings.append(emb)
            print(f"[CAPTURED] {len(embeddings)}/{NUM_SAMPLES}")
    if key == ord("q") or len(embeddings) >= NUM_SAMPLES:
        break

cap.release()
cv2.destroyAllWindows()

# ---------------- VALIDATION ----------------
if len(embeddings) == 0:
    raise RuntimeError("Enrollment failed: no face embeddings captured.")

mean_embedding = np.mean(embeddings, axis=0)
mean_embedding /= np.linalg.norm(mean_embedding)

# Load or create database
if os.path.exists(SAVE_PATH):
    db = np.load(SAVE_PATH, allow_pickle=True).item()
else:
    db = {}

db[NAME] = mean_embedding
np.save(SAVE_PATH, db)
print(f"[SUCCESS] Enrollment completed for {NAME}")