from scrapy import Spider, Request
import re
from datetime import datetime, timedelta
from .property import Property
from typing import List

class DomainScraperSpider(Spider):
    name = "domain_scraper"
    allowed_domains = ["domain.com.au"]
    start_urls = ["https://domain.com.au"]

    def __init__(self, suburb_list: List[str], time_period: str, name: str, all_properties: List[Property], **kwargs):
        '''
        Scraper instance is specific to a suburb and time period
        '''
        self.suburb_list = suburb_list
        self.time_period = int(time_period)
        self.all_properties = all_properties

        super().__init__(name, **kwargs)

    def start_requests(self):
        '''
        "main" function of the scraper, starting scraping from the first page of the search results
        '''
        for suburb in self.suburb_list:
            starting_page_number = 1
            domain_dot_com_URL = f"https://www.domain.com.au/sold-listings/{suburb}/?sort=solddate-desc&page={starting_page_number}"
            yield Request(
                url=domain_dot_com_URL,
                callback=self.parse_search_results,
                meta={'suburb': suburb, 'page_number': starting_page_number}
            )

    def parse_search_results(self, response):
        '''
        Processes the search results page, and then moves onto the next page
        '''
        # Extract the parameters from the meta dictionary
        suburb = response.meta['suburb']
        page_number = response.meta['page_number']

        # Extract property list from the search results page
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]')
        property_list = response.xpath('//li[@class="css-1qp9106"]')
        property_list = first_property + property_list

        # Extract last page number
        last_page = response.xpath('//div[@class="css-1ytqxcs"]/a[@data-testid="paginator-page-button"]/text()').getall()[-1]

        # Process each property and cast to property object
        for property_item in property_list:
            # Extract all data from HTML
            address_line1 = property_item.xpath(".//a/h2/span[@data-testid='address-line1']/text()").get()
            address_line2 = property_item.xpath('.//h2[@data-testid="address-wrapper"]/span[@data-testid="address-line2"]/span/text()').getall()
            price = property_item.xpath(".//p[@data-testid='listing-card-price']/text()").get()
            sold_status = property_item.xpath('.//div[@data-testid="listing-card-tag"]/span[@class="css-1nj9ymt"]/text()').get()
            property_url = property_item.xpath('.//a/@href').get()
            property_id = re.search(r'(\d+)$', property_url).group()
            
            # gets date of current property 
            current_date = sold_status_to_date(sold_status)

            # Stop searching if we are past last monday 
            if (self.time_period >= int(current_date)):
                return
            
            # Create property object and add to property results
            property_obj = Property(address_line1, address_line2, price, sold_status, property_url, property_id)

            # Check if property price was found 
            if property_obj.price == -1:
                address_line_1 = property_obj.address_line_1
                address_line_2 = property_obj.address_line_2

                property_url = form_URL(address_line_1, address_line_2, 0)
                yield Request(property_url, callback=self.check_property_exists, meta={'curr_property': property_obj})
            else:
                self.all_properties.append(property_obj)

            # self.property_results.add_property(property_obj)

        # Scrape next page if it exists
        if (page_number < last_page):
            next_page_number = page_number + 1
            domain_search_url = f'https://www.domain.com.au/sold-listings/{suburb}/?sort=solddate-desc&page={next_page_number}'
            yield Request(
                url=domain_search_url,
                callback=self.parse_search_results,
                meta={'suburb': suburb, 'page_number': next_page_number}
            )
        

    def check_property_exists(self, response):
        '''
        Before the price search, the property must exist, if it does not exist, then we can skip the property
        If it does, we need to extract the HTML so we can check it against future scrapes
        '''
        curr_property = response.meta['curr_property']

        # Check that inital property actually exists
        property_html = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()
        if not property_html:
            return

        # If it does, form the URL again, and start the price search
        url = form_URL(curr_property.address_line_1, curr_property.address_line_2, 5e6)
        yield Request(url, callback=self.search_property, meta={'curr_property': curr_property, 
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
            curr_property.set_price(int((low + high) / 2))
            self.all_properties.append(curr_property)
            return

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
        yield Request(url, callback=self.search_property, meta={'curr_property': curr_property, 
                                                                       'property_html': property_html,
                                                                       'low': low,
                                                                       'high': high})

def form_URL(ad1, ad2, price):
    '''
    Given the property fields, forms the URL to be scraped
    '''
    return f"https://www.domain.com.au/sold-listings/{ad2}/?price={price}-any&sort=dateupdated-desc&street={ad1}"

def sold_status_to_date(sold_status):
    # Use regular expression to find the date part in the string
    date_str = re.search(r'\d+\s\w+\s\d{4}', sold_status).group()

    # Parse the extracted date string into a datetime object
    date_obj = datetime.strptime(date_str, "%d %b %Y")

    # Convert the datetime object to the desired format
    new_date_str = date_obj.strftime("%Y%m%d")

    return new_date_str
    
