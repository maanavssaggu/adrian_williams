import sys
from scraper.firebase_db import FireBaseDB
from scraper.spiders.property import Property
from scraper.main import scrape_listings
from datetime import datetime, timedelta

fb_db = FireBaseDB()

suburb_list = [
    'ABBOTSFORD-NSW-2046',
    # ... (other suburbs)
    'WESTGATE-NSW-2048'
]

def last_monday():
    today = datetime.today()
    last_monday = today - timedelta(days=today.weekday() + 1)
    return last_monday.strftime("%Y%m%d")

print(last_monday())  # Output: date of last Monday in YYYYMMDD format

def run_scraper():
    last_monday_date = last_monday() # Fixed variable name conflict
    for suburb in suburb_list:
        print(f"scraping: {suburb} right now")
        data = scrape_listings([suburb], last_monday_date)
        fb_db.upload(data)
        print(f"\n. finished scraping: {suburb} and uploaded it to Firebase. It had {len(data)} properties")

if __name__ == "__main__":
    run_scraper()  # Just call the function directly
