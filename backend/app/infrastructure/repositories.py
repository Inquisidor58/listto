import uuid
from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.domain.interfaces import ICategoryRepository, IItemRepository, IStoreRepository, IUserRepository
from app.domain.models import Category, Item, ListType, Store, StoreType, User


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> List[User]:
        return list(self._session.execute(select(User).order_by(User.name)).scalars().all())

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self._session.get(User, user_id)

    def get_by_name(self, name: str) -> Optional[User]:
        return self._session.execute(select(User).where(User.name == name)).scalar_one_or_none()

    def create(self, name: str, alias: Optional[str] = None) -> User:
        user = User(name=name, alias=alias)
        self._session.add(user)
        self._session.flush()
        self._session.refresh(user)
        return user

    def update_alias(self, user_id: uuid.UUID, alias: str) -> Optional[User]:
        user = self._session.get(User, user_id)
        if user:
            user.alias = alias
            self._session.flush()
            self._session.refresh(user)
        return user

    def delete(self, user_id: uuid.UUID) -> None:
        self._session.execute(delete(User).where(User.id == user_id))


class CategoryRepository(ICategoryRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> List[Category]:
        return list(self._session.execute(select(Category).order_by(Category.name)).scalars().all())

    def get_by_id(self, category_id: uuid.UUID) -> Optional[Category]:
        return self._session.get(Category, category_id)

    def create(self, name: str) -> Category:
        category = Category(name=name)
        self._session.add(category)
        self._session.flush()
        self._session.refresh(category)
        return category

    def update(self, category_id: uuid.UUID, name: str) -> Optional[Category]:
        category = self._session.get(Category, category_id)
        if category:
            category.name = name
            self._session.flush()
            self._session.refresh(category)
        return category

    def delete(self, category_id: uuid.UUID) -> None:
        self._session.execute(delete(Category).where(Category.id == category_id))


class StoreRepository(IStoreRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all(self, store_type: Optional[StoreType] = None) -> List[Store]:
        query = select(Store)
        if store_type is not None:
            query = query.where(Store.store_type.in_([store_type, StoreType.AMBOS]))
        query = query.order_by(Store.name)
        return list(self._session.execute(query).scalars().all())

    def get_by_id(self, store_id: uuid.UUID) -> Optional[Store]:
        return self._session.get(Store, store_id)

    def create(self, name: str, store_type: StoreType = StoreType.MERCADO) -> Store:
        store = Store(name=name, store_type=store_type)
        self._session.add(store)
        self._session.flush()
        self._session.refresh(store)
        return store

    def update(self, store_id: uuid.UUID, name: str, store_type: Optional[StoreType] = None) -> Optional[Store]:
        store = self._session.get(Store, store_id)
        if store:
            store.name = name
            if store_type is not None:
                store.store_type = store_type
            self._session.flush()
            self._session.refresh(store)
        return store

    def delete(self, store_id: uuid.UUID) -> None:
        self._session.execute(delete(Store).where(Store.id == store_id))


class ItemRepository(IItemRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all(self, list_type: Optional[ListType] = None, category_id: Optional[uuid.UUID] = None, store_id: Optional[uuid.UUID] = None, checked: Optional[bool] = None) -> List[Item]:
        query = select(Item)
        if list_type is not None:
            query = query.where(Item.list_type == list_type)
        if category_id is not None:
            query = query.where(Item.category_id == category_id)
        if store_id is not None:
            query = query.where(Item.store_id == store_id)
        if checked is not None:
            query = query.where(Item.checked == checked)
        query = query.order_by(Item.created_at.desc())
        return list(self._session.execute(query).scalars().all())

    def get_by_id(self, item_id: uuid.UUID) -> Optional[Item]:
        return self._session.get(Item, item_id)

    def create(self, item: Item) -> Item:
        self._session.add(item)
        self._session.flush()
        self._session.refresh(item)
        return item

    def update(self, item_id: uuid.UUID, data: dict) -> Optional[Item]:
        item = self._session.get(Item, item_id)
        if item:
            for key, value in data.items():
                setattr(item, key, value)
            self._session.flush()
            self._session.refresh(item)
        return item

    def delete(self, item_id: uuid.UUID) -> None:
        self._session.execute(delete(Item).where(Item.id == item_id))

    def toggle_checked(self, item_id: uuid.UUID) -> Optional[Item]:
        item = self._session.get(Item, item_id)
        if item:
            item.checked = not item.checked
            self._session.flush()
            self._session.refresh(item)
        return item