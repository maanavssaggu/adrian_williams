"""
Scrapes Domain.com website and stores property's sold within the last week of a certain area in 
Sydney. 
"""

suburb = "earlwood-nsw-2206"
#TODO implement in a method to iterate through all regions in /subrubs/ dir

page_number = 1 # starts from 1 

URL = f"https://www.domain.com.au/sold-listings/{suburb}/?sort=solddate-desc&page={page_number}"

#TODO add a method to only search up to a week ago - from the current monday 

