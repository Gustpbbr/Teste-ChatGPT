"""
ACEE — IL-Voz: Interpretador Leve de Voz
=========================================
MVP funcional: extrai features prosódicas de arquivo .wav e produz VSE.

Baseado na spec ACEE Cap-06 §6.2.1 (IL-Voz).
Dependências: pip install librosa numpy scikit-learn

Uso:
    python3 il_voz.py audio.wav

Output:
    JSON com VSE (emoção, valência, arousal, features detalhadas)
"""

import sys
import json
import math
from pathlib import Path
from typing import Optional

import numpy as np

try:
    import librosa
except ImportError:
    print("❌ Instale librosa: pip install librosa")
    sys.exit(1)

from vse import VSE, EMOCOES


# ── Config ────────────────────────────────────────────────────────
SAMPLE_RATE = 16000  # Hz (reduz pra análise leve)
JANELA_MS = 3000     # analisa até 3 segundos
CONFIANCA_MINIMA = 0.3  # abaixo disso retorna neutro


def extrair_features(audio_path: str) -> dict:
    """Extrai features prosódicas de arquivo .wav.

    Retorna dict com: pitch (F0), energia (RMS), taxa de fala,
    shimmer, jitter, formantes, spectral centroid, zero-crossing rate.
    """
    y, sr = librosa.load(audio_path, sr=SAMPLE_RATE, duration=JANELA_MS/1000)
    
    if len(y) < sr * 0.2:  # menos de 200ms → sinal inválido
        return {"erro": "audio_muito_curto", "duracao_ms": len(y)/sr*1000}
    
    duracao_ms = len(y) / sr * 1000
    
    # ── Energia (RMS) ─────────────────────────────────────────
    rms = float(np.sqrt(np.mean(y**2)))
    
    # ── Pitch (F0) via autocorrelação ──────────────────────────
    f0, f0_conf = _estimar_pitch(y, sr)
    
    # ── Zero-crossing rate ─────────────────────────────────────
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)[0]))
    
    # ── Spectral centroid (brilho do som) ──────────────────────
    centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)[0]))
    
    # ── MFCC (coeficientes mel) ────────────────────────────────
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = [float(x) for x in np.mean(mfcc, axis=1)]
    
    # ── Shimmer (variação de amplitude) e Jitter (variação de F0)
    shimmer = _calcular_shimmer(y)
    jitter = _calcular_jitter(y, sr) if f0_conf > 0.5 else 0.0
    
    # ── Taxa de fala estimada ──────────────────────────────────
    # Conta "pulsos" de energia acima de threshold
    energia_envelope = np.array([np.mean(np.abs(y[i:i+int(sr*0.05)])) 
                                  for i in range(0, len(y), int(sr*0.05))])
    pulsos = np.sum(energia_envelope > np.mean(energia_envelope) * 1.2)
    taxa_fala = pulsos / (duracao_ms / 1000) * 2  # pulsos/segundo
    
    return {
        "duracao_ms": round(duracao_ms, 1),
        "rms": round(rms, 6),
        "f0_hz": round(f0, 1),
        "f0_confianca": round(f0_conf, 2),
        "zcr": round(zcr, 4),
        "spectral_centroid_hz": round(centroid, 1),
        "mfcc_1_3_mean": [round(x, 2) for x in mfcc_mean[:3]],
        "shimmer": round(shimmer, 4),
        "jitter": round(jitter, 4),
        "taxa_fala_pps": round(taxa_fala, 1),
        "qualidade_sinal": round(min(1.0, f0_conf * (rms / 0.01)), 2),
    }


def _estimar_pitch(y: np.ndarray, sr: int) -> tuple:
    """Estima F0 por autocorrelação. Retorna (f0_hz, confiança)."""
    try:
        f0, voiced_flag, _ = librosa.pyin(
            y, fmin=50, fmax=500, sr=sr, fill_na=0
        )
        f0_voiced = f0[voiced_flag > 0]
        if len(f0_voiced) == 0:
            return 0.0, 0.0
        f0_mean = float(np.median(f0_voiced))
        confianca = len(f0_voiced) / len(f0)
        return f0_mean, confianca
    except Exception:
        return 0.0, 0.0


def _calcular_shimmer(y: np.ndarray) -> float:
    """Shimmer = variação de amplitude pico a pico."""
    picos = []
    for i in range(1, len(y) - 1):
        if y[i] > y[i-1] and y[i] > y[i+1] and y[i] > 0:
            picos.append(y[i])
    if len(picos) < 3:
        return 0.0
    amplitudes = np.array(picos)
    return float(np.std(amplitudes) / (np.mean(amplitudes) + 1e-10))


def _calcular_jitter(y: np.ndarray, sr: int) -> float:
    """Jitter = variação de período entre picos."""
    picos_idx = []
    for i in range(1, len(y) - 1):
        if y[i] > y[i-1] and y[i] > y[i+1] and y[i] > 0:
            picos_idx.append(i)
    if len(picos_idx) < 4:
        return 0.0
    periodos = np.diff(picos_idx) / sr * 1000  # ms
    return float(np.std(periodos) / (np.mean(periodos) + 1e-10))


