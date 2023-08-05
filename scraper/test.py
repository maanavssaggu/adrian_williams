from firebase_db import FireBaseDB
from spiders.property import Property

fb_db = FireBaseDB()

# self, address_line_1: str, address_line_2: List[str], price: str, sold_status_date: str, property_url: str, property_id: str):

prop = Property("123 Test St", ["CAMPERDOWN", "NSW", "2050"], "$1,000,000", "Sold at auction 26 Jul 2023", "https://www.google.com/maps", "1234")

query = [prop]

fb_db.upload(properties=query)