"""
Gus Voice — Assistente por Voz (Fase A)
=========================================
Wake word "Gus" → grava áudio → transcreve → Ollama → responde com voz.

Funcionamento:
  1. Escuta continuamente pela wake word "Gus" (Porcupine)
  2. Ao detectar, grava 5 segundos de áudio
  3. Transcreve usando Whisper tiny (offline) ou fallback Ollama
  4. Envia texto pro Ollama (Gemma) com system prompt do Gus
  5. Responde em voz alta via TTS do Android

Pré-requisitos no Termux:
  pkg install python python-pip termux-api
  pip install pvporcupine numpy sounddevice requests
  pip install openai-whisper  # ou: pip install faster-whisper

  # Instalar Termux:API do F-Droid (app separado) para TTS
  # Dar permissão de microfone ao Termux

Uso:
  python3 gus_voice.py
"""

import os
import sys
import json
import time
import wave
import io
import tempfile
from pathlib import Path
from threading import Thread
from typing import Optional

# ── Config ────────────────────────────────────────────────────────
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_LLM = os.getenv("GUS_MODEL", "gemma3:4b")
SAMPLE_RATE = 16000
RECORD_SECONDS = 5
WAKE_WORD = "gus"

# ── System Prompt ─────────────────────────────────────────────────
SYSTEM = """Você é o Gus, assistente pessoal do Gustavo.
Responda SEMPRE em português brasileiro.
Seja extremamente conciso — 1 a 3 frases curtas no máximo.
Respostas diretas, informais, úteis. Sem enrolação.
Você está rodando offline num Galaxy S20."""


# ── Inicialização ─────────────────────────────────────────────────
_tts_available = False
_stt_available = False
_whisper_model = None


def init():
    """Verifica dependências disponíveis."""
    global _tts_available, _stt_available
    
    # TTS via termux-api
    try:
        import subprocess
        r = subprocess.run(["termux-tts-speak", "teste"], capture_output=True, timeout=5)
        _tts_available = r.returncode == 0
    except:
        _tts_available = False
    
    # STT via whisper
    try:
        import whisper
        _stt_available = True
    except ImportError:
        _stt_available = False
    
    print(f"🎤 Gus Voice — Inicializando...")
    print(f"   TTS (termux-api): {'✅' if _tts_available else '❌'}")
    print(f"   STT (whisper):    {'✅' if _stt_available else '❌ (fallback: Ollama)'}")
    
    if not _tts_available:
        print("   ⚠️  Instale Termux:API do F-Droid para voz")


# ── TTS ───────────────────────────────────────────────────────────
def speak(text: str):
    """Fala o texto usando TTS do Android."""
    text = text.strip()
    if not text:
        return
    print(f"🔊 Gus: {text}")
    if _tts_available:
        try:
            import subprocess
            subprocess.run(["termux-tts-speak", text], timeout=15)
        except:
            pass


# ── STT (Speech-to-Text) ─────────────────────────────────────────
def transcribe(audio_data: bytes) -> str:
    """Transcreve áudio para texto."""
    if _stt_available:
        return _transcribe_whisper(audio_data)
    return _transcribe_ollama(audio_data)


def _transcribe_whisper(audio_data: bytes) -> str:
    """Usa Whisper tiny local."""
    global _whisper_model
    import whisper
    import numpy as np
    
    if _whisper_model is None:
        print("   📥 Carregando Whisper tiny (~150MB, só na primeira vez)...")
        _whisper_model = whisper.load_model("tiny")
    
    # Converte bytes → numpy array
    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    
    result = _whisper_model.transcribe(audio_np, language="pt", fp16=False)
    return result["text"].strip()


def _transcribe_ollama(audio_data: bytes) -> str:
    """Fallback: usa Ollama como STT (menos preciso, mas sem dependência extra)."""
    # Salva em arquivo temporário
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_data)
        f.flush()
        path = f.name
    
    try:
        # Converte WAV → base64
        import base64
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        import requests
        r = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": MODEL_LLM,
            "prompt": "Transcreva EXATAMENTE o áudio em português. Retorne APENAS a transcrição, sem comentários.",
            "images": [b64],
            "stream": False,
        }, timeout=60)
        return r.json().get("response", "").strip()
    except:
        return "erro_na_transcricao"
    finally:
        os.unlink(path)


