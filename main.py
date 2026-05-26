import os
import shutil
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List, Optional

from models.schemas import (
    Stock, NewsAnalysisResult, DividendCalendar, MacroData, Profile,
    PriceHistoryItem, DividendItem, DividendType,
    PortfolioItem, PortfolioResponse, PortfolioDividend, PortfolioDividendResponse,
)
from skills.stock_skill import get_stocks_by_profile, get_all_filters
from skills.news_skill import analyze_news_sentiment
from services.hgbrasil import get_macro_data
from services.brapi import get_stock_history, get_stock_quote
from services.dados_mercado import get_cvm_code, get_dividends as get_dm_dividends
from services.google_sheets import get_portfolio_from_sheets, get_portfolio_dividends
from services.custom_portfolio import add_stock as add_custom_stock, get_all as get_custom_stocks, sell_stock as sell_custom_stock

TICKER_ALIASES = {
    "TAEE4": "TAEE11",
}

REALISTIC_PRICES = {
    "ITUB4": 41.78, "BBAS3": 22.07, "BBSE3": 34.83, "TAEE11": 42.22,
    "TAEE4": 13.35,
    "CPFE3": 49.74, "PSSA3": 49.61, "CXSE3": 17.60, "ENGI11": 54.05,
    "EQTL3": 43.68, "SBSP3": 32.87, "BBDC4": 19.27, "ITSA4": 13.60,
    "SANB11": 29.33, "BPAC11": 59.02, "PETR4": 47.27, "PRIO3": 66.54,
    "VALE3": 81.23, "SUZB3": 43.01, "WEGE3": 44.94, "CMIG4": 11.97,
    "EGIE3": 33.82, "CPLE3": 15.75, "TRPL4": 28.50, "CSMG3": 55.25,
    "ALOS3": 31.21, "GGBR4": 24.36, "USIM5": 8.74, "CSNA3": 6.70,
    "ABEV3": 16.95, "VIVT3": 39.19, "RENT3": 47.65, "MGLU3": 8.03,
    "LREN3": 14.69, "CYRE3": 23.20, "RADL3": 21.76, "HYPE3": 23.47,
    "VBBR3": 32.83, "RAIL3": 16.69, "B3SA3": 18.36, "RDOR3": 40.35,
    "ROMI3": 6.85, "FLRY3": 16.83, "ASAI3": 9.35, "SMFT3": 18.18,
    "ENEV3": 27.59, "VAMO3": 4.01, "CEAB3": 12.28, "CURY3": 31.48,
    "COGN3": 2.81, "VVAR3": 6.80,
}

