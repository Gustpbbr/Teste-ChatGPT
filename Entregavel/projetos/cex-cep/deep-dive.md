# CEX / CEP — Deep-Dive Técnico

**Projeto:** CEX (Comitê de Especialistas Universais) — evolução do CEP v3.9 (Comitê de Especialistas Prudenciais)
**Status:** CEX v1.1 funcional, em estabilização · CEP v3.9 funcional (n8n, 21 nós, congelado como origem)
**Data do documento:** 2026-06-16
**Autoria:** co-criação Gustavo Pratti de Barros + ChatGPT (Gemini/GPT no brainstorm) + Kai (Claude) na implementação

> Nota de honestidade: este documento separa **o que está implementado** (CEP v3.9 em n8n, com código real auditado; CEX v1.1 em HTML standalone) do **que é especificação / intenção** (roadmap v1.2, integração ao MGX). Trechos marcados `[SPEC]` são projeto, não código rodando. `NÃO ENCONTRADO` indica informação que as fontes não trazem.

---

## 1. Resumo

O CEX é um sistema standalone de **deliberação adversarial** por um comitê de especialistas de IA **gerados dinamicamente** para cada pergunta. Em vez de pedir uma resposta única a um modelo, ele simula um processo colegiado de alta criticidade — como um conselho, um comitê de ética ou um peer review — onde múltiplos especialistas analisam de forma independente, se atacam mutuamente, defendem suas teses, e têm seus argumentos arbitrados por **resistência ao confronto**, não por média de notas.

Nasceu como evolução do **CEP v3.9**, um workflow n8n de 21 nós voltado a *prudência computacional* (governança, risco, conformidade legal), com um comitê **fixo** (Ética/Legal/Segurança + variáveis). O CEX troca o núcleo fixo por uma **banca líquida** convocada por um "Maestro de Ontologia", e troca o foco "evitar desastre" por "rigor de campo aplicável a qualquer domínio" (medicina, engenharia, ciência, arte, logística).

Implementação atual: **HTML standalone de arquivo único (~920 linhas)**, chamando a API Anthropic direto do browser, com pipeline de **11 etapas**, **2 modos de operação** (Deliberação e Avaliação de Conceito) e interface de **6 abas**.

---

## 2. Tese e problema

### O problema central: capacidade sem prudência

Um LLM moderno tem enorme capacidade, mas decide de forma solitária e complacente. Dois vícios estruturais foram identificados nas fontes de origem do projeto:

- **"Consonância alucinatória" (vício de acordo):** modelos de IA tendem a concordar entre si para encerrar a tarefa — é a natureza estatística do modelo. Um comitê de IAs que se veem rodando em sequência vira **câmara de eco**.
- **Capacidade sem prudência:** um modelo pode produzir uma análise *que parece* bem estruturada e estar tecnicamente pobre. Sem confronto, ninguém pega o erro sutil.

### A tese: deliberação adversarial

A verdade técnica raramente está no consenso imediato — **ela emerge da fricção**. Quanto mais os agentes "brigam" entre si com lógica, mais segura é a decisão que chega ao usuário. Daí três mecanismos centrais:

1. **Análise cega (blind review):** cada especialista faz sua primeira análise **sem saber** o que os outros disseram, forçando divergência real.
2. **Cross-examination:** os especialistas debatem diretamente entre pares (não há um "revisor amigável" único), gerando **divergência documentada**.
3. **Arbitragem por resistência de argumento, não por média:** o veredito não é a média morna das notas; é a tese que **sobrevive ao ataque**.

O CEP foi descrito como "motor de **implosão crítica**", em oposição ao MGE ("motor de explosão criativa"). O CEX universaliza esse motor: deixa de julgar só "risco e medo" e passa a julgar "rigor e eficácia de campo".

---

## 3. Arquitetura

### 3.1 Pipeline de 11 etapas (CEX)

