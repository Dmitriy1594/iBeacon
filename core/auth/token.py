"""
token.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

import random
import datetime
import mmh3
from hashlib import sha256

import fastapi

from core.utils import to_epoch

random.seed("Salt_dfdf4395790sd__sdfgjopjrpg" + str(datetime.datetime.now()))


# async def check_token_header(api_token: str = fastapi.Header(...)):
#     if api_token is None:
#         raise fastapi.HTTPException(
#             status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=[
#                 {
#                     "loc": [
#                         "header",
#                         api_token
#                     ],
#                     "msg": "Don't have 'Api-Token' in header!",
#                     "type": "type_error.header"
#                 }
#             ]
#         )
#         # raise fastapi.HTTPException(status_code=400, detail="Don't have 'Api-Token' in header!")
#
#     hash_ = await api_token_hash(api_token)
#     info = TOKENS.get_message(hash_)
#
#     if info['t_delete']:
#         raise fastapi.HTTPException(
#             status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=[
#                 {
#                     "loc": [
#                         "header",
#                         api_token
#                     ],
#                     "msg": "Token is deleted!",
#                     "type": "type_error.header"
#                 }
#             ]
#         )
#         # raise fastapi.HTTPException(status_code=400, detail="token is deleted")
#
#     if info['t_valid'] and info['t_valid'] < to_epoch(datetime.datetime.now()):
#         raise fastapi.HTTPException(
#             status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=[
#                 {
#                     "loc": [
#                         "header",
#                         api_token
#                     ],
#                     "msg": "Token is expired!",
#                     "type": "type_error.header"
#                 }
#             ]
#         )
#         # raise fastapi.HTTPException(status_code=400, detail="token is expired")


def is_api_token(token: str) -> bool:
    if not token.startswith('PI'):
        return False
    if not token.endswith('TOKEN'):
        return False
    return True


def generate_random_token(length=12 + 2) -> str:
    assert length > 8 + 2

    numbers = '0123456789'

    n0 = numbers[random.randint(0, len(numbers) - 1)]
    n1 = numbers[random.randint(0, len(numbers) - 1)]

    alphabet = numbers + 'aAbBcCdDEeFfGgHhGgKkLlMmNnPpQqRrSsTtXxYyZz'  # not OoIi

    sequence = ''.join(
        alphabet[random.randint(0, len(alphabet) - 1)]
        for i in range(length - 2)
    )

    token = f'PI{n0}{sequence}{n1}TOKEN'

    assert is_api_token(token)
    return token


def api_token_hash(token: str) -> str:
    if is_api_token(token) is False:
        # raise fastapi.HTTPException(status_code=400, detail="It's not a token!")
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": [
                        "body",
                        token
                    ],
                    "msg": "It's not a token!",
                    "type": "type_error.body"
                }
            ]
        )

    _salt = 'sdfgj2235_sdnojhois'
    _salt2 = '354_498902sdfkjOLKg'

    hash_ = sha256((token + _salt).encode('utf-8')).hexdigest()
    hash_ = sha256((hash_ + _salt2).encode('utf-8')).hexdigest()

    return hash_.upper()


# assert api_token_hash(
#     "SW3425430582355TOKEN") == '1D6967827DD270F85052FDF0A64E465CD1797FC4E51432E6EACF7B2EA845227F'

# if __name__ == "__main__":
#     print(generate_random_token())
