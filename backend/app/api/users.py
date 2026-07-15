import os
import uuid

from fastapi import APIRouter, Depends

from app.application.services import UserService
from app.api.deps import get_user_service
from app.domain.schemas import UserCreate, UserResponse, UserUpdateAlias

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def list_users(service: UserService = Depends(get_user_service)):
    return service.get_all()


@router.get("/me", response_model=UserResponse)
def get_or_create_me(service: UserService = Depends(get_user_service)):
    name = os.getenv("USERNAME") or os.getenv("USER") or "unknown"
    user = service.get_by_name(name)
    if not user:
        user = service.create(name)
    return user


@router.post("", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create(data.name, data.alias)


@router.patch("/{user_id}/alias", response_model=UserResponse)
def update_alias(user_id: uuid.UUID, data: UserUpdateAlias, service: UserService = Depends(get_user_service)):
    user = service.update_alias(user_id, data.alias)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: uuid.UUID, service: UserService = Depends(get_user_service)):
    service.delete(user_id)
