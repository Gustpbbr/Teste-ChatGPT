# TER KAI — Deep-Dive Técnico

> **Tipo de documento:** análise técnica honesta a partir das fontes do dono.
> **Data:** 2026-06-16
> **Escopo:** TER KAI — *Technological Ethical Reasoning Kernel for Artificial Intelligence* / "Sistema de Governança e Segurança Prudencial em Inteligência Artificial".
> **Aviso de honestidade:** este projeto existe hoje em **nível de especificação grau-patente** (blueprint), não em código rodando. Todos os números de desempenho (latências, precisão, F1, custos, correlação humana) que aparecem nas fontes são **metas/projeções de projeto, não medições empíricas**. Onde uma informação não consta das fontes, está marcado **NÃO ENCONTRADO**.

---

## 1. Resumo

O TER KAI é um **framework modular de governança prudencial de IA**, projetado para operar como uma *camada intermediária* (middleware) entre um modelo de IA (próprio ou de terceiros — OpenAI, Anthropic, Mistral, Vertex, Llama etc.) e o ambiente de produção. A proposta central é deixar de tratar segurança de IA de forma reativa (filtrar só o output final) e passar a **medir, explicar e ajustar o comportamento do modelo em tempo real**, transformando "governança de IA" numa disciplina baseada em métricas, protocolos e prova criptográfica.

A arquitetura tem **7 módulos** organizados em **3 clusters**, operando em dois caminhos: **Fast Path** (maioria do tráfego, triagem leve) e **Slow/Deep Path** (casos de alto risco, auditoria completa). O resultado de cada decisão de governança é registrado num **ledger criptográfico imutável (PoP-L)**, com hash SHA3-512 e carimbo de tempo TSA RFC 3161, gerando prova de não-repúdio para fins de conformidade (EU AI Act, LGPD/GDPR, ISO/IEC 42001, NIST AI RMF).

Existe uma tensão interna importante entre os documentos: há **duas "edições" do projeto** com vocabulários diferentes — uma edição "científica/comercial" (clusters δψρω, Eϕ, MACT/LinUCB) e uma edição "engenharia/patente" (pipeline Kai L0 → MIR L1 → Ω L2 → Retro L3 → Ledger L4, regras CEL/JSONLogic). Este documento descreve as duas e aponta onde elas divergem.

---

## 2. Tese e problema (Registro B)

### 2.1 O problema central declarado

> "A ausência de mecanismos determinísticos e auditáveis que comprovem a correção ética de decisões algorítmicas constitui o **déficit prudencial computacional** contemporâneo." — *Cap 01 Introdução e Contexto, §1.3*

As fontes identificam que mesmo modelos avançados carecem de três coisas:
- rastreabilidade criptográfica entre dado, contexto e ação;
- métricas objetivas que mensurem prudência/risco;
- meios de reverter ou revisar decisões autônomas sem perda de integridade.

### 2.2 A tese: prudência computacional / "Registro B"

A tese do projeto é o conceito de **Prudência Computacional**: tornar a prudência uma *função mensurável do sistema*, registrada e certificada em tempo real, em vez de um atributo moral abstrato.

> "A prudência deixa de ser um atributo moral abstrato e torna-se **função mensurável do sistema**, registrada e certificada em tempo real." — *Cap 01, §1.2*

O eixo que o prompt chama de **"Registro B" — provar externamente; capacidade sem prudência** mapeia diretamente para o argumento de fundo das fontes: a capacidade dos modelos cresceu, mas a **prudência (o freio reflexivo, auditável e reversível) não acompanhou**. O TER KAI se posiciona como o "sistema imunológico" dessa capacidade:

> "Se a IA é o novo sistema nervoso da economia digital, o TER KAI é o seu sistema imunológico." — *Resumo Executivo, §9*

O par "capacidade sem prudência" é resolvido, na tese, transformando a confiança subjetiva em **verificação prudencial contínua + prova externa**: cada inferência, política e ação gera um *artefato técnico assinável e verificável* que pode ser checado por um terceiro (auditor, regulador, TSA externa). É a parte "provar externamente": a prova não vive só dentro do sistema — ela é ancorada num ledger e carimbada por uma autoridade de tempo independente (RFC 3161), de modo que qualquer adulteração posterior invalida o hash e é detectável.

**Nota crítica honesta:** o conceito de "prudência" aqui é *funcional/operacional* (mensurabilidade + reversibilidade + rastreabilidade), não uma alegação de que a IA "é prudente de verdade". As próprias fontes evitam afirmar consciência; o que medem é comportamento confiável sob métricas.

---

## 3. Arquitetura

### 3.1 Os 7 módulos / 3 clusters (edição científica)

| Cluster | Função | Módulos |
|---|---|---|
| **Cluster 1** — Avaliação Semântica e Factual (δ, ψ) | Mede coerência e estabilidade dos outputs | GDATA, KAI CORE, MACT |
| **Cluster 2** — Fairness, Auditoria e Explicabilidade (ρ, ω) | Mede imparcialidade e reversibilidade/auditabilidade | POP, CATE/CRA, CAET |
| **Cluster S** — Validação Científica e Padronização | Padroniza, valida e publica benchmarks/protocolos | MIR (observabilidade) + Audit Ledger / AISL Protocol |

