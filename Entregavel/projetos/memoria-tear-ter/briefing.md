# Linha de memória: TEAR → TER → Gus — briefing

> 📄 **Estado: TESE MADURA + specs + logs de conversa.** Pouco código; muita formulação.
> Fonte: Google Drive (pastas TEAR/TER) e repos com os dumps. Síntese técnica detalhada
> em `docs/12-linha-de-memoria-tear-ao-gus.md` do repo Gus Encarnado.

## A ideia única que atravessa tudo

> **O LLM é *stateless* ("presente estático"); a memória real precisa morar fora dele.
> A identidade vive num grafo persistente, não no modelo.**

Formulado por conta própria em 2025. Em 2026 é exatamente para onde o campo convergiu
(Letta, Mem0, Zep/Graphiti).

## As três fases

1. **TEAR** (início 2025) — protocolo reflexivo nascido do **ensino de inglês**; vira
   arquitetura cognitiva leve (~10k tokens) sobre o LLM, sem retraining. **Registrado na
   Biblioteca Nacional (08/10/2025).** Módulo de memória: **MEM-LOG** (snapshots reusáveis
   entre sessões). Reconhece honestamente: *"não há memória real entre chats, apenas simulação"*.
2. **TER** (meados 2025) — generaliza para metacognição/ética de qualquer LLM. Aqui a memória
   amadurece: **Ledger** como "memória moral" (*"imutável mas reinterpretável — não apaga o
   passado, compreende de novo"*), **3 camadas RAG** (episódica/semântica/prudencial),
   **PMM/PSM** (estado persistente), **esquecimento controlado** (`ForgettingWindow`,
   preserva hard-fails; decay EWMA), e **CHB (Coherence Heartbeat)** — ritmo temporal que
   detecta *drift*. Níveis 1.0→6.0→Ω.
3. **Gus** (2026) — a implementação real: Hub vetorial (Qdrant), grafo de fragmentos, dois
   "cérebros" (memórias do usuário + autobiografia do agente), multi-porta.

## Por que importa

- A tese antecipou o campo e tem **recorte próprio** (memória + prudência + afeto + local),
  não "mais um framework de memória".
- Os mecanismos do TER mapeiam quase 1:1 em conceitos hoje validados: `ForgettingWindow`
  ≈ memória auto-editada (Letta); Ledger reinterpretável ≈ grafo bi-temporal (Graphiti);
  CHB ≈ detecção de drift.

## Limitações honestas

- É **spec + transcrição de conversa**, não sistema rodando (exceto o Gus, parcial).
- Terminologia inconsistente entre versões; siglas mudam.
- Os chats têm **métricas grandiosas e linguagem de "consciência/pré-AGI"** — tratar como
  aspiração histórica, não resultado.
