import json
import uuid
from datetime import datetime
from typing import Any, Optional

import httpx

from app.config import settings

_client: Optional[httpx.Client] = None


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(
            base_url=f"{settings.supabase_url}/rest/v1",
            headers={
                "apikey": settings.supabase_key,
                "Authorization": f"Bearer {settings.supabase_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=10,
        )
    return _client


def to_uuid(val: Any) -> Optional[uuid.UUID]:
    if isinstance(val, uuid.UUID):
        return val
    if isinstance(val, str):
        return uuid.UUID(val)
    return None


def parse_row(row: dict) -> dict:
    parsed = {}
    for k, v in row.items():
        if k.endswith("_id") and v:
            parsed[k] = to_uuid(v)
        elif k == "id" and v:
            parsed[k] = to_uuid(v)
        elif k.endswith("_at") and v:
            parsed[k] = datetime.fromisoformat(v.replace("Z", "+00:00")) if isinstance(v, str) else v
        elif isinstance(v, str) and v.lower() in ("true", "false"):
            parsed[k] = v.lower() == "true"
        else:
            parsed[k] = v
    return parsed


def supabase_get(table: str, params: Optional[dict] = None) -> list[dict]:
    client = _get_client()
    resp = client.get(f"/{table}", params=params or {})
    resp.raise_for_status()
    return [parse_row(r) for r in resp.json()]


def supabase_get_by_id(table: str, id_val: uuid.UUID) -> Optional[dict]:
    client = _get_client()
    resp = client.get(f"/{table}", params={"id": f"eq.{id_val}", "select": "*"})
    resp.raise_for_status()
    rows = resp.json()
    return parse_row(rows[0]) if rows else None


def supabase_insert(table: str, data: dict) -> dict:
    client = _get_client()
    resp = client.post(
        f"/{table}",
        content=json.dumps(data, default=str),
        headers={"Prefer": "return=representation"},
    )
    resp.raise_for_status()
    rows = resp.json()
    return parse_row(rows[0]) if rows else {}


def supabase_update(table: str, id_val: uuid.UUID, data: dict) -> Optional[dict]:
    client = _get_client()
    resp = client.patch(
        f"/{table}",
        params={"id": f"eq.{id_val}"},
        content=json.dumps(data, default=str),
        headers={"Prefer": "return=representation"},
    )
    resp.raise_for_status()
    rows = resp.json()
    return parse_row(rows[0]) if rows else None


def supabase_delete(table: str, id_val: uuid.UUID) -> None:
    client = _get_client()
    resp = client.delete(f"/{table}", params={"id": f"eq.{id_val}"})
    resp.raise_for_status()
