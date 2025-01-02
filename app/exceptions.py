import logging
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

log = logging.getLogger(__name__)


class LoginFailedWarning(Exception):
    """E.g. 'Login failed because password was wrong'"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


def add_exception_handlers(app: FastAPI):

    @app.exception_handler(NoResultFound)
    async def _no_result_found(request: Request, exc: NoResultFound):
        log.error("%s %s: %s", request.method, request.url, exc)
        return PlainTextResponse(
            status_code=404,
            content=b"A result was required but none was found",
        )

    @app.exception_handler(MultipleResultsFound)
    async def _multiple_results_found(request: Request, exc: MultipleResultsFound):
        log.error("%s %s: %s", request.method, request.url, exc)
        return PlainTextResponse(
            status_code=500,
            content=b"A single result was required but more than one were found",
        )

    @app.exception_handler(LoginFailedWarning)
    async def _authentication_failed(request: Request, exc: LoginFailedWarning):
        log.warning("%s %s: %s", request.method, request.url, exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
