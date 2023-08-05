from firebase_admin import auth, credentials
import firebase_admin
import os
import requests
import json

class Auth:
    """
    call this class for new user to add them to the database.
    """

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

        self.api_key = "AIzaSyAjbnS3xKUB0HryMJCrZiLithqhu0b87II"

    def create_firebase_user(self, email, password) -> bool:
        '''
        Creates a firebase user with the given email and password
        '''
        if (email is None or password is None):
            print('Email or Password is none')
            return False

        try:
            auth.create_user(email=email, password=password)
            return True
        except Exception as e:
            print(f'Error creating user: {e}')
            return False

    def authenticate_user_with_email_and_password(self, email, password) -> bool:
        '''
        Verifies if a user is an authorised user
        '''
        # Creates URL request to send to public Google API
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(self.api_key)
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"email": email, "password": password, "returnSecureToken": True})

        # Run the request
        response_obj = requests.post(request_ref, headers=headers, data=data).json()

        # If the response echos the email, then it was valid, otherwise it was not
        if 'email' in response_obj:
            return True
        
        return False  