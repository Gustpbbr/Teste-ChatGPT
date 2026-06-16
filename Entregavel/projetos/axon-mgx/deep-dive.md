# Deep-Dive Técnico — Axon & MGX

**Data do documento:** 2026-06-16
**Autor:** análise técnica consolidada a partir das fontes do Google Drive de Gustavo Pratti de Barros
**Escopo:** dois projetos distintos — **Axon** (governança contextual de automação) e **MGX** (motor integrado MGE+CEX+MEX com humano no loop).
**Princípio editorial:** honestidade acima de hype. Onde algo é especificação e não implementação, está marcado como tal. Onde a fonte não cobre um ponto, está marcado como **NÃO ENCONTRADO**.

> Nota de proveniência logo de saída: todas as fontes carregam data **2026-03-29** (briefings/conceitos) e conversas-base de mar/2026. Há também uma demanda de **2026-05-03** registrando que um fragmento de memória sobre MGX foi marcado como **incorreto** pelo próprio Gustavo (ver seção Proveniência). Nada aqui foi inventado para preencher lacunas.

---

# PARTE I — AXON

## 1. Resumo

Axon é um **sistema de governança contextual para automação**: um intermediário inteligente entre estados humanos e ações digitais. Em vez de regras rígidas do tipo "se X então Y" (paradigma IFTTT/Shortcuts), o Axon adiciona uma **camada de deliberação** — antes de executar uma ação automatizada, ele avalia se a ação é *prudente* dado o contexto, o estado do usuário e o risco/reversibilidade da ação.

Estado real: **conceitual puro**. Existe blueprint em pseudocódigo, crítica multi-especialista (7 domínios) e roadmap de 12 meses. **Implementação: nenhuma. Validação com usuários: não iniciada.** É descrito pela própria fonte como o projeto "mais ambicioso comercialmente e com mais riscos".

## 2. Tese / problema

A automação tradicional é binária e cega ao contexto: dispara a ação quando a condição é satisfeita, sem perguntar se *agora* é o momento certo nem se o estado da pessoa torna a ação inadequada. O problema que o Axon ataca: **automações úteis em média podem ser nocivas em momentos específicos** (sobrecarga sensorial, fadiga, estado emocional ruim, contexto de risco).

A tese central é introduzir um "guardião prudente" que decide não só *se* a regra dispara, mas *se é prudente disparar*, avaliando três perguntas (verbatim da fonte):
- o contexto atual justifica essa ação?
- o nível de risco é aceitável dado o estado do usuário?
- a ação é reversível?

## 3. Arquitetura

A fonte descreve o Axon conceitualmente, não em diagrama de componentes. O que está documentado:

- **Posição arquitetural:** intermediário ("guardião prudente") *entre* o usuário e seus dispositivos/apps. Toda ação automatizada passa por ele antes de executar.
- **Camada de deliberação:** o diferencial sobre IFTTT/Shortcuts é justamente essa camada — não substitui o motor de regras, o *supervisiona*.
- **Entradas de contexto declaradas:** contexto atual, estado emocional, hora do dia, padrões de uso, nível de risco da ação.
- **Critérios de decisão:** justificativa contextual, aceitabilidade de risco condicionada ao estado do usuário, reversibilidade da ação.

**NÃO ENCONTRADO:** especificação de módulos internos, modelo de dados, pipeline de inferência, como o "estado emocional" é estimado (sensor? auto-relato? inferência?), nem onde o processamento roda (local vs nuvem). Dado o nicho (biometria de menores), a rota de processamento é uma decisão de arquitetura crítica **ainda em aberto na fonte**.

## 4. Especificação

O nível de especificação existente é **blueprint conceitual em pseudocódigo** (descrito como "Completo" na tabela de estado), mas o conteúdo do pseudocódigo **não consta** nas fontes lidas — apenas a menção de que ele existe.

O que está especificado em texto:
- **Modelo de avaliação por ação:** cada ação automatizada é submetida ao tripé contexto/risco/reversibilidade antes de executar.
- **Diferenciação funcional vs automação clássica:** decisão sobre "se é prudente" e não apenas "se a condição é verdadeira".

