from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services import CategoryService, ItemService, StoreService, UserService
from app.config import settings
from app.infrastructure.database import get_session
from app.infrastructure.repositories import (
    CategoryRepository,
    ItemRepository,
    StoreRepository,
    UserRepository,
)

IS_SUPABASE = bool(settings.supabase_url and settings.supabase_key)


def _build_user(session=None):
    return UserService(UserRepository(session))


def _build_category(session=None):
    return CategoryService(CategoryRepository(session))


def _build_store(session=None):
    return StoreService(StoreRepository(session))


def _build_item(session=None):
    return ItemService(ItemRepository(session))


if IS_SUPABASE:

    def get_user_service():
        return _build_user()

    def get_category_service():
        return _build_category()

    def get_store_service():
        return _build_store()

    def get_item_service():
        return _build_item()

else:

    def get_user_service(session: Session = Depends(get_session)):
        return _build_user(session)

    def get_category_service(session: Session = Depends(get_session)):
        return _build_category(session)

    def get_store_service(session: Session = Depends(get_session)):
        return _build_store(session)

    def get_item_service(session: Session = Depends(get_session)):
        return _build_item(session)
