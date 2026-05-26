# Configuração e Setup

## Dependências

Ver `requirements.txt`:

| Pacote | Versão | Propósito |
|--------|--------|-----------|
| fastapi | >=0.115.0 | Framework web REST |
| uvicorn[standard] | >=0.32.0 | Servidor ASGI |
| pydantic | >=2.9.2 | Validação de dados/schemas |
| python-dotenv | >=1.0.1 | Carregar .env |
| httpx | >=0.27.2 | HTTP async client |
| aiohttp | >=3.10.5 | HTTP async alternativo |
| openai | >=1.54.0 | DeepSeek API (compatível OpenAI SDK) |
| pytz | >=2024.2 | Fuso horário |
| gspread | >=6.2.0 | Google Sheets API |
| yfinance | >=1.3.0 | Yahoo Finance (não usado ativamente) |
| pandas | >=2.0.0 | Manipulação de dados (não usado ativamente) |

## Setup

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
```

## Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `BRAPI_TOKEN` | Não | Token Brapi.dev (free se vazio) |
| `DADOS_MERCADO_TOKEN` | Não | Token Dados de Mercado |
| `HG_BRASIL_KEY` | Não | API Key HG Brasil |
| `PARTNR_TOKEN` | Não | Token Partnr.ai |
| `DEEP_SEEK_KEY` | Não | API Key DeepSeek |
| `OPENAI_API_KEY` | Não | API Key OpenAI (fallback) |
| `SHEET1_ID` | Não | ID da planilha Google Sheets 1 |
| `SHEET2_ID` | Não | ID da planilha Google Sheets 2 |

Todas as variáveis são opcionais — o sistema degrada graciosamente:
- Sem token de API → fallback para dados mock/realistic_data
- Sem DeepSeek → fallback para análise por keywords
- Sem Google Sheets → fallback para carteira mock

## Execução

### Script rápido (recomendado)

```bash
./start.sh
```

O script ativa o virtualenv, instala dependências se necessário, copia `.env` se não existir, e inicia o servidor.

### Manual

```bash
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Produção

```bash
# Sem --reload
uvicorn main:app --host 0.0.0.0 --port 8000
```

Servidor disponível em `http://localhost:8000`

## Estrutura de Fallbacks

```
Google Sheets (auth) → Google Sheets (CSV) → Mock Portfolio
Partnr.ai → Dados de Mercado → Mock News
DeepSeek → Keyword Sentiment Analysis
Brapi → Realistic Prices
```
