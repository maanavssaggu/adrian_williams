from .property import Property

class PropertyResults:
    '''
    Class to store the results of the property search
    '''
    def __init__(self):
        self._price_included = []
        self._price_excluded = []

    def add_property(self, property: Property):
        if (property.price == -1):
            self._price_excluded.append(property)
        else:
            self._price_included.append(property)

    def get_price_included(self):
        return self._price_included
    
    def get_price_excluded(self):
        return self._price_excluded