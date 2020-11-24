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

from processing.api.ip import get_ip

HOST = "0.0.0.0"

# PORT = 5004
# PORT = 5002
PORT = 8000

PATH_TO_API = "/v1"

SQL_DBS = ["PI",]

SERVER_URL = get_ip()

PI_SSH_CONNECTION_PROPERTIES = {
    "host": "192.168.31.97",
    "user": "pi",
    "connect_kwargs": {
        "password": "Romakin1594"
    }
}


