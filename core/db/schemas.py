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
    address: str
    uuid: str
    ip: str
    locate_data: str
    scanning_seconds: float = 5.0
    meters_detection: float = 1.0

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
                "address": "address",
                "uuid": "string",
                "ip": "192.168.31.97",
                "locate_data": "json_data",
                "scanning_seconds": 5.0,
                "meters_detection": 1.0
            }
        }


class PIFindBase(BaseModel):
    name: Optional[str] = "name"
    address: Optional[str] = "address"
    uuid: Optional[str] = "uuid"
    active: Optional[bool] = False
    ip: Optional[str]


class PIUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    currencies: Optional[List[str]] = None
    count_visitors: Optional[int] = None
    locate_data: Optional[str] = None
    active: Optional[bool] = False
    # old
    old_name: Optional[str] = None
    old_uuid: Optional[str] = None


class PIUpdateByID(BaseModel):
    id: int
    name: Optional[str] = None
    price: Optional[float] = None


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


# Beacon
class BeaconBase(BaseModel):
    date: float
    product_name: str
    device_name: str
    uuid: str = "No data"
    address: str
    addressType: str
    txPower: int = -69
    rssi: int
    meters: float

    class Config:
        schema_extra = {
            "example": {
                "date": 1609967007.7562,
                "device_name": "fenix 5x",
                "uuid": [
                    "6a4e3e10-667b-11e3-949a-0800200c9a66"
                ],
                "address": "D0:72:10:EC:BE:64",
                "addressType": "random",
                "txPower": 12,
                "rssi": -66,
                "meters": 0.7405684692262438,
                "product_name": "Product Name"
            }
        }


class Beacon(BeaconBase):
    id: int

    class Config:
        orm_mode = True


class BeaconCreate(BeaconBase):
    pass


class BeaconMultipleFind(BaseModel):
    product_name: Optional[str]
    device_name: Optional[str]
    txPower: Optional[int]
    rssi: Optional[int]
    meters: Optional[float]


#  check beacon in PI db
class BeaconFind(BaseModel):
    date: Optional[float]
    product_name: Optional[str]
    device_name: Optional[str]
    address: Optional[str]
    addressType: Optional[str]
    txPower: Optional[int]
    rssi: Optional[int]
    meters: Optional[float]

