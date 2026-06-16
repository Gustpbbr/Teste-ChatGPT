# Gus Voice — Assistente por Voz (Fase A)

> Wake word → grava → transcreve → Ollama → TTS. 100% offline.

## Instalação (S20 + Termux)

```bash
# 1. Instalar apps (F-Droid)
#    - Termux
#    - Termux:API (para TTS e microfone)

# 2. No Termux:
pkg update && pkg upgrade
pkg install python python-pip termux-api

# 3. Dependências Python
pip install requests numpy sounddevice
pip install openai-whisper    # Whisper tiny (~150 MB)

# 4. Ollama (já instalado da Fase 0)
ollama serve &
ollama pull gemma3:4b
```

## Uso

```bash
python3 gus_voice.py
# → Fala "Gus" (ou pressiona Enter no modo manual)
# → Faça sua pergunta
# → Gus responde em voz
```

## Modos

| Componente | Opção A (completo) | Opção B (fallback) |
|-----------|-------------------|-------------------|
| Wake word | Porcupine "Gus" | Pressionar Enter |
| STT | Whisper tiny | Ollama (transcrição) |
| LLM | Gemma 4B | — |
| TTS | Android nativo | ❌ (só texto) |

## Arquitetura

```
[Porcupine] ──wake──→ [Gravação 5s] ──bytes──→ [Whisper tiny]
                                                      ↓
[Android TTS] ←──texto── [Ollama Gemma] ←──texto── [Transcrição]
```

## Próximo: Fase B

Adiciona: câmera → captura frame → classificação → "Gus, o que você vê?"
