from urllib.parse import quote, urlparse

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from app.config import settings


def _get_engine():
    url = settings.database_url
    if "+asyncpg" in url:
        url = url.replace("+asyncpg", "+pg8000")

    if "pg8000" in url and "pooler" not in url and "db." in url:
        parsed = urlparse(url)
        project_ref = parsed.hostname.replace("db.", "").replace(".supabase.co", "")
        pw = parsed.password or ""
        url = (
            f"postgresql+pg8000://postgres.{project_ref}:{quote(pw, safe='')}"
            f"@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
        )

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
