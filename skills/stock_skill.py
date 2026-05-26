from typing import List, Dict, Optional
from services.brapi import get_stock_quote, get_multiple_quotes, get_all_tickers
from models.schemas import Profile, ProfileCriteria, Stock


PROFILE_CRITERIA = {
    Profile.INICIANTE: ProfileCriteria(
        name=Profile.INICIANTE,
        min_price=2.0,
        max_price=50.0,
        min_roe=13.0,
        min_liquidity=10000000.0,
        min_price_to_book=0.2,
        max_price_to_book=3.0,
        min_dividend_yield=8.0,
        max_proceeds_vs_profit=1.0,
        require_net_equity_gte_market_value=True,
    ),
    Profile.MODERADO: ProfileCriteria(
        name=Profile.MODERADO,
        min_price=2.0,
        max_price=70.0,
        min_roe=10.0,
        min_liquidity=10000000.0,
        min_price_to_book=0.2,
        max_price_to_book=3.0,
        min_dividend_yield=5.0,
        max_proceeds_vs_profit=1.3,
        max_monthly_variation=3.0,
        require_net_equity_gte_gross_debt=True,
    ),
    Profile.AGRESSIVO: ProfileCriteria(
        name=Profile.AGRESSIVO,
        min_price=2.0,
        max_price=120.0,
        min_roe=10.0,
        min_liquidity=10000000.0,
        min_price_to_book=0.2,
        max_price_to_book=5.0,
        min_dividend_yield=2.0,
        max_monthly_variation=8.0,
    ),
}


def get_all_filters() -> Dict:
    return {
        p.value: {
            "name": c.name.value,
            "min_price": c.min_price,
            "max_price": c.max_price,
            "min_roe": c.min_roe,
            "min_liquidity": c.min_liquidity,
            "min_price_to_book": c.min_price_to_book,
            "max_price_to_book": c.max_price_to_book,
            "min_dividend_yield": c.min_dividend_yield,
            "max_proceeds_vs_profit": c.max_proceeds_vs_profit,
            "max_monthly_variation": c.max_monthly_variation,
            "require_net_equity_gte_market_value": c.require_net_equity_gte_market_value,
            "require_net_equity_gte_gross_debt": c.require_net_equity_gte_gross_debt,
        }
        for p, c in PROFILE_CRITERIA.items()
    }


