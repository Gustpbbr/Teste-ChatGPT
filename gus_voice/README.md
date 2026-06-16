# Gus Voice + Vision — Fase A + B

> Wake word → voz OU visão → responde. 100% offline no S20.

## Instalação

```bash
# Termux + Termux:API (F-Droid)
pkg update && pkg upgrade
pkg install python python-pip termux-api

# Dependências
pip install requests numpy sounddevice pillow
pip install openai-whisper

# Ollama
ollama pull gemma3:4b
```

## Arquivos

| Arquivo | Função |
|---------|--------|
| `gus_voice.py` | Fase A: voz → LLM → TTS |
| `gus_vision.py` | Fase B: câmera → descrição / OCR |
| `gus_full.py` | Integrado: voz + visão |

## Uso

```bash
# Apenas voz
python3 gus_voice.py

# Voz + visão integrados
python3 gus_full.py
```

## Comandos suportados

| Você diz | Gus faz |
|----------|---------|
| "Gus, o que você vê?" | Tira foto e descreve a cena |
| "Gus, o que está escrito?" | OCR — extrai texto da câmera |
| "Gus, analise o vídeo" | 5 frames em 5s, descreve cada |
| Qualquer outra frase | Chat normal com Ollama |

## Arquitetura Completa

```
[Wake Word "Gus"]
       ↓
[Grava áudio 5s] ──→ [Whisper tiny] ──→ texto
       ↓                                      ↓
[Detecta intenção]                    [Comando de câmera?]
       ↓                                      ↓
[Chat normal]                      [Captura foto]
       ↓                                      ↓
[Ollama Gemma] ←────────────────── [Ollama Vision]
       ↓
[Android TTS] ──→ resposta em voz
```

## Próximo: Fase C

Adiciona: screen capture → "Gus, o que tá na tela?"
