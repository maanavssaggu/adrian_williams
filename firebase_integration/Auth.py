from asyncio import exceptions
from firebase_admin import auth, exceptions, credentials
import firebase_admin
import os 

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

    def verify_firebase_user(self, email, password) -> bool:
        '''
        Verify a firebase user with the given email and password
        is a valid user
        '''
    
    def user_exists(self, email):

        """
        call this with the email you wanna check exists and it will return true if they 
        exist and false if they do not 
        """
        try:
            user = auth.get_user_by_email(email)
            return True
        except auth.UserNotFoundError as user_not_found:
            print(f'user not found: {user_not_found}')
            return False
        except exceptions.FirebaseError as e:
            raise


myobj = Auth()
myobj.create_firebase_user('akshattest@gmail.com', 'password')

        


        