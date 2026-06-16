#!/bin/bash
# ============================================================
# 🦾 Gus Local — Inicializador Unificado
# ============================================================
# Inicia Ollama + Gus Local Server + Interface Web
#
# Pré-requisitos:
#   1. Ollama instalado
#   2. Modelo baixado: ollama pull gemma3:4b
#   3. Python 3.10+ + dependências
#
# Uso: bash start.sh
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "🦾 Gus Local — Inicializando..."
echo ""

# ── 1. Verifica dependências ──────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 não encontrado"
    exit 1
fi

if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Instalando dependências Python..."
    pip install fastapi uvicorn requests 2>/dev/null
fi

# ── 2. Inicia Ollama ──────────────────────────────────────────
if ! pgrep ollama > /dev/null; then
    echo "🚀 Iniciando Ollama..."
    ollama serve &
    sleep 3
fi

if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama não iniciou. Execute 'ollama serve' manualmente."
    exit 1
fi
echo "✅ Ollama rodando"

# ── 3. Verifica modelo ────────────────────────────────────────
MODEL="${GUS_MODEL:-gemma3:4b}"
if ! ollama list | grep -q "$MODEL"; then
    echo "📥 Baixando modelo $MODEL..."
    ollama pull "$MODEL"
fi
echo "✅ Modelo $MODEL disponível"

# ── 4. Inicia Banco de Memória ─────────────────────────────────
python3 -c "from memory import init_db; init_db()" 2>/dev/null
echo "✅ Memória local inicializada"

# ── 5. Inicia Servidor ─────────────────────────────────────────
PORT="${GUS_PORT:-8080}"
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   🦾 GUS LOCAL ONLINE                     ║"
echo "║   http://localhost:$PORT                      ║"
echo "║   /docs — Swagger API                     ║"
echo "║   Ctrl+C para encerrar                    ║"
echo "╚══════════════════════════════════════════╝"
echo ""

python3 server.py
