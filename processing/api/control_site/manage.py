"""
manage.py

created by dromakin as 18.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]

__status__ = 'Development'
__version__ = '20201118'

# TODO для управления программой на raspberry pi через запросы по ssh или простой сервер на raspberry pi.
# TODO оптимально - делать запуск через терминальную команду ssh.

import datetime


def main():
    print(datetime.datetime.now())


if __name__ == "__main__":
    main()
