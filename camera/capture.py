from picamera2 import Picamera2
import time
import cv2

class Camera:
    def __init__(self, width=640, height=480):
        self.picam2 = Picamera2()
    
        config = self.picam2.create_preview_configuration(
            main={"size": (width, height), "format":"RGB888"}
        )
        self.picam2.configure(config)
        
        self.picam2.start()
        time.sleep(1.0)
    
    def get_frame(self):
        frame = self.picam2.capture_array()
        return frame
    
    def release(self):
        self.picam2.stop()