"""

config -- all configuration settings MUST be written in this file

RULES:
    1) It some value CAN be changed, please move it  into config.settings

created by dromakin as 10.10.2020
Project iBeacon

----
EXAMPLES of __init__.py 

"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

import os

# path of config.
# if you wand test some Mongo, Redis, Kafka and etc.,
# you can change CONFIG_PATH
CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))

ROOT_PATH = os.path.dirname(CONFIG_PATH)

# DEFAULT_TEMPLATE_PATH = os.path.join(ROOT_PATH, 'doc', 'templates')

# illegal chars for database names and for collection names in MongoDB
# ILLEGAL_MONGO_CHARS = '-. /\\^$#=+?<>[]{}:;"\'~`@%&*(),'

# Max length of apiuser name
# MAX_LEN_CUSTOMER = 12

# will hit you in the face with piss rags!
# STANDARD_HEALTH_PORT = 8094


# --------------------------------------------------------------------------------------------------------------------

# for root, dirs, files in os.walk(CONFIG_PATH):
#     for file in files:
#        if '.private.' in file:
#            os.remove(os.path.join(root, file))
# if os.path.exists(os.path.join(CONFIG_PATH, 'environment.private.txt')):
#     print("delete environment.private.txt")
#     os.remove(os.path.join(CONFIG_PATH, 'environment.private.txt'))
