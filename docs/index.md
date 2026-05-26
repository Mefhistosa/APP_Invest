# APP Investidor

Suite de acompanhamento de investimentos em ações brasileiras. Recomenda ativos conforme perfil de investidor usando dados fundamentalistas, análise de sentimento de notícias e indicadores macroeconômicos.

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.11+, FastAPI, Uvicorn |
| Frontend | HTML5, CSS3, JavaScript (vanilla), ECharts |
| APIs de Dados | Brapi.dev, Dados de Mercado, Partnr.ai, HG Brasil |
| IA | DeepSeek (análise de sentimento) com fallback por keywords |
| Planilhas | Google Sheets (gspread + export CSV) |
| Ambientes | python-dotenv, variáveis de ambiente |

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    APP Investidor                            │
│  ┌──────────┐   ┌────────────┐   ┌──────────────────────┐  │
│  │  SPA      │   │  FastAPI   │   │   Skills Layer       │  │
│  │  Frontend │──▶│  REST API  │──▶│  (Regras de Negocio)  │  │
│  │  index.html│  │  main.py   │   │  stock_skill.py       │  │
│  └──────────┘   └─────┬──────┘   │  news_skill.py        │  │
│                       │          └──────────┬───────────┘  │
│                       │                     │              │
│              ┌────────▼─────────────────────▼──────────┐   │
│              │           Services Layer                 │   │
│              │  (Integracoes Externas)                  │   │
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

```
app_investidor/
  main.py                Servidor FastAPI (porta 8000), rotas REST
  index.html             SPA frontend com ECharts
  requirements.txt       Dependências Python
  .env                   Configuração (tokens de API)
  service_account.json   (opcional) Google Sheets service account
  credentials.json       (opcional) Google Sheets OAuth2
  models/
    schemas.py           Modelos Pydantic (schemas de dados)
  skills/
    stock_skill.py       Lógica de recomendação por perfil de investidor
    news_skill.py        Busca e análise de sentimento de notícias
  services/
    brapi.py             Preços e cotações em tempo real via Brapi.dev
    dados_mercado.py     Dados fundamentalistas via Dados de Mercado
    google_sheets.py     Leitura de carteira de investimentos do Google Sheets
    hgbrasil.py          Dados macroeconômicos via HG Brasil
    news_sentiment.py    Análise de sentimento com DeepSeek + keywords
    partnr.py            Screener de ações e notícias financeiras via Partnr.ai
  docs/
    index.md             Este arquivo
    api.md               Documentação da API REST
    models.md            Schemas e tipos de dados
    services.md          Serviços de integração externa
    skills.md            Lógica de domínio (skills)
    frontend.md          Interface web SPA
    config.md            Configuração e setup
```

## Fluxo Principal

```
Usuário → Seleciona Perfil → /api/v1/stocks/{perfil}
  ├─ Brapi → Preços e cotações
  ├─ Realistic Data → Dados fundamentalistas fallback
  ├─ Filtros por perfil (ROE, DY, P/VP, liquidez, etc.)
  ├─ Ordenação por dividend yield → Top 10
  └─ Partnr/Dados Mercado → Notícias → DeepSeek → Sentimento
       └─ Top 5 com notícias positivas
```

## Endpoints Principais

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/stocks/{profile}` | Recomendações por perfil |
| GET | `/api/v1/news/{ticker}` | Análise de sentimento |
| GET | `/api/v1/dividends/{ticker}` | Calendário de dividendos |
| GET | `/api/v1/macro` | Dados macroeconômicos |
| GET | `/api/v1/history/{ticker}` | Histórico de preços |
| GET | `/api/v1/portfolio` | Carteira do investidor |
| GET | `/api/v1/portfolio/dividends` | Dividendos da carteira |
| GET | `/api/v1/portfolio/chart/{ticker}` | Dados para gráfico |
| GET | `/api/v1/filters` | Critérios dos perfis |
| GET | `/api/v1/health` | Health check |
| GET | `/` | Frontend SPA |

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configurar tokens
uvicorn main:app --reload --port 8000
```

Ver [config.md](config.md) para variáveis de ambiente e setup completo.