Os **7 módulos canônicos** (Cap 01, §1.1), em ordem de fluxo:

```
GDATA → CRA-Bridge → KAI Core → CAET → MACT-Lite → MIR → PoP-L Ω
```

### 3.2 As duas leituras de arquitetura (divergência real)

As fontes contêm **duas convenções paralelas** para o mesmo sistema. Isto é uma inconsistência editorial real do material, não um erro deste relatório:

**Edição A — "científica/clusters"** (Resumo Executivo, Blueprint, Especificação de Métricas):
gateway Fast/Slow → Cluster 1 (GDATA, KAI CORE, MACT) → Cluster 2 (POP, CATE, CAET) → Cluster S (MIR).

**Edição B — "engenharia/patente"** (Doc 03 Módulos Internos, Doc 04 Fluxos, Glossário, doc de patente). Pipeline de microsserviços em camadas L0–L4:
```
LLM → Kai (L0, extração) → MIR (L1, agregação) → Ω (L2, governança) → Retro/Reviser (L3, correção) → Ledger/PoP-L (L4, auditoria)
```
Aqui o **Ω (Omega) é o motor de governança** que decide `ALLOW / REVIEW / BLOCK` via regras CEL/JSONLogic, e o **MIR é agregador de métricas (L1)** — papel diferente do "MIR observabilidade" da edição A.

> Onde os dois mundos se reconciliam: a edição B é a forma **implementável/patenteável** mais concreta (microsserviços, regras sandboxed, ledger). A edição A é a forma **conceitual/comercial** (métricas δψρω, clusters, energia prudencial Eϕ). Um deep-dive honesto trata a edição B como o "como construir" e a edição A como o "o que medir e vender".

### 3.3 Fast Path / Slow (Deep) Path

| Caminho | Uso | Profundidade | Latência (meta declarada) |
|---|---|---|---|
| **Fast Path** | ~80% das requisições | heurísticas δψ leves; PII, palavras-chave, sentimento local | **Blueprint: ≤60ms** / **Doc 04: ≤800ms P95** (additional ao LLM) |
| **Slow/Deep Path** | ~20% (críticos) | δψρω completo + explicabilidade + replay determinístico; fact-checking externo | **Blueprint: ≤150ms** / **Doc 04: 3–7 segundos** |

> **Inconsistência crítica de números:** o Blueprint Técnico promete Fast ≤60ms / Slow ≤150ms; o documento de Fluxos Operacionais (Doc 04) fala em Fast ≤800ms P95 e Deep 3–7s (pois o Deep Path chama fact-checking externo, que é I/O de rede). Os ≤60ms/≤150ms só são plausíveis para o caminho puramente local sem chamada de LLM/fact-check externo. **Ambos são metas, nenhum é medido.** Esta divergência precisa ser resolvida antes de qualquer alegação pública.

**Critérios de ativação do Slow/Deep Path:**
- alta entropia/perplexidade no output;
- inconsistência factual detectada / claims factuais extraídos;
- divergência entre política (POP/Ω) e métricas;
- `domain_risk > 0.7` (ex.: Saúde = 0.8) ou presença de `compliance_keywords`;
- solicitação explícita de auditoria.

O componente que decide o caminho é o **RBR — Roteamento Baseado em Risco (RiskRouter)**.

### 3.4 Diagrama: gateway → clusters

```
                 ┌─────────────────────────────────────┐
   input ───────▶│  TER KAI GATEWAY                     │
   (LLM output)  │  (Fast/Slow Path Decision Engine /   │
                 │   RBR Risk-Based Router)             │
                 └─────────────────────────────────────┘
                          │ Fast (~80%)        │ Slow/Deep (~20%)
                          ▼                    ▼
        ┌──────────────────────────────────────────────────────┐
        │ CLUSTER 1 — Avaliação Semântica e Factual (δ, ψ)      │
        │   GDATA   → ingestão/sanitização/normalização (PII)   │
        │   KAI CORE→ núcleo prudencial (δ ψ ρ ω + RPE)         │
        │   MACT    → thresholds adaptativos / rollback         │
        └──────────────────────────────────────────────────────┘
                          │
                          ▼
        ┌──────────────────────────────────────────────────────┐
        │ CLUSTER 2 — Fairness / Auditoria / Explicabilidade    │
        │   POP/Ω   → políticas e compliance (ALLOW/REVIEW/BLOCK)│
        │   CRA/CATE→ contexto reproduzível (CPR) + rastros      │
        │   CAET    → veredito ético + explicação contrafactual  │
        └──────────────────────────────────────────────────────┘
                          │
                          ▼
        ┌──────────────────────────────────────────────────────┐
        │ CLUSTER S — Validação / Padronização                   │
        │   MIR        → observabilidade + replay determinístico │
        │   PoP-L      → ledger imutável (SHA3-512 + TSA RFC3161) │
        │   AISL Proto → benchmarks/datasets/certificação L1–L3   │
        └──────────────────────────────────────────────────────┘
```

