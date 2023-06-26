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

# # to run the find price excluded script 
# # Get the absolute path of the directory where the script is located
# script_dir = os.path.dirname(os.path.abspath(__file__))

# Define your paths
rel_path = "../data/price_excluded"
exc_property_folder_path = rel_path

for file in os.listdir(exc_property_folder_path):
    if file.endswith('.csv'):
        print(file)
        file_path = os.path.join(exc_property_folder_path, file)
        print('file path ----------------', file_path)
        with open(file_path, 'r') as suburb:
            suburb_dict = csv.DictReader(suburb)
            for i, property in enumerate(suburb_dict):
                ad1 = str(property['address_line1'])
                ad2 = str(property['address_line2'])
                is_price_withheld = property['price'] == 'Price Withheld'
                file_name = file
                print(f'{ad1}, {ad2}, {is_price_withheld}')
                # only search if needed
                if is_price_withheld:
                    print(f'i: {i}') 
                    ad1 = ad1.replace(" ", "+")
                    ad2 = ad2.replace(" ", "-")
                    # print('ad1: ', ad1)
                    # print('ad2: ', ad2)
                    process.crawl(
                        price_withheld_scraper,
                        address_line_1=ad1,
                        address_line_2=ad2,
                        file_path_given=file_path,
                        row_index=i,
                        file_name = file_name,
                    )
process.start()



# Start the crawling process
# process.start()





