from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider
import re
from datetime import datetime, timedelta
from .property import Property
from .property_results import PropertyResults
import re
from datetime import datetime, timedelta
from typing import List

class DomainScraperSpider(Spider):
    name = "domain_scraper"
    allowed_domains = ["domain.com.au"]
    start_urls = ["https://domain.com.au"]

    def __init__(self, suburb_list: List[str], time_period: str, name: str, property_results_obj: PropertyResults, **kwargs):
        '''
        Scraper instance is specific to a suburb and time period
        '''
        self.suburb_list = suburb_list
        self.time_period = time_period
        self.property_results = property_results_obj

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
                meta={'suburb': suburb, 'page_number': starting_page_number, 'first_property_sold_date': None}
            )

    def parse_search_results(self, response):
        '''
        Processes the search results page, and then moves onto the next page
        '''
        # Extract the parameters from the meta dictionary
        suburb = response.meta['suburb']
        page_number = response.meta['page_number']
        first_property_sold_date = response.meta['first_property_sold_date']

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

            # set the first property 
            if first_property_sold_date is None:
                first_property_sold_date = current_date

            # get our cutoff date 
            search_to_date = last_monday_date(first_property_sold_date)

            # Stop searching if we are past last monday 
            if (is_before(search_to_date, current_date)):
                raise CloseSpider('Searched up until required date')
            
            # Create property object and add to property results
            property_obj = Property(address_line1, address_line2, price, sold_status, property_url, property_id)
            self.property_results.add_property(property_obj)

        # Scrape next page if it exists
        if (page_number < int(last_page)):
            next_page_number = page_number + 1
            domain_search_url = f'https://www.domain.com.au/sold-listings/{suburb}/?sort=solddate-desc&page={next_page_number}'
            yield Request(
                url=domain_search_url,
                callback=self.parse_search_results,
                meta={'suburb': suburb, 'page_number': next_page_number, 'first_property_sold_date': first_property_sold_date}
            )
        else:
            raise CloseSpider('Searched up until required date')
            
            

"""
Converts sold status to easier to compute data -> this function should be relocated
"""

def sold_status_to_date(sold_status):
    remaining_string = re.split(r'(\d+)', sold_status, maxsplit=2)[1:-1]
    month = remaining_string[1].strip()
    month_mapping = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }

    try:
        if month in month_mapping:
            month_number = month_mapping[month]
    except Exception as e:
        print(e)
        
    remaining_string = remaining_string[0] + str(month_number) + remaining_string[2]
    return remaining_string

"""
Calculates date of the last monday from current week 
 i.e. if today is the 12/6 Mon output: 5/6 Mon 
      or today is the 15/6 Thurs output: 5/6 Mon
"""

def last_monday_date(date_string):
    
    """
        Returns a date of last monday from todays date
    
        input: date with format "ddmmyyyy"
        output: date of last monday "ddmmyyyy"
    """
    
    date = int(date_string[0:2])
    month = int(date_string[2:4])
    year = int(date_string[4:])
    
    input_date = datetime(year, month, date)

    # Calculate the difference in days between the input date and the previous Monday
    if input_date.weekday() == 0: # if the input date is Monday
        return input_date.date().strftime("%d%m%Y")
    else:
        days_to_monday = input_date.weekday() 
        delta = timedelta(days=days_to_monday)

        # Subtract the timedelta to get the date of the previous Monday
        previous_monday = input_date - delta
        return previous_monday.date().strftime("%d%m%Y")


def is_before(curr, compareTo):
    """
        Returns if current date is before another date 
    
        input: two dates with format "ddmmyyyy"
        output: true/false
    """
    
    curr = datetime.strptime(curr, "%d%m%Y")
    compareTo = datetime.strptime(compareTo, "%d%m%Y")
    print(curr, compareTo)
    return curr>compareTo
    
