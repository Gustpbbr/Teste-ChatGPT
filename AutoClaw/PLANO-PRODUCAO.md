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

## 📅 Etapa 2 — Phronesis-Bench Final ✅ CONCLUÍDA

| Item | Detalhe |
|------|---------|
| **O que é** | Framework completo de benchmark de prudência |
| **Stack** | Python + APIs (Anthropic, OpenAI, Google) |
| **Output** | `results.json` + `summary.md` + `radar.html` |
| **Arquivos** | `phronesis/corpora.py`, `metrics.py`, `runner.py`, `visualize.py` |
| **Dependência** | API keys para rodar (código pronto) |
| **Status** | ✅ Framework pronto. Rodar com API keys quando disponível. |

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

## 📅 Etapa 4 — MGE/CEX como APIs ✅ CONCLUÍDA

| Item | Detalhe |
|------|---------|
| **O que é** | FastAPI substituindo HTML standalone |
| **Stack** | Python FastAPI + Anthropic API |
| **Output** | `/mge/generate` (10 agentes) + `/cex/review` (6 dimensões) |
| **Arquivos** | `mge_cex_api/server.py`, `test_client.py` |
| **Status** | ✅ Funcional. `uvicorn server:app --port 8765` |

---

## 📅 Etapa 5 — Gus offline integrado ✅ CONCLUÍDA

| Item | Detalhe |
|------|---------|
| **O que é** | Servidor unificado: Ollama + API REST + memória local |
| **Stack** | Python FastAPI + Ollama + SQLite |
| **Output** | `bash start.sh` → http://localhost:8080 |
| **Arquivos** | `gus_local/server.py`, `memory.py`, `start.sh` |
| **Status** | ✅ Testado: Ollama + memória + health check OK |

---

## 📊 Progresso

```
[✅ 1] ── [✅ 2] ── [⏳ 3] ── [✅ 4] ── [✅ 5]
 80%      80%      0%       80%      80%

✅ 4 de 5 concluídas. Resta apenas Etapa 3 (MASE Fase 1 — precisa de Arduino).

Próxima: Etapa 3 — MASE Fase 1 (Voz→LED)
```
