# Tech Context

## Stack Principal
| Tecnologia | Versão | Propósito |
|-----------|--------|-----------|
| Python | 3.12 | Runtime |
| FastAPI | >=0.115.0 | Framework REST |
| Uvicorn | >=0.32.0 | Servidor ASGI |
| Pydantic | >=2.9.2 | Validação de schemas |
| ECharts | 5.4.3 | Gráficos frontend |

## Dependências Python
| Pacote | Versão | Uso |
|--------|--------|-----|
| httpx | >=0.27.2 | HTTP async client |
| aiohttp | >=3.10.5 | HTTP async alternativo |
| openai | >=1.54.0 | DeepSeek API (SDK compatível) |
| python-dotenv | >=1.0.1 | Carregar .env |
| gspread | >=6.2.0 | Google Sheets API |
| odfpy | >=1.4.1 | Leitura de arquivos .ods |
| pytz | >=2024.2 | Fuso horário |
| python-multipart | >=0.0.18 | Upload de arquivos |

## APIs Externas
| API | Função | Token (env) |
|-----|--------|-------------|
| Brapi.dev | Cotações em tempo real, histórico | `BRAPI_TOKEN` |
| Dados de Mercado | Dados fundamentalistas, proventos | `DADOS_MERCADO_TOKEN` |
| Partnr.ai | Notícias financeiras, screener | `PARTNR_TOKEN` |
| HG Brasil | Dados macroeconômicos | `HG_BRASIL_KEY` |
| DeepSeek | Análise de sentimento de notícias | `DEEP_SEEK_KEY` |

Todas as chaves são opcionais — sistema degrada graciosamente.

## Configuração de Ambiente
```bash
cp .env.example .env
# Configurar tokens conforme necessário
uvicorn main:app --reload --port 8000
```

## Estrutura de Diretórios
```
app_investidor/
  main.py                Servidor FastAPI (porta 8000), rotas REST
  index.html             SPA frontend com ECharts
  requirements.txt       Dependências Python
  .env                   Configuração (tokens de API)
  custom_stocks.json     Stocks adicionados manualmente
  lista_acao.ods         Planilha ODS da carteira
  start.sh               Script de inicialização
  models/
    schemas.py           Modelos Pydantic
  skills/
    stock_skill.py       Recomendação por perfil
    news_skill.py        Análise de sentimento
  services/
    brapi.py             Brapi.dev
    dados_mercado.py     Dados de Mercado
    google_sheets.py     Google Sheets
    hgbrasil.py          HG Brasil
    news_sentiment.py    DeepSeek + keywords
    partnr.py            Partnr.ai
    ods_reader.py        Leitor ODS
    custom_portfolio.py  Stocks manuais
  docs/                  Documentação
  memory-bank/           Memory Bank (este diretório)
```

## Endpoints da API
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/stocks/{profile}` | Recomendações por perfil |
| GET | `/api/v1/news/{ticker}` | Análise de sentimento |
| GET | `/api/v1/dividends/{ticker}` | Calendário de dividendos |
| GET | `/api/v1/macro` | SELIC e CDI |
| GET | `/api/v1/history/{ticker}` | Histórico OHLCV |
| GET | `/api/v1/portfolio` | Carteira consolidada |
| GET | `/api/v1/portfolio/dividends` | Dividendos da carteira |
| GET | `/api/v1/portfolio/chart/{ticker}` | Dados para gráfico |
| GET | `/api/v1/filters` | Critérios dos perfis |
| POST | `/api/v1/portfolio/upload-ods` | Upload de ODS |
| POST | `/api/v1/portfolio/reload-ods` | Recarregar ODS |
| POST | `/api/v1/portfolio/add` | Adicionar ativo manual |
| POST | `/api/v1/portfolio/sell` | Vender ativo |
| GET | `/api/v1/health` | Health check |
