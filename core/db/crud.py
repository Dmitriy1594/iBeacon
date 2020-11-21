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
    return db.query(models.Raspberry).filter(
        models.Raspberry.id == id,
        models.Raspberry.active == active
    ).first()


def get_pis(db: Session, skip: int = 0, limit: int = 100, active: bool = True):
    return db.query(models.Raspberry).query(
        models.Raspberry.active == active
    ).offset(skip).limit(limit).all()


# Update (default - active)
def update_all(
        db: Session,
        name: str,
        price: float,
        currencies: str,
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


def update_pi_name_and_uuid(
        db: Session,
        name: str,
        uuid: str,
        old_name: str,
        old_uuid: str
):
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
    return get_pi_by_name(db, name)


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
    return get_pi_by_name(db, name)


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
    uuid = pi.uuid
    locate_data = pi.locate_data
    active = False
    db_pi = models.Raspberry(
        name=name,
        price=price,
        currencies=currencies,
        count_visitors=count_visitors,
        uuid=uuid,
        locate_data=locate_data,
        active=active,
    )
    db.add(db_pi)
    db.commit()
    db.refresh(db_pi)
    return db_pi
