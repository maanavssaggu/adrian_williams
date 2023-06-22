import re
from datetime import datetime, timedelta

"""
Converts sold status to easier to compute data -> this function should be relocated
"""

def sold_status_to_date(sold_status):
    remaining_string = re.split(r'(\d+)', sold_status, maxsplit=2)[1:-1]
    month = remaining_string[1].strip()
    month_mapping = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }

    try:
        if month in month_mapping:
            month_number = month_mapping[month]
    except Exception as e:
        print(e)
        
    remaining_string = remaining_string[0] + str(month_number) + remaining_string[2]
    return remaining_string

"""
Calculates date of the last monday from current week 
 i.e. if today is the 12/6 Mon output: 5/6 Mon 
      or today is the 15/6 Thurs output: 5/6 Mon
"""

def last_monday_date(date_string):
    
    """
        Returns a date of last monday from todays date
    
        input: date with format "ddmmyyyy"
        output: date of last monday "ddmmyyyy"
    """
    
    date = int(date_string[0:2])
    month = int(date_string[2:4])
    year = int(date_string[4:])
    
    input_date = datetime(year, month, date)

    # Calculate the difference in days between the input date and the previous Monday
    if input_date.weekday() == 0: # if the input date is Monday
        return input_date.date().strftime("%d/%m/%Y")
    else:
        days_to_monday = input_date.weekday() 
        delta = timedelta(days=days_to_monday)

        # Subtract the timedelta to get the date of the previous Monday
        previous_monday = input_date - delta
        return previous_monday.date().strftime("%d%m%Y")


def is_date_before(curr, compareTo):
    """
        Returns if current date is before another date 
    
        input: two dates with format "ddmmyyyy"
        output: true/false
    """
    curr = datetime.strptime(curr, "%d%m%Y")
    compareTo = datetime.strptime(compareTo, "%d%m%Y")

    return curr>compareTo
    