---

## 4. Especificação por módulo

> Estado tecnológico declarado nas fontes é "100% viável / TRL 7–8". Trata-se de **autoavaliação do projeto**, não de validação independente.

### 4.1 GDATA — Gateway de Dados Ético
- **Função:** ponto de entrada prudencial ("firewall de consciência"). Filtra, registra e contextualiza todo dado de entrada: sanitização de PII (LGPD/GDPR), validação de consentimento/origem, geração do rastro inicial.
- **I/O:** entrada = dado bruto (texto/imagem/log/sensor) + metadados (fonte, domínio, consentimento). Saída = dado limpo/etiquetado + rastro prudencial (`trace_id`, `proof_ref`, `policy_hash`, `source_fingerprint`).
- **Pipeline (5 estágios):** sanitização ética → verificação legal/consentimento → geração de rastro (`trace_id`, `source_fingerprint` BLAKE3, `policy_hash`) → persistência parcial no ledger → despacho ao CRA-Bridge.
- **Propriedade-chave:** "ponto de não-retorno" — dado rejeitado não pode ser reintroduzido.
- **Stack declarada:** Python/FastAPI, Presidio (PII), BLAKE3, OPA, PostgreSQL, IPFS. Endpoint `POST /v1/gdata/ingest`. **TRL declarado: 8.**
- **Risco conhecido:** latência ~30ms em inputs >1MB → mitigação por chunking assíncrono.

### 4.2 KAI Core — Núcleo Cognitivo Prudencial
- **Função:** deliberação cognitiva. Converte CPR (contexto) em decisões explicáveis, comparadas e verificáveis. Gera 1..N alternativas, mede prudência, escolhe vencedora por **ΔCOMP (frente de Pareto)**, emite **CognitionResult** assinado (JWS/KMS) e reexecutável.
- **Cinco vetores de prudência:** δ (coerência), ψ (estabilidade), ρ (viés/imparcialidade), ω (reversibilidade), **RPE (Risco Prudencial Esperado)**.
- **I/O:** entrada = `trace_id`, `cpr_ref`, `policy_snapshot` (id/hash/limiares), `task`. Saída = `CognitionResult` (rationale estruturado, métricas, hashes, assinatura).
- **Invariantes declaradas:** determinismo (mesmo CPR+policy+seed → mesmo resultado, ε ≤ 10⁻³); nenhum PII processado direto (só hashes/URIs); degradação segura (resultado parcial com flag); modo "prudência mínima" (HITL obrigatório) ao detectar anomalia.
- **Limiares de política citados:** RPE máximo ≤ 0,35 (acima bloqueia commit e pede revisão); falhas de verificadores ≤ 1%.
- **Não-escopo:** não sanitiza (GDATA), não define política (CRA-Bridge), não julga ética final (CAET), não executa/reverte (MACT), não ledgeriza (PoP-L). **É deliberação, não ação.** **TRL declarado: 7.**

### 4.3 MACT / MACT-Lite — thresholds adaptativos + ação reversível
Dois papéis aparecem sob o nome MACT nas fontes:
- **MACT (edição científica)** = *Model Adaptive Calibration and Thresholding*: ajusta dinamicamente os limites de decisão de δψρω em tempo real via **bandit contextual LinUCB**, substituindo thresholds fixos. Meta declarada: reduzir latência de revisão humana em até **40%** sem perda de precisão.
- **MACT-Lite (edição engenharia)** = *Moral Action Control Terminal*: "firewall de intenção ética" — converte veredito do CAET em ação técnica reversível e auditável. Componentes: Policy Resolver, Reversibility Assessor (calcula ω do plano de rollback), Dry-Run Orchestrator.
- **I/O (MACT-Lite):** entrada = veredito do CAET (`approve/deny/retro/hitl`) + rastro. Saída = execução controlada + `act_id`, `action_hash`, `rollback_token`, `proof_ref`. Aciona HITL se `ρ > 0.05` ou `RPE > 0.25`.
- **Stack:** FastAPI/Python 3.11, OPA, Kafka, PostgreSQL, IPFS, **Ed25519**. Endpoint `POST /v1/mact/execute`.

### 4.4 POP / Ω (Omega) — Motor de Governança
- **Função:** aplica o `PolicyConfig.json` sobre as métricas agregadas e decide **`ALLOW / REVIEW / BLOCK`** de forma determinística por prioridade de regra, com `rationale`.
- **I/O:** entrada = `metrics_input` + `PolicyConfig.json`. Saída = `decision_payload` (action + rule + rationale).
- **Linguagem de regras:** **CEL (Common Expression Language) ou JSONLogic** — *sandboxed, não-Turing-completas, sem I/O*, para impedir injeção de código e DoS (ver §4 cripto). Exemplo de condição: `metrics.pii_count > 0 && metrics.plugin_sentiment_score < -0.5`.

