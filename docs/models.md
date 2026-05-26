# Models — Schemas Pydantic

Arquivo: `models/schemas.py`

Todos os schemas usam `pydantic.BaseModel` para validação e serialização.

## Enums

### `Profile`

| Valor | Descrição |
|-------|-----------|
| `iniciante` | Perfil conservador, foco em dividendos |
| `moderado` | Equilíbrio entre risco e retorno |
| `agressivo` | Maior potencial de crescimento |

### `DividendType`

| Valor | Descrição |
|-------|-----------|
| `JCP` | Juros sobre Capital Próprio |
| `DIVIDENDO` | Dividendo convencional |

### `NewsAnalysis`

| Valor | Descrição |
|-------|-----------|
| `boa` | Sentimento positivo (positive_count > negative_count) |
| `ruim` | Sentimento negativo (negative_count > positive_count) |

## Schemas

### `Stock`

Modelo principal de recomendação de ações.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `ticker` | `str` | Código do ativo (ex: ITUB4) |
| `name` | `str` | Nome da empresa |
| `price` | `float` | Preço atual |
| `previous_price` | `float` | Fechamento anterior |
| `variation` | `float` | Variação percentual |
| `dividend_yield` | `float` | Dividend Yield 12 meses (%) |
| `dividend_type` | `DividendType` | JCP ou DIVIDENDO |
| `dividend_value` | `float` | Valor do dividendo por ação |
| `dividend_value_to_pay` | `float` | Valor a pagar |
| `ytd_accumulated` | `float` | Total acumulado no ano |
| `payment_date` | `str` | Data do próximo pagamento |
| `cut_off_date` | `str` | Data ex-dividendo |
| `roe` | `float` | Retorno sobre Patrimônio Líquido (%) |
| `daily_liquidity` | `float` | Liquidez diária média (R$) |
| `price_to_book` | `float` | Preço/Valor Patrimonial (P/VP) |
| `net_equity` | `Optional[float]` | Patrimônio Líquido |
| `gross_debt` | `Optional[float]` | Dívida Bruta |
| `market_value` | `Optional[float]` | Valor de Mercado |
| `net_profit` | `Optional[float]` | Lucro Líquido |
| `total_proceeds` | `Optional[float]` | Total de Proventos |
| `monthly_variation` | `float` | Variação mensal (%) |
| `news_analysis` | `Optional[NewsAnalysis]` | Análise de sentimento |
| `news_score` | `int` | Score de sentimento (positive - negative) |
| `profile` | `Optional[Profile]` | Perfil associado |

### `NewsItem`

Artigo de notícia financeira.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `title` | `str` | Título da notícia |
| `source` | `str` | Fonte (InfoMoney, Exame, etc.) |
| `url` | `str` | URL do artigo |
| `published_at` | `str` | Data de publicação |
| `view_count` | `Optional[int]` | Visualizações |
| `ticker` | `Optional[str]` | Ativo relacionado |
| `sentiment` | `Optional[str]` | Sentimento (positivo/negativo) |

### `NewsAnalysisResult`

Resultado consolidado da análise de sentimento.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `ticker` | `str` | Ativo analisado |
| `analysis` | `Optional[NewsAnalysis]` | Classificação (boa/ruim) |
| `score` | `int` | Score líquido de sentimento |
| `positive_count` | `int` | Qtd de notícias positivas |
| `negative_count` | `int` | Qtd de notícias negativas |
| `articles` | `List[NewsItem]` | Artigos analisados |

### `DividendCalendar`

Calendário de dividendos de um ativo.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `ticker` | `str` | Ativo |
| `next_payment_date` | `Optional[str]` | Próximo pagamento |
| `cut_off_date` | `Optional[str]` | Data de corte |
| `type` | `Optional[DividendType]` | Tipo do dividendo |
| `next_amount` | `Optional[float]` | Valor do próximo |
| `ytd_total` | `float` | Total recebido no ano |
| `history` | `List[DividendItem]` | Histórico de pagamentos |

### `PortfolioItem`

Item individual da carteira de investimentos.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `ticker` | `str` | Ativo |
| `name` | `str` | Nome da empresa |
| `quantity` | `float` | Quantidade de ações |
| `avg_price` | `float` | Preço médio de compra |
| `total_invested` | `float` | Total investido |
| `current_price` | `float` | Cotação atual |
| `variation` | `float` | Variação (%) |
| `current_value` | `float` | Valor atual total |
| `result` | `float` | Resultado (R$) |
| `result_percent` | `float` | Resultado (%) |

### `PortfolioDividend`

Dividendo recebido na carteira.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `ticker` | `str` | Ativo |
| `value` | `float` | Valor por ação |
| `date_com` | `str` | Data com |
| `date_pay` | `str` | Data de pagamento |
| `type` | `str` | Tipo (JCP/DIVIDENDO) |
| `dy` | `float` | Dividend Yield (%) |

### `ProfileCriteria`

Critérios de filtro para cada perfil de investidor.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | `Profile` | Perfil alvo |
| `min_price` | `float` | Preço mínimo |
| `max_price` | `float` | Preço máximo |
| `min_roe` | `float` | ROE mínimo (%) |
| `min_liquidity` | `float` | Liquidez mínima (R$) |
| `min_price_to_book` | `float` | P/VP mínimo |
| `max_price_to_book` | `float` | P/VP máximo |
| `min_dividend_yield` | `float` | DY mínimo (%) |
| `max_proceeds_vs_profit` | `Optional[float]` | Máx proventos/lucro |
| `max_monthly_variation` | `Optional[float]` | Máx variação mensal |
| `require_net_equity_gte_market_value` | `bool` | PL >= Valor Mercado |
| `require_net_equity_gte_gross_debt` | `bool` | PL >= Dívida Bruta |
