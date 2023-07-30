from datetime import date,timedelta,datetime
def date_subtractor(give_date: date, days_to_subtract: int) -> date:
    return give_date - timedelta(days=days_to_subtract)

def get_today_date() -> date:
    return date.today()

def get_previous_friday(current_date: date) -> date:
    day_of_week = current_date.weekday()
    days_to_subtract = (day_of_week - 4) % 7
    previous_friday = date_subtractor(current_date, days_to_subtract)
    return previous_friday

def is_weekend(current_date):
    return current_date.weekday() in [5, 6]


def get_previous_date(current_date):
    return current_date - timedelta(days=1)

def date_to_string_format_yyyy_mm_dd(date_obj):
    return date_obj.strftime('%Y-%m-%d')

def compare_dates(previous_date,fetch_date):
    # Convert date strings to datetime objects
    current_date = get_today_date()
    previous_date = previous_date
    fetch_date = datetime.strptime(fetch_date, '%Y-%m-%d')
 
    # Check for conditions
    if current_date == fetch_date and current_date > previous_date:
        return True
    else:
        return False
