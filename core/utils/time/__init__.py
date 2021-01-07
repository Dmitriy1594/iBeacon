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

import datetime
from calendar import monthrange

import fastapi


async def check_time(t1: int, t2: int):
    if t1 > t2:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": [
                        "body",
                        t1
                    ],
                    "msg": f"{t1} > {t2}, but must be t2 > t1",
                    "type": "type_error.body"
                }
            ]
        )
    elif is_epoch(t1) is False:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": [
                        "body",
                        t1
                    ],
                    "msg": f"t1 is not ",
                    "type": "type_error.body"
                }
            ]
        )
    elif is_epoch(t2) is False:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": [
                        "body",
                        t2
                    ],
                    "msg": f"{t1} > {t2}, but must be t2 > t1",
                    "type": "type_error.body"
                }
            ]
        )


def is_epoch(param) -> bool:
    # Copy from
    # https://gitlab.cybertonica.com/Pipeline/sw-engine/-/blob/master/core/__init__.py
    if not isinstance(param, int):
        return False
    if param < 946684800000:  # 2000.01.01
        return False
    if param > 4102444800000:  # 2100.01.01
        return False
    return True


def to_short_epoch(param) -> int:
    t = to_epoch(param)
    return t // 1000


def epoch2datetime(epoch: int):
    # Copy from
    # https://gitlab.cybertonica.com/Pipeline/sw-engine/-/blob/master/core/__init__.py
    assert is_epoch(epoch)
    return datetime.datetime.utcfromtimestamp(epoch / 1000)


def to_epoch(param) -> int:
    # Copy from
    # https://gitlab.cybertonica.com/Pipeline/sw-engine/-/blob/master/core/__init__.py
    if is_epoch(param):
        return param
    if isinstance(param, datetime.datetime):
        return datetime2epoch(param)
    raise NotImplementedError(f"type({type(param)}) is not supported")


def to_datetime(param) -> datetime.datetime:
    # Copy from
    # https://gitlab.cybertonica.com/Pipeline/sw-engine/-/blob/master/core/__init__.py
    if isinstance(param, datetime.datetime):
        return param
    if is_epoch(param):
        return epoch2datetime(param)
    if is_epoch(param * 1000):
        return epoch2datetime(param * 1000)
    raise NotImplementedError(f"type({type(param)}) is not supported")


def datetime2epoch(datetime_: datetime.datetime):
    # Copy from
    # https://gitlab.cybertonica.com/Pipeline/sw-engine/-/blob/master/core/__init__.py
    first_dt = datetime.datetime.utcfromtimestamp(0)
    return int((datetime_ - first_dt).total_seconds() * 1000)


if __name__ == "__main__":
    print(int(datetime2epoch(datetime.datetime(2020, 10, 11))))
    print(int(datetime2epoch(datetime.datetime(2020, 12, 2))))
    # print(monthrange(2020, 11))
    t1 = 1605218589000
    t2 = 1607240189000

    datet1 = datetime.datetime.utcfromtimestamp(to_short_epoch(t1)).strftime('%Y%m')
    datet1_n = int(datet1)
    datet2 = datetime.datetime.utcfromtimestamp(to_short_epoch(t2)).strftime('%Y%m')
    datet2_n = int(datet2)

    year = int(datetime.datetime.utcfromtimestamp(to_short_epoch(t1)).strftime('%Y'))
    month = int(datetime.datetime.utcfromtimestamp(to_short_epoch(t1)).strftime('%m'))
    max_day_month_1 = monthrange(year, month)[1]

    t2_ = datetime.datetime.strptime(datet1 + f"{max_day_month_1}", '%Y%m%d')
    t1_ = datetime.datetime.strptime(datet2 + "01", '%Y%m%d')

    print(datetime2epoch(t2_))
    print(datetime2epoch(t1_))

    print()

