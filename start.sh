#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$APP_DIR"

# Detect Python interpreter
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PYTHON="$cmd"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "-> ERRO: Python nao encontrado. Instale python3 com: sudo apt install python3"
    exit 1
fi

echo "-> Usando interpretador: $($PYTHON --version)"

if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "-> Criando .env a partir de .env.example"
        cp .env.example .env
    else
        echo "-> ATENCAO: sem .env encontrado. Tokens de API serao mockados."
    fi
fi

if [ ! -d venv ]; then
    echo "-> Criando ambiente virtual venv/"
    if ! "$PYTHON" -m venv venv; then
        echo "-> ERRO: nao foi possivel criar o venv. Verifique se python3-venv esta instalado:"
        echo "  sudo apt install python3-venv"
        exit 1
    fi
fi

echo "-> Ativando venv e verificando dependencias"
source venv/bin/activate

if [ -f requirements.txt ]; then
    echo "-> Instalando dependencias..."
    pip install -r requirements.txt
fi

# Check if port 8000 is already in use
if ss -tlnp 2>/dev/null | grep -q :8000; then
    echo "-> AVISO: Porta 8000 ja esta em uso. Encerrando processo existente..."
    kill $(ss -tlnp | grep :8000 | grep -oP 'pid=\K[0-9]+') 2>/dev/null || true
    sleep 1
fi

echo "-> Iniciando servidor APP Investidor em http://localhost:8000"
echo "   (Ctrl+C para parar)"
echo ""
uvicorn main:app --reload --host 0.0.0.0 --port 8000
