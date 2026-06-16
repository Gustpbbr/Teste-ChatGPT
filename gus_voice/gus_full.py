"""
Gus Voice + Vision — Integrado (Fase A + B)
=============================================
Wake word → voz OU visão → responde.

Comandos de voz suportados:
  "Gus, o que você vê?"       → tira foto e descreve
  "Gus, o que está escrito?"  → OCR da câmera
  "Gus, analise o vídeo"      → captura 5 frames e descreve cada
  [qualquer outra frase]      → chat normal com Ollama

Uso: python3 gus_full.py
"""

import sys
from pathlib import Path

# Adiciona diretório atual pro import
sys.path.insert(0, str(Path(__file__).parent))

from gus_voice import (
    init, speak, transcribe, record, chat, listen_for_wake, OLLAMA_URL
)
from gus_vision import capturar, descrever, extrair_texto, analisar_video


def detectar_comando(texto: str) -> tuple[str, str]:
    """Detecta intenção do comando de voz. Retorna (modo, prompt/extra)."""
    t = texto.lower()
    
    if any(p in t for p in ["o que você vê", "o que vc vê", "o que tá vendo", "descreva a cena"]):
        return "visao", "O que você vê nesta imagem?"
    
    if any(p in t for p in ["o que está escrito", "lê isso", "leia a tela", "texto da tela"]):
        return "ocr", ""
    
    if any(p in t for p in ["analise o vídeo", "analisar vídeo", "gravar cena"]):
        return "video", ""
    
    return "chat", texto


def executar_comando(modo: str, prompt: str) -> str:
    """Executa o comando detectado."""
    if modo == "visao":
        print("📷 Capturando...")
        img = capturar()
        if img:
            return descrever(img, prompt)
        return "Não consegui acessar a câmera"
    
    elif modo == "ocr":
        print("📷 Capturando para OCR...")
        img = capturar()
        if img:
            return extrair_texto(img)
        return "Não consegui acessar a câmera"
    
    elif modo == "video":
        frames = analisar_video(duracao_s=5, intervalo_s=1.0)
        if frames:
            return "Análise do vídeo:\n" + "\n".join(f"• {d}" for d in frames)
        return "Não consegui capturar frames"
    
    else:
        return chat(prompt)


def main():
    init()
    
    import requests
    try:
        requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        print("✅ Ollama online\n")
    except:
        print("❌ Ollama offline\n")
        return
    
    print("Comandos: 'o que você vê' | 'o que está escrito' | 'analise o vídeo'\n")
    
    try:
        while True:
            if not listen_for_wake():
                break
            
            audio = record()
            if audio is None:
                continue
            
            print("📝 Transcrevendo...")
            texto = transcribe(audio)
            if not texto or texto == "erro_na_transcricao":
                speak("Não entendi. Pode repetir?")
                continue
            
            print(f"💬 Você: {texto}")
            
            modo, prompt = detectar_comando(texto)
            print(f"   → Modo: {modo}")
            
            resposta = executar_comando(modo, prompt)
            print(f"🦾 Gus: {resposta}")
            speak(resposta)
            print()
            
    except KeyboardInterrupt:
        print("\n👋 Até mais!")
        speak("Até mais!")


if __name__ == "__main__":
    main()