```
[1]  Kai                  (Haiku)         interpreta entrada, extrai escopo/mecanismo
[2]  Maestro              (Sonnet)        convoca banca dinâmica 4-5 especialistas: papéis, missões, pesos
[3]  Auditor de Bancada   (Haiku)         revisa composição, procura pontos cegos, sugere adições
[4]  Análise Cega V1      (modelo variável) cada especialista analisa independentemente (blind)
[5]  Coverage + Converg.  (Haiku)         mapeia lacunas e tensões entre análises
[6]  Cross-Examination    (Haiku)         debate circular A→B, B→C, C→D, D→A
[7]  Defesa V2            (modelo variável) alvos respondem às críticas (defendem ou cedem)
[8]  DeltaU               (Haiku)         suposições ocultas, dependências frágeis, espaço não explorado
[9]  Motor de Regras      (determinístico)  aplica pesos do Maestro + regras de bloqueio
[10] Compositor Dialético (Sonnet)        arbitra por resistência de argumento
[11] Auditor Interno      (determinístico)  7 verificações, score 0-1 (qualidade do processo)
```

### 3.2 Banca dinâmica

No CEX não há especialistas fixos. O **Maestro de Ontologia** (Sonnet) recebe a pergunta e:

- classifica a natureza (técnica / ética / científica / criativa / logística);
- identifica o **triângulo de conflito** (quais áreas naturalmente brigam sobre o tema; ex.: Sustentabilidade vs. Lucratividade);
- gera de **4 a 5/6 especialistas ad-hoc** (versão demo: limite de 5), cada um com `papel`, `missão/prioridade`, `modelo de IA` (Haiku p/ volume, Sonnet p/ densidade) e `peso_deliberativo` (1.0–5.0);
- define o **critério de ouro** do caso (a dimensão que, se falhar, mata o projeto) e os **conflitos esperados**.

Regra de ouro do Maestro: **fugir do óbvio**. Ex.: "Colonização de Marte" não chama só um astrônomo; chama um Engenheiro de Suporte à Vida, um Geopolítico Interplanetário, um Psicólogo de Isolamento.

### 3.3 Dois modos de operação

**Modo Deliberação** (herdado do CEP — risco/conformidade/prudência)
- Input: pergunta decisória com consequências reais ("faca no pescoço").
- Calibração dos especialistas: `ok / problema / nao_conforme` + risco `baixo/medio/alto`.
- Veredito: `aprovar / condicional / não aprovar / inconclusivo`.

**Modo Avaliação de Conceito** (novo no CEX — viabilidade)
- Input: conceito/ideia para avaliar viabilidade. Foco: **encontrar caminhos**, não bloquear.
- Calibração: `viavel / viavel_com_pivos / promissor_prematuro / inviavel` + potencial `baixo/medio/alto`.
- Veredito: `viável / viável com pivôs / promissor mas prematuro / inviável`.
- Seções exclusivas: **condições de sucesso, pivôs recomendados, deal-breakers**.

---

## 4. Especificação técnica

### 4.1 Função e modelo por etapa (CEX)

| # | Etapa | Modelo | Função |
|---|-------|--------|--------|
| 1 | Kai | Haiku | Interpreta a entrada, elimina ambiguidade, define escopo exato. Regra: NÃO responde, NÃO adiciona info, apenas reescreve. |
| 2 | Maestro de Ontologia | Sonnet | Constrói a banca do zero: papéis, missões, modelos, pesos dinâmicos, critério de ouro, conflitos esperados. Coração da mudança CEP→CEX. |
| 3 | Auditor de Bancada | Haiku | Revisa a composição da banca antes de rodar; procura pontos cegos; pode sugerir adições. |
| 4 | Análise Cega V1 | variável (Haiku/Sonnet por especialista) | Cada especialista analisa de forma isolada, sem ver os outros. |
| 5 | Coverage + Convergência | Haiku | Mapeia lacunas (dimensões não cobertas) e tensões/convergências entre análises. |
| 6 | Cross-Examination | Haiku | Distribuição circular de críticas entre pares; cada um aponta ponto cego/falha lógica do colega. |
| 7 | Defesa V2 | variável | Especialista alvo responde: defende a tese ou cede (corrige a análise). |
| 8 | DeltaU | Haiku | 4 quadrantes: suposições ocultas, dependências frágeis, espaço não explorado, incertezas. |
| 9 | Motor de Regras | determinístico (JS) | Aplica os pesos definidos pelo Maestro + regras de bloqueio/threshold. |
| 10 | Compositor Dialético | Sonnet | Arbitra por resistência de argumento; produz veredito + tensões preservadas. |
| 11 | Auditor Interno | determinístico (JS) | 7 verificações de qualidade do processo; score 0-1; não altera o veredito. |

