#!/usr/bin/env python3
"""
FASE 0 — Prova de Conceito: Gus offline com IA local
=====================================================
Objetivo: Provar que o Gus funciona com modelo local (Gemma 1B via Ollama),
          sem internet, sem API externa, mantendo a identidade do system prompt.

Pré-requisitos:
  1. Ollama instalado e rodando (ollama serve)
  2. Modelo baixado: ollama pull gemma3:1b
  3. Python 3.10+

Uso:
  python3 fase0_gus_local.py
  > Digite sua mensagem (ou 'sair'): Gus, como você está?
  > Gus: [resposta offline do Gemma]
"""

import subprocess
import sys
import os
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────
MODEL = "gemma3:1b"          # Modelo local via Ollama
GUS_SYSTEM_PROMPT = Path(__file__).parent.parent.parent / "Gus" / "gus" / "system_prompt.md"

# ── Carrega o system prompt do Gus ────────────────────────────────
def carregar_system_prompt() -> str:
    if GUS_SYSTEM_PROMPT.exists():
        sp = GUS_SYSTEM_PROMPT.read_text(encoding="utf-8")
        # Trunca se for muito grande pro modelo pequeno
        if len(sp) > 3000:
            sp = sp[:3000] + "\n\n[... system prompt truncado para caber no Gemma 1B ...]"
        return sp
    # Fallback mínimo se o arquivo não existir
    return (
        "Você é o Gus, o agente pessoal do Gustavo Pratti de Barros. "
        "Responda em português brasileiro, de forma direta e informal. "
        "Você tem acesso à memória, ferramentas e pode ajudar com tarefas do dia a dia."
    )

# ── Geração via Ollama ────────────────────────────────────────────
def gerar_resposta_local(messages: list[dict], system: str) -> tuple[str, dict]:
    """Chama Ollama local com histórico de mensagens + system prompt."""
    
    # Ollama API: POST /api/chat
    import json
    import urllib.request
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            *messages,
        ],
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 512,  # tokens máximos
        }
    }
    
    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    
    t0 = __import__("time").time()
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        
        elapsed = __import__("time").time() - t0
        text = result.get("message", {}).get("content", "")
        metadata = {
            "model": result.get("model", MODEL),
            "tokens_in": result.get("prompt_eval_count", 0),
            "tokens_out": result.get("eval_count", 0),
            "elapsed_s": round(elapsed, 1),
            "provider": "ollama-local",
        }
        return text, metadata
    
    except Exception as e:
        return f"Erro ao chamar Ollama: {e}", {"error": str(e)}


# ── Interface interativa ──────────────────────────────────────────
def main():
    print("=" * 60)
    print("🦾 FASE 0 — Gus Local (Gemma 1B via Ollama)")
    print(f"   Modelo: {MODEL}")
    print(f"   Status: OFFLINE (sem APIs externas)")
    print("=" * 60)
    
    system_sp = carregar_system_prompt()
    print(f"\n📋 System prompt carregado: {len(system_sp)} caracteres")
    
    # Quick test de conectividade com Ollama
    try:
        import urllib.request
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5)
        print("✅ Ollama respondendo\n")
    except:
        print("❌ Ollama não está rodando. Execute: ollama serve\n")
        return
    
    history: list[dict] = []
    
    print("Digite sua mensagem ('sair' para encerrar, 'limpar' para resetar)\n")
    
    while True:
        try:
            user_input = input("> Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais!")
            break
        
        if not user_input:
            continue
        if user_input.lower() in ("sair", "exit", "q"):
            print("Até mais!")
            break
        if user_input.lower() in ("limpar", "clear"):
            history = []
            print("🧹 Histórico limpo.\n")
            continue
        
        history.append({"role": "user", "content": user_input})
        
        # Mantém só as últimas 10 mensagens pra não estourar contexto
        recent = history[-10:]
        
        print("⏳ Pensando...", end=" ", flush=True)
        resposta, meta = gerar_resposta_local(recent, system_sp)
        print(f"({meta.get('elapsed_s', '?')}s, {meta.get('tokens_out', '?')} tokens)")
        
        print(f"\n🦾 Gus: {resposta}\n")
        history.append({"role": "assistant", "content": resposta})


if __name__ == "__main__":
    main()
