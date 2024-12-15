import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.common import async_engine
from app.exceptions import add_exception_handlers
from app.api import add_routers

log = logging.getLogger(__name__)


@asynccontextmanager
async def _lifespan(_: FastAPI):
    log.info("startup procedures")
    yield
    log.info("shutdown procedures")
    await async_engine.dispose()


def _create_app():
    app_ = FastAPI(lifespan=_lifespan)
    add_routers(app=app_)
    add_exception_handlers(app=app_)
    return app_


app = _create_app()
