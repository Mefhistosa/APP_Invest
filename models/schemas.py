from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class DividendType(str, Enum):
    JCP = "JCP"
    DIVIDENDO = "DIVIDENDO"


class NewsAnalysis(str, Enum):
    BOA = "boa"
    RUIM = "ruim"


class Profile(str, Enum):
    INICIANTE = "iniciante"
    MODERADO = "moderado"
    AGRESSIVO = "agressivo"


class Stock(BaseModel):
    ticker: str
    name: str
    price: float
    previous_price: float
    variation: float
    dividend_yield: float
    dividend_type: DividendType
    dividend_value: float
    dividend_value_to_pay: float
    ytd_accumulated: float
    payment_date: str
    cut_off_date: str
    roe: float
    daily_liquidity: float
    price_to_book: float
    net_equity: Optional[float] = None
    gross_debt: Optional[float] = None
    market_value: Optional[float] = None
    net_profit: Optional[float] = None
    total_proceeds: Optional[float] = None
    monthly_variation: float = 0.0
    news_analysis: Optional[NewsAnalysis] = None
    news_score: int = 0
    profile: Optional[Profile] = None


class NewsItem(BaseModel):
    title: str
    source: str
    url: str
    published_at: str
    view_count: Optional[int] = None
    ticker: Optional[str] = None
    sentiment: Optional[str] = None


class NewsAnalysisResult(BaseModel):
    ticker: str
    analysis: Optional[NewsAnalysis] = None
    score: int = 0
    positive_count: int = 0
    negative_count: int = 0
    articles: List[NewsItem] = []


class DividendItem(BaseModel):
    ticker: str
    amount: float
    adj_amount: Optional[float] = None
    type: DividendType
    ex_date: Optional[str] = None
    payable_date: Optional[str] = None
    record_date: Optional[str] = None


class DividendCalendar(BaseModel):
    ticker: str
    next_payment_date: Optional[str] = None
    cut_off_date: Optional[str] = None
    type: Optional[DividendType] = None
    next_amount: Optional[float] = None
    ytd_total: float = 0.0
    history: List[DividendItem] = []


class PriceHistoryItem(BaseModel):
    date: str
    open: float
    close: float
    high: float
    low: float
    volume: Optional[int] = None


class MacroData(BaseModel):
    selic: Optional[float] = None
    cdi: Optional[float] = None
    date: str


class PortfolioItem(BaseModel):
    ticker: str
    name: str
    quantity: float
    avg_price: float
    total_invested: float
    current_price: float
    variation: float
    current_value: float
    result: float
    result_percent: float


class PortfolioDividend(BaseModel):
    ticker: str
    value: float
    date_com: str
    date_pay: str
    type: str
    dy: float


class PortfolioResponse(BaseModel):
    items: List[PortfolioItem]
    total_invested: float
    total_current: float
    total_result: float
    total_result_percent: float


class PortfolioDividendResponse(BaseModel):
    dividends: List[PortfolioDividend]


class ProfileCriteria(BaseModel):
    name: Profile
    min_price: float
    max_price: float
    min_roe: float
    min_liquidity: float
    min_price_to_book: float
    max_price_to_book: float
    min_dividend_yield: float
    max_proceeds_vs_profit: Optional[float] = None
    max_monthly_variation: Optional[float] = None
    require_net_equity_gte_market_value: bool = False
    require_net_equity_gte_gross_debt: bool = False
