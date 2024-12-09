from fastapi import APIRouter
from .routers.items import router as items_router

router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(items_router)
