# Services — Integrações Externas

Camada de integração com APIs de dados financeiros. Cada serviço encapsula um provedor externo.

---

## Brapi (`services/brapi.py`)

Integração com [Brapi.dev](https://brapi.dev) para dados de mercado brasileiro.

| Função | Descrição |
|--------|-----------|
| `get_stock_quote(ticker)` | Cotação individual em tempo real |
| `get_multiple_quotes(tickers)` | Cotações em lote (múltiplos tickers) |
| `get_stock_history(ticker, days)` | Histórico OHLCV por período |
| `get_all_tickers()` | Lista de tickers monitorados (~65 ativos) |

**Config:** `BRAPI_TOKEN` (env, default `"free"`)

**Notas:**
- Token free tem limite de requisições
- Retorna `None`/`[]` em caso de erro (sem exceptions propagadas)

---

## Dados de Mercado (`services/dados_mercado.py`)

Integração com [api.dadosdemercado.com.br](https://api.dadosdemercado.com.br) para dados fundamentalistas.

| Função | Descrição |
|--------|-----------|
| `get_market_ratios(cvm_code)` | Índices de mercado (P/L, EV/EBITDA, etc.) |
| `get_financial_ratios(cvm_code)` | Indicadores financeiros (ROE, ROA, margens) |
| `get_dividends(cvm_code)` | Histórico de proventos |
| `get_dividend_yield(ticker)` | Dividend Yield histórico |
| `get_stock_quotes(ticker)` | Cotações históricas |
| `get_companies()` | Lista de empresas disponíveis |
| `get_news()` | Notícias financeiras recentes |
| `get_cvm_code(ticker)` | Mapa ticker → código CVM (dict estático) |

**Config:** `DADOS_MERCADO_TOKEN` (env)

**Notas:**
- Sem token, retorna `None`/`[]` silenciosamente (degradação graciosa)
- Mapa CVM contém ~50 empresas
- Códigos CVM no formato `CVm_CODE_MAP`

---

## HG Brasil (`services/hgbrasil.py`)

Integração com [HG Brasil Finance](https://hgbrasil.com/finance) para dados macroeconômicos.

| Função | Descrição |
|--------|-----------|
| `get_stock_price(symbol)` | Cotação individual |
| `get_stock_prices(symbols)` | Cotações em lote |
| `get_macro_data()` | SELIC e CDI atuais |

**Config:** `HG_BRASIL_KEY` (env)

**Notas:**
- Sem API key, retorna `None` silenciosamente
- Dados macro retornam do endpoint raiz da API financeira

---

## Partnr (`services/partnr.py`)

Integração com [Partnr.ai](https://partnr.ai) para screening e notícias.

| Função | Descrição |
|--------|-----------|
| `screener(filters)` | Filtro avançado de ações |
| `get_news(tickers, limit)` | Notícias financeiras por ticker |
| `get_stock_data(ticker)` | Dados cadastrais da empresa |
| `get_quotes(ticker)` | Cotações históricas |

**Config:** `PARTNR_TOKEN` (env)

**Notas:**
- Sem token, retorna `[]` silenciosamente
- Principal fonte de notícias do sistema

---

## News Sentiment (`services/news_sentiment.py`)

Análise de sentimento de notícias financeiras.

| Função | Descrição |
|--------|-----------|
| `ai_sentiment_analysis(articles)` | Análise via DeepSeek API |
| `keyword_sentiment_analysis(text)` | Análise por keywords (fallback) |
| `keyword_batch_analysis(articles)` | Batch analysis via keywords |
| `classify_sentiment(positive, negative)` | Classifica como boa/ruim/neutra |

**Keywords positivas:** lucro, crescimento, alta, ganho, recorde, expansão, dividendo, aprovação, etc.
**Keywords negativas:** prejuízo, queda, baixa, perda, crise, recessão, multa, fraude, etc.

**Config:** `DEEP_SEEK_KEY` (env)

**Fluxo:**
1. Tenta DeepSeek (`model: deepseek-chat`) com prompt estruturado
2. Se falhar (sem key, erro, timeout), fallback para keyword matching
3. Keywords são contadas por ocorrência no título + corpo

---

## Google Sheets (`services/google_sheets.py`)

Leitura de carteira de investimentos do Google Sheets.

| Função | Descrição |
|--------|-----------|
| `get_portfolio_from_sheets()` | Carteira do investidor |
| `get_portfolio_dividends(tickers)` | Dividendos da carteira |
| `fetch_sheet_as_csv(sheet_id)` | Exporta planilha como CSV |
| `parse_portfolio_from_csv(csv_text)` | Parse do CSV para dict |
| `parse_portfolio_from_worksheet(worksheet)` | Parse via gspread |

**IDs de planilhas:**
- `SHEET1_ID`: `1jyEveMHVnwqZzAFBLTMiynmot-tafYnhavijpVBoadU`
- `SHEET2_ID`: `1e0upnG4TNa-NRMZS3tAWvaZk3_P7V4EYA1NAPuim-aE`

**Autenticação (tentativa em ordem):**
1. Service Account (`service_account.json`)
2. OAuth2 (`credentials.json` + `authorized_user.json`)
3. CSV export público (sem auth)
4. **Fallback:** carteira mock (`MOCK_PORTFOLIO` com 15 ativos)

**Estrutura esperada da planilha:**
- Linhas 1-3: cabeçalho ignorado
- Linha 4+: `Ticker | ... | Quantidade | Preço Médio | ...`
- Colunas: índice 0 (ticker), 3 (quantidade), 4 (preço médio)
