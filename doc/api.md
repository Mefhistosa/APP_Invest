# API — Documentacao dos Endpoints (deprecated)

> **A documentacao foi movida para [`docs/api.md`](/home/dsa/Documentos/app_investidor/docs/api.md).**

Base URL: `http://localhost:8000/api/v1`

---

## `GET /stocks/{profile}`

Recomenda acoes filtradas pelo perfil do investidor.

**Parametros:**
- `profile` (path, obrigatorio): `iniciante`, `moderado` ou `agressivo`

**Fluxo interno:**
1. Busca tickers disponiveis via Brapi (`get_all_tickers`)
2. Obtem cotacoes em tempo real (Brapi) com fallback para `REALISTIC_DATA`
3. Aplica filtros do perfil: ROE, DY, P/VP, liquidez, variacao mensal
4. Ordena por dividend yield (decrescente) → Top 10
5. Para cada acao, busca noticias e analisa sentimento
6. Retorna as 10 melhores

**Resposta (200):** `List[Stock]`

```json
[
  {
    "ticker": "ITUB4",
    "name": "Itau Unibanco",
    "price": 41.78,
    "previous_price": 42.45,
    "variation": -1.58,
    "dividend_yield": 8.5,
    "dividend_type": "JCP",
    "dividend_value": 0.89,
    "dividend_value_to_pay": 0.89,
    "ytd_accumulated": 2.67,
    "payment_date": "2026-06-15",
    "cut_off_date": "2026-06-01",
    "roe": 18.2,
    "daily_liquidity": 250000000,
    "price_to_book": 2.15,
    "net_equity": 250000000000,
    "gross_debt": 800000000000,
    "market_value": 400000000000,
    "net_profit": 30000000000,
    "total_proceeds": 25000000000,
    "monthly_variation": 1.23,
    "news_analysis": "boa",
    "news_score": 3,
    "profile": "iniciante"
  }
]
```

**Erros:**
- `400` — Perfil invalido (valores aceitos: `iniciante`, `moderado`, `agressivo`)

---

## `GET /news/{ticker}`

Analise de sentimento das noticias recentes de um ativo.

**Parametros:**
- `ticker` (path, obrigatorio): codigo do ativo (ex: ITUB4)

**Fluxo interno:**
1. Busca noticias via Partnr.ai (ate 50 artigos)
2. Se vazio, fallback para Dados de Mercado (ultimos 7 dias)
3. Se ainda vazio, gera noticias mock
4. Seleciona top 5 por view_count
5. Analisa sentimento via DeepSeek (ou keyword fallback)
6. Classifica como `boa` (positive > negative) ou `ruim`

**Resposta (200):** `NewsAnalysisResult`

```json
{
  "ticker": "ITUB4",
  "analysis": "boa",
  "score": 3,
  "positive_count": 4,
  "negative_count": 1,
  "articles": [
    {
      "title": "ITUB4 apresenta resultados solidos no trimestre",
      "source": "InfoMoney",
      "url": "https://example.com/news1",
      "published_at": "2026-05-05",
      "view_count": 15000,
      "ticker": "ITUB4",
      "sentiment": null
    }
  ]
}
```

---

## `GET /dividends/{ticker}`

Calendario de dividendos de um ativo.

**Parametros:**
- `ticker` (path, obrigatorio): codigo do ativo

**Fluxo interno:**
1. Busca codigo CVM da empresa via `CVm_CODE_MAP`
2. Obtem proventos via Dados de Mercado API
3. Se sem dados, gera dados realistas estimados
4. Identifica proximo pagamento e total YTD

**Resposta (200):** `DividendCalendar`

```json
{
  "ticker": "ITUB4",
  "next_payment_date": "2026-06-15",
  "cut_off_date": "2026-06-01",
  "type": "DIVIDENDO",
  "next_amount": 0.22,
  "ytd_total": 0.66,
  "history": [
    {
      "ticker": "ITUB4",
      "amount": 0.50,
      "adj_amount": null,
      "type": "DIVIDENDO",
      "ex_date": "2026-05-15",
      "payable_date": "2026-06-01",
      "record_date": null
    }
  ]
}
```

**Erros:**
- `404` — Empresa nao encontrada para o ticker informado

---

## `GET /macro`

Indicadores macroeconomicos (SELIC e CDI).

**Fluxo interno:**
1. Consulta HG Brasil API
2. Fallback para valores default (SELIC=14.75, CDI=14.75)

**Resposta (200):** `MacroData`

```json
{
  "selic": 14.75,
  "cdi": 14.75,
  "date": "2026-05-05"
}
```

