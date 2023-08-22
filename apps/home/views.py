from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.http import FileResponse
from scraper.main import scrape_listings
from scraper.firebase_db import FireBaseDB
from main import last_monday
from main import today_date
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import yellow, green
from typing import List
from reportlab.platypus import Paragraph
from scraper.spiders.property import Property

def generate_basic_pdf(file_path, properties: List[Property]):
    print("i am downloading the pdf")
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Define Arial font size 11
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    style.fontName = 'Arial'
    style.fontSize = 11

    # Set the font and size
    c.setFont("Helvetica", 12)

    current_suburb = None
    y_position = height -100

    line_break = -50
    curr_suburb = ""
    line_height = 20  # Gap between lines
    for property in properties:
        # Check if new suburb, and if so, print suburb header

        

        property_string = turn_property_to_string(property=property)
        c.drawString(100, y_position, property_string)
        y_position = y_position-line_height

        # split if a new suburb 
        suburb = property.address_line_2
        
        if(curr_suburb != suburb):
            y_position = y_position - 30

        curr_suburb = suburb
        # Check if the page is filled, and add a new page if needed
        if y_position < 50:
            c.showPage()
            y_position = height - 50

    c.save()




# Create your views here.
def home(request):
    if (settings.LOGGED_IN == False):
        return redirect("/")

    return render(request, "home/home.html")

#TODO Akshat
def scrape_listings_req(request):
    suburb_list = dict(request.POST)
    if "suburbs" not in suburb_list:
        return redirect("/home/")

    suburb_list = suburb_list["suburbs"]

    if len(suburb_list) == 0:
        return redirect("/home/")

    fb_db = FireBaseDB()

    last_monday_date = last_monday()
    today = today_date()

    scraped_properties = fb_db.get_properties(last_monday, today, suburb_list)
    request.session['scraped_properties'] = scraped_properties 

    print(f'scraped properties: {scraped_properties}')
    context = {}
    if scraped_properties is None or scraped_properties == []:
        print('i am here')
        context['no_properties_found'] = True
    else:
        context['properties'] = scraped_properties

    return render(request, "home/home.html", context)


def generate_pdf_request(request):
    scraped_properties_dict = request.session.get('scraped_properties', [])  # Retrieve from session

    # Convert dictionaries to Property objects
    scraped_properties = []
    for prop_dict in scraped_properties_dict:
        prop = Property("", [], "0", "1 Jan 2023", "", "")
        prop.dict_to_property(prop_dict)
        scraped_properties.append(prop)

    if request.POST.get("generate_pdf") == "true" and scraped_properties:
        file_path = "test.pdf"
        generate_basic_pdf(file_path, scraped_properties)  # Pass properties to the function

        with open(file_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        response = HttpResponse(content=pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="test.pdf"'
        return response

    return redirect("/home/")

def turn_property_to_string(property: Property):
    price = format_price(property.price)
    address_line_1 = property.address_line_1
    address_line_2 = property.address_line_2
    sold_status = property.sold_status_date
     # Split the input by the '-' character
    parts = address_line_2.split('-')
    
    # Return the first part, which is the suburb name, and strip any leading or trailing spaces
    suburb = parts[0].strip()

    # Format the output with fixed-width fields
    output = address_line_1 + ", " + suburb + ", " + "sold for " + "$" + price
    print(output)
    return output

def format_price(price):
    # Convert the price to an integer if it's a string
    if isinstance(price, str):
        price = int(price)
        
    # Format the price with commas and return the result
    return "{:,}".format(price)
