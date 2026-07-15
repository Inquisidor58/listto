import uuid
from typing import List, Optional

import httpx
from bs4 import BeautifulSoup

from app.domain.interfaces import ICategoryRepository, IItemRepository, IStoreRepository, IUserRepository
from app.domain.models import Category, Item, ListType, Store, StoreType, User


class UserService:
    def __init__(self, repo: IUserRepository):
        self._repo = repo

    async def get_all(self) -> List[User]:
        return await self._repo.get_all()

    async def get_by_name(self, name: str) -> Optional[User]:
        return await self._repo.get_by_name(name)

    async def create(self, name: str, alias: Optional[str] = None) -> User:
        return await self._repo.create(name, alias)

    async def update_alias(self, user_id: uuid.UUID, alias: str) -> Optional[User]:
        return await self._repo.update_alias(user_id, alias)

    async def delete(self, user_id: uuid.UUID) -> None:
        await self._repo.delete(user_id)


class CategoryService:
    def __init__(self, repo: ICategoryRepository):
        self._repo = repo

    async def get_all(self) -> List[Category]:
        return await self._repo.get_all()

    async def create(self, name: str) -> Category:
        return await self._repo.create(name)

    async def update(self, category_id: uuid.UUID, name: str) -> Optional[Category]:
        return await self._repo.update(category_id, name)

    async def delete(self, category_id: uuid.UUID) -> None:
        await self._repo.delete(category_id)


class StoreService:
    def __init__(self, repo: IStoreRepository):
        self._repo = repo

    async def get_all(self, store_type: Optional[StoreType] = None) -> List[Store]:
        return await self._repo.get_all(store_type)

    async def create(self, name: str, store_type: StoreType = StoreType.MERCADO) -> Store:
        return await self._repo.create(name, store_type)

    async def update(self, store_id: uuid.UUID, name: str, store_type: Optional[StoreType] = None) -> Optional[Store]:
        return await self._repo.update(store_id, name, store_type)

    async def delete(self, store_id: uuid.UUID) -> None:
        await self._repo.delete(store_id)


async def extract_image_url(url: str) -> Optional[str]:
    try:
        async with httpx.AsyncClient(timeout=8, follow_redirects=True) as client:
            resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code != 200:
                return None
            soup = BeautifulSoup(resp.text, "lxml")
            for prop in ("og:image", "twitter:image"):
                meta = soup.find("meta", property=prop) or soup.find("meta", attrs={"name": prop})
                if meta and meta.get("content"):
                    return meta["content"]
    except Exception:
        return None
    return None


class ItemService:
    def __init__(self, repo: IItemRepository):
        self._repo = repo

    async def get_all(self, list_type: Optional[ListType] = None, category_id: Optional[uuid.UUID] = None, store_id: Optional[uuid.UUID] = None, checked: Optional[bool] = None) -> List[Item]:
        return await self._repo.get_all(list_type, category_id, store_id, checked)

    async def get_by_id(self, item_id: uuid.UUID) -> Optional[Item]:
        return await self._repo.get_by_id(item_id)

    async def create(self, data: dict) -> Item:
        item = Item(**data)
        return await self._repo.create(item)

    async def update(self, item_id: uuid.UUID, data: dict) -> Optional[Item]:
        return await self._repo.update(item_id, data)

    async def update_image(self, item_id: uuid.UUID, image_url: str) -> Optional[Item]:
        return await self._repo.update(item_id, {"image_url": image_url})

    async def delete(self, item_id: uuid.UUID) -> None:
        await self._repo.delete(item_id)

    async def toggle_checked(self, item_id: uuid.UUID) -> Optional[Item]:
        return await self._repo.toggle_checked(item_id)
