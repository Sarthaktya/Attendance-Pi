import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

cred = credentials.Certificate("attendance-pi-38ffd-firebase-adminsdk-fbsvc-ca00634882.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://attendance-pi-38ffd-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

def upload_attendance(name, confidence):

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%H:%M:%S")

    ref = db.reference(f"attendance/{date}")

    data = {
        "timestamp": timestamp,
        "confidence": float(confidence)
    }

    ref.child(name).set(data)