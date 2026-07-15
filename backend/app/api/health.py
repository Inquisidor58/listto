from fastapi import APIRouter

from app.config import settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health():
    return {
        "status": "ok",
        "mode": "supabase" if settings.supabase_url else "sqlite",
    }