**NÃO ENCONTRADO:** schema de dados, contratos de API, formato dos "padrões de uso", política de fallback quando o Axon está indisponível, thresholds de risco.

## 5. Decisões de design

Decisões explícitas registradas:
- **Go-to-market por nicho** em vez de horizontal: foco em **famílias com crianças neurodivergentes**. Justificativas declaradas:
  - necessidade real de governança contextual (rotinas adaptativas, prevenção de sobrecarga sensorial);
  - *willingness to pay* alto (pais investem pesadamente em ferramentas que ajudam);
  - barreira regulatória menor que saúde adulta;
  - comunidade ativa e vocal (boca a boca).
- **Deliberação como camada separada** da automação (não reescrever IFTTT, e sim supervisioná-lo).
- **Submeter o projeto a crítica multi-especialista antes de codar** (7 domínios: arquitetura de sistemas, ML engineering, legal/regulatório, UX, HCI, produto, segurança). Gustavo engajou substantivamente com todas.

## 6. Estado de implementação (HONESTO)

| Item | Status (verbatim da fonte) |
|---|---|
| Blueprint conceitual (pseudocódigo) | Completo |
| Crítica multi-especialista | Completa |
| Roadmap 12 meses | Definido |
| Implementação | **NENHUMA** |
| Validação com usuários | **NÃO INICIADA** |

Tradução honesta: **nada foi construído.** Não há código, protótipo, nem teste com usuário. Tudo o que existe é documental e analítico. A distância até um MVP testável é descrita pela própria fonte como "grande" e o escopo realista como "multi-ano".

## 7. Ética / regulatório

Este é o eixo mais sensível do Axon, e a fonte é explícita sobre ele. Riscos regulatórios declarados, cada um tratado como "campo minado regulatório independente":

- **Biometria → LGPD/GDPR:** implicações "pesadas". Se o Axon inferir estado emocional/sensorial a partir de dados biométricos, cai sob regimes de dado pessoal sensível.
- **Classificação como dispositivo médico:** acionada se o produto fizer *claims* de saúde. Isso muda o regime regulatório inteiro (ANVISA/FDA/CE-MDR).
- **Monitoramento de menores:** legislação específica por país, mais restritiva. O nicho escolhido (crianças neurodivergentes) coloca o produto exatamente nessa categoria desde o dia 1.

Observação crítica honesta: o nicho que foi escolhido por *reduzir* barreira regulatória relativa à saúde adulta **simultaneamente** ativa o vetor "monitoramento de menores" e aproxima do vetor "dispositivo médico" (sobrecarga sensorial é território clínico). É um trade-off regulatório real, não resolvido na fonte.

## 8. Estado da arte + diferencial

- **Baseline de mercado:** automação por regras (IFTTT, Apple Shortcuts, Tasker, Home Assistant). Todas são "se X então Y" sem deliberação contextual de prudência.
- **Diferencial declarado do Axon:** a camada de deliberação — avaliar prudência, risco condicionado ao estado e reversibilidade, em vez de só avaliar a condição-gatilho.

**NÃO ENCONTRADO:** benchmark contra concorrentes nominais no espaço de wellbeing/neurodivergência, nem citação a produtos específicos do nicho. O diferencial está afirmado conceitualmente, não validado contra alternativas reais.

## 9. Limitações / riscos

- **Risco de execução:** zero implementação; o salto conceito→MVP é grande e multi-ano.
- **Risco regulatório triplo:** biometria + menores + possível dispositivo médico, simultâneos.
- **Risco de validação:** nenhuma validação com usuário; a premissa de "willingness to pay alto" é hipótese não testada.
- **Risco de inferência de estado:** estimar "estado emocional" de forma confiável é, por si, um problema de ML aberto e eticamente delicado em menores. A fonte lista ML engineering entre os críticos, mas não traz a solução.
- **Risco de priorização:** a própria fonte recomenda **não priorizar** o Axon até o Phronesis-Bench estar submetido, e mesmo depois ponderar se projetos mais pragmáticos não dariam retorno mais rápido.

