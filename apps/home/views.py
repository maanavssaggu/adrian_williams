from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from scraper.main import scrape_listings


# Create your views here.
def home(request):
    # if (settings.LOGGED_IN == False):
    #     return redirect("/")

    return render(request, "home/home.html")

def scrape_listings_req(request):
    print("We are hitting the scrape listings endpoint")
    return redirect("/home/") 