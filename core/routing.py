"""
routing.py

created by dromakin as 17.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__copyright__ = "Cybertonica LLC, London, 2020"
__status__ = 'Development'
__version__ = '20201117'

from typing import List

import fastapi
from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import PlainTextResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from sqlalchemy.orm import Session

from core.db import crud, models, schemas
from core.db.database import SessionLocal, engine

from config.environment import DEBUG
from config.settings import PATH_TO_API

from processing.api.imports import (
    help,
    auth,
    site_get
)

models.Base.metadata.create_all(bind=engine)


# TODO: теги

app = fastapi.FastAPI(
    debug=DEBUG,
    title='control-api',
    # description="**Tokens** in headers are provided on request.",
    openapi_url=f'{PATH_TO_API}',
    # openapi_tags=tags_metadata,
    docs_url=None,
    redoc_url=None
)

app.include_router(
    help.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    auth.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    site_get.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

# TODO: когда доделаю сайт эти ссылки нужно будет встроить в сайт и сделать возиожность подключения к ним через авторизацию

# OPENAPI
@app.get(path=f'{PATH_TO_API}', tags=["secret"], include_in_schema=False)
async def get_open_api_endpoint():
    return JSONResponse(get_openapi(title="FastAPI", version="2.0.0", routes=app.routes))


# ADMIN PANEL
@app.get(path='/admin', tags=["secret"], include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url=f'{PATH_TO_API}', title="docs")


# DOCS
@app.get(path='/docs', tags=["help"], include_in_schema=False)
async def get_documentation():
    return get_redoc_html(openapi_url=f'{PATH_TO_API}', title="docs")


@app.get(path='/', tags=["help"], include_in_schema=False)
async def root():
    return RedirectResponse("/docs")
