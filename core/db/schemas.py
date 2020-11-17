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


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


# class AdminBase(BaseModel):
#     login: str
#
#
# class AdminCreate(AdminBase):
#     password: str
#
#
# class Admin(AdminBase):
#     id: int
#     is_active: bool
#
#     class Config:
#         orm_mode = True
#
#
# class PIBase(BaseModel):
#     name: str
#     price: float
#     currencies: str
#     count_visitors: int
#     uuid: str
#     locate_data: str
#
#
# class PICreate(PIBase):
#     pass
#
#
# class PI(PIBase):
#     id: int
#
#     class Config:
#         orm_mode = True
