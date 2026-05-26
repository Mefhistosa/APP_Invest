# System Patterns — App Investidor

## Arquitetura em Camadas

```
┌─────────────────────────────────────┐
│         Frontend SPA (Vanilla JS)   │
│  index.html + ECharts 5.4.3 (CDN)  │
│  4 abas: Ações | Gráficos |         │
│  Dividendos | Recomendações         │
└──────────────┬──────────────────────┘
               │ HTTP (fetch API)
               ▼
┌─────────────────────────────────────┐
│         API REST (FastAPI)          │
│  main.py — 14 endpoints             │
│  CORS aberto, Pydantic v2 schemas   │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
┌─────────────┐   ┌──────────────┐
│   Skills    │   │   Services   │
│ (Regras de  │   │ (Integrações)│
│  negócio)   │   │              │
├─────────────┤   ├──────────────┤
│ stock_skill │   │ brapi.py     │
│ news_skill  │   │ dados_mercado│
└─────────────┘   │ partnr.py    │
                  │ hgbrasil.py  │
                  │ news_sentiment│
                  │ google_sheets│
                  │ ods_reader   │
                  │ custom_portfolio│
                  └──────────────┘
```

## Padrões de Design

### Repository Pattern (Services)
Cada fonte de dados externa tem seu próprio módulo em `services/`. Toda comunicação externa passa por esses módulos. Fallbacks locais quando APIs falham.

### Strategy Pattern (Skills)
`stock_skill.py` implementa 3 estratégias de filtragem (iniciante/moderado/agressivo). `news_skill.py` coordena pipeline de coleta + análise de sentimento.

### Chain of Responsibility (Fallbacks)
`google_sheets.py:get_portfolio_from_sheets()` tenta ODS → gspread → CSV → mock, em ordem decrescente de confiabilidade.

### Singleton (Dados Hardcoded)
`stock_skill.py:REALISTIC_DATA` e `main.py:REALISTIC_PRICES` funcionam como caches locais imutáveis para ~48 ativos.

## Fluxos de Dados

### Recomendação por Perfil
```
GET /api/v1/stocks/{profile}
  → stock_skill.get_stocks_by_profile()
    → REALISTIC_DATA (cache local)
    → Aplica filtros do perfil
    → Ordena por score composto
  ← Top 10 ativos com scores
```

### Carteira do Usuário
```
GET /api/v1/portfolio
  → google_sheets.get_portfolio_from_sheets()
    → ods_reader.get_portfolio_from_ods()  [tenta ODS local]
    → gspread [tenta Google Sheets API]
    → fetch_sheet_as_csv [tenta export CSV]
    → MOCK_PORTFOLIO  [fallback]
  ← Lista de posições (ticker, quantidade, preço médio)
```

### Análise de Sentimento
```
GET /api/v1/news/{ticker}
  → news_skill.get_news_for_ticker()
    → partnr.py (busca notícias)
    → dados_mercado.py (fallback)
    → generate_mock_news() (fallback final)
  → news_skill.analyze_news_sentiment()
    → ai_sentiment_analysis() [DeepSeek]
    → keyword_sentiment_analysis() [fallback]
  ← Notícias com classificação (boa/ruim)
```

## Decisões Arquiteturais

| Decisão | Trade-off |
|---------|-----------|
| Vanilla JS (sem framework) | Curva de aprendizado zero, mas sem componentes reutilizáveis |
| Dados mock hardcoded | Disponibilidade total, mas requer atualização manual |
| Múltiplas fontes de carteira | Flexibilidade máxima, mas lógica de parsing duplicada |
| DeepSeek para sentimento | Gratuito/open source, mas menos preciso que APIs pagas |
| CORS aberto (`*`) | Simplicidade em dev, mas inseguro para produção |