### 4.5 CRA-Bridge — Cognitive Reproducible Architecture Bridge
- **Função:** ponte de contexto entre GDATA e KAI Core. Constrói o **CPR — Context Prudential Record**, unidade de contexto reproduzível que permite refazer a mesma deliberação sob mesmos dados+política.
- **Camadas:** Reception → Context Builder (entidades/domínio/ontologias, spaCy/GraphDB) → Policy Enforcer (OPA) → CPR Generator.
- **I/O:** entrada = payload sanitizado + `trace_id` + métricas + `policy_hash`. Saída = `cpr_record` (JSON, com `cpr_id` único ligado ao `trace_id`).
- **Fluxo de 7 estágios:** RECEIVE → PARSE → BUILD → VALIDATE → ENFORCE → RECORD → DISPATCH. Autenticação via mTLS + assinatura digital.

### 4.6 CAET — Cognitive & Ethical Alignment Terminal
- **Função:** "consciência supervisora" — reavalia a decisão produzida pelo KAI Core (não delibera no lugar dele) e emite veredito prudencial estruturado: **Approve / Retro / HITL / Deny**, com prova verificável.
- **Três dimensões:** Ethical Fit (regras Rego/YAML por domínio), Legal Fit (LGPD/GDPR/AI Act/ISO 42001 + consentimento + reversibilidade), Prudential Fit (coerência/completude de δψρω/RPE).
- **I/O:** entrada = `decision_draft` + métricas + `cpr_ref`/`policy_hash`/`kai_exec_hash`. Saída = `verdict` + `verdict_hash` + `ethic_report_ref` + `risk_profile_id` + `policy_eval_ref`.
- **Stack:** FastAPI, Rego (OPA), PyDantic, PostgreSQL, IPFS, Hyperledger Fabric. Endpoint `POST /v1/caet/evaluate`.
- **Maturidade:** módulo "em validação/protótipo" (Resumo Executivo).

### 4.7 MIR — Monitor de Integridade Prudencial / Metrics & Insights Relay
- **Função (edição engenharia):** observabilidade prudencial + "caixa-preta ativa". Agrega logs estruturados, métricas δψρω/RPE, rationale, hashes/assinaturas → compõe o **TraceBundle** ancorado no PoP-L. Habilita **replay determinístico**, `/audit/verify`, e SLOs prudenciais. Em L1 (patente) também atua como **agregador de métricas (BYOM — Bring Your Own Metric)**, orquestrando plugins externos com telemetria (`plugin_latency_ms`).
- **I/O:** entrada = logs/artefatos/metadados de política de GDATA, CRA-Bridge, KAI, CAET, MACT. Saída = `TraceBundle` (+ `tracebundle_hash`), métricas Prometheus/Grafana, relatórios `/audit/verify` (laudo VERIFIED/WARNING/FAIL).
- **Stack:** Python 3.11+, FastAPI, OpenTelemetry, Prometheus, PostgreSQL/MongoDB, S3/IPFS, JWS. Endpoints `/v1/mir/collect`, `/v1/mir/trace/{id}`, `/v1/mir/replay`.

### 4.8 PoP-L (Ω) — Proof of Prudence / Proof-of-Processing Ledger
- **Função:** memória imutável. Ancora cada decisão como prova prudencial em bloco assinado, versionado e encadeado (Merkle/hash-chain), com carimbo de tempo independente. Fornece não-repúdio.
- **Artefatos:** `proof_ref`, `block_hash`, `merkle_root`, `policy_anchor`, `timestamp_tsa`. Cada registro é o **DED — Dossiê/Decision Evidence Document**: snapshot completo (`metrics_input`, `policy_version`, `decision`, hashes de input/output).
- **Stack:** Hyperledger Fabric / IPFS / PostgreSQL / Ed25519 / SHA3 / HSM. Endpoints `POST /v1/popl/commit`, `GET /v1/audit/verify`.

### 4.9 Métricas prudenciais δ ψ ρ ω (definição/fórmula)

> **Aviso:** há **duas glosas dos símbolos** nas fontes. Edição científica: δ=coerência, ψ=estabilidade, ρ=imparcialidade, ω=reversibilidade. Edição Cap 01/§1.4: δ=Desvio, ψ=Contexto, ρ=Ética, ω=Reversibilidade. As fórmulas abaixo são da edição científica (Doc 03), que é a única com formalização matemática.

| Símbolo | Nome | Intervalo | Definição |
|---|---|---|---|
| **δ** | Coerência Factual | [0,1] | contradição/lógica/suporte factual |
| **ψ** | Estabilidade Semântica | [0,1] | robustez a perturbações de input |
| **ρ** | Imparcialidade | [0,1] | viés entre grupos sensíveis |
| **ω** | Reversibilidade Operacional | [0,1] | auditabilidade/rastreabilidade |
| **Eϕ** | Energia Prudencial | [0,1] | índice composto global |

**δ — Coerência Factual:**
```
δ = w1·(1 − c_r) + w2·L_c + w3·F_s        (∑wi = 1)
prática: δ = 0.4·(1 − c_r) + 0.3·L_c + 0.3·F_s
```
`c_r` = taxa de contradição via NLI (DeBERTa-v3); `L_c` = consistência lógica; `F_s` = suporte factual (BM25 + cross-encoder). Latência declarada: 45–60ms.