# ── Gravação ──────────────────────────────────────────────────────
def record(duration: int = RECORD_SECONDS) -> Optional[bytes]:
    """Grava áudio do microfone."""
    try:
        import sounddevice as sd
        import numpy as np
        
        print(f"🎙️  Gravando {duration}s...")
        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='int16'
        )
        sd.wait()
        
        # Converte pra WAV bytes
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SAMPLE_RATE)
            w.writeframes(audio.tobytes())
        return buf.getvalue()
    
    except ImportError:
        # Fallback: usa termux-microphone-record
        try:
            import subprocess
            path = "/tmp/gus_recording.wav"
            subprocess.run([
                "termux-microphone-record",
                "-f", path,
                "-l", str(duration),
                "-b", "16",
                "-r", str(SAMPLE_RATE),
            ], timeout=duration + 5)
            if os.path.exists(path):
                data = open(path, "rb").read()
                os.unlink(path)
                return data
        except:
            pass
        return None


# ── LLM ───────────────────────────────────────────────────────────
def chat(prompt: str, contexto: str = "") -> str:
    """Envia prompt pro Ollama e retorna resposta."""
    import requests
    
    messages = [{"role": "system", "content": SYSTEM}]
    if contexto:
        messages.append({"role": "system", "content": contexto})
    messages.append({"role": "user", "content": prompt})
    
    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat", json={
            "model": MODEL_LLM,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 150}
        }, timeout=60)
        return r.json().get("message", {}).get("content", "").strip()
    except Exception as e:
        return f"Erro: {e}"


# ── Wake Word Detection ───────────────────────────────────────────
def listen_for_wake():
    """Escuta continuamente pela wake word usando Porcupine."""
    try:
        import pvporcupine
        import pyaudio
        import struct
        
        # Tenta carregar keyword "Gus" (precisa de access key gratuita)
        # Fallback: keyword pré-treinada "computer" + renomeia
        porcupine = pvporcupine.create(
            access_key=os.getenv("PICOVOICE_KEY", ""),
            keywords=["computer"]  # "Gus" precisaria de custom keyword
        )
        
        pa = pyaudio.PyAudio()
        stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        
        print(f"👂 Aguardando 'Gus'... (Ctrl+C para sair)")
        
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            if porcupine.process(pcm_unpacked) >= 0:
                print("🎯 Wake word detectada!")
                return True
                
    except ImportError:
        # Fallback: modo simples — tecla Enter como wake
        print("⚠️  Porcupine não instalado. Modo manual: pressione Enter para falar.")
        try:
            input()
            return True
        except (EOFError, KeyboardInterrupt):
            return False


# ── Loop Principal ────────────────────────────────────────────────
def main():
    init()
    
    # Verifica Ollama
    import requests
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        print(f"✅ Ollama online — modelo: {MODEL_LLM}\n")
    except:
        print("❌ Ollama offline. Execute: ollama serve\n")
        return
    
    # Histórico simples
    contexto = ""
    
    try:
        while True:
            if not listen_for_wake():
                break
            
            # Grava
            audio = record()
            if audio is None:
                print("❌ Erro na gravação")
                continue
            
            # Transcreve
            print("📝 Transcrevendo...")
            texto = transcribe(audio)
            if not texto or texto == "erro_na_transcricao":
                print("❌ Não entendi")
                speak("Desculpe, não entendi. Pode repetir?")
                continue
            
            print(f"💬 Você: {texto}")
            
            # Responde
            print("🤔 Pensando...")
            resposta = chat(texto, contexto)
            
            # Atualiza contexto (últimas 2 interações)
            contexto = f"Última interação:\nUsuário: {texto}\nGus: {resposta[:200]}"
            
            # Fala
            speak(resposta)
            print()
            
    except KeyboardInterrupt:
        print("\n👋 Até mais!")
        speak("Até mais, Gustavo!")


if __name__ == "__main__":
    main()