## 10. Roadmap

A fonte afirma um **roadmap de 12 meses "Definido"**, mas **o detalhamento das fases/marcos não consta** nos arquivos lidos. **NÃO ENCONTRADO:** milestones, ordem de execução, critérios de gate.

Diretriz estratégica explícita (verbatim do espírito da fonte): despriorizar até o Phronesis-Bench ser submetido; reavaliar contra alternativas pragmáticas (MGE como ferramenta, consultoria multi-agente) que dariam retorno mais rápido.

---

# PARTE II — MGX

## 1. Resumo

MGX (na fonte: *"Motor de Geração e Execução Integrada"*) é um **sistema de orquestração cognitiva** que integra três motores de IA — **MGE** (geração), **CEX** (validação/deliberação) e **MEX** (execução) — com uma **camada de deliberação humana ativa entre cada estágio**. O princípio não é pipeline industrial linear; é um **grafo de decisão com loops humanos**, onde a informação circula, refina, volta, recombina e só avança quando o humano decide.

Estado real: **misto e honesto** — MGE e CEX existem como artefatos funcionais (HTML standalone), MEX é só conceito, e a **camada de orquestração MGX em si é documento conceitual, pré-implementação**.

## 2. Tese / problema

O mercado de multi-agentes (CrewAI, AutoGen, Agno) otimiza para **tirar o humano do loop** — autonomia máxima. A tese do MGX é o oposto: em problemas de alto valor e ambíguos (ideação→viabilidade→execução), a melhor arquitetura **coloca o humano no centro** como co-decisor, dando-lhe ferramentas para navegar o espaço de soluções: pausar, redirecionar, combinar resultados de diferentes rodadas e voltar a estágios anteriores sem perder nada.

Problema técnico subjacente que a arquitetura resolve: **preservar contexto e rastreabilidade** ao longo de um processo não-linear de muitas rodadas de LLM, sem estourar a janela de contexto nem perder o histórico de decisões.

## 3. Arquitetura

### 3.1 Os três motores

- **MGE — Motor de Geração Estruturada.** Gera rupturas criativas via inversão de dogmas, cruzamento de domínios e "membrana de novidade" (filtro anticlichê). É o "acelerador" / a "centelha".
- **CEX — Comitê de Especialistas Universais.** Delibera sobre viabilidade via banca dinâmica, debate adversarial entre pares (cross-examination) e auditoria determinística. É o "freio e o leme" / a "blindagem".
- **MEX — Motor de Execução.** Materializa o veredito do CEX em artefatos executáveis (código, documentação, backlog, modelagem financeira, plano de riscos). É a "Oficina" / "The Build Box". **Conceitual, não implementado.**

### 3.2 Grafo de decisão (fases 0→3.5, bidirecionais)

Não é pipeline; é grafo com loops humanos. Fases (verbatim):

- **Fase 0** — Exploração livre (conversa sem motor ativo)
- **Fase 1** — Geração (MGE roda)
- **Fase 1.5** — Deliberação pós-MGE (humano discute resultados, combina, descarta)
- **Fase 2** — Validação (CEX roda com contexto total)
- **Fase 2.5** — Deliberação pós-CEX (pode voltar ao MGE ou re-rodar CEX)
- **Fase 3** — Execução (MEX roda)
- **Fase 3.5** — Deliberação pós-MEX (pode voltar a qualquer fase)

Propriedades-chave: **transições não-lineares** e **nenhum snapshot é destruído ao voltar**. As fases ".5" são os pontos de humano-no-loop — são elas que definem o MGX.

### 3.3 Arquitetura de memória (3 camadas)

- **Camada 1 — Estado vivo:** a conversa atual na janela de contexto. ~15-20k tokens.
- **Camada 2 — Snapshots cristalizados:** outputs completos de cada rodada de motor, salvos com ID único (`MGE-001`, `CEX-002`, etc), em storage externo, consultáveis sob demanda.
- **Camada 3 — Diário de decisões:** log compacto de cada decisão humana, sempre presente em contexto, raramente acima de 2-3k tokens. Formato:
  ```
  [DEC-001] timestamp | fase | decisão/motivo
  ```

