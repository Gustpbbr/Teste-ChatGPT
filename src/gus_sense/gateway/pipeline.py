"""Pipeline do Gateway — orquestra coleta → filtro → evento → PII → ingest.

Território: T-PIPE (tarefa T7). Implementação de referência.
Ver docs/04-bloco-1-sensor-wearable.md.
"""
from __future__ import annotations

from typing import Callable, Sequence

from ..hub_client import HubClient
from ..schema import Fragmento
from .filters import Baseline, Event, denoise, detect_events, windowize
from .sensors import Sensor

# Função que recebe texto e devolve texto redigido (PII removida). Reusa a
# lógica de patterns_sensiveis do Gus. Injetada pra ser testável.
ScrubPII = Callable[[str], str]


class Gateway:
    def __init__(
        self,
        sensors: Sequence[Sensor],
        hub: HubClient,
        scrub_pii: ScrubPII,
        baselines: dict[str, Baseline] | None = None,
        janela_seg: int = 60,
    ) -> None:
        self.sensors = sensors
        self.hub = hub
        self.scrub_pii = scrub_pii
        self.baselines = baselines or {}
        self.janela_seg = janela_seg

    def run_once(self) -> list[Fragmento]:
        """Um ciclo do Gateway.

        Para cada sensor: stream -> windowize -> denoise -> detect_events.
        Cada Event vira Fragmento (sensivel=true p/ biometria), passa por scrub_pii,
        e é ingerido. Hub fora -> resultado "pendente" (degradável), não quebra.
        Stream sem eventos -> retorna [] (anti-memória-lixão).
        """
        fragmentos: list[Fragmento] = []
        for sensor in self.sensors:
            readings = list(sensor.stream())
            for janela in windowize(readings, self.janela_seg):
                base = self.baselines.get(janela.metric)
                if base is None:
                    continue  # sem baseline não há como detectar evento
                janela = denoise(janela)
                for ev in detect_events(janela, base):
                    frag = self._event_para_fragmento(ev, sensor.name)
                    self.hub.ingestar(frag)  # degradável; pendente é aceitável
                    fragmentos.append(frag)
        return fragmentos

    def _event_para_fragmento(self, ev: Event, sensor_name: str) -> Fragmento:
        """Constrói o Fragmento a partir de um Event.

        area="saude" + via="sensor-*" -> schema força metadata.sensivel=True (rota local).
        """
        conteudo = self.scrub_pii(ev.descricao)
        return Fragmento(
            conteudo=conteudo,
            tipo="sensorial",
            area="saude",
            camada_temporal="semana",
            confianca=0.9 if ev.severidade == "atencao" else 0.7,
            via="sensor-wearable",
            user_id="gustavo",
            metadata={"sensor": sensor_name},
        )
