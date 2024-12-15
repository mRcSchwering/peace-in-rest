import logging
from fastapi import APIRouter
from app.dependencies import SessionDep
from app.schemas.items import (
    ItemsResponse,
    ItemResponse,
    CreateItemPayload,
    UpdateItemPayload,
)
from app.services import item_service

log = logging.getLogger(__name__)

router = APIRouter(prefix="/items")


@router.get("", response_model=ItemsResponse, response_model_exclude_none=True)
async def get_items(session: SessionDep, user_pubid: str):
    log.info("Getting all items for user %s", user_pubid)
    items = await item_service.get_all_items(sess=session, user_pubid=user_pubid)
    return ItemsResponse.from_items(items=items)


@router.get("/{pubid}", response_model=ItemResponse, response_model_exclude_none=True)
async def get_item_by_id(session: SessionDep, pubid: str):
    log.info("Getting item %s", pubid)
    item = await item_service.get_item(sess=session, pubid=pubid)
    return ItemResponse.from_orm(item)


@router.post(
    "", response_model=ItemResponse, response_model_exclude_none=True, status_code=201
)
async def create_item(session: SessionDep, payload: CreateItemPayload):
    log.info("Creating new item for user %s", payload.user_pubid)
    item = await item_service.create_item(
        sess=session, user_pubid=payload.user_pubid, name=payload.name
    )
    return ItemResponse.from_orm(item)


@router.put("/{pubid}", response_model=ItemResponse, response_model_exclude_none=True)
async def update_item(session: SessionDep, pubid: str, payload: UpdateItemPayload):
    log.info("Updating item %s", pubid)
    item = await item_service.update_item(
        sess=session, pubid=pubid, added=payload.added
    )
    return ItemResponse.from_orm(item)


@router.delete("/{pubid}", response_model_exclude_none=True)
async def delete_item(session: SessionDep, pubid: str):
    log.info("Deleting item %s", pubid)
    await item_service.delete_item(sess=session, pubid=pubid)
