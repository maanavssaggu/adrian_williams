import scrapy
from scrapy.exceptions import CloseSpider
import time 

class price_withheld_scraper(scrapy.Spider):
    name = "price_finder_bst"

    def __init__(self, address_line_1=None, address_line_2=None, property=None, name=None, **kwargs):
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.property = property
        self.min_price = int(5e4)
        self.max_price = int(5e6)
        self.property_present = None
        self.start_time = None
        super().__init__(name=None, **kwargs)

    def start_requests(self):
        self.start_time = time.time()  # Log the start time
        url = self.URL(self.address_line_1, self.address_line_2, self.min_price)
        yield scrapy.Request(url, callback=self.initial_parse)

    def URL(self, ad1, ad2, price):
        url = f"https://www.domain.com.au/sold-listings/{ad2}/?price={price}-any&sort=dateupdated-desc&street={ad1}"
        return url

    def initial_parse(self, response):
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()
        self.property_present = first_property
        mid_price = (self.max_price + self.min_price) // 2
        url = self.URL(self.address_line_1, self.address_line_2, mid_price)
        yield scrapy.Request(url, callback=self.parse, meta={'price': mid_price})

    def parse(self, response):
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()
        price = response.meta['price'] # mid price 

        if not first_property or first_property != self.property_present:
            if price - self.min_price <= int(5e4): # mid_price - minimum <= 50000 
                print(f"Property disappeared at price: {price}") # within our acceptance range 
            else: # means the property disappeared 
                self.max_price = price # now set the mid price to be the max price 
                mid_price = (self.max_price + self.min_price) // 2 # new mid = halfway between 
                url = self.URL(self.address_line_1, self.address_line_2, mid_price) # search through that 
                yield scrapy.Request(url, callback=self.parse, meta={'price': mid_price})
        else:
            if self.max_price - price <= int(5e4):
                print(f"Property disappeared at price: {self.max_price}")
            else:
                self.min_price = price
                mid_price = (self.max_price + self.min_price) // 2
                url = self.URL(self.address_line_1, self.address_line_2, mid_price)
                yield scrapy.Request(url, callback=self.parse, meta={'price': mid_price})
