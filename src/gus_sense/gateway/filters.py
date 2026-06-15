"""Filtros do Gateway — o coração anti-memória-lixão.

Território: T-FILTER (tarefa T3). Leitura normal -> ZERO evento.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator

from .sensors import Reading


@dataclass
class Window:
    metric: str
    readings: list[Reading]
    # estatísticas derivadas preenchidas por denoise()
    media: float | None = None
    pico: float | None = None


@dataclass
class Baseline:
    """Média móvel dos últimos 7 dias por métrica."""
    metric: str
    media_7d: float
    desvio_7d: float


@dataclass
class Event:
    metric: str
    descricao: str         # legível, vira `conteudo` do fragmento
    valor: float
    severidade: str        # "info" | "atencao"


def windowize(readings: Iterable[Reading], seconds: int = 60) -> Iterator[Window]:
    """Agrupa leituras em janelas temporais de `seconds`."""
    # TODO(T3)
    raise NotImplementedError("T3")


def denoise(window: Window) -> Window:
    """Remove outliers grosseiros, suaviza, preenche estatísticas da janela."""
    # TODO(T3)
    raise NotImplementedError("T3")


def detect_events(window: Window, baseline: Baseline) -> list[Event]:
    """Só desvios relevantes vs baseline viram Event. Normal -> []."""
    # TODO(T3): regras em docs/04 (HR repouso > baseline+40 por >15min; sono <5h; HRV cai >30%).
    raise NotImplementedError("T3")
