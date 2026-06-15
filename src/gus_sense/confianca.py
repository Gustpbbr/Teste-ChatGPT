"""A3 — Confiança/proveniência: trust score por fragmento + ajuste por feedback.

Base da explicabilidade da proatividade. Trust parte da `confianca` do fragmento
e sobe/cai conforme confirmações e refutações registradas no metadata.
"""
from __future__ import annotations

from .schema import Fragmento

_PASSO_CONFIRMA = 0.1
_PASSO_REFUTA = 0.2


def trust(frag: Fragmento) -> float:
    """Confiança efetiva em [0,1]: base + confirmações - refutações."""
    c = int(frag.metadata.get("confirmacoes", 0))
    r = int(frag.metadata.get("refutacoes", 0))
    val = frag.confianca + _PASSO_CONFIRMA * c - _PASSO_REFUTA * r
    return max(0.0, min(1.0, val))


def confirmar(frag: Fragmento) -> Fragmento:
    """Registra uma confirmação (o dado se mostrou certo)."""
    frag.metadata["confirmacoes"] = int(frag.metadata.get("confirmacoes", 0)) + 1
    return frag


def refutar(frag: Fragmento) -> Fragmento:
    """Registra uma refutação (o dado se mostrou errado)."""
    frag.metadata["refutacoes"] = int(frag.metadata.get("refutacoes", 0)) + 1
    return frag


def proveniencia(frag: Fragmento) -> str:
    """Texto curto de proveniência, pra explicabilidade ('de onde veio')."""
    return f"via={frag.via} · {frag.tipo} · trust={trust(frag):.2f}"
