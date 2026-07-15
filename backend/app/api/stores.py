import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.application.services import StoreService
from app.api.deps import get_store_service
from app.domain.models import StoreType
from app.domain.schemas import StoreCreate, StoreResponse, StoreUpdate

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("", response_model=list[StoreResponse])
async def list_stores(
    store_type: Optional[StoreType] = None,
    service: StoreService = Depends(get_store_service),
):
    return await service.get_all(store_type)


@router.post("", response_model=StoreResponse, status_code=201)
async def create_store(data: StoreCreate, service: StoreService = Depends(get_store_service)):
    return await service.create(data.name, data.store_type)


@router.put("/{store_id}", response_model=StoreResponse)
async def update_store(store_id: uuid.UUID, data: StoreUpdate, service: StoreService = Depends(get_store_service)):
    store = await service.update(store_id, data.name, data.store_type)
    if not store:
        raise HTTPException(404, "Store not found")
    return store


@router.delete("/{store_id}", status_code=204)
async def delete_store(store_id: uuid.UUID, service: StoreService = Depends(get_store_service)):
    await service.delete(store_id)
