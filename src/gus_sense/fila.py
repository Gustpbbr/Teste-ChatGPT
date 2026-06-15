"""A5 — Fila de pendentes: reenvia sozinha quando o Hub volta.

Quando o HubClient devolve "pendente" (Hub fora), o fragmento entra aqui e é
reenviado no próximo replay em que o Hub estiver saudável. Idempotência simples
por contagem; storage injetável pra testar.
"""
from __future__ import annotations

from dataclasses import dataclass

from .hub_client import HubClient
from .schema import Fragmento


@dataclass
class ReplayResult:
    enviados: int
    restantes: int


class FilaPendentes:
    def __init__(self, store: list[Fragmento] | None = None) -> None:
        self._itens: list[Fragmento] = store if store is not None else []

    def enfileirar(self, frag: Fragmento) -> None:
        self._itens.append(frag)

    def pendentes(self) -> list[Fragmento]:
        return list(self._itens)

    def replay(self, hub: HubClient) -> ReplayResult:
        """Reenvia a fila se o Hub estiver saudável. Mantém os que falharem."""
        if not hub.health():
            return ReplayResult(enviados=0, restantes=len(self._itens))

        restantes: list[Fragmento] = []
        enviados = 0
        for frag in self._itens:
            if hub.ingestar(frag).status == "ok":
                enviados += 1
            else:
                restantes.append(frag)
        self._itens = restantes
        return ReplayResult(enviados=enviados, restantes=len(restantes))


def ingestar_com_fila(hub: HubClient, fila: FilaPendentes, frag: Fragmento) -> str:
    """Tenta ingerir; se vier 'pendente', enfileira pra replay. Retorna o status."""
    res = hub.ingestar(frag)
    if res.status != "ok":
        fila.enfileirar(frag)
    return res.status
