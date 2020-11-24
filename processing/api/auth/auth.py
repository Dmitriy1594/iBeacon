"""
auth.py

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


# Sign
# Sign on
@router.post(
    f"{PATH_TO_API}" + "/sign_on/",
    response_model=schemas.User,
    tags=["site",]
)
def sign_on(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# Sign in
@router.post(
    f"{PATH_TO_API}" + "/sign_in/",
    response_model=schemas.User,
    tags=["site",]
)
def sign_in(auth_model: schemas.UserCreate, db: Session = Depends(get_db)):
    login = auth_model.login
    password = auth_model.password
    hash_password = api_token_hash(password)

    db_user = crud.get_user_by_login(db, login=login)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Please sign up!")
    return Response(status_code=200)


# Forget password
@router.post(
    f"{PATH_TO_API}" + "/change_password/",
    response_model=schemas.User,
    tags=["site",]
)
def change_password(auth_model: schemas.UserCreate, db: Session = Depends(get_db)):
    login = auth_model.login
    password = auth_model.password
    return crud.update_password(db, login=login, new_password=password)


# Users
@router.get(
    f"{PATH_TO_API}" + "/users/",
    response_model=List[schemas.User],
    tags=["site",]
)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get(
    f"{PATH_TO_API}" + "/users/{user_id}",
    response_model=schemas.User,
    tags=["site",]
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