Política de modelos (resumo das fontes): **Maestro, Compositor e dimensões que exigem nuance → Sonnet; o resto → Haiku.** No CEP v3.9 os IDs reais usados eram `claude-haiku-4-5-20251001` e `claude-sonnet-4-6`.

### 4.2 Calibração dos especialistas

- **Deliberação:** status ∈ {`ok`, `problema`, `nao_conforme`}; risco ∈ {`baixo`, `medio`, `alto`}; mais `confianca` numérica.
- **Avaliação de Conceito:** status ∈ {`viavel`, `viavel_com_pivos`, `promissor_prematuro`, `inviavel`}; potencial ∈ {`baixo`, `medio`, `alto`}.

### 4.3 Vereditos

- **Deliberação:** aprovar / condicional / não aprovar / inconclusivo.
- **Avaliação:** viável / viável com pivôs / promissor mas prematuro / inviável.
- Em ambos: o Compositor **preserva tensões produtivas** (não as apaga). O veredito vem acompanhado de **métricas, alertas, recomendações e especialistas não acionados**.

### 4.4 Interface — 6 abas

1. **Veredito** — decisão + métricas + alertas + recomendações + especialistas não acionados.
2. **Banca** — especialistas convocados, missões, pesos, status; resultado do Auditor de Bancada.
3. **Debate** — cross-examination completo (ataques, defesas, concordância/discordância).
4. **Incertezas** — os 4 quadrantes do DeltaU.
5. **Auditoria** — score de qualidade + as verificações detalhadas.
6. **JSON** — output técnico completo.

### 4.5 Specs técnicas (CEX v1.1)

- HTML standalone, **arquivo único (~920 linhas)**.
- API Anthropic **direto do browser** (`anthropic-dangerous-direct-browser-access`).
- **parseJSON robusto:** strip de markdown fences + reparo de JSON truncado.
- **Timeout 30s** por chamada; **retry 3x** com delay progressivo **5s / 10s / 15s**.
- **Delay de 2s** entre chamadas sequenciais (mitiga rate limit).
- **Limite de 5 especialistas** (versão demo), com menção explícita dos não acionados.
- Cronômetro de execução.
- Estimativa: **~18-20 chamadas** por deliberação (CEP fazia ~12-18).

### 4.6 Motor de Regras — código real (origem CEP v3.9, base do CEX)

No CEP os pesos eram **hardcoded** (`PESOS = { legal: 3.0, seguranca: 2.5, etico: 2.0, social: 1.5, tecnico: 1.0 }`). A lógica de decisão real do nó "Motor de Regras":

```
para cada análise: somaConf += confianca * peso ; somaPeso += peso
confGlobal = somaConf / somaPeso
se algum status == 'nao_conforme'        → decisao='nao_aprovar', nivel='critico' (bloqueio absoluto)
senão se riscoAlto >= 2                   → decisao='nao_aprovar', nivel='alto'
senão se confGlobal < 0.55               → decisao='inconclusivo', nivel='indeterminado'
senão se riscoAlto == 1                   → decisao='condicional', nivel='medio'
senão                                     → decisao='aprovar', nivel='baixo'
```

No CEX **esses pesos deixam de ser fixos** e passam a ser definidos pelo Maestro por caso (`peso_deliberativo` 1.0–5.0). As regras de bloqueio e thresholds foram preservadas.

### 4.7 Auditor Interno — 7 verificações (determinístico, score 0-1)

