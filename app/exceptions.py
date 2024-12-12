import logging
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

log = logging.getLogger(__name__)


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
