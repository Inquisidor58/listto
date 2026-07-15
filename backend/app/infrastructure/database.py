from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from app.config import settings


def _get_engine():
    url = settings.database_url
    if url.startswith("postgresql+asyncpg"):
        url = url.replace("+asyncpg", "+pg8000")
    if "pg8000" in url and "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    if "pg8000" in url:
        url = url.replace("%2A", "*").replace("%2a", "*")
    return create_engine(url, echo=False)


engine = _get_engine()
SessionLocal = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(engine)
