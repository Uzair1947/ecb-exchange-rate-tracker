import requests
import xml.etree.ElementTree as ET
from decimal import Decimal

# Helper function to fetch and parse XML data from ECB
def fetch_ecb_xml_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve XML data from {url}. Status code: {response.status_code}")
    return response.content

# Function to parse current exchange rates from ECB
def parse_current_exchange_rates(previous_day_rates):
    base_url = "https://www.ecb.europa.eu/stats/eurofxref/"
    daily_sub_url = "eurofxref-daily.xml"
    url = base_url + daily_sub_url

    xml_data = fetch_ecb_xml_data(url)
    tree = ET.ElementTree(ET.fromstring(xml_data))

    namespace = {"ns": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}
    parent_cube = tree.find(".//ns:Cube", namespace)

    data = []
    for cube in parent_cube.findall("ns:Cube", namespace):
        data_date = cube.attrib.get("time")
        for currency in cube.findall("ns:Cube", namespace):
            currency_name = currency.attrib.get("currency")
            rate = Decimal(currency.attrib.get("rate"))
    
            if currency_name in previous_day_rates:
                change = Decimal(((rate - previous_day_rates[currency_name]) / previous_day_rates[currency_name]) * 100)
                data.append({
                    "DATE": data_date,
                    "CURRENCY": currency_name,
                    "RATE": rate,
                    "CHANGE": change
                }) 
            else:
                data.append({
                    "DATE": data_date,
                    "CURRENCY": currency_name,
                    "RATE": rate
                }) 
    
    return data

# Function to parse quarterly exchange rates from ECB
def parse_exchange_rates_quarterly():
    base_url = "https://www.ecb.europa.eu/stats/eurofxref/"
    quarterly_sub_url = "eurofxref-hist-90d.xml"
    url = base_url + quarterly_sub_url

    xml_data = fetch_ecb_xml_data(url)
    tree = ET.ElementTree(ET.fromstring(xml_data))

    namespace = {"ns": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}
    parent_cube = tree.find(".//ns:Cube", namespace)

    data = []
    previous_day_rates = {}
    for cube in parent_cube.findall("ns:Cube", namespace)[::-1]:
        data_date = cube.attrib.get("time")
        for currency in cube.findall("ns:Cube", namespace):
            currency_name = currency.attrib.get("currency")
            rate = Decimal(currency.attrib.get("rate"))
            if currency_name in previous_day_rates:
                previous_rate = previous_day_rates[currency_name]
                change = Decimal(((rate - previous_rate) / previous_rate) * 100)
                previous_day_rates[currency_name] = rate
                data.append({
                    "DATE": data_date,
                    "CURRENCY": currency_name,
                    "RATE": rate,
                    "CHANGE": change
                })  
            else:
                previous_day_rates[currency_name] = rate
                    
    return data