A lógica é separar o que precisa estar *sempre* no contexto (diário, leve) do que pode ser *recuperado sob demanda* (snapshots, pesados).

### 3.4 Compilador de contexto

Módulo que monta o prompt ideal antes de cada rodada de motor, em três passos:
1. **Coleta:** lê o diário + identifica snapshots relevantes.
2. **Extração seletiva:** puxa só os trechos necessários dos snapshots.
3. **Montagem:** combina tudo num prompt coeso.

Para sessões longas, pode usar **Haiku como resumidor prévio** (etapa de compressão antes da montagem final).

### 3.5 mgxState (objeto central)

Objeto de estado que carrega toda a sessão (verbatim, JS):
```javascript
mgxState = {
  session_id, created_at, current_phase,
  decisions: [...],
  snapshots: { mge: [...], cex: [...], mex: [...] },
  executive_summary: "...",
  conversation_digest: "..."
}
```

## 4. Especificação

### 4.1 MGE v2.0 (implementado)
- **Formato:** HTML standalone (~2070 linhas), tema escuro, **funcional**.
- **Arquivo:** `MGE_ultimo_codigo_chat.txt` (v2.0, não v2.1).
- **Pipeline:** 10 agentes criando portfólio de conceitos com avaliação independente.
- **Abas (UI):** Portfólio, Combinações, Processo, JSON Bruto, Glossário, Explorar.
- **v2.1** (micro-validadores, split do Transgressor, bracket-balancing parser, tema claro) foi implementada num chat anterior do Claude, **mas o HTML não foi recuperado** — pode estar salvo localmente. O artefato canônico recuperável é a v2.0.

### 4.2 CEP v3.9 → CEX v1.1 (evolução implementada)
- **CEP v3.9:** workflow n8n (JSON, ~1300 linhas, 21 nós). Base original. Especialistas fixos + dinâmicos, revisor crítico, re-acionamento, motor de regras com pesos fixos, auditor interno determinístico. Arquivo: `CEP_v3_9_final__1_.json`.
- **CEX v1.1:** HTML standalone (~920 linhas), **funcional com bugs conhecidos**. Arquivo: `CEX_v1.1.html`. Maestro dinâmico, cross-examination, dois modos, auditor interno, 6 abas.

Mudanças CEP→CEX (duas transformações simultâneas: plataforma e arquitetura):

*Plataforma:* n8n → HTML/JS standalone; HTTP Request nodes → `fetch()` com `Promise.race` timeout; `getWorkflowStaticData` → objeto JS em memória; sem UI → interface visual com 6 abas.

*Arquitetura:*
- **Analisador de Domínio → Maestro de Ontologia (Sonnet):** CEP sugeria extras além de 5 especialistas fixos; CEX gera a banca inteira do zero, sem fixos, com critério de ouro/viabilidade, pesos dinâmicos e conflitos esperados.
- **Novo: Auditor de Bancada (Haiku):** revisa composição da banca, procura pontos cegos, pode sugerir adições.
- **Revisor Crítico → Cross-Examination:** de revisor único para debate direto entre pares, distribuição circular (A→B, B→C, C→D, D→A). Tipologia de problemas do CEP preservada.
- **Motor de Regras fixo → Adaptativo:** pesos hardcoded (legal=3.0, segurança=2.5, ...) → pesos definidos pelo Maestro por caso. Regras de bloqueio e thresholds preservados.
- **Compositor Prudencial → Dialético:** de síntese por resumo para arbitragem por resistência de argumento; quatro categorias de veredito.
- **Novo: Modo Avaliação de Conceito:** além do modo Deliberação (risco), um modo Avaliação (viabilidade), com calibrações, vereditos e prompts distintos por modo.

