""" 
Propety class creates property objects.
"""

class Property:
    def __init__(self, name: str, region: str, price_withheld: bool, sale_date: int, price: int = None):
        self.name = name
        self.region = region
        self.price = price
        self.price_withheld = price_withheld
        self.sale_date = sale_date
