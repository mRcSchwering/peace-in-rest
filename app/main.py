from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.api.v1.version import router as v1_router
from app.database import engine
from app.database.models.common import Base

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    log.info("startup procedure")
    Base.metadata.create_all(engine)
    yield
    log.info("shutdown procedure")


app = FastAPI(lifespan=lifespan)
app.include_router(v1_router)
