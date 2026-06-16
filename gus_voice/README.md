# Gus Voice + Vision + Screen — Fase A + B + C

> Assistente completo: voz, câmera, tela. 100% offline no S20.

## Comandos de Voz

| Você diz | Gus faz |
|----------|---------|
| "Gus, o que você vê?" | Câmera: tira foto e descreve |
| "Gus, o que está escrito?" | Câmera: OCR |
| "Gus, analise o vídeo" | Câmera: 5 frames em 5s |
| "Gus, o que tá na tela?" | Tela: screenshot e descrição |
| "Gus, lê a tela" | Tela: extrai texto |
| "Gus, resume a tela" | Tela: 1 frase |
| Qualquer outra frase | Chat com Ollama |

## Arquivos

| Arquivo | Função |
|---------|--------|
| `gus_voice.py` | Fase A: voz pura |
| `gus_vision.py` | Fase B: câmera |
| `gus_screen.py` | Fase C: tela |
| `gus_full.py` | Integrado: voz + câmera + tela |

## CLI (sem voz)

```bash
python3 gus_voice.py      # Chat por voz
python3 gus_screen.py     # Descreve tela
python3 gus_screen.py ocr # Extrai texto da tela
python3 gus_screen.py ask "essa fatura está certa?"
```

## Arquitetura Final

```
[Wake Word "Gus"]
       ↓
[Grava áudio] → [Whisper] → texto
       ↓
[Detecta intenção]
       ↓
  ┌────┼────┬──────────┐
  ↓    ↓    ↓          ↓
Chat Câmera Tela     Vídeo
  ↓    ↓    ↓          ↓
  └────┴────┴──────────┘
       ↓
[Ollama Gemma 4B]
       ↓
[Android TTS] → voz
```
