"""
tests.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

import datetime
import pytest
import os


def test_simple():
    try:
        a = 1 / 0
    except Exception as e:
        assert True


if __name__ == "__main__":
    os.system("pytest tests.py")
