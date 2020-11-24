"""
__init__.py

created by dromakin as 23.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201123'

import datetime
from forex_python.converter import CurrencyRates, Decimal


def get_currencies(price_for_default_currency: float, currencies: list) -> dict:
    result_d = dict()

    c = CurrencyRates()

    default_currency = currencies[0]
    result_d[default_currency] = price_for_default_currency

    for cur in currencies[1:]:
        result_d[cur] = float("{:.2f}".format(c.convert(default_currency, cur, price_for_default_currency)))

    return result_d


def main():
    print(datetime.datetime.now())
    print(get_currencies(1000, [
        "RUB",
        "USD",
        "EUR",
        "GBP"
    ]))


if __name__ == "__main__":
    main()
