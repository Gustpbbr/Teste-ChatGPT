"""
ACEE — VSE: Vetor Simbólico de Emoção
======================================
Formato padronizado de saída dos Interpretadores Leves (ILs).
Baseado na spec ACEE Cap-06 (VSE_Core, schema ACEESym).

Cada VSE representa o estado emocional inferido a partir de um canal
sensorial (voz, face, pupila, texto, etc.) em um formato estruturado
e serializável.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional
import json
import uuid


@dataclass
class VSE:
    """Vetor Simbólico de Emoção — moeda comum entre CMA e NCAC."""

    # ── Identificação ──────────────────────────────────────────
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    schema_version: str = "acee-v1.0"
    canal: str = "voz"  # voz, facial, pupilar, texto, postural, fisio, etc.

    # ── Origem ─────────────────────────────────────────────────
    uid_origem: str = "anonimo"  # ID do usuário (anonimizado se necessário)
    score_confianca: float = 0.0  # 0.0–1.0, qualidade da inferência

    # ── Temporal ───────────────────────────────────────────────
    timestamp_geracao: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    janela_sinal_ms: int = 0  # duração da janela de áudio analisada

    # ── Emoção ─────────────────────────────────────────────────
    emocao_primaria: str = "neutro"
    emocao_secundaria: Optional[str] = None
    valencia: float = 0.0  # -1.0 (negativa) a +1.0 (positiva)
    arousal: float = 0.0  # 0.0 (calmo) a 1.0 (excitado)
    dominancia: Optional[float] = None  # 0.0–1.0 (opcional)

    # ── Metadados ──────────────────────────────────────────────
    codigo_ambiguidade: str = "baixo"  # baixo, medio, alto
    qualidade_sinal: float = 1.0  # 0.0–1.0
    parametros_canal: dict = field(default_factory=dict)  # específicos do IL

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def neutro(cls, canal: str = "voz") -> "VSE":
        """Factory para VSE neutro (fallback quando não há sinal claro)."""
        return cls(
            canal=canal,
            emocao_primaria="neutro",
            valencia=0.0,
            arousal=0.0,
            score_confianca=0.0,
            codigo_ambiguidade="alto",
            qualidade_sinal=0.0,
        )


# ── Emoções suportadas ─────────────────────────────────────────
EMOCOES = [
    "neutro",
    "alegria",
    "tristeza",
    "raiva",
    "medo",
    "surpresa",
    "nojo",
    "calmo",
    "ansioso",
    "interessado",
    "entediado",
    "frustrado",
]
