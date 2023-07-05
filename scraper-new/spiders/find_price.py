import scrapy
from scrapy.exceptions import CloseSpider
from .property import Property
from .property_results import PropertyResults
from typing import List


class PriceWithheldScraper(scrapy.Spider):
    '''
    Scrapes just the price for those witheld properties, properties to be queried should be in the following format
        address_line_2 = 'earlwood-nsw-2206'
        address_line_1 = "13+winston+avenue"
        price = 1820000
    '''
    name = "price_scraper"
    allowed_domains = ["domain.com.au"]
    start_urls = ["https://domain.com.au"]

    def __init__(self, property_results: PropertyResults, all_properties_result: List[Property], name: str, **kwargs):
        self.property_results = property_results
        self.all_properties_result = all_properties_result
        super().__init__(name, **kwargs)


    def start_requests(self):
        '''
        Main function of the scraper, starting scraping with minimum price of 0 for each property
        '''
        print("Starting")
        for property in self.property_results.get_price_excluded():
            print("We actually have something here")
            address_line_1 = property.address_line_1
            address_line_2 = property.address_line_2

            property_url = form_URL(address_line_1, address_line_2, 0)
            print("Formed first URL")
            yield scrapy.Request(property_url, callback=self.check_property_exists, meta={'curr_property': property})

        
    def check_property_exists(self, response):
        '''
        Before the price search, the property must exist, if it does not exist, then we can skip the property
        If it does, we need to extract the HTML so we can check it against future scrapes
        '''
        print("Now checking existence")
        curr_property = response.meta['curr_property']

        # Check that inital property actually exists
        property_html = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()
        if not property_html:
            raise CloseSpider('Initial property not found')

        # If it does, form the URL again, and start the price search
        url = form_URL(curr_property.address_line_1, curr_property.address_line_2, 0)
        print("Formed second URL")
        yield scrapy.Request(url, callback=self.search_property, meta={'price': 0, 'curr_property': curr_property, 'property_html': property_html})

    def search_property(self, response):
        '''
        Performs a price search on the specified property, if the property is found, then we can stop the search
        '''
        print("Actually starting search")
        return
        # Extract the property fields from the response
        searched_price = response.meta['price']
        curr_property = response.meta['curr_property']
        property_html = response.meta['property_html']

        # Check if the property exists at the searched price
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()
        
        # If it doesnt, we can end the search and populate the result list with the property
        if not first_property or first_property != property_html:
            property_with_price = self.copy_property(curr_property)
            property_with_price.price = searched_price
            self.all_properties_result.append(property_with_price)
            raise CloseSpider(f"Property found at price: {searched_price}")

        # If it does, we need to search again with a higher price, so increment with 50k
        new_price_to_search = searched_price + 5e4
        url = self.form_URL(curr_property.address_line_1, curr_property.address_line_2, new_price_to_search)
        yield scrapy.Request(url, callback=self.search_property, meta={'price': new_price_to_search, 'curr_property': curr_property, 'property_html': property_html})



    


def copy_property(self, init_property: Property):
    '''
    Copies the property object and adds it to the list of properties
    '''
    property_copy = Property(init_property.address_line_1, None, init_property.price, init_property.sold_status_date, init_property.property_url, init_property.property_id)
    property_copy.address_line_2 = init_property.address_line_2
    return property_copy

def form_URL(ad1, ad2, price):
    '''
    Given the property fields, forms the URL to be scraped
    '''
    return f"https://www.domain.com.au/sold-listings/{ad2}/?price={price}-any&sort=dateupdated-desc&street={ad1}"