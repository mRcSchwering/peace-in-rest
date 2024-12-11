from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.api.v1.version import router as v1_router

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    log.info("startup procedures")
    yield
    log.info("shutdown procedures")


app = FastAPI(lifespan=lifespan)
app.include_router(v1_router)