*Preservado sem mudança:* Kai, Ambiguidade Check, Coverage Mapper, Convergence Examiner, DeltaU, Auditor Interno (7 verificações, score 0-1), Product Formatter.

*Modelos por agente no CEX:* Maestro = Sonnet; Compositor = Sonnet; análises de dimensões que exigem nuance = Sonnet; resto = Haiku.

*Custo:* CEP ~12-18 chamadas; CEX ~18-20 (com limite de 5 especialistas na versão demo).

*Decisões técnicas do CEX:* HTML standalone arquivo único; API direto do browser (`anthropic-dangerous-direct-browser-access`); `parseJSON` com strip de markdown fences e reparo de JSON truncado; retry 3x com delay progressivo (5s/10s/15s); timeout de 30s por chamada; delay de 2s entre chamadas sequenciais; limite de 5 especialistas na versão demo.

### 4.3 MEX (conceitual)
Origem: conversas com Gemini (`MEX_gemini.txt`). Na fonte de conceito (mgx-001) é "Motor de Execução"; na conversa-origem é proposto como **"MEX (Motor de Execução e Artefatos)" / "A Oficina" / "The Build Box"**. Componentes conceituais:
- **Arquiteto de Implementação (Maestro do MEX):** assume a ideia aprovada como certa e decompõe "vontade" em "tarefas"; gestão de dependências (comprar/codar/contratar); cronograma sintético (Gantt ou backlog de sprints estilo Jira/Trello).
- **Squads sintéticas de entrega:** convoca *Executores* (não "sabedores" como o CEX) — Squad Digital (Fullstack + UX + Prompt Engineer), Squad de Produto Físico (Eng. Mecânico + Supply Chain + Designer), Squad de Negócios (Growth + Jurídico Contratual + CFO/modelagem). Nível: "saber-fazer" / executivo-operacional sênior.
- **Gerador de Ativos Mínimos:** entregar arquivos, não texto — código real (repo GitHub com boilerplate), protótipo visual (prompts para geradores de imagem, SVG/HTML wireframes), documentação executiva (plano de negócios PDF, projeção CSV/XLSX, pitch deck PPTX).
- **Modo de Iteração com o Real (proposta):** "Simulador de Colisão de Mercado" — gêmeo digital que simula 1 ano de mercado e gera relatório de resiliência. **NÃO implementado, é proposta dentro da conversa-origem.**

### 4.4 MGX (orquestração)
Documento conceitual v1.0. **Pré-implementação.** Define a camada que conecta MGE+CEX+MEX com deliberação humana entre fases, diário de decisões, compilador de contexto e navegação não-linear (seções 3.2-3.5).

## 5. Decisões de design

- **Humano no centro, por desígnio** (anti-tendência do mercado): as fases ".5" são parte da arquitetura, não um afterthought.
- **Imutabilidade de snapshots:** voltar nunca destrói output anterior — permite recombinar livremente.
- **Separação memória leve/pesada:** diário sempre em contexto; snapshots sob demanda — controla custo e janela.
- **Standalone HTML primeiro, framework depois:** MGE e CEX nasceram como HTML de arquivo único, chamando a API Anthropic direto do browser. Decisão pragmática de prototipagem rápida.
- **Roteamento de modelo por papel:** Sonnet onde há nuance (Maestro, Compositor), Haiku no resto e como resumidor — otimização custo/qualidade explícita.
- **Banca 100% dinâmica no CEX:** abandono dos especialistas fixos do CEP em favor de geração total pelo Maestro.
- **Agno como base candidata de produção:** framework Python open-source mapeado por oferecer memória, knowledge stores, teams, workflows e human-in-the-loop nativos. **Decisão de uso pendente** — é candidato, não escolhido.

## 6. Estado de implementação (HONESTO)

| Artefato | Formato | Status |
|---|---|---|
| **MGE v2.0** | HTML standalone ~2070 linhas | **Funcional** (v2.1 melhorada existe mas HTML não recuperado) |
| **CEP v3.9** | n8n JSON, 21 nós | Funcional, base original, substituído pelo CEX |
| **CEX v1.1** | HTML standalone ~920 linhas | **Funcional com bugs conhecidos** |
| **MEX** | só conceito (Gemini) | **NÃO implementado** |
| **MGX (orquestração)** | doc conceitual v1.0 | **Pré-implementação** |

