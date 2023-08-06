from firebase_db import FireBaseDB
from spiders.property import Property

fb_db = FireBaseDB()

res = fb_db.get_properties("20230726", "20230726", ["CAMPERDOWN-NSW-2050"])

# self, address_line_1: str, address_line_2: List[str], price: str, sold_status_date: str, property_url: str, property_id: str):

# prop = Property("123 Test St", ["CAMPERDOWN", "NSW", "2050"], "$1,000,000", "Sold at auction 26 Jan 2023", "https://www.google.com/maps", "1234")

# query = [prop]

# fb_db.upload(properties=query)

print(res[0])