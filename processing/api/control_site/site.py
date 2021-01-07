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

import json

from fastapi import APIRouter, BackgroundTasks, Response, Request

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
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
@router.post(
    f"{PATH_TO_API}" + "/create_pi/",
    response_model=schemas.PI,
    tags=["create", "PI", "site"]
)
def create_pi(pi: schemas.PICreate, db: Session = Depends(get_db)):
    db_pi = crud.get_pi_by_name(db, pi.name)
    if db_pi is not None:
        raise HTTPException(status_code=404, detail="PI exist!")
    new_pi = crud.create_pi(db, pi=pi)
    return new_pi


# Get
@router.post(
    f"{PATH_TO_API}" + "/get_pi_by_name/",
    response_model=schemas.PI,
    tags=["get", "PI", "site"]
)
def get_pis(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    db_pi = crud.get_pi_by_name(db, name=pi.name,)
    return db_pi


@router.get(
    f"{PATH_TO_API}" + "/get_pis/",
    response_model=List[schemas.PI],
    tags=["get", "PI", "site"]
)
def get_pis(skip: int = 0, limit: int = 100, active: bool = True, db: Session = Depends(get_db)):
    pis = crud.get_pis(db, skip=skip, limit=limit, active=active)
    return pis


@router.get(
    f"{PATH_TO_API}" + "/get_pis/{pi_id}",
    response_model=schemas.PI,
    tags=["get", "PI", "site"]
)
def get_pi(pi_id: int, active: bool = None, db: Session = Depends(get_db)):
    pi = None
    if active is None:
        pi = crud.get_pi(db, id=pi_id, active = None)
    else:
        pi = crud.get_pi(db, id=pi_id, active=active)
    if pi is None:
        raise HTTPException(status_code=404, detail="PI not found")
    return pi


@router.post(
    f"{PATH_TO_API}" + "/get_pi_data/",
    response_model=schemas.PI,
    tags=["get", "PI"]
)
def get_pi_data(find_scheme: schemas.PIFindBase, db: Session = Depends(get_db)):
    name = find_scheme.name
    uuid = find_scheme.uuid
    active = find_scheme.active
    pi = crud.get_pi_by_name(db, name=name, active=active)
    if pi is None:
        raise HTTPException(status_code=404, detail="PI not found")
    return pi


# Update
@router.post(
    f"{PATH_TO_API}" + "/update_pi/",
    response_model=schemas.PI,
    tags=["update", "PI", "site"]
)
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


# PIUpdateByID
@router.post(
    f"{PATH_TO_API}" + "/update_by_id/",
    response_model=schemas.PI,
    tags=["update", "PI", "site"]
)
def update_by_id(pi: schemas.PIUpdateByID, db: Session = Depends(get_db)):
    pi_id = pi.id
    name = pi.name
    price = pi.price
    return crud.update_pi_by_id(db, name, price, pi_id)


@router.post(
    f"{PATH_TO_API}" + "/update_price_by_name/",
    response_model=schemas.PI,
    tags=["update", "PI", "site"]
)
def update_price_by_name(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    price = pi.price
    currencies = pi.currencies
    return crud.update_pi_price_by_name(db, name, price, currencies)


@router.post(
    f"{PATH_TO_API}" + "/update_name_and_uuid/",
    response_model=schemas.PI,
    tags=["update", "PI", "site"]
)
def update_name_and_uuid(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    uuid = pi.uuid
    # old
    old_name = pi.old_name
    old_uuid = pi.old_uuid
    return crud.update_pi_name_and_or_uuid(db, name, uuid, old_name, old_uuid)


@router.post(
    f"{PATH_TO_API}" + "/increase_count_visitors/",
    response_model=schemas.PI,
    tags=["update", "PI", "site"]
)
def increase_count_visitors(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    db_pi = crud.get_pi_by_name(db, name=name,)
    if db_pi is not None:
        count_visitors = db_pi.count_visitors + 1
        return crud.update_count_visitors(db, name, count_visitors)
    else:
        return JSONResponse(content=jsonable_encoder({"error": "Can't update count visitors. pi not found."}))


@router.post(
    f"{PATH_TO_API}" + "/set_null_count_visitors/",
    response_model=schemas.PI,
    tags=["update", "PI", "site"]
)
def set_null_count_visitors(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    db_pi = crud.get_pi_by_name(db, name=name,)
    if db_pi is not None:
        count_visitors = 0
        return crud.update_count_visitors(db, name, count_visitors)
    else:
        return JSONResponse(content=jsonable_encoder({"error": "Can't update count visitors. pi not found."}))


@router.post(
    f"{PATH_TO_API}" + "/update_locate_data_by_name/",
    response_model=schemas.PI,
    tags=["update", "PI", "site"]
)
def update_locate_data_by_name(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    locate_data_ = pi.locate_data
    locate_data = json.loads(locate_data_)
    # uuid_ = locate_data["uuid"]
    # uuid = None
    # if len(uuid_) > 0:
    #     uuid = uuid_[0]
    # db_pi = crud.get_pi_by_uuid(db, uuid)
    # if db_pi is not None:
    #     return JSONResponse(content=jsonable_encoder({"error": "This is a PI = )"}))

    db_pi = crud.get_pi_by_address(db, address=locate_data["address"])
    if db_pi is not None:
        return JSONResponse(content=jsonable_encoder({"error": "This is a PI = )"}))

    return crud.update_pi_locate_data(db, name, locate_data_)


@router.post(
    f"{PATH_TO_API}" + "/get_locate_data_by_name/",
    response_model=schemas.PI,
    tags=["update", "PI", "site"]
)
def get_locate_data_by_name(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    db_pi = crud.get_pi_by_name(db, name=name,)
    data = db_pi.locate_data
    if data == "json_data":
        return JSONResponse(content=jsonable_encoder({"error": "locate_data has not been updated!"}))
    else:
        locate_data = json.loads(data)
        return JSONResponse(content=jsonable_encoder(locate_data))


@router.post(
    f"{PATH_TO_API}" + "/update_activate_by_name/",
    response_model=schemas.PI,
    tags=["update", "PI", "site"]
)
def update_activate_by_name(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    name = pi.name
    active = pi.active
    return crud.update_pi_active(db, name, active)


templates = Jinja2Templates(directory="./templates")


@router.get(path='/menu', tags=["site", "pages"], include_in_schema=False, response_class=HTMLResponse)
async def menu(request: Request, id: str = None, login: str = None, db: Session = Depends(get_db)):
    if id is None or login is None:
        return RedirectResponse("/auth")

    pis_no_active = jsonable_encoder(crud.get_pis(db, skip=0, limit=1000, active=False))
    pis_active = jsonable_encoder(crud.get_pis(db, skip=0, limit=1000, active=True))

    return templates.TemplateResponse(
        "starter-template.html", {"request": request, "id": id, "login": login, "pis_no_active": pis_no_active, "pis_active": pis_active})

