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

            #print('trying to chuck it into, -------------: ', abs_file_path)

            if not first_property or first_property != self.property_present:
                if price - self.min_price <= int(5e4): # mid_price - minimum <= 50000 
                    print(f"price is: {price}") # within our acceptance range 
                    field_names = ['address_line1', 'address_line2', 'price', 'sold_status_date', 'property_url', 'property_id']
                    write_to_csv(field_names, abs_file_path, self.row_index, self.max_price, self.address_line_1, self.address_line_2)
                    # try:
                    #     with open(abs_file_path, 'r') as file:
                    #         reader = csv.DictReader(file)
                    #         data = list(reader)

                    #     # change price witheld to actual price
                    #     print(f'I am going to add the actual price to row \n {self.row_index} in {abs_file_path} \n for {self.address_line_1} {self.address_line_2}')
                    #     data[self.row_index]['price'] = round_to_nearest_thousand(self.max_price)

                    #     # add the changed data back into the csv 
                    #     with open(abs_file_path, 'w', newline='') as output_file:
                    #         writer = csv.DictWriter(output_file, fieldnames=field_names)
                    #         if is_file_empty(abs_file_path):
                    #             writer.writeheader()
                    #         writer.writerows(data)
                    # except FileNotFoundError:
                    #     print(f"File {abs_file_path} not found.")

                else: # means the property disappeared -> narrow down the search space so its within acceptance range 
                    self.max_price = price # now set the mid price to be the max price 
                    mid_price = (self.max_price + self.min_price) // 2 # new mid = halfway between 
                    url = self.URL(self.address_line_1, self.address_line_2, mid_price) # search through that 
                    yield scrapy.Request(url, callback=self.parse, meta={'price': mid_price}) # crawl to see if its still there 
            else: # property didnt disapear so narrow down the search space 
                if self.max_price - price <= int(5e4):
                    if os.path.isdir(os.path.join(script_dir, exc_property_folder_path)): 
                        field_names = ['address_line1', 'address_line2', 'price', 'sold_status_date', 'property_url', 'property_id']

                        write_to_csv(field_names, abs_file_path, self.row_index, self.max_price, self.address_line_1, self.address_line_2)


                else:
                    self.min_price = price
                    mid_price = (self.max_price + self.min_price) // 2
                    url = self.URL(self.address_line_1, self.address_line_2, mid_price)
                    yield scrapy.Request(url, callback=self.parse, meta={'price': mid_price})

        except:
            raise CloseSpider('Connection lost, will retry')

def write_to_csv(field_names, abs_file_path, data_index_row, price, ad1, ad2):
    field_names = ['address_line1', 'address_line2', 'price', 'sold_status_date', 'property_url', 'property_id']

    try:
        with open(abs_file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)

        # change price witheld to actual price
        print(f'I am going to add the actual price to row \n {data_index_row} in {abs_file_path} \n for {ad1} {ad2}')
        data[data_index_row]['price'] = round_to_nearest_thousand(price)

        # add the changed data back into the csv 
        with open(abs_file_path, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=field_names)
            if is_file_empty(abs_file_path):
                writer.writeheader()
            writer.writerows(data)
    except FileNotFoundError:
        print(f"File {abs_file_path} not found.")

def round_to_nearest_thousand(num):
    return round(num, -3) if num >= 1000 else num

def is_file_empty(file_path):
    """Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return os.path.exists(file_path) and os.path.getsize(file_path) == 0
