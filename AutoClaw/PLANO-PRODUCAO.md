# 🦾 Plano de Produção — Etapas

> Cronograma de desenvolvimento progressivo. Cada etapa gera código funcional.
> Atualizado: 17 Jun 2026

---

## 📅 Etapa 1 — ACEE MVP: IL-Voz ✅ CONCLUÍDA

| Item | Detalhe |
|------|---------|
| **O que é** | Interpretador Leve de Voz — áudio → features → emoção |
| **Stack** | Python + Librosa (zero APIs externas) |
| **Output** | VSE (Vetor Simbólico de Emoção) em JSON |
| **Arquivos** | `acee/vse.py`, `acee/il_voz.py`, `acee/demo.py` |
| **Status** | ✅ Funcional. Pipeline testado. |

---

## 📅 Etapa 2 — Phronesis-Bench Final ⏳ Pendente

| Item | Detalhe |
|------|---------|
| **O que é** | Rodar +2 modelos, gerar results.json, radar chart, paper |
| **Stack** | Python + APIs (Anthropic, OpenAI, Google) |
| **Output** | `results.json` + visualização + paper draft |
| **Dependência** | API keys |
| **Status** | ⏳ A fazer |

---

## 📅 Etapa 3 — MASE Fase 1 (Voz → LED) ⏳ Pendente

| Item | Detalhe |
|------|---------|
| **O que é** | Loop completo: microfone → análise de tom → LED RGB |
| **Stack** | Python (host) + Arduino C++ (dispositivo) |
| **Output** | Sistema funcional: falar → luz muda de cor |
| **Dependência** | Arduino Nano + fita LED (~R$110) |
| **Status** | ⏳ A fazer |

---

## 📅 Etapa 4 — MGE/CEX como APIs ⏳ Pendente

| Item | Detalhe |
|------|---------|
| **O que é** | Conversão dos HTML standalone para FastAPI |
| **Stack** | Python FastAPI + Anthropic API |
| **Output** | APIs REST documentadas |
| **Dependência** | API key Anthropic |
| **Status** | ⏳ A fazer |

---

## 📅 Etapa 5 — Gus offline integrado ⏳ Pendente

| Item | Detalhe |
|------|---------|
| **O que é** | Gus completo rodando local (Ollama + Qdrant) |
| **Stack** | Python + Ollama + Qdrant |
| **Dependência** | Ambiente local com Ollama |
| **Status** | ⏳ A fazer (Fase 0 já validada) |

---

## 📊 Progresso

```
[✅ 1] ── [⏳ 2] ── [⏳ 3] ── [⏳ 4] ── [⏳ 5]
 20%      0%       0%       0%       0%

Próxima: Etapa 2 — Phronesis-Bench Final
```
