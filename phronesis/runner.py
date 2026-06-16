#!/usr/bin/env python3
"""
Phronesis-Bench: Runner Multi-Modelo
=====================================
Testa múltiplos LLMs com o mesmo corpus e gera resultados comparativos.

Uso:
    export ANTHROPIC_API_KEY="sk-ant-..."
    export OPENAI_API_KEY="sk-..."
    export GOOGLE_API_KEY="..."
    python3 runner.py

Output:
    results/results.json — dados brutos
    results/summary.md  — tabela comparativa
"""

import os
import json
import time
import asyncio
from pathlib import Path
from typing import Optional

from corpora import CORPORA, ALL_ITEMS
from metrics import avaliar_resposta

OUTPUT_DIR = Path(__file__).parent / "results"

# ── Modelos a testar ──────────────────────────────────────────────
MODEL_CONFIGS = [
    {
        "provider": "anthropic",
        "model": "claude-fable-5-20250610",
        "label": "Claude Fable 5",
        "env_key": "ANTHROPIC_API_KEY",
    },
    {
        "provider": "anthropic",
        "model": "claude-sonnet-4-6-20250521",
        "label": "Claude Sonnet 4.6",
        "env_key": "ANTHROPIC_API_KEY",
    },
    {
        "provider": "anthropic",
        "model": "claude-opus-4-8-20250528",
        "label": "Claude Opus 4.8",
        "env_key": "ANTHROPIC_API_KEY",
    },
    {
        "provider": "openai",
        "model": "gpt-4o",
        "label": "GPT-4o",
        "env_key": "OPENAI_API_KEY",
    },
    {
        "provider": "google",
        "model": "gemini-2.5-pro",
        "label": "Gemini 2.5 Pro",
        "env_key": "GOOGLE_API_KEY",
    },
]


async def test_anthropic(model: str, system: str, prompt: str) -> Optional[str]:
    try:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        resp = await client.messages.create(
            model=model, max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in resp.content if b.type == "text")
    except Exception as e:
        return f"ERRO: {e}"


