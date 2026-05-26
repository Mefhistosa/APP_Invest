import os
import httpx
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.hgbrasil.com/finance"
API_KEY = os.getenv("HG_BRASIL_KEY", "")


async def get_stock_price(symbol: str) -> Optional[Dict]:
    if not API_KEY:
        return None
    try:
        url = f"{BASE_URL}/stock_price"
        params = {"key": API_KEY, "symbol": symbol.lower()}
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("results", {}).get(symbol.upper()):
                    return data["results"][symbol.upper()]
        return None
    except Exception as e:
        print(f"HG Brasil stock_price error for {symbol}: {e}")
        return None


async def get_stock_prices(symbols: List[str]) -> Dict:
    if not API_KEY:
        return {}
    try:
        symbols_str = ",".join([s.lower() for s in symbols])
        url = f"{BASE_URL}/stock_price"
        params = {"key": API_KEY, "symbol": symbols_str}
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                return {k.upper(): v for k, v in data.get("results", {}).items()}
        return {}
    except Exception as e:
        print(f"HG Brasil batch stock_price error: {e}")
        return {}


async def get_macro_data() -> Optional[Dict]:
    if not API_KEY:
        return None
    try:
        url = BASE_URL
        params = {"key": API_KEY}
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("results", {}).get("taxes"):
                    return data["results"]["taxes"][0]
        return None
    except Exception as e:
        print(f"HG Brasil macro error: {e}")
        return None
