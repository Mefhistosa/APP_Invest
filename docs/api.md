# API — Documentação dos Endpoints

Base URL: `http://localhost:8000/api/v1`

---

## GET `/stocks/{profile}`

Recomenda ações filtradas pelo perfil do investidor.

**Parâmetros:**
- `profile` (path, obrigatório): `iniciante`, `moderado` ou `agressivo`

**Fluxo interno:**
1. Busca tickers disponíveis via Brapi (`get_all_tickers`)
2. Obtém cotações em tempo real (Brapi) com fallback para `REALISTIC_DATA`
3. Aplica filtros do perfil: ROE, DY, P/VP, liquidez, variação mensal, etc.
4. Ordena por dividend yield (decrescente) → Top 10
5. Para cada ação, busca notícias e analisa sentimento
6. Retorna as 10 melhores

**Exemplo resposta:**
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
    "roe": 18.2,
    "daily_liquidity": 250000000,
    "price_to_book": 2.15,
    "news_analysis": "boa",
    "news_score": 3,
    "profile": "iniciante"
  }
]
```

---

## GET `/news/{ticker}`

Análise de sentimento das notícias recentes de um ativo.

**Parâmetros:**
- `ticker` (path, obrigatório): código do ativo (ex: ITUB4)

**Fluxo interno:**
1. Busca notícias via Partnr.ai (até 50 artigos)
2. Se vazio, fallback para Dados de Mercado (últimos 7 dias)
3. Se ainda vazio, gera notícias mock
4. Seleciona top 5 por view_count
5. Analisa sentimento via DeepSeek (ou keyword fallback)
6. Classifica como "boa" (positive > negative) ou "ruim" (negative > positive)

**Exemplo resposta:**
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
      "ticker": "ITUB4"
    }
  ]
}
```

---

## GET `/dividends/{ticker}`

Calendário de dividendos de um ativo.

**Parâmetros:**
- `ticker` (path, obrigatório): código do ativo

**Fluxo interno:**
1. Busca código CVM da empresa via `CVm_CODE_MAP`
2. Obtém proventos via Dados de Mercado API
3. Se sem dados, gera dados realistas estimados
4. Identifica próximo pagamento e total YTD

**Exemplo resposta:**
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
      "type": "DIVIDENDO",
      "ex_date": "2026-05-15",
      "payable_date": "2026-06-01"
    }
  ]
}
```

---

## GET `/macro`

Indicadores macroeconômicos (SELIC e CDI).

**Fluxo interno:**
1. Consulta HG Brasil API
2. Fallback para valores default (SELIC=14.75, CDI=14.75)

**Exemplo resposta:**
```json
{
  "selic": 14.75,
  "cdi": 14.75,
  "date": "2026-05-05"
}
```

---

## GET `/filters`

Retorna os critérios de filtro de cada perfil de investidor.

**Exemplo resposta:**
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
    "min_dividend_yield": 8.0
  }
}
```

---

## GET `/history/{ticker}`

Histórico de preços OHLCV.

**Parâmetros:**
- `ticker` (path, obrigatório): código do ativo
- `days` (query, opcional, default=30): período em dias

**Fluxo interno:**
1. Consulta Brapi API para histórico
2. Fallback para dados sintéticos realistas (variação aleatória controlada)

**Exemplo resposta:**
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

## GET `/portfolio`

Carteira completa do investidor com valores atualizados.

**Fluxo interno:**
1. Tenta Google Sheets (service account → OAuth2 → CSV export)
2. Fallback para carteira mock (`MOCK_PORTFOLIO` com 15 ativos)
3. Para cada ativo, busca cotação atual via Brapi
4. Fallback de cotação via `REALISTIC_PRICES`
5. Calcula valor investido, valor atual, resultado (R$ e %)

**Exemplo resposta:**
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

## GET `/portfolio/dividends`

Dividendos da carteira do investidor.

**Fluxo interno:**
1. Obtém carteira do Google Sheets
2. Busca dividendos mock (`MOCK_DIVIDENDS`)
3. Enriquece com Dividend Yield do `REALISTIC_DATA`
4. Ordena por data de pagamento (decrescente)

---

## GET `/portfolio/chart/{ticker}`

Dados para gráfico de candlestick/linha.

**Parâmetros:**
- `ticker` (path, obrigatório)
- `days` (query, opcional, default=30, min=1, max=365)

**Fluxo interno:**
1. Busca histórico via Brapi
2. Fallback para dados sintéticos realistas (random walk controlado)
3. Converte timestamps para datas ISO

---

## GET `/health`

Health check.

```json
{
  "status": "ok",
  "version": "1.1.0"
}
```

---

## GET `/`

Frontend SPA (index.html).
