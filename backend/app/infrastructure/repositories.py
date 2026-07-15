import enum
import uuid
from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.config import settings
from app.domain.interfaces import ICategoryRepository, IItemRepository, IStoreRepository, IUserRepository
from app.domain.models import Category, Item, ListType, Store, StoreType, User


def _model_kwargs(model_obj):
    cols = {}
    for c in model_obj.__table__.columns:
        val = getattr(model_obj, c.name)
        if isinstance(val, enum.Enum):
            val = val.value
        cols[c.name] = val
    return cols

USE_SUPABASE = bool(settings.supabase_url and settings.supabase_key)


class UserRepository(IUserRepository):
    def __init__(self, session: Optional[Session] = None):
        self._session = session

    def get_all(self) -> List[User]:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_get as get
            rows = get("users", {"select": "*", "order": "name.asc"})
            return [User(**r) for r in rows]
        return list(self._session.execute(select(User).order_by(User.name)).scalars().all())

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_get_by_id as get
            row = get("users", user_id)
            return User(**row) if row else None
        return self._session.get(User, user_id)

    def get_by_name(self, name: str) -> Optional[User]:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_get as get
            rows = get("users", {"name": f"eq.{name}", "select": "*"})
            return User(**rows[0]) if rows else None
        return self._session.execute(select(User).where(User.name == name)).scalar_one_or_none()

    def create(self, name: str, alias: Optional[str] = None) -> User:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_insert as ins
            row = ins("users", {"name": name, "alias": alias})
            return User(**row)
        user = User(name=name, alias=alias)
        self._session.add(user)
        self._session.flush()
        self._session.refresh(user)
        return user

    def update_alias(self, user_id: uuid.UUID, alias: str) -> Optional[User]:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_update as upd
            row = upd("users", user_id, {"alias": alias})
            return User(**row) if row else None
        user = self._session.get(User, user_id)
        if user:
            user.alias = alias
            self._session.flush()
            self._session.refresh(user)
        return user

    def delete(self, user_id: uuid.UUID) -> None:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_delete as dlt
            dlt("users", user_id)
            return
        self._session.execute(delete(User).where(User.id == user_id))


class CategoryRepository(ICategoryRepository):
    def __init__(self, session: Optional[Session] = None):
        self._session = session

    def get_all(self) -> List[Category]:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_get as get
            rows = get("categories", {"select": "*", "order": "name.asc"})
            return [Category(**r) for r in rows]
        return list(self._session.execute(select(Category).order_by(Category.name)).scalars().all())

    def get_by_id(self, category_id: uuid.UUID) -> Optional[Category]:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_get_by_id as get
            row = get("categories", category_id)
            return Category(**row) if row else None
        return self._session.get(Category, category_id)

    def create(self, name: str) -> Category:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_insert as ins
            row = ins("categories", {"name": name})
            return Category(**row)
        category = Category(name=name)
        self._session.add(category)
        self._session.flush()
        self._session.refresh(category)
        return category

    def update(self, category_id: uuid.UUID, name: str) -> Optional[Category]:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_update as upd
            row = upd("categories", category_id, {"name": name})
            return Category(**row) if row else None
        category = self._session.get(Category, category_id)
        if category:
            category.name = name
            self._session.flush()
            self._session.refresh(category)
        return category

    def delete(self, category_id: uuid.UUID) -> None:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_delete as dlt
            dlt("categories", category_id)
            return
        self._session.execute(delete(Category).where(Category.id == category_id))


