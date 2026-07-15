import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.domain.models import ListType, StoreType


class UserCreate(BaseModel):
    name: str
    alias: Optional[str] = None


class UserUpdateAlias(BaseModel):
    alias: str


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    alias: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StoreCreate(BaseModel):
    name: str
    store_type: StoreType = StoreType.MERCADO


class StoreUpdate(BaseModel):
    name: Optional[str] = None
    store_type: Optional[StoreType] = None


class StoreResponse(BaseModel):
    id: uuid.UUID
    name: str
    store_type: StoreType
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ItemCreate(BaseModel):
    list_type: ListType = ListType.MERCADO
    name: str
    quantity: int = 1
    url: Optional[str] = None
    notes: Optional[str] = None
    category_id: Optional[uuid.UUID] = None
    store_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    url: Optional[str] = None
    notes: Optional[str] = None
    category_id: Optional[uuid.UUID] = None
    store_id: Optional[uuid.UUID] = None
    checked: Optional[bool] = None


class ItemResponse(BaseModel):
    id: uuid.UUID
    list_type: ListType
    name: str
    quantity: int
    url: Optional[str]
    image_url: Optional[str]
    notes: Optional[str]
    checked: bool
    category_id: Optional[uuid.UUID]
    store_id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
