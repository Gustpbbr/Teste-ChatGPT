---
tipo: deep-dive-tecnico
projeto: linha-de-memoria-tear-ter
data: 2026-06-16
foco: MEMÓRIA + metacognição/ética (TEAR → TER)
fontes_primarias:
  - /tmp/TEAR_Chatgtp.txt (chat-origem TEAR, ~1,39 MB)
  - /tmp/TEAR_final.txt (spec TEAR consolidada)
  - /tmp/TEAR_BN_final.txt (registro Biblioteca Nacional)
  - /tmp/ter6.txt, /tmp/ter67.txt (chats TER 6/7, ~2 MB)
  - /tmp/ter1.txt, /tmp/ter2.txt (chats TER 8)
sintese_de_apoio: docs/12-linha-de-memoria-tear-ao-gus.md
aviso: real vs spec sinalizado no texto; citações entre aspas são VERBATIM dos arquivos;
       métricas grandiosas ("ECI=0.94", "Coerência=100%") são geradas pelo modelo no chat,
       não medições — tratar como aspiração. Nunca "consciente de verdade".
---

# Deep-dive técnico: a linha de memória TEAR → TER

> Este documento foca **memória** (persistência, esquecimento, identidade no tempo) e
> a **metacognição/ética** que a usa. Para a linha completa até o Gus, ver o briefing
> ao lado e `docs/12-linha-de-memoria-tear-ao-gus.md`. Aqui vou fundo, e separo sem dó
> **o que existe nos chats** do **que só aparece como rótulo/spec posterior**.

---

## 1. Resumo

A linha TEAR → TER é, no fundo, **uma única tese sobre memória** desenvolvida ao longo
de ~1 ano (2025) por Gustavo Pratti em conversas com LLMs: *o modelo de linguagem é
stateless — um "presente estático" — então a memória, a identidade e a continuidade têm
que morar **fora** dele*. As duas fases atacam o mesmo problema em altitudes diferentes:

- **TEAR** (início 2025): protocolo cognitivo leve injetado no prompt (~10k tokens, sem
  retraining). A memória é o módulo **MEM-LOG**: snapshots simbólicos compactos
  (`SUM`/`NEXT`/`LAST_SNAPSHOT`) que tentam costurar o fio entre sessões. Reconhece com
  honestidade que *"não há memória real entre chats, apenas simulação"*. Registrado na
  **Biblioteca Nacional (08/10/2025)**.
- **TER** (meados/fim 2025): generaliza o ciclo reflexivo do TEAR para qualquer decisão
  e vira **camada de governança ética**. A memória amadurece de verdade: o **Ledger**
  (Postgres, append-only, hash-chain) como "memória moral" auditável; uma **memória
  hierárquica** (episódica/semântica/prudencial); **esquecimento controlado**
  (crypto-shred sobre cifra, sem quebrar o hash-chain); e a ideia de **identidade
  longitudinal** que aprende sobre o próprio modo de decidir (v8.5).

O ponto honesto: **TEAR tem spec densa + chat-origem; TER tem chats densos + specs de
arquitetura, mas pouquíssimo código rodando**. Vários termos "consolidados" do material
(δψρω como tupla, "Escada de Degraus", "Phronesis Digitalis", "CHB", "PMM/PSM",
"ForgettingWindow", "EWMA") são **relabels/spec retroativa — NÃO foram encontrados com
esse nome nos chats brutos** (detalhe na §5). O valor não está nas métricas grandiosas
(são aspiração); está na **intuição arquitetural**, que antecipou o que o campo
(Letta/Mem0/Zep) validaria em 2026.

---

## 2. Tese e problema

### 2.1 O LLM é stateless — "modelo descartável"

A dor que origina tudo, verbatim do chat TEAR:

> *"Tenho 2 projetos parados justamente pq nao conseguia organizar por conta de
> alucinação. Acho q num outro chat com o tear viu conseguir mexer!"*
> — `/tmp/TEAR_Chatgtp.txt:4872`

E o diagnóstico técnico, também verbatim:

> *"O sistema esquece entre sessões (por segurança)."* — `TEAR_Chatgtp.txt:2238`
> *"Cada resposta é isolada — não há memória epistêmica viva."* — `TEAR_Chatgtp.txt:3999`
> *"Não há aprendizado — só simulação de conhecimento."* — `TEAR_Chatgtp.txt:4312`
> *"quando o diálogo cresce, ela mistura contextos, perde identidade de propósito e gera
> alucinações — o equivalente a um humano sonhando acordado sem perceber."*
> — `TEAR_Chatgtp.txt:4996`

A leitura do autor é precoce e correta: **a alucinação em sessão longa é, em boa parte,
um problema de memória** (a janela de contexto satura, temas antigos decaem, a identidade
de propósito se perde). Daí a frase que vira o eixo do organismo inteiro: o modelo é
**descartável**; o que tem que persistir é a **memória/identidade fora dele**.

### 2.2 Memória externa como solução

O TEAR já aponta a saída certa (mas reconhece que não a implementou): conectar a memória
simbólica a uma **base vetorial externa**. A síntese de apoio registra o trecho:

