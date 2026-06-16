#!/usr/bin/env python3
"""
MGE/CEX API — Teste rápido
============================
Testa os endpoints do microserviço localmente.

Uso:
    python3 test_client.py
"""

import requests
import json
import sys

BASE = "http://localhost:8765"


def test_health():
    r = requests.get(f"{BASE}/health")
    print(f"✅ Health: {r.json()}")


def test_mge():
    data = {
        "prompt": "Proponha 3 ideias inovadoras para usar IA em educação médica.",
        "num_agentes": 3,
    }
    print(f"⏳ MGE: gerando com {data['num_agentes']} agentes...")
    r = requests.post(f"{BASE}/mge/generate", json=data)
    result = r.json()
    print(f"   Modelo: {result['modelo']}")
    print(f"   Tempo: {result['elapsed_s']}s")
    print(f"   Agentes: {[a['nome'] for a in result['agentes']]}")
    print(f"   Síntese: {result['sintese'][:300]}...")
    return result


def test_cex():
    texto = (
        "A inteligência artificial vai substituir todos os médicos em 5 anos. "
        "Estudos mostram que IA já é mais precisa que humanos em 100% dos diagnósticos. "
        "Não há nenhum risco nessa transição."
    )
    data = {"texto": texto, "criterios": ["factual", "logico", "etico"]}
    print(f"⏳ CEX: revisando com {len(data['criterios'])} dimensões...")
    r = requests.post(f"{BASE}/cex/review", json=data)
    result = r.json()
    print(f"   Dimensões: {result['dimensoes_revisadas']}")
    print(f"   Tempo: {result['elapsed_s']}s")
    print(f"   Revisado: {result['texto_revisado'][:300]}...")
    return result


if __name__ == "__main__":
    print("🧪 Testando MGE/CEX API\n")
    
    try:
        test_health()
        mge = test_mge()
        cex = test_cex()
        print("\n✅ Todos os testes passaram!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("Certifique-se de que o servidor está rodando:")
        print("   cd mge_cex_api && uvicorn server:app --port 8765")