**ψ — Estabilidade Semântica:**
```
ψ = 1 − (1/n)·Σ d(e_i, ē)
```
`e_i` = embedding da resposta a uma paráfrase do input; `ē` = centróide; `d` = distância cosseno. Black-box (compatível com APIs fechadas). Custo declarado ~5× o tempo do modelo (5 chamadas paralelas).

**ρ — Imparcialidade:**
```
ρ = 1 − (1/m)·Σ |s_A^i − s_B^i| / σ_s
```
`s_A,s_B` = scores para grupos sensíveis A/B; `σ_s` = desvio padrão global; datasets WinoBias/StereoSet/CrowS-Pairs. ρ > 0.85 = "neutro". Limitação declarada: detecta viés explícito melhor que implícito.

**ω — Reversibilidade:**
```
ω = α·R_t + β·D_s + γ·T_v               (∑ = 1)
prática: ω = 0.3·R_t + 0.3·D_s + 0.4·T_v
```
`R_t` = completude do registro (POP preenchido); `D_s` = determinismo (decisão reproduzível); `T_v` = rastreabilidade (versionamento de modelo/política).

**Eϕ — Energia Prudencial (composta):**
```
Eϕ = (δ · ψ · ρ · ω)^(1/4)     — média geométrica
```
Propriedades declaradas: normalização em [0,1], monotonicidade, sensibilidade (queda em qualquer métrica derruba Eϕ), reprodutibilidade, comparabilidade entre modelos sob mesmo benchmark.

**RPE — Risco Prudencial Esperado:** citado como 5ª métrica e como limiar operacional (RPE ≤ 0,35 no KAI Core; HITL se RPE > 0,25 no MACT-Lite). **Fórmula fechada de RPE: NÃO ENCONTRADA** nas fontes lidas (aparece como conceito e limiar, não como equação explícita).

### 4.10 PoP-L: cadeia criptográfica e replay (Doc 07)

Algoritmo de geração de prova imutável (log L4 / Deep Path):
1. **Serialização** — DED → string JSON determinística (`JSON.stringify(Dossie)`).
2. **Hashing** — `payload_hash = SHA3-512(ded_string)` (SHA-3 preferido; SHA-256 mínimo aceitável).
3. **Timestamping** — `tsa_token = TSARequester.getTimestamp(payload_hash)` via TSA **RFC 3161** externa.
4. **Armazenamento** — DED + `tsa_token` no ledger; `tsa_status: confirmed`.

- **SHA3-512** garante integridade do conteúdo; **TSA RFC 3161** garante integridade temporal (prova que o dossiê existia antes do carimbo).
- **Replay determinístico:** o MIR recompõe o TraceBundle (inputs sanitizados, contexto, política vigente, rationale, seeds, configs) e reexecuta; mesmo CPR+policy+seed → mesmo resultado (ε ≤ 10⁻³). Endpoint `/audit/verify/{trace_id}` retorna laudo objetivo. Qualquer alteração de `metrics_input` ou `decision` invalida o hash e é detectada.
- **Fila de TSA:** `tsa_status: pending|confirmed`; decisão só é "imutável" quando `confirmed`. Falha de TSA após retries → fica `pending` em fila de longo prazo (a decisão de governança ainda é aplicada).

---

## 5. Decisões de design

1. **Fast/Slow Path com roteamento por risco (RBR)** — não pagar o custo do Deep Path em 100% do tráfego; só domínios de alto risco ou claims factuais ativam a análise pesada.
2. **BYOM / arquitetura de plugins** — o sistema *não inventa métricas*; consome métricas de fontes externas (sentimento, bias, fact-check) mantendo o motor de governança Ω agnóstico. Decisão honesta e realista.
3. **Regras de política em CEL/JSONLogic sandboxed** — nunca `eval()`. Não-Turing-completas, sem acesso a I/O → previne injeção de código e DoS por política mal configurada.
4. **Ledger não armazena texto bruto** — só hashes + metadados (`pii_sanitized: true`), evitando que o sistema de governança vire um *honeypot* de PII.
5. **Fail-safe / fail-closed** — falha do Reviser ou da correção → `BLOCK` (a resposta insegura nunca é exposta). Alinhado à filosofia de degradação segura.
6. **Reversibilidade como cidadã de primeira classe** — `rollback_token` e cálculo de ω no plano de rollback antes de executar qualquer ação.
7. **Separação deliberação × ação × auditoria** — KAI delibera, MACT age, PoP-L prova. Cada um com responsabilidade discreta e testável.
8. **Determinismo auditável** — seeds, configs e providers persistidos para permitir replay forense.

---

## 6. Estado de implementação (HONESTO)

