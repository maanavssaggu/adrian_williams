from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.domain_scraper import DomainScraperSpider
from spiders.property import Property
from typing import List


def scrape_listings(suburb_list: List[str], time_period: str) -> List[Property]:
    """
        Scrape the listings for the given suburb list and time period, places in two separate lists
        which is represented by the PropertyResults object
    """

    res = []

    # Define configs and scrape listings
    process = CrawlerProcess(get_project_settings())
    process.crawl(DomainScraperSpider,
                suburb_list = suburb_list,
                time_period = time_period,
                all_properties = res,
                name='domain_scraper')
    process.start()

    return res
    


suburb_list_test = ["camperdown-nsw-2050"]
time_period_test = "1-year"

all_properties = scrape_listings(suburb_list_test, time_period_test)

print(len(all_properties))

for prop in all_properties:
    print(prop)
