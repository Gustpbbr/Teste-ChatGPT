"""Sensores — interface base e adaptador wearable.

Território: T-SENSOR (tarefa T4). Implementação de referência.
v0 lê de fonte MOCKADA (JSON); API real (Whoop/Oura/Apple) fica pra depois.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, Protocol


@dataclass
class Reading:
    metric: str            # "hr" | "hrv" | "sleep"
    value: float
    ts: datetime
    unit: str


class Sensor(Protocol):
    name: str
    def stream(self) -> Iterator[Reading]: ...


class WearableSensor:
    """Adaptador de wearable. v0: lê leituras de um arquivo JSON mockado.

    Formato esperado: lista de objetos {metric, value, ts (ISO 8601), unit}.
    """
    name = "wearable"

    def __init__(self, fonte: str) -> None:
        self.fonte = fonte

    def stream(self) -> Iterator[Reading]:
        dados = json.loads(Path(self.fonte).read_text(encoding="utf-8"))
        for item in sorted(dados, key=lambda d: d["ts"]):
            yield Reading(
                metric=str(item["metric"]),
                value=float(item["value"]),
                ts=datetime.fromisoformat(item["ts"]),
                unit=str(item.get("unit", "")),
            )
