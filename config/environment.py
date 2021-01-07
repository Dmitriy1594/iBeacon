"""
environment.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

import os


DEBUG = os.getenv("DEBUG", False)
if DEBUG == 'True':
    DEBUG = True

DB_URL = os.getenv('DB_URL')

# TEST_BRANCH = os.getenv("TEST_BRANCH", 'False')
#
# URL_SHARED = os.getenv("URL_SHARED", 'https://sw-analysis-api-shared.cybertonica.com')
# PORT_SHARED = os.getenv("PORT_SHARED", 443)
#
# URL_TEST = os.getenv("URL_TEST")
# PORT_TEST = os.getenv("PORT_TEST", 443)

