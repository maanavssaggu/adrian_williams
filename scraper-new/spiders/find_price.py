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
        for property in self.property_results.get_price_excluded():
            address_line_1 = property.address_line_1
            address_line_2 = property.address_line_2

            property_url = form_URL(address_line_1, address_line_2, 0)
            yield scrapy.Request(property_url, callback=self.check_property_exists, meta={'curr_property': property})

        
    def check_property_exists(self, response):
        '''
        Before the price search, the property must exist, if it does not exist, then we can skip the property
        If it does, we need to extract the HTML so we can check it against future scrapes
        '''
        curr_property = response.meta['curr_property']

        # Check that inital property actually exists
        property_html = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()
        if not property_html:
            raise CloseSpider('Initial property not found')

        # If it does, form the URL again, and start the price search
        url = form_URL(curr_property.address_line_1, curr_property.address_line_2, 5e6)
        yield scrapy.Request(url, callback=self.search_property, meta={'curr_property': curr_property, 
                                                                       'property_html': property_html,
                                                                       'low': 0,
                                                                       'high': 1e7})

    def search_property(self, response):
        '''
        Performs a price search on the specified property, if the property is found, then we can stop the search
        '''
        # Extract the property fields from the response
        curr_property = response.meta['curr_property']
        property_html = response.meta['property_html']
        low = response.meta['low']
        high = response.meta['high']

        # If property is found
        if ((high - low) <= 1e5):
            property_with_price = copy_property(curr_property)
            property_with_price.price = (low + high) / 2
            self.all_properties_result.append(property_with_price)
            raise CloseSpider(f"Property found at price: {(low + high) / 2}")

        # Check if the property exists at the searched price
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()
        
        # Update bounds based on whether the property exists or not
        if not first_property or first_property != property_html:
            high = (low + high) / 2
        else:
            low = (low + high) / 2

        # Update price fields
        new_price_to_search = (low + high) / 2
        url = form_URL(curr_property.address_line_1, curr_property.address_line_2, new_price_to_search)
        yield scrapy.Request(url, callback=self.search_property, meta={'curr_property': curr_property, 
                                                                       'property_html': property_html,
                                                                       'low': low,
                                                                       'high': high})
        


def copy_property(init_property: Property):
    '''
    Copies the property object and adds it to the list of properties
    '''
    property_copy = Property(init_property.address_line_1, ["test", "stret"], str(init_property.price), init_property.sold_status_date, init_property.property_url, init_property.property_id)
    property_copy.address_line_2 = init_property.address_line_2
    return property_copy

def form_URL(ad1, ad2, price):
    '''
    Given the property fields, forms the URL to be scraped
    '''
    return f"https://www.domain.com.au/sold-listings/{ad2}/?price={price}-any&sort=dateupdated-desc&street={ad1}"