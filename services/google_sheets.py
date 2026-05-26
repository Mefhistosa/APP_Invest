import os
import csv
import io
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

SHEET1_ID = "1jyEveMHVnwqZzAFBLTMiynmot-tafYnhavijpVBoadU"
SHEET2_ID = "1e0upnG4TNa-NRMZS3tAWvaZk3_P7V4EYA1NAPuim-aE"

SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "service_account.json")
OAUTH_CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials.json")
AUTHORIZED_USER_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "authorized_user.json")

MOCK_PORTFOLIO = [
    {"ticker": "ITUB4", "name": "Itau Unibanco", "quantity": 100, "avg_price": 35.50},
    {"ticker": "PETR4", "name": "Petrobras", "quantity": 50, "avg_price": 42.30},
    {"ticker": "VALE3", "name": "Vale", "quantity": 30, "avg_price": 68.90},
    {"ticker": "BBDC4", "name": "Bradesco", "quantity": 80, "avg_price": 18.75},
    {"ticker": "BBAS3", "name": "Banco do Brasil", "quantity": 60, "avg_price": 24.50},
    {"ticker": "WEGE3", "name": "WEG", "quantity": 40, "avg_price": 38.20},
    {"ticker": "ABEV3", "name": "Ambev", "quantity": 120, "avg_price": 14.80},
    {"ticker": "BBSE3", "name": "BB Seguridade", "quantity": 70, "avg_price": 30.40},
    {"ticker": "ITSA4", "name": "Itausa", "quantity": 200, "avg_price": 10.90},
    {"ticker": "SANB11", "name": "Santander", "quantity": 90, "avg_price": 28.60},
    {"ticker": "TAEE11", "name": "Taesa", "quantity": 50, "avg_price": 38.00},
    {"ticker": "PRIO3", "name": "Petrorio", "quantity": 35, "avg_price": 55.20},
    {"ticker": "RENT3", "name": "Localiza", "quantity": 25, "avg_price": 42.50},
    {"ticker": "EGIE3", "name": "Engie Brasil", "quantity": 45, "avg_price": 30.80},
    {"ticker": "CMIG4", "name": "Cemig", "quantity": 150, "avg_price": 10.20},
]

