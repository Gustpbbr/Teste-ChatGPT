"""
Gus Local — Servidor Unificado
===============================
Gus completo offline: Ollama + memória local + interface web.

Executar:
    python3 server.py

Dependências:
    pip install fastapi uvicorn ollama
    ollama pull gemma3:4b
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from memory import lembrar, recordar, contexto_set, contexto_get, stats as mem_stats

# ── Config ──────────────────────────────────────────────────────
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("GUS_MODEL", "gemma3:4b")
PORT = int(os.getenv("GUS_PORT", "8080"))

app = FastAPI(title="Gus Local", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SYSTEM_PATH = Path(__file__).parent.parent.parent / "Gus" / "gus" / "system_prompt.md"

def _load_system() -> str:
    if SYSTEM_PATH.exists():
        sp = SYSTEM_PATH.read_text(encoding="utf-8")
        if len(sp) > 4000:
            sp = sp[:4000] + "\n\n[system prompt truncado — executando offline com memória local]"
        return sp
    return (
        "Você é o Gus, agente pessoal do Gustavo Pratti de Barros. "
        "Responda em português brasileiro, direto e informal. "
        "Você tem memória local persistente (SQLite) e roda 100% offline."
    )

SYSTEM = _load_system()


# ── Schemas ──────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    messages: list[dict]
    save_memory: bool = True


class MemoryRequest(BaseModel):
    texto: str
    tipo: str = "fragmento"
    tags: list[str] = []
    importancia: float = 0.5


class ConfigRequest(BaseModel):
    chave: str
    valor: str


# ── Helpers ──────────────────────────────────────────────────────
def _build_context(query: str) -> str:
    """Busca memórias relevantes e monta contexto pro modelo."""
    memorias = recordar(query=query, limite=5)
    if not memorias:
        return ""
    ctx = ["\n\n--- MEMÓRIAS RELEVANTES ---"]
    for m in memorias:
        ctx.append(f"[{m['tipo']}] {m['texto'][:300]}")
    return "\n".join(ctx)


def _extract_memories(user_msg: str, assistant_msg: str):
    """Extrai fatos importantes da conversa e salva como memórias."""
    # Salva a interação
    resumo = f"Usuário: {user_msg[:200]}\nGus: {assistant_msg[:200]}"
    lembrar(resumo, tipo="dialogo", tags=["chat"], importancia=0.3)
    
    # Tenta extrair fatos com prompt simples
    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat", json={
            "model": MODEL, "stream": False,
            "messages": [
                {"role": "system", "content": (
                    "Extraia 1-3 fatos importantes desta conversa. "
                    "Responda APENAS com JSON: [{\"fato\":\"...\", \"tipo\":\"...\"}]. "
                    "Tipos: preferencia, projeto, pessoa, tarefa, nota."
                )},
                {"role": "user", "content": f"Usuário: {user_msg[:500]}\n\nGus: {assistant_msg[:300]}"}
            ],
            "options": {"temperature": 0.3, "num_predict": 200}
        }, timeout=30)
        data = r.json()
        text = data.get("message", {}).get("content", "")
        
        # Parse do JSON (pode vir com markdown)
        import re
        json_match = re.search(r'\[[\s\S]*\]', text)
        if json_match:
            fatos = json.loads(json_match.group())
            for f in fatos:
                if isinstance(f, dict) and "fato" in f:
                    lembrar(
                        f["fato"], tipo=f.get("tipo", "nota"),
                        tags=["extraido"], importancia=0.6
                    )
    except:
        pass  # extração de memória é best-effort


# ── Endpoints ────────────────────────────────────────────────────
@app.get("/health")
async def health():
    """Status do Gus Local."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        ollama_ok = r.status_code == 200
    except:
        ollama_ok = False
    
    return {
        "status": "ok" if ollama_ok else "degraded",
        "ollama": ollama_ok,
        "model": MODEL,
        "memory": mem_stats(),
    }


@app.post("/chat")
async def chat(req: ChatRequest):
    """Chat com o Gus (com memória)."""
    try:
        r_ollama = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if r_ollama.status_code != 200:
            raise HTTPException(503, "Ollama offline")
    except:
        raise HTTPException(503, "Ollama offline. Execute: ollama serve")
    
    messages = [{"role": "system", "content": SYSTEM}]
    
    # Injeta memórias relevantes no contexto
    last_user = next((m["content"] for m in reversed(req.messages) if m["role"] == "user"), "")
    if last_user:
        contexto = _build_context(last_user)
        if contexto:
            messages.append({"role": "system", "content": contexto})
    
    messages.extend(req.messages[-10:])  # últimas 10 mensagens
    
    t0 = time.time()
    
    r = requests.post(f"{OLLAMA_URL}/api/chat", json={
        "model": MODEL, "messages": messages, "stream": False,
        "options": {"temperature": 0.7, "num_predict": 500}
    }, timeout=120)
    
    data = r.json()
    resposta = data.get("message", {}).get("content", "")
    elapsed = time.time() - t0
    
    # Salva memória
    if req.save_memory and last_user and resposta:
        _extract_memories(last_user, resposta)
    
    return {
        "model": MODEL,
        "content": resposta,
        "elapsed_s": round(elapsed, 2),
        "tokens_in": data.get("prompt_eval_count", 0),
        "tokens_out": data.get("eval_count", 0),
    }


@app.post("/memory/add")
async def memory_add(req: MemoryRequest):
    """Adiciona memória manualmente."""
    mid = lembrar(req.texto, tipo=req.tipo, tags=req.tags, importancia=req.importancia)
    return {"id": mid, "status": "ok"}


@app.get("/memory/search")
async def memory_search(q: str = "", tipo: str = "", limite: int = 10):
    """Busca memórias."""
    results = recordar(query=q or None, tipo=tipo or None, limite=limite)
    return {"query": q, "total": len(results), "results": results}


@app.get("/memory/stats")
async def memory_stats():
    """Estatísticas da memória."""
    return mem_stats()


@app.post("/config")
async def config_set(req: ConfigRequest):
    """Define configuração (persiste localmente)."""
    contexto_set(req.chave, req.valor)
    return {"status": "ok", "chave": req.chave}


@app.get("/config/{chave}")
async def config_get(chave: str):
    """Recupera configuração."""
    valor = contexto_get(chave)
    if valor is None:
        raise HTTPException(404, f"Config '{chave}' não encontrada")
    return {"chave": chave, "valor": valor}


# ── Página Web ───────────────────────────────────────────────────
@app.get("/")
async def index():
    """Interface web do Gus Local."""
    return {"name": "Gus Local", "version": "1.0", "docs": "/docs", "endpoints": {
        "chat": "POST /chat",
        "memory_add": "POST /memory/add",
        "memory_search": "GET /memory/search?q=termo",
        "memory_stats": "GET /memory/stats",
        "config": "POST /config + GET /config/{chave}",
        "health": "GET /health",
    }}


if __name__ == "__main__":
    import uvicorn
    print(f"""
╔══════════════════════════════════════════╗
║   🦾 GUS LOCAL v1.0                       ║
║   Modelo: {MODEL:<30} ║
║   Memória: SQLite local                   ║
║   🌐 http://localhost:{PORT}                  ║
╚══════════════════════════════════════════╝
""")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