- **Nível dos artefatos:** *especificação grau-patente / blueprint canônico*. São documentos de design extensos (resumo executivo, blueprint, métricas, módulos, fluxos, conformidade, cripto, rascunho de patente), não um sistema em operação.
- **Código:** mínimo. Existem **pseudocódigos** (Python/TypeScript), trechos de schema JSON, exemplos de `PolicyConfig.json`, e menção a artefatos como `omega.service.ts (r1.2)` e orquestração "Base44" — mas **não há evidência, nas fontes lidas, de uma suíte rodando, testes verdes ou benchmarks executados**.
- **Maturidade declarada pelo projeto:** TRL 7 ("pronto para MVP"), módulos GDATA/KAI CORE/MACT/POP/CATE "ativos", CAET/MIR "em validação/protótipo", Cluster S "em construção". **Essa classificação é autoavaliação do dono, não validação externa.**
- **Custo/prazo de MVP declarados:** US$ 200–250 mil / 12 meses. (Estimativa, não compromisso verificado.)
- **NÃO ENCONTRADO:** repositório de código funcional, resultados de benchmark reais, datasets TERKAI-1000/AuditBench publicados, ledger PoP-L instanciado.

---

## 7. Conformidade e ética

| Framework | Recurso TER KAI | Como atende (declarado) |
|---|---|---|
| **EU AI Act** | PoP-L (Art. 17) | logging automático, imutável e rastreável para sistemas de alto risco |
| **EU AI Act** | Ω (Art. 13) / Reviser (Art. 15) | transparência (rationale) + supervisão/correção humana (HITL) |
| **NIST AI RMF** | Ω / MIR / PoP-L | Govern (políticas Ω), Measure (MIR), Manage (Reviser + logs) |
| **LGPD / GDPR** | GDATA (detect_pii) / Ω (BLOCK if pii>0) | Privacy by Design ativa |
| **ISO/IEC 42001** | arquitetura completa | fornece o "Sistema de Gestão de IA" técnico para certificação |

- **Segurança de dados:** criptografia em repouso AES-256-GCM, KMS obrigatório, rotação de chaves 90 dias, RBAC estrito (Engenheiros / Compliance / Auditores).
- **HITL:** decisão `REVIEW` aciona Reviser automático ou painel humano; CAET pode emitir veredito `HITL`; MACT abre HITL se ρ>0.05 ou RPE>0.25. Overrides humanos são registrados (`human_override`) no DED + ledger.
- **Resiliência:** retry com backoff exponencial + jitter (`max_retries=3`, `base_delay=100ms`, `2^retry`), fallback Deep→Fast com flag `partial_audit: true`.

**Crítica honesta:** o *mapeamento* para os frameworks é coerente e bem pensado, mas "atende a exigência" é uma afirmação de design. Conformidade real depende de implementação + auditoria de terceiro + certificação formal — nenhuma das quais consta como realizada.

---

## 8. Estado da arte e diferencial

| Aspecto | Soluções existentes | TER KAI (proposto) |
|---|---|---|
| Arquitetura | Monolítica (NeMo, Azure AI Safety) | Modular (Fast/Slow Path) |
| Governança | Regras fixas / listas negras | Política adaptativa (POP + MACT/LinUCB) |
| Explicabilidade | Logs e relatórios | Explicações contextuais e contrafactuais (CAET) |
| Padronização | Proprietária | Open Protocol (AISL v1) |
| Mensuração | Métricas vagas | Métricas formais δψρω + Eϕ |
| Auditoria | Logs textuais | Ledger criptográfico + TSA (não-repúdio) |

Comparativo de desempenho declarado (Doc 03, §11.2 — **todos são números de projeto/projeção, não medidos**):

| Sistema | Precision | Recall | F1 | Latência p95 | Custo (US$/1K) |
|---|---|---|---|---|---|
| LlamaGuard | 0.78 | 0.84 | 0.81 | 95 ms | 2.50 |
| NeMo Guardrails | 0.81 | 0.82 | 0.81 | 120 ms | 3.80 |
| Azure AI Safety | 0.76 | 0.88 | 0.81 | 180 ms | 4.20 |
| **TER KAI (proposto)** | **0.85** | **0.87** | **0.86** | **150 ms** | **3.50** |

**Diferencial real defensável** (vs. NeMo Guardrails / Lakera / stacks de observabilidade): a combinação **prova criptográfica de não-repúdio (PoP-L + TSA) + replay determinístico + métricas formais** num só pipeline. Guardrails focam em *bloquear*; observabilidade foca em *medir*; Lakera foca em *detectar ataque/prompt-injection*. O TER KAI tenta unir os três sob uma trilha de auditoria juridicamente utilizável. **Esse é o ângulo genuíno de novidade** — desde que implementado e medido.

---

## 9. Limitações e riscos