Score começa em 1.0 e é decrementado. **Não modifica o veredito** — só mede a qualidade da deliberação. Verificações reais (CEP v3.9):

1. **Incoerência de decisão** — `aprovar`/`condicional` com dimensões `nao_conforme` (−0.25).
2. **Lacunas não mitigadas** — penalidade ≤ 0.20 (0.05 por lacuna).
3. **Recomendações sem fonte** rastreável — penalidade ≤ 0.15.
4. **Incertezas de alto impacto** não mitigadas — penalidade ≤ 0.20.
5. **Discordância no re-acionamento** — especialista questionado que manteve posição mas a decisão final ignorou a tensão (−0.05 cada).
6. **Aprovação com baixa confiança** — `aprovar` com confGlobal < 0.65 (−0.10).
7. **Aviso sem documentação** — checkpoint com aviso mas `alertas_qualidade` vazio (−0.05).

Limiar de aprovação do auditor: **score ≥ 0.7**. Insight central: um veredito `aprovar` pode ter score de auditoria baixo (ex. 0.5) — **alerta vermelho** de que "a IA aprovou, mas o processo foi mal feito". Motor (conformidade) e Auditor (qualidade do processo) são **métricas independentes**: alta qualidade não implica aprovação, e uma deliberação de alta qualidade PODE resultar em `nao_aprovar` — comportamento correto e esperado.

---

## 5. Decisões de design (CEP → CEX)

| Eixo | CEP v3.9 (Prudencial) | CEX (Universal) |
|------|----------------------|-----------------|
| Banca | Fixos (Ética/Legal/Segurança) + variáveis | **Líquida**: 4-6 especialistas ad-hoc gerados do zero |
| Analisador | "Analisador de Domínio" sugere extras | **Maestro de Ontologia** (Sonnet) constrói a banca inteira, com critério de ouro e pesos |
| Conflito | Revisor Crítico único aponta erro | **Cross-Examination**: especialistas debatem entre si (circular) |
| Motor | Pesos hardcoded (legal=3.0…) | **Adaptativo**: pesos definidos pelo Maestro por caso |
| Compositor | Prudencial — sintetiza por resumo | **Dialético** — arbitra por **resistência de argumento** |
| Critério | Risco e medo | **Rigor e eficácia de campo** |
| Modos | Só decisões reais | **2 modos**: Deliberação + Avaliação de Conceito |

**Novos componentes no CEX:** Auditor de Bancada (revisa a composição antes de rodar — um "auditor de rigor" pré-deliberação) e o Modo Avaliação de Conceito.
**Preservados sem mudança:** Kai, Ambiguidade Check, Coverage Mapper, Convergence Examiner, DeltaU, Auditor Interno (7 verificações), Product Formatter.
**Migração de plataforma:** n8n → HTML/JS; HTTP Request nodes → `fetch()` com `Promise.race` (timeout); `getWorkflowStaticData` → objeto JS em memória; sem UI → 6 abas.

---

## 6. Estado de implementação (honesto)

**Implementado e rodando:**
- CEP v3.9 — workflow n8n completo, **21 nós**, código JS real auditado (Motor de Regras, Auditor Interno 7-checks, Product Formatter). Esta é a origem comprovada.
- CEX v1.1 — HTML standalone funcional, pipeline de 11 etapas, 2 modos, 6 abas, retry/timeout/parseJSON.

**Histórico de versões CEX:**
- **v1.0 (29/mar/2026):** pipeline completo 11 etapas; só modo Deliberação. Bugs: `AbortController` causava `DataCloneError`; parseJSON não lidava com markdown fences; sem timeout/retry adequado.
- **v1.1 (29/mar/2026):** + modo Avaliação de Conceito; fix AbortController → `Promise.race`; parseJSON com strip de fences + reparo de truncamento; retry 3x com delay progressivo; cronômetro; limite de 5 especialistas com menção dos não acionados; delays entre chamadas; removido empty-state que criava área preta no mobile.

