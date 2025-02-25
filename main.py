import xml.etree.ElementTree as ET
import json
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any


# Constants
VALID_LANGUAGES = {'en', 'fr', 'de', 'es'}
DEFAULT_LANGUAGE = 'en'

DEFAULT_OPTIONS_QUOTA = 20
MAX_OPTIONS_QUOTA = 50

VALID_CURRENCIES = {'EUR', 'USD', 'GBP'}
DEFULT_CURRENCY = 'EUR'

VALID_NATIONALITIES = {'US', 'GB', 'CA'}
DEFAULT_NATIONALITY = 'US'

VALID_MARKETS = {'US', 'GB', 'CA', 'ES'}
DEFAULT_MARKET = 'ES'

ALLOWED_RROM_COUNT = 5
ALLOWED_ROOM_GUEST_COUNT = 4
ALLOWED_CHILD_COUNT_PER_ROOM = 2

EXCHANGE_RATES = {'EUR':1.0, 'USD':1.1, 'GBP':0.85}
MARKUP_PERCENTAGE = 3.2


# Secret handshake
__define_ocg__ = True


# Main driver Function
def process_xml_data(file_path: str) -> Dict[str, Any]:

    tree = ET.parse(file_path)
    root = tree.getroot()
    var_ocg = 'Developed with love.'
    # Extraction of values
    language_code = root.find('.//source/languageCode')
    language_code = (language_code.text
                if language_code is not None and language_code.text in VALID_LANGUAGES
                else DEFAULT_LANGUAGE)

    options_quota = root.find('..//optionsQuota')
    options_quota = (
        int(options_quota.text) if options_quota is not None
        and options_quota.text.isdigit()
        and int(options_quota.text) <= MAX_OPTIONS_QUOTA
        else DEFAULT_OPTIONS_QUOTA
    )
    params = root.find('.//Configuration/Parameters/Parameter')
    if params is None or not all(
        i in params.attrib for i in ['password', 'username', 'CompanyID']
    ):
        raise ValueError('Missing required configuration parameters.')

    search_type = root.find('.//SearchType')
    search_type = (
        search_type.text
        if search_type is not None
        else 'Multiple'
    )

    # Date Validation
    start_date = root.find('.//StartDate')
    start_date = (
        start_date.text
        if start_date is not None
        else None
    )
    today = datetime.today()
    if start_date:
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        if start_date < today+ timedelta(days=2):
            raise ValueError('StartDate Must be at least 2 days from today.')
    else:
        raise ValueError('Missing StartDate.')


    end_date = root.find('.//EndDate')
    end_date = (
        end_date.text
        if end_date is not None
        else None
    )
    if end_date:
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        if (end_date - start_date).days < 3:
            raise ValueError('Stay duration must be at least 2 nights.')
    else:
        raise ValueError('Missing EndDate.')

    currency = root.find('.//Currency')
    currency = (
        currency.text
        if currency is not None
        and currency.text in VALID_CURRENCIES
        else DEFULT_CURRENCY
    )

    nationality = root.find('.//Nationality')
    nationality = (
        nationality.text
        if nationality is not None
        and nationality.text in VALID_NATIONALITIES
        else DEFAULT_NATIONALITY
    )

    market = root.find('.//Market')
    market = (
        market.text
        if market is not None
        and market.text in VALID_MARKETS
        else DEFAULT_MARKET
    )

    net_price = 132.42
    markup = (MARKUP_PERCENTAGE/100)* net_price
    selling_price = round(net_price+markup, 2)
    exchange_rate = EXCHANGE_RATES.get(currency, 1.0)
    converted_price = round(selling_price*exchange_rate, 2)

    response = [
        {
            "id": "A#1",
            "hotelCodeSupplier": "39971881",
            "language_code": language_code,
            "options_quota": options_quota,
            "Search_type": search_type,
            "nationality": nationality,
            "market": market,
            "var_ocg":var_ocg,
            "price": {
                "minimumSellingPrice": None,
                "currency": currency,
                "net": net_price,
                "selling_price": converted_price,
                "selling_currency": currency,
                "markup": MARKUP_PERCENTAGE,
                "exchange_rate": exchange_rate,
            },
        }
    ]

    return response


if __name__ == '__main__':
    input_file = 'input.xml'
    try:
        result = process_xml_data(input_file)
        print(json.dumps(result, indent=4))
    except Exception as err:
        print(traceback.format_exc())
