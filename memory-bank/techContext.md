# Tech Context — App Investidor

## Stack Tecnológico

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Runtime | Python | 3.12.3 |
| Framework Web | FastAPI | >=0.115.0 |
| Servidor ASGI | Uvicorn | >=0.32.0 |
| Validação | Pydantic | >=2.9.2 |
| Frontend | Vanilla JS + HTML5 + CSS3 | — |
| Gráficos | ECharts | 5.4.3 (CDN) |
| Templates | Jinja2 (não usado ativamente) | — |

## Dependências (requirements.txt)

| Pacote | Versão | Finalidade |
|--------|--------|------------|
| fastapi | >=0.115.0 | Framework REST |
| python-multipart | >=0.0.18 | Upload de arquivos |
| uvicorn[standard] | >=0.32.0 | Servidor ASGI |
| pydantic | >=2.9.2 | Schemas/validação |
| python-dotenv | >=1.0.1 | Variáveis de ambiente |
| httpx | >=0.27.2 | HTTP async (APIs externas) |
| aiohttp | >=3.10.5 | HTTP async (não usado ativamente) |
| openai | >=1.54.0 | Cliente DeepSeek (API compatível) |
| pytz | >=2024.2 | Fuso horário |
| gspread | >=6.2.0 | Google Sheets API |
| pandas | >=2.0.0 | Leitura ODS |
| odfpy | >=1.4.1 | Engine ODF para pandas |
| yfinance | >=1.3.0 | Yahoo Finance (não usado ativamente) |

## APIs Externas

| API | Endpoints Usados | Auth | Fallback |
|-----|-----------------|------|----------|
| Brapi.dev | /api/quote/{ticker}, /api/quote/history | Token (query param) | REALISTIC_PRICES |
| Dados de Mercado | /api/v1/ratios, /api/v1/dividends, /api/v1/dy, /api/v1/quotes | Token (header) | REALISTIC_DATA |
| HG Brasil | /financial/stock_price, /financial/macro | Key (query param) | Dados mock |
| Partnr.ai | /v1/screener, /v1/news, /v1/stock_data, /v1/quotes | Token (header) | Mock news |
| DeepSeek | /v1/chat/completions (API compatível OpenAI) | Key (header) | Keyword sentiment |

## Configuração (.env)

```
BRAPI_TOKEN=<token>
DADOS_MERCADO_TOKEN=<token>
HG_BRASIL_KEY=<key>
PARTNR_TOKEN=<token>
DEEP_SEEK_KEY=<key>
SHEET1_ID=1jyEveMHVnwqZzAFBLTMiynmot-tafYnhavijpVBoadU
SHEET2_ID=1e0upnG4TNa-NRMZS3tAWvaZk3_P7V4EYA1NAPuim-aE
```

## Estrutura de Diretórios

```
app_investidor/
├── main.py                    # Servidor FastAPI + endpoints
├── index.html                 # Frontend SPA
├── requirements.txt           # Dependências Python
├── start.sh                   # Script de inicialização
├── custom_stocks.json         # Carteira local (JSON)
├── lista_acao.ods             # Carteira local (planilha)
├── models/
│   └── schemas.py             # Pydantic models
├── skills/
│   ├── stock_skill.py         # Recomendação por perfil
│   └── news_skill.py          # Pipeline de notícias
├── services/
│   ├── brapi.py               # Integração Brapi.dev
│   ├── dados_mercado.py       # Integração Dados de Mercado
│   ├── hgbrasil.py            # Integração HG Brasil
│   ├── partnr.py              # Integração Partnr.ai
│   ├── news_sentiment.py      # Análise DeepSeek + keywords
│   ├── google_sheets.py       # Leitura Google Sheets
│   ├── ods_reader.py          # Leitura planilha ODS
│   └── custom_portfolio.py    # Carteira JSON local
├── docs/                      # Documentação atual
├── doc/                       # Documentação deprecada
├── memory-bank/               # Este Memory Bank
├── venv/                      # Ambiente virtual Python
└── .env                       # Variáveis de ambiente (gitignored)
```

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Frontend SPA |
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/stocks/{profile}` | Recomendações por perfil |
| GET | `/api/v1/news/{ticker}` | Análise de sentimento |
| GET | `/api/v1/dividends/{ticker}` | Calendário de dividendos |
| GET | `/api/v1/macro` | Dados macroeconômicos |
| GET | `/api/v1/filters` | Critérios dos perfis |
| GET | `/api/v1/history/{ticker}` | Histórico de preços |
| GET | `/api/v1/portfolio` | Carteira do usuário |
| GET | `/api/v1/portfolio/dividends` | Dividendos da carteira |
| GET | `/api/v1/portfolio/chart/{ticker}` | Dados para gráfico |
| POST | `/api/v1/portfolio/upload-ods` | Upload de ODS |
| POST | `/api/v1/portfolio/reload-ods` | Recarregar ODS local |
| POST | `/api/v1/portfolio/add` | Adicionar ação |
| POST | `/api/v1/portfolio/sell` | Vender/reduzir ação |
