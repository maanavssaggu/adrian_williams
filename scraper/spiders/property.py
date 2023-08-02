from typing import List

class Property:
    '''
    Define Property object for casting scrapted data results
    '''
    def __init__(self, address_line_1: str, address_line_2: List[str], price: str, sold_status_date: str, property_url: str, property_id: str):
        self.address_line_1 = address_line_1
        self.address_line_2 = "-".join(address_line_2)

        self.price_string = ""
        
        # Convert price to int
        if (price == "Price Withheld"):
            self.price = -1
            self.approx_price = True
        else:
            self.price = int(price.replace('$', '').replace(',', ''))
            self.approx_price = False
            
        self.set_price(self.price)
        self.sold_status_date = sold_status_date
        self.property_url = property_url
        self.property_id = property_id
        

    '''
    Turn data into a dictionary to pass to fire_base
    '''

    def propertery_to_dict(self):
        data = {'property_id': self.property_id,
                'price': self.price,
                'adress_line1': self.address_line_1,
                'address_line2': self.address_line_2,
                'property_url': self.property_url,
                'sold_date': self.sold_status_date
        }

        return data
    
    def set_price(self, price):
        self.price = price
        if (price == -1):
            self.price_string = ""
        
        else:
            string_price = str(price)
            count = 1
            result_string = ""
            for i in range(len(string_price) - 1, -1, -1):
                result_string = string_price[i] + result_string
                if (count % 3 == 0 and count != len(string_price)):
                    result_string = "," + result_string
                count += 1

            self.price_string = result_string

    
    def __str__(self):
        return f'{{"address_line_1": "{self.address_line_1}", "address_line_2": {self.address_line_2}, "price": {self.price}, "sold_status_date": "{self.sold_status_date}", "property_url": "{self.property_url}", "property_id": "{self.property_id}"}}'
