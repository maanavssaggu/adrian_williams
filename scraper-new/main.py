from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.find_price import PriceWithheldScraper
from spiders.domain_scraper import DomainScraperSpider
from spiders.property_results import PropertyResults
from spiders.property import Property
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

    for property in property_results.get_price_included():
        print(property)

    return property_results


suburb_list = ['Camperdown-NSW-2050']
scrape_listings(suburb_list = suburb_list, time_period = '1y')


def find_prices_of_price_witheld(property_results_obj: PropertyResults) -> List[Property]:
    """
    From the property results, find all prices from excluded list and scrape them
    """
    # We will atleast have the included property results list as a result
    all_properties = property_results_obj.get_price_included().copy()
    
    # Define configs and scrape prices only
    process = CrawlerProcess(get_project_settings())
    process.crawl(PriceWithheldScraper,
                property_results = property_results_obj,
                all_properties_result = all_properties,
                name='price_scraper')      
    process.start()

    return all_properties





