"""
inits.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

from core.auth.token import generate_random_token


if __name__ == '__main__':
    print(generate_random_token(14))

