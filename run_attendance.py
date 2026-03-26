import cv2
from camera.webcam_stream import PiCameraStream
from recognition.recognizer import FaceRecognizer
from detection.face_detector import FaceDetector
from recognition.embedder import FaceEmbedder
from tracking.temporal_tracker import TemporalTracker
from attendance_engine import AttendanceEngine
from firebase_handler import upload_attendance

# -----------------------------
# Initialization
# -----------------------------
print("[INFO] Initializing Attendance System...")

detector = FaceDetector(confidence_threshold=0.4)

embedder = FaceEmbedder(
    "models/face_recognition_sface_2021dec.onnx"
)

recognizer = FaceRecognizer(
    "known_embeddings.npy",
    threshold=0.50
)

tracker = TemporalTracker(min_duration=2.0)
attendance = AttendanceEngine()

cap = PiCameraStream()

print("[INFO] Attendance System running")
print("[INFO] Press 'q' to exit")

# -----------------------------
# Main loop
# -----------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        print("[ERROR] Failed to read frame")
        break

    faces = detector.detect(frame)

    # Process every detected face
    for (x1, y1, x2, y2) in faces:

        face = frame[y1:y2, x1:x2]

        if face.size == 0:
            continue

        # -------------------------
        # Recognition
        # -------------------------
        embedding = embedder.embed(face)
        name, distance = recognizer.recognize(embedding)

        # -------------------------
        # Temporal Logic
        # -------------------------
        if name != "Unknown":

            if tracker.update(name):

                if attendance.mark_present(name):
                    print(f"[ATTENDANCE] {name} marked PRESENT")

                    upload_attendance(name, distance)

        # -------------------------
        # Display
        # -------------------------
        label = name

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# -----------------------------
# Clean Up
# -----------------------------
cap.release()
cv2.destroyAllWindows()