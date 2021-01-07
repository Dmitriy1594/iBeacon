"""
description.py

For fields description

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

_FIELD_DESCRIPTION = {
    "t1": {
        "ru": "t1 время в UNIX epoch начала запроса.",
        "en": "t1 time in UNIX epoch start request.",
    },
    "t2": {
        "ru": "t2 время в UNIX epoch окончание запроса.",
        "en": "t2 time in UNIX epoch end request.",
    },
    "platform": {
        "ru": "web, mobile, desktop - платформа, которая использовалась.",
        "en": "web, mobile, desktop - platform that have already used by."
    },
    "apiuser": {
        "ru": "один из кастомеров, который используется в системе, например stfs.",
        "en": "one of the apiusers that is used in the system, for example stfs."
    },
    "cookie": {
        "ru": "данные куки из алерта.",
        "en": "cookie data from alert."
    },
    "name": {
        "ru": "название алерта, например DEV_TOOLS или BOT.",
        "en": "name of alert, for example DEV_TOOLS or BOT."
    },
    "date": {
        "ru": "дата в формате UTC, например 2020-06-02.",
        "en": "date in format UTC, for example 2020-06-02."
    },
    "group_days": {
        "ru": "группировние дней.",
        "en": "grouping days."
    },
    "severity": {
        "ru": "10, 50, 90 - риск",
        "en": "10, 50, 90 - risks",
    },
    "period": {
        "ru": "minute, hour, day, week, month.",
        "en": "minute, hour, day, week, month."
    },
    "count_alerts": {
        "ru": "количество алертов, минимум 2.",
        "en": "lots of alerts, min is 2."
    },
    "team": {
        "ru": "название команды.",
        "en": "command name."
    },
    "ipdata_keys": {
        "ru": 'поля, которые нужно вернуть с ipdata.co, default: ["city", "country_name", "threat"]',
        "en": 'keys that return from ipdata.co, default: ["city", "country_name", "threat"]'
    },
    "referrer": {
        "ru": 'referrer',
        "en": 'referrer',
    },
    "count_ip": {
        "ru": 'количество ip, указанное в этом параметре',
        "en": 'the number of ip specified in this parameter',
    },
    "ip_list": {
        "ru": 'список ip',
        "en": 'list of ip',
    },
    "places": {
        "ru": 'Mongo urls',
        "en": 'Mongo urls',
    },
    "query": {
        "ru": 'Mongo request',
        "en": 'Mongo request',
    },
    "mongo": {
        "ru": 'Mongo async_client',
        "en": 'Mongo async_client'
    }
}

ALL_PARAMS_SW_ALERTS = ['id', 'tid', 'date', 'time', 'time_beacon', 'name', 'cookie', 'hashid',
                        'webGL', 'canvas', 'deviceId', 'messages', 'reasons', 'labels', 'score',
                        'severity', 'ip', 'platform', 'referrer', 'apiuser', 'customer']

ALL_PARAMS_SW_STATISTIC = ['id', 'target', 'value', 'tid', 'date', 'time', 'cookie', 'hashid',
                           'webGL', 'canvas', 'deviceId', 'ip', 'platform', 'apiuser', 'customer']

if __name__ == '__main__':
    print()