app = FastAPI(
    title="APP Investidor API",
    description="API para recomendacao de acoes por perfil de investidor",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/stocks/{profile}")
async def get_stocks(profile: str) -> List[Stock]:
    try:
        profile_enum = Profile(profile)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Perfil invalido: {profile}. Use 'iniciante', 'moderado' ou 'agressivo'.")
    stocks = await get_stocks_by_profile(profile_enum)
    return stocks


@app.get("/api/v1/news/{ticker}")
async def get_news(ticker: str) -> NewsAnalysisResult:
    result = await analyze_news_sentiment(ticker.upper())
    return result


@app.get("/api/v1/dividends/{ticker}")
async def get_dividends(ticker: str) -> DividendCalendar:
    cvm = get_cvm_code(ticker.upper())
    if not cvm:
        raise HTTPException(status_code=404, detail=f"Empresa nao encontrada para {ticker}")

    raw_dividends = await get_dm_dividends(cvm)

    if not raw_dividends:
        from skills.stock_skill import get_realistic_data
        realistic = get_realistic_data(ticker.upper())
        dy = realistic.get("dy", 5.0) if realistic else 5.0
        price = realistic.get("price", 30.0) if realistic else 30.0
        div_value = price * dy / 100

        return DividendCalendar(
            ticker=ticker.upper(),
            next_payment_date="2026-06-15",
            cut_off_date="2026-06-01",
            type=DividendType.DIVIDENDO,
            next_amount=div_value / 4,
            ytd_total=div_value * 0.75,
        )

    history = []
    next_pay = None
    next_amount = 0.0
    ytd_total = 0.0

    for div in raw_dividends:
        item = DividendItem(
            ticker=div.get("ticker", ticker.upper()),
            amount=div.get("amount", 0),
            type=div.get("type", "DIVIDENDO"),
            ex_date=div.get("ex_date"),
            payable_date=div.get("payable_date"),
            record_date=div.get("record_date"),
        )
        history.append(item)

        if div.get("payable_date") and div.get("payable_date") >= "2026-05-01":
            if not next_pay or div["payable_date"] < next_pay:
                next_pay = div["payable_date"]
                next_amount = div.get("amount", 0)

        if div.get("payable_date", "").startswith("2026"):
            ytd_total += div.get("amount", 0)

    return DividendCalendar(
        ticker=ticker.upper(),
        next_payment_date=next_pay,
        cut_off_date=history[0].ex_date if history else None,
        type=history[0].type if history else DividendType.DIVIDENDO,
        next_amount=next_amount,
        ytd_total=ytd_total,
        history=history,
    )


@app.get("/api/v1/macro")
async def get_macro() -> MacroData:
    data = await get_macro_data()
    if data:
        return MacroData(
            selic=data.get("selic"),
            cdi=data.get("cdi"),
            date=data.get("date", "2026-05-05"),
        )
    return MacroData(selic=14.75, cdi=14.75, date="2026-05-05")


@app.get("/api/v1/filters")
async def get_filters():
    return get_all_filters()


@app.get("/api/v1/history/{ticker}")
async def get_history(ticker: str, days: int = 30) -> List[PriceHistoryItem]:
    raw = await get_stock_history(ticker.upper(), days)
    if not raw:
        return []
    historical_data = raw[0].get("historicalDataPrice", []) if raw else []
    result = []
    for item in historical_data[-days:]:
        result.append(PriceHistoryItem(
            date=item.get("date", ""),
            open=item.get("open", 0),
            close=item.get("close", 0),
            high=item.get("high", 0),
            low=item.get("low", 0),
            volume=item.get("volume"),
        ))
    return result


@app.get("/api/v1/portfolio")
async def get_portfolio() -> PortfolioResponse:
    portfolio = await get_portfolio_from_sheets()
    custom = get_custom_stocks()

    ods_by_ticker: dict = {}
    for p in portfolio:
        ods_by_ticker[p["ticker"]] = p
    for c in custom:
        t = c["ticker"]
        q = c["quantity"]
        ap = c["avg_price"]
        if t in ods_by_ticker:
            existing = ods_by_ticker[t]
            old_qty = existing["quantity"]
            old_price = existing["avg_price"]
            new_qty = old_qty + q
            new_avg = (old_qty * old_price + q * ap) / new_qty
            existing["quantity"] = new_qty
            existing["avg_price"] = round(new_avg, 2)
        else:
            ods_by_ticker[t] = c

    merged = list(ods_by_ticker.values())
    items = []
    total_invested = 0.0
    total_current = 0.0

    for p in merged:
        ticker = p["ticker"]
        resolved_ticker = TICKER_ALIASES.get(ticker, ticker)
        quantity = p["quantity"]
        avg_price = p["avg_price"]
        total_invested_item = quantity * avg_price

        current_price = None
        try:
            quote = await get_stock_quote(resolved_ticker)
            if quote:
                current_price = quote.get("regularMarketPrice")
        except Exception:
            pass

        if not current_price:
            current_price = REALISTIC_PRICES.get(ticker) or REALISTIC_PRICES.get(resolved_ticker, avg_price * 1.05)

        current_value = quantity * current_price
        variation = ((current_price - avg_price) / avg_price) * 100 if avg_price > 0 else 0
        result = current_value - total_invested_item
        result_percent = ((current_value - total_invested_item) / total_invested_item) * 100 if total_invested_item > 0 else 0

        from skills.stock_skill import get_realistic_data
        rd = get_realistic_data(ticker)
        name = rd.get("name", ticker) if rd else ticker

        items.append(PortfolioItem(
            ticker=ticker,
            name=name,
            quantity=quantity,
            avg_price=avg_price,
            total_invested=round(total_invested_item, 2),
            current_price=round(current_price, 2),
            variation=round(variation, 2),
            current_value=round(current_value, 2),
            result=round(result, 2),
            result_percent=round(result_percent, 2),
        ))
        total_invested += total_invested_item
        total_current += current_value

    return PortfolioResponse(
        items=items,
        total_invested=round(total_invested, 2),
        total_current=round(total_current, 2),
        total_result=round(total_current - total_invested, 2),
        total_result_percent=round(((total_current - total_invested) / total_invested) * 100, 2) if total_invested > 0 else 0,
    )


@app.get("/api/v1/portfolio/dividends")
async def get_portfolio_dividends_endpoint() -> PortfolioDividendResponse:
    portfolio = await get_portfolio_from_sheets()
    tickers = [p["ticker"] for p in portfolio]

    all_dividends = await get_portfolio_dividends(tickers)

    divs = []
    for ticker, dividends in all_dividends.items():
        from skills.stock_skill import get_realistic_data
        rd = get_realistic_data(ticker)
        dy = rd.get("dy", 5.0) if rd else 5.0
        for d in dividends:
            divs.append(PortfolioDividend(
                ticker=ticker,
                value=d.get("value", 0),
                date_com=d.get("date_com", ""),
                date_pay=d.get("date_pay", ""),
                type=d.get("type", "DIVIDENDO"),
                dy=dy,
            ))

    divs.sort(key=lambda x: x.date_pay, reverse=True)
    return PortfolioDividendResponse(dividends=divs)


@app.post("/api/v1/portfolio/upload-ods")
async def upload_portfolio_ods(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".ods"):
        raise HTTPException(status_code=400, detail="Envie um arquivo .ods valido")

    from services.ods_reader import read_ods

    content = await file.read()
    tmp_path = os.path.join(os.path.dirname(__file__), "uploaded_" + file.filename)
    try:
        with open(tmp_path, "wb") as f:
            f.write(content)

        portfolio = read_ods(tmp_path)
        if not portfolio:
            raise HTTPException(status_code=400, detail="Nao foi possivel ler dados do arquivo ODS. Verifique se as colunas 'Ativo', 'QTDE' e 'VL Compra' existem.")

        target_path = os.path.join(os.path.dirname(__file__), "lista_acao.ods")
        shutil.move(tmp_path, target_path)

        return {"status": "ok", "items": portfolio}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar ODS: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.post("/api/v1/portfolio/reload-ods")
async def reload_portfolio_ods():
    from services.ods_reader import get_portfolio_from_ods

    portfolio = get_portfolio_from_ods()
    if not portfolio:
        raise HTTPException(status_code=400, detail="Nao foi possivel ler o arquivo lista_acao.ods. Verifique se o arquivo existe em /home/dsa/Documentos/app_investidor/lista_acao.ods")

    return {"status": "ok", "items": portfolio}


@app.post("/api/v1/portfolio/add")
async def add_portfolio_item(ticker: str = Query(...), quantity: float = Query(...), avg_price: float = Query(...)):
    add_custom_stock(ticker, abs(quantity), abs(avg_price))
    return {"status": "ok", "ticker": ticker.upper(), "quantity": abs(quantity), "avg_price": abs(avg_price)}


@app.post("/api/v1/portfolio/sell")
async def sell_portfolio_item(ticker: str = Query(...), quantity: float = Query(...)):
    abs_qty = abs(quantity)
    if abs_qty <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    portfolio = await get_portfolio_from_sheets()
    custom = get_custom_stocks()
    ods_by_ticker: dict = {}
    for p in portfolio:
        ods_by_ticker[p["ticker"]] = p
    for c in custom:
        t = c["ticker"]
        q = c["quantity"]
        ap = c["avg_price"]
        if t in ods_by_ticker:
            existing = ods_by_ticker[t]
            old_qty = existing["quantity"]
            old_price = existing["avg_price"]
            new_qty = old_qty + q
            new_avg = (old_qty * old_price + q * ap) / new_qty
            existing["quantity"] = new_qty
            existing["avg_price"] = round(new_avg, 2)
        else:
            ods_by_ticker[t] = c
    merged_lookup = ods_by_ticker

    ticker_upper = ticker.upper()
    if ticker_upper not in merged_lookup:
        raise HTTPException(status_code=404, detail=f"Ativo {ticker_upper} nao encontrado na carteira")

    original = merged_lookup[ticker_upper]
    orig_qty = original["quantity"]
    orig_avg = original["avg_price"]

    if abs_qty > orig_qty:
        raise HTTPException(status_code=400, detail=f"Quantidade para vender ({abs_qty}) excede a quantidade disponivel ({orig_qty})")

    sell_custom_stock(ticker_upper, abs_qty,
                      original_quantity=orig_qty, original_avg_price=orig_avg)
    return {"status": "ok", "ticker": ticker_upper, "quantity_sold": abs_qty}


@app.get("/api/v1/portfolio/chart/{ticker}")
async def get_portfolio_chart(ticker: str, days: int = Query(default=30, ge=1, le=365)):
    resolved_ticker = TICKER_ALIASES.get(ticker.upper(), ticker.upper())
    from services.brapi import get_stock_history as brapi_history
    raw = await brapi_history(resolved_ticker, days)
    if raw and raw[0].get("historicalDataPrice"):
        historical = raw[0]["historicalDataPrice"]
        result = []
        for item in historical[-days:]:
            ts = item.get("date", 0)
            if isinstance(ts, (int, float)):
                from datetime import datetime
                d = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            else:
                d = str(ts)
            result.append({
                "date": d,
                "open": item.get("open", 0),
                "high": item.get("high", 0),
                "low": item.get("low", 0),
                "close": item.get("close", 0),
                "volume": item.get("volume"),
            })
        return result

    import random
    from datetime import datetime, timedelta
    result = []
    base_price = REALISTIC_PRICES.get(ticker.upper()) or REALISTIC_PRICES.get(resolved_ticker, 30.0)
    for i in range(days):
        d = (datetime.now() - timedelta(days=days - i - 1)).strftime("%Y-%m-%d")
        var = random.uniform(-0.03, 0.03)
        close = round(base_price * (1 + var), 2)
        result.append({
            "date": d,
            "open": round(close * 0.995, 2),
            "high": round(close * 1.01, 2),
            "low": round(close * 0.99, 2),
            "close": close,
            "volume": random.randint(1000000, 10000000),
        })
        base_price = close
    return result


@app.get("/")
async def serve_index():
    return FileResponse("index.html")


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "version": "1.1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
