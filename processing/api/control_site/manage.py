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

import fabric
from fabric import Connection

# from config.settings import PI_SSH_CONNECTION_PROPERTIES
PI_SSH_CONNECTION_PROPERTIES = {
    # "host": "192.168.31.97",
    "host": "192.168.8.104",
    "user": "pi",
    "connect_kwargs": {
        "password": "Romakin1594"
    }
}


# send settings.json
def send_settings():
    # echo 'Hello, world.' >foo.txt
    c = Connection(**PI_SSH_CONNECTION_PROPERTIES)
    command = "cd ~/Documents/display/settings && pwd"
    return c.run(command, hide=True).stdout.strip()


# Start program
# update data.json
# update settings.json

# Stop program

# Update program


if __name__ == '__main__':
    send_settings()
