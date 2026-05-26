# System Patterns

## Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────┐
│                    APP Investidor                            │
│  ┌──────────┐   ┌────────────┐   ┌──────────────────────┐  │
│  │  SPA      │   │  FastAPI   │   │   Skills Layer       │  │
│  │  Frontend │──▶│  REST API  │──▶│  (Regras de Negócio)  │  │
│  │  index.html│  │  main.py   │   │  stock_skill.py       │  │
│  └──────────┘   └─────┬──────┘   │  news_skill.py        │  │
│                       │          └──────────┬───────────┘  │
│                       │                     │              │
│              ┌────────▼─────────────────────▼──────────┐   │
│              │           Services Layer                 │   │
│              │  (Integrações Externas)                  │   │
│              │                                          │   │
│  ┌───────────┼────────┬──────────┬──────────┬─────────┐│   │
│  │  Brapi    │Dados   │  Partnr  │ HG Brasil│ Google  ││   │
│  │  .dev     │Mercado │  .ai     │          │ Sheets  ││   │
│  └───────────┴────────┴──────────┴──────────┴─────────┘│   │
│              │                                          │   │
│              └──────────────────────────────────────────┘   │
│                                           │                 │
│                                    ┌──────▼──────┐          │
│                                    │   DeepSeek  │          │
│                                    │  (Sentimento)│         │
│                                    └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## Camadas

### 1. Frontend (SPA)
- `index.html` — Único arquivo, JavaScript vanilla
- ECharts para gráficos OHLCV
- fetch() para comunicação com API
- Responsivo (breakpoint 900px)

### 2. API (FastAPI)
- `main.py` — Rotas REST, injeção de dependências
- Models Pydantic em `models/schemas.py`
- Endpoints versionados: `/api/v1/*`

### 3. Skills (Regras de Negócio)
- `stock_skill.py` — Recomendação, filtros por perfil, dados realistas
- `news_skill.py` — Busca e análise de sentimento de notícias

### 4. Services (Integrações Externas)
- `brapi.py` — Cotações e histórico via Brapi.dev
- `dados_mercado.py` — Dados fundamentalistas via Dados de Mercado
- `partnr.py` — Notícias e screener via Partnr.ai
- `hgbrasil.py` — Dados macroeconômicos via HG Brasil
- `google_sheets.py` — Leitura de carteira do Google Sheets
- `news_sentiment.py` — Análise DeepSeek com fallback keyword
- `ods_reader.py` — Leitura de arquivos ODS
- `custom_portfolio.py` — Stocks adicionados manualmente

## Padrões de Design

### Degradação Graciosa (Graceful Degradation)
Toda integração externa tem fallback:
1. API real → cache local → dados mock/realistas
2. DeepSeek → análise por keywords
3. Google Sheets auth → CSV export → carteira mock

### Cache Local (Realistic Data)
Dict com 48 ativos brasileiros com dados fundamentalistas estáticos.
Usado como fallback primário quando APIs externas não respondem.

### Pipeline de Recomendação
```
get_stocks_by_profile(profile):
  1. all_tickers = get_all_tickers()
  2. brapi_quotes = get_multiple_quotes(tickers[:20])
  3. Para cada ticker:
     a. Busca cotação (batch → individual)
     b. Busca realistic_data
     c. build_stock_from_data()
     d. filter_stock() com critérios do perfil
  4. Ordena por dividend yield decrescente
  5. Top 10
  6. analyze_news_for_ticker() para cada stock
  7. Retorna stocks enriquecidos
```

### Pipeline de Notícias
```
analyze_news_sentiment(ticker):
  1. Partnr.ai (50 artigos)
  2. Fallback Dados de Mercado (7 dias)
  3. Fallback Mock News
  4. Top 5 por view_count
  5. DeepSeek → Keyword fallback
  6. Classifica boa/ruim
```

### Consolidação de Carteira
ODS (lista_acao.ods) + Custom Portfolio (custom_stocks.json) mesclados por ticker.
Preço médio recalculado ponderado por quantidade quando um ticker existe em ambas fontes.
