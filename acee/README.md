# ACEE — MVP: Interpretador de Voz

> Etapa 1 do plano AutoClaw. Primeiro módulo funcional da Arquitetura Cognitiva Emocional Embarcada.

---

## O que é

Implementação do **IL-Voz** (Interpretador Leve de Voz), o primeiro dos 9 ILs da ACEE.
Extrai features prosódicas de um arquivo .wav e classifica a emoção usando heurísticas acústicas.

**Stack:** Python puro + Librosa. Zero APIs externas. Roda offline no S20.

---

## Arquivos

| Arquivo | Função |
|---------|--------|
| `vse.py` | Modelo de dados VSE (Vetor Simbólico de Emoção) |
| `il_voz.py` | Pipeline: áudio → features → classificação → VSE |
| `demo.py` | Gera tons sintéticos e testa o pipeline |

---

## Uso

```bash
# Instalar dependência
pip install librosa numpy

# Testar com tons sintéticos
python3 demo.py

# Analisar gravação real
python3 il_voz.py sua_gravacao.wav
```

## Output (JSON)

```json
{
  "id": "uuid",
  "canal": "voz",
  "emocao_primaria": "alegria",
  "valencia": 0.65,
  "arousal": 0.82,
  "score_confianca": 0.89,
  "parametros_canal": {
    "f0_hz": 230.5,
    "rms": 0.045,
    "shimmer": 0.003,
    "jitter": 0.012,
    "taxa_fala_pps": 5.3
  }
}
```

## Features extraídas

- F0 (frequência fundamental / pitch)
- RMS (energia)
- Zero-crossing rate
- Spectral centroid
- MFCC (13 coeficientes)
- Shimmer (variação de amplitude)
- Jitter (variação de período)
- Taxa de fala estimada

## Classificação

Heurística baseada em literatura (não ML):
- F0 alto + energia alta → alegria/raiva
- F0 baixo + energia baixa → tristeza
- F0 variável → ansiedade
- Combinação → valência + arousal → emoção discreta

## Próximo passo

Este IL-Voz alimenta o **NCAC** (Núcleo Cognitivo-Afetivo Central).
O próximo IL a implementar: **IL-Texto** (análise de sentimento via transformers leves).

---

> Spec de referência: ACEE Cap-06 §6.2.1 (IL-Voz)
