import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.application.services import CategoryService
from app.api.deps import get_category_service
from app.domain.schemas import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def list_categories(service: CategoryService = Depends(get_category_service)):
    return service.get_all()


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(data: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    return service.create(data.name)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: uuid.UUID, data: CategoryUpdate, service: CategoryService = Depends(get_category_service)):
    category = service.update(category_id, data.name)
    if not category:
        raise HTTPException(404, "Category not found")
    return category


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: uuid.UUID, service: CategoryService = Depends(get_category_service)):
    service.delete(category_id)
