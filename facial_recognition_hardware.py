import face_recognition
import cv2
import numpy as np
from picamera2 import Picamera2
import time
import pickle
import csv
from datetime import datetime, date
from gpiozero import Button
from RPLCD.i2c import CharLCD


# LCD SETUP 
lcd = CharLCD(
    i2c_expander='PCF8574',  
    address=0x27,            
    port=1,                 
    cols=16,                
    rows=2,                 
    charmap='A00'           
)

# Function to display text on the LCD
def lcd_show(line1="", line2=""):
    lcd.clear()                        
    lcd.write_string(line1[:16])      
    if line2:
        lcd.cursor_pos = (1, 0)         
        lcd.write_string(line2[:16])    


# LOAD FACE DATA
with open("encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())       # Load binary pickle data into Python dictionary

known_face_encodings = data["encodings"]

known_face_names = data["names"]

# List defining the order in which attendance will be taken
attendance_list = ["Aarna", "Sarthak", "Chaitanya", "Garveet"]


# GPIO SETUP

start_button = Button(17, pull_up=True) 
check_button = Button(23, pull_up=True)


# DAILY CSV SETUP 
today_str = date.today().isoformat() #YYYY-MM-DD format
CSV_FILE = f"attendance_{today_str}.csv"
attendance_result = {}

# Function to initialize the CSV file
def init_csv():
    try:
        with open(CSV_FILE, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Status", "Timestamp"])
    except FileExistsError:
        pass

# Function to mark attendance for a person
def mark_attendance(name, status):
    attendance_result[name] = status    # Store result in memory for LCD summary
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, status, datetime.now().strftime("%H:%M:%S")])

# CAMERA SETUP
picam2 = None
cv_scaler = 4

# Function to start the camera
def start_camera():
    global picam2                        
    picam2 = Picamera2()                
    picam2.configure(
        picam2.create_preview_configuration(
            main={
                "format": "XRGB8888",   
                "size": (1280, 720)    
            }
        )
    )
    picam2.start()                      
    time.sleep(0.5)                     


# Function to stop the camera
def stop_camera():
    global picam2
    if picam2:
        picam2.stop()                   
        picam2 = None                   

# FACE CHECK FUNCTION

# Function to verify a specific person using face recognition
def check_person_once(expected_name, duration=0.3):
    start_time = time.time()             

    # Run face detection for a fixed duration
    while time.time() - start_time < duration:

        # Capture one frame from the camera and convert it into a numpy array.
        frame = picam2.capture_array()

small = cv2.resize(
    frame,              
    (0, 0),            
    fx=1/cv_scaler,        
    fy=1/cv_scaler       
)

        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb)

        encodings = face_recognition.face_encodings(rgb, locations)

        for encoding in encodings:

            # Compute distance between this encoding and all known encodings
            distances = face_recognition.face_distance(
                known_face_encodings, encoding
            )

            # Find index of the closest match
            best_match = np.argmin(distances)

            # Check if distance is within acceptable threshold
            if distances[best_match] < 0.45:

                if known_face_names[best_match] == expected_name:
                    return True          # Person verified

    # Return False if no valid match is found
    return False


# MAIN PROGRAM 

# Initialize today's CSV file
init_csv()

# Display system ready message on LCD
lcd_show("System Ready", "Press START")

# Wait until START button is pressed
start_button.wait_for_press()

# Display system started message
lcd_show("System Started", today_str)

# Turn on the camera
start_camera()

# Loop through each person in attendance list
for person in attendance_list:
    attempts = 0                         # Reset attempt counter

    # Allow up to 3 attempts per person
    while attempts < 3:
        lcd_show(person, f"Press CHECK {attempts+1}/3")
        check_button.wait_for_press()    # Wait for CHECK button press

        lcd_show("Checking...", person)
        match = check_person_once(person)

        if match:
            lcd_show(person, "PRESENT")
            mark_attendance(person, "Present")
            time.sleep(1.5)
            break                        # Move to next person
        else:
            attempts += 1
            lcd_show("Not Matched", f"Try {attempts}/3")
            time.sleep(1)

    # Mark absent if all attempts fail
    if attempts >= 3:
        lcd_show(person, "ABSENT")
        mark_attendance(person, "Absent")
        time.sleep(1.5)


# LCD DAILY SUMMARY 

lcd.clear()
lcd_show("Today's", "Attendance")
time.sleep(2)

# Display attendance summary on LCD
for name, status in attendance_result.items():
    lcd_show(name, status.upper())
    time.sleep(2)

# Display confirmation message
lcd_show("Saved to CSV", today_str)

# Stop the camera
stop_camera()

# Clear LCD before exiting
time.sleep(2)
lcd.clear()