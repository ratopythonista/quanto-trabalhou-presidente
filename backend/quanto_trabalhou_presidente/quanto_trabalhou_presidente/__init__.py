__version__ = "0.0.1"


import uuid
import time
import traceback
from importlib.metadata import version  # PYTHON >= 3.8

from loguru import logger
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from quanto_trabalhou_presidente.config import DESCRIPTION
from quanto_trabalhou_presidente.routes import appointment
from quanto_trabalhou_presidente.exceptions import QuantoTrabalhouPresidenteException


app = FastAPI(
    title="Quanto Trabalhou o Presidente?",
    description=DESCRIPTION,
    version=__version__,
    docs_url="/swagger",
    redoc_url="/docs"
)

logger.level("INCOME REQUEST", no=1, color="<yellow>")
logger.level("PROCESSED REQUEST", no=2, color="<yellow>")

app.include_router(appointment.router, prefix='/appointment', tags=['appointment'])


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    id = uuid.uuid1()

    logger.log("INCOME REQUEST", f"[{request.method}] ID: {id} - IP: {request.client.host}"
               + f" - ENDPOINT: {request.url.path}")

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.log("PROCESSED REQUEST", f"[{request.method}] ID: {id} - IP: {request.client.host}"
               + f" - ENDPOINT: {request.url.path} - EXCECUTION TIME: {process_time}")
    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.exception_handler(QuantoTrabalhouPresidenteException)
async def camara_exception_handler(request: Request, exception: QuantoTrabalhouPresidenteException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "status": exception.status_code,
            "message": exception.message,
            "stacktrace": traceback.format_exc()
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "message": "Invalid Request Field",
            "stacktrace": traceback.format_exc()
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exception: HTTPException):
    message = {401: "Not Authorize", 404: "Not Found", 405: "Method Not Allowd"}
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "status": exception.status_code,
            "message": message[exception.status_code],
            "stacktrace": traceback.format_exc()
        }
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_credentials=True,
    allow_headers=['*']
)
