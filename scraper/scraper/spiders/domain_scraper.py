from scrapy import Spider, Request
import requests
import re
import csv
from datetime import datetime, timedelta
import time 
# from utils import last_monday_date, sold_status_to_date


class DomainScraperSpider(Spider):
    name = "domain_scraper"
    allowed_domains = ["domain.com.au"]
    start_urls = ["https://domain.com.au"]

    def start_requests(self):
        suburb_list = ['earlwood-nsw-2206', 'Newtown-nsw-2042', 'Camperdown-NSW-2050']
        for suburb in suburb_list:
            page_number = 1  # starts from 1
            domain_dot_com_URL = f"https://www.domain.com.au/sold-listings/{suburb}/?sort=solddate-desc&page={page_number}"
            yield Request(
                url=domain_dot_com_URL,
                callback=self.parse_search_results,
                meta={'suburb': suburb, 'page_number': page_number, 'first_property_sold_date': None}
            )

    def parse_search_results(self, response):
        start = time.time()
        suburb = response.meta['suburb']
        page_number = response.meta['page_number']
        first_property_sold_date = response.meta['first_property_sold_date']

        property_list = response.xpath('//li[@class="css-1qp9106"]')
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]')
        property_list = first_property + property_list

        # Get all page numbers
        page_numbers = response.xpath('//div[@class="css-1ytqxcs"]/a[@data-testid="paginator-page-button"]/text()').getall()
        last_page = page_numbers[-1]

        search_to_date = 0

        # Process each property and write to the appropriate file
        for i, property_item in enumerate(property_list):
            address_line1 = property_item.xpath(".//a/h2/span[@data-testid='address-line1']/text()").get()
            address_line2 = property_item.xpath('.//h2[@data-testid="address-wrapper"]/span[@data-testid="address-line2"]/span/text()').getall()
            price = property_item.xpath(".//p[@data-testid='listing-card-price']/text()").get()
            sold_status = property_item.xpath('.//div[@data-testid="listing-card-tag"]/span[@class="css-1nj9ymt"]/text()').get()

            # gets date of current property 
            current_date = sold_status_to_date(sold_status)

            # set the first property 
            if first_property_sold_date is None:
                first_property_sold_date = current_date

            # get our cutoff date 
            search_to_date = last_monday_date(first_property_sold_date)

            # Stop searching if we are past last monday 
            if (is_before(search_to_date, current_date)):
                print('stopped here')
                break

            data = {
                'address_line1': address_line1,
                'address_line2': ' '.join(address_line2),  # joins the list into a string
                'price': price,
                'sold_status_date': sold_status,
            }

            print('Extracted data:', address_line1, address_line2, price, sold_status)

            # Write the data to the appropriate file
            suburb_price_included = f'/Users/sickkent/Documents/adrian_williams_software/data/price_included/{suburb}.csv'
            suburb_price_excluded = f'/Users/sickkent/Documents/adrian_williams_software/data/price_excluded/{suburb}_excluded.csv'

            field_names = ['address_line1', 'address_line2', 'price', 'sold_status_date']

            if (price == "Price Withheld"):
                with open(suburb_price_excluded, 'a', newline='') as exc_price_file:
                    writer_price_exc = csv.DictWriter(exc_price_file, fieldnames=field_names)
                    if exc_price_file.tell() == 0: # initilise csv file
                        writer_price_exc.writeheader()
                    writer_price_exc.writerow(data) # update csv file
            else:
                with open(suburb_price_included, 'a', newline='') as price_inc_file:
                    writer_price_inc = csv.DictWriter(price_inc_file, fieldnames=field_names)
                    if price_inc_file.tell() == 0:
                        writer_price_inc.writeheader()
                    writer_price_inc.writerow(data)

        end = time.time()
        total_time = end - start

        formatted_time = "{:.2f}".format(total_time)
        self.logger.info(f"Total time taken: {formatted_time} seconds")

        for page_num in range(page_number + 1, int(last_page) + 1):
            domain_search_url = f'https://www.domain.com.au/sold-listings/{suburb}/?sort=solddate-desc&page={page_num}'
            yield Request(
                url=domain_search_url,
                callback=self.parse_search_results,
                meta={'suburb': suburb, 'page_number': page_num, 'first_property_sold_date': first_property_sold_date}
            )
            
        

import re
from datetime import datetime, timedelta

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
    