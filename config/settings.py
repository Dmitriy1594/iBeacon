"""
settings.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

import os
import json

from config.environment import DEBUG

HOST = "0.0.0.0"

# PORT = 5004
PORT = 5002

PATH_TO_API = "/v1"

SQL_DBS = ["PI",]
