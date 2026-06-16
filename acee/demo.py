"""
ACEE — Demo: Testa o IL-Voz com tons sintéticos
================================================
Gera arquivos .wav com diferentes características emocionais
e testa o pipeline de classificação.

Uso: python3 demo.py
"""

import subprocess
import sys
import numpy as np
from pathlib import Path
from il_voz import analisar_audio

SAMPLE_RATE = 16000
DURATION = 2.0  # segundos


def gerar_tom(freq: float, amplitude: float, ruido: float = 0.0, variacao: float = 0.0) -> np.ndarray:
    """Gera tom puro (ou com ruído/vibrato) para teste."""
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
    
    # Vibrato (variação de frequência)
    if variacao > 0:
        freq_inst = freq + variacao * freq * np.sin(2 * np.pi * 5 * t)
        sinal = amplitude * np.sin(2 * np.pi * freq_inst * t)
    else:
        sinal = amplitude * np.sin(2 * np.pi * freq * t)
    
    # Ruído
    if ruido > 0:
        sinal += ruido * np.random.randn(len(t))
    
    # Envelope (fade in/out)
    fade = min(1000, len(t) // 10)
    sinal[:fade] *= np.linspace(0, 1, fade)
    sinal[-fade:] *= np.linspace(1, 0, fade)
    
    # Normaliza
    sinal = sinal / (np.max(np.abs(sinal)) + 1e-10)
    return sinal.astype(np.float32)


def salvar_wav(sinal: np.ndarray, path: str):
    """Salva array numpy como WAV."""
    import wave
    sinal_int16 = (sinal * 32767).astype(np.int16)
    with wave.open(path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(sinal_int16.tobytes())


def main():
    print("=" * 60)
    print("🧪 ACEE — Demo IL-Voz")
    print("=" * 60)
    
    tmp = Path("/tmp/acee_demo")
    tmp.mkdir(exist_ok=True)
    
    testes = [
        # (nome, freq, amp, ruido, variacao, emocao_esperada)
        ("01_neutro", 150, 0.5, 0.01, 0.0, "neutro/calmo"),
        ("02_alegre", 250, 0.7, 0.01, 0.05, "alegria"),
        ("03_triste", 90, 0.3, 0.02, 0.0, "tristeza"),
        ("04_agitado", 350, 0.8, 0.03, 0.08, "raiva/ansioso"),
        ("05_sussurro", 100, 0.08, 0.05, 0.0, "neutro (sinal fraco)"),
    ]
    
    resultados = []
    
    for nome, freq, amp, ruido, vibrato, esperado in testes:
        fpath = tmp / f"{nome}.wav"
        sinal = gerar_tom(freq, amp, ruido, vibrato)
        salvar_wav(sinal, str(fpath))
        
        vse = analisar_audio(str(fpath))
        
        print(f"\n🎵 {nome} (F0={freq}Hz, amp={amp:.1f}) → esperado: {esperado}")
        print(f"   Emoção: {vse.emocao_primaria} | V={vse.valencia:+1.2f} A={vse.arousal:.2f} | conf={vse.score_confianca:.2f}")
        print(f"   Features: F0={vse.parametros_canal['f0_hz']:.0f}Hz RMS={vse.parametros_canal['rms']:.4f} "
              f"ZCR={vse.parametros_canal['zcr']:.4f} jitter={vse.parametros_canal['jitter']:.4f}")
        
        resultados.append({
            "nome": nome,
            "esperado": esperado,
            "obtido": vse.emocao_primaria,
            "valencia": vse.valencia,
            "arousal": vse.arousal,
            "confianca": vse.score_confianca,
        })
    
    # ── Resumo ──────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("📊 RESUMO")
    print(f"{'='*60}")
    acertos = 0
    for r in resultados:
        ok = "✅" if r["obtido"] != "neutro" or "neutro" in r["esperado"] else "⚠️"
        if "✅" in ok:
            acertos += 1
        print(f"  {ok} {r['nome']:15s} → {r['obtido']:12s} (esperado: {r['esperado']})")
    
    print(f"\n  Classificações não-neutras: {acertos}/{len(testes)}")
    print(f"  Arquivos gerados em: {tmp}/")
    print(f"\n💡 Grave sua própria voz e teste:")
    print(f"   python3 il_voz.py sua_gravacao.wav")


if __name__ == "__main__":
    main()
