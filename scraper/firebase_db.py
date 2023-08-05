import os
from firebase_admin import credentials
import firebase_admin
from firebase_admin import firestore
from spiders.property import Property
from typing import List

class FireBaseDB:
    def __init__(self):
        # get paths to initilise firebase
        relative_path = "credentials/aw-wsr-firebase-adminsdk-458m1-cdc8443299.json"
        base_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(base_dir, relative_path)

        # initilise firebase if not already initilised
        cred = credentials.Certificate(absolute_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, 
                {
                    "databaseURL": "https://aw-wsr-default-rtdb.firebaseio.com/"
                }
            )
        self.db = firestore.client()

    #upload data to firebase by property id
    def upload(self, properties: List[Property]) -> None:
        """
        input: A list of property objects
        """
        for property in properties:
            doc_ref = self.db.collection(property.date_str).document(property.address_line_2).collection("properties").document(property.property_id)
            doc_ref.set(property.propertery_to_dict())