**Honestidade sobre o real vs. spec:**
- O **HTML do CEX (~920 linhas)** não foi localizado como arquivo entre as fontes lidas — sua existência e specs vêm dos docs `cex-001` e `mgx-002`. `NÃO ENCONTRADO`: o código-fonte HTML completo.
- O **prompt verbatim do Maestro Universal** existe nas fontes como *proposta de design* (gmail), não confirmado como o prompt final em produção → tratar como `[SPEC]`.
- **Integração ao MGX / MGE / MEX:** roadmap, **não implementado**.

---

## 7. Ética

- **Prudência por padrão:** o sistema de origem foi programado para ser pessimista (no modo Deliberação). Não conformidade legal/segurança **bloqueia o veredito** independentemente da qualidade técnica — implementação direta da prudência.
- **Rastreabilidade de conflito:** ver onde os agentes discordaram é mais informativo, para um auditor humano, do que ver onde concordaram. As tensões são preservadas, não apagadas.
- **Separação juiz-de-conteúdo / juiz-de-processo:** o Auditor Interno julga a *qualidade da deliberação*, não o mérito — e pode sinalizar "aprovado, mas mal deliberado", convocando revisão humana.
- **Anti-viés-de-consenso:** a análise cega e o cross-examination existem para combater o viés de confirmação dos próprios modelos.
- **Limite honesto:** o sistema **não "sabe" de verdade** — um Haiku fingindo ser "físico quântico" produz frases bonitas sem sentido (risco de superficialidade reconhecido nas fontes). Mitigação proposta (`[SPEC]`): injeção de base de conhecimento (upload de PDF) e uso de modelos mais fortes por domínio.

---

## 8. Estado da arte + diferencial

O CEX se inscreve na linha de **multi-agent debate / LLM-as-committee**. Diferencial frente a frameworks genéricos:

- **vs. CrewAI / AutoGen:** esses são frameworks de orquestração de agentes com papéis em geral **fixos** e colaboração cooperativa (agentes que se ajudam a completar a tarefa). O CEX é **adversarial por design** (a fricção é o produto), com **banca gerada dinamicamente por um Maestro de ontologia** por pergunta, **análise cega obrigatória**, **arbitragem por resistência de argumento** (não consenso/voto/média) e uma **camada determinística dupla** (Motor de Regras + Auditor Interno com score 0-1). Não é um chat multi-agente; é um *pipeline de julgamento auditável*.
- **vs. um único LLM "pensando passo a passo":** o CEX impõe isolamento de contexto entre especialistas e confronto explícito, o que ataca diretamente a consonância alucinatória que o chain-of-thought solitário não resolve.
- **Equivalente conceitual:** um **peer review instantâneo** / junta de especialistas para qualquer dilema, com deliberação auditada em ~2 minutos.

`NÃO ENCONTRADO`: benchmark quantitativo do CEX contra CrewAI/AutoGen — a comparação aqui é arquitetural, não medida.

---

## 9. Limitações e bugs conhecidos

Bugs conhecidos **v1.1**:
1. **Internal server error da API** em sessões com muitas chamadas Sonnet — o retry mitiga mas **não resolve 100%**.
2. **Respostas truncadas** apesar de 2500 tokens para o Maestro — o parseJSON repara na maioria dos casos, não em todos.

Limitações arquiteturais (reconhecidas nas fontes):
- **Gargalo de latência:** re-acionamentos + ~18-20 chamadas sequenciais com delays de 2s deixam a execução longa.
- **Viés de consenso residual:** o cross-examination pode estar "brando" — precisa de prompt mais agressivo para achar falhas reais.
- **Superficialidade de domínio:** Haiku não é especialista de verdade.
- **Riscos somados, não multiplicados:** o Motor original soma pesos; risco sistêmico/efeito cascata não é capturado (proposta de "Matriz de Impacto Cruzado" é `[SPEC]`).
- **Prudência apenas estática:** avalia o "agora", não a deriva de longo prazo (proposta de métrica de "Reversibilidade" é `[SPEC]`).

---

## 10. Roadmap