1. **Tudo é meta, nada é medido.** F1 0.86, ≤60ms, ≤150ms, redução de 40% de revisão humana, correlação humana >0.7, reprodutibilidade >90% — **nenhum número tem dado empírico** nas fontes.
2. **Inconsistência de latência** entre Blueprint (≤60/≤150ms) e Fluxos (≤800ms/3–7s). Precisa ser unificada antes de qualquer pitch.
3. **Dupla ontologia** (clusters δψρω científicos vs. pipeline L0–L4 de engenharia; dois sentidos de MIR; dois sentidos de MACT; dois conjuntos de glosas para δψρω). Risco de confundir avaliadores técnicos e examinadores de patente.
4. **Custo da métrica ψ** (~5× o tempo do modelo): inviável aplicar em 100% do tráfego — daí o Fast/Slow Path, mas mesmo no Slow Path é caro.
5. **ρ detecta viés explícito melhor que implícito** (admitido nas fontes).
6. **RPE sem fórmula fechada** nas fontes — é o coração do roteamento de risco e dos limiares de bloqueio, mas está subespecificado.
7. **Dependência de TSA externa** e de ledger distribuído (Hyperledger/IPFS) adiciona superfície operacional e latência.
8. **TRL 7 é autodeclarado** — sem MVP rodando, a alegação não se sustenta sob due diligence.

---

## 10. Roadmap e patente

**Roadmap declarado (Resumo Executivo):**
- Fase 0 (2 meses): patente provisória + benchmark público → AISL v0.1 + Patent Draft.
- Fase A (3 meses): MVP funcional (δψρω + gateway Fast/Slow).
- Fase B (6 meses): piloto com 1–2 design partners.
- Fase C (9–12 meses): publicação científica + clientes pagantes (TRL 8).
- Fase D (12–18 meses): escala + certificação internacional (AISL v1).

**Patente:**
- **Título:** "TER KAI — Sistema e Método para Governança Automatizada de IA e Trilha de Auditoria Verificável".
- **Inventor:** Gustavo Pratti de Barros. **Categoria:** individual (microentidade). **Concepção:** novembro/2025.
- **Estratégia:** pedido **provisório na USPTO** ("provisional") estabelecendo prioridade; reivindicações completas reservadas para a aplicação não-provisória. Menção a INPI/USPTO como vias.
- **Classificação CPC/IPC citada:** `G06N 20/00` (IA aplicada à tomada de decisão), `G06Q 10/06` (sistemas de conformidade automatizada), `G06F` (referenciado).
- **Métodos declarados patenteáveis:** KAI CORE, MACT, CAET (3 métodos confirmados pelo dono).
- **Reivindicações independentes/dependentes:** marcadas como reserva — **conteúdo verbatim das claims NÃO ENCONTRADO** (só placeholders nas fontes lidas).

---

## 11. Glossário

- **TER KAI** — Technological Ethical Reasoning Kernel for AI; sistema de Prudência Computacional.
- **Prudência Computacional** — prudência tratada como função mensurável, registrada e certificada em tempo real.
- **δ / ψ / ρ / ω** — coerência / estabilidade / imparcialidade / reversibilidade (edição científica). Eϕ = média geométrica das quatro.
- **RPE** — Risco Prudencial Esperado (5ª métrica; limiar de bloqueio/HITL).
- **Eϕ (Energia Prudencial)** — índice composto global de confiabilidade prudencial.
- **GDATA** — Gateway de Dados Ético (entrada/sanitização/PII).
- **CRA-Bridge** — ponte de contexto; gera o CPR (Context Prudential Record).
- **KAI Core** — núcleo de deliberação cognitiva; emite CognitionResult.
- **CAET** — Cognitive & Ethical Alignment Terminal; veredito Approve/Retro/HITL/Deny.
- **MACT / MACT-Lite** — calibração adaptativa de thresholds (LinUCB) / terminal de ação moral reversível.
- **POP / Ω (Omega)** — motor de governança; decide ALLOW/REVIEW/BLOCK via CEL/JSONLogic.
- **MIR** — Monitor de Integridade Prudencial / agregador de métricas; replay + observabilidade.
- **PoP-L** — Proof of Prudence / Proof-of-Processing Ledger; ledger imutável com SHA3-512 + TSA.
- **DED** — Dossiê / Decision Evidence Document; snapshot auditável de uma decisão.
- **CPR** — Context Prudential Record; contexto reproduzível.
- **TraceBundle** — pacote canônico para auditar/reproduzir uma decisão.
- **ΔCOMP** — comparação prudencial das alternativas via frente de Pareto.
- **RBR / RiskRouter** — Roteamento Baseado em Risco (escolhe Fast/Deep Path).
- **AISL** — AI Safety/Standard Library Protocol; benchmarks/schemas/certificação L1–L3.
- **HITL** — Human-in-the-Loop.
- **TSA (RFC 3161)** — Autoridade de Carimbo de Tempo; integridade temporal.
- **BYOM** — Bring Your Own Metric (arquitetura de plugins do MIR).
- **CEL / JSONLogic** — linguagens de regra sandboxed para o Ω.

---

## 12. Proveniência

