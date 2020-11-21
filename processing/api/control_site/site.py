"""
get.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

from typing import List

from fastapi import APIRouter, BackgroundTasks, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.db import crud, schemas
from core.db.database import SessionLocal
from core.auth.token import api_token_hash, generate_random_token

from config.settings import PATH_TO_API

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create
@router.post(f"{PATH_TO_API}" + "/create_pi/", response_model=schemas.PICreate)
def create_pi(pi: schemas.PICreate, db: Session = Depends(get_db)):
    db_pi = crud.get_pi_by_name(db, pi.name)
    if db_pi is None:
        raise HTTPException(status_code=404, detail="PI not found")
    return crud.create_pi(db, pi=db_pi)


# Get
@router.get(f"{PATH_TO_API}" + "/get_pis/", response_model=List[schemas.PI])
def get_pis(skip: int = 0, limit: int = 100, active: bool = True, db: Session = Depends(get_db)):
    pis = crud.get_pis(db, skip=skip, limit=limit, active=active)
    return pis


@router.get(f"{PATH_TO_API}" + "/get_pis/{user_id}", response_model=schemas.PI)
def get_pi(pi_id: int, active: bool, db: Session = Depends(get_db)):
    pi = crud.get_pi(db, id=pi_id, active=active)
    if pi is None:
        raise HTTPException(status_code=404, detail="PI not found")
    return pi


@router.post(f"{PATH_TO_API}" + "/get_pi_data/", response_model=schemas.PI)
def get_pi_data(find_scheme: schemas.PIFindBase, db: Session = Depends(get_db)):
    name = find_scheme.name
    uuid = find_scheme.uuid
    active = find_scheme.active
    pi = crud.get_pi_by_name(db, name=name, active=active)
    if pi is None:
        raise HTTPException(status_code=404, detail="PI not found")
    return pi


# Update
@router.post(f"{PATH_TO_API}" + "/update_pi/", response_model=schemas.PI)
def update_pi(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    price = pi.price
    currencies = pi.currencies
    count_visitors = pi.count_visitors
    uuid = pi.uuid
    locate_data = pi.locate_data
    # old
    old_name = pi.old_name
    old_uuid = pi.old_uuid

    # update all
    if name is not None and \
            price is not None and \
            currencies is not None and \
            count_visitors is not None and \
            uuid is not None and \
            locate_data is not None and \
            old_name is not None and \
            old_uuid is not None:

        pi_ = crud.update_all(
            db,
            name,
            price,
            currencies,
            count_visitors,
            uuid,
            locate_data,
            old_name,
            old_uuid
        )

        if pi_ is None:
            raise HTTPException(status_code=404, detail="PI didn't update. New PI didn't find.")
        return pi_
    else:
        raise HTTPException(status_code=404, detail="PI didn't update. Field problem.")


@router.post(f"{PATH_TO_API}" + "/update_price_by_name/", response_model=schemas.PI)
def update_price_by_name(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    price = pi.price
    currencies = pi.currencies
    return crud.update_pi_price_by_name(db, name, price, currencies)


@router.post(f"{PATH_TO_API}" + "/update_name_and_uuid/", response_model=schemas.PI)
def update_name_and_uuid(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    uuid = pi.uuid
    # old
    old_name = pi.old_name
    old_uuid = pi.old_uuid
    return crud.update_pi_name_and_uuid(db, name, uuid, old_name, old_uuid)


@router.post(f"{PATH_TO_API}" + "/update_locate_data_by_name/", response_model=schemas.PI)
def update_locate_data_by_name(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    locate_data = pi.locate_data
    return crud.update_pi_locate_data(db, name, locate_data)


@router.post(f"{PATH_TO_API}" + "/update_activate_by_name/", response_model=schemas.PI)
def update_activate_by_name(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    name = pi.name
    active = pi.active
    return crud.update_pi_active(db, name, active)
