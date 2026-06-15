"""Fragmento — unidade de memória, compatível com o schema gus-18 do Gus.

Território: T-SCHEMA (tarefa T1). Implementação de referência.
NÃO mudar os nomes de campo: precisam casar com o Hub do Gus existente.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Literal, get_args

# --- Enums gus-18 (manter sincronizado com o Gus) ---
Tipo = Literal[
    "biografico", "fato", "decisao", "preferencia", "identidade_operacional",
    "episodico", "meta_reflexao", "projeto", "rotina", "procedural", "sensorial",
]
CamadaTemporal = Literal["efemero", "sessao", "semana", "rotina", "permanente"]
Estado = Literal["ativo", "estavel", "historico", "esquecido"]
UserId = Literal["gustavo", "gus"]

TIPOS = frozenset(get_args(Tipo))
CAMADAS = frozenset(get_args(CamadaTemporal))
ESTADOS = frozenset(get_args(Estado))
USER_IDS = frozenset(get_args(UserId))

# Áreas cujo conteúdo é sensível por padrão (LGPD) -> rota local obrigatória.
SENSITIVE_AREAS = frozenset({"dimagem"})


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
        self._normalizar()

    def _normalizar(self) -> None:
        if not self.conteudo or not self.conteudo.strip():
            raise ValueError("conteudo não pode ser vazio")
        if self.tipo not in TIPOS:
            raise ValueError(f"tipo inválido: {self.tipo!r} (válidos: {sorted(TIPOS)})")
        if self.camada_temporal not in CAMADAS:
            raise ValueError(f"camada_temporal inválida: {self.camada_temporal!r}")
        if self.estado not in ESTADOS:
            raise ValueError(f"estado inválido: {self.estado!r}")
        if self.user_id not in USER_IDS:
            raise ValueError(f"user_id inválido: {self.user_id!r} (válidos: {sorted(USER_IDS)})")
        if not self.via or not self.via.strip():
            raise ValueError("via não pode ser vazia")

        # clamp confiança em [0, 1]
        self.confianca = max(0.0, min(1.0, float(self.confianca)))

        # coerência de sensibilidade (LGPD): biometria de sensor + área clínica
        # nascem sensíveis -> força rota local. Explícito sempre vence pra True.
        sensivel = bool(self.metadata.get("sensivel", False))
        biometria = self.via.startswith("sensor-") and self.area == "saude"
        if self.area in SENSITIVE_AREAS or biometria:
            sensivel = True
        self.metadata["sensivel"] = sensivel


def validar(frag: Fragmento) -> Fragmento:
    """Revalida/normaliza um fragmento (idempotente). Levanta ValueError se inválido."""
    novo = replace(frag)  # dispara __post_init__ de novo
    return novo
