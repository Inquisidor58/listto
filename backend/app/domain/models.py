import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


class ListType(str, enum.Enum):
    MERCADO = "mercado"
    ONLINE = "online"
    DESEOS = "deseos"


class StoreType(str, enum.Enum):
    MERCADO = "mercado"
    ONLINE = "online"
    AMBOS = "ambos"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    alias: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    items = relationship("Item", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    items = relationship("Item", back_populates="category")


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    store_type: Mapped[StoreType] = mapped_column(Enum(StoreType), default=StoreType.MERCADO, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    items = relationship("Item", back_populates="store")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    list_type: Mapped[ListType] = mapped_column(Enum(ListType), default=ListType.MERCADO, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    checked: Mapped[bool] = mapped_column(Boolean, default=False)
    category_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    store_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("stores.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    category = relationship("Category", back_populates="items")
    store = relationship("Store", back_populates="items")
    user = relationship("User", back_populates="items")
