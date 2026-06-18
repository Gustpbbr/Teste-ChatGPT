# CEX / CEP — Comitê de Especialistas · briefing

> 🟢 **CEP v3.9 (n8n, código real)** / 🟡 **CEX v1.1 (HTML)**.
> Detalhe técnico completo em [`deep-dive.md`](deep-dive.md).

## O que é
Um sistema de **deliberação adversarial por comitê** de especialistas **gerados dinamicamente**.
Dado uma decisão ou conceito, convoca uma "banca", faz os especialistas debaterem entre si, e
chega a um veredito auditável. CEX é a evolução do CEP (de comitê fixo → banca dinâmica).

## Como funciona
Pipeline de **11 etapas**: Kai (interpreta) → Maestro (convoca banca 4–5 especialistas com pesos)
→ Auditor de Bancada → Análise Cega → Coverage/Convergência → Cross-Examination (debate circular)
→ Defesa → DeltaU (incertezas) → Motor de Regras → **Compositor Dialético** (arbitra por
**resistência de argumento, não média**) → Auditor Interno. Dois modos: **Deliberação** (risco/
conformidade) e **Avaliação de Conceito** (viabilidade).

## Por que importa
- Deliberação **prudente e auditável** — mostra o debate, as dissidências e o porquê do veredito.
- Arbitragem por força de argumento (não voto médio) + auditor de rigor (detecta debate "teatral").
- O **CEP v3.9 é código n8n real** (pesos hardcoded, motor de regras determinístico).

## Limitações honestas
- CEX v1.1: bugs de estabilidade de API e truncamento de JSON (mitigados, não 100% resolvidos).
- O HTML standalone do CEX não foi localizado nas fontes (documentado, não confirmado).
- Será integrado ao MGX como motor de validação — integração ainda não construída.

**Fonte:** Drive (`cex-001`, pasta `CEP`, JSON n8n `CEP_v3_9_final`). Co-criado com ChatGPT/Kai.
