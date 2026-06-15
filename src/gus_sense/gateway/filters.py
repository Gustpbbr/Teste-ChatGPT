"""Filtros do Gateway — o coração anti-memória-lixão.

Território: T-FILTER (tarefa T3). Implementação de referência.
Leitura normal -> ZERO evento. Só desvios relevantes vs baseline viram Event.
"""
from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import Iterable, Iterator

from .sensors import Reading

# Fração de desvio em relação à mediana acima da qual um ponto é tratado como
# ruído grosseiro e descartado pelo denoise (robusto a spike isolado).
_OUTLIER_REL = 0.4
# HR de repouso acima de baseline + este delta (bpm) vira evento.
_HR_DELTA = 40.0
# Sono (horas) abaixo disto vira evento.
_SONO_MIN_H = 5.0
# HRV abaixo desta fração da baseline vira evento (queda > 30%).
_HRV_FRAC = 0.7


@dataclass
class Window:
    metric: str
    readings: list[Reading]
    media: float | None = None
    pico: float | None = None


@dataclass
class Baseline:
    """Média móvel dos últimos 7 dias por métrica."""
    metric: str
    media_7d: float
    desvio_7d: float = 0.0


@dataclass
class Event:
    metric: str
    descricao: str         # legível, vira `conteudo` do fragmento
    valor: float
    severidade: str        # "info" | "atencao"


def windowize(readings: Iterable[Reading], seconds: int = 60) -> Iterator[Window]:
    """Agrupa leituras em janelas temporais de `seconds`, por métrica."""
    por_metrica: dict[str, list[Reading]] = {}
    for r in readings:
        por_metrica.setdefault(r.metric, []).append(r)

    for metric, rs in por_metrica.items():
        rs.sort(key=lambda r: r.ts)
        bucket: list[Reading] = []
        inicio = None
        for r in rs:
            if inicio is None:
                inicio = r.ts
            if bucket and (r.ts - inicio).total_seconds() >= seconds:
                yield Window(metric=metric, readings=bucket)
                bucket = []
                inicio = r.ts
            bucket.append(r)
        if bucket:
            yield Window(metric=metric, readings=bucket)


def denoise(window: Window) -> Window:
    """Remove outliers grosseiros (robusto via mediana) e preenche estatísticas."""
    vals = [r.value for r in window.readings]
    if not vals:
        return window
    med = statistics.median(vals)
    if med > 0:
        mantidos = [r for r in window.readings if abs(r.value - med) <= _OUTLIER_REL * med]
        if mantidos:
            window.readings = mantidos
            vals = [r.value for r in mantidos]
    window.media = statistics.mean(vals)
    window.pico = max(vals)
    return window


def detect_events(window: Window, baseline: Baseline) -> list[Event]:
    """Só desvios relevantes vs baseline viram Event. Normal -> []."""
    if window.media is None:
        window = denoise(window)
    media = window.media or 0.0
    eventos: list[Event] = []

    if window.metric == "hr":
        if media > baseline.media_7d + _HR_DELTA:
            eventos.append(Event(
                "hr",
                f"HR repouso elevado: {media:.0f}bpm (baseline {baseline.media_7d:.0f}).",
                media, "atencao",
            ))
    elif window.metric == "sleep":
        if media < _SONO_MIN_H:
            eventos.append(Event("sleep", f"Sono curto: {media:.1f}h.", media, "atencao"))
    elif window.metric == "hrv":
        if baseline.media_7d > 0 and media < baseline.media_7d * _HRV_FRAC:
            eventos.append(Event(
                "hrv",
                f"HRV baixa: {media:.0f} (baseline {baseline.media_7d:.0f}).",
                media, "atencao",
            ))
    return eventos
