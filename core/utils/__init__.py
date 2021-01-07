"""
__init__.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'


from core.utils.time import *


def is_cookie(param) -> bool:
    # Copy from
    # https://gitlab.cybertonica.com/Pipeline/sw-engine/-/blob/master/core/__init__.py
    if not isinstance(param, str):
        return False
    if len(param) != len('d9e7a870f8d446eba6663b180a4dc329'):
        return False
    if any(a not in '01234567890abcdef' for a in param):
        return False
    return True


def is_platform(platform):
    if platform is None:
        return False
    if not isinstance(platform, str):
        return False
    if platform in ['web', 'mobile', 'desktop']:
        return True
    return False



