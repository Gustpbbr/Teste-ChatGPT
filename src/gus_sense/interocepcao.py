"""Bloco 0 — Interocepção: o Gus percebe o próprio estado interno.

Território: T-INTERO (tarefa T6). Ver docs/03-bloco-0-interocepcao.md.
Escreve auto-fragmentos no brain user_id="gus" (autobiografia), nunca "gustavo".
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from .hub_client import HubClient
from .schema import Fragmento

Severidade = Literal["ok", "warn", "erro"]


@dataclass
class Health:
    componente: str            # "hub" | "curador"
    ok: bool
    detalhe: str               # legível: "última escrita há 3h12"
    ultima_escrita: datetime | None
    severidade: Severidade


def hub_health(hub: HubClient) -> Health:
    """O Hub responde? Quando foi a última escrita?"""
    # TODO(T6): usar hub.health() + hub.ultima_escrita(). Hub fora -> severidade="erro",
    # sem levantar exceção (degradável).
    raise NotImplementedError("T6")


def curador_heartbeat(hub: HubClient, janela_horas: int = 6) -> Health:
    """Curador escreveu nas últimas `janela_horas`?

    > janela -> warn ; > 12h -> erro.
    """
    # TODO(T6)
    raise NotImplementedError("T6")


def emit_self_fragment(h: Health, hub: HubClient) -> Fragmento | None:
    """Emite auto-fragmento se severidade != 'ok'.

    Anti-spam: só na TRANSIÇÃO de severidade (ok->warn, warn->erro), não a cada check.
    Fragmento: user_id="gus", tipo="meta_reflexao", area="infra-hub", via="interocepcao".
    """
    # TODO(T6)
    raise NotImplementedError("T6")


def check_all(hub: HubClient) -> list[Health]:
    """Roda todos os checks. Usado por cron (ciclo vital) e sob demanda."""
    # TODO(T6)
    raise NotImplementedError("T6")
