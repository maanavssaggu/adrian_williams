from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.domain_scraper import DomainScraperSpider
from .spiders.property import Property
from typing import List
from multiprocessing import Process, Queue



def _scrape_listings(suburb_list: List[str], time_period: str, return_queue) -> List[Property]:
    """
        Scrape the listings for the given suburb list and time period
    """

    property_results = []

    # Define configs and scrape listings
    process = CrawlerProcess(get_project_settings())
    process.crawl(DomainScraperSpider,
                suburb_list = suburb_list,
                time_period = time_period,
                all_properties = property_results,
                name='domain_scraper')
    process.start()

    return_queue.put(property_results)



def scrape_listings(suburb_list: List[str], time_period: str) -> List[Property]:
    """
        Wrapper function for the scrape_listings function, this function is used to catch any errors
        that occur during the scraping process and return an empty list if any errors occur

        returns list of Property objects
    """
    # Initialise queue to return the result
    q = Queue()
    
    # Start and run the scraper in a separate process
    process = Process(target=_scrape_listings, args=(suburb_list, time_period, q))
    process.start()
    process.join()

    # Get the result from the queue
    out = q.get()
    return out
