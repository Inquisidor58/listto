from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services import CategoryService, ItemService, StoreService, UserService
from app.infrastructure.database import get_session
from app.infrastructure.repositories import CategoryRepository, ItemRepository, StoreRepository, UserRepository


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(UserRepository(session))


def get_category_service(session: Session = Depends(get_session)) -> CategoryService:
    return CategoryService(CategoryRepository(session))


def get_store_service(session: Session = Depends(get_session)) -> StoreService:
    return StoreService(StoreRepository(session))


def get_item_service(session: Session = Depends(get_session)) -> ItemService:
    return ItemService(ItemRepository(session))
