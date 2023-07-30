from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scrape_listings_req/', views.scrape_listings_req, name='scrape_listings_req'),
]