def classificar_emocao(features: dict) -> dict:
    """Classifica emoção a partir de features prosódicas.
    
    Usa heurísticas baseadas em literatura (não ML):
    - F0 alto + energia alta → alegria/raiva
    - F0 baixo + energia baixa → tristeza/calma
    - F0 variável (jitter/shimmer altos) → ansiedade/medo
    - Taxa de fala alta → excitação; baixa → calma/tristeza
    """
    if "erro" in features:
        return {
            "emocao_primaria": "neutro",
            "valencia": 0.0,
            "arousal": 0.0,
            "confianca": 0.0,
            "ambiguidade": "alto",
            "motivo": features["erro"],
        }
    
    f0 = features["f0_hz"]
    f0_conf = features["f0_confianca"]
    rms = features["rms"]
    zcr = features["zcr"]
    taxa_fala = features["taxa_fala_pps"]
    jitter = features["jitter"]
    shimmer = features["shimmer"]
    mfcc1 = features["mfcc_1_3_mean"][0] if features["mfcc_1_3_mean"] else 0
    
    if f0_conf < 0.2:
        return {"emocao_primaria": "neutro", "valencia": 0.0, "arousal": 0.0, 
                "confianca": 0.1, "ambiguidade": "alto", "motivo": "f0_baixa_confianca"}
    
    # ── Arousal (excitação) ────────────────────────────────────
    # Combinando: energia + taxa de fala + ZCR + F0
    arousal_raw = (
        _escala(rms, 0.001, 0.1) * 0.35 +
        _escala(taxa_fala, 1, 8) * 0.25 +
        _escala(zcr, 0.01, 0.15) * 0.15 +
        _escala(f0, 80, 350) * 0.25
    )
    arousal = round(min(1.0, max(0.0, arousal_raw)), 2)
    
    # ── Valência (positividade) ─────────────────────────────────
    # F0 médio-alto (120-250Hz) + energia moderada → positivo
    # F0 muito alto + jitter alto → possível raiva (negativo)
    # F0 baixo → tende a tristeza
    if 120 < f0 < 280 and rms > 0.01 and jitter < 0.03:
        valencia_raw = 0.5 + (rms * 30) - (jitter * 5)
    elif f0 > 280 and jitter > 0.04:
        valencia_raw = -0.3  # raiva/ansiedade
    elif f0 < 100:
        valencia_raw = -0.2  # tende a tristeza
    else:
        valencia_raw = 0.0
    
    valencia = round(max(-1.0, min(1.0, valencia_raw)), 2)
    
    # ── Emoção discreta ─────────────────────────────────────────
    if arousal > 0.55:
        if valencia > 0.15:
            emocao = "alegria"
        elif valencia < -0.15:
            emocao = "ansioso" if jitter < 0.08 else "raiva"
        else:
            emocao = "surpresa"
    elif arousal < 0.25:
        if valencia < -0.15:
            emocao = "tristeza"
        elif valencia > 0.1:
            emocao = "calmo"
        else:
            emocao = "entediado"
    else:
        if valencia > 0.2:
            emocao = "interessado"
        elif valencia < -0.25:
            emocao = "frustrado"
        else:
            emocao = "neutro"
    
    # ── Confiança ───────────────────────────────────────────────
    confianca = round(f0_conf * features["qualidade_sinal"], 2)
    if confianca < CONFIANCA_MINIMA:
        emocao = "neutro"
        valencia = 0.0
        arousal = 0.0
    
    return {
        "emocao_primaria": emocao,
        "valencia": valencia,
        "arousal": arousal,
        "confianca": confianca,
        "ambiguidade": "baixo" if confianca > 0.7 else ("medio" if confianca > 0.4 else "alto"),
        "dominancia": None,
    }


def _escala(valor: float, vmin: float, vmax: float) -> float:
    """Normaliza valor para [0, 1] com clamping."""
    if vmax == vmin:
        return 0.5
    return max(0.0, min(1.0, (valor - vmin) / (vmax - vmin)))


# ── Interface principal ──────────────────────────────────────────
def analisar_audio(audio_path: str) -> VSE:
    """Pipeline completo: áudio .wav → features → emoção → VSE."""
    features = extrair_features(audio_path)
    emocao = classificar_emocao(features)
    
    vse = VSE(
        canal="voz",
        uid_origem="anonimo",
        score_confianca=emocao["confianca"],
        janela_sinal_ms=int(features.get("duracao_ms", 0)),
        emocao_primaria=emocao["emocao_primaria"],
        valencia=emocao["valencia"],
        arousal=emocao["arousal"],
        dominancia=emocao.get("dominancia"),
        codigo_ambiguidade=emocao["ambiguidade"],
        qualidade_sinal=features.get("qualidade_sinal", 0.0),
        parametros_canal={
            "f0_hz": features.get("f0_hz", 0),
            "rms": features.get("rms", 0),
            "zcr": features.get("zcr", 0),
            "shimmer": features.get("shimmer", 0),
            "jitter": features.get("jitter", 0),
            "taxa_fala_pps": features.get("taxa_fala_pps", 0),
            "spectral_centroid_hz": features.get("spectral_centroid_hz", 0),
            "mfcc_1_3": features.get("mfcc_1_3_mean", []),
        },
    )
    return vse


# ── CLI ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 il_voz.py <arquivo.wav>")
        print("   Ex: python3 il_voz.py gravacao.wav")
        sys.exit(1)
    
    path = sys.argv[1]
    if not Path(path).exists():
        print(f"❌ Arquivo não encontrado: {path}")
        sys.exit(1)
    
    print(f"🎤 Analisando: {path}")
    vse = analisar_audio(path)
    
    print("\n📊 Features extraídas:")
    for k, v in vse.parametros_canal.items():
        if isinstance(v, float):
            print(f"   {k}: {v:.4f}")
        else:
            print(f"   {k}: {v}")
    
    print(f"\n🧠 Emoção inferida: {vse.emocao_primaria}")
    print(f"   Valência: {vse.valencia}  |  Arousal: {vse.arousal}")
    print(f"   Confiança: {vse.score_confianca}  |  Ambiguidade: {vse.codigo_ambiguidade}")
    
    print(f"\n📦 VSE JSON:")
    print(vse.to_json())