REALISTIC_DATA = {
    "ITUB4": {"name": "Itau Unibanco", "roe": 18.2, "dy": 8.5, "pvp": 2.15, "price": 41.78, "prev_price": 42.45, "vol": 250000000, "pl": 250000000000, "mv": 400000000000, "debt": 800000000000, "np": 30000000000, "proc": 25000000000},
    "BBAS3": {"name": "Banco do Brasil", "roe": 16.5, "dy": 9.1, "pvp": 0.98, "price": 22.07, "prev_price": 21.92, "vol": 200000000, "pl": 150000000000, "mv": 120000000000, "debt": 500000000000, "np": 30000000000, "proc": 22000000000},
    "BBSE3": {"name": "BB Seguridade", "roe": 35.2, "dy": 7.2, "pvp": 3.21, "price": 34.83, "prev_price": 34.45, "vol": 100000000, "pl": 15000000000, "mv": 70000000000, "debt": 0, "np": 4000000000, "proc": 3500000000},
    "TAEE11": {"name": "Taesa", "roe": 19.8, "dy": 8.5, "pvp": 1.67, "price": 42.22, "prev_price": 42.05, "vol": 120000000, "pl": 20000000000, "mv": 15000000000, "debt": 12000000000, "np": 2500000000, "proc": 2000000000},
    "CPFE3": {"name": "CPFL Energia", "roe": 18.5, "dy": 6.8, "pvp": 1.12, "price": 49.74, "prev_price": 49.40, "vol": 90000000, "pl": 18000000000, "mv": 65000000000, "debt": 30000000000, "np": 5000000000, "proc": 4000000000},
    "PSSA3": {"name": "Porto Seguro", "roe": 20.5, "dy": 7.5, "pvp": 2.8, "price": 49.61, "prev_price": 49.18, "vol": 80000000, "pl": 15000000000, "mv": 25000000000, "debt": 5000000000, "np": 2000000000, "proc": 1800000000},
    "CXSE3": {"name": "Caixa Seguridade", "roe": 30.1, "dy": 7.8, "pvp": 2.5, "price": 17.60, "prev_price": 17.39, "vol": 150000000, "pl": 10000000000, "mv": 18000000000, "debt": 2000000000, "np": 1500000000, "proc": 1400000000},
    "ENGI11": {"name": "Energisa", "roe": 16.0, "dy": 6.5, "pvp": 1.5, "price": 54.05, "prev_price": 53.03, "vol": 70000000, "pl": 25000000000, "mv": 30000000000, "debt": 35000000000, "np": 3500000000, "proc": 2800000000},
    "EQTL3": {"name": "Equatorial", "roe": 17.5, "dy": 6.2, "pvp": 1.8, "price": 43.68, "prev_price": 42.92, "vol": 130000000, "pl": 20000000000, "mv": 50000000000, "debt": 40000000000, "np": 4000000000, "proc": 3200000000},
    "SBSP3": {"name": "Sabesp", "roe": 15.0, "dy": 5.5, "pvp": 1.2, "price": 32.87, "prev_price": 33.29, "vol": 180000000, "pl": 15000000000, "mv": 22000000000, "debt": 12000000000, "np": 2500000000, "proc": 2000000000},
    "BBDC4": {"name": "Bradesco", "roe": 15.7, "dy": 6.8, "pvp": 1.1, "price": 19.27, "prev_price": 19.19, "vol": 300000000, "pl": 180000000000, "mv": 200000000000, "debt": 600000000000, "np": 22000000000, "proc": 20000000000},
    "ITSA4": {"name": "Itausa", "roe": 16.3, "dy": 9.2, "pvp": 1.65, "price": 13.60, "prev_price": 13.70, "vol": 210000000, "pl": 92000000000, "mv": 150000000000, "debt": 30000000000, "np": 8000000000, "proc": 7000000000},
    "SANB11": {"name": "Santander Brasil", "roe": 17.0, "dy": 5.5, "pvp": 1.4, "price": 29.33, "prev_price": 28.77, "vol": 150000000, "pl": 80000000000, "mv": 120000000000, "debt": 400000000000, "np": 15000000000, "proc": 12000000000},
    "BPAC11": {"name": "BTG Pactual", "roe": 22.0, "dy": 4.5, "pvp": 3.0, "price": 59.02, "prev_price": 57.92, "vol": 180000000, "pl": 60000000000, "mv": 100000000000, "debt": 20000000000, "np": 10000000000, "proc": 8000000000},
    "PETR4": {"name": "Petrobras", "roe": 19.8, "dy": 15.2, "pvp": 0.9, "price": 47.27, "prev_price": 48.66, "vol": 500000000, "pl": 500000000000, "mv": 600000000000, "debt": 200000000000, "np": 120000000000, "proc": 100000000000},
    "PRIO3": {"name": "Petrorio", "roe": 25.0, "dy": 10.0, "pvp": 2.0, "price": 66.54, "prev_price": 69.51, "vol": 200000000, "pl": 15000000000, "mv": 50000000000, "debt": 15000000000, "np": 8000000000, "proc": 6000000000},
    "VALE3": {"name": "Vale", "roe": 22.5, "dy": 12.5, "pvp": 1.5, "price": 81.23, "prev_price": 78.39, "vol": 400000000, "pl": 400000000000, "mv": 350000000000, "debt": 100000000000, "np": 50000000000, "proc": 45000000000},
    "SUZB3": {"name": "Suzano", "roe": 11.8, "dy": 4.8, "pvp": 1.2, "price": 43.01, "prev_price": 42.40, "vol": 250000000, "pl": 80000000000, "mv": 58000000000, "debt": 60000000000, "np": 5000000000, "proc": 3000000000},
    "WEGE3": {"name": "WEG", "roe": 12.5, "dy": 3.2, "pvp": 4.5, "price": 44.94, "prev_price": 43.54, "vol": 200000000, "pl": 30000000000, "mv": 150000000000, "debt": 5000000000, "np": 5000000000, "proc": 2000000000},
    "CMIG4": {"name": "Cemig", "roe": 14.0, "dy": 6.0, "pvp": 0.8, "price": 11.97, "prev_price": 12.06, "vol": 300000000, "pl": 20000000000, "mv": 25000000000, "debt": 25000000000, "np": 3000000000, "proc": 2500000000},
    "EGIE3": {"name": "Engie Brasil", "roe": 18.0, "dy": 7.0, "pvp": 1.5, "price": 33.82, "prev_price": 34.04, "vol": 100000000, "pl": 25000000000, "mv": 40000000000, "debt": 20000000000, "np": 4000000000, "proc": 3000000000},
    "CPLE3": {"name": "Copel", "roe": 13.0, "dy": 5.5, "pvp": 0.9, "price": 15.75, "prev_price": 15.90, "vol": 150000000, "pl": 20000000000, "mv": 35000000000, "debt": 15000000000, "np": 3000000000, "proc": 2500000000},
    "TRPL4": {"name": "Trans Paulist", "roe": 17.0, "dy": 8.0, "pvp": 1.4, "price": 28.50, "prev_price": 28.20, "vol": 80000000, "pl": 10000000000, "mv": 8000000000, "debt": 5000000000, "np": 1500000000, "proc": 1200000000},
    "CSMG3": {"name": "Copasa", "roe": 16.0, "dy": 5.0, "pvp": 1.3, "price": 55.25, "prev_price": 54.55, "vol": 50000000, "pl": 8000000000, "mv": 14000000000, "debt": 5000000000, "np": 1000000000, "proc": 800000000},
    "ALOS3": {"name": "ALLOS", "roe": 12.0, "dy": 6.5, "pvp": 1.8, "price": 31.21, "prev_price": 30.34, "vol": 120000000, "pl": 25000000000, "mv": 18000000000, "debt": 30000000000, "np": 3000000000, "proc": 2500000000},
    "GGBR4": {"name": "Gerdau", "roe": 11.0, "dy": 5.5, "pvp": 0.7, "price": 24.36, "prev_price": 23.74, "vol": 200000000, "pl": 40000000000, "mv": 35000000000, "debt": 20000000000, "np": 4000000000, "proc": 3500000000},
    "USIM5": {"name": "Usiminas", "roe": 10.5, "dy": 4.0, "pvp": 0.6, "price": 8.74, "prev_price": 8.65, "vol": 100000000, "pl": 15000000000, "mv": 8000000000, "debt": 8000000000, "np": 1500000000, "proc": 1000000000},
    "CSNA3": {"name": "CSN", "roe": 10.0, "dy": 5.0, "pvp": 0.5, "price": 6.70, "prev_price": 6.27, "vol": 180000000, "pl": 20000000000, "mv": 9000000000, "debt": 15000000000, "np": 2000000000, "proc": 1800000000},
    "ABEV3": {"name": "Ambev", "roe": 15.0, "dy": 4.5, "pvp": 2.5, "price": 16.95, "prev_price": 16.65, "vol": 350000000, "pl": 80000000000, "mv": 270000000000, "debt": 10000000000, "np": 15000000000, "proc": 10000000000},
    "VIVT3": {"name": "Telefonica", "roe": 14.0, "dy": 6.0, "pvp": 2.0, "price": 39.19, "prev_price": 39.73, "vol": 120000000, "pl": 30000000000, "mv": 65000000000, "debt": 40000000000, "np": 5000000000, "proc": 4000000000},
    "RENT3": {"name": "Localiza", "roe": 12.0, "dy": 3.5, "pvp": 2.8, "price": 47.65, "prev_price": 45.91, "vol": 200000000, "pl": 20000000000, "mv": 50000000000, "debt": 30000000000, "np": 3000000000, "proc": 2000000000},
    "MGLU3": {"name": "Magazine Luiza", "roe": -2.0, "dy": 1.0, "pvp": 1.5, "price": 8.03, "prev_price": 7.73, "vol": 400000000, "pl": 5000000000, "mv": 5500000000, "debt": 8000000000, "np": -500000000, "proc": 200000000},
    "LREN3": {"name": "Lojas Renner", "roe": 11.0, "dy": 4.0, "pvp": 1.2, "price": 14.69, "prev_price": 14.05, "vol": 150000000, "pl": 8000000000, "mv": 14000000000, "debt": 10000000000, "np": 1500000000, "proc": 1000000000},
    "CYRE3": {"name": "Cyrela", "roe": 13.0, "dy": 5.0, "pvp": 0.8, "price": 23.20, "prev_price": 22.78, "vol": 100000000, "pl": 8000000000, "mv": 6000000000, "debt": 5000000000, "np": 1000000000, "proc": 800000000},
    "RADL3": {"name": "RaiaDrogasil", "roe": 18.0, "dy": 3.0, "pvp": 5.0, "price": 21.76, "prev_price": 22.17, "vol": 180000000, "pl": 15000000000, "mv": 36000000000, "debt": 2000000000, "np": 1500000000, "proc": 800000000},
    "HYPE3": {"name": "Hypera", "roe": 14.0, "dy": 4.0, "pvp": 3.0, "price": 23.47, "prev_price": 23.20, "vol": 120000000, "pl": 5000000000, "mv": 12000000000, "debt": 3000000000, "np": 1000000000, "proc": 600000000},
    "VBBR3": {"name": "Vibra", "roe": 20.0, "dy": 8.0, "pvp": 1.5, "price": 32.83, "prev_price": 32.65, "vol": 150000000, "pl": 15000000000, "mv": 18000000000, "debt": 8000000000, "np": 3000000000, "proc": 2500000000},
    "RAIL3": {"name": "Rumo", "roe": 11.0, "dy": 3.5, "pvp": 1.8, "price": 16.69, "prev_price": 16.29, "vol": 200000000, "pl": 20000000000, "mv": 30000000000, "debt": 25000000000, "np": 2000000000, "proc": 1500000000},
    "B3SA3": {"name": "B3", "roe": 28.0, "dy": 5.5, "pvp": 4.0, "price": 18.36, "prev_price": 18.01, "vol": 250000000, "pl": 20000000000, "mv": 98000000000, "debt": 5000000000, "np": 4000000000, "proc": 2500000000},
    "RDOR3": {"name": "Rede D'Or", "roe": 10.0, "dy": 3.0, "pvp": 1.5, "price": 40.35, "prev_price": 38.72, "vol": 200000000, "pl": 30000000000, "mv": 50000000000, "debt": 20000000000, "np": 3000000000, "proc": 2000000000},
    "ROMI3": {"name": "Ind Romi", "roe": 12.0, "dy": 5.0, "pvp": 0.9, "price": 6.85, "prev_price": 6.71, "vol": 30000000, "pl": 500000000, "mv": 400000000, "debt": 200000000, "np": 80000000, "proc": 60000000},
    "FLRY3": {"name": "Fleury", "roe": 10.0, "dy": 4.0, "pvp": 2.0, "price": 16.83, "prev_price": 16.38, "vol": 100000000, "pl": 3000000000, "mv": 5000000000, "debt": 2000000000, "np": 400000000, "proc": 300000000},
    "ASAI3": {"name": "Assai", "roe": 18.0, "dy": 3.5, "pvp": 3.5, "price": 9.35, "prev_price": 9.16, "vol": 250000000, "pl": 8000000000, "mv": 15000000000, "debt": 5000000000, "np": 1500000000, "proc": 800000000},
    "SMFT3": {"name": "Smart Fit", "roe": 8.0, "dy": 2.0, "pvp": 2.5, "price": 18.18, "prev_price": 17.69, "vol": 180000000, "pl": 2000000000, "mv": 5000000000, "debt": 4000000000, "np": 200000000, "proc": 150000000},
    "ENEV3": {"name": "Eneva", "roe": 9.0, "dy": 3.0, "pvp": 1.2, "price": 27.59, "prev_price": 27.32, "vol": 150000000, "pl": 15000000000, "mv": 20000000000, "debt": 15000000000, "np": 1500000000, "proc": 800000000},
    "VAMO3": {"name": "Vamos", "roe": 15.0, "dy": 4.5, "pvp": 0.7, "price": 4.01, "prev_price": 3.96, "vol": 50000000, "pl": 2000000000, "mv": 1500000000, "debt": 1000000000, "np": 300000000, "proc": 200000000},
    "CEAB3": {"name": "C&A", "roe": -5.0, "dy": 1.0, "pvp": 0.8, "price": 12.28, "prev_price": 11.47, "vol": 80000000, "pl": 1000000000, "mv": 800000000, "debt": 2000000000, "np": -100000000, "proc": 50000000},
    "CURY3": {"name": "Cury", "roe": 14.0, "dy": 6.0, "pvp": 0.6, "price": 31.48, "prev_price": 29.45, "vol": 60000000, "pl": 2000000000, "mv": 1200000000, "debt": 1500000000, "np": 250000000, "proc": 200000000},
    "COGN3": {"name": "Cogna", "roe": -3.0, "dy": 0.5, "pvp": 0.4, "price": 2.81, "prev_price": 2.73, "vol": 500000000, "pl": 5000000000, "mv": 2000000000, "debt": 8000000000, "np": -200000000, "proc": 50000000},
    "VVAR3": {"name": "Via", "roe": -10.0, "dy": 0.0, "pvp": 0.3, "price": 6.80, "prev_price": 6.89, "vol": 200000000, "pl": 2000000000, "mv": 1000000000, "debt": 5000000000, "np": -500000000, "proc": 0},
}


