import json
import urllib.request

from fastapi import APIRouter

router = APIRouter(prefix="/exchange", tags=["exchange"])


@router.get("/usd-cop")
def usd_cop_rate():
    try:
        resp = urllib.request.urlopen("https://open.er-api.com/v6/latest/USD", timeout=5)
        data = json.loads(resp.read())
        return {"usd_cop": data["rates"]["COP"]}
    except Exception:
        return {"usd_cop": None}
