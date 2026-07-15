import httpx
from fastapi import APIRouter

router = APIRouter(prefix="/exchange", tags=["exchange"])


@router.get("/usd-cop")
def usd_cop_rate():
    try:
        resp = httpx.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        data = resp.json()
        cop = data["rates"]["COP"]
        return {"usd_cop": cop}
    except Exception:
        return {"usd_cop": None}
