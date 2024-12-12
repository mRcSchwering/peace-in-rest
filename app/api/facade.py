from fastapi import FastAPI
from app.api.v1.version import router as v1_router


def add_routers(app: FastAPI):
    app.include_router(v1_router)
