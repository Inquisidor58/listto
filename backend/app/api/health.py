from fastapi import APIRouter
from sqlalchemy import text

from app.infrastructure.database import engine

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health():
    result = {}
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            result["db"] = "connected"
    except Exception as e:
        result["db"] = str(e)
    result["using_url"] = str(engine.url)
    return result
