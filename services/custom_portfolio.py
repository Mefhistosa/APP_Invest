import json
import os
from typing import List, Dict

CUSTOM_STOCKS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom_stocks.json")


def _load() -> List[Dict]:
    if not os.path.exists(CUSTOM_STOCKS_FILE):
        return []
    try:
        with open(CUSTOM_STOCKS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def _save(stocks: List[Dict]):
    with open(CUSTOM_STOCKS_FILE, "w") as f:
        json.dump(stocks, f, indent=2)


def add_stock(ticker: str, quantity: float, avg_price: float) -> List[Dict]:
    stocks = _load()
    ticker = ticker.upper()
    for s in stocks:
        if s["ticker"] == ticker:
            old_qty = s["quantity"]
            old_price = s["avg_price"]
            new_qty = old_qty + quantity
            new_avg = (old_qty * old_price + quantity * avg_price) / new_qty
            s["quantity"] = new_qty
            s["avg_price"] = round(new_avg, 2)
            _save(stocks)
            return stocks
    stocks.append({
        "ticker": ticker,
        "name": ticker,
        "quantity": quantity,
        "avg_price": avg_price,
    })
    _save(stocks)
    return stocks


def sell_stock(ticker: str, quantity_to_sell: float,
               original_quantity: float = 0, original_avg_price: float = 0) -> Dict:
    stocks = _load()
    ticker = ticker.upper()
    found = False
    for s in stocks:
        if s["ticker"] == ticker:
            s["quantity"] -= quantity_to_sell
            if s["quantity"] <= 0:
                stocks.remove(s)
            found = True
            break
    if not found:
        remaining = original_quantity - quantity_to_sell
        if remaining > 0:
            stocks.append({
                "ticker": ticker,
                "name": ticker,
                "quantity": remaining,
                "avg_price": original_avg_price,
            })
    _save(stocks)
    return {"ticker": ticker, "quantity_sold": quantity_to_sell}


def get_all() -> List[Dict]:
    return _load()
