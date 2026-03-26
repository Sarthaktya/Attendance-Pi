import cv2
import numpy as np


class FaceEmbedder:
    def __init__(self, model_path):
        self.net = cv2.dnn.readNet(model_path)

    def embed(self, face):
        face = cv2.resize(face, (112, 112))
        blob = cv2.dnn.blobFromImage(
            face,
            scalefactor=1.0 / 255,
            size=(112, 112),
            mean=(0, 0, 0),
            swapRB=True,
            crop=False
        )

        self.net.setInput(blob)
        emb = self.net.forward()
        emb = emb.flatten()
        emb = emb / np.linalg.norm(emb)

        return emb
