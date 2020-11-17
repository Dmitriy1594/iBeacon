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
def get_pi_by_name(db: Session, name: str, active: bool):
    return db.query(models.Raspberry).filter(
        models.Raspberry.name == name,
        models.Raspberry.active == active
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
def update_pi_name(db: Session, name: str, active: bool = True):
    db.query(models.Raspberry).filter(
        models.Raspberry.name == name,
        models.Raspberry.active == active
    ).update({"name": name})
    db.commit()
    return get_pi_by_name(db, name, active)


def update_pi_price_by_name(db: Session, name: str, price: float, active: bool = True):
    db.query(models.Raspberry).filter(
        models.Raspberry.name == name,
        models.Raspberry.active == active
    ).update({"price": price})
    db.commit()
    return get_pi_by_name(db, name, active)
