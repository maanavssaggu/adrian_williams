from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
def home(request):
    if (settings.LOGGED_IN == False):
        return redirect("/")

    return render(request, "home/home.html")