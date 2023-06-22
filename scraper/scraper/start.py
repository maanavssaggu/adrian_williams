from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.find_price_bst import price_withheld_scraper

process = CrawlerProcess(get_project_settings())
# process.crawl(price_withheld_scraper)
# process.start()

# Remove the instance creation and pass the spider class directly to crawl method
process.crawl(price_withheld_scraper, address_line_1="13+Winston+Avenue", address_line_2="EARLWOOD-NSW-2206")
process.start()
