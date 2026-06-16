# Matriz de Maturidade

> Grau honesto de cada projeto/componente. Legenda:
> 🟢 **roda** (código funcional verificado) · 🟡 **parcial** (parte roda) ·
> 📄 **spec** (documentado, sem código verificado) · ⏸ **pausado** · ❓ **citado/não especificado**

## Por projeto

| Projeto | Maturidade | Evidência | O que falta |
|---|---|---|---|
| **Phronesis-Bench** | 🟢🟢 | API FastAPI + corpora A–G + **resultados preliminares** (2 modelos) | mais modelos; `results.json` versionado; unificar métricas |
| **MGE** | 🟢 | HTML standalone funcional + n8n v3.0 (18 nós) | proxy p/ uso público; validação semântica entre agentes |
| **CEX / CEP** | 🟢 (CEP) / 🟡 (CEX) | CEP v3.9 = JSON n8n real auditado; CEX v1.1 HTML (specs) | HTML do CEX não achado; bugs ativos; estabilidade de API |
| **Gus** | 🟡 | bot Telegram + Hub Qdrant em produção; `gus_sense` com ~59 testes | fusão completa (corpo+sentidos); blocos 2–5 |
| **TER (memória)** | 📄 | specs densas + chats; registro BN (TEAR) | PoC implementável; só roda via Gus |
| **TER KAI** | 📄 | blueprint grau-patente (pseudocódigo, schemas, PolicyConfig) | código; resolver inconsistência de latência; fórmula do RPE |
| **ACEE** | 📄 | spec grau-patente (Cap-04→09: CMA/ILs/VSE/NCAC) | código; é só especificação |
| **MASE** | ❓ | citado no corpus ACEE como efetor/ambiente físico | spec própria inexistente |
| **MGX** | 📄 | design completo (fases, mgxState, compilador de contexto) | orquestração não construída |
| **MEX** | 📄 | conceito (terceiro motor, materialização) | tudo |
| **Axon** | 📄 | blueprint conceitual + crítica multi-especialista + roadmap 12m | implementação zero; validação com usuários não iniciada |
| **SMI** | ⏸ | memória prudencial / deliberação multiagente | pausado |
| **Segundo Cérebro** | 🟢 | conjunto de briefings/índice em uso (boot de chats) | — (é PKM, não produto) |

## Resumo executivo

- **O que comprovadamente roda hoje:** Phronesis-Bench (+ resultados), MGE (standalone),
  CEP v3.9 (n8n), CEX v1.1, bot Telegram + Hub Qdrant do Gus, `gus_sense` (testes verdes).
- **O que é spec rica sem código:** TER, TER KAI, ACEE, MEX, MGX, Axon.
- **Pausado/citado:** SMI (pausa), MASE (citado).

## Avisos transversais (valem para quase tudo)

1. **Métricas grandiosas = metas, não medições.** Números como ECI≈0.94, δ=0.10, latências
   60/150ms, F1 0.86 são **projeções/alvos de projeto**, não resultados medidos. (Exceção: os
   resultados do Phronesis, que são medições preliminares — com seus próprios caveats.)
2. **Linguagem histórica de "consciência/pré-AGI"** aparece em specs antigas — tratar como
   aspiração, não afirmação técnica. O próprio material reconhece isso.
3. **Relabels entre fontes** (δψρω, Escada de Degraus, Phronesis Digitalis, MEM-LOG): o que a
   consolidação chama X às vezes não aparece com esse nome nos chats brutos. Ver `GLOSSARIO-MESTRE.md`.
4. **Construído por autor não-programador** (todo código via IA) → maturidade de engenharia limitada.
