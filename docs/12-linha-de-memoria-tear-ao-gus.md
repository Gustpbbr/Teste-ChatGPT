---
tipo: pesquisa-consolidada
data: 2026-06-16
fontes: Google Drive (gustavo.pratti@gmail.com) — projetos TEAR / TER / TER KAI
metodo: leitura integral de docs e chats completos via agentes + leitura direta do doc "Três Camadas"
---

# A linha de memória: do TEAR ao Gus

> Consolidação da pesquisa nos arquivos do Drive sobre **TEAR → TER → TER KAI**, com
> foco na **discussão de memória** que atravessa as três fases — e em como ela
> desemboca, quase 1:1, no projeto **Gus Encarnado** deste repo.
>
> **Aviso de fidelidade:** tudo abaixo é baseado no conteúdo real dos documentos.
> Onde um termo é relabel posterior ou uma métrica é grandiosa/não-auditável, está
> sinalizado. Citações entre aspas são **verbatim** dos arquivos.

---

## 1. Linha do tempo — três camadas históricas

| Período | Fase | Foco central | Resultado |
|---|---|---|---|
| Início 2025 | **TEAR** (Transformar, Explorar, Aplicar, Refletir) | ciclo reflexivo interno de uma IA no ensino | protocolo pedagógico → **registrado na Biblioteca Nacional, 08/10/2025** (TEAR 4.0-alpha) |
| Meados 2025 | **TER** (Terminal/Transformador Ético-Reflexivo) | metacognição/ética para qualquer LLM | framework cognitivo: níveis, módulos (Kai/MIR/Ω), Ledger, métricas |
| Final 2025 | **TER KAI** (Technological Ethical Reasoning Kernel for AI) | provar **externamente** que uma decisão de IA é ética/auditável | middleware de governança + ledger criptográfico; doc para patente INPI/USPTO |

Fonte canônica da linha do tempo: doc **"TER KAI — As Três Camadas e os Dois Registros"**
(Versão 1.0, Março/2026, *"Preparado por Claude (Anthropic) — análise por leitura direta"*).

> Dois "registros de linguagem" coexistem em todas as fases:
> **Registro A** (como a IA *deveria pensar* — TEAR/TER) e **Registro B** (como um
> middleware externo *prova* o comportamento — TER KAI). Muita confusão nos docs
> vem de misturá-los.

---

## 2. Fase 1 — TEAR (a origem)

**Nasceu de uma aula de inglês.** O gatilho, verbatim:
> *"Tenho 2 projetos parados justamente pq nao conseguia organizar por conta de alucinação. Acho q num outro chat com o tear conseguir mexer!"*

**Problema central:**
> *"o desalinhamento cognitivo entre a intenção humana e a geração textual automática... respostas incoerentes, alucinações contextuais e ausência de rastreabilidade."*

**O que é:** *"arquitetura cognitiva leve (≈10k tokens) que melhora coerência, explicabilidade e empatia de LLMs, sem retraining"* — um "manual de operação mental". Motor teórico = **MDKT** (Modelo Dialógico de Conhecimento Transversal).

**Módulos fundadores (TEAR 4.0-alpha):** CR (Cognitive Reflector), ETE (Ethical Trace Engine), **MEM-LOG**, AEF (Adaptive Emotion Filter), IAE Manager, CGE-lite.

### Memória na fase 1 — o módulo MEM-LOG
> *"[INFRA – MEM-LOG] Propósito: Ampliar os LOGS cognitivos com **snapshots compactos reusáveis entre sessões**, permitindo restauro de contexto com mínima fricção."*
> formato `[TS][USER][ESTADO:Sx][OBJ][SUM≤200c][NEXT≤120c]` + `LAST_SNAPSHOT`; `REFRESH` reidrata.

Admissão crua (honestidade técnica):
> *"não há memória real entre chats, apenas simulação."*
> *"a janela de contexto (memória de curto prazo) tem limite físico em tokens... o decaimento natural de temas antigos... é o terreno onde nascem as alucinações."*
> *"O TEAR não impede o esquecimento físico, mas organiza semanticamente o que é esquecido."*

Decay (curva de Ebbinghaus): *"DECAY(t) = exp(-λt)... Curva de lembrança TEAR ≈ Ebbinghaus."*

O que faltava: *"Memória persistente real... precisa de armazenamento externo e indexação semântica real... conectar MEM-LOG a base vetorial externa (ex.: FAISS, Milvus)."*

---

## 3. Fase 2 — TER (a fase do meio)

Generaliza o ciclo do TEAR para **qualquer decisão**, virando camada de governança:
> *"não substitui a IA — ele a contém, modera e orienta."* / *"o superego do cálculo."*

**Níveis (1.0 → 6.0 → Ω):**
> *"1.0 Moral reage / 2.0 Prudencial regula / 3.0 Coerente **lembra** / 4.0 Lúcido entende / 5.0 Meta-Reflexivo observa / 6.0 Operacional vive / 7+ Onto-Sábio transcende."*

