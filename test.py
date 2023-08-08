import sys 
sys.path.append("/Users/sickkent/Documents/aw-wsr/adrian_williams/scraper/spiders/")
print(sys.path)

from scraper.firebase_db import FireBaseDB
from scraper.spiders.property import Property
from scraper.main import scrape_listings

fb_db = FireBaseDB()

# res = fb_db.get_properties("20200101", "20230101", ["CAMPERDOWN-NSW-2050", "NEWTOWN-NSW-2042"])

# # fb_db = FireBaseDB()

suburb_list =[
 'ABBOTSFORD-NSW-2046',
 'ALEXANDRIA-NSW-2015',
 'ANNANDALE-NSW-2038',
 'ASHBURY-NSW-2193',
 'ASHFIELD-NSW-2131',
 'BALMAIN-NSW-2041',
 'BALMAIN-EAST-NSW-2041',
 'BEACONSFIELD-NSW-2015',
 'BELFIELD-NSW-2191',
 'BIRCHGROVE-NSW-2041',
 'BREAKFAST-POINT-NSW-2137',
 'BURWOOD-NSW-2134',
 'BURWOOD-HEIGHTS-NSW-2136',
 'CABARITA-NSW-2137',
 'CAMPERDOWN-NSW-2050',
 'CANADA-BAY-NSW-2046',
 'CHISWICK-NSW-2046',
 'CLEMTON-PARK-NSW-2206',
 'CONCORD-NSW-2137',
 'CONCORD-WEST-NSW-2138',
 'CROYDON-NSW-2132',
 'CROYDON-PARK-NSW-2133',
 'DRUMMOYNE-NSW-2047',
 'DULWICH-HILL-NSW-2203',
 'EARLWOOD-NSW-2206',
 'ENFIELD-NSW-2136',
 'ENFIELD-SOUTH-NSW-2133',
 'ENMORE-NSW-2042',
 'ERSKINEVILLE-NSW-2043',
 'EVELEIGH-NSW-2015',
 'FIVE-DOCK-NSW-2046',
 'FOREST-LODGE-NSW-2037',
 'GLEBE-NSW-2037',
 'HABERFIELD-NSW-2045',
 'HOMEBUSH-NSW-2140',
 'HOMEBUSH-BAY-NSW-2127',
 'HOMEBUSH-SOUTH-NSW-2140',
 'HOMEBUSH-WEST-NSW-2140',
 'HURLSTONE-PARK-NSW-2193',
 'LEICHHARDT-NSW-2040',
 'LEWISHAM-NSW-2049',
 'LIBERTY-GROVE-NSW-2138',
 'LILLYFIELD-NSW-2040',
 'MARRICKVILLE-NSW-2204',
 'MARRICKVILLE-METRO-NSW-2204',
 'MARRICKVILLE-SOUTH-NSW-2204',
 'MISSENDEN-ROAD-NSW-2050',
 'MORTLAK-NSW-2137',
 'NEWINGTON-NSW-2127',
 'NEWTOWN-NSW-2042',
 'NORTH-STRATHFIELD-NSW-2137',
 'PETERSHAM-NSW-2049',
 'PETERSHAM-NORTH-NSW-2049',
 'RHODES-NSW-2138',
 'ROD-POINT-NSW-2046',
 'ROZELLE-NSW-2039',
 'RUSSELL-LEA-NSW-2046',
 'ST-PETERS-NSW-2044',
 'STANMORE-NSW-2048',
 'STRATHFIELD-NSW-2135',
 'STRATHFIELD-SOUTH-NSW-2136',
 'SUMMER-HILL-NSW-2130',
 'SYDENHAM-NSW-2044',
 'TEMPE-NSW-2044',
 'THE-UNIVERSITY-OF-SYDNEY-NSW-2006',
 'ULTIMO-NSW-2007',
 'UNDERCLIFFE-NSW-2372',
 'WAREEMBA-NSW-2046',
 'WENTWORTH-POINT-NSW-2127',
 'WESTGATE-NSW-2048'
]

# suburb_list =[
#  'ALEXANDRIA-NSW-2015',
#  'ANNANDALE-NSW-2038',
# ]
#res = fb_db.get_properties("20230701", "20230804", ["NEWTOWN-NSW-2042"])

if __name__ == "__main__":
    data = scrape_listings(['ALEXANDRIA-NSW-2015'], "20230725")
    # fb_db.upload(data)
    # x = fb_db.get_properties("20230701", "20230804", ["ABBOTSFORD-NSW-2046"])
    # print(x)
    #print(len(res))





# suburb_list = ["ROZELLE-NSW-2039"]

# data = scrape_listings(suburb_list, "20230715")
# # print(type(data))
# # fb_db.upload(data)
# # self, address_line_1: str, address_line_2: List[str], price: str, sold_status_date: str, property_url: str, property_id: str):

# # prop = Property("123 Test St", ["CAMPERDOWN", "NSW", "2050"], "$1,000,000", "Sold at auction 26 Jan 2023", "https://www.google.com/maps", "1234")

# # query = [prop]

# # fb_db.upload(properties=query)

# # print(res)