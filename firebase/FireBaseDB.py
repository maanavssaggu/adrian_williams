from curses import doupdate
from distutils.command.upload import upload
import os
import re
from tracemalloc import Snapshot 
from firebase_admin import credentials
import firebase_admin
from firebase_admin import firestore
import datetime
import Query

class FireBaseDB:

    #constructor
    def __init__(self, property_data=None):
        self.property_data = property_data

        # get paths to initilise firebase
        relative_path = "../credentials/aw-wsr-firebase-adminsdk-458m1-cdc8443299.json"
        base_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(base_dir, relative_path)

        # initilise firebase if not already initilised
        cred = credentials.Certificate(absolute_path)
        if not firebase_admin._apps:

            firebase_admin.initialize_app(cred, {
                "databaseURL": "https://aw-wsr-default-rtdb.firebaseio.com/"
            })
            self.db = firestore.client()
            print(self.date_to_unix_timestamp('04042003'))
            print('firebase initilised')
        else:
            # upload any data given in the constructor
            if(property_data!=None):
                upload(self.property_data)

    #upload data to firebase by property id
    def upload(self, data):
        """
        input: Property object, or a dictionary with keys: property_id, price, subrub so far
        output: nothing, but uploads data to firebase 
        """
        
        db = firestore.client()
        property_id = data['property_id']
        doc_ref = db.collection("properties").document(property_id)

        # change dates to unix timestamps
        date = data['date_sold']
        
        #changes date to a timestamp, if already timestamped nothing will change
        date_timestamped = self.date_to_unix_timestamp(date)
        data['date_sold'] = date_timestamped    
        
        #uploads data
        doc_ref.set(data)
        print('uploaded data')

    #checks if property exists by query
    #TODO: implement so it checks multiple suburbs at the same time 
    def check_exists_query(self, query: Query):
        """
        input: query object 
        output: boolean expression as to whether exists, and the property_data if exists
        """

        # if not isinstance(query, Query):
        #     raise TypeError(f"Parameter 'query' must be an instance of Query.")

        date_min = self.date_to_unix_timestamp(query.date_min)
        date_max = self.date_to_unix_timestamp(query.date_max)

        suburb = query.suburb

        db = firestore.client()

        #print(db.collection("properties").get()['date_sold'])

        query_results = db.collection("properties") \
                .where("date_sold", ">=", date_min) \
                .where("date_sold", "<=", date_max) \
                .where("suburb", "==", suburb) \
                .stream()

        ret = []
        for result in query_results:
            data = result.to_dict()
            ret.append(data)
        print(ret)

        # returns False if query doesnt exist 
        if len(ret)==0:
            return False

        # returns true if query exists and the returns list of propertys
        return True, ret


    #deletes a entry from database
    def delete_by_property_id(self, property_id):

        """
        deletes an entry in the firestore
        """
        #TODO
        raise NotImplementedError

    #deletes a entry from database
    def delete_by_query(self, query: Query):

        """
        deletes by querys
        """
        #TODO
        raise NotImplementedError

    # get method to get a property
    def get_property_by_id(self, property_id):

        """
        input: property_id
        output: property data of corresponding id. outputs None if id doesnt exist
        """

        db = firestore.client()

        data_ref = db.collection('properties').document(property_id)
        data = data_ref.get()

        if data.exists:
            print(f'property_exists: {data.to_dict()}')
            return data.to_dict()

        print('property either doesnt exist or is not in our database')
        return None

    def date_to_unix_timestamp(self, input_date):
        """
        input: date string = 'DDMMYYYY'
        output: timestamp int
        """
        print(f'date_to_unix_timestamp input: {input_date}')

        if not self.is_timestamp(input_date):
            print(f"trying to turn this date into a timestamp: \n {input_date}")
            date = datetime.datetime.strptime(input_date, "%d%m%Y")
            timestamp= int(date.timestamp())
            return timestamp
        else:
            return input_date
    
    def date_in_range(date_min, date_max, date_to_consider):
        """
        input: date range, date to consider
        output: true if the date to consider is within range 
                false if the date to consider is not within range
        """
        return date_to_consider>=date_min and date_to_consider<=date_max

    
    def is_timestamp(self, value):
        """
        input: date 
        output: true/False depending on whether or not it is a timestamp
        """
        return isinstance(value, datetime.datetime)
