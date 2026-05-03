#!/bin/bash
# ClaudeTrader — Setup inicial
set -e

cd "$(dirname "$0")"

echo "── ClaudeTrader Setup ──"

# 1. Verifica Python 3.12+
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python detectado: $PYTHON_VERSION"
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)'; then
    echo "AVISO: Python 3.12+ recomendado (MCP server exige)."
fi

# 2. Cria venv se não existir
if [ ! -d ".venv" ]; then
    echo "Criando virtualenv em .venv/ ..."
    python3 -m venv .venv
fi

# 3. Ativa venv
source .venv/bin/activate

# 4. Atualiza pip e instala deps
echo "Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Verifica .env
if [ ! -f ".env" ]; then
    echo "AVISO: .env não encontrado. Crie com:"
    echo "  GROQ_API_KEY=sua_chave"
    echo "  OPEN_ROUTER=sua_chave"
fi

# 6. Cria diretório de memória de decisões
mkdir -p .claude/memory/investment-decisions

echo ""
echo "── Setup concluído ──"
echo "Para executar: source .venv/bin/activate && ./run_app.sh"
echo "Neo4j (opcional): docker compose up -d neo4j"
