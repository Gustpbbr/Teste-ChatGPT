"""Sensores — interface base e adaptador wearable.

Território: T-SENSOR (tarefa T4). v0 lê de fonte MOCKADA (JSON); API real depois.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
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

    Plugar API real (Whoop/Oura/Apple) é fora de escopo do Bloco 1.
    """
    name = "wearable"

    def __init__(self, fonte: str) -> None:
        # TODO(T4): fonte = caminho do JSON mockado (ver tests/fixtures).
        self.fonte = fonte

    def stream(self) -> Iterator[Reading]:
        # TODO(T4): ler a fonte e emitir Reading válidos, ordenados por ts.
        raise NotImplementedError("T4")
