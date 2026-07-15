import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.application.services import ItemService, extract_image_url
from app.api.deps import get_item_service
from app.domain.models import ListType
from app.domain.schemas import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemResponse])
async def list_items(
    list_type: Optional[ListType] = None,
    category_id: Optional[uuid.UUID] = None,
    store_id: Optional[uuid.UUID] = None,
    checked: Optional[bool] = None,
    service: ItemService = Depends(get_item_service),
):
    return await service.get_all(list_type, category_id, store_id, checked)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: uuid.UUID, service: ItemService = Depends(get_item_service)):
    item = await service.get_by_id(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item


@router.post("", response_model=ItemResponse, status_code=201)
async def create_item(data: ItemCreate, service: ItemService = Depends(get_item_service)):
    item = await service.create(data.model_dump())
    if item.url:
        image_url = await extract_image_url(item.url)
        if image_url:
            item = await service.update_image(item.id, image_url)
    return item


@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: uuid.UUID, data: ItemUpdate, service: ItemService = Depends(get_item_service)):
    existing = await service.get_by_id(item_id)
    if not existing:
        raise HTTPException(404, "Item not found")
    item = await service.update(item_id, data.model_dump(exclude_unset=True))
    if data.url and data.url != (existing.url or ""):
        image_url = await extract_image_url(data.url)
        if image_url:
            item = await service.update_image(item_id, image_url)
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: uuid.UUID, service: ItemService = Depends(get_item_service)):
    await service.delete(item_id)


@router.post("/{item_id}/toggle", response_model=ItemResponse)
async def toggle_item(item_id: uuid.UUID, service: ItemService = Depends(get_item_service)):
    item = await service.toggle_checked(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item
