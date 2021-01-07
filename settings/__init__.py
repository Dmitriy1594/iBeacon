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

settingsDir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'settings')


def get_settings():
    with open(os.path.join(settingsDir, "settings.json"), 'r') as json_file:
        settings = json.load(json_file)

    return settings
