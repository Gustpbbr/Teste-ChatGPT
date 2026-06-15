"""Cliente fino do Hub Qdrant do Gus. DEGRADÁVEL por contrato.

Território: T-HUB (tarefa T2).
Regra: Hub fora NUNCA derruba o chamador. Retorna resultado "pendente".
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .schema import Fragmento

IngestStatus = Literal["ok", "pendente", "erro"]


@dataclass
class IngestResult:
    status: IngestStatus
    id: str | None = None
    detalhe: str = ""


class HubClient:
    """Wrapper de I/O com o Hub. Endpoints reusam o Gus existente.

    Config via env (ver .env.example): HUB_URL, HUB_TOKEN.
    """

    def __init__(self, url: str | None = None, token: str | None = None) -> None:
        # TODO(T2): ler env, montar sessão HTTP.
        self.url = url
        self.token = token

    def ingestar(self, frag: Fragmento) -> IngestResult:
        """Escreve um fragmento no Hub.

        Retry com backoff exponencial (2/4/8/16s). Se esgotar/Hub fora:
        retorna IngestResult(status="pendente") — NÃO levanta exceção fatal.
        """
        # TODO(T2)
        raise NotImplementedError("T2")

    def health(self) -> bool:
        """True se o Hub responde. Nunca levanta — em dúvida, False."""
        # TODO(T2)
        raise NotImplementedError("T2")

    def ultima_escrita(self) -> object | None:
        """Timestamp da última escrita conhecida (para interocepção)."""
        # TODO(T2)
        raise NotImplementedError("T2")
