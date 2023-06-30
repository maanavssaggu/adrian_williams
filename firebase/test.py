from FireBaseDB import FireBaseDB
from Query import Query
import datetime

fb_db = FireBaseDB()

data ={ 'property_id': '2014',
        'price': '$1000',
        'suburb': 'amaroo',
        'date_sold': '01042003'
}

data2 ={ 'property_id': '1114',
        'price': '$5120',
        'suburb': 'belco',
        'date_sold': '05042003'
}

data3 ={ 'property_id': '4214',
        'price': '$1000',
        'suburb': 'belco',
        'date_sold': '06042003'
}

data4 ={ 'property_id': '2114',
        'price': '$5120',
        'suburb': 'belco',
        'date_sold': '10042003'
}


fb_db.upload(data=data)
fb_db.upload(data=data2)
fb_db.upload(data=data3)
fb_db.upload(data=data4)

query = Query(date_min='04042003', date_max='07042003', suburb='belco')

fb_db.check_exists(query=query)
#expecting output: 1114, 2013


# fb_db.check_exists(query=query)