MOCK_DIVIDENDS = {
    "ITUB4": [
        {"value": 0.45, "date_com": "2026-04-15", "date_pay": "2026-05-05", "type": "JCP", "dy": 8.5},
        {"value": 0.52, "date_com": "2026-01-10", "date_pay": "2026-02-05", "type": "DIVIDENDO", "dy": 8.5},
    ],
    "PETR4": [
        {"value": 1.85, "date_com": "2026-03-20", "date_pay": "2026-04-25", "type": "DIVIDENDO", "dy": 15.2},
        {"value": 2.10, "date_com": "2025-12-15", "date_pay": "2026-01-20", "type": "JCP", "dy": 15.2},
    ],
    "VALE3": [
        {"value": 2.65, "date_com": "2026-04-01", "date_pay": "2026-04-30", "type": "DIVIDENDO", "dy": 12.5},
        {"value": 3.12, "date_com": "2025-11-20", "date_pay": "2025-12-15", "type": "JCP", "dy": 12.5},
    ],
    "BBDC4": [
        {"value": 0.28, "date_com": "2026-03-10", "date_pay": "2026-04-10", "type": "JCP", "dy": 6.8},
        {"value": 0.35, "date_com": "2025-12-05", "date_pay": "2026-01-15", "type": "DIVIDENDO", "dy": 6.8},
    ],
    "BBAS3": [
        {"value": 0.55, "date_com": "2026-04-05", "date_pay": "2026-05-10", "type": "JCP", "dy": 9.1},
        {"value": 0.62, "date_com": "2026-01-20", "date_pay": "2026-02-20", "type": "DIVIDENDO", "dy": 9.1},
    ],
    "WEGE3": [
        {"value": 0.18, "date_com": "2026-03-25", "date_pay": "2026-04-20", "type": "DIVIDENDO", "dy": 3.2},
    ],
    "ABEV3": [
        {"value": 0.22, "date_com": "2026-02-10", "date_pay": "2026-03-15", "type": "DIVIDENDO", "dy": 4.5},
    ],
    "BBSE3": [
        {"value": 0.65, "date_com": "2026-04-10", "date_pay": "2026-05-05", "type": "DIVIDENDO", "dy": 7.2},
        {"value": 0.70, "date_com": "2025-12-20", "date_pay": "2026-01-25", "type": "JCP", "dy": 7.2},
    ],
    "ITSA4": [
        {"value": 0.32, "date_com": "2026-03-30", "date_pay": "2026-04-25", "type": "JCP", "dy": 9.2},
        {"value": 0.38, "date_com": "2025-12-10", "date_pay": "2026-01-20", "type": "DIVIDENDO", "dy": 9.2},
    ],
    "SANB11": [
        {"value": 0.41, "date_com": "2026-02-28", "date_pay": "2026-03-31", "type": "JCP", "dy": 5.5},
    ],
    "TAEE11": [
        {"value": 0.90, "date_com": "2026-04-20", "date_pay": "2026-05-15", "type": "DIVIDENDO", "dy": 8.5},
        {"value": 1.05, "date_com": "2026-01-15", "date_pay": "2026-02-10", "type": "DIVIDENDO", "dy": 8.5},
    ],
    "PRIO3": [
        {"value": 1.50, "date_com": "2026-03-15", "date_pay": "2026-04-20", "type": "DIVIDENDO", "dy": 10.0},
    ],
    "RENT3": [
        {"value": 0.42, "date_com": "2026-04-08", "date_pay": "2026-05-06", "type": "DIVIDENDO", "dy": 3.5},
    ],
    "EGIE3": [
        {"value": 0.60, "date_com": "2026-03-05", "date_pay": "2026-04-10", "type": "DIVIDENDO", "dy": 7.0},
        {"value": 0.55, "date_com": "2025-12-01", "date_pay": "2026-01-10", "type": "JCP", "dy": 7.0},
    ],
    "CMIG4": [
        {"value": 0.18, "date_com": "2026-04-12", "date_pay": "2026-05-08", "type": "DIVIDENDO", "dy": 6.0},
    ],
}


def get_mock_portfolio() -> List[Dict]:
    return MOCK_PORTFOLIO


def get_mock_dividends() -> Dict[str, List[Dict]]:
    return MOCK_DIVIDENDS


def _get_gspread_client():
    try:
        if os.path.exists(SERVICE_ACCOUNT_FILE):
            import gspread
            gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
            return gc
    except Exception as e:
        print(f"Erro ao autenticar com service account: {e}")

    try:
        if os.path.exists(OAUTH_CREDENTIALS_FILE):
            import gspread
            gc = gspread.oauth(
                credentials_filename=OAUTH_CREDENTIALS_FILE,
                authorized_user_filename=AUTHORIZED_USER_FILE,
            )
            return gc
    except Exception as e:
        print(f"Erro ao autenticar com OAuth2: {e}")

    return None


async def fetch_sheet_as_csv(sheet_id: str) -> Optional[str]:
    import httpx
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(url)
            if resp.status_code == 200 and resp.text:
                return resp.text
        return None
    except Exception as e:
        print(f"Error fetching sheet {sheet_id}: {e}")
        return None