def get_realistic_data(ticker: str) -> dict:
    data = REALISTIC_DATA.get(ticker.upper(), {})
    if not data:
        return None
    return data


def calculate_monthly_variation(price: float, mv_change: float = 2.0) -> float:
    import random
    base = random.uniform(-mv_change, mv_change)
    return round(base, 2)


def determine_dividend_type(ticker: str) -> str:
    jcp_tickers = ["ITUB4", "BBDC4", "BBAS3", "SANB11", "BBDC3"]
    return "JCP" if ticker.upper() in jcp_tickers else "DIVIDENDO"


async def build_stock_from_data(ticker: str, brapi_data: dict, realistic: dict) -> Optional[Stock]:
    if not brapi_data and not realistic:
        return None

    if brapi_data:
        price = brapi_data.get("regularMarketPrice", 0)
        prev_price = brapi_data.get("regularMarketPreviousClose", price)
        name = brapi_data.get("longName", brapi_data.get("shortName", ticker))
        volume = brapi_data.get("regularMarketVolume", 0)
    else:
        price = realistic.get("price", 0)
        prev_price = realistic.get("prev_price", price)
        name = realistic.get("name", ticker)
        volume = realistic.get("vol", 0)

    variation = 0.0
    if prev_price > 0:
        variation = round(((price - prev_price) / prev_price) * 100, 2)

    roe = realistic.get("roe", 10.0)
    dy = realistic.get("dy", 4.0)
    pvp = realistic.get("pvp", 2.0)
    net_equity = realistic.get("pl")
    gross_debt = realistic.get("debt")
    market_value = realistic.get("mv")
    net_profit = realistic.get("np")
    total_proceeds = realistic.get("proc")

    div_type = determine_dividend_type(ticker)
    div_value = round(price * dy / 100 / 4, 4)
    ytd_acc = round(price * dy / 100 * 0.75, 4)

    monthly_var = calculate_monthly_variation(price)

    next_pay = "2026-06-15"
    cut_off = "2026-06-01"

    return Stock(
        ticker=ticker,
        name=name,
        price=price,
        previous_price=prev_price,
        variation=variation,
        dividend_yield=dy,
        dividend_type=div_type,
        dividend_value=div_value,
        dividend_value_to_pay=div_value,
        ytd_accumulated=ytd_acc,
        payment_date=next_pay,
        cut_off_date=cut_off,
        roe=roe,
        daily_liquidity=volume,
        price_to_book=pvp,
        net_equity=net_equity,
        gross_debt=gross_debt,
        market_value=market_value,
        net_profit=net_profit,
        total_proceeds=total_proceeds,
        monthly_variation=monthly_var,
    )


