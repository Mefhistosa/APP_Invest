import os
import httpx
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://data.partnr.ai/v2"
API_TOKEN = os.getenv("PARTNR_TOKEN", "")

HEADERS = {"Authorization": f"Bearer {API_TOKEN}"} if API_TOKEN else {}


async def screener(filters: Dict = None) -> List[Dict]:
    if not API_TOKEN:
        return []
    try:
        url = f"{BASE_URL}/screener"
        params = filters or {}
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers=HEADERS, params=params)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("results", [])
        return []
    except Exception as e:
        print(f"Partnr screener error: {e}")
        return []


async def get_news(tickers: List[str] = None, limit: int = 50) -> List[Dict]:
    if not API_TOKEN:
        return []
    try:
        url = f"{BASE_URL}/noticias"
        params = {"limit": limit}
        if tickers:
            params["tickers"] = ",".join(tickers)
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers=HEADERS, params=params)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("results", [])
        return []
    except Exception as e:
        print(f"Partnr news error: {e}")
        return []


async def get_stock_data(ticker: str) -> Optional[Dict]:
    if not API_TOKEN:
        return None
    try:
        url = f"{BASE_URL}/empresas"
        params = {"ticker": ticker}
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=HEADERS, params=params)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                if results:
                    return results[0] if isinstance(results, list) else results
        return None
    except Exception as e:
        print(f"Partnr stock data error for {ticker}: {e}")
        return None


async def get_quotes(ticker: str) -> List[Dict]:
    if not API_TOKEN:
        return []
    try:
        url = f"{BASE_URL}/cotacoes"
        params = {"ticker": ticker}
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=HEADERS, params=params)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("results", [])
        return []
    except Exception as e:
        print(f"Partnr quotes error for {ticker}: {e}")
        return []