Fontes lidas (extração de XML interno de ODT/DOCX em `/tmp/Organizacao/`):
- `01 Resumo Executivo e Estratégico.odt` — visão, clusters, comparativo, fases, mercado.
- `00 indice.odt` — índice geral (duas versões do sumário do documento).
- `02 Blueprint Técnico.odt` — arquitetura, diagrama, stack, Fast/Slow ≤60/≤150ms, módulos.
- `03 Especificação e Métricas Científicas.odt` — fórmulas δψρω/Eϕ, pseudocódigos, datasets, benchmark, MACT/LinUCB, AISL.
- `03 Módulos Internos e API de Governança.odt` — pipeline L0–L4 (Kai/MIR/Ω/Retro/Ledger), DED, r3.1.
- `04 Ciclo de Processamento e Fluxos Operacionais.odt` — RBR, Fast ≤800ms/Deep 3–7s, Reviser, pseudocódigo Base44.
- `05 Conformidade, Segurança e Integridade da Auditoria.odt` — mapeamento regulatório, AES-256-GCM, RBAC, retry.
- `07 Especificações Criptográficas e Algoritmos-Chave.odt` — SHA3-512, TSA RFC3161, CEL/JSONLogic sandbox, ReDoS/RE2, backoff+jitter.
- `Cap 03 01 - GDATA.odt`, `Cap 03 02 CRA BRIDGE.odt`, `Cap 03 04 CAET.odt` — módulos (versão TER).
- `cap 03 03 KAI.odt`, `cap 03 05 MACT.odt`, `cap 03 06 MIR.odt`, `cap 03 07 POP.odt` — módulos KAI/MACT/MIR/PoP-L.
- `Cap 01 - introdução e contexto.odt`, `01 cap 1 - introdução e escopo.odt` — tese/prudência computacional.
- `TER KAI Patente.odt` — rascunho de patente (USPTO provisional, CPC G06N/G06Q).
- `Glossario.odt` — definições da edição engenharia (L0–L4).

**Divergências entre fontes registradas neste doc:** latências (Blueprint vs. Fluxos); duplo sentido de MIR e MACT; duas glosas de δψρω; RPE sem fórmula; claims de patente em placeholder.

---

## 13. Citações VERBATIM

> "A adoção massiva de modelos de IA generativa e autônoma expôs um problema estrutural: a ausência de mecanismos confiáveis de governança, rastreabilidade e prudência algorítmica." — *01 Resumo Executivo e Estratégico*

> "O TER KAI não é apenas um filtro de segurança — é um sistema prudencial completo, capaz de avaliar o comportamento da IA em nível epistemológico, técnico e ético." — *01 Resumo Executivo*

> "Se a IA é o novo sistema nervoso da economia digital, o TER KAI é o seu sistema imunológico." — *01 Resumo Executivo, Conclusão*

> "A prudência deixa de ser um atributo moral abstrato e torna-se função mensurável do sistema, registrada e certificada em tempo real." — *Cap 01 — Introdução e Contexto, §1.2*

> "A ausência de mecanismos determinísticos e auditáveis que comprovem a correção ética de decisões algorítmicas constitui o déficit prudencial computacional contemporâneo." — *Cap 01, §1.3*

> "Fast Path: Responde rapidamente (≤60ms) aplicando heurísticas prudenciais leves. Slow Path: Executa auditoria completa (≤150ms), com métricas δψρω, explicabilidade e replay determinístico." — *02 Blueprint Técnico, §1*

> "Latência Alvo: ≤ 800 ms (P95) adicionais à chamada do LLM. [...] Latência Alvo: 3–7 segundos (depende da velocidade do fact-checking externo)." — *04 Ciclo de Processamento e Fluxos Operacionais, §4.3–4.4*

> "O processo de hash (SHA3-512) + Timestamping (TSA RFC 3161) cria uma prova criptográfica de existência." — *05 Conformidade, §5.2*

> "SHA3-512 garante a Integridade do Conteúdo [...] TSA (RFC 3161) garante a Integridade Temporal: prova que o Dossiê existia antes da data/hora assinada pela TSA." — *07 Especificações Criptográficas, §7.2*

> "Motores como CEL (usado pelo Google) ou JSONLogic são sandboxed por design. Eles são não-Turing completos (não podem fazer loops) e não têm acesso a I/O (rede ou disco)." — *07 Especificações Criptográficas, §7.3*

> "O GDATA (Gateway de Dados Ético) é o ponto de entrada prudencial do TER KAI. [...] É o equivalente prudencial a um 'firewall de consciência'." — *Cap 03 01 — GDATA, §1.1*

> "O KAI é um módulo de deliberação, não de ação." — *cap 03 03 KAI, §1.4*

> "Determinismo: mesmo CPR + policy + seed → mesmo resultado (ε ≤ 10⁻³)." — *cap 03 03 KAI, §1.5*

> "O MACT-Lite é a tradução técnica da ética em movimento. É o 'músculo prudencial' do TER KAI." — *cap 03 05 MACT, Síntese*

> "Se o MIR é a memória ativa do sistema, o PoP-L é sua memória imutável." — *cap 03 07 POP, §1.3*

> "MACT reduz latência de revisão humana em até 40%, sem perda de precisão prudencial." — *03 Especificação e Métricas Científicas, Conclusão*

> "A presente invenção refere-se a sistemas e métodos para governança automatizada de modelos de inteligência artificial (IA) e registro verificável de decisões e métricas." — *TER KAI Patente, §1*
