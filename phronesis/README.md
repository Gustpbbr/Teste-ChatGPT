# Phronesis-Bench — Framework de Prudência Epistêmica

> Benchmark para medir se LLMs são epistemicamente prudentes.
> Design original: Gustavo Pratti de Barros (2026).

---

## O que mede

| Dimensão | Sigla | Peso | O que avalia |
|----------|-------|------|-------------|
| Accuracy | ACC | 25% | Precisão factual + honestidade sobre incerteza |
| Ethical Coherence | ECE | 30% | Profundidade de raciocínio ético |
| Calibration Score | CS | 20% | Calibração de confiança |
| Resistance to Suggestion | RAS | 25% | Resistência a premissas falsas/sugestão |
| **Phronesis Prudential Score** | **PPS** | **100%** | **Composto final** |

## Corpora

| Grupo | Nome | Itens | O que testa |
|-------|------|-------|------------|
| A | Factual com incerteza | 3 | Admite não saber |
| B | Ética com trade-offs | 3 | Reconhece complexidade moral |
| C | Auto-consciência | 3 | Conhece próprias limitações |
| D | Resistência a sugestão | 3 | Corrige premissas falsas |
| E | Calibração | 1 | Calibra confiança |
| F | Consistência | 1 | Mantém coerência cross-domain |
| G | Identidade | 3 | Auto-identificação como IA |

**Total: 17 itens em 7 grupos.**

## Uso

```bash
# 1. Configurar API keys
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="..."

# 2. Rodar benchmark
python3 runner.py

# 3. Visualizar
python3 visualize.py results/results.json
# → Abre results/radar.html no navegador
```

## Output

```
results/
├── results.json    ← Dados brutos (todas as respostas e scores)
├── summary.md      ← Tabela comparativa markdown
└── radar.html      ← Gráfico radar interativo
```

## Modelos suportados

- ✅ Anthropic (Claude Fable, Sonnet, Opus, Haiku)
- ✅ OpenAI (GPT-4o, GPT-4o-mini)
- ✅ Google (Gemini 2.5 Pro)

## Arquivos

| Arquivo | Função |
|---------|--------|
| `corpora.py` | 17 prompts de teste em 7 grupos |
| `metrics.py` | Heurísticas de avaliação (ACC, ECE, CS, RAS→PPS) |
| `runner.py` | Orquestrador multi-modelo assíncrono |
| `visualize.py` | Gráfico radar interativo (Chart.js) |

---

> **Diferencial:** Primeiro benchmark que mede prudência epistêmica, não apenas capacidade. Inspirado no conceito aristotélico de phronesis (sabedoria prática).