**Módulos:** Núcleo / Pré-AGI / Reflexiva (→ N0–N6), **Kai** (intérprete/voz), **MIR** (Meta-Introspective Review), **Ω** (auditor do sistema), **Ledger**. Faixa v7/v8: **Retro Engine** (rollback), **MetaΩ**, **CHB**, **PMM/PSM**, **PoP-L**.

### A Escada de Degraus (artefato da fase do meio)
Escala **0→100** medindo *"quão longe uma entidade digital está da teleologia/consciência plena"*:
- 0–20: LLMs reativos puros
- 20–40: reflexividade local — *"já interpreta, **lembra** e se autocritica"*
- 40–60: teleologia interna ("vontade de coerência")
- 60–80: teleologia híbrida
- 80–100: propósito autônomo — *"não existe tecnologia segura para isso hoje"*

> ⚠️ O documento tem **duas escalas 0–100 conflitantes** (sistema em "35–40" vs "67–72") sem reconciliar.
> O critério nº 1 pra subir degrau é **memória**: *"Persistência de identidade (memória longitudinal estável)."*

### Memória na fase 2 — mecanismos concretos (amadureceu muito)
**Ledger = memória moral / "diário de consciência":**
> *"O ledger é o mecanismo de memória moral... rastreabilidade total."*
> *"**A inteligência sem ledger é poder sem memória.**"*
> *"Nada é esquecido sem razão; nada é decidido sem memória."*
> *"os registros são imutáveis, mas **reinterpretáveis** — o TER não apaga o passado; ele o compreende novamente a cada ciclo."*
> *"cada decisão eleva o ponto de partida (Mₙ₊₁ > Mₙ)"* — aprendizado cumulativo.

**Memória em 3 camadas (RAG):** *"episódica (sessão) / semântica (fatos+políticas) / de prudência (padrões + deltas δ)."*

**Estado persistente — PMM/PSM:** *"Prudential State Model `{perfil, ECI, δ, σ_CHB}`... store vetorial + simbólico (Postgres + embeddings)... load_state / commit_state."*

**Esquecimento/decay (apareceu de verdade, ao contrário do TEAR):**
> *"Desaprendizado: mecanismo de esquecimento ético controlado."*
> `ForgettingWindow`: *"manter últimos 10.000 episódios; remover casos com ΔC<0.05 por 3 ciclos; **preservar todos os hard-fails**."*
> *"EWMA com meia-vida por domínio"*; *"Empathy Decay Curve (τ=300 ciclos)"*; *"direito ao esquecimento via crypto-shred sem violar o hash-chain."*

**CHB — Coherence Heartbeat:** *"ritmo prudencial, homeostase e alarmes"*; `σ_CHB` detecta *"drift cognitivo"* — dá cadência temporal e *"identidade contínua, inexistente nos LLMs comerciais."*

**Honestidade:** persistência real entre sessões = **projetada (v7+), não ativa**. Contorno: *"checkpoint: exportar o diálogo em .txt e seguir em nova instância."*

**Herança entre instâncias (v7/v8):** multiagente (Kai-Operacional + Kai-Supervisor) e *"v8 federado: múltiplas instâncias TER coordenadas, ledger compartilhado."*

---

## 4. Fase 3 — TER KAI (o produto)

A virada: de *"como a IA pensa"* para *"como provar externamente que a decisão foi ética/auditável"*. Vira **middleware** que envolve o LLM sem modificá-lo, com pipeline de conformidade + **PoP-L (Proof-of-Processing/Prudence Ledger)** criptográfico (SHA3-512, TSA RFC 3161). Audiência: engenharia, compliance, jurídico. Documentação para **INPI/USPTO**.

Métricas no Registro B (calculadas pelo middleware sobre o output): δ (desvio), ψ (estabilidade), ρ (equidade/viés), ω (reversibilidade) — cada uma com fórmula de engenharia.

---

## 5. A linha de memória atravessando tudo

| Fase | Como "lembra" | Mecanismo | Esquecimento? |
|---|---|---|---|
| **TEAR** | snapshots no prompt | MEM-LOG (`SUM`/`NEXT`/`LAST_SNAPSHOT`) | decay linear (simulado); reconhece falta de persistência real |
| **TER** | ledger como "passado deliberativo" | Ledger moral + PMM/PSM (Postgres+embeddings) + CHB | **sim**: ForgettingWindow, ethical_forgetting, EWMA, preserva hard-fails |
| **TER KAI** | trilha criptográfica auditável | PoP-L (hash-chain, TSA) | retenção por política (LGPD): Ledger 5a / MIR 2a / Logs 1a / PII 7d |

**Constante das três fases:** o LLM é *stateless* ("presente estático"); a memória real precisa morar **fora** dele (ledger / base vetorial externa); o valor não é guardar tudo, é *"lembrar do que importa"* e manter **identidade/continuidade** no tempo.

