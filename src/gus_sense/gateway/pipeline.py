"""Pipeline do Gateway — orquestra coleta → filtro → evento → PII → ingest.

Território: T-PIPE (tarefa T7). Ver docs/04-bloco-1-sensor-wearable.md.
"""
from __future__ import annotations

from typing import Callable, Sequence

from ..hub_client import HubClient
from ..schema import Fragmento
from . import filters
from .sensors import Sensor

# Função que recebe texto e devolve texto redigido (PII removida). Reusa
# a lógica de patterns_sensiveis do Gus. Injetada pra ser testável.
ScrubPII = Callable[[str], str]


class Gateway:
    def __init__(
        self,
        sensors: Sequence[Sensor],
        hub: HubClient,
        scrub_pii: ScrubPII,
        baselines: dict | None = None,
    ) -> None:
        self.sensors = sensors
        self.hub = hub
        self.scrub_pii = scrub_pii
        self.baselines = baselines or {}

    def run_once(self) -> list[Fragmento]:
        """Um ciclo do Gateway.

        Para cada sensor: stream -> windowize -> denoise -> detect_events.
        Cada Event vira Fragmento (sensivel=true p/ biometria), passa por scrub_pii,
        e é ingerido. Hub fora -> resultado "pendente" (degradável), não quebra.
        Stream sem eventos -> retorna [] (anti-memória-lixão).
        """
        # TODO(T7): montar o fluxo usando filters.* e construir Fragmento gus-18 válido.
        raise NotImplementedError("T7")

    def _event_para_fragmento(self, ev: "filters.Event") -> Fragmento:
        """Constrói o Fragmento a partir de um Event.

        area="saude", via="sensor-wearable", user_id="gustavo",
        camada_temporal="semana", metadata={"sensivel": True, "sensor": ...}.
        """
        # TODO(T7)
        raise NotImplementedError("T7")
