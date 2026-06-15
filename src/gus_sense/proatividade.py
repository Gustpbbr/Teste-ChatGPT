"""Bloco 5 — Proatividade (núcleo testável): o Gus detecta o que merece atenção.

v0 com sinais tratáveis sem embeddings:
  - lacuna: área monitorada sem fragmento recente (silêncio anômalo)
  - acúmulo de esquecidos: muitos fragmentos `estado="esquecido"` numa área

Detecção de contradição semântica (dois nós que se atraem e brilham vermelho)
precisa de embeddings e fica pra uma versão posterior.

Estes sinais alimentam a proatividade espacial do VR (Bloco 5 completo) e o
afeto funcional do Gus.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .schema import Fragmento


@dataclass
class Sinal:
    tipo: str          # "lacuna" | "acumulo_esquecidos"
    descricao: str
    area: str
    severidade: str    # "info" | "atencao"
    motivo: str = ""   # A3: explicabilidade — por que este sinal foi gerado


def detectar_lacuna(
    frags: list[Fragmento], area: str, agora: datetime | None = None, max_silencio_h: float = 48
) -> Sinal | None:
    """Sinaliza se uma área monitorada não tem fragmento ativo recente."""
    agora = agora or datetime.now(timezone.utc)
    ativos = [f for f in frags if f.area == area and f.estado != "esquecido"]
    if not ativos:
        return Sinal(
            "lacuna", f"Nenhum registro em '{area}'.", area, "atencao",
            motivo="área monitorada sem nenhum fragmento ativo",
        )

    mais_recente = max(f.criado_em for f in ativos)
    silencio_h = (agora - mais_recente).total_seconds() / 3600
    if silencio_h > max_silencio_h:
        return Sinal(
            "lacuna",
            f"'{area}' sem registro há {silencio_h:.0f}h.",
            area,
            "atencao",
            motivo=f"silêncio {silencio_h:.0f}h > limite {max_silencio_h:.0f}h",
        )
    return None


def detectar_acumulo_esquecidos(frags: list[Fragmento], limiar: int = 5) -> list[Sinal]:
    """Sinaliza áreas com muitos fragmentos esquecidos (candidato a revisão)."""
    por_area: dict[str, int] = {}
    for f in frags:
        if f.estado == "esquecido":
            por_area[f.area] = por_area.get(f.area, 0) + 1

    return [
        Sinal(
            "acumulo_esquecidos", f"'{area}' tem {n} esquecidos — revisar?", area, "info",
            motivo=f"{n} esquecidos >= limiar {limiar}",
        )
        for area, n in por_area.items()
        if n >= limiar
    ]


def analisar(
    frags: list[Fragmento], areas_monitoradas: list[str], agora: datetime | None = None
) -> list[Sinal]:
    """Roda todos os detectores. Usado por cron (ciclo vital) e sob demanda."""
    sinais: list[Sinal] = []
    for area in areas_monitoradas:
        lacuna = detectar_lacuna(frags, area, agora)
        if lacuna:
            sinais.append(lacuna)
    sinais.extend(detectar_acumulo_esquecidos(frags))
    return sinais
