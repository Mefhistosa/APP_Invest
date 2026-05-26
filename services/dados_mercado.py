import os
import httpx
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.dadosdemercado.com.br/v1"
TOKEN = os.getenv("DADOS_MERCADO_TOKEN", "")

HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}


async def get_market_ratios(cvm_code: int) -> Optional[Dict]:
    if not TOKEN:
        return None
    try:
        url = f"{BASE_URL}/companies/{cvm_code}/market_ratios"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=HEADERS)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("results"):
                    return data["results"][-1] if isinstance(data["results"], list) else data["results"]
        return None
    except Exception as e:
        print(f"Dados de Mercado market_ratios error: {e}")
        return None


async def get_financial_ratios(cvm_code: int) -> Optional[Dict]:
    if not TOKEN:
        return None
    try:
        url = f"{BASE_URL}/companies/{cvm_code}/ratios?statement_type=con&period_type=ttm"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=HEADERS)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("results"):
                    return data["results"][-1] if isinstance(data["results"], list) else data["results"]
        return None
    except Exception as e:
        print(f"Dados de Mercado financial_ratios error: {e}")
        return None


async def get_dividends(cvm_code: int) -> List[Dict]:
    if not TOKEN:
        return []
    try:
        url = f"{BASE_URL}/companies/{cvm_code}/dividends"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=HEADERS)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("results", [])
        return []
    except Exception as e:
        print(f"Dados de Mercado dividends error: {e}")
        return []


async def get_dividend_yield(ticker: str) -> List[Dict]:
    if not TOKEN:
        return []
    try:
        url = f"{BASE_URL}/tickers/{ticker}/dy"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=HEADERS)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("results", [])
        return []
    except Exception as e:
        print(f"Dados de Mercado DY error for {ticker}: {e}")
        return []


async def get_stock_quotes(ticker: str, period_init: str = None, period_end: str = None) -> List[Dict]:
    if not TOKEN:
        return []
    try:
        url = f"{BASE_URL}/tickers/{ticker}/quotes"
        params = {}
        if period_init:
            params["period_init"] = period_init
        if period_end:
            params["period_end"] = period_end
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=HEADERS, params=params)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("results", [])
        return []
    except Exception as e:
        print(f"Dados de Mercado quotes error for {ticker}: {e}")
        return []


async def get_companies() -> List[Dict]:
    if not TOKEN:
        return []
    try:
        url = f"{BASE_URL}/companies"
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers=HEADERS)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("results", [])
        return []
    except Exception as e:
        print(f"Dados de Mercado companies error: {e}")
        return []


async def get_news() -> List[Dict]:
    if not TOKEN:
        return []
    try:
        url = f"{BASE_URL}/news"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=HEADERS)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("results", [])
        return []
    except Exception as e:
        print(f"Dados de Mercado news error: {e}")
        return []


CVm_CODE_MAP = {
    "ITUB4": 1023, "BBDC4": 1537, "BBAS3": 1015, "SANB11": 1999, "BPAC11": 20885,
    "BBSE3": 1023, "CXSE3": 21619, "PETR4": 1852, "PRIO3": 22330, "VALE3": 4689,
    "CSNA3": 2310, "GGBR4": 3302, "USIM5": 4457, "GOAU4": 3305, "WEGE3": 5410,
    "SUZB3": 22543, "KLBN11": 1671, "ABEV3": 22500, "RADL3": 1788, "HYPE3": 1206,
    "RENT3": 1927, "TAEE11": 4055, "CPFE3": 2495, "EGIE3": 2892, "ENGI11": 2953,
    "EQTL3": 3509, "TRPL4": 4224, "SBSP3": 4647, "ITSA4": 1023, "BBDC3": 1537,
    "BRAP4": 2471, "CSAN3": 2211, "VBBR3": 1849, "VIVT3": 2052, "TIMS3": 22836,
    "MGLU3": 19439, "AMER3": 5702, "LREN3": 1682, "AZZA3": 5637, "CYRE3": 1340,
    "MRVE3": 1728, "TOTS3": 4383, "B3SA3": 22552, "CMIG4": 2404, "CPLE3": 1241,
    "CSMG3": 1528, "PSSA3": 1777, "FLRY3": 1341, "RDOR3": 2074, "EMBJ3": 1295,
    "RAIL3": 1795, "ALOS3": 1192, "ASAI3": 22202, "SMFT3": 22195, "ENEV3": 22186,
    "VAMO3": 1857, "ROMI3": 1817, "CEAB3": 1617, "CURY3": 22262, "COGN3": 1344,
    "VVAR3": 5280, "PNVL3": 1735,
}


def get_cvm_code(ticker: str) -> Optional[int]:
    return CVm_CODE_MAP.get(ticker.upper())
