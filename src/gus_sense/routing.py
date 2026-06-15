"""Roteamento de modelo — rota local obrigatória pra dado sensível (fail-closed).

Bloco 3. Espelha a decisão fail-closed do MCP do Gus: dado sensível só é
processado por modelo local (Gemma). Se o local estiver indisponível, BLOQUEIA —
nunca cai pra nuvem.
"""
from __future__ import annotations

from typing import Callable, Literal

from .schema import SENSITIVE_AREAS, Fragmento

Rota = Literal["local", "cloud"]


class RotaBloqueada(Exception):
    """Dado sensível exige modelo local, mas ele está indisponível."""


def is_sensivel(frag: Fragmento) -> bool:
    return bool(frag.metadata.get("sensivel")) or frag.area in SENSITIVE_AREAS


def route(frag: Fragmento, local_disponivel: Callable[[], bool] | bool = False) -> Rota:
    """Decide a rota de processamento de um fragmento.

    - sensível -> "local" (e exige modelo local; senão RotaBloqueada — fail-closed)
    - caso contrário -> "cloud"
    """
    disponivel = local_disponivel() if callable(local_disponivel) else bool(local_disponivel)
    if is_sensivel(frag):
        if not disponivel:
            raise RotaBloqueada(
                "dado sensível e modelo local indisponível — bloqueado (fail-closed)"
            )
        return "local"
    return "cloud"
