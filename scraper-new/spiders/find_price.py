import scrapy
from scrapy.exceptions import CloseSpider
import time

property = "13 Winston Avenue,EARLWOOD NSW 2206"
address_line_2 = 'earlwood-nsw-2206'
address_line_1 = "13+winston+avenue"
init_price = int(5e4)

# price solde at 1820000

def URL(ad1, ad2, price):
    return f"https://www.domain.com.au/sold-listings/{ad2}/?price={price}-any&sort=dateupdated-desc&street={ad1}"

class price_withheld_scraper(scrapy.Spider):
    
    prices = []
    name = "price_finder_basic"

    def __init__(self, name=None, **kwargs):
        self.property_present = None
        self.property_price = 0
        self.start_time = None

    def start_requests(self):
        self.start_time = time.time()  # Log the start time
        url = URL(address_line_1, address_line_2, init_price)
        print(url)
        yield scrapy.Request(url, callback=self.initial_parse)

    def initial_parse(self, response):
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()

        if not first_property:
            raise CloseSpider('Initial property not found.')

        self.property_present = first_property
        init_price = int(1e6)
        for i in range (init_price, int(5e6), int(5e4)):
            print(f"${i}")
            self.logger.info(f"Property disappeared at price: {self.property_price}")
            url = URL(address_line_1, address_line_2, i)
            yield scrapy.Request(url, callback=self.parse, meta={'price': i})

    def parse(self, response):
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()
        price = response.meta['price']

        if not first_property or first_property != self.property_present:
            self.property_price = price
            self.prices.append(self.property_price)
            print(f"Property disappeared at price: {self.property_price}")
            raise CloseSpider(f'Property disappeared. Last seen price: {self.property_price}')