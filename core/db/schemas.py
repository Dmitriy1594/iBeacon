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

from typing import List, Optional

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
    currencies: str
    count_visitors: int
    uuid: str
    locate_data: str


class PIFindBase(BaseModel):
    name: Optional[str] = "name"
    uuid: Optional[str] = "uuid"
    active: Optional[bool] = True


class PICreate(PIBase):
    pass


class PI(PIBase):
    id: int
    active: bool = False

    class Config:
        orm_mode = True
