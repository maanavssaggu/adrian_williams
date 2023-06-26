import os
import scrapy
from scrapy.exceptions import CloseSpider
import time 
import csv 

class price_withheld_scraper(scrapy.Spider):
    name = "price_finder_bst"

    def __init__(self, address_line_1=None, address_line_2=None, property=None, 
                            file_path_given=None, file_name = None, ame=None, row_index =None, **kwargs):
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.property = property
        self.min_price = int(5e4)
        self.max_price = int(5e6)
        self.property_present = None
        self.start_time = None
        self.file_path_given = file_path_given
        self.row_index = row_index
        self.file_name = file_name
        super().__init__(name=None, **kwargs)

    def start_requests(self):
        self.start_time = time.time()  # Log the start time
        url = self.URL(self.address_line_1, self.address_line_2, self.min_price)
        yield scrapy.Request(url, callback=self.initial_parse)

    def URL(self, ad1, ad2, price):
        url = f"https://www.domain.com.au/sold-listings/{ad2}/?price={price}-any&sort=dateupdated-desc&street={ad1}"
        print(url)
        return url

    def initial_parse(self, response):
        first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()
        self.property_present = first_property
        mid_price = (self.max_price + self.min_price) // 2
        url = self.URL(self.address_line_1, self.address_line_2, mid_price)
        yield scrapy.Request(url, callback=self.parse, meta={'price': mid_price})

    def parse(self, response):
        try:
            first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]').get()
            price = response.meta['price'] # mid price 

            # Define your paths to csv files
            exc_property_folder_path ="../../data/price_excluded"

            # Get absolute path
            script_dir = os.path.dirname(__file__)
            abs_file_path = os.path.join(script_dir, exc_property_folder_path, self.file_name)

            print('trying to chuck it into, -------------: ', abs_file_path)

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
                    if os.path.isdir(os.path.join(script_dir, exc_property_folder_path)): 
                        field_names = ['address_line1', 'address_line2', 'price', 'sold_status_date', 'property_url', 'property_id']

                        try:
                            with open(abs_file_path, 'r') as file:
                                reader = csv.DictReader(file, fieldnames=field_names)
                                if any(item['address_line1'] == self.address_line_1 and 
                                       item['address_line2'] == self.address_line_2 and 
                                       item['price'] == str(price) for item in reader):
                                    print('Skipping - already in list.')
                                else:
                                    with open(abs_file_path, 'a') as file:
                                        writer = csv.writer(file)
                                        writer.writerow([self.address_line_1, self.address_line_2, price, 'Unknown', 'Unknown', 'Unknown'])
                        except FileNotFoundError as e:
                            print(f"Couldn't find the file. Error: {e}")

                else:
                    self.min_price = price
                    mid_price = (self.max_price + self.min_price) // 2
                    url = self.URL(self.address_line_1, self.address_line_2, mid_price)
                    yield scrapy.Request(url, callback=self.parse, meta={'price': mid_price})

        except:
            raise CloseSpider('Connection lost, will retry')



def round_to_nearest_thousand(num):
    return round(num, -3) if num >= 1000 else num
