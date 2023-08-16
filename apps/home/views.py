from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from scraper.main import scrape_listings
from scraper.firebase_db import FireBaseDB

# Create your views here.
def home(request):
    if (settings.LOGGED_IN == False):
        return redirect("/")

    return render(request, "home/home.html")

#TODO Akshat
def scrape_listings_req(request):
    suburb_list = dict(request.POST)
    if ("suburbs" not in suburb_list):
        return redirect("/home/")

    suburb_list = suburb_list["suburbs"]

    if (len(suburb_list) == 0):
        return redirect("/home/")

    #scraped_properties = scrape_listings(suburb_list, "20230715")
    fb_db = FireBaseDB()
    # scraped_properties = scrape_listings(suburb_list, "20230715")
    # fb_db.upload(scraped_properties)

    scraped_properties = fb_db.get_properties("20230701", "20230804", suburb_list)

    print(f'scraped properties: {scraped_properties}')
    context = {}
    if scraped_properties == None or scraped_properties == []:
        print('i am here')
        context['no_properties_found'] = True
    else:
        context['properties'] = scraped_properties

    return render(request, "home/home.html", context)