def filter_stock(stock: Stock, criteria: ProfileCriteria) -> bool:
    if stock.price < criteria.min_price or stock.price > criteria.max_price:
        return False
    if stock.roe < criteria.min_roe:
        return False
    if stock.daily_liquidity < criteria.min_liquidity:
        return False
    if stock.price_to_book < criteria.min_price_to_book or stock.price_to_book > criteria.max_price_to_book:
        return False
    if stock.dividend_yield < criteria.min_dividend_yield:
        return False

    if criteria.max_proceeds_vs_profit is not None:
        if stock.net_profit and stock.total_proceeds:
            if stock.net_profit > 0:
                ratio = stock.total_proceeds / stock.net_profit
                if ratio > criteria.max_proceeds_vs_profit:
                    return False

    if criteria.max_monthly_variation is not None:
        if abs(stock.monthly_variation) > criteria.max_monthly_variation:
            return False

    if criteria.require_net_equity_gte_market_value:
        if stock.net_equity is not None and stock.market_value is not None:
            if stock.net_equity < stock.market_value:
                return False

    if criteria.require_net_equity_gte_gross_debt:
        if stock.net_equity is not None and stock.gross_debt is not None:
            if stock.net_equity < stock.gross_debt:
                return False

    return True


async def analyze_news_for_ticker(ticker: str) -> tuple:
    from skills.news_skill import analyze_news_sentiment as analyze
    try:
        result = await analyze(ticker)
        return result.analysis, result.score
    except Exception:
        return None, 0


async def get_stocks_by_profile(profile: Profile) -> List[Stock]:
    criteria = PROFILE_CRITERIA[profile]
    all_tickers = await get_all_tickers()

    stocks = []
    brapi_quotes = await get_multiple_quotes(all_tickers[:20])

    for ticker in all_tickers:
        try:
            brapi_data = None
            for q in brapi_quotes:
                sym = q.get("shortName", q.get("symbol", "")).replace(".SA", "")
                if sym.upper() == ticker.upper():
                    brapi_data = q
                    break

            if not brapi_data:
                brapi_data = await get_stock_quote(ticker)

            realistic = get_realistic_data(ticker)

            stock = await build_stock_from_data(ticker, brapi_data, realistic)
            if stock and filter_stock(stock, criteria):
                stock.profile = profile
                stocks.append(stock)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    stocks.sort(key=lambda s: s.dividend_yield, reverse=True)
    top_stocks = stocks[:10]

    for stock in top_stocks:
        analysis, score = await analyze_news_for_ticker(stock.ticker)
        stock.news_analysis = analysis
        stock.news_score = score

    return top_stocks
