# this python file uses the following encoding: utf-8
import logging
import traceback
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from sqlalchemy.exc import OperationalError, ProgrammingError, IntegrityError
from pydantic.error_wrappers import ValidationError as SerializationError
from app import exceptions, models
from app.db import SessionLocal, engine

import app.api.namespace1 as namespace1


models.Base.metadata.create_all(bind=engine)

# app
log = logging.getLogger(__name__)
app = FastAPI(
    title='The API Title',
    version='0.0.1',
    description='some description')

app.include_router(namespace1.router)


# db session middleware
@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# exception handlers
@app.exception_handler(Exception)
def default_error_handler(request, exc):
    log.warning(traceback.format_exc())
    log.warning(exc)
    msg = "It's not you, it's us! ...sorry"
    return JSONResponse(content={'message': msg}, status_code=500)


@app.exception_handler(exceptions.ValidationError)
def input_validation_error_handler(request, exc):
    msg = 'Input validation failed' if str(exc) == '' else str(exc)
    log.warning(msg)
    return JSONResponse(content={'message': msg}, status_code=400)


@app.exception_handler(exceptions.NoResultFound)
def no_results_found_error_handler(request, exc):
    msg = 'A database result was required but none was found' if str(exc) == '' else str(exc)
    log.warning(msg)
    return JSONResponse(content={'message': msg}, status_code=404)


@app.exception_handler(exceptions.AlreadyExists)
def already_exists_error_handler(request, exc):
    msg = 'Such a record already exists' if str(exc) == '' else str(exc)
    log.warning(msg)
    return JSONResponse(content={'message': msg}, status_code=406)


@app.exception_handler(OperationalError)
def db_operational_error_handler(request, exc):
    log.warning(traceback.format_exc())
    log.warning(exc)
    msg = 'Database operational error: database connected? schema exists? table exists?'
    return JSONResponse(content={'message': msg}, status_code=500)


@app.exception_handler(ProgrammingError)
def db_programming_error_handler(request, exc):
    log.warning(traceback.format_exc())
    log.warning(exc)
    msg = 'The database does not allow this action: Sth wrong with the SQL query? No rights?'
    return JSONResponse(content={'message': msg}, status_code=406)


@app.exception_handler(IntegrityError)
def db_integrity_error_handler(request, exc):
    log.warning(traceback.format_exc())
    log.warning(exc)
    msg = 'The database does not allow this content: NULL or UNIQUE constraint violated?'
    return JSONResponse(content={'message': msg}, status_code=406)


@app.exception_handler(SerializationError)
def pydantic_validation_error_handler(request, exc):
    log.warning(traceback.format_exc())
    log.warning(exc)
    msg = 'There was an error during serialization of the response'
    return JSONResponse(content={'message': msg}, status_code=500)
