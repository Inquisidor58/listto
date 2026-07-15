from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from app.config import settings

IS_SUPABASE = bool(settings.supabase_url and settings.supabase_key)


class Base(DeclarativeBase):
    pass


engine = None
SessionLocal = None

if not IS_SUPABASE:
    engine = create_engine(settings.database_url, echo=False)
    SessionLocal = sessionmaker(engine, expire_on_commit=False)


def get_session():
    if IS_SUPABASE:
        raise NotImplementedError("Supabase mode doesn't use SQL sessions")
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
    if not IS_SUPABASE and engine is not None:
        Base.metadata.create_all(engine)
