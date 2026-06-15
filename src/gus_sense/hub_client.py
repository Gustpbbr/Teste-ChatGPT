"""Cliente fino do Hub Qdrant do Gus. DEGRADÁVEL por contrato.

Território: T-HUB (tarefa T2). Implementação de referência.
Regra: Hub fora NUNCA derruba o chamador. Retorna resultado "pendente".
"""
from __future__ import annotations

import json
import os
import time
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Literal

from .schema import Fragmento

IngestStatus = Literal["ok", "pendente", "erro"]

# Transporte injetável: recebe um Fragmento, devolve o id criado, levanta em falha.
# Permite testar sem rede e trocar urllib por httpx no futuro.
Transport = Callable[[Fragmento], str]


@dataclass
class IngestResult:
    status: IngestStatus
    id: str | None = None
    detalhe: str = ""


class HubClient:
    """Wrapper de I/O com o Hub. Endpoints reusam o Gus existente.

    Config via env (ver .env.example): HUB_URL, HUB_TOKEN.
    """

    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        *,
        transport: Transport | None = None,
        health_probe: Callable[[], bool] | None = None,
        sleep: Callable[[float], None] = time.sleep,
        base_backoff: float = 2.0,
    ) -> None:
        self.url = (url if url is not None else os.getenv("HUB_URL", "")) or ""
        self.token = (token if token is not None else os.getenv("HUB_TOKEN", "")) or ""
        self._transport = transport
        self._health_probe = health_probe
        self._sleep = sleep
        self._base_backoff = base_backoff
        self._ultima_escrita: datetime | None = None

    def ingestar(self, frag: Fragmento) -> IngestResult:
        """Escreve um fragmento no Hub.

        Retry com backoff exponencial (2/4/8/16s). Se esgotar/Hub fora:
        retorna IngestResult(status="pendente") — NÃO levanta exceção fatal.
        """
        transport = self._transport
        if transport is None:
            if not self.url:
                return IngestResult("pendente", detalhe="Hub não configurado (HUB_URL ausente)")
            transport = self._http_transport

        delay = self._base_backoff
        ultimo_erro = ""
        for tentativa in range(4):
            try:
                frag_id = transport(frag)
                self._ultima_escrita = datetime.now(timezone.utc)
                return IngestResult("ok", id=frag_id)
            except Exception as e:  # degradável: nunca propaga
                ultimo_erro = str(e)
                if tentativa < 3:
                    self._sleep(delay)
                    delay *= 2
        return IngestResult("pendente", detalhe=f"Hub indisponível: {ultimo_erro}")

    def health(self) -> bool:
        """True se o Hub responde. Nunca levanta — em dúvida, False."""
        try:
            if self._health_probe is not None:
                return bool(self._health_probe())
            return bool(self.url)  # TODO(T2+): ping real em GET /hub/health
        except Exception:
            return False

    def ultima_escrita(self) -> datetime | None:
        """Timestamp da última escrita bem-sucedida por este cliente."""
        return self._ultima_escrita

    def _http_transport(self, frag: Fragmento) -> str:
        payload = json.dumps(frag.__dict__, default=str).encode()
        req = urllib.request.Request(
            self.url.rstrip("/") + "/hub/ingestar",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
            data = json.loads(resp.read())
        return str(data.get("id", ""))
