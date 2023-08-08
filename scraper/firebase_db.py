import os
from firebase_admin import credentials
import firebase_admin
from firebase_admin import firestore
from .spiders.property import Property
from typing import List
from datetime import datetime, timedelta
import time 

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
            # Create a reference to the document to be stored
            # The document will be stored at /suburbs/{suburb}/properties/{date_property_id}
            print(f'property address: {property.address_line_2}')
            doc_ref = self.db.collection('suburbs').document(property.address_line_2).collection('properties').document(f"{property.date_str}_{property.property_id}")
            
            print(property.property_to_dict())
            # Set the document data
            doc_ref.set(property.property_to_dict())

            # Check if the document exists
            doc = doc_ref.get()

            # Also store the date in the 'dates_parsed' collection
            self.db.collection('dates_parsed').document(property.date_str).set({'date': property.date_str})


    # # TODO FOR MAANAV
    # def get_properties(self, start_date: str, end_date: str, suburbs: List[str]) -> List[Property]:
    #     '''
    #         Given a date range and suburn list, returns a list of sold properties
    #     '''
    #     properties = []
    #     while(self.is_end_after_start(start_date, end_date)):
    #         for suburb in suburbs:
    #             doc_ref = self.db.collection(start_date).document(suburb).collection("properties")
    #             docs = doc_ref.stream()
    #             for doc in docs:
    #                 temp_prop = Property("", [], "0", "1 Jan 2023", "", "")
    #                 temp_prop.dict_to_property(doc.to_dict())
    #                 properties.append(temp_prop)
            
    #         start_date = 999999999 # TODO need to change to increment
            
    #     return properties

    # TODO FOR MAANAV
    def get_properties(self, start_date: str, end_date: str, suburbs: List[str]) -> List[Property]:
        '''
            Given a date range and suburb list, returns a list of sold properties

            Collection -> Document -> Collection -> Document
            Suburbs  -> suburb -> "date-properties" -> property_data

            /suburbs/CAMPERDOWN-NSW-2050/properties/20210212_412
        '''
        properties = []
            
        suburbs_ref = self.db.collection('suburbs')

        for suburb in suburbs:
            print(f'suburb: {suburb}')

            suburb_ref = suburbs_ref.document(suburb)

            doc_snapshot = suburb_ref.get()
            
            # Check if the document ID matches the suburb
            if not doc_snapshot.id == suburb:
                print(f'document ID does not match suburb: {suburb}')
                continue

            print('suburb exists')

            prop_ref = suburb_ref.collection('properties')
            
            # Fetch all properties sold between start_date and end_date
            query = prop_ref.where('date', '>=', int(start_date))
            docs = query.stream()

            for doc in docs:
                temp = doc.to_dict()
                properties.append(temp)

        if properties == []:  # Use [] instead of None to check for no properties
            print('no properties for this query in firebase.')
        return properties
    
    def get_next_date(self, all_dates: List[str], current_date: str) -> str:
        '''
            finds the next date in the dates we have in our db
        '''
        # find all dates in all_dates that are after current_date
        future_dates = [int(date) for date in all_dates if int(date) > int(current_date)]
        if future_dates:
            # return the earliest date that is after current_date
            return min(future_dates)
        else:
            # no more dates available
            return None
    
    def get_all_dates(self) -> List[int]:
        dates = self.db.collection('dates_parsed')
        docs = dates.stream()
        try:
            all_dates = [int(doc.id) for doc in docs]
            print(all_dates)
        except ValueError:
            print("Error: document ID in dates_parsed collection is not a number.")
            all_dates = []
        return all_dates


    
    def increment_date(self, start_date:str) -> str: 
        '''
            increments the date given in YYYYMMDD format and takes into account 
            different months and leap years. 
        '''
        # convert the date string to a datetime object
        date_obj = datetime.strptime(start_date, '%Y%m%d')

        # add one day to the date
        date_obj += timedelta(days=1)

        # convert the new date back to a string and return it
        return date_obj.strftime('%Y%m%d')
    
    def is_end_after_start(self, start_date: str, end_date: str) -> bool:
        '''
            Checks if the end date is after the start date, assuming YYYYMMDD format
        '''
        return int(end_date) >= int(start_date)