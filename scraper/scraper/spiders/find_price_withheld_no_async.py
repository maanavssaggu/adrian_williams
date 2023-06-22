import scrapy
from scrapy import signals
from scrapy.exceptions import CloseSpider

property = "13 Winston Avenue,EARLWOOD NSW 2206"
address_line_2 = 'earlwood-nsw-2206'
address_line_1 = "13+winston+avenue"
init_price = int(15e5)

# price solde at 1820000

def URL(ad1, ad2, price):
    return f"https://www.domain.com.au/sold-listings/{ad2}/?price={price}-any&sort=dateupdated-desc&street={ad1}"

class price_withheld_scraper(scrapy.Spider):
    
    name = "price_finder_no_async"

    def __init__(self, name=None, **kwargs):
        self.property_present = None
        self.property_price = 0

    def start_requests(self):
        url = URL(address_line_1, address_line_2, init_price)
        print(url)
        yield scrapy.Request(url, callback=self.initial_parse)

    def initial_parse(self, response):
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()

        if not first_property:
            raise CloseSpider('Initial property not found.')

        self.property_present = first_property
        self.price_to_check = int(15e5)  # start with this price
        url = URL(address_line_1, address_line_2, self.price_to_check)
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()

        if not first_property or first_property != self.property_present:
            self.property_price = self.price_to_check
            print(f"Property disappeared at price: {self.property_price}")
            raise CloseSpider(f'Property disappeared. Last seen price: {self.property_price}')
        else:
            self.price_to_check += int(5e4)
            if self.price_to_check <= int(5e6):
                url = URL(address_line_1, address_line_2, self.price_to_check)
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider, reason):
        self.logger.info(f'Spider closed: {reason}')
        # do any final tasks or cleanup here


# import requests
# import scrapy 


# #property = "13 Winston Avenue,EARLWOOD NSW 2206,Price Withheld,Sold at auction 10 Jun 2023"
# property = "13 Winston Avenue,EARLWOOD NSW 2206"
# adress_line_2 = 'earlwood-nsw-2206'
# address_line_1 = "33/37+iredale+street"
# price = 0 # init value 

# URL = f"https://www.domain.com.au/sold-listings/{adress_line_2}/?price={price}"
# # "https://www.domain.com.au/sold-listings/newtown-nsw-2042/?price=500000-any&sort=dateupdated-desc&street=33%2f37+iredale+street"


# def URL(ad1, ad2, price):
#     """
#         address_line_2: earlwood-nsw-2206
#         address_line_1: 33/37+iredale+street
#     """

#     return f"https://www.domain.com.au/sold-listings/{ad2}/?price={price}-any&sort=dateupdated-desc&street={ad1}"


# class price_withheld_scraper(scrapy.Spider):
    
#     name = "price_finder"

#     def __init__(self, name=None, **kwargs):
#         self.property_present = -1 
#         self.property_price = 0


#     def start_requests(self):
#         init_price = 0 
#         base_url = URL(address_line_1, adress_line_2, init_price)
#         for i in range (init_price, int(5e6), int(5e4)):
#             url = URL(address_line_1, adress_line_2, i)
#             yield scrapy.Request(
#                 url, 
#                 callback=self.parse,
#                 meta={'price': i}
#             )

#     def parse(self, response, **kwargs):
#         first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]')
#         sold_status = first_property.xpath('.//div[@data-testid="listing-card-tag"]/span[@class="css-1nj9ymt"]/text()').get()
#         price = response.meta['price']
#         print(sold_status)
#         # gets date of current property 
#         current_date = (sold_status)
#         if (self.property_present==0 or self.property_present==current_date):
#             self.property_present = current_date
#         else:
#             # property doesnt_exist 
#             self.property_price = price
#             print(str(price))
#             return property + self.property_price