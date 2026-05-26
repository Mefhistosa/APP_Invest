# Skills — Lógica de Domínio

Camada de lógica de negócio que orquestra os serviços externos e aplica as regras de domínio.

---

## Stock Skill (`skills/stock_skill.py`)

Módulo principal de recomendação de ações por perfil de investidor.

### Perfis e Critérios

Cada perfil tem critérios definidos em `PROFILE_CRITERIA`:

| Critério | Iniciante | Moderado | Agressivo |
|----------|-----------|----------|-----------|
| Preço | R$ 2-50 | R$ 2-70 | R$ 2-120 |
| ROE min | 13% | 10% | 10% |
| Liquidez min | R$ 10M | R$ 10M | R$ 10M |
| P/VP | 0.2-3.0 | 0.2-3.0 | 0.2-5.0 |
| DY min | 8% | 5% | 2% |
| Prov./Lucro max | 100% | 130% | — |
| Variação mensal max | — | 3% | 8% |
| PL >= Valor Mercado | Sim | — | — |
| PL >= Dívida Bruta | — | Sim | — |

### Funções Principais

| Função | Descrição |
|--------|-----------|
| `get_stocks_by_profile(profile)` | Pipeline completo: busca → filtra → ordena → analisa → retorna top 10 |
| `filter_stock(stock, criteria)` | Aplica todos os filtros de um perfil a um stock |
| `build_stock_from_data(ticker, brapi_data, realistic)` | Monta objeto Stock a partir de fontes de dados |
| `get_all_filters()` | Retorna critérios de todos os perfis |
| `get_realistic_data(ticker)` | Busca dados fundamentalistas do cache local |
| `calculate_monthly_variation(price)` | Gera variação mensal sintética |
| `determine_dividend_type(ticker)` | Define JCP para bancos, DIVIDENDO para demais |

### Dados Realistas (`REALISTIC_DATA`)

Cache local com dados fundamentalistas de 48 ativos brasileiros. Cada entrada contém:

| Campo | Descrição |
|-------|-----------|
| `name` | Nome da empresa |
| `roe` | ROE (%) |
| `dy` | Dividend Yield 12m (%) |
| `pvp` | P/VP |
| `price` | Preço de referência (R$) |
| `prev_price` | Preço anterior |
| `vol` | Volume/liquidez diária |
| `pl` | Patrimônio Líquido |
| `mv` | Valor de Mercado |
| `debt` | Dívida Bruta |
| `np` | Lucro Líquido |
| `proc` | Total de Proventos |

Usado como fallback quando APIs externas não respondem.

### Fluxo de Recomendação

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

---

## News Skill (`skills/news_skill.py`)

Módulo de busca e análise de sentimento de notícias.

### Funções

| Função | Descrição |
|--------|-----------|
| `get_news_for_ticker(ticker, limit)` | Busca notícias de múltiplas fontes com fallback |
| `analyze_news_sentiment(ticker)` | Pipeline completo: busca → analisa → classifica |
| `generate_mock_news(ticker)` | Gera 5 notícias mock para demonstração |

### Fluxo de Notícias

```
analyze_news_sentiment(ticker):
  1. get_news_for_ticker(ticker):
     a. Tenta Partnr.ai (até 50 artigos)
     b. Se vazio, fallback Dados de Mercado (7 dias)
     c. Se vazio, generate_mock_news()
     d. Ordena por view_count desc
     e. Top 5
  2. Converte artigos para dict
  3. ai_sentiment_analysis():
     a. Tenta DeepSeek com prompt estruturado
     b. Se falhar, keyword_batch_analysis()
  4. classify_sentiment(positive, negative)
  5. Retorna NewsAnalysisResult
```

### Mock News

Quando não há notícias reais disponíveis, gera notícias sintéticas com:
- Fontes variadas (InfoMoney, Investidor10, Exame, Valor Econômico, Suno Research)
- View counts realistas (7k-15k)
- Datas nos últimos 5 dias
- Títulos genéricos positivos
