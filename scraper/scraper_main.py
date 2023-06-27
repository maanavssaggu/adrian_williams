from re import sub
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.find_price_bst import price_withheld_scraper
from spiders.domain_scraper import DomainScraperSpider

import os 
import csv



# gets list of propertys 
def get_property_data(suburb_list=None, time_period=None):
    """
    example of how to run this:
        suburb_list = ['earlwood-nsw-2206', 'Newtown-nsw-2042', 'Camperdown-NSW-2050']
        get_property_data(suburb_list)
    """

    process = CrawlerProcess(get_project_settings())
    process.crawl(DomainScraperSpider,
                suburb_list = suburb_list,
                time_period = time_period)
    process.start()


def find_prices_of_price_witheld():
    """
    just calling this will go through all the csvs in price_excluded and then updata their prices 
    """

    # Define your paths
    rel_path = "../data/price_excluded"
    exc_property_folder_path = rel_path

    process = CrawlerProcess(get_project_settings())

    for file in os.listdir(exc_property_folder_path):
        if file.endswith('.csv'):
            
            file_path = os.path.join(exc_property_folder_path, file)
            
            with open(file_path, 'r') as suburb:
                suburb_dict = csv.DictReader(suburb)
                for i, property in enumerate(suburb_dict):
                    ad1 = str(property['address_line1'])
                    ad2 = str(property['address_line2'])
                    property_id = str(property['property_id'])
                    is_price_withheld = property['price'] == 'Price Withheld'
                    file_name = file
                    
                    # only search if needed
                    if is_price_withheld:
                        print(f'i: {i}') 
                        ad1 = ad1.replace(" ", "+")
                        ad2 = ad2.replace(" ", "-")

                        process.crawl(
                            price_withheld_scraper,
                            address_line_1=ad1,
                            address_line_2=ad2,
                            file_path_given=file_path,
                            row_index=i,
                            file_name = file_name,
                            property_id = property_id,
                        )
    process.start()


# TODO 
# add function to find property price of a specific property and add to the csv 
#suburb_list = ['earlwood-nsw-2206', 'Newtown-nsw-2042', 'Camperdown-NSW-2050']
#get_property_data(suburb_list)
find_prices_of_price_witheld()



