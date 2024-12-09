from fastapi import APIRouter
from .routers.items import router as items_router
from .routers.users import router as users_router

router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(items_router)
router.include_router(users_router)
