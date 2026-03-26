import cv2

class PiCameraStream:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)

    def read(self):
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        self.cap.release()