import logging
from exchange_rates_manager import ExchangeRatesManager
from utils import get_previous_friday,get_today_date,is_weekend,date_to_string_format_yyyy_mm_dd
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Handler function for AWS Lambda
def lambda_handler(event, context):
    try:
        # Extract the path from the event to determine the endpoint
        path = event['path']
        dynamo_manager = ExchangeRatesManager()
        current_date = get_today_date()
        if is_weekend(current_date):
                current_date = get_previous_friday(current_date)
        current_date = date_to_string_format_yyyy_mm_dd(current_date)
        if path == "/exchange-rates/current":
            current_exchange_rates = dynamo_manager.fetch_exchange_rates_from_db(columns="CURRENCY, RATE", date=current_date)
            if current_exchange_rates is not None:
                if current_exchange_rates:
                    return {
                        "statusCode": 200,
                        "date" : current_date,
                        "body": {item["CURRENCY"]: str(item["RATE"]) for item in current_exchange_rates}
                    }
                else:
                    return {
                        "statusCode": 404,
                        "body": "Exchange rate data not found for the current date"
                    }
            else:
                return {
                    "statusCode": 500,
                    "body": "An error occurred while fetching exchange rate data"
                }
        elif path == "/exchange-rates/change":
            current_exchange_rates = dynamo_manager.fetch_exchange_rates_from_db(columns="CURRENCY, CHANGE", date=current_date)
            if current_exchange_rates is not None:
                if current_exchange_rates:
                    return {
                        "statusCode": 200,
                        'date' : current_date,
                        "body": {item["CURRENCY"]: str(item["CHANGE"]) for item in current_exchange_rates}
                    }
                else:
                    return {
                        "statusCode": 404,
                        "body": "Exchange rate data not found for the current date"
                    }
            else:
                return {
                    "statusCode": 500,
                    "body": "An error occurred while fetching exchange rate data"
                }
        else:
            return {
                "statusCode": 404,
                "body": "Invalid endpoint"
            }

    except Exception as e:
        logging.error("Error occurred: %s", str(e))
        return {
            "statusCode": 500,
            "body": "An error occurred while processing the data"
        }
