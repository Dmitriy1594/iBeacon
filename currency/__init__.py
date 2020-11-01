"""
__init__.py

created by dromakin as 01.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201101'

import os
import json

currencyDir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'currency')
CURRENCY_JSON = "currencies.json"


class CurrencyCodes:

    def __init__(self):
        pass

    def _get_data(self, currency_code):
        with open(os.path.join(currencyDir, CURRENCY_JSON)) as f:
            currency_data = json.loads(f.read())
        currency_dict = next((item for item in currency_data if item["cc"] == currency_code), None)
        return currency_dict

    def _get_data_from_symbol(self, symbol):
        with open(os.path.join(currencyDir, CURRENCY_JSON)) as f:
            currency_data = json.loads(f.read())
        currency_dict = next((item for item in currency_data if item["symbol"] == symbol), None)
        return currency_dict

    def get_symbol(self, currency_code):
        currency_dict = self._get_data(currency_code)
        if currency_dict:
            return currency_dict.get('symbol')
        return None

    def get_currency_name(self, currency_code):
        currency_dict = self._get_data(currency_code)
        if currency_dict:
            return currency_dict.get('name')
        return None

    def get_currency_code_from_symbol(self, symbol):
        currency_dict = self._get_data_from_symbol(symbol)
        if currency_dict:
            return currency_dict.get('cc')
        return None


_CURRENCY_CODES = CurrencyCodes()

get_symbol = _CURRENCY_CODES.get_symbol
get_currency_name = _CURRENCY_CODES.get_currency_name
get_currency_code_from_symbol = _CURRENCY_CODES.get_currency_code_from_symbol


def check_price(price=None) -> str:
    price_ = None
    if isinstance(price, str):
        price_ = price

    if isinstance(price, int):
        price_ = str(price)

    if isinstance(price, float):
        price_ = "{:.2f}".format(price)

    if price is None:
        price_ = "0.0"

    return price_


def check_currency(currency=None) -> str:
    currency_ = None

    if currency is None:
        currency_ = "RUB"

    if currency.isupper() is True:
        currency_ = currency

    return currency_