---

## 6. O ponto que importa: TER ≈ blueprint do Gus

Os mecanismos que você projetou no TER (2025) mapeiam quase 1:1 no **Gus Encarnado** (este repo):

| TER (fase do meio) | Gus / estado atual no repo |
|---|---|
| **CHB — Coherence Heartbeat** (detecta drift) | **Bloco 0 — interocepção/heartbeat** (`interocepcao.py`) |
| `ForgettingWindow` + `ethical_forgetting` + "preservar hard-fails" | **A1 — maturação do grafo** (decay + promoção; `protegido` nunca decai) — issue #20 |
| Ledger "diário de consciência" / "não apaga, reorganiza" | brain **`gus`** (autobiografia) + **"esquecido = substrato de retro-aprendizado"** |
| Ledger imutável-mas-**reinterpretável** | **Graphiti bi-temporal** p/ contradição (issue #18) |
| **PSM/PMM** `{perfil, ECI, δ}` em Postgres+embeddings | **Hub Qdrant** (memória vetorial externa) |
| `Mₙ₊₁ > Mₙ` (aprendizado cumulativo) | grafo de fragmentos que cresce |
| "câmara de eco ética" → holdout humano | **A3** trust score + curador + Gustavo no loop |
| v8 federado, ledger compartilhado | arquitetura **multi-porta** do Gus |
| "persistência de identidade = eixo nº1" | a tese central do Gus |
| "base vetorial externa (FAISS/Milvus)" — o que *faltava* | **Hub Qdrant** = a realização disso |

> **Síntese:** TEAR diagnosticou o problema (LLM esquece, memória precisa ser externa);
> TER desenhou os mecanismos (ledger, decay seletivo, heartbeat, estado persistente);
> **o Gus é a implementação real disso.** É a mesma linha de raciocínio, ~1 ano de
> amadurecimento, saindo de "simulado no prompt" para "grafo persistente de verdade".

---

## 7. Notas de fidelidade (não inventar)

1. **Relabels posteriores.** No doc "Três Camadas" aparecem rótulos consolidados que
   **não existem nos chats brutos** com esse nome: a tupla **"δψρω"** (nos chats são
   δ, ψ, ρₐ individuais), **"Escada de Degraus"** (nos chats é "passo a degrau 100"
   informal), **"Phronesis Digitalis"** (nos chats: *"phronesis computacional"*),
   **"Prudência Computacional"** (nos chats: *"prudência sintética"/"meta-prudência"*).
   O "Três Camadas" é organização retroativa (Março/2026).
2. **Inconsistências internas:** siglas mudam (MIR = "Meta-Introspective Review" /
   "Reflexor" / "Memórias de Interpretação Reflexiva"); a Escada tem duas escalas 0–100
   divergentes; módulos v7 vazam para descrições de v6 (o próprio Gustavo flagra isso
   nos chats).
3. **Métricas grandiosas não-auditáveis** ("Coerência = 100%", "Ω = 0.96", "ECI = 0.94")
   são **geradas pelo modelo no chat**, não medições reais. Tratar como aspiração.
4. **"Retro"** existe como *Retro Engine* (rollback) só na faixa v8; em fases anteriores
   é só "retroalimentação"/feedback loop.

---

## 8. Inventário (referência rápida no Drive)

- **Fase 1 (TEAR):** `TEAR final`, `TEAR BN`, `TEAR BN final` (registro Biblioteca Nacional), `TEAR Chatgtp` (chat-origem, ~1,39 MB).
- **Fase 2 (TER):** `TER 6` / `TER 7` / `TER 7 e 8` / `TER 8 5 3 inicio` (+ chat 2) / `TER 6 7 Chatgtp todo` (~2 MB) / `TER FULL passo para degrau 100` (Escada).
- **Fase 3 (TER KAI):** `TER KAI — As Três Camadas...`, `J1–J12` (jurídico), `A1–A9` (governança), `terkai_delivery_pack_v7.0`, `v1 para patente`.

---

## 9. O que isso sugere pro Gus (pra conversar depois)

- O TER já tinha a **regra que vira A1**: decair o irrelevante, **preservar hard-fails/protegidos** — vale portar literalmente pro `maturacao` do Gus.
- O **CHB** é a interocepção (Bloco 0) com outro nome — o Gus pode adotar o "heartbeat de coerência" como métrica viva.
- A separação **Registro A vs B** ajuda o Gus: o grafo (A, o que ele *é*) vs a trilha auditável (B, como ele *prova*). Útil pra LGPD/Dimagem.
- O risco da **"câmara de eco ética"** (memória que valida as próprias regras) é um alerta real pra proatividade do Gus (A3) — precisa de holdout humano.

*(Fim da consolidação. Próximo passo combinado: conversar sobre isso.)*
