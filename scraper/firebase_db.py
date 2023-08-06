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

    # TODO FOR MAANAV
    def upload(self, properties: List[Property]) -> None:
        """
            Given a list of properties, uploads them to the firebase database
        """
        for property in properties:
            doc_ref = self.db.collection(property.date_str).document(property.address_line_2).collection("properties").document(property.property_id)
            doc_ref.set(property.propertery_to_dict())

    # TODO FOR MAANAV
    def get_properties(self, start_date: str, end_date: str, suburbs: List[str]) -> List[Property]:
        '''
            Given a date range and suburn list, returns a list of sold properties
        '''
        properties = []
        while(self.is_end_after_start(start_date, end_date)):
            for suburb in suburbs:
                doc_ref = self.db.collection(start_date).document(suburb).collection("properties")
                docs = doc_ref.stream()
                for doc in docs:
                    temp_prop = Property("", [], "0", "1 Jan 2023", "", "")
                    temp_prop.dict_to_property(doc.to_dict())
                    properties.append(temp_prop)
            
            start_date = 999999999 # TODO need to change to increment
            
        return properties

    
    def is_end_after_start(self, start_date: str, end_date: str) -> bool:
        '''
            Checks if the end date is after the start date, assuming YYYYMMDD format
        '''
        return int(end_date) >= int(start_date)