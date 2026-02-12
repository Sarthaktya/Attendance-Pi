import cv2
import os
from datetime import datetime
from picamera2 import Picamera2
import time

# Change this to the name of the person you're capturing images for.
PERSON_NAME = "Sarthak"  

def create_folder(name):
    dataset_folder = "dataset"
    if not os.path.exists(dataset_folder): #Ensure the "dataset" folder exists, if it does not, make it.
        os.makedirs(dataset_folder)
    
    person_folder = os.path.join(dataset_folder, name) #Now it will create a subfolder inside the dataset folder for the mentioned paerson's name.
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    return person_folder

def capture_photos(name):
    folder = create_folder(name)
    
    # Initialize the camera
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)})) #We want frames in a 4-channel 8-bit format
    picam2.start() #Start actual video streaming from the camera

    # Allow camera to warm up
    time.sleep(2)

    photo_count = 0 #Keep track of how many images have been taken
    
    print(f"Taking photos for {name}. Press SPACE to capture, 'q' to quit.")
    
    while True:
        # Capture frame from Pi Camera
        frame = picam2.capture_array() #Converts the frame into a Numpy array. Each pixel has RGB and 'aplha' (transparency) values
        
        # Display the frame
        cv2.imshow('Capture', frame) #A separate window of 'live feed' is opened.
        
        key = cv2.waitKey(1) #For every single frame, check if any key was pressed on the keyboard or not, for 1ms. For different keys its a different
        #number generated and returned in 'key'. 
        
        if key == ord(' '):  # The ord() function converts a ssingle letter/argument inside it into an UNICODE integer, here it is done for the Space
            #key
            #Image is saved using this block of code
            photo_count += 1 #The count variable incremets by 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") #Gets the present date and time, which is used to save photos.
            filename = f"{name}_{timestamp}.jpg" #Person's name and the mtimestamp are joined
            filepath = os.path.join(folder, filename) #Writes this image in the person's folder in the parent Dataset folder
            cv2.imwrite(filepath, frame) #Image is saved as .jpg 
            print(f"Photo {photo_count} saved: {filepath}")
        
        elif key == ord('q'):  # Q key
            break #Loop is exited and the capture is ended.
    
    # Clean up
    cv2.destroyAllWindows() #Closes the capture window.
    picam2.stop() #Stops the camera.
    print(f"Photo capture completed. {photo_count} photos saved for {name}.")