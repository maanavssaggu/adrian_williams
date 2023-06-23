from re import sub
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.find_price_bst import price_withheld_scraper
from spiders.domain_scraper import DomainScraperSpider

import os 
import csv

# gets list of propertys 
# FIXME add a logic which stops searching if there are propertys alredy in our database

process = CrawlerProcess(get_project_settings())
process.crawl(DomainScraperSpider)
process.start()

# # Get the absolute path of the directory where the script is located
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Define your paths
# rel_path = "../../data/price_excluded"
# exc_property_folder_path = os.path.join(script_dir, rel_path)

# for file in os.listdir(exc_property_folder_path):
#     if file.endswith('.csv'):
#         print(file)
#         file_path = os.path.join(exc_property_folder_path, file)

#         with open(file_path, 'r') as suburb:
#             #suburb_name = str.split(file, '-')[0] #gets name of suburb from name of file
#             suburb_dict = csv.DictReader(suburb)
#             for i, property in enumerate(suburb_dict):
#                 ad1 = str(property['address_line1'])
#                 ad2 = str(property['address_line2'])
#                 is_price_witheld = property['price']=='Price Withheld'
#                 #print(f"property['price'] {property['price']}")
               
#                 #only search if need to 
#                 if(is_price_witheld):
#                     print(f'i: {i}') 
#                     process.crawl(price_withheld_scraper, address_line_1="13+Winston+Avenue", address_line_2="EARLWOOD-NSW-2206", file_path_given=file_path, row_index = i)
#                     process.start()
            

            

# # need: ad_line1, ad_line2
# # process.crawl(price_withheld_scraper, address_line_1="13+Winston+Avenue", address_line_2="EARLWOOD-NSW-2206")
# # process.start()


