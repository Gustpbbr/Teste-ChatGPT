"""Fragmento — unidade de memória, compatível com o schema gus-18 do Gus.

Território: T-SCHEMA (tarefa T1). Implementar validação e enums.
NÃO mudar os nomes de campo: precisam casar com o Hub do Gus existente.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

# --- Enums gus-18 (manter sincronizado com o Gus) ---
Tipo = Literal[
    "biografico", "fato", "decisao", "preferencia", "identidade_operacional",
    "episodico", "meta_reflexao", "projeto", "rotina", "procedural", "sensorial",
]
CamadaTemporal = Literal["efemero", "sessao", "semana", "rotina", "permanente"]
Estado = Literal["ativo", "estavel", "historico", "esquecido"]
UserId = Literal["gustavo", "gus"]


@dataclass
class Fragmento:
    """Fragmento no schema gus-18. Ver docs/01-arquitetura.md."""
    conteudo: str
    tipo: Tipo = "episodico"
    area: str = ""
    camada_temporal: CamadaTemporal = "sessao"
    confianca: float = 0.7
    via: str = "sensor"            # ver gus-13 (taxonomia via)
    user_id: UserId = "gustavo"
    estado: Estado = "ativo"
    metadata: dict = field(default_factory=dict)
    criado_em: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        # TODO(T1): validar enums, clamp confianca em [0,1], exigir conteudo não-vazio,
        # garantir metadata["sensivel"] coerente com area (ex.: dimagem/biometria -> True).
        raise NotImplementedError("T1: implementar validação gus-18")


def validar(frag: Fragmento) -> Fragmento:
    """Valida e normaliza um fragmento. Levanta ValueError se inválido."""
    # TODO(T1)
    raise NotImplementedError("T1")
