#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  🦾 GUS LOCAL — Instalador Automático (Galaxy S20)
#  
#  Uso: 1. Instale o Termux do F-Droid
#       2. No Termux, cole esta linha:
#          curl -sL https://raw.githubusercontent.com/Gustpbbr/Teste-ChatGPT/organizacao-autoclaw/MASE/setup.sh | bash
#       3. Aguarde ~15 min (download do modelo)
#       4. Pronto — Gus rodando offline no seu celular
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}   🦾 GUS LOCAL — Instalador v1.0${NC}"
echo -e "${CYAN}   Galaxy S20 + Gemma 4B via Ollama${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# ── Verifica ambiente ──────────────────────────────────────────
if [ ! -d /data/data/com.termux/files/home ]; then
    echo -e "${RED}❌ Este script só roda no Termux.${NC}"
    echo "   Instale: https://f-droid.org/packages/com.termux/"
    exit 1
fi

# ── RAM check ───────────────────────────────────────────────────
RAM_MB=$(free -m | awk '/Mem:/ {print $2}')
echo -e "📊 RAM detectada: ${RAM_MB} MB"
if [ "$RAM_MB" -lt 4000 ]; then
    MODELO="gemma3:1b"
    echo -e "${YELLOW}⚠️  RAM < 4 GB → usando gemma3:1b (815 MB)${NC}"
elif [ "$RAM_MB" -lt 7000 ]; then
    MODELO="gemma3:1b"
    echo -e "${YELLOW}⚠️  RAM < 8 GB → usando gemma3:1b (815 MB)${NC}"
else
    MODELO="gemma3:4b"
    echo -e "${GREEN}✅ RAM ≥ 8 GB → usando gemma3:4b (2.5 GB — qualidade alta)${NC}"
fi
echo ""

# ── Passo 1: Dependências ──────────────────────────────────────
echo -e "${YELLOW}[1/5] Instalando dependências...${NC}"
pkg update -y -q 2>/dev/null
pkg upgrade -y -q 2>/dev/null
pkg install -y python python-pip git wget curl proot proot-distro 2>/dev/null
pip install -q ollama requests 2>/dev/null
echo -e "${GREEN}✅ Dependências instaladas${NC}"

# ── Passo 2: Instalar Ollama ────────────────────────────────────
echo -e "${YELLOW}[2/5] Instalando Ollama...${NC}"
if command -v ollama &>/dev/null; then
    echo -e "${GREEN}✅ Ollama já instalado: $(ollama --version)${NC}"
else
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}✅ Ollama instalado${NC}"
fi

# ── Passo 3: Iniciar Ollama ─────────────────────────────────────
echo -e "${YELLOW}[3/5] Iniciando Ollama...${NC}"
# Mata processo anterior se existir
pkill ollama 2>/dev/null || true
sleep 1
ollama serve &
sleep 3
echo -e "${GREEN}✅ Ollama rodando em localhost:11434${NC}"

# ── Passo 4: Baixar modelo ──────────────────────────────────────
echo -e "${YELLOW}[4/5] Baixando modelo ${MODELO}...${NC}"
echo -e "   (isso pode levar 10-15 minutos na primeira vez)"
if ollama list | grep -q "${MODELO}"; then
    echo -e "${GREEN}✅ Modelo ${MODELO} já presente${NC}"
else
    ollama pull "${MODELO}"
    echo -e "${GREEN}✅ Modelo ${MODELO} baixado${NC}"
fi

# ── Passo 5: Testar ─────────────────────────────────────────────
echo -e "${YELLOW}[5/5] Testando...${NC}"
echo ""
echo -e "   ${CYAN}🧪 Teste rápido:${NC}"
RESPOSTA=$(ollama run "${MODELO}" "Responda em português em no máximo 15 palavras: quem é você?" 2>/dev/null)
echo -e "   ${GREEN}🦾 Gus: ${RESPOSTA}${NC}"
echo ""

# ── Criar atalho ────────────────────────────────────────────────
mkdir -p ~/gus-local
cat > ~/gus-local/gus_chat.py << 'PYEOF'
#!/usr/bin/env python3
"""Gus Local — Chat interativo com IA local (Ollama)"""
import requests, json, sys, os
from datetime import datetime

MODEL = os.getenv("GUS_MODEL", "gemma3:4b")
OLLAMA = "http://localhost:11434/api/chat"

SYSTEM = """Você é o Gus, agente pessoal do Gustavo Pratti de Barros.
Responda em português brasileiro, de forma direta, informal e útil.
Você tem acesso a memória (Hub Qdrant) e pode ajudar com tarefas diárias,
pesquisa, código, e conversas. Seja conciso — respostas curtas e diretas."""

def chat():
    print("🦾 Gus Local —", MODEL)
    print("   Digite 'sair' para encerrar, 'limpar' para resetar\n")
    msgs = [{"role": "system", "content": SYSTEM}]
    
    while True:
        try:
            user = input("> Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais!")
            break
        
        if not user: continue
        if user.lower() in ("sair","exit","q"): print("Até mais!"); break
        if user.lower() in ("limpar","clear"):
            msgs = [{"role": "system", "content": SYSTEM}]
            print("🧹 Limpo!\n"); continue
        
        msgs.append({"role": "user", "content": user})
        
        # Mantém últimas 12 mensagens
        recent = [msgs[0]] + msgs[-11:] if len(msgs) > 12 else msgs
        
        try:
            t0 = datetime.now()
            r = requests.post(OLLAMA, json={
                "model": MODEL, "messages": recent, "stream": False,
                "options": {"temperature": 0.7, "num_predict": 300}
            }, timeout=120)
            data = r.json()
            resposta = data.get("message",{}).get("content","")
            elapsed = (datetime.now()-t0).total_seconds()
            
            print(f"\n🦾 Gus: {resposta}")
            print(f"   ({elapsed:.1f}s, {data.get('eval_count','?')} tokens)\n")
            msgs.append({"role": "assistant", "content": resposta})
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            print("   Ollama está rodando? Execute: ollama serve\n")

if __name__ == "__main__":
    chat()
PYEOF

# ── Atalho ───────────────────────────────────────────────────────
cat > ~/gus-local/iniciar.sh << 'SHEOF'
#!/bin/bash
# Inicia o Gus Local
cd ~/gus-local

# Garante que Ollama está rodando
if ! pgrep ollama > /dev/null; then
    echo "Iniciando Ollama..."
    ollama serve &
    sleep 3
fi

python3 gus_chat.py
SHEOF
chmod +x ~/gus-local/iniciar.sh

# ── Finalizado ───────────────────────────────────────────────────
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}   ✅ GUS LOCAL INSTALADO COM SUCESSO!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "   📁 Pasta: ${CYAN}~/gus-local/${NC}"
echo -e ""
echo -e "   🚀 Para iniciar:"
echo -e "      ${CYAN}cd ~/gus-local && bash iniciar.sh${NC}"
echo -e ""
echo -e "   🧪 Para testar rápido:"
echo -e "      ${CYAN}ollama run ${MODELO} 'Olá Gus!'${NC}"
echo ""
echo -e "   📱 Pronto! Gus rodando 100% offline no seu S20."
echo ""
