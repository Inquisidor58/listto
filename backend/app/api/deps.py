from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services import CategoryService, ItemService, StoreService, UserService
from app.infrastructure.database import get_session
from app.infrastructure.repositories import CategoryRepository, ItemRepository, StoreRepository, UserRepository


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(UserRepository(session))


async def get_category_service(session: AsyncSession = Depends(get_session)) -> CategoryService:
    return CategoryService(CategoryRepository(session))


async def get_store_service(session: AsyncSession = Depends(get_session)) -> StoreService:
    return StoreService(StoreRepository(session))


async def get_item_service(session: AsyncSession = Depends(get_session)) -> ItemService:
    return ItemService(ItemRepository(session))
