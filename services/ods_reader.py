import os
from typing import List, Dict

ODS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lista_acao.ods")


def parse_ods_dataframe(df) -> List[Dict]:
    if df.empty:
        return []

    df["total_cost"] = df["VL Compra"] * df["QTDE"]

    grouped = df.groupby("Ativo", as_index=False).agg(
        quantity=("QTDE", "sum"),
        total_cost=("total_cost", "sum"),
    )
    grouped["avg_price"] = (grouped["total_cost"] / grouped["quantity"]).round(2)

    portfolio = []
    for _, row in grouped.iterrows():
        portfolio.append({
            "ticker": row["Ativo"].strip().upper(),
            "name": row["Ativo"].strip().upper(),
            "quantity": round(row["quantity"], 4),
            "avg_price": row["avg_price"],
        })

    portfolio.sort(key=lambda x: x["quantity"] * x["avg_price"], reverse=True)
    return portfolio


def read_ods(path: str) -> List[Dict]:
    try:
        import pandas as pd
        df = pd.read_excel(path, engine="odf")
        return parse_ods_dataframe(df)
    except ImportError:
        print("Warning: odfpy not installed. Install with: pip install odfpy")
        return []
    except Exception as e:
        print(f"Warning: failed to read ODS file {path}: {e}")
        return []


def get_portfolio_from_ods() -> List[Dict]:
    if not os.path.exists(ODS_PATH):
        return []
    return read_ods(ODS_PATH)
