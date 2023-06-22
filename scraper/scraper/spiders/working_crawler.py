# from scrapy import Spider, Request
# import re

# # TODO add implementation for all suburbs required -> make seperate json file for each 
# class DomainScraperSpider(Spider):
#     name = "domain_scraper"
#     allowed_domains = ["domain.com.au"]
#     start_urls = ["https://domain.com.au"]

#     def start_requests(self):
#         suburb_list = ['earlwood-nsw-2206']
#         for suburb in suburb_list:
#             page_number = 1  # starts from 1
#             domain_dot_com_URL = f"https://www.domain.com.au/sold-listings/{suburb}/?sort=solddate-desc&page={page_number}"
#             yield Request(
#                 url=domain_dot_com_URL,
#                 callback=self.parse_search_results,
#                 meta={'suburb': suburb, 'page_number': page_number}
#             )
#         print(domain_dot_com_URL)

#     def parse_search_results(self, response):
#         suburb = response.meta['suburb']
#         page_number = response.meta['page_number']

        
#         property_list = response.xpath('//li[@class="css-1qp9106"]')
#         first_property = response.xpath('//li[@class="is-first-in-list css-1qp9106"]')
#         property_list = first_property + property_list
       

#         #print(f"p1: {property_list}, has size: {len(property_list)}, has type: {type(property_list)}")
#         #print(f"p2: {property_list_2}, has size: {len(property_list_2)}, has type: {type(property_list_2)}")

#         # extract property data
#         for property_item in property_list:
#             # Extract the property details
#             address_line1 = property_item.xpath(".//a/h2/span[@data-testid='address-line1']/text()").get()
#             address_line2 = property_item.xpath('.//h2[@data-testid="address-wrapper"]/span[@data-testid="address-line2"]/span/text()').getall()
#             print(address_line2)
#             price = property_item.xpath(".//p[@data-testid='listing-card-price']/text()").get()
#             sold_status = property_item.xpath('.//div[@data-testid="listing-card-tag"]/span[@class="css-1nj9ymt"]/text()').get()

#             # Process the extracted data as needed
#             # For example, you can yield a dictionary with the extracted data
#             yield {
#                 'address_line1': address_line1,
#                 'address_line2': address_line2,
#                 'price': price,
#                 'sold_status': sold_status,
#             }

#             print('Extracted data:', address_line1, address_line2, price, sold_status)

#         # Get all page numbers
#         page_numbers = response.xpath('//div[@class="css-1ytqxcs"]/a[@data-testid="paginator-page-button"]/text()').getall()
#         last_page = page_numbers[-1]

#         for page_num in range(page_number + 1, int(last_page) + 1):
#             domain_search_url = f'https://www.domain.com.au/sold-listings/{suburb}/?sort=solddate-desc&page={page_num}'
#             yield Request(
#                 url=domain_search_url,
#                 callback=self.parse_search_results,
#                 meta={'suburb': suburb, 'page_number': page_num}
#             )

# """
# Converts sold status to easier to compute data -> this function should be relocated
# """

# def sold_status_to_date(sold_status):
    
#     #print(f"input: {sold_status}")
#     remaining_string = re.split(r'(\d+)', sold_status, maxsplit=2)[1:-1]
#     month = remaining_string[1].strip()
#     #print(f"extracted month: {month}")
#     month_mapping = {
#         "Jan": "01",
#         "Feb": "02",
#         "Mar": "03",
#         "Apr": "04",
#         "May": "05",
#         "Jun": "06",
#         "Jul": "07",
#         "Aug": "08",
#         "Sep": "09",
#         "Oct": "10",
#         "Nov": "11",
#         "Dec": "12"
#     }

#     if month in month_mapping:
#         month_number = month_mapping[month]
#         print(f'{month} = {month_number}')
#     else:
#         print(f"Invalid month: {month}")
        
#     remaining_string = remaining_string[0]+str(month_number)+remaining_string[2]
#     return remaining_string
