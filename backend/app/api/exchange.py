import httpx
from fastapi import APIRouter

router = APIRouter(prefix="/exchange", tags=["exchange"])


@router.get("/usd-cop")
async def usd_cop_rate():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get("https://open.er-api.com/v6/latest/USD")
            data = resp.json()
            cop = data["rates"]["COP"]
            return {"usd_cop": cop}
    except Exception:
        return {"usd_cop": None}