**Bugs conhecidos no CEX v1.1:**
1. *Internal server error* em chamadas Sonnet após muitas requisições sequenciais — mitigado com delay de 2s + retry 3x, mas ainda pode ocorrer.
2. *JSON truncado* em respostas longas — mitigado com `parseJSON` que repara brackets abertos.
3. *Timeout no Kai* — reduzido pra 30s, mas pode falhar consistentemente se a API estiver sobrecarregada.

**Leitura honesta:** dos três motores, **dois existem e rodam** (MGE, CEX) e **um não** (MEX). A peça que dá nome ao projeto — a orquestração MGX — **ainda não foi construída**; é exatamente o que liga tudo e é o que falta. Logo, "MGX" hoje é mais um *conceito de integração validado em partes* do que um sistema integrado.

## 7. Ética / regulatório

A fonte **não detalha** um regime regulatório para o MGX como faz para o Axon — é uma ferramenta de produtividade cognitiva, não um produto que coleta biometria de menores. **NÃO ENCONTRADO:** análise LGPD/GDPR específica do MGX.

Pontos éticos implícitos relevantes:
- **Chave de API direto no browser** (`anthropic-dangerous-direct-browser-access`): aceitável para protótipo pessoal, **inadequado para produto distribuído** (exposição de credencial). É dívida a resolver na migração para backend (Agno).
- **Humano-no-loop como salvaguarda:** o desígnio de manter o humano como co-decisor é, em si, uma postura ética (responsabilidade e supervisão) alinhada às boas práticas de agentes.

## 8. Estado da arte + diferencial

- **Concorrentes nominais:** CrewAI, AutoGen, Agno — frameworks multi-agente que otimizam autonomia (humano fora do loop).
- **Diferencial do MGX:** inverte a premissa — humano no centro, com ferramentas de navegação do espaço de soluções (combinar, descartar, voltar) e memória/rastreabilidade explícitas (diário de decisões + snapshots imutáveis).
- **Posição honesta:** o diferencial é de *postura de design*, não de tecnologia inédita. Os mesmos frameworks concorrentes (incl. Agno) suportam human-in-the-loop; o que o MGX propõe de original é a *centralidade* do humano e o grafo não-linear com memória em 3 camadas como primeira-classe.

## 9. Limitações / riscos

- **A peça central não existe:** sem a orquestração MGX construída, o "motor integrado" é integração no papel.
- **MEX inexistente:** a Fase 3 não tem motor real; toda a metade "execução" do sistema é conceitual.
- **Estabilidade do CEX:** três classes de bug ativas (erros de servidor, JSON truncado, timeout) só mitigadas, não eliminadas.
- **Dívida arquitetural do protótipo:** HTML standalone + API no browser não escala para produto; migração para Agno é trabalho não-trivial e ainda *pendente de decisão*.
- **Custo/latência:** ~18-20 chamadas por rodada de CEX, com delays e retries, tornam ciclos completos lentos e caros; o limite de 5 especialistas é uma concessão da versão demo.
- **Risco de memória/proveniência:** a demanda de 2026-05-03 mostra que um curador automático já gerou um fragmento **incorreto** sobre o MGX ("metodologia aplicada em projetos passados") — sinal de que descrições do projeto derivam fácil para imprecisão se não ancoradas nas fontes primárias.

## 10. Roadmap

Próximos passos, em ordem de prioridade (verbatim da fonte mgx-004):
1. ~~Construir CEX v1.0~~ ✅ (v1.1 entregue)
2. Estabilizar CEX v1.1 (resolver bugs de API/timeout)
3. Construir MEX v1.0 como HTML standalone
4. Construir camada de orquestração MGX
5. Integrar os três motores
6. Avaliar migração pra Agno (framework Python) como backend de produção

