import cv2
import numpy as np


class FaceDetector:
    def __init__(self,
                 model_path="models/res10_300x300_ssd_iter_140000.caffemodel",
                 config_path="models/deploy.prototxt",
                 confidence_threshold=0.4):   # lowered threshold

        self.net = cv2.dnn.readNetFromCaffe(config_path, model_path)
        self.confidence_threshold = confidence_threshold

    def detect(self, frame):
        h, w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)),
            1.0,
            (300, 300),
            (104.0, 177.0, 123.0),
            swapRB=False,
            crop=False
        )

        self.net.setInput(blob)
        detections = self.net.forward()

        faces = []

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > self.confidence_threshold:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")

                faces.append((x1, y1, x2, y2))

        return faces
