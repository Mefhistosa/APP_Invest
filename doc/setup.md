# Setup e Configuracao (deprecated)

> **A documentacao foi movida para [`docs/config.md`](/home/dsa/Documentos/app_investidor/docs/config.md).**

## Dependencias

| Pacote | Versao | Proposito |
|--------|--------|-----------|
| fastapi | >=0.115.0 | Framework web REST |
| uvicorn[standard] | >=0.32.0 | Servidor ASGI |
| pydantic | >=2.9.2 | Validacao de dados |
| python-dotenv | >=1.0.1 | Carregar .env |
| httpx | >=0.27.2 | HTTP async client |
| aiohttp | >=3.10.5 | HTTP async alternativo |
| openai | >=1.54.0 | DeepSeek API (SDK OpenAI) |
| pytz | >=2024.2 | Fuso horario |
| gspread | >=6.2.0 | Google Sheets API |
| yfinance | >=1.3.0 | Yahoo Finance (nao usado ativamente) |
| pandas | >=2.0.0 | Manipulacao de dados (nao usado ativamente) |

## Setup Rapido

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Variaveis de Ambiente

Todas sao opcionais — o sistema degrada graciosamente.

| Variavel | Fallback se ausente |
|----------|---------------------|
| `BRAPI_TOKEN` | Modo free (limitado) |
| `DADOS_MERCADO_TOKEN` | Servico nao disponivel |
| `HG_BRASIL_KEY` | Servico nao disponivel |
| `PARTNR_TOKEN` | Servico nao disponivel |
| `DEEP_SEEK_KEY` | Analise por keywords |
| `SHEET1_ID` | Usa sheet ID default |
| `SHEET2_ID` | Usa sheet ID default |

## Cadeia de Fallbacks

```
Google Sheets: Service Account → OAuth2 → CSV Export → Mock Portfolio
Noticias: Partnr.ai → Dados de Mercado → Mock News
Sentimento: DeepSeek → Keyword Analysis
Cotacoes: Brapi → Realistic Prices (fallback estatico)
Macro: HG Brasil → Valores default (SELIC=14.75, CDI=14.75)
```
