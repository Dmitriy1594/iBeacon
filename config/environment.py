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

DOCKER_RUN = os.getenv('DOCKER_RUN', False)
if DOCKER_RUN == "True":
    DOCKER_RUN = True

SERVER_URL_ = os.getenv("SERVER_URL", None)