---

## `GET /filters`

Retorna os criterios de filtro de cada perfil de investidor.

**Resposta (200):**

```json
{
  "iniciante": {
    "name": "iniciante",
    "min_price": 2.0,
    "max_price": 50.0,
    "min_roe": 13.0,
    "min_liquidity": 10000000.0,
    "min_price_to_book": 0.2,
    "max_price_to_book": 3.0,
    "min_dividend_yield": 8.0,
    "max_proceeds_vs_profit": 1.0,
    "max_monthly_variation": null,
    "require_net_equity_gte_market_value": true,
    "require_net_equity_gte_gross_debt": false
  }
}
```

---

## `GET /history/{ticker}`

Historico de precos OHLCV.

**Parametros:**
- `ticker` (path, obrigatorio): codigo do ativo
- `days` (query, opcional, default=30): periodo em dias

**Fluxo interno:**
1. Consulta Brapi API para historico
2. Fallback para dados sinteticos realistas (random walk controlado)

**Resposta (200):** `List[PriceHistoryItem]`

```json
[
  {
    "date": "2026-04-05",
    "open": 42.10,
    "close": 42.50,
    "high": 42.80,
    "low": 41.90,
    "volume": 15000000
  }
]
```

---

## `GET /portfolio`

Carteira completa do investidor com valores atualizados.

**Fluxo interno:**
1. Tenta Google Sheets (service account → OAuth2 → CSV export)
2. Fallback para carteira mock (`MOCK_PORTFOLIO` com 15 ativos)
3. Para cada ativo, busca cotacao atual via Brapi
4. Fallback de cotacao via `REALISTIC_PRICES`
5. Calcula valor investido, valor atual, resultado (R$ e %)

**Resposta (200):** `PortfolioResponse`

```json
{
  "items": [
    {
      "ticker": "ITUB4",
      "name": "Itau Unibanco",
      "quantity": 100,
      "avg_price": 35.50,
      "total_invested": 3550.00,
      "current_price": 41.78,
      "variation": 17.69,
      "current_value": 4178.00,
      "result": 628.00,
      "result_percent": 17.69
    }
  ],
  "total_invested": 15000.00,
  "total_current": 17500.00,
  "total_result": 2500.00,
  "total_result_percent": 16.67
}
```

---

## `GET /portfolio/dividends`

Dividendos da carteira do investidor.

**Fluxo interno:**
1. Obtem carteira do Google Sheets
2. Busca dividendos mock (`MOCK_DIVIDENDS`)
3. Enriquece com Dividend Yield do `REALISTIC_DATA`
4. Ordena por data de pagamento (decrescente)

**Resposta (200):** `PortfolioDividendResponse`

```json
{
  "dividends": [
    {
      "ticker": "PETR4",
      "value": 1.85,
      "date_com": "2026-03-20",
      "date_pay": "2026-04-25",
      "type": "DIVIDENDO",
      "dy": 15.2
    }
  ]
}
```

---

## `GET /portfolio/chart/{ticker}`

Dados para grafico de linha.

**Parametros:**
- `ticker` (path, obrigatorio)
- `days` (query, opcional, default=30, min=1, max=365)

**Fluxo interno:**
1. Busca historico via Brapi
2. Fallback para dados sinteticos (random walk controlado)

**Resposta (200):** `List[dict]`

```json
[
  {
    "date": "2026-04-05",
    "open": 42.10,
    "high": 42.80,
    "low": 41.90,
    "close": 42.50,
    "volume": 15000000
  }
]
```

---

## `GET /health`

Health check. Sem autenticacao.

```json
{
  "status": "ok",
  "version": "1.1.0"
}
```

---

## `GET /`

Frontend SPA (`index.html`).

---

## Resumo dos Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | `/api/v1/stocks/{profile}` | Recomendacoes por perfil |
| GET | `/api/v1/news/{ticker}` | Analise de sentimento |
| GET | `/api/v1/dividends/{ticker}` | Calendario de dividendos |
| GET | `/api/v1/macro` | Dados macroeconomicos |
| GET | `/api/v1/history/{ticker}` | Historico de precos |
| GET | `/api/v1/portfolio` | Carteira do investidor |
| GET | `/api/v1/portfolio/dividends` | Dividendos da carteira |
| GET | `/api/v1/portfolio/chart/{ticker}` | Dados para grafico |
| GET | `/api/v1/filters` | Criterios dos perfis |
| GET | `/api/v1/health` | Health check |
| GET | `/` | Frontend SPA |
