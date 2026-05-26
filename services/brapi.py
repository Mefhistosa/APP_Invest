import os
import httpx
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

BRAPI_URL = "https://brapi.dev/api"
BRAPI_TOKEN = os.getenv("BRAPI_TOKEN", "free")


async def get_stock_quote(ticker: str) -> Optional[Dict]:
    try:
        url = f"{BRAPI_URL}/quote/{ticker}?token={BRAPI_TOKEN}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            data = resp.json()
            if data.get("results") and len(data["results"]) > 0:
                return data["results"][0]
        return None
    except Exception as e:
        print(f"Brapi error for {ticker}: {e}")
        return None


async def get_multiple_quotes(tickers: List[str]) -> List[Dict]:
    try:
        tickers_str = ",".join(tickers)
        url = f"{BRAPI_URL}/quote/{tickers_str}?token={BRAPI_TOKEN}"
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url)
            data = resp.json()
            return data.get("results", [])
    except Exception as e:
        print(f"Brapi batch error: {e}")
        return []


async def get_stock_history(ticker: str, days: int = 365) -> List[Dict]:
    try:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        url = f"{BRAPI_URL}/quote/{ticker}?token={BRAPI_TOKEN}&range={days}d"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            data = resp.json()
            return data.get("results", [])
    except Exception as e:
        print(f"Brapi history error for {ticker}: {e}")
        return []


async def get_all_tickers() -> List[str]:
    common_tickers = [
        "ITUB4", "BBDC4", "BBAS3", "SANB11", "BPAC11", "BBSE3", "CXSE3",
        "PETR4", "PRIO3", "VALE3", "CSNA3", "GGBR4", "USIM5", "GOAU4",
        "WEGE3", "SUZB3", "KLBN11", "ABEV3", "RADL3", "HYPE3", "RENT3",
        "TAEE11", "TAEE4", "CPFE3", "EGIE3", "ENGI11", "EQTL3", "TRPL4", "SBSP3",
        "ITSA4", "BBDC3", "BRAP4", "CSAN3", "VBBR3", "VIVT3", "TIMS3",
        "MGLU3", "AMER3", "LREN3", "AZZA3", "CYRE3", "MRVE3", "TOTS3",
        "B3SA3", "CMIG4", "CPLE3", "CSMG3", "PSSA3", "FLRY3", "RDOR3",
        "EMBJ3", "RAIL3", "ALOS3", "ASAI3", "SMFT3", "ENEV3", "VAMO3",
        "ROMI3", "CEAB3", "CURY3", "COGN3", "VVAR3", "PNVL3",
    ]
    return list(set(common_tickers))
