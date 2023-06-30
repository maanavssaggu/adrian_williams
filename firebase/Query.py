from datetime import date


class Query:
    
    # constructor -> for single suburb
    def __init__(self, date_min, date_max, property_id=None, suburb=None, suburbs=None) -> None:
        """
        inputs: dates to be formatted as strings: 'DDMMYYYY'    
                suburb to be formatted as a string: 'suburb name - state - postcode' 
                                                eg:  earlwood-nsw-2206'
                suburbs to be inputted as a list of suburbs
        """
        self.date_min = date_min
        self.date_max = date_max
        self.suburb = suburb
        self.suburbs = suburbs
        self.property_id = property_id

    # def get_date_min(self):
    #     return self.get_date_min
    
    # def get_date_max(self):
    #     return self.get_date_max

    
