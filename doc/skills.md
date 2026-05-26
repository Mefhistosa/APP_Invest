# Skills — Logica de Dominio (deprecated)

> **A documentacao foi movida para [`docs/skills.md`](/home/dsa/Documentos/app_investidor/docs/skills.md).**

Camada de negocio que orquestra servicos externos e aplica regras de dominio.

---

## Stock Skill (`skills/stock_skill.py`)

Modulo principal de recomendacao de acoes por perfil.

### Perfis e Criterios

| Criterio | Iniciante | Moderado | Agressivo |
|----------|-----------|----------|-----------|
| Preco | R$ 2-50 | R$ 2-70 | R$ 2-120 |
| ROE min | 13% | 10% | 10% |
| Liquidez min | R$ 10M | R$ 10M | R$ 10M |
| P/VP | 0.2-3.0 | 0.2-3.0 | 0.2-5.0 |
| DY min | 8% | 5% | 2% |
| Prov./Lucro max | 100% | 130% | — |
| Variacao mensal | — | <= 3% | <= 8% |
| PL >= Valor Mercado | Exigido | — | — |
| PL >= Divida Bruta | — | Exigido | — |

### Funcoes Principais

| Funcao | Descricao |
|--------|-----------|
| `get_stocks_by_profile(profile)` | Pipeline completo: busca → filtra → ordena → analisa → top 10 |
| `filter_stock(stock, criteria)` | Aplica todos os filtros de um perfil |
| `build_stock_from_data(ticker, brapi_data, realistic)` | Monta objeto Stock |
| `get_all_filters()` | Retorna criterios de todos os perfis |
| `get_realistic_data(ticker)` | Busca dados fundamentalistas do cache local |
| `determine_dividend_type(ticker)` | JCP para bancos, DIVIDENDO para demais |

### Fluxo de Recomendacao

```
get_stocks_by_profile(profile):
  1. all_tickers = get_all_tickers() (~65 tickers)
  2. brapi_quotes = get_multiple_quotes(tickers[:20])
  3. Para cada ticker:
     a. Busca cotacao (batch → individual)
     b. Busca realistic_data (fallback)
     c. build_stock_from_data()
     d. filter_stock() com criterios do perfil
  4. Ordena por dividend yield (decrescente)
  5. Top 10
  6. analyze_news_for_ticker() para cada stock
  7. Retorna stocks enriquecidos com sentimento
```

### `REALISTIC_DATA`

Cache local com dados fundamentalistas de 48 ativos brasileiros. Usado como fallback quando as APIs externas nao respondem.

Cada entrada contem: `name`, `roe`, `dy`, `pvp`, `price`, `prev_price`, `vol`, `pl`, `mv`, `debt`, `np`, `proc`.

---

## News Skill (`skills/news_skill.py`)

Modulo de busca e analise de sentimento de noticias.

### Funcoes

| Funcao | Descricao |
|--------|-----------|
| `get_news_for_ticker(ticker, limit)` | Busca noticias de multiplas fontes com fallback |
| `analyze_news_sentiment(ticker)` | Pipeline completo: busca → analisa → classifica |
| `generate_mock_news(ticker)` | Gera 5 noticias mock para demonstracao |

### Fluxo de Noticias

```
analyze_news_sentiment(ticker):
  1. get_news_for_ticker(ticker):
     a. Tenta Partnr.ai (ate 50 artigos)
     b. Fallback: Dados de Mercado (7 dias)
     c. Fallback: generate_mock_news()
     d. Ordena por view_count desc
     e. Top 5
  2. Converte artigos para dict
  3. ai_sentiment_analysis() -> DeepSeek ou keyword
  4. classify_sentiment(positive, negative)
  5. Retorna NewsAnalysisResult
```

### Mock News

Quando nao ha noticias reais, gera 5 noticias sinteticas com:
- Fontes: InfoMoney, Investidor10, Exame, Valor Economico, Suno Research
- View counts: 7k-15k
- Datas: ultimos 5 dias
- Titulos genericos positivos