**Decisão pendente declarada:** Phronesis-Bench (deadline 16/abril, hackathon Kaggle/DeepMind) vs MGX (sem deadline). Sessões separadas em uso para cada projeto.

---

# APÊNDICES (comuns)

## Glossário

- **Axon** — sistema conceitual de governança contextual de automação ("guardião prudente" entre usuário e dispositivos).
- **MGX** — "Motor de Geração e Execução Integrada"; camada de orquestração de MGE+CEX+MEX com humano no loop. Pré-implementação.
- **MGE** — Motor de Geração Estruturada; gera rupturas criativas (inversão de dogmas, cruzamento de domínios, membrana de novidade). HTML v2.0 funcional.
- **CEP** — Comitê de Especialistas Prudenciais; versão original em n8n (v3.9, 21 nós). Base do CEX.
- **CEX** — Comitê de Especialistas Universais; evolução do CEP em HTML standalone (v1.1). Banca dinâmica, cross-examination, dois modos.
- **MEX** — Motor de Execução (na origem: "Motor de Execução e Artefatos" / "A Oficina" / "The Build Box"); materializa veredito em artefatos. Conceitual.
- **Kai** — agente Guardião do Escopo; só libera o processo se houver uma decisão real ("faca no pescoço"); bloqueia perguntas genéricas. Preservado do CEP no CEX.
- **Maestro de Ontologia** — agente (Sonnet) que monta a banca de especialistas do zero no CEX, com pesos dinâmicos.
- **Auditor de Bancada** — agente (Haiku) novo no CEX; revisa a composição da banca e procura pontos cegos.
- **Cross-Examination** — debate adversarial circular entre especialistas pares (A→B→C→D→A), substitui o revisor único do CEP.
- **Auditor Interno** — verificação determinística (7 checagens, score 0-1) preservada do CEP no CEX.
- **DeltaU / Convergence Examiner / Coverage Mapper / Ambiguidade Check** — componentes do CEP preservados no CEX.
- **Compilador de contexto** — módulo do MGX que monta o prompt ideal por rodada (coleta → extração seletiva → montagem).
- **mgxState** — objeto de estado central da sessão MGX (session_id, fase, decisões, snapshots, sumário, digest).
- **Diário de decisões** — Camada 3 de memória; log compacto sempre em contexto (`[DEC-001] timestamp | fase | decisão/motivo`).
- **Snapshots cristalizados** — Camada 2; outputs imutáveis com ID único em storage externo.
- **Agno** — framework Python open-source candidato a backend de produção (memória, teams, workflows, human-in-the-loop nativos).
- **Membrana de novidade** — filtro anticlichê do MGE.

## Proveniência

| Fonte | fileId | Tipo | Data | Uso neste doc |
|---|---|---|---|---|
| `axon-00-briefing.md` | 1v-B-nas6gKTv3hbd3vUrlZhWUubuYdHI | briefing | 2026-03-29 | Toda a Parte I (Axon) |
| `mgx-001-conceito-geral.md` | 1DfL-v6NHR735gl6b_O7cgKPv9TsJX1PU | raciocínio/conceito | 2026-03-29 | Arquitetura, memória, compilador, mgxState, diferencial, Agno |
| `mgx-002-cep-para-cex-evolucao.md` | 1-TT9CsVmggRE2T8gQdHk5d63GzISazjg | decisões/raciocínio | 2026-03-29 | Especificação CEP→CEX, modelos, custo, decisões técnicas |
| `mgx-003-analise-identidade-llms.md` | 1mUjGoY2r7Wtk5ZtjL1jt4hVqSsO8ApHb | resultado/análise | 2026-03-29 | Contexto de origem (assinaturas cognitivas dos 3 LLMs) |
| `mgx-004-estado-do-projeto.md` | 1vHo2D7pqdnkxEbBgtrOxqcjxnxqjCMGJ | estado-do-projeto | 2026-03-29 | Inventário de artefatos, bugs, roadmap, decisão pendente |
| `MEX gemini.txt` | 1bXC3W0EB2ue5i8Yd1qoIs1AqxXgzpXEa | conversa Gemini | mar/2026 | Detalhe conceitual do MEX (seção 4.3) |
| `2026-05-03...delete-fragmento-mgx-errado.md` | 1yTFhhwBd-... (e duplicatas) | demanda | 2026-05-03 | Nota de proveniência (fragmento MGX incorreto) |