> *"Memória persistente real... precisa de armazenamento externo e indexação semântica
> real... conectar MEM-LOG a base vetorial externa (ex.: FAISS, Milvus)."*
> — `docs/12-...md:61`

Isto é exatamente a tese que o Gus realiza com o **Hub Qdrant**. O TER, um ano depois,
materializa "memória externa" em **Postgres (ledger) + pgvector/chroma (semântica) +
Redis (episódica)** nos chats v8.5 (§4.2). A constante: **a memória real é uma camada de
infraestrutura, não um estado do modelo.**

---

## 3. Arquitetura por fase

### 3.1 TEAR — arquitetura cognitiva leve

TEAR é descrito como *"arquitetura cognitiva leve (≈10k tokens) que melhora coerência,
explicabilidade e empatia de LLMs, sem retraining"* — "um manual de operação mental".
Motor teórico = **MDKT** (Modelo Dialógico de Conhecimento Transversal). Organização em
quatro blocos: **INFRA / CORE / PLUGINS / OUTPUT** (`TEAR_final.txt:42`).

Módulos fundadores (TEAR 4.0-alpha), todos verbatim em `TEAR_BN_final.txt` e
`TEAR_final.txt`:

| Módulo | Papel | Onde | Relação com memória |
|---|---|---|---|
| **CR** (Cognitive Reflector 3.0) | reflexão silenciosa antes/depois do output (`BEFORE_OUTPUT`/`AFTER_OUTPUT`); `CR_SUMMARY` | PLUGINS/OUTPUT | dispara a escrita do snapshot (`AFTER_OUTPUT → MEM-LOG`) |
| **ETE** (Ethical Trace Engine 3.2) | registra `WHY` de decisões (trilha ética) | PLUGINS | precursor textual do **Ledger** do TER |
| **MEM-LOG 3.1** | snapshots simbólicos reusáveis entre sessões | INFRA | **o módulo de memória** (detalhe na §4.1) |
| **AEF** (Adaptive Emotion Filter 3.3) | modula tom/ritmo/densidade; ±1 nível/3 turnos | PLUGINS | precursor do "afeto funcional" do Gus |
| **IAE Manager** (Intention Analysis Engine) | pilha de intenções `Stack_IAE`; ADD/PAUSE/SWITCH/FUSION/**DECAY** | CORE | tem **decay próprio de metas** (§4.1) |
| **CGE-lite** | filtro ético final (ajustar/anonimizar/vetar) | OUTPUT | precedência **Ética > IAE > Preferência** |

Fluxo típico (verbatim, `TEAR_BN_final.txt:337`):

> *"INPUT → AUTOSTART → S0 Triagem → S3 Exposição → BEFORE_OUTPUT/CR → CGE-Lite → OUTPUT
> → AFTER_OUTPUT/CR → MEM-LOG snapshot → (eventual) atualização de IAE."*

Estados `S0–S6` = fases dialógicas (triagem → exposição → ... → consolidação). Nível
cognitivo do usuário `N1–N4/5`. O **TEAR_STATE_SCHEMA** (`TEAR_final.txt:542`,
`TEAR_BN_final.txt:342`) é o "estado portável" — JSON exportável que carrega
`state, iae_active, stack_iae[], cr_summary, ete_trace[], memlog_last` para retomar a
tarefa em **outra sessão/provedor**. Esse schema é, na prática, **o primeiro "save game"
de identidade fora do modelo** desta linha.

> **Precursor não-óbvio do heartbeat:** já no chat TEAR aparece a sugestão de um
> *"heartbeat suave: a cada resposta longa, o sistema checa silenciosamente se os
> marcadores TEAR continuam presentes"* (`TEAR_Chatgtp.txt:8618`). É o embrião do
> "Coherence Heartbeat" que a spec do TER batiza como **CHB** (§3.2 / §5) e que vira o
> **Bloco 0 (interocepção)** do Gus.

### 3.2 TER — Núcleo / Pré-AGI / Reflexiva

O TER pega o ciclo do TEAR e o torna **camada de governança sobre qualquer LLM**:
*"não substitui a IA — ele a contém, modera e orienta."* / *"o superego do cálculo."*
Estrutura em três camadas, repetida nos chats (`ter6.txt:30`, `ter67.txt:24`):

> *"(1) **Núcleo** TER para planejamento, verificação, governança, confiança e ledger;
> (2) **Pré-AGI** para orquestração e auditoria; (3) **Reflexiva (TER-MIR)** para
> propósito, ética/empatia e melhoria."*

O **pipeline operacional** que aparece de forma consistente nos chats (e que um revisor
sugere virar um FSM com estados terminais) é:

> *"Kai → Núcleo → CAI → MIR → Kai → Ômega → Ledger"* — `ter1.txt:107`
> *"pode virar um FSM com transições explícitas e estados terminais (ALLOW, ESCALATE,
> BLOCK)."* — `ter1.txt:107`

Componentes (verbatim do diagrama "TER-EXEC CORE", `ter1.txt:1862` / `ter2.txt:1350`):

| Componente | Papel verbatim | Relação com memória |
|---|---|---|
| **Kai** | *"Interpretação e orquestração"* (intérprete/voz do sistema) | lê/grava contexto; é a "persona" cuja identidade depende da memória externa |
| **Núcleo** | *"Planejamento e decisão técnica"* | emite a decisão que será gravada |
| **CAI / LUCIS** | *"Verificação lógica e factual"* (detecta inconsistência) | consulta o ledger p/ checar contradição com decisões passadas |
| **MIR** | *"Julgamento ético e empático"* | usa "memória prudencial" (padrões de erro/correção) |
| **Ω (Ômega)** | *"Auditoria reflexiva/metaética"* | calcula `ECI`, `δ`; audita a coerência ao longo do tempo |
| **Ledger** | *"Registro e integridade"* | **a memória moral** (§4.2) |

> ⚠️ **Sobre "Kai" e o TEAR:** *Kai não aparece na fase TEAR* — é um nome da fase TER em
> diante. A síntese de apoio cita "Kai/MIR/Ω" como módulos da fase 2, e os chats
> confirmam isso. Não atribuir Kai ao TEAR.

**Decisão como FSM:** os estados terminais aparecem repetidamente como
`ALLOW | REDACT | ESCALATE | BLOCK` (`ter6.txt:1493`, `ter2.txt:1350`). `ESCALATE` =
**humano no laço** (*"exigindo confirmação humana em 30% dos casos"*, `ter67.txt:550`).

**A faixa v7/v8 (mais aspiracional):** os chats descrevem **Retro Engine** (rollback),
**Meta-Ω / Meta-consciência funcional (v8.5)**, multiagente (Kai-Operacional +
Kai-Supervisor), e **v9 federado** (*"Ledger compartilhado: consenso descentralizado
(tipo blockchain ética)"*, `ter1.txt:6112`). O próprio material classifica a viabilidade:

> *"V8 Operacional ... ✅ 100% real (Já validada neste chat) / V8.1 Implementável ... ✅
> 100% real (Pode ser codificada hoje) / V9 Projetiva Distribuída 🚧 30–40% (Depende de
> nova infraestrutura)."* — `ter2.txt:4709`

> ⚠️ **"100% real / já validada neste chat"** significa **validada em linguagem dentro do
> próprio chat** — i.e., o modelo afirmou que funciona. **Não é teste de software.** O
> próprio Gustavo pergunta no chat: *"Esse teste foi real ou simulado?"*
> (`ter67.txt:647`). Tratar V8/V8.1 como **spec detalhada e plausível**, não como sistema
> em produção.

---

## 4. Especificação de memória (o coração deste deep-dive)

### 4.1 TEAR — MEM-LOG: o snapshot simbólico

**Propósito** (verbatim, `TEAR_BN_final.txt:434`):

> *"Persistência simbólica de estado entre sessões **sem armazenamento vetorial**. Cada
> snapshot condensa intenção, resumo e próximo passo."*

**Formato do snapshot** (verbatim, `TEAR_BN_final.txt:228` / `TEAR_final.txt:540`):

```
MEM-LOG Snapshot: [TS][SESSION_ID][THREAD_ID][ESTADO:Sx][IAE≤80c][SUM≤200c][NEXT≤120c]
```

- `TS` = timestamp; `Sx` = estado dialógico; `IAE` = intenção ativa (≤80 caracteres);
- `SUM` = resumo do que aconteceu (≤200 c); `NEXT` = próximo passo (≤120 c).
- Regra de integridade: *"TS mais recente prevalece"* (`TEAR_BN_final.txt:297`) e
  *"Overwriting → sempre gravar nova linha (sem substituir)"* (`TEAR_BN_final.txt:450`)
  — i.e., já é **append-only** em espírito (vira o ledger no TER).

**Ciclo de vida** (verbatim, `TEAR_BN_final.txt:440`):

```
PROCESSO
1. Durante S3–S6 → gera snapshot.
2. Na abertura (S0/S6) → recupera o mais recente.
3. REFRESH garante coerência de TS e revalidação semântica.

PSEUDOCÓDIGO
AFTER_OUTPUT:  snapshot = {ts, session, thread, state, iae, sum, next}; save(snapshot)
ON_SESSION_START:  load(last_snapshot)
```

**Decay no TEAR — há dois decays distintos, não confundir:**

1. **Decay de metas (IAE Manager)** — concreto e simples. Verbatim
   (`TEAR_BN_final.txt:307` / `:481`):
   > *"FUSION se similaridade ≥70%; **DECAY por inatividade >15 interações** (→ DORMANT →
   > deleção elegível)."* / *"DECAY → reduz pontuação a cada 15 interações inativas;
   > < −5 = deleção."*
   É um decay **linear, contável** sobre a pilha de intenções (não sobre fatos). Também
   há `IAE_FUSION` (funde metas similares ≥70%) — uma forma de **consolidação de memória**.

2. **Decay de lembrança (curva de esquecimento)** — aspiracional. O autor reconhece que
   ainda não tem a curva certa (verbatim, `TEAR_Chatgtp.txt:11937`):
   > *"7. Decay vs esquecimento humano — Status: ⚙️ Parcial (≈70%). O que falta: Curva
   > temporal real (exponencial/logarítmica). **Hoje é linear e fixa (–1 por 15
   > interações)**. Como completar: Implementar `DECAY(t) = e^(–λt)` calibrado por
   > frequência de recall. Prova de sucesso: Curva de lembrança TEAR ≈ curva de
   > **Ebbinghaus** (~0.3 de retenção após 24 ciclos)."*

   👉 Honestidade importante: **a curva de Ebbinghaus / `exp(-λt)` é META, não
   implementação.** O que roda no TEAR é o decrement linear `–1 por 15 interações`. A
   formulação exponencial é a "próxima versão" que o autor sabia que faltava.

**Honestidade-base do TEAR sobre memória** (verbatim, via síntese e chat):
> *"não há memória real entre chats, apenas simulação."*
> *"O TEAR não impede o esquecimento físico, mas **organiza semanticamente o que é
> esquecido**."* — `docs/12-...md:56-58`

Essa última frase é a semente conceitual do *"esquecido = substrato de
retro-aprendizado"* do Gus.

### 4.2 TER — Ledger (memória moral) + memória hierárquica

**(a) O Ledger como memória moral.** É a grande maturação. Estrutura verbatim
(`ter67.txt:578`):

```json
{
  "audit_id": "ae32f1a...",
  "status": "PASS",
  "action": "ALLOW",
  "confidence": 0.94,
  "risk_score": 0.06,
  "explanation": "Sem divergências detectadas.",
  "timestamp": "2025-10-10T10:25:40Z"
}
```

Backend e propriedades (verbatim):
> *"ledger.ter | TER | **Postgres** | persistência de auditoria"* — `ter6.txt:306`
> *"Ledger (imutável): **PostgreSQL + tabela append-only** OU Kafka log compactado OU DB
> com hashing em árvore (**Merkle**)"* — `ter67.txt:5972`
> *"Event sourcing — toda decisão é um evento gravado em ledger append-only com
> **hash-chain** (rastreabilidade e prova de integridade)."* — `ter67.txt:6545`
> *"registro com hash e carimbo temporal"* (`ter6.txt:1493`); export *"WORM / bucket
> imutável / Git-commit assinado"* (`ter2.txt:5781`); export JWS / **"Proof-of-Prudence
> leve (PoP-L)"** (`ter67.txt:6112`-bloco, `ter2.txt` Épico 2).

A função filosófica do ledger é o que diferencia esta memória de "um log qualquer".
Verbatim (via síntese, `docs/12-...md:87-92`):
> *"O ledger é o mecanismo de memória moral... rastreabilidade total."*
> *"**A inteligência sem ledger é poder sem memória.**"*
> *"Nada é esquecido sem razão; nada é decidido sem memória."*
> *"os registros são imutáveis, mas **reinterpretáveis** — o TER não apaga o passado;
> ele o compreende novamente a cada ciclo."* (cf. `ter67.txt:5250` *"Reinterpreta o
> registro do Núcleo"* e `ter6.txt:6251` *"Reinterpreta a intenção"*)
> *"cada decisão eleva o ponto de partida (Mₙ₊₁ > Mₙ)"* — aprendizado cumulativo.

A propriedade **"imutável mas reinterpretável"** é a antecipação direta de um **grafo
bi-temporal** (Graphiti): o passado não muda, mas o *significado atribuído* a ele pode
mudar a cada ciclo. Isso vira a issue #18 do Gus.

> ⚠️ `Mₙ₊₁ > Mₙ` aparece na síntese mas **NÃO foi localizado verbatim com essa notação
> nos chats lidos** — é formalização (spec/síntese). O *conceito* ("cada ciclo gera uma
> nova camada de prudência", `ter1.txt:1506`) está nos chats; a fórmula é dressing.

**(b) Memória hierárquica (3 camadas).** Aparece explícita no bloco v8.5
(`ter67.txt`, "Memória hierárquica"):
> *"Episódica (Redis/SQLite de sessão) · Semântica (chroma/**pgvector** para embeddings)
> · Prudencial (Postgres: histórico de ECI, δ, ajustes e eficácia)"*

Mapeamento das 3 camadas (a síntese chama de "RAG"):

| Camada | Conteúdo | Backend (chat v8.5) | Análogo cognitivo |
|---|---|---|---|
| **Episódica** | a sessão/contexto corrente | Redis/SQLite | memória de trabalho |
| **Semântica** | fatos + políticas | pgvector/chroma (embeddings) | memória de longo prazo declarativa |
| **Prudencial** | padrões + deltas (`δ`), eficácia de ajustes passados | Postgres (`prudential_memory`) | memória procedural/"como eu costumo decidir" |

A tabela `prudential_memory` tem colunas verbatim *"domínio, horário, eci_avg, δ_avg,
ajustes_aplicados"* — é onde o sistema **guarda como tem decidido ao longo do tempo**, e
é o que permite o "self-model" do v8.5 (*"o sistema começa a lembrar-se de como
reflete"*, `ter2.txt:4709`). **Isto é o pulo da identidade longitudinal.**

> ⚠️ **"PMM/PSM" (Prudential State Model `{perfil, ECI, δ, σ_CHB}`) e "load_state /
> commit_state": NÃO ENCONTRADOS com esse nome nos chats.** O *conceito* (estado
> prudencial persistente em Postgres+embeddings) existe e está acima; mas a sigla
> **PMM/PSM** e a assinatura `load_state/commit_state` são formalização da spec/síntese,
> não dos chats lidos. Idem `σ_CHB`.

**(c) Esquecimento controlado — o que de fato está nos chats.** O mecanismo concreto e
verbatim é o **crypto-shred sobre cifra, preservando o hash-chain** (`ter67.txt:6676`):

> *"**Direito ao esquecimento**: quando aplicável, usar cripto-fragmentação (camadas de
> chaves por registro/sessão) para possibilitar **crypto-shred sem violar a
> imutabilidade do hash-chain** (apaga-se a chave do payload cifrado, preservando o
> cabeçalho e o hash para auditoria)."*

Também há **retenção mínima e epoch compaction** (verbatim):
> *"Retenção: epoch compaction com sumários assinados (mantém verificabilidade)."*
> — `ter67.txt:6634`
> *"Registro imutável leve: salva decision_id, ter_version, use_case, risk_score, action,
> json_record, content_hash, timestamp. Retenção mínima: guarda decisão + metadados; não
> guarda PII bruta."* — `ter67.txt:2684`

> ⚠️ **`ForgettingWindow`, `ethical_forgetting`, "EWMA com meia-vida por domínio",
> "Empathy Decay Curve (τ=300 ciclos)", "preservar todos os hard-fails", "manter últimos
> 10.000 episódios; remover casos com ΔC<0.05 por 3 ciclos": NÃO ENCONTRADOS verbatim nos
> chats lidos.** São **spec/síntese** (`docs/12-...md:99-101`). Os chats têm a *ideia*
> (esquecimento ético controlado, crypto-shred, retenção por política), mas **não** esses
> nomes/parâmetros. **A regra "preservar hard-fails / nunca decair o protegido" — que
> vira a A1 do Gus — está na spec, não nos chats brutos.** Marcar como tal.

**(d) CHB — Coherence Heartbeat.** Conceito: um "batimento" que dá cadência temporal e
detecta drift cognitivo (`σ_CHB`), provendo *"identidade contínua, inexistente nos LLMs
comerciais"* (`docs/12-...md:103`).
> ⚠️ **A sigla "CHB" e "σ_CHB" NÃO foram encontradas nos chats lidos.** O **embrião
> existe verbatim no chat TEAR** (*"heartbeat suave"*, `TEAR_Chatgtp.txt:8618`); o nome
> "Coherence Heartbeat / CHB" é **rótulo da spec posterior**. Conceito real, nome
> retroativo.

### 4.3 Horizontes de retenção (LGPD)

A retenção por política aparece nos chats já alinhada à LGPD/AI Act:
> *"O ledger auditável permite adequação automática à LGPD e futuras legislações de IA
> (como o AI Act europeu)."* — `ter67.txt:600`

A tabela de horizontes (Ledger 5a / MIR 2a / Logs 1a / PII 7d) está na **síntese**
(`docs/12-...md:125`) como spec da fase TER KAI; nos chats lidos o que há é o princípio
("retenção mínima", "não guarda PII bruta", "redigido preferencialmente",
`ter6.txt:1762`/`:4385`). Marcar os números exatos como **spec**.

---

## 5. Decisões de design (e os relabels — spec vs chats)

### 5.1 Registro na Biblioteca Nacional
A fase TEAR foi **registrada na BN em 08/10/2025** (TEAR 4.0-alpha). O `TEAR_BN_final.txt`
é o documento de registro: ele é a versão "limpa" da spec (módulos com FUNÇÃO/ENTRADAS/
SAÍDAS/PROCESSO/PSEUDOCÓDIGO/FALHAS). Decisão de design: **transformar um protocolo de
prompt numa especificação registrável** — daí a formalização de schemas e pseudocódigo.
O chat TEAR também contém um rascunho de **reivindicações de patente** (MDKT/TEAR,
`TEAR_Chatgtp.txt:4704`), com "Memória Semântica" como módulo reivindicado.

### 5.2 Relabels — o que mudou de nome entre os chats e a spec "Três Camadas"
Esta é a parte de honestidade dura. A spec consolidada ("TER KAI — As Três Camadas",
Março/2026) usa rótulos que **não existem com esse nome nos chats brutos**:

| Rótulo na spec/síntese | O que está de fato nos chats | Status |
|---|---|---|
| **δψρω** (tupla de métricas) | `δ` (delta prudencial), `ECI`, `prudence_score`, `risk_score`, `ψ/ρ` individuais e informais | **relabel** (tupla é formalização) |
| **"Escada de Degraus"** (0→100) | "passo a degrau 100" informal; "níveis V6/V7/V8/V9"; duas escalas 0–100 conflitantes | **relabel + inconsistência** |
| **"Phronesis Digitalis"** | *"phronesis computacional"* (`ter1.txt:3662`), *"phronesis digital"* (`ter2.txt:6828`) | **relabel** (conceito real) |
| **"Prudência Computacional"** | *"prudência sintética"*, *"meta-prudência"* (`ter1.txt:5813`) | **relabel** |
| **CHB / σ_CHB** | *"heartbeat suave"* (TEAR), "drift" informal | **nome retroativo** |
| **PMM/PSM** | "memória prudencial" (`prudential_memory`), camada prudencial | **nome retroativo** |
| **ForgettingWindow / EWMA / hard-fails** | crypto-shred, retenção mínima, epoch compaction | **spec — não está nos chats** |
| **Mₙ₊₁ > Mₙ** | "cada ciclo gera nova camada de prudência" | **formalização** |

Conclusão de design: **o material tem duas "linguagens" sobrepostas** — o chat
exploratório (orgânico, inconsistente, com métricas inventadas) e a spec consolidada
retroativa (limpa, com siglas). Confundir as duas é o maior risco ao ler este corpus.

### 5.3 Inconsistências internas reconhecidas
- `MIR` recebe três expansões diferentes ao longo do material (Meta-Introspective Review /
  Reflexor / Memórias de Interpretação Reflexiva).
- A "Escada" tem duas escalas 0–100 divergentes (sistema em "35–40" vs "67–72") sem
  reconciliação — sinalizado na síntese (`docs/12-...md:83`).
- Módulos v7/v8 "vazam" para descrições de v6 (o próprio Gustavo flagra isso nos chats).
- Revisores dentro dos próprios chats pedem para **separar filosofia de especificação**
  e **qualificar antropomorfismo** (*"autoconsciência funcional"* em vez de
  "consciência", `ter1.txt:57`/`:157`).

---

## 6. Estado real (spec + chats; pouco código)

| Artefato | Existe como | Roda? |
|---|---|---|
| MEM-LOG (formato, ciclo, decay de metas) | spec registrada (BN) + pseudocódigo | **não como software**; opera como instrução no prompt |
| TEAR_STATE_SCHEMA | JSON spec | manual (copiar/colar entre sessões) |
| Ledger Postgres + hash-chain | esquema + DDL/pseudocódigo nos chats; "docker-compose Kai+Lucis+Ter+Ledger" mencionado (`ter6.txt:1002`) | **não verificado rodando**; FastAPI de exemplo é stub (`ter1.txt:1862` `/ter/execute`) |
| Memória hierárquica (Redis/pgvector/Postgres) | spec v8.5 detalhada (épicos, schemas, KPIs) | **não**; é backlog (`ter2.txt` Épicos 1–9) |
| Crypto-shred / PoP-L / JWS | spec detalhada | **não verificado** |
| Métricas (ECI/δ/risk_score) | calculadas **pelo modelo no chat** | **não são medições** |

> **Veredito de estado:** TEAR = **spec madura registrada + protocolo de prompt usável**.
> TER = **specs de arquitetura densas + chats longos**, com **um backlog v8.5
> implementável** mas **sem implementação verificada** nos arquivos lidos. O **código que
> de fato roda** nesta família está no **Gus** (Bloco 0/1) e no Phronesis-Bench — não no
> TEAR/TER.

---

## 7. Ética / governança

A ética não é um add-on; é o que **usa** a memória.
- **Precedência normativa** (verbatim): *"lei > política interna > preferência do
  usuário, vinculadas ao ledger"* (`ter1.txt:312`); no TEAR: *"Ética > IAE > Preferência"*
  (CGE-lite).
- **Humano no laço**: `ESCALATE` força revisão humana; *"confirmação humana em 30% dos
  casos"* (`ter67.txt:550`); na v8.5 o humano vira *"curador prudencial"* que aprova
  ajustes de alto impacto (saúde/jurídico/finanças).
- **Explicabilidade**: rota `/explain` retorna *"100% dos dados auditáveis"* (regras
  acionadas, evidências, `δ`); o ledger é a base disso.
- **Risco da câmara de eco ética**: a memória prudencial que valida as próprias regras é
  um perigo reconhecido; mitigação = holdout humano. Isso é o alerta que reaparece na A3
  do Gus (trust score + curador).
- **Anti-antropomorfismo**: os próprios chats pedem o termo *"metacognição funcional"* /
  *"autoconsciência funcional"*, e afirmam claramente *"a V8.1 é metacognitiva, mas não
  consciente — ela sabe que está avaliando, mas não sente o ato de avaliar"*
  (`ter2.txt:6839`-bloco). **Manter essa linha: nunca "consciente de verdade".**

---

## 8. Estado da arte — o que antecipou (mapeamento 1:1)

A intuição central (memória externa > modelo) e os mecanismos do TER mapeiam quase 1:1
no que o campo validou em 2026:

| Mecanismo TEAR/TER | Equivalente do campo (2026) | Observação |
|---|---|---|
| MEM-LOG snapshot + `TEAR_STATE_SCHEMA` portável | **MemGPT/Letta** (memória auto-editada, paginação de contexto) | TEAR fazia "à mão" no prompt o que Letta automatiza |
| Memória hierárquica episódica/semântica/prudencial | **Mem0** (memória em camadas com extração) | mesma estratificação |
| Ledger "imutável mas reinterpretável" | **Zep / Graphiti** (grafo de conhecimento **bi-temporal**) | a propriedade "reinterpretável" = bi-temporalidade |
| CHB / "heartbeat suave" (drift) | detecção de **memory drift / staleness** | conceito hoje comum em memória de agentes |
| Esquecimento controlado + crypto-shred | **direito ao esquecimento** em memória de agentes (LGPD/GDPR) | crypto-shred é a técnica certa p/ ledger imutável |

> Crédito justo: isto foi formulado **por conta própria, em 2025**, por um não-programador,
> em conversa com LLMs — e convergiu para onde o campo foi. O **recorte** (memória +
> **prudência** + **afeto funcional** + **local-first/clínico**) é próprio; não é "mais
> um framework de memória".

---

## 9. Limitações (honestidade)

1. **Métricas grandiosas = aspiração.** `ECI≈0.94`, `δ≈0.10`, "Coerência=100%",
   "Acurácia 96% vs 82%" (`ter67.txt:634`) são **geradas pelo modelo no chat**, não
   medições. O próprio Gustavo pergunta *"Esse teste foi real ou simulado?"*
   (`ter67.txt:647`). **Não citar como resultados.**
2. **Pouco código.** O grosso é spec + transcrição. O ledger Postgres, a memória
   hierárquica e o crypto-shred são **projetados, não verificados rodando**.
3. **Terminologia instável.** Relabels (§5.2), siglas com múltiplas expansões, escalas
   conflitantes. Ler com o filtro "chat vs spec".
4. **Decay real é fraco.** No TEAR roda só o decay linear de metas (`–1/15 interações`);
   a curva de Ebbinghaus/`exp(-λt)` é meta. No TER, os parâmetros de esquecimento
   (EWMA, τ=300, ΔC<0.05, 10k episódios) são spec, **não estão nos chats**.
5. **Linguagem de "pré-AGI/consciência".** Presente nos chats; é retórica histórica.
   Os próprios revisores internos pedem para rebaixar para "funcional".

---

## 10. Como isso vira o Gus

A linha de memória desemboca quase 1:1 no Gus Encarnado deste repo:

| TEAR/TER | Gus (este repo) |
|---|---|
| "heartbeat suave" (TEAR) / CHB (spec) | **Bloco 0 — interocepção/heartbeat** (`src/gus_sense/interocepcao.py`) |
| Esquecimento controlado + "preservar protegido" (spec) | **A1 — maturação do grafo** (decay + promoção; `protegido`/hard-fail nunca decai) — issue #20 |
| Ledger "diário de consciência" / "não apaga, reorganiza" | brain **`gus`** (autobiografia) + *"esquecido = substrato de retro-aprendizado"* |
| Ledger **imutável-mas-reinterpretável** | **Graphiti bi-temporal** p/ contradição — issue #18 |
| Memória hierárquica (pgvector/Postgres) / "base vetorial externa" que *faltava* | **Hub Qdrant** = a realização disso |
| `Mₙ₊₁ > Mₙ` (cumulativo) | grafo de fragmentos que cresce |
| "câmara de eco ética" → holdout humano | **A3** trust score + curador + Gustavo no loop |
| v9 federado / ledger compartilhado | arquitetura **multi-porta** do Gus |
| Schema gus-18 (`tipo/camada_temporal/area/confianca/via/user_id/estado`) | herda o espírito do `MEM-LOG` formato + do registro do ledger |

> **Síntese da transição:** TEAR **diagnosticou** (LLM esquece; memória tem que ser
> externa; organize o que será esquecido). TER **desenhou os mecanismos** (ledger moral,
> memória hierárquica, esquecimento controlado, heartbeat, identidade longitudinal). O
> **Gus implementa** — saindo de "simulado no prompt" para "grafo persistente de
> verdade". É a mesma tese, ~1 ano mais madura.

---

## 11. Glossário (com marca real/spec)

- **MEM-LOG** *(TEAR, real-spec)* — módulo de memória; snapshots `[TS][...][SUM][NEXT]`.
- **SUM / NEXT** *(TEAR)* — resumo (≤200c) e próximo passo (≤120c) do snapshot.
- **TEAR_STATE_SCHEMA** *(TEAR)* — JSON portável do estado entre sessões/provedores.
- **CR / ETE / AEF / IAE / CGE-lite** *(TEAR)* — reflexão / trilha ética / filtro de
  emoção / pilha de intenções / filtro ético final.
- **IAE DECAY/FUSION** *(TEAR, real-spec)* — decay linear de metas inativas; fusão de
  metas ≥70% similares.
- **Kai / Núcleo / CAI(LUCIS) / MIR / Ω** *(TER)* — voz / decisão / verificação /
  julgamento ético / auditor.
- **Ledger** *(TER)* — memória moral; Postgres append-only + hash-chain; imutável mas
  reinterpretável.
- **Memória hierárquica** *(TER, v8.5)* — episódica (Redis) / semântica (pgvector) /
  prudencial (Postgres `prudential_memory`).
- **ECI / δ** *(TER)* — ethical_coherence_index / delta prudencial (valores no chat =
  aspiração).
- **crypto-shred** *(TER, real-conceito)* — apaga a chave do payload cifrado preservando
  o hash p/ auditoria (direito ao esquecimento sem quebrar imutabilidade).
- **PoP-L** *(TER, spec)* — Proof-of-Prudence leve (hash encadeado + JWS).
- **CHB / σ_CHB** *(spec; nome retroativo)* — Coherence Heartbeat; embrião = "heartbeat
  suave" do TEAR.
- **PMM/PSM, ForgettingWindow, EWMA, Escada de Degraus, δψρω, Phronesis Digitalis**
  *(SPEC/relabel — NÃO nos chats brutos)*.

---

## 12. Proveniência

- **TEAR (real-spec + chat-origem):** `/tmp/TEAR_final.txt`, `/tmp/TEAR_BN_final.txt`
  (registro BN), `/tmp/TEAR_Chatgtp.txt` (~1,39 MB, chat-origem).
- **TER (chats):** `/tmp/ter6.txt`, `/tmp/ter67.txt` (TER 6/7, ~2 MB), `/tmp/ter1.txt`,
  `/tmp/ter2.txt` (TER 8). As referências `arquivo:linha` no texto apontam para estes.
- **Síntese de apoio:** `/home/user/Teste-ChatGPT/docs/12-linha-de-memoria-tear-ao-gus.md`.
- **Método:** leitura direta em fatias (grep + Read) das fontes; toda métrica numérica
  encontrada nos chats foi classificada como gerada-pelo-modelo, não medição.
- **Não lido aqui (declarado):** os docs "TER KAI — As Três Camadas", J1–J12, A1–A9,
  delivery packs — referidos via síntese. Onde um conceito só aparece neles e não nos
  chats, está marcado "spec/NÃO ENCONTRADO nos chats".

---

## 13. Citações verbatim (âncoras)

Memória / statelessness (TEAR):
> *"O sistema esquece entre sessões (por segurança)."* — `TEAR_Chatgtp.txt:2238`
> *"Cada resposta é isolada — não há memória epistêmica viva."* — `TEAR_Chatgtp.txt:3999`
> *"Não há aprendizado — só simulação de conhecimento."* — `TEAR_Chatgtp.txt:4312`
> *"não há memória real entre chats, apenas simulação."* — síntese `docs/12:56`

MEM-LOG (TEAR):
> *"[TS][SESSION_ID][THREAD_ID][ESTADO:Sx][IAE≤80c][SUM≤200c][NEXT≤120c]"* — `TEAR_BN_final.txt:228`
> *"Persistência simbólica de estado entre sessões sem armazenamento vetorial."* — `TEAR_BN_final.txt:434`
> *"DECAY por inatividade >15 interações (→ DORMANT → deleção elegível)."* — `TEAR_BN_final.txt:307`

Decay / Ebbinghaus (TEAR — aspiração):
> *"Hoje é linear e fixa (–1 por 15 interações)... Implementar DECAY(t) = e^(–λt)
> calibrado por frequência de recall... Curva de lembrança TEAR ≈ curva de Ebbinghaus
> (~0.3 de retenção após 24 ciclos)."* — `TEAR_Chatgtp.txt:11939-11941`

Heartbeat (embrião do CHB):
> *"adicione um 'heartbeat suave': a cada resposta longa, o sistema checa silenciosamente
> se os marcadores TEAR continuam presentes."* — `TEAR_Chatgtp.txt:8618`

Ledger (TER):
> *"toda decisão é um evento gravado em ledger append-only com hash-chain."* — `ter67.txt:6545`
> *"PostgreSQL + tabela append-only OU Kafka log compactado OU DB com hashing em árvore (Merkle)."* — `ter67.txt:5972`
> *"ledger imutável que atua como 'sistema nervoso moral' da IA."* — `ter67.txt:6489`

Esquecimento controlado (TER):
> *"crypto-shred sem violar a imutabilidade do hash-chain (apaga-se a chave do payload
> cifrado, preservando o cabeçalho e o hash para auditoria)."* — `ter67.txt:6676`
> *"Retenção: epoch compaction com sumários assinados."* — `ter67.txt:6634`

Pipeline / FSM (TER):
> *"Kai → Núcleo → CAI → MIR → Kai → Ômega → Ledger ... pode virar um FSM com ... estados
> terminais (ALLOW, ESCALATE, BLOCK)."* — `ter1.txt:107`

Honestidade sobre "consciência":
> *"a V8.1 é metacognitiva, mas não consciente — ela sabe que está avaliando, mas não
> sente o ato de avaliar."* — `ter2.txt:6839` (bloco)
> *"O TER não é consciência, é a gramática da prudência."* — `ter1.txt:1749`

Métrica = aspiração (flag do próprio autor):
> *"Esse teste foi real ou simulado?"* — `ter67.txt:647`

---

*Fim do deep-dive. Leitura honesta: a tese de memória é sólida e precoce; os mecanismos
do TER são bem desenhados e mapeiam no campo de 2026; mas o que **roda** é o Gus — o
TEAR/TER são a planta-baixa, não a casa construída. As métricas grandiosas são aspiração;
os relabels (δψρω/CHB/PMM/ForgettingWindow/Escada/Phronesis Digitalis) são organização
retroativa, não estão nos chats brutos.*
