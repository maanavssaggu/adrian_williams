from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.find_price import price_withheld_scraper
from spiders.domain_scraper import DomainScraperSpider
from spiders.property_results import PropertyResults
from typing import List

import os 
import csv


def scrape_listings(suburb_list: List[str], time_period: str) -> PropertyResults:
    """
        Scrape the listings for the given suburb list and time period, places in two separate lists
        which is represented by the PropertyResults object
    """
    # Initialise the PropertyResults object
    property_results = PropertyResults()

    # Define configs and scrape listings
    process = CrawlerProcess(get_project_settings())
    process.crawl(DomainScraperSpider,
                suburb_list = suburb_list,
                time_period = time_period,
                property_results_obj = property_results,
                name='domain_scraper')
    process.start()

    print(len(property_results._price_included))
    print(len(property_results._price_excluded))

    return property_results


suburb_list = ['Camperdown-NSW-2050', 'Newtown-nsw-2042']
scrape_listings(suburb_list = suburb_list, time_period = '1y')


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


