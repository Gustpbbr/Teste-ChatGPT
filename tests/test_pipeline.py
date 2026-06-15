"""Testes do pipeline do Gateway — Bloco 1 (tarefa T7)."""
from datetime import datetime, timedelta, timezone

from gus_sense.gateway.filters import Baseline
from gus_sense.gateway.pipeline import Gateway
from gus_sense.gateway.sensors import Reading
from gus_sense.hub_client import HubClient

_BASE = datetime(2026, 6, 15, 6, 0, tzinfo=timezone.utc)
_BASELINES = {"hr": Baseline("hr", media_7d=62)}


def _ident(s: str) -> str:
    return s


class FakeSensor:
    name = "wearable"

    def __init__(self, valores):
        self._valores = valores

    def stream(self):
        for i, v in enumerate(self._valores):
            yield Reading("hr", v, _BASE + timedelta(seconds=i), "bpm")


def test_stream_normal_zero_fragmentos():
    """Leituras normais -> Gateway.run_once() retorna []."""
    g = Gateway([FakeSensor([61, 62, 63, 62])], HubClient(url=""), _ident, _BASELINES)
    assert g.run_once() == []


def test_evento_gera_fragmento_sensivel():
    """Evento -> 1 fragmento gus-18 válido com metadata.sensivel=True."""
    g = Gateway([FakeSensor([110, 111, 112, 110])], HubClient(url=""), _ident, _BASELINES)
    frags = g.run_once()
    assert len(frags) == 1
    assert frags[0].metadata["sensivel"] is True
    assert frags[0].tipo == "sensorial"
    assert frags[0].area == "saude"


def test_hub_fora_vira_pendente_sem_quebrar():
    """Hub indisponível -> ingest 'pendente', pipeline não levanta."""
    hub = HubClient(url="")  # sem URL -> ingest devolve pendente
    g = Gateway([FakeSensor([110, 111, 112])], hub, _ident, _BASELINES)
    frags = g.run_once()
    assert len(frags) == 1
