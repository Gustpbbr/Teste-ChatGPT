"""
MGE/CEX — Microserviço FastAPI
===============================
Motor de Geração Estruturada + Comitê de Especialistas Universais.
Versão API (substitui os HTML standalone).

Executar:
    pip install fastapi uvicorn anthropic
    export ANTHROPIC_API_KEY="sk-ant-..."
    uvicorn server:app --host 0.0.0.0 --port 8765

Endpoints:
    POST /mge/generate    — Geração estruturada multi-agente
    POST /cex/review      — Cross-examination por comitê
    GET  /health          — Status do serviço
"""

import os
import json
import asyncio
import time
from typing import Optional
from dataclasses import dataclass, field

import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ── Config ──────────────────────────────────────────────────────
app = FastAPI(title="MGE/CEX API", version="2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MODEL_DEFAULT = os.getenv("MGE_MODEL", "claude-sonnet-4-6-20250521")
MAX_TOKENS = int(os.getenv("MGE_MAX_TOKENS", "2048"))
client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# ── Schemas ──────────────────────────────────────────────────────
class MGERequest(BaseModel):
    prompt: str = Field(..., description="Tema ou pergunta para geração")
    num_agentes: int = Field(default=5, ge=1, le=10)
    max_tokens_resposta: int = Field(default=800)
    modelo: Optional[str] = None


class CEXRequest(BaseModel):
    texto: str = Field(..., description="Texto a ser examinado pelo comitê")
    criterios: list[str] = Field(default=["factual", "logico", "etico", "clareza"])
    modelo: Optional[str] = None


class JobStatus(BaseModel):
    job_id: str
    status: str = "pending"
    elapsed_s: float = 0
    resultado: Optional[dict] = None


# ── MGE: Agentes Especialistas ───────────────────────────────────
MGE_AGENTS = {
    "criativo": "Você é um especialista criativo. Gere ideias originais, divergentes e surpreendentes. Evite clichês. Pense lateralmente.",
    "critico": "Você é um crítico analítico. Avalie rigorosamente, identifique falhas, contradições e fraquezas. Seja honesto, mesmo que duro.",
    "sintetizador": "Você é um sintetizador. Integre múltiplas perspectivas em uma visão coerente. Encontre padrões e conexões entre ideias díspares.",
    "pratico": "Você é um especialista prático. Foque em viabilidade, implementação, recursos necessários. O que funciona no mundo real?",
    "etico": "Você é um consultor ético. Avalie implicações morais, justiça, equidade, impacto social. Identifique riscos éticos e sugira mitigação.",
    "tecnico": "Você é um especialista técnico. Analise com profundidade técnica, precisão e rigor. Fundamente em dados e evidências.",
    "empatico": "Você é um especialista em experiência humana. Considere o impacto emocional, psicológico e relacional. Como isso afeta as pessoas?",
    "estrategista": "Você é um estrategista. Pense em longo prazo, tendências, cenários. Qual a visão de futuro e os passos para chegar lá?",
    "curador": "Você é um curador de conhecimento. Selecione o melhor de cada perspectiva, descarte o redundante, preserve o essencial. Qualidade sobre quantidade.",
    "provocador": "Você é um provocador intelectual. Questione premissas, desafie o status quo, proponha alternativas radicais. E se o oposto fosse verdade?",
}


async def _call_agent(name: str, system_extra: str, prompt: str, model: str) -> dict:
    """Chama um agente especialista."""
    system = f"{system_extra}\n\nResponda em português brasileiro. Seja conciso — máximo 3 parágrafos."
    try:
        resp = await client.messages.create(
            model=model, max_tokens=800,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in resp.content if b.type == "text")
        return {"agente": name, "resposta": text, "status": "ok"}
    except Exception as e:
        return {"agente": name, "resposta": str(e), "status": "error"}


async def _synthesize(agent_outputs: list[dict], prompt: str, model: str) -> str:
    """Sintetiza outputs dos agentes em uma resposta final."""
    partes = "\n\n---\n\n".join(
        f"### {a['agente'].upper()}\n{a['resposta'][:500]}"
        for a in agent_outputs if a["status"] == "ok"
    )
    system = (
        "Você é um sintetizador master. Integre as perspectivas abaixo em uma "
        "resposta final coerente, destacando convergências, divergências produtivas "
        "e insights originais. Responda em português brasileiro, 4-5 parágrafos."
    )
    resp = await client.messages.create(
        model=model, max_tokens=1200,
        system=system,
        messages=[{"role": "user", "content": f"Tema: {prompt}\n\nPerspectivas:\n{partes}"}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


# ── CEX: Comitê de Cross-Examination ─────────────────────────────
CEX_CHECKLISTS = {
    "factual": "Verifique a precisão factual. Identifique afirmações não fundamentadas, dados incorretos, fontes ausentes. Cada problema encontrado: explique e sugira correção.",
    "logico": "Verifique a coerência lógica. Identifique contradições, falácias, saltos argumentativos, premissas não declaradas. Avalie a solidez do raciocínio.",
    "etico": "Verifique implicações éticas. Identifique vieses, preconceitos, danos potenciais, grupos afetados. Avalie justiça, equidade e responsabilidade.",
    "clareza": "Verifique clareza e comunicação. Identifique ambiguidades, jargão desnecessário, estruturas confusas. O texto é compreensível para o público-alvo?",
    "criativo": "Verifique originalidade. Identifique clichês, lugares-comuns, pensamento convergente previsível. Há ideias genuinamente novas?",
    "tecnico": "Verifique rigor técnico. Identifique imprecisões, simplificações excessivas, erros conceituais. O tratamento técnico é adequado à complexidade do tema?",
}

CEX_SYNTHESIS = (
    "Você é um editor-chefe. Com base nas revisões abaixo, produza uma versão revisada "
    "do texto original que incorpore as correções necessárias e melhore a qualidade geral. "
    "Mantenha o tom e o estilo do original, mas corrija problemas identificados. "
    "Responda em português brasileiro."
)


async def _review_dimension(texto: str, dimensao: str, criterio: str, model: str) -> dict:
    """Revisa o texto em uma dimensão específica."""
    try:
        resp = await client.messages.create(
            model=model, max_tokens=600,
            system=f"Você é um revisor especializado em: {dimensao}. {criterio}",
            messages=[{"role": "user", "content": f"Analise:\n\n{texto}"}],
        )
        review = "".join(b.text for b in resp.content if b.type == "text")
        return {"dimensao": dimensao, "review": review, "status": "ok"}
    except Exception as e:
        return {"dimensao": dimensao, "review": str(e), "status": "error"}


# ── Endpoints ────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL_DEFAULT, "provider": "anthropic"}


@app.post("/mge/generate")
async def mge_generate(req: MGERequest):
    """Geração estruturada multi-agente."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise HTTPException(500, "ANTHROPIC_API_KEY não configurada")
    
    model = req.modelo or MODEL_DEFAULT
    agentes = list(MGE_AGENTS.items())[:req.num_agentes]
    
    t0 = time.time()
    
    # Fase 1: Agentes em paralelo
    tasks = [_call_agent(name, sys, req.prompt, model) for name, sys in agentes]
    outputs = await asyncio.gather(*tasks)
    
    # Fase 2: Síntese
    sintese = await _synthesize(outputs, req.prompt, model)
    
    elapsed = time.time() - t0
    
    return {
        "modelo": model,
        "num_agentes": req.num_agentes,
        "elapsed_s": round(elapsed, 2),
        "agentes": [
            {"nome": a["agente"], "status": a["status"], "resumo": a["resposta"][:200]}
            for a in outputs
        ],
        "sintese": sintese,
    }


@app.post("/cex/review")
async def cex_review(req: CEXRequest):
    """Cross-examination por comitê de especialistas."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise HTTPException(500, "ANTHROPIC_API_KEY não configurada")
    
    model = req.modelo or MODEL_DEFAULT
    criterios = {k: v for k, v in CEX_CHECKLISTS.items() if k in req.criterios}
    
    t0 = time.time()
    
    # Fase 1: Revisão paralela em múltiplas dimensões
    tasks = [_review_dimension(req.texto, dim, crit, model) for dim, crit in criterios.items()]
    reviews = await asyncio.gather(*tasks)
    
    # Fase 2: Síntese da revisão
    partes = "\n\n---\n\n".join(
        f"### {r['dimensao'].upper()}\n{r['review']}"
        for r in reviews if r["status"] == "ok"
    )
    
    resp = await client.messages.create(
        model=model, max_tokens=1500,
        system=CEX_SYNTHESIS,
        messages=[{"role": "user", "content": f"TEXTO ORIGINAL:\n{req.texto}\n\nREVISÕES:\n{partes}"}],
    )
    texto_revisado = "".join(b.text for b in resp.content if b.type == "text")
    
    elapsed = time.time() - t0
    
    return {
        "modelo": model,
        "dimensoes_revisadas": list(criterios.keys()),
        "elapsed_s": round(elapsed, 2),
        "reviews": [
            {"dimensao": r["dimensao"], "status": r["status"], "resumo": r["review"][:200]}
            for r in reviews
        ],
        "texto_revisado": texto_revisado,
    }


if __name__ == "__main__":
    import uvicorn
    print(f"🚀 MGE/CEX API v2.0 — http://localhost:8765")
    print(f"   Modelo: {MODEL_DEFAULT}")
    print(f"   Endpoints: /health, /mge/generate, /cex/review")
    uvicorn.run(app, host="0.0.0.0", port=8765)
