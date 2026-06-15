"""Bloco 0 — Interocepção: o Gus percebe o próprio estado interno.

Território: T-INTERO (tarefa T6). Implementação de referência.
Escreve auto-fragmentos no brain user_id="gus" (autobiografia), nunca "gustavo".
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal

from .hub_client import HubClient
from .schema import Fragmento

Severidade = Literal["ok", "warn", "erro"]

# Estado por componente p/ anti-spam (emite só na transição de severidade).
_ESTADO_SEVERIDADE: dict[str, str] = {}


@dataclass
class Health:
    componente: str            # "hub" | "curador"
    ok: bool
    detalhe: str               # legível: "última escrita há 3h12"
    ultima_escrita: datetime | None
    severidade: Severidade


def hub_health(hub: HubClient) -> Health:
    """O Hub responde? Degradável: em falha, severidade='erro', sem levantar."""
    try:
        ok = bool(hub.health())
    except Exception:
        ok = False
    try:
        ultima = hub.ultima_escrita()
    except Exception:
        ultima = None
    sev: Severidade = "ok" if ok else "erro"
    return Health("hub", ok, "Hub responde" if ok else "Hub não responde", ultima, sev)


def curador_heartbeat(hub: HubClient, janela_horas: int = 6) -> Health:
    """Curador escreveu nas últimas `janela_horas`? > janela -> warn ; > 12h -> erro."""
    try:
        ultima = hub.ultima_escrita()
    except Exception:
        ultima = None
    if ultima is None:
        return Health("curador", False, "curador nunca escreveu (ou desconhecido)", None, "erro")

    delta_h = (datetime.now(timezone.utc) - ultima).total_seconds() / 3600
    if delta_h > 12:
        sev: Severidade = "erro"
    elif delta_h > janela_horas:
        sev = "warn"
    else:
        sev = "ok"
    return Health("curador", sev == "ok", f"última escrita há {delta_h:.1f}h", ultima, sev)


def emit_self_fragment(
    h: Health, hub: HubClient, estado: dict[str, str] | None = None
) -> Fragmento | None:
    """Emite auto-fragmento se severidade != 'ok'.

    Anti-spam: só na TRANSIÇÃO de severidade (não a cada check).
    Fragmento: user_id="gus", tipo="meta_reflexao", area="infra-hub", via="interocepcao".
    """
    estado = _ESTADO_SEVERIDADE if estado is None else estado
    anterior = estado.get(h.componente, "ok")
    estado[h.componente] = h.severidade

    if h.severidade == "ok" or h.severidade == anterior:
        return None

    frag = Fragmento(
        conteudo=f"[interocepção] {h.componente}: {h.detalhe} (severidade={h.severidade}).",
        tipo="meta_reflexao",
        area="infra-hub",
        camada_temporal="sessao",
        confianca=0.9,
        via="interocepcao",
        user_id="gus",
    )
    try:
        hub.ingestar(frag)
    except Exception:
        pass  # degradável: percepção do próprio mal-estar não pode quebrar
    return frag


def check_all(hub: HubClient) -> list[Health]:
    """Roda todos os checks. Usado por cron (ciclo vital) e sob demanda."""
    return [hub_health(hub), curador_heartbeat(hub)]


def reset_estado() -> None:
    """Limpa o estado de anti-spam (uso em testes / reinício de ciclo)."""
    _ESTADO_SEVERIDADE.clear()
