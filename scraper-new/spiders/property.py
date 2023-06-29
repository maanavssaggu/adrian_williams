
class Property:
    '''
    Define Property object for casting scrapted data results
    '''
    def __init__(self, address_line_1: str, address_line_2: str, price: int, sold_status_date: str, property_url: str, property_id: str):
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        
        # Convert price to int
        if (price == "Price Withheld"):
            self.price = -1
        else:
            self.price = int(price.replace('$', '').replace(',', ''))

        self.price = price
        self.sold_status_date = sold_status_date
        self.property_url = property_url
        self.property_id = property_id