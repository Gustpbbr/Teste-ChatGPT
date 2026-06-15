"""Testes do WearableSensor (tarefa T4)."""
from datetime import datetime

from gus_sense.gateway.sensors import Reading, WearableSensor

FONTE = "tests/fixtures/wearable-mock.json"


def test_stream_emite_readings_validos():
    leituras = list(WearableSensor(FONTE).stream())
    assert leituras
    assert all(isinstance(r, Reading) for r in leituras)
    assert all(isinstance(r.ts, datetime) for r in leituras)


def test_stream_ordenado_por_ts():
    leituras = list(WearableSensor(FONTE).stream())
    ts = [r.ts for r in leituras]
    assert ts == sorted(ts)