def parse_portfolio_from_csv(csv_text: str) -> List[Dict]:
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)

    if len(rows) < 4:
        return []

    data_rows = [r for r in rows[3:40] if len(r) >= 5 and r[0].strip()]

    grouped = {}
    for row in data_rows:
        ticker = row[0].strip().upper()
        if not ticker:
            continue

        try:
            quantity = abs(float(str(row[3]).replace(",", ".").strip())) if len(row) > 3 else 0
            price = float(str(row[4]).replace(",", ".").strip()) if len(row) > 4 else 0
        except (ValueError, IndexError):
            continue

        if quantity == 0 and price == 0:
            continue

        if ticker not in grouped:
            grouped[ticker] = {"total_qty": 0.0, "total_cost": 0.0, "count": 0}

        grouped[ticker]["total_qty"] += quantity
        grouped[ticker]["total_cost"] += quantity * price
        grouped[ticker]["count"] += 1

    portfolio = []
    for ticker, data in grouped.items():
        total_qty = data["total_qty"]
        avg_price = round(data["total_cost"] / total_qty, 2) if total_qty > 0 else 0
        portfolio.append({
            "ticker": ticker,
            "name": ticker,
            "quantity": round(total_qty, 4),
            "avg_price": avg_price,
        })

    portfolio.sort(key=lambda x: x["quantity"] * x["avg_price"], reverse=True)
    return portfolio


def parse_portfolio_from_worksheet(worksheet) -> List[Dict]:
    rows = worksheet.get_all_values()
    if len(rows) < 4:
        return []

    data_rows = [r for r in rows[3:40] if len(r) >= 5 and r[0].strip()]

    grouped = {}
    for row in data_rows:
        ticker = row[0].strip().upper()
        if not ticker:
            continue

        try:
            quantity = abs(float(str(row[3]).replace(",", ".").strip())) if len(row) > 3 else 0
            price = float(str(row[4]).replace(",", ".").strip()) if len(row) > 4 else 0
        except (ValueError, IndexError):
            continue

        if quantity == 0 and price == 0:
            continue

        if ticker not in grouped:
            grouped[ticker] = {"total_qty": 0.0, "total_cost": 0.0, "count": 0}

        grouped[ticker]["total_qty"] += quantity
        grouped[ticker]["total_cost"] += quantity * price
        grouped[ticker]["count"] += 1

    portfolio = []
    for ticker, data in grouped.items():
        total_qty = data["total_qty"]
        avg_price = round(data["total_cost"] / total_qty, 2) if total_qty > 0 else 0
        portfolio.append({
            "ticker": ticker,
            "name": ticker,
            "quantity": round(total_qty, 4),
            "avg_price": avg_price,
        })

    portfolio.sort(key=lambda x: x["quantity"] * x["avg_price"], reverse=True)
    return portfolio


async def get_portfolio_from_sheets() -> List[Dict]:
    from services.ods_reader import get_portfolio_from_ods

    ods_result = get_portfolio_from_ods()
    if ods_result:
        return ods_result

    gc = _get_gspread_client()
    if gc:
        for sheet_id in (SHEET1_ID, SHEET2_ID):
            try:
                sh = gc.open_by_key(sheet_id)
                ws = sh.sheet1
                result = parse_portfolio_from_worksheet(ws)
                if result:
                    return result
            except Exception as e:
                print(f"Erro ao acessar planilha {sheet_id} via gspread: {e}")

    csv1 = await fetch_sheet_as_csv(SHEET1_ID)
    if csv1:
        result = parse_portfolio_from_csv(csv1)
        if result:
            return result

    csv2 = await fetch_sheet_as_csv(SHEET2_ID)
    if csv2:
        result = parse_portfolio_from_csv(csv2)
        if result:
            return result

    return get_mock_portfolio()


async def get_portfolio_dividends(tickers: List[str]) -> Dict[str, List[Dict]]:
    mock = get_mock_dividends()
    result = {}
    for t in tickers:
        if t in mock:
            result[t] = mock[t]
        else:
            result[t] = [
                {"value": round(5.0 * 30 / 100, 2), "date_com": "2026-04-01", "date_pay": "2026-05-01", "type": "DIVIDENDO", "dy": 5.0}
            ]
    return result