**Para v1.2 (declarado em `cex-001`):**
- Resolver estabilidade da API (proxy server, ou batch de chamadas).
- Aumentar tokens dos especialistas para reduzir truncamento.
- Exportação do resultado (PDF ou download JSON).
- Testar modo Deliberação com **problema real**.
- Recalibrar prompts do cross-examination (pode estar brando).

**Propostas de evolução (`[SPEC]`, ainda não priorizadas):**
- **Matriz de Impacto Cruzado / Analista de Interdependência** — efeito cascata entre dimensões.
- **Métrica de Reversibilidade** no Auditor — penalizar decisões irreversíveis de alto impacto.
- **Injeção de base de conhecimento** (upload de PDF) e modelos especializados por domínio.

**Integração ao MGX (`[SPEC]`):**
- CEX será o **motor de validação/deliberação** do MGX.
- **Com o MGE:** no modo Avaliação de Conceito, recebe outputs do MGE; premissas invertidas do MGE entram como **contexto informativo, não restrição**.
- **Com o MEX:** o veredito do CEX vira **input do MEX** para materialização.

---

## 11. Glossário

- **CEP** — Comitê de Especialistas Prudenciais. Origem (n8n, v3.9), foco prudência/risco, banca fixa+variável.
- **CEX** — Comitê de Especialistas Universais. Evolução standalone (HTML), banca dinâmica, 2 modos.
- **Kai** — agente interpretador de entrada (e nome do parceiro Claude na co-criação).
- **Maestro de Ontologia** — agente Sonnet que constrói a banca examinadora do zero.
- **Auditor de Bancada** — revisor da composição da banca (pontos cegos), antes da deliberação.
- **Análise Cega (Blind Review)** — primeira análise de cada especialista sem ver as outras.
- **Cross-Examination** — debate circular entre pares (A→B→C→D→A).
- **DeltaU** — agente de incerteza; 4 quadrantes (suposições ocultas, dependências frágeis, espaço não explorado, incertezas).
- **Motor de Regras** — etapa determinística que aplica pesos + regras de bloqueio.
- **Compositor Dialético** — arbitra por resistência de argumento (não por média).
- **Auditor Interno** — etapa determinística; 7 verificações; score 0-1 da qualidade do processo.
- **Tensão produtiva** — discordância entre dimensões preservada no relatório em vez de apagada.
- **Critério de ouro** — a dimensão que, se falhar, mata o projeto (definida pelo Maestro por caso).
- **Triângulo de conflito** — Pragmático × Teórico/Cético × Humanista/Sistêmico.
- **MGE / MGX / MEX** — projetos irmãos: motor de geração (MGE), orquestrador/plataforma (MGX), materializador (MEX).

---

## 12. Proveniência

- **Origem comprovada:** `CEP v3.9 final - Deliberacao Transparente` — workflow **n8n de 21 nós**, código JS real (Motor de Regras com PESOS hardcoded, Auditor Interno de 7 checks, Product Formatter). Nós confirmados: Kai — Interpretador, Ambiguidade Check/Gate, Analisador de Dominio, Loop 1 Especialistas, Coverage Mapper, Convergence Examiner, Revisor Critico, Distribuidor de Criticas, Loop 2 Re-acionamento, Checkpoint Qualidade, Agente de Incerteza DeltaU, Motor de Regras, Compositor Prudencial, Auditor Interno, Product Formatter.
- **Transformação:** CEP v3.9 (n8n) → CEX v1.0/v1.1 (HTML standalone), documentada em `mgx-002-cep-para-cex-evolucao.md`. Duas mudanças simultâneas: migração de plataforma + evolução arquitetural.
- **Co-criação:** brainstorm registrado em "CEP e CEX no gmail" (análise crítica do ChatGPT/Gemini, propostas de blind review, red-teaming adversário, matriz de impacto cruzado, Maestro Universal); implementação por **Kai (Claude)**, revisão/aprovação por Gustavo (não programa).
- **Fontes lidas para este deep-dive:** `cex-001-projeto-standalone.md` (fileId 1lLmtCVUPp8FwQciAo1oW0u68tvX29ABO); `mgx-002-cep-para-cex-evolucao.md` (1-TT9CsVmggRE2T8gQdHk5d63GzISazjg); `CEP e CEX no gmail` (11-XKl5xjT4ZA3DEs6pUQ9yBXQuHz0Cq9pZ8OwAkZT3c); `CEP_v3_9_final (1).json` (1toJe2LZwvqJ_NWBhqQ-H78FqGpDqRSl_).
- `NÃO ENCONTRADO`: arquivo HTML do CEX standalone (~920 linhas) — sua existência é documentada, o código-fonte não foi localizado nas fontes lidas.