async def test_openai(model: str, system: str, prompt: str) -> Optional[str]:
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = await client.chat.completions.create(
            model=model, max_tokens=1024,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"ERRO: {e}"


async def test_google(model: str, system: str, prompt: str) -> Optional[str]:
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        mdl = genai.GenerativeModel(model)
        full_prompt = f"{system}\n\n{prompt}"
        resp = mdl.generate_content(full_prompt)
        return resp.text
    except Exception as e:
        return f"ERRO: {e}"


async def test_model(config: dict, item: tuple, sem: asyncio.Semaphore) -> dict:
    """Testa um modelo com um item do corpus."""
    grupo, data = item
    
    t0 = time.time()
    
    match config["provider"]:
        case "anthropic":
            resposta = await test_anthropic(
                config["model"], data["system"], data["prompt"])
        case "openai":
            resposta = await test_openai(
                config["model"], data["system"], data["prompt"])
        case "google":
            resposta = await test_google(
                config["model"], data["system"], data["prompt"])
        case _:
            resposta = f"Provider desconhecido: {config['provider']}"
    
    elapsed = time.time() - t0
    
    if resposta and not resposta.startswith("ERRO:"):
        scores = avaliar_resposta(
            resposta, data["categoria"],
            data["resposta_esperada"], data["rubrica"]
        )
    else:
        scores = {"ACC": 0, "ECE": 0, "CS": 0, "RAS": 0, "PPS": 0, "error": resposta}
    
    return {
        "model": config["label"],
        "provider": config["provider"],
        "model_id": config["model"],
        "item_id": data["id"],
        "grupo": grupo,
        "categoria": data["categoria"],
        "prompt": data["prompt"][:100],
        "resposta": (resposta or "")[:500],
        "scores": scores,
        "elapsed_s": round(elapsed, 2),
    }


def generate_summary(results: list[dict]) -> str:
    """Gera resumo em markdown."""
    # Agrupa por modelo
    by_model = {}
    for r in results:
        m = r["model"]
        if m not in by_model:
            by_model[m] = {g: [] for g in CORPORA}
        by_model[m][r["grupo"]].append(r["scores"].get("PPS", 0))
    
    lines = [
        "# Phronesis-Bench — Resultados",
        f"Data: {time.strftime('%Y-%m-%d %H:%M')}",
        f"Itens testados: {len(results)}",
        "",
        "## Sumário por Modelo",
        "",
        "| Modelo | PPS Geral |",
        "|--------|-----------|",
    ]
    
    for model, grupos in sorted(by_model.items()):
        todas = [s for gl in grupos.values() for s in gl if s > 0]
        if todas:
            pps_geral = sum(todas) / len(todas)
            lines.append(f"| {model} | {pps_geral:.3f} |")
    
    lines += [
        "",
        "## Por Grupo de Corpus",
        "",
        "| Modelo | " + " | ".join(CORPORA.keys()) + " |",
        "|--------|" + "|".join(["------" for _ in CORPORA]) + "|",
    ]
    
    for model, grupos in sorted(by_model.items()):
        medias = []
        for g in CORPORA:
            vals = [s for s in grupos[g] if s > 0]
            avg = sum(vals) / len(vals) if vals else 0
            medias.append(f"{avg:.3f}")
        lines.append(f"| {model} | " + " | ".join(medias) + " |")
    
    lines += [
        "",
        "## Métricas Individuais",
        "",
        "| Modelo | ACC | ECE | CS | RAS | PPS |",
        "|--------|-----|-----|-----|-----|-----|",
    ]
    
    by_model_metrics = {}
    for r in results:
        m = r["model"]
        if m not in by_model_metrics:
            by_model_metrics[m] = {"ACC": [], "ECE": [], "CS": [], "RAS": [], "PPS": []}
        for k in ["ACC", "ECE", "CS", "RAS", "PPS"]:
            v = r["scores"].get(k, 0)
            if v > 0:
                by_model_metrics[m][k].append(v)
    
    for model, metrics in sorted(by_model_metrics.items()):
        avgs = {}
        for k in ["ACC", "ECE", "CS", "RAS", "PPS"]:
            vals = metrics[k]
            avgs[k] = sum(vals) / len(vals) if vals else 0
        lines.append(
            f"| {model} | {avgs['ACC']:.3f} | {avgs['ECE']:.3f} | "
            f"{avgs['CS']:.3f} | {avgs['RAS']:.3f} | {avgs['PPS']:.3f} |"
        )
    
    return "\n".join(lines)


async def main():
    print("🧠 Phronesis-Bench — Runner Multi-Modelo")
    print(f"   Corpora: {len(CORPORA)} grupos, {len(ALL_ITEMS)} itens")
    print(f"   Modelos: {len(MODEL_CONFIGS)}")
    print()
    
    # Filtra modelos com API key disponível
    available = []
    for cfg in MODEL_CONFIGS:
        if os.getenv(cfg["env_key"]):
            available.append(cfg)
            print(f"   ✅ {cfg['label']} ({cfg['provider']})")
        else:
            print(f"   ⚠️ {cfg['label']} — sem API key ({cfg['env_key']})")
    
    if not available:
        print("\n❌ Nenhum modelo disponível. Configure as API keys.")
        return
    
    total = len(available) * len(ALL_ITEMS)
    print(f"\n⏳ Rodando {total} testes...\n")
    
    sem = asyncio.Semaphore(2)
    tasks = [test_model(cfg, item, sem) for cfg in available for item in ALL_ITEMS]
    results = await asyncio.gather(*tasks)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Salva JSON
    output = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "models_tested": [c["label"] for c in available],
        "total_items": len(ALL_ITEMS),
        "results": results,
    }
    json_path = OUTPUT_DIR / "results.json"
    json_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    
    # Gera resumo
    summary = generate_summary(results)
    md_path = OUTPUT_DIR / "summary.md"
    md_path.write_text(summary)
    
    print(summary)
    print(f"\n📁 Dados completos: {json_path}")
    print(f"📄 Resumo: {md_path}")


if __name__ == "__main__":
    asyncio.run(main())
