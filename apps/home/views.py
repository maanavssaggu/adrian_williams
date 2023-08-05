from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from scraper.main import scrape_listings


# Create your views here.
def home(request):
    # TODO uncomment this when login is implemented
    # if (settings.LOGGED_IN == False):
    #     return redirect("/")

    return render(request, "home/home.html")

def scrape_listings_req(request):
    suburb_list = dict(request.POST)
    if ("suburbs" not in suburb_list):
        return redirect("/home/")

    suburb_list = suburb_list["suburbs"]

    if (len(suburb_list) == 0):
        return redirect("/home/")

    scraped_properties = scrape_listings(suburb_list, "1y")

    context = {}
    context['properties'] = scraped_properties

    return render(request, "home/home.html", context)