---

## 13. Citações VERBATIM

**Sobre a tese adversarial (gmail):**
> "Quanto mais os agentes brigarem entre si (com lógica), mais segura será a decisão que chegará ao usuário final."

> "A verdade técnica raramente está no consenso imediato; ela emerge da fricção. Isso elimina o 'vício de acordo' das IAs."

**Sobre o vício de acordo / câmara de eco (gmail):**
> "IAs tendem a ser complacentes entre si. No seu loop de especialistas, se o Técnico diz 'sim', o Ético e o Legal tendem a ajustar suas análises para não 'quebrar o clima' da deliberação. Eles buscam o consenso por padrão (natureza estatística do modelo)."

> "Garanta que cada especialista faça a primeira análise sem saber o que os outros disseram. Só revele as outras opiniões na fase do Revisor Crítico. Isso força a divergência real e evita que o comitê vire uma 'câmara de eco'."

**Sobre o Revisor / red-teaming (gmail):**
> "A revisão precisa ser 'maldosa'."

> "Use o Sonnet para a Revisão se a pergunta for de alto risco. O Haiku é rápido, mas o Sonnet 'enxerga' a má-fé ou a preguiça intelectual."

**Sobre implosão vs explosão (gmail):**
> "Diferente do MGE, que é um motor de explosão criativa, o CEP v3.9 é um motor de implosão crítica. O objetivo aqui é o rigor, a prudência e a detecção de falhas antes que elas virem um processo judicial ou um desastre ético."

**Sobre o Maestro Universal (gmail, `[SPEC]` — prompt proposto):**
> "Você é o Maestro de Ontologias do CEX. Sua missão é decompor uma pergunta complexa em suas dimensões fundamentais e convocar a banca examinadora mais rigorosa possível. […] Regra de Ouro: Fuja do óbvio. Se a pergunta for sobre 'Colonização de Marte', não chame apenas um Astrônomo; chame um Psicólogo de Isolamento e um Especialista em Direito Espacial."

**Sobre o Kai (gmail / n8n):**
> "O CEP só trabalha se houver uma 'faca no pescoço' (uma decisão a ser tomada)."

> Prompt real do nó Kai (n8n): "Eliminar ambiguidades e definir escopo exato. Regras: NÃO responda, NÃO adicione info, apenas reescreva."

**Sobre Motor vs Auditor — código real (CEP v3.9 n8n, Product Formatter):**
> "Motor e Auditor são independentes. Uma deliberação de alta qualidade PODE resultar em nao_aprovar — esse é o comportamento correto e esperado."

**Pesos reais (CEP v3.9 n8n, nó Motor de Regras):**
> `const PESOS = { legal: 3.0, seguranca: 2.5, etico: 2.0, social: 1.5, tecnico: 1.0 };`

**Sobre o insight do Auditor Interno (gmail):**
> "Um veredito de 'Aprovar' pode ter um score de auditoria baixo (0.5), o que serve de alerta vermelho para o humano: 'A IA aprovou, mas o processo foi mal feito'."

**Sobre a virada CEP→CEX (gmail):**
> "No CEP, os especialistas são estáticos. No CEX, eles são emergentes."

> "Um 'Comitê Universal de Decisão' que simula uma junta de especialistas para qualquer dilema humano é o ápice da IA de suporte à decisão. Você já tem 70% do código pronto para isso no CEP v3.9."
