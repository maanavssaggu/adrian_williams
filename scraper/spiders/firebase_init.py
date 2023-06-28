import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import initialize_app

def initilise_firebase():
    cred = credentials.Certificate("credentials/aw-wsr-firebase-adminsdk-458m1-b68fb8fd1d.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://aw-wsr-default-rtdb.firebaseio.com/"
    })

# initilise_firebase()

# db = firebase_admin.db.reference()
# data = db.child("Propertys")
# print(data.get())