Notas de proveniência:
- Os arquivos foram lidos diretamente via Google Drive MCP. Os `.md` de origem usam escape de markdown (`\#`, `\*`), normalizado nas citações abaixo.
- Há **três duplicatas** do mesmo documento de demanda de delete (fileIds 1yTFhhwBd-tVrJBXhvUczaLyfv7FKgiy, 1GaHU12e6kifBwZb_4iTDAXvF4Clh9FOW, 1viNLHtvqXmL1wCumDT2FdH_GwEFQWsM6) em estados diferentes (pendente/bloqueado).
- **NÃO ENCONTRADO:** documentos de spec técnica do Axon além do briefing v00; conteúdo do pseudocódigo do Axon; detalhamento das fases do roadmap de 12 meses do Axon; HTML do MGE v2.1; análise regulatória do MGX.

## Citações VERBATIM

**Axon — conceito central (axon-00-briefing.md):**
> "O Axon age como um 'guardião prudente' entre o usuário e seus dispositivos/apps. Antes de executar qualquer ação automatizada, avalia: o contexto atual justifica essa ação? O nível de risco é aceitável dado o estado do usuário? A ação é reversível?"

**Axon — diferencial (axon-00-briefing.md):**
> "Isso é diferente de automação tradicional (IFTTT, Shortcuts) porque inclui uma camada de deliberação — não só 'se' executar, mas 'se é prudente' executar."

**Axon — avaliação honesta (axon-00-briefing.md):**
> "Projeto mais ambicioso comercialmente e com mais riscos. Escopo realista é multi-ano. Conceito forte, mas distância até MVP testável é grande. Recomendação: não priorizar até Phronesis-Bench estar submetido..."

**MGX — princípio arquitetural (mgx-001-conceito-geral.md):**
> "Grafo de decisão com loops humanos, não pipeline industrial. A informação circula, é refinada, volta, recombina e só avança quando o humano decide."

**MGX — diferencial competitivo (mgx-001-conceito-geral.md):**
> "O mercado de multi-agentes (CrewAI, AutoGen, Agno) foca em tirar o humano do loop. O MGX faz o oposto: coloca o humano no centro com ferramentas pra navegar o espaço de soluções."

**MGX — diário de decisões (mgx-001-conceito-geral.md):**
> "[DEC-001] timestamp | fase | decisão/motivo"

**MGX — não-linearidade (mgx-001-conceito-geral.md):**
> "Transições são não-lineares. Nenhum snapshot é destruído ao voltar."

**MEX — origem (MEX gemini.txt):**
> "Minha sugestão é a criação de um módulo chamado MEX (Motor de Execução e Artefatos) ou simplesmente 'A Oficina'. Ele funcionaria a posteriori ao veredito do CEX."

**MEX — nível de especialidade (MEX gemini.txt):**
> "Enquanto o CEX convoca 'Doutores e Cientistas' (especialistas em Saber), o MEX convoca 'Engenheiros e Mestres de Obra' (especialistas em Fazer)."

**MGX — estado do MEX (mgx-004-estado-do-projeto.md):**
> "MEX (Motor de Execução) — Formato: apenas conceito arquitetural — Status: não implementado"

**MGX — fragmento incorreto de memória (demanda 2026-05-03):**
> "Conteúdo: 'A metodologia MGX foi aplicada em projetos passados e se tornou referência para as decisões e desenvolvimentos atuais.' Problema: Conteúdo vago e impreciso. MGX (MGE + CEX + MEX) é um pipeline ativo em desenvolvimento, não 'metodologia aplicada em projetos passados'. Gustavo confirmou que está errado."
