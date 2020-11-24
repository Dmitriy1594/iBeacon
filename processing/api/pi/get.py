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
import datetime
import json

from fabric import Connection

from fastapi import APIRouter, BackgroundTasks, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from processing.api.money_converter import get_currencies

from core.db import crud, schemas
from core.db.database import SessionLocal
from core.auth.token import api_token_hash, generate_random_token

from config.settings import PATH_TO_API, SERVER_URL, PI_SSH_CONNECTION_PROPERTIES

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# data.json
@router.post(
    f"{PATH_TO_API}" + "/get_data_json/",
    response_model=schemas.PIdata,
    tags=["PI", "manage"]
)
def get_data_json(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)
    product = pi_.name
    price = pi_.price
    default_buttons_currency = pi_.currencies
    currencies = get_currencies(price, default_buttons_currency)

    # get first no active PI
    # pi = crud.get_first_no_active_pi(db)
    # pi.currencies
    data_json = {
        "product": product,
        "currencies": currencies,
    }

    return JSONResponse(content=jsonable_encoder(data_json))


@router.post(
    f"{PATH_TO_API}" + "/deploy_data_json/",
    response_model=schemas.PIdata,
    tags=["PI", "manage"]
)
def deploy_data_json(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)
    product = pi_.name
    price = pi_.price
    default_buttons_currency = pi_.currencies
    currencies = get_currencies(price, default_buttons_currency)

    data_json = {
        "product": product,
        "currencies": currencies,
    }

    # ssh connect to PI
    # deploy data.json
    c = Connection(**PI_SSH_CONNECTION_PROPERTIES)
    command = f"cd ~/Documents/display/data &&\
                >data.json && \
                echo '{json.dumps(data_json)}' >data.json"
    out_str = c.run(command, hide=True).stdout.strip()
    if out_str == "":
        com = "cd ~/Documents/display/data && cat data.json"
        out_str = c.run(com, hide=True).stdout.strip()

    info = {
        "data": data_json,
        "remote_out_str": out_str
    }

    return JSONResponse(content=jsonable_encoder(info))


# settings.json
@router.post(
    f"{PATH_TO_API}" + "/get_settings_pi/",
    response_model=schemas.PIsettings,
    tags=["PI", "manage"]
)
def get_settings_pi(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)
    default_buttons_currency = pi_.currencies
    default_currency = default_buttons_currency[0]
    version = str(datetime.datetime.now().timestamp())

    settings_json = {
        "server_url": SERVER_URL,
        "default_currency": default_currency,
        "default_buttons_currency": default_buttons_currency,
        "version": version
    }

    return JSONResponse(content=jsonable_encoder(settings_json))


@router.post(
    f"{PATH_TO_API}" + "/deploy_settings_json/",
    response_model=schemas.PIsettings,
    tags=["PI", "manage"]
)
def deploy_settings_json(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)
    default_buttons_currency = pi_.currencies
    default_currency = default_buttons_currency[0]
    version = str(datetime.datetime.now().timestamp())

    settings_json = {
        "server_url": SERVER_URL,
        "default_currency": default_currency,
        "default_buttons_currency": default_buttons_currency,
        "version": version
    }

    # ssh connect to PI
    # deploy settings.json
    c = Connection(**PI_SSH_CONNECTION_PROPERTIES)
    command = f"cd ~/Documents/display/settings &&\
                 >settings.json && \
                 echo '{json.dumps(settings_json)}' >settings.json"
    out_str = c.run(command, hide=True).stdout.strip()
    if out_str == "":
        com = "cd ~/Documents/display/settings && cat settings.json"
        out_str = c.run(com, hide=True).stdout.strip()

    info = {
        "data": settings_json,
        "remote_out_str": out_str
    }

    return JSONResponse(content=jsonable_encoder(info))


def save_locate_data():
    pass
