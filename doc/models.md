# Models — Schemas Pydantic (deprecated)

> **A documentacao foi movida para [`docs/models.md`](/home/dsa/Documentos/app_investidor/docs/models.md).**

Arquivo: `models/schemas.py`

Todos os schemas usam `pydantic.BaseModel` para validacao e serializacao.

---

## Enums

### `Profile`

Define os perfis de investidor disponiveis.

| Valor | Descricao |
|-------|-----------|
| `iniciante` | Perfil conservador, foco em dividendos |
| `moderado` | Equilibrio entre risco e retorno |
| `agressivo` | Maior potencial de crescimento |

### `DividendType`

Define os tipos de proventos.

| Valor | Descricao |
|-------|-----------|
| `JCP` | Juros sobre Capital Proprio |
| `DIVIDENDO` | Dividendo convencional |

### `NewsAnalysis`

Classificacao de sentimento de noticias.

| Valor | Descricao |
|-------|-----------|
| `boa` | Sentimento positivo |
| `ruim` | Sentimento negativo |

---

## Schemas

### `Stock`

Modelo principal — representa uma acao recomendada.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `ticker` | `str` | Codigo do ativo (ex: ITUB4) |
| `name` | `str` | Nome da empresa |
| `price` | `float` | Preco atual |
| `previous_price` | `float` | Fechamento anterior |
| `variation` | `float` | Variacao percentual |
| `dividend_yield` | `float` | Dividend Yield 12 meses (%) |
| `dividend_type` | `DividendType` | JCP ou DIVIDENDO |
| `dividend_value` | `float` | Valor do dividendo por acao |
| `dividend_value_to_pay` | `float` | Valor a pagar |
| `ytd_accumulated` | `float` | Total acumulado no ano |
| `payment_date` | `str` | Data do proximo pagamento |
| `cut_off_date` | `str` | Data ex-dividendo |
| `roe` | `float` | Retorno sobre PL (%) |
| `daily_liquidity` | `float` | Liquidez diaria media (R$) |
| `price_to_book` | `float` | Preco/Valor Patrimonial (P/VP) |
| `net_equity` | `Optional[float]` | Patrimonio Liquido |
| `gross_debt` | `Optional[float]` | Divida Bruta |
| `market_value` | `Optional[float]` | Valor de Mercado |
| `net_profit` | `Optional[float]` | Lucro Liquido |
| `total_proceeds` | `Optional[float]` | Total de Proventos |
| `monthly_variation` | `float` | Variacao mensal (%) |
| `news_analysis` | `Optional[NewsAnalysis]` | Analise de sentimento |
| `news_score` | `int` | Score (positive - negative) |
| `profile` | `Optional[Profile]` | Perfil associado |

### `NewsItem`

Artigo de noticia financeira.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `title` | `str` | Titulo da noticia |
| `source` | `str` | Fonte |
| `url` | `str` | URL do artigo |
| `published_at` | `str` | Data de publicacao |
| `view_count` | `Optional[int]` | Visualizacoes |
| `ticker` | `Optional[str]` | Ativo relacionado |
| `sentiment` | `Optional[str]` | Sentimento (positivo/negativo) |

### `NewsAnalysisResult`

Resultado consolidado da analise de sentimento.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `ticker` | `str` | Ativo analisado |
| `analysis` | `Optional[NewsAnalysis]` | Classificacao (boa/ruim) |
| `score` | `int` | Score liquido |
| `positive_count` | `int` | Qtd de noticias positivas |
| `negative_count` | `int` | Qtd de noticias negativas |
| `articles` | `List[NewsItem]` | Artigos analisados |

### `DividendCalendar`

Calendario de dividendos de um ativo.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `ticker` | `str` | Ativo |
| `next_payment_date` | `Optional[str]` | Proximo pagamento |
| `cut_off_date` | `Optional[str]` | Data de corte |
| `type` | `Optional[DividendType]` | Tipo do dividendo |
| `next_amount` | `Optional[float]` | Valor do proximo |
| `ytd_total` | `float` | Total recebido no ano |
| `history` | `List[DividendItem]` | Historico de pagamentos |

### `DividendItem`

Item individual do historico de dividendos.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `ticker` | `str` | Ativo |
| `amount` | `float` | Valor por acao |
| `adj_amount` | `Optional[float]` | Valor ajustado |
| `type` | `DividendType` | JCP ou DIVIDENDO |
| `ex_date` | `Optional[str]` | Data ex |
| `payable_date` | `Optional[str]` | Data pagamento |
| `record_date` | `Optional[str]` | Data record |

### `PriceHistoryItem`

Ponto de historico OHLCV.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `date` | `str` | Data |
| `open` | `float` | Abertura |
| `close` | `float` | Fechamento |
| `high` | `float` | Maxima |
| `low` | `float` | Minima |
| `volume` | `Optional[int]` | Volume |

### `MacroData`

Indicadores macroeconomicos.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `selic` | `Optional[float]` | Taxa SELIC (%) |
| `cdi` | `Optional[float]` | Taxa CDI (%) |
| `date` | `str` | Data de referencia |

### `PortfolioItem`

Item da carteira de investimentos.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `ticker` | `str` | Ativo |
| `name` | `str` | Nome da empresa |
| `quantity` | `float` | Quantidade |
| `avg_price` | `float` | Preco medio de compra |
| `total_invested` | `float` | Total investido |
| `current_price` | `float` | Cotacao atual |
| `variation` | `float` | Variacao (%) |
| `current_value` | `float` | Valor atual total |
| `result` | `float` | Resultado (R$) |
| `result_percent` | `float` | Resultado (%) |

### `PortfolioDividend`

Dividendo recebido na carteira.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `ticker` | `str` | Ativo |
| `value` | `float` | Valor |
| `date_com` | `str` | Data com |
| `date_pay` | `str` | Data pagamento |
| `type` | `str` | Tipo (JCP/DIVIDENDO) |
| `dy` | `float` | Dividend Yield (%) |

### `PortfolioResponse`

Resposta consolidada da carteira.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `items` | `List[PortfolioItem]` | Itens da carteira |
| `total_invested` | `float` | Total investido |
| `total_current` | `float` | Valor atual total |
| `total_result` | `float` | Resultado total (R$) |
| `total_result_percent` | `float` | Rentabilidade (%) |

### `PortfolioDividendResponse`

Resposta de dividendos da carteira.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `dividends` | `List[PortfolioDividend]` | Lista de dividendos |

### `ProfileCriteria`

Criterios de filtro para cada perfil de investidor.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `name` | `Profile` | Perfil alvo |
| `min_price` | `float` | Preco minimo |
| `max_price` | `float` | Preco maximo |
| `min_roe` | `float` | ROE minimo (%) |
| `min_liquidity` | `float` | Liquidez minima (R$) |
| `min_price_to_book` | `float` | P/VP minimo |
| `max_price_to_book` | `float` | P/VP maximo |
| `min_dividend_yield` | `float` | DY minimo (%) |
| `max_proceeds_vs_profit` | `Optional[float]` | Max proventos/lucro |
| `max_monthly_variation` | `Optional[float]` | Max variacao mensal |
| `require_net_equity_gte_market_value` | `bool` | Exige PL >= Valor Mercado |
| `require_net_equity_gte_gross_debt` | `bool` | Exige PL >= Divida Bruta |
