# Services — Integracoes Externas (deprecated)

> **A documentacao foi movida para [`docs/services.md`](/home/dsa/Documentos/app_investidor/docs/services.md).**

Camada de integracao com APIs de dados financeiros. Cada servico encapsula um provedor externo. Todas as funcoes degradam graciosamente quando os tokens nao estao configurados.

---

## Brapi (`services/brapi.py`)

Integracao com [Brapi.dev](https://brapi.dev) para dados de mercado brasileiro.

| Funcao | Descricao |
|--------|-----------|
| `get_stock_quote(ticker)` | Cotacao individual em tempo real |
| `get_multiple_quotes(tickers)` | Cottacoes em lote |
| `get_stock_history(ticker, days)` | Historico OHLCV por periodo |
| `get_all_tickers()` | Lista de ~65 tickers monitorados |

**Config:** `BRAPI_TOKEN` (env, default `"free"`)

**Degradacao:** Retorna `None`/`[]` em caso de erro.

---

## Dados de Mercado (`services/dados_mercado.py`)

Integracao com [api.dadosdemercado.com.br](https://api.dadosdemercado.com.br).

| Funcao | Descricao |
|--------|-----------|
| `get_market_ratios(cvm_code)` | Indices de mercado (P/L, EV/EBITDA) |
| `get_financial_ratios(cvm_code)` | Indicadores financeiros (ROE, ROA) |
| `get_dividends(cvm_code)` | Historico de proventos |
| `get_dividend_yield(ticker)` | Dividend Yield historico |
| `get_stock_quotes(ticker)` | Cotacoes historicas |
| `get_companies()` | Lista de empresas disponiveis |
| `get_news()` | Noticias financeiras recentes |
| `get_cvm_code(ticker)` | Mapa ticker → codigo CVM (interno) |

**Config:** `DADOS_MERCADO_TOKEN` (env)

**Degradacao:** Sem token, retorna `None`/`[]` silenciosamente.

---

## HG Brasil (`services/hgbrasil.py`)

Integracao com [HG Brasil Finance](https://hgbrasil.com/finance).

| Funcao | Descricao |
|--------|-----------|
| `get_stock_price(symbol)` | Cotacao individual |
| `get_stock_prices(symbols)` | Cotacoes em lote |
| `get_macro_data()` | SELIC e CDI atuais |

**Config:** `HG_BRASIL_KEY` (env)

**Degradacao:** Sem API key, retorna `None` silenciosamente.

---

## Partnr (`services/partnr.py`)

Integracao com [Partnr.ai](https://partnr.ai) para screening e noticias.

| Funcao | Descricao |
|--------|-----------|
| `screener(filters)` | Filtro avancado de acoes |
| `get_news(tickers, limit)` | Noticias financeiras por ticker |
| `get_stock_data(ticker)` | Dados cadastrais da empresa |
| `get_quotes(ticker)` | Cotacoes historicas |

**Config:** `PARTNR_TOKEN` (env)

**Degradacao:** Sem token, retorna `[]` silenciosamente.

---

## News Sentiment (`services/news_sentiment.py`)

Analise de sentimento de noticias financeiras.

| Funcao | Descricao |
|--------|-----------|
| `ai_sentiment_analysis(articles)` | Analise via DeepSeek API |
| `keyword_sentiment_analysis(text)` | Analise por keywords (fallback) |
| `keyword_batch_analysis(articles)` | Batch analysis via keywords |
| `classify_sentiment(positive, negative)` | Classifica como boa/ruim/neutra |

**Keywords positivas:** lucro, crescimento, alta, ganho, recorde, expansao, dividendo, aprovado, oportunidade

**Keywords negativas:** prejuizo, queda, baixa, perda, crise, recessao, multa, fraude, corrupcao

**Config:** `DEEP_SEEK_KEY` (env)

**Fluxo:**
```
ai_sentiment_analysis(articles)
  ├── DeepSeek API (model: deepseek-chat)
  │   Parse JSON response → positive_factors / negative_factors
  │   Se falhar → keyword_batch_analysis (fallback)
  └── Retorna {positive: N, negative: N}
```

---

## Google Sheets (`services/google_sheets.py`)

Leitura de carteira de investimentos do Google Sheets.

| Funcao | Descricao |
|--------|-----------|
| `get_portfolio_from_sheets()` | Carteira do investidor |
| `get_portfolio_dividends(tickers)` | Dividendos da carteira |

**Ordem de autenticacao:**
1. Service Account (`service_account.json`)
2. OAuth2 (`credentials.json` + `authorized_user.json`)
3. CSV export (acesso publico)
4. **Fallback:** carteira mock (`MOCK_PORTFOLIO`)

**IDs de planilhas:** `SHEET1_ID` e `SHEET2_ID` (configuraveis via .env)

**Estrutura esperada:**
```
Linha 1-3: cabecalho (ignorado)
Linha 4+: Ticker | ... | Quantidade | Preco Medio | ...
Colunas: 0 (ticker), 3 (quantidade), 4 (preco medio)
```
