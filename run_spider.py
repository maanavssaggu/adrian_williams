from scraper.main import scrape_listings
from scraper.firebase_db import FireBaseDB
from scraper.spiders.property import Property

import sys

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) < 2:
        print("Usage: python script_name.py suburb1 suburb2 suburb3 ...")
        return
    
    suburbs_to_scrape = sys.argv[1:]  # Get the list of suburbs from command-line arguments

    # Now you can run the web scraping script here and pass the suburbs
    #scrape_listings(suburbs_to_scrape)  # Assuming this is how you pass the suburbs to the spider
    
    # You might want to do something with the scraped data, like storing it in a database
    #firebase_db = FireBaseDB()  # Create a FireBaseDB instance
    for suburb in suburbs_to_scrape:
        print(suburb)
        property_data = scrape_listings(suburb, "20230809")
        print(f"just scraped {suburb} onto the next")
        #firebase_db.store_data(property_data)  # Store the scraped data in the database

if __name__ == "__main__":
    main()