class StoreRepository(IStoreRepository):
    def __init__(self, session: Optional[Session] = None):
        self._session = session

    def get_all(self, store_type: Optional[StoreType] = None) -> List[Store]:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_get as get
            params = {"select": "*", "order": "name.asc"}
            if store_type:
                params["store_type"] = f"in.({store_type.value},{StoreType.AMBOS.value})"
            rows = get("stores", params)
            return [Store(**r) for r in rows]
        query = select(Store)
        if store_type is not None:
            query = query.where(Store.store_type.in_([store_type, StoreType.AMBOS]))
        query = query.order_by(Store.name)
        return list(self._session.execute(query).scalars().all())

    def get_by_id(self, store_id: uuid.UUID) -> Optional[Store]:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_get_by_id as get
            row = get("stores", store_id)
            return Store(**row) if row else None
        return self._session.get(Store, store_id)

    def create(self, name: str, store_type: StoreType = StoreType.MERCADO) -> Store:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_insert as ins
            row = ins("stores", {"name": name, "store_type": store_type.value})
            return Store(**row)
        store = Store(name=name, store_type=store_type)
        self._session.add(store)
        self._session.flush()
        self._session.refresh(store)
        return store

    def update(self, store_id: uuid.UUID, name: str, store_type: Optional[StoreType] = None) -> Optional[Store]:
        data = {"name": name}
        if store_type is not None:
            data["store_type"] = store_type.value
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_update as upd
            row = upd("stores", store_id, data)
            return Store(**row) if row else None
        store = self._session.get(Store, store_id)
        if store:
            store.name = name
            if store_type is not None:
                store.store_type = store_type
            self._session.flush()
            self._session.refresh(store)
        return store

    def delete(self, store_id: uuid.UUID) -> None:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_delete as dlt
            dlt("stores", store_id)
            return
        self._session.execute(delete(Store).where(Store.id == store_id))


class ItemRepository(IItemRepository):
    def __init__(self, session: Optional[Session] = None):
        self._session = session

    def get_all(self, list_type: Optional[ListType] = None, category_id: Optional[uuid.UUID] = None, store_id: Optional[uuid.UUID] = None, checked: Optional[bool] = None) -> List[Item]:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_get as get
            params = {"select": "*", "order": "created_at.desc"}
            if list_type:
                params["list_type"] = f"eq.{list_type.value}"
            if category_id:
                params["category_id"] = f"eq.{category_id}"
            if store_id:
                params["store_id"] = f"eq.{store_id}"
            if checked is not None:
                params["checked"] = f"eq.{str(checked).lower()}"
            rows = get("items", params)
            return [Item(**r) for r in rows]
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
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_get_by_id as get
            row = get("items", item_id)
            return Item(**row) if row else None
        return self._session.get(Item, item_id)

    def create(self, item: Item) -> Item:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_insert as ins
            data = _model_kwargs(item)
            data.pop("id", None)
            row = ins("items", data)
            return Item(**row)
        self._session.add(item)
        self._session.flush()
        self._session.refresh(item)
        return item

    def update(self, item_id: uuid.UUID, data: dict) -> Optional[Item]:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_update as upd
            clean = {}
            for k, v in data.items():
                if isinstance(v, enum.Enum):
                    clean[k] = v.value
                elif isinstance(v, uuid.UUID):
                    clean[k] = str(v)
                elif v is not None:
                    clean[k] = v
            row = upd("items", item_id, clean)
            return Item(**row) if row else None
        item = self._session.get(Item, item_id)
        if item:
            for key, value in data.items():
                setattr(item, key, value)
            self._session.flush()
            self._session.refresh(item)
        return item

    def delete(self, item_id: uuid.UUID) -> None:
        if USE_SUPABASE:
            from app.infrastructure.supabase import supabase_delete as dlt
            dlt("items", item_id)
            return
        self._session.execute(delete(Item).where(Item.id == item_id))

    def toggle_checked(self, item_id: uuid.UUID) -> Optional[Item]:
        if USE_SUPABASE:
            item = self.get_by_id(item_id)
            if item:
                return self.update(item_id, {"checked": not item.checked})
            return None
        item = self._session.get(Item, item_id)
        if item:
            item.checked = not item.checked
            self._session.flush()
            self._session.refresh(item)
        return item
