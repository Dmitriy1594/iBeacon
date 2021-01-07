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
import random
import colorsys

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

from config.settings import PATH_TO_API, SERVER_URL, PI_SSH_CONNECTION_PROPERTIES, PORT

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

    connection_settings = PI_SSH_CONNECTION_PROPERTIES
    connection_settings["host"] = pi_.ip

    # ssh connect to PI
    c = Connection(**connection_settings)

    # deploy data.json
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
    scanning_seconds = pi_.scanning_seconds
    meters_detection = pi_.meters_detection
    version = str(datetime.datetime.now().timestamp())

    settings_json = {
        "server_url": SERVER_URL + ":" + PORT,
        "default_currency": default_currency,
        "default_buttons_currency": default_buttons_currency,
        "scanning_seconds": scanning_seconds,
        "meters_detection": meters_detection,
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
    scanning_seconds = pi_.scanning_seconds
    meters_detection = pi_.meters_detection
    version = str(datetime.datetime.now().timestamp())

    settings_json = {
        "server_url": SERVER_URL + ":" + str(PORT),
        "default_currency": default_currency,
        "default_buttons_currency": default_buttons_currency,
        "scanning_seconds": scanning_seconds,
        "meters_detection": meters_detection,
        "version": version
    }

    connection_settings = PI_SSH_CONNECTION_PROPERTIES
    connection_settings["host"] = pi_.ip

    # ssh connect to PI
    c = Connection(**connection_settings)

    # deploy settings.json
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


# turn on program
@router.post(
    f"{PATH_TO_API}" + "/turn_on/",
    response_model=schemas.PIsettings,
    tags=["PI", "manage"]
)
def turn_on(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)

    connection_settings = PI_SSH_CONNECTION_PROPERTIES
    connection_settings["host"] = pi_.ip

    active = pi_.active
    if active == False:
        # ssh connect to PI
        # c = Connection(**connection_settings)
        command = "sudo systemctl start display.service"
        # # remote run program
        # c.run(command, hide=True)

        with Connection(**connection_settings) as c:
            c.run(command)

        info = {
            "info_output": "Program is running!"
        }

        # update in DB
        crud.update_pi_active(db, pi.name, True)

        # result
        return JSONResponse(content=jsonable_encoder(info))
    else:
        info = {
            "info_output": "This PI is active!",
        }
        return JSONResponse(content=jsonable_encoder(info))


@router.post(
    f"{PATH_TO_API}" + "/update_turn_by_pi/",
    response_model=schemas.PIsettings,
    tags=["PI", ]
)
def update_turn_by_pi(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)
    active = pi_.active
    if active == False:
        info = {
            "info_output": "Program is running!"
        }

        # update in DB
        crud.update_pi_active(db, pi.name, True)

        # result
        return JSONResponse(content=jsonable_encoder(info))
    else:
        info = {
            "info_output": "This PI is active!",
        }
        return JSONResponse(content=jsonable_encoder(info))


# turn off program
@router.post(
    f"{PATH_TO_API}" + "/turn_off/",
    response_model=schemas.PIsettings,
    tags=["PI", "manage"]
)
def turn_off(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)

    connection_settings = PI_SSH_CONNECTION_PROPERTIES
    connection_settings["host"] = pi_.ip

    active = pi_.active
    if active == True:
        # ssh connect to PI
        # c = Connection(**connection_settings)
        # command = "ps aux | grep display.py | awk '{print $2}' | xargs kill -9"
        command = "sudo systemctl stop display.service"
        # out_str = str()
        # remote stop program
        # out_str = c.run(command, hide=True).stdout.strip()

        with Connection(**connection_settings) as c:
            c.run(command)

        info = {
            "info_output": "PI is no active more!"
        }

        # update in DB
        crud.update_pi_active(db, pi.name, False)

        # result
        return JSONResponse(content=jsonable_encoder(info))
    else:
        info = {
            "info_output": "This PI is non-active!",
        }
        return JSONResponse(content=jsonable_encoder(info))


# status
@router.post(
    f"{PATH_TO_API}" + "/status_pi/",
    response_model=schemas.PIsettings,
    tags=["PI", "manage"]
)
def status_pi(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)

    connection_settings = PI_SSH_CONNECTION_PROPERTIES
    connection_settings["host"] = pi_.ip

    # ssh connect to PI
    # c = Connection(**connection_settings)
    command = "sudo systemctl status display.service"
    out_str = str()
    # remote get status program
    # out_str = c.run(command, hide=True).stdout.strip()

    with Connection(**connection_settings) as c:
        out_str = c.run(command, hide=True).stdout.strip()

    info = {
        "info_output": out_str
    }

    # result
    return JSONResponse(content=jsonable_encoder(info))


# Beacon
# add_locate_data = update_locate_data_by_name
@router.post(
    f"{PATH_TO_API}" + "/add_beacon/",
    response_model=schemas.Beacon,
    tags=["PI", "beacon"]
)
def add_beacon(beacon: schemas.BeaconCreate, db: Session = Depends(get_db)):
    address = beacon.address
    db_pi = crud.get_pi_by_address(db, address=address)
    if db_pi is not None:
        return JSONResponse(content=jsonable_encoder({"error": "This is a PI = )"}))

    db_beacon = crud.get_beacon_by_device_name(db, beacon.device_name)
    if db_beacon is not None:
        raise HTTPException(status_code=404, detail="Device exist!")
    db_beacon = crud.create_beacon(db, pi_beacon=beacon)
    return db_beacon


# GET
@router.get(
    f"{PATH_TO_API}" + "/get_beacons/",
    response_model=schemas.Beacon,
    tags=["PI", "beacon"]
)
def get_beacons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    beacons = crud.get_beacons(db, skip=skip, limit=limit)
    return beacons


@router.post(
    f"{PATH_TO_API}" + "/get_beacons_by_product_name/",
    response_model=schemas.Beacon,
    tags=["PI", "beacon"]
)
def get_beacons_by_product_name(beacon: schemas.BeaconMultipleFind, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    beacons = crud.get_beacons_by_product_name(db, product_name=beacon.product_name, skip=skip, limit=limit)
    return beacons


@router.post(
    f"{PATH_TO_API}" + "/get_beacons_by_date_period/",
    response_model=schemas.Beacon,
    tags=["PI", "beacon"]
)
def get_beacons_by_date_period(t1, t2, db: Session = Depends(get_db)):
    if t1 >= t2:
        return JSONResponse(content=jsonable_encoder({"error": "t1 >= t2"}))
    else:
        # t1 < t2
        beacons = crud.get_beacons_by_date_period(db, t1, t2)
        return beacons


@router.post(
    f"{PATH_TO_API}" + "/get_data_plot_by_product/",
    response_model=schemas.BeaconBase,
    tags=["PI", "beacon"]
)
def get_data_plot_by_product(beacon: schemas.BeaconMultipleFind, db: Session = Depends(get_db)):
    beacons = crud.get_beacons_by_product_name(db, product_name=beacon.product_name,)
    data = list()
    backgroundColor = []
    label = "Beacons"
    labels = []

    for beacon in beacons:
        data.append(beacon.meters)
        h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
        r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
        backgroundColor.append(f"RGBA({r},{g},{b},0.5")
        labels.append(beacon.device_name)

    data_ = {
        "datasets":
            [
                {
                    "data": data,
                    "backgroundColor": backgroundColor,
                    "label": label,
                }
            ],
        "labels": labels,
    }

    return JSONResponse(content=jsonable_encoder(data_))


# DELETE Beacons
# delete_beacons_by_date_period
@router.post(
    f"{PATH_TO_API}" + "/delete_beacons_by_date_period/",
    response_model=schemas.Beacon,
    tags=["PI", "beacon"]
)
def delete_beacons_by_date_period(t1, t2, db: Session = Depends(get_db)):
    if t1 >= t2:
        return JSONResponse(content=jsonable_encoder({"error": "t1 >= t2"}))
    else:
        # t1 < t2
        beacons = crud.delete_beacons_by_date_period(db, t1, t2)
        return beacons


# delete_by_product_name
@router.post(
    f"{PATH_TO_API}" + "/delete_by_product_name/",
    response_model=schemas.Beacon,
    tags=["PI", "beacon"]
)
def delete_by_product_name(beacon: schemas.BeaconMultipleFind, db: Session = Depends(get_db)):
    beacons = crud.delete_by_product_name(db, product_name=beacon.product_name)
    return beacons
