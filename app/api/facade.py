from fastapi import FastAPI
from .routers.auth import router as auth_router
from .routers.items import router as items_router
from .routers.users import router as users_router


def add_routers(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(items_router)
