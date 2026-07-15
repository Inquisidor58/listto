import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.application.services import CategoryService
from app.api.deps import get_category_service
from app.domain.schemas import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
async def list_categories(service: CategoryService = Depends(get_category_service)):
    return await service.get_all()


@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(data: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    return await service.create(data.name)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: uuid.UUID, data: CategoryUpdate, service: CategoryService = Depends(get_category_service)):
    category = await service.update(category_id, data.name)
    if not category:
        raise HTTPException(404, "Category not found")
    return category


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: uuid.UUID, service: CategoryService = Depends(get_category_service)):
    await service.delete(category_id)
