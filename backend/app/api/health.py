import socket

from fastapi import APIRouter
from sqlalchemy import text

from app.infrastructure.database import engine

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    result = {"status": "ok", "checks": {}}

    try:
        host = "db.tdtzpqymfwdrnjdixxcp.supabase.co"
        ip = socket.getaddrinfo(host, 5432)
        result["checks"]["dns"] = f"{host} resolved to {ip[0][4][0]}"
    except Exception as e:
        result["checks"]["dns"] = f"DNS failed: {e}"

    try:
        s = socket.create_connection((host, 5432), timeout=5)
        result["checks"]["tcp"] = f"Port 5432 open via {s.getpeername()}"
        s.close()
    except Exception as e:
        result["checks"]["tcp"] = f"TCP failed: {e}"

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            result["checks"]["db"] = "Database connected"
    except Exception as e:
        result["checks"]["db"] = f"DB failed: {e}"

    return result
