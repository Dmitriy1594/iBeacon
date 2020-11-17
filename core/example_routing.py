"""
core.routing -- main module for route functions

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

import os
import fastapi
from fastapi import Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import PlainTextResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from core.auth import check_token_header

# import core.json as json
# from core.utils import is_platform, to_epoch, to_short_epoch, is_epoch

# from processing.api.description import _FUNCTIONS_WITHOUT_apiuser
from processing.api.models import ValidationErrorModelResponse
from processing.api.imports import (
    inits,
    help,
)

from config.environment import DEBUG
from config.settings import PATH_TO_API


tags_metadata = [
    {
        "name": "help",
        "description": "Help methods.",
    },
    {
        "name": "get",
        "description": "All methods to **get** or **count** data about _alerts_ and _statistics_.",
    },
    {
        "name": "alerts",
        "description": "Methods to **get** or **count** data about _alerts_.",
        # "externalDocs": {
        #     "description": "Items external docs",
        #     "url": "https://fastapi.tiangolo.com/",
        # },
    },
    {
        "name": "statistic",
        "description": "Methods to **get** or **count** data about _statistics_.",
    },
    {
        "name": "ip",
        "description": "Methods to **get** ip data from n-memory cache or data providers.",
    },
    {
        "name": "old",
        "description": "Deprecated methods but supported.",
    }
]

app = fastapi.FastAPI(
    debug=DEBUG,
    title='sw-report-api',
    description="**Tokens** in headers are provided on request.",
    openapi_url=f'{PATH_TO_API}',
    openapi_tags=tags_metadata,
    docs_url=None,
    redoc_url=None
)


# Validation error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


app.include_router(inits.router)

app.include_router(
    help.router,
    dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
        422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    },
)

# return back
app.include_router(
    ip.router,
    dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
        422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    },
)

# app.include_router(
#     alerts.router,
#     dependencies=[fastapi.Depends(check_token_header)],
#     responses={404: {"description": "Not found"}},
# )

app.include_router(
    get_alerts.router,
    dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
        422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    },
)

# app.include_router(
#     alert_statistic.router,
#     dependencies=[fastapi.Depends(check_token_header)],
#     responses={404: {"description": "Not found"}},
# )

app.include_router(
    get_statistics.router,
    dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
        422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    },
)

# app.include_router(
#     statistic.router,
#     dependencies=[fastapi.Depends(check_token_header)],
#     responses={404: {"description": "Not found"}},
# )
#
# app.include_router(
#     ueba.router,
#     dependencies=[fastapi.Depends(check_token_header)],
#     responses={404: {"description": "Not found"}},
# )


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
