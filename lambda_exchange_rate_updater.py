from exchange_rate_parser import parse_current_exchange_rates,parse_exchange_rates_quarterly
from exchange_rates_manager import ExchangeRatesManager
from utils import get_today_date,get_previous_date,get_previous_friday,is_weekend,date_to_string_format_yyyy_mm_dd

# Lambda function entry point
def lambda_handler(event, context):
    try:
        # Fetch current exchange rate data
        dynamodb_manager = ExchangeRatesManager()
        if dynamodb_manager.table_exists():
            previous_date = get_previous_date(get_today_date())
            if is_weekend(previous_date):
                previous_date = get_previous_friday(previous_date)
            previous_date_data = dynamodb_manager.fetch_exchange_rates_from_db(date=date_to_string_format_yyyy_mm_dd(previous_date),columns="CURRENCY, RATE")
            previous_date_data = {item["CURRENCY"]: str(item["RATE"]) for item in previous_date_data}
            fetch_data = parse_current_exchange_rates(previous_date_data)
            if previous_date == fetch_data[0]['DATE']:
                print('Data already uptodate')
            dynamodb_manager.insert_data(fetch_data=fetch_data)
        else:
            dynamodb_manager.create_dynamodb_table()
            fetch_data = parse_exchange_rates_quarterly()
            print(fetch_data)
            dynamodb_manager.insert_data(fetch_data=fetch_data)
        return {
            "statusCode": 200,
            "body": "Data inserted successfully!"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": "An error occurred while processing the data"
        }

print(lambda_handler(None,None))