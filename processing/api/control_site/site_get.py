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


def get_pi_data(find_scheme: schemas.PIFindBase, db: Session = Depends(get_db)):
    name = find_scheme.name
    # uuid = find_scheme.uuid
    active = find_scheme.active
    pi = crud.get_pi_by_name(db, name=name, active=active)
    if pi is None:
        raise HTTPException(status_code=404, detail="PI not found")
    return pi

# Update
# TODO нужно доделать update для name, price, currencies, update_all и вынести в другой файл
