"""
gen_master_token -- module for generate tokens


created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

from typing import List
import datetime

import core.json as json
from core.utils import to_epoch
from core.auth.token import generate_random_token, api_token_hash


def make_token_files(
        team,
        comments: List,
        private_path,
        public_path,
        start=datetime.datetime.now(),
        count=12,
        period: datetime.timedelta = datetime.timedelta(days=30),
        period_window=datetime.timedelta(days=2),
):
    private_path = private_path.replace('{date}', datetime.datetime.now().strftime('%Y%m%d'))
    public_path = public_path.replace('{date}', datetime.datetime.now().strftime('%Y%m%d'))
    private_path = private_path.replace('{team}', team)
    public_path = public_path.replace('{team}', team)
    assert private_path != public_path

    info_list = list()

    for comment in comments:
        for i in range(count):
            begin = start + i * period
            end = start + (i + 1) * period + period_window
            token = generate_random_token()
            info = {
                "_token": token,
                "token_hash": api_token_hash(token),
                "team": team,
                "t_insert": to_epoch(begin),
                "_t_insert": begin,
                "t_valid": to_epoch(end),
                "_t_valid": end,
                "t_delete": None,
                "comment": comment,
            }
            info_list.append(info)

    with open(private_path, 'w') as fw:
        json.dump(info_list, fw)

    for info in info_list:
        for key in list(info.keys()):
            if key.startswith('_'):
                del info[key]

    with open(public_path, 'w') as fw:
        json.dump(info_list, fw)


if __name__ != "__main__":
    raise Exception("must be start")


if __name__ == "__main__":
    make_token_files(
        team='cbt',
        comments=[
            "Dmitriy Romakin password",
            "Boris Zverkov password",
            "Dev token",
            "DevOps token",
            "Admin token",
            "Developer token",
            "Tester token",
            "Maintainer token",
            "Site token",

        ],
        private_path='./../../config/tokens/tokens.{team}.{date}.private.json',
        public_path='./../../config/tokens/tokens.{team}.{date}.public.json',
        period=datetime.timedelta(days=120),
    )
