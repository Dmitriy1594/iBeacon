"""
schemas.py

created by dromakin as 16.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__copyright__ = "Cybertonica LLC, London, 2020"
__status__ = 'Development'
__version__ = '20201116'

from typing import List, Optional, Dict

from pydantic import BaseModel


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


# class UserPassword(UserCreate):
#     admin_token: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class PIBase(BaseModel):
    name: str
    price: float
    currencies: List[str]
    count_visitors: int = 0
    uuid: str
    ip: str
    locate_data: str = "json_data"

    class Config:
        schema_extra = {
            "example": {
                "name": "Product Name",
                "price": 1000,
                "currencies": [
                    "RUB",
                    "USD",
                    "EUR",
                    "GBP"
                ],
                "count_visitors": 0,
                "uuid": "string",
                "ip": "192.168.31.97",
                "locate_data": "json_data"
            }
        }


class PIFindBase(BaseModel):
    name: Optional[str] = "name"
    uuid: Optional[str] = "uuid"
    active: Optional[bool] = False
    ip: Optional[str]


class PIUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    currencies: Optional[List[str]] = None
    count_visitors: Optional[int] = None
    uuid: Optional[str] = None
    locate_data: Optional[str] = None
    active: Optional[bool] = False
    # old
    old_name: Optional[str] = None
    old_uuid: Optional[str] = None


class PICreate(PIBase):
    pass


class PI(PIBase):
    id: int
    active: bool = False

    class Config:
        orm_mode = True


class PIdata(BaseModel):
    product: str
    currencies: dict


class PIsettings(BaseModel):
    server_ip: str
    default_currency: str = "RUB"
    default_buttons_currency: List[str] = ["RUB", "USD", "EUR", "GBP"]
    version: str
