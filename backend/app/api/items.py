import traceback
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.application.services import ItemService
from app.api.deps import get_item_service
from app.domain.models import ListType
from app.domain.schemas import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemResponse])
def list_items(
    list_type: Optional[ListType] = None,
    category_id: Optional[uuid.UUID] = None,
    store_id: Optional[uuid.UUID] = None,
    checked: Optional[bool] = None,
    service: ItemService = Depends(get_item_service),
):
    return service.get_all(list_type, category_id, store_id, checked)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: uuid.UUID, service: ItemService = Depends(get_item_service)):
    item = service.get_by_id(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item


@router.post("", response_model=ItemResponse, status_code=201)
def create_item(data: ItemCreate, service: ItemService = Depends(get_item_service)):
    return service.create(data.model_dump())


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(item_id: uuid.UUID, data: ItemUpdate, service: ItemService = Depends(get_item_service)):
    item = service.update(item_id, data.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(404, "Item not found")
    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: uuid.UUID, service: ItemService = Depends(get_item_service)):
    service.delete(item_id)


@router.post("/{item_id}/toggle", response_model=ItemResponse)
def toggle_item(item_id: uuid.UUID, service: ItemService = Depends(get_item_service)):
    item = service.toggle_checked(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item
