import scrapy
from scrapy.exceptions import CloseSpider

property = "13 Winston Avenue,EARLWOOD NSW 2206"
address_line_2 = 'earlwood-nsw-2206'
address_line_1 = "13+winston+avenue"
init_price = int(5e4)

def URL(ad1, ad2, price):
    return f"https://www.domain.com.au/sold-listings/{ad2}/?price={price}-any&sort=dateupdated-desc&street={ad1}"

class price_withheld_scraper(scrapy.Spider):
    name = "price_finder_concurrent"

    def __init__(self, name=None, **kwargs):
        self.property_present = None
        self.disappeared_prices = []

    def start_requests(self):
        url = URL(address_line_1, address_line_2, init_price)
        yield scrapy.Request(url, callback=self.initial_parse)

    def initial_parse(self, response):
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()

        if not first_property:
            raise CloseSpider('Initial property not found.')

        self.property_present = first_property
        for i in range (int(1e6), int(5e6), int(5e4)):
            url = URL(address_line_1, address_line_2, i)
            yield scrapy.Request(url, callback=self.parse, meta={'price': i})

    def parse(self, response):
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()
        price = response.meta['price']

        if not first_property or first_property != self.property_present:
            self.disappeared_prices.append(price)
            print(f"Property disappeared at price: {price}")
