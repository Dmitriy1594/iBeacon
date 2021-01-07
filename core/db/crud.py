"""
crud.py

created by dromakin as 17.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__copyright__ = "Cybertonica LLC, London, 2020"
__status__ = 'Development'
__version__ = '20201117'

from typing import List, Optional, Dict

from fastapi import HTTPException

from sqlalchemy.orm import Session

from . import models, schemas

from core.auth.token import api_token_hash, generate_random_token


# Auth
# sign on
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = api_token_hash(token=user.password)
    db_user = models.User(login=user.login, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# sign in
def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


# help.py
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# Change password
def update_password(db: Session, login: str, new_password: str):
    hashed_password = api_token_hash(token=new_password)
    db.query(models.User).filter(models.User.login == login).update(
        {"hashed_password": hashed_password})
    db.commit()
    return get_user_by_login(db, login)


# Control site
# Get
def get_pi_by_name(db: Session, name: str, active: bool = None):
    if active is not None:
        return db.query(models.Raspberry).filter(
            models.Raspberry.name == name,
            models.Raspberry.active == active
        ).first()
    else:
        return db.query(models.Raspberry).filter(
            models.Raspberry.name == name,
        ).first()


def get_pi(db: Session, id: int, active: bool):
    if active is None:
        return db.query(models.Raspberry).filter(
            models.Raspberry.id == id,
        ).first()
    else:
        return db.query(models.Raspberry).filter(
            models.Raspberry.id == id,
            models.Raspberry.active == active
        ).first()


def get_pi_by_uuid(db: Session, uuid: str):
    return db.query(models.Raspberry).filter(
        models.Raspberry.uuid == uuid,
    ).first()


def get_first_no_active_pi(db: Session):
    return db.query(models.Raspberry).filter(
        models.Raspberry.active == False
    ).first()


def get_pis(db: Session, skip: int = 0, limit: int = 100, active: bool = True):
    return db.query(models.Raspberry).filter(
        models.Raspberry.active == active
    ).offset(skip).limit(limit).all()


# Update (default - active)
def update_all(
        db: Session,
        name: str,
        price: float,
        currencies: List[str],
        count_visitors: int,
        uuid: str,
        locate_data: str,
        old_name: str,
        old_uuid: str,
):
    q = None
    if old_uuid is not None:
        q = db.query(models.Raspberry).filter(
            models.Raspberry.name == old_name,
            models.Raspberry.uuid == old_uuid,
        )
    else:
        q = db.query(models.Raspberry).filter(
            models.Raspberry.name == old_name,
        )

    q.update(
        {
            "name": name,
            "price": price,
            "currencies": currencies,
            "count_visitors": count_visitors,
            "uuid": uuid,
            "locate_data": locate_data,
        }
    )
    db.commit()
    return get_pi_by_name(db, name)


def update_pi_by_id(
        db: Session,
        name: str = None,
        price: float = None,
        pi_id: int = None,
):
    if name is not None and price is not None:
        db.query(models.Raspberry).filter(
            models.Raspberry.id == pi_id,
        ).update(
            {
                "name": name,
                "price": price,
            }
        )
    elif name is not None and price is None:
        db.query(models.Raspberry).filter(
            models.Raspberry.id == pi_id,
        ).update(
            {
                "name": name,
            }
        )
    elif name is None and price is not None:
        db.query(models.Raspberry).filter(
            models.Raspberry.id == pi_id,
        ).update(
            {
                "price": price,
            }
        )
    db.commit()
    return get_pi_by_name(db, name)


def update_pi_price_by_name(
        db: Session,
        name: str,
        price: float,
        currencies: str = None
):
    if currencies is not None:
        db.query(models.Raspberry).filter(
            models.Raspberry.name == name,
        ).update(
            {
                "price": price,
                "currencies": currencies,
            }
        )
    else:
        db.query(models.Raspberry).filter(
            models.Raspberry.name == name,
        ).update({"price": price})
    db.commit()
    return get_pi_by_name(db, name)


def update_pi_name_and_or_uuid(
        db: Session,
        name: str,
        uuid: str,
        old_name: str,
        old_uuid: str
):
    if old_name is not None or old_uuid is not None:
        if name is not None and uuid is not None:
            db.query(models.Raspberry).filter(
                models.Raspberry.name == old_name,
                models.Raspberry.uuid == old_uuid,
            ).update(
                {
                    "uuid": uuid,
                    "name": name
                }
            )
            db.commit()
            return get_pi_by_name(db, name)
        elif name is not None:
            db.query(models.Raspberry).filter(
                models.Raspberry.name == old_name,
            ).update(
                {
                    "name": name
                }
            )
            db.commit()
            return get_pi_by_name(db, name)
        elif uuid is not None:
            db.query(models.Raspberry).filter(
                models.Raspberry.uuid == old_uuid,
            ).update(
                {
                    "uuid": uuid
                }
            )
            db.commit()
            return get_pi_by_name(db, name)
        else:
            raise HTTPException(status_code=404,
                                detail="PI didn't update. Fields problem: uuid or name.")
    else:
        raise HTTPException(status_code=404,
                            detail="PI didn't update. Fields problem: old_name or old_uuid.")


def update_pi_locate_data(
        db: Session,
        name: str,
        locate_data: str
):
    db.query(models.Raspberry).filter(
        models.Raspberry.name == name,
    ).update(
        {
            "locate_data": locate_data,
        }
    )
    db.commit()
    db_pi = get_pi_by_name(db, name)
    return db_pi


def update_pi_active(
        db: Session,
        name: str,
        active: bool
):
    db.query(models.Raspberry).filter(
        models.Raspberry.name == name,
    ).update(
        {
            "active": active,
        }
    )
    db.commit()
    db_pi = get_pi_by_name(db, name)
    return db_pi


# IF find - ignore
def get_pi_by_address(
    db: Session,
    address: str,
):
    return db.query(models.Raspberry).filter(
        models.Raspberry.address == address,
    ).first()


# increase visitors count
def update_count_visitors(db: Session, name: str, count_visitors: int):
    db.query(models.Raspberry).filter(
        models.Raspberry.name == name,
    ).update(
        {
            "count_visitors": count_visitors,
        }
    )
    db.commit()
    db_pi = get_pi_by_name(db, name)
    return db_pi


# Create
# PI
def create_pi(
        db: Session,
        pi: schemas.PICreate,
):
    name = pi.name
    price = pi.price
    currencies = pi.currencies
    count_visitors = pi.count_visitors
    address = pi.address
    uuid = pi.uuid
    locate_data = pi.locate_data
    active = False
    ip = pi.ip
    scanning_seconds = pi.scanning_seconds
    meters_detection = pi.meters_detection

    db_pi = models.Raspberry(
        name=name,
        price=price,
        currencies=currencies,
        count_visitors=count_visitors,
        address=address,
        uuid=uuid,
        locate_data=locate_data,
        active=active,
        ip=ip,
        scanning_seconds=scanning_seconds,
        meters_detection=meters_detection,
    )
    db.add(db_pi)
    db.commit()
    db.refresh(db_pi)
    return db_pi


# Beacons and PI
def get_count_visitors_by_name(
    db: Session,
    name: str,
):
    lots = db.query(models.Beacon).filter(
        models.Beacon.product_name == name,
    ).count()

    db.query(models.Raspberry).filter(
        models.Raspberry.name == name,
    ).update(
        {
            "count_visitors": int(lots),
        }
    )
    db.commit()
    db_pi = get_pi_by_name(db, name)
    return db_pi


# BEACONS
# Beacon create
def create_beacon(
        db: Session,
        pi_beacon: schemas.BeaconCreate,
):
    date = pi_beacon.date
    product_name = pi_beacon.product_name
    device_name = pi_beacon.device_name
    uuid = pi_beacon.uuid
    address = pi_beacon.address
    addressType = pi_beacon.addressType
    txPower = pi_beacon.txPower
    rssi = pi_beacon.rssi
    meters = pi_beacon.meters
    db_pi_beacon = models.Beacon(
        date=date,
        product_name=product_name,
        device_name=device_name,
        uuid=uuid,
        address=address,
        addressType=addressType,
        txPower=txPower,
        rssi=rssi,
        meters=meters,
    )
    db.add(db_pi_beacon)
    db.commit()
    db.refresh(db_pi_beacon)
    return db_pi_beacon


# find beacons
def get_beacon_by_device_name(
    db: Session,
    device_name: str,
):
    return db.query(models.Beacon).filter(
        models.Beacon.device_name == device_name,
    ).first()


def get_beacons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Beacon).offset(skip).limit(limit).all()


def get_beacons_by_product_name(db: Session, product_name: str, skip: int = 0, limit: int = 100):
    return db.query(models.Beacon).filter(
        models.Beacon.product_name == product_name,
    ).offset(skip).limit(limit).all()


def get_beacons_by_date_period(
    db: Session,
    t1: float,
    t2: float,
):
    return db.query(models.Beacon).filter(
        models.Beacon.date <= t2,
        models.Beacon.date >= t1,
    ).first()


def get_data_plot_by_product(db: Session, product_name: str,):
    return db.query(models.Beacon).filter(
        models.Beacon.product_name == product_name,
    ).all()


# DELETE
def delete_beacons_by_date_period(
    db: Session,
    t1: float,
    t2: float,
):
    # get deleted beacons
    beacons = db.query(models.Beacon).filter(
        models.Beacon.date <= t2,
        models.Beacon.date >= t1,
    ).all()
    # delete
    db.query(models.Beacon).filter(
        models.Beacon.date <= t2,
        models.Beacon.date >= t1,
    ).delete()
    db.commit()
    return beacons


def delete_by_product_name(db: Session, product_name: str,):
    # get deleted beacons
    beacons = db.query(models.Beacon).filter(
        models.Beacon.product_name == product_name,
    ).all()
    # delete
    db.query(models.Beacon).filter(
        models.Beacon.product_name == product_name,
    ).delete()
    db.commit()
    return beacons
