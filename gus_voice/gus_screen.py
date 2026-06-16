"""
Gus Screen — Análise de Tela (Fase C)
=======================================
Captura a tela do celular e analisa com Ollama Vision.

Funcionalidades:
  1. Captura screenshot (Android screencap nativo)
  2. OCR — extrai todo texto visível
  3. Descreve — resume o que está acontecendo na tela
  4. Analisa — pergunta específica sobre o conteúdo

Pré-requisitos: Nenhum extra (screencap é built-in do Android)

Uso:
  python3 gus_screen.py              → captura e descreve
  python3 gus_screen.py ocr          → extrai texto
  python3 gus_screen.py ask "pergunta" → analisa com pergunta específica
"""

import os
import io
import base64
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("GUS_VISION_MODEL", "gemma3:4b")


def capturar_tela() -> Optional[bytes]:
    """Captura screenshot do Android. Retorna bytes PNG."""
    path = "/tmp/gus_screen.png"
    
    try:
        r = subprocess.run(
            ["screencap", "-p", path],
            capture_output=True, timeout=10
        )
        if r.returncode == 0 and os.path.exists(path):
            data = open(path, "rb").read()
            os.unlink(path)
            if len(data) > 100:  # screenshot válido >100 bytes
                return data
    except:
        pass
    
    # Fallback: termux-api
    try:
        path2 = "/tmp/gus_screen2.png"
        subprocess.run(["termux-screenshot", path2], timeout=10)
        if os.path.exists(path2):
            data = open(path2, "rb").read()
            os.unlink(path2)
            return data
    except:
        pass
    
    return None


def enviar_para_ollama(imagem_bytes: bytes, prompt: str, max_tokens: int = 300) -> str:
    """Envia imagem pro Ollama Vision."""
    b64 = base64.b64encode(imagem_bytes).decode()
    
    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": MODEL,
            "prompt": prompt,
            "images": [b64],
            "stream": False,
            "options": {"num_predict": max_tokens}
        }, timeout=60)
        return r.json().get("response", "").strip()
    except Exception as e:
        return f"Erro: {e}"


def descrever_tela() -> str:
    """Descreve o que está acontecendo na tela."""
    img = capturar_tela()
    if not img:
        return "Não consegui capturar a tela"
    
    return enviar_para_ollama(img, (
        "Esta é uma captura de tela de um celular. "
        "Descreva em português brasileiro, em 2-4 frases curtas: "
        "1) Qual app ou página está aberta? "
        "2) Qual o conteúdo principal? "
        "3) Há algo importante ou urgente visível? "
        "Seja objetivo e direto."
    ))


def extrair_texto_tela() -> str:
    """OCR: extrai todo texto visível na tela."""
    img = capturar_tela()
    if not img:
        return "Não consegui capturar a tela"
    
    return enviar_para_ollama(img, (
        "Extraia TODO o texto visível nesta captura de tela. "
        "Retorne APENAS o texto encontrado, organizado por seção. "
        "Mantenha a formatação original (títulos, parágrafos, listas). "
        "Se houver números, datas, nomes — inclua com precisão. "
        "Se não houver texto, responda 'sem texto na tela'."
    ), max_tokens=500)


def perguntar_sobre_tela(pergunta: str) -> str:
    """Faz uma pergunta específica sobre o conteúdo da tela."""
    img = capturar_tela()
    if not img:
        return "Não consegui capturar a tela"
    
    return enviar_para_ollama(img, (
        f"Analise esta captura de tela e responda à pergunta: {pergunta}\n"
        "Responda em português brasileiro, de forma direta e útil."
    ))


def traduzir_tela(idioma_destino: str = "português") -> str:
    """Traduz o texto da tela para o idioma especificado."""
    img = capturar_tela()
    if not img:
        return "Não consegui capturar a tela"
    
    return enviar_para_ollama(img, (
        f"Traduza todo o texto visível nesta tela para {idioma_destino}. "
        "Mantenha a estrutura e formatação originais. "
        "Retorne APENAS o texto traduzido."
    ), max_tokens=500)


def resumir_tela() -> str:
    """Resumo ultra-conciso da tela (1 frase)."""
    img = capturar_tela()
    if not img:
        return "Não consegui capturar a tela"
    
    return enviar_para_ollama(img, (
        "Resuma esta tela em UMA frase em português. "
        "Apenas o essencial: qual app/site e o que está acontecendo."
    ), max_tokens=80)


# ── Integração com Voz ──────────────────────────────────────────
def comandos_tela() -> dict:
    """Retorna comandos de voz para screen analysis."""
    return {
        "o que tá na tela": descrever_tela,
        "o que está na tela": descrever_tela,
        "descreve a tela": descrever_tela,
        "lê a tela": extrair_texto_tela,
        "leia a tela": extrair_texto_tela,
        "texto da tela": extrair_texto_tela,
        "traduz a tela": traduzir_tela,
        "resume a tela": resumir_tela,
    }


# ── CLI ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2 or sys.argv[1] == "ver":
        print("📱 Capturando tela...")
        print(descrever_tela())
    
    elif sys.argv[1] == "ocr":
        print("📱 Extraindo texto...")
        print(extrair_texto_tela())
    
    elif sys.argv[1] == "resumo":
        print("📱 Resumindo...")
        print(resumir_tela())
    
    elif sys.argv[1] == "traduzir":
        idioma = sys.argv[2] if len(sys.argv) > 2 else "português"
        print(f"📱 Traduzindo para {idioma}...")
        print(traduzir_tela(idioma))
    
    elif sys.argv[1] == "ask" and len(sys.argv) > 2:
        pergunta = " ".join(sys.argv[2:])
        print(f"📱 Analisando: {pergunta}")
        print(perguntar_sobre_tela(pergunta))
    
    else:
        print("Uso:")
        print("  python3 gus_screen.py              → descreve a tela")
        print("  python3 gus_screen.py ocr          → extrai texto")
        print("  python3 gus_screen.py resumo       → resume em 1 frase")
        print("  python3 gus_screen.py traduzir [idioma]  → traduz")
        print("  python3 gus_screen.py ask 'pergunta'     → analisa")
