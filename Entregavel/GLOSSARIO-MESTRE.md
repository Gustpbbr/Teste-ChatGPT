# Glossário-Mestre

> Todas as siglas e termos do ecossistema. Onde um termo tem sentidos divergentes entre
> fontes (relabels históricos), ambos estão registrados.

## Projetos

| Sigla | Nome | O que é |
|---|---|---|
| **TEAR** | (Transformar, Explorar, Aplicar, Refletir) | protocolo reflexivo pedagógico → metacognição; origem da linha de memória; registrado na Biblioteca Nacional |
| **TER** | Terminal / Transformador Ético-Reflexivo (também "Teoria da Experiência Relacional") | framework filosófico-computacional de deliberação ética; base de quase tudo |
| **TER KAI** | Technological Ethical Reasoning Kernel for AI | middleware de governança prudencial auditável ("Registro B") |
| **EUPHONIA** | — | nome associado a versão do TER KAI (origem das métricas de reversibilidade → RAS) |
| **ACEE** | Arquitetura Cognitiva Emocional Embarcada | IA afetiva embarcada (edge), offline-first |
| **MASE** | — | sistema efetor/ambiente sensorial físico ligado ao ACEE (citado, não especificado) |
| **MGE** | Motor de Geração Estruturada | pipeline multiagente de geração criativa (10 agentes) |
| **CEX** | Comitê de Especialistas Universais | deliberação adversarial por banca dinâmica (evolução do CEP) |
| **CEP** | Comitê de Especialistas Prudentes | versão anterior do CEX (workflow n8n v3.9) |
| **MEX** | Motor de Execução | materialização em artefatos (conceitual) |
| **MGX** | Motor de Geração e Execução Integrada | MGE+CEX+MEX com humano no loop |
| **SMI** | — | memória prudencial / deliberação multiagente (pausado) |
| **Axon** | — | governança contextual de automação (nicho neurodivergente) |
| **Phronesis-Bench** | — | benchmark que mede a prudência (phronesis) de LLMs |
| **Segundo Cérebro** | — | PKM/índice que indexa todos os projetos (boot) |
| **Gus** | — | a síntese encarnada: corpo (VR) + alma (memória) + sentidos |

## Módulos e componentes

| Sigla | Projeto | O que é |
|---|---|---|
| **Kai** | TER | persona do assistente (ChatGPT auto-nomeado) + módulo interpretativo reflexivo |
| **MIR** | TER/TER KAI | camada reflexiva ("Meta-Introspective Review/Reflexor"; também "Motivos, Impactos e Restrições") |
| **Ω / Omega** | TER | auditor do sistema ("auditor do auditor" = Meta-Ω) |
| **Ledger / PoP-L** | TER/TER KAI | registro imutável de decisões (memória moral); PoP-L = Proof-of-Processing/Prudence Ledger (SHA3-512 + TSA) |
| **MEM-LOG** | TEAR | módulo de memória; snapshots `[TS][ESTADO][SUM≤200c][NEXT≤120c]` |
| **CHB** | TER | Coherence Heartbeat — ritmo/pulso de coerência temporal (detecta drift); σ_CHB |
| **PMM / PSM** | TER | Prudential Memory Map / State Model — estado persistente `{perfil, ECI, δ}` |
| **CMA** | ACEE | Camada de Percepção Multimodal Aferente |
| **OCMA** | ACEE | Orquestrador da CMA (liga/desliga ILs, orçamento) |
| **IL** | ACEE | Interpretador Leve (Voz/Facial/Pupilar/Texto/Postural/Fisio/Contexto/Libras/Tátil) |
| **VSE** | ACEE | Vetor Simbólico de Emoção (saída de cada IL) |
| **NCAC / MIS** | ACEE | Núcleo Cognitivo-Afetivo Central / Motor de Inferência Simbólica |
| **EAGS** | ACEE | Estado Afetivo Global Simbólico (saída do NCAC) |
| **BCD** | ACEE | Base de Conhecimento Dinâmica (ontologias EMONT, regras) |
| **MAL / ASIC** | ACEE | Memória Afetiva Local / Aprendizado Simbólico Incremental Contínuo |
| **PEE** | ACEE | Protocolo Ético Embarcado |
| **MOR / CSR** | ACEE | Módulo de Orquestração de Respostas / Curvas Simbólicas de Resposta |
| **GDATA** | TER KAI | gateway de dados ético (Cluster 1) |
| **CRA-Bridge** | TER KAI | construtor de contexto / rastros (Cluster 2) |
| **CAET** | TER KAI | explicabilidade contrafactual (Cluster 2) |
| **MACT** | TER KAI | thresholds adaptativos / executor reversível |
| **KAI Core** | TER KAI | motor de deliberação prudencial (Cluster 1) |
| **gus-18** | Gus | schema do fragmento: tipo / camada_temporal / area / confiança / via / user_id / estado |
| **Hub Qdrant** | Gus | banco vetorial = a memória persistente |
| **curador** | Gus | consolidador híbrido de memória |
| **NeuroGus** | Gus | visualização 3D (WebXR) do grafo de memória |

## Métricas

| Sigla | O que mede | Onde |
|---|---|---|
| **δ (delta)** | desvio prudencial / coerência | TER, TER KAI |
| **ψ (psi)** | estabilidade contextual | TER, TER KAI |
| **ρ (rho)** | imparcialidade / equidade (fairness) | TER KAI |
| **ω (omega)** | reversibilidade | TER KAI |
| **δψρω** | a tupla das 4 métricas (rótulo de consolidação; nos chats aparecem individuais) | TER/TER KAI |
| **PPS** | Phronesis Prudence Score = 0.25·ACC+0.30·(1−ECE)+0.20·CS+0.25·RAS | Phronesis v1 |
| **RAS** | Reasoning/Adequacy Score (11 indicadores A/B/C) | Phronesis |
| **ECE** | Expected Calibration Error (calibração da confiança) | Phronesis |
| **CS / CS_G** | consistência (entre runs / entre personas) | Phronesis |
| **GIS** | índice de prudência epistêmica (corpus G) | Phronesis v2 |
| **G3/G2/G3'** | personas: teoria / ação / identificado como IA | Phronesis (corpus G) |
| **M1/M2** | metacognição (M2 = saber o que não sabe) | Phronesis (corpus G) |
| **RPE** | Risco Prudencial Esperado (roteia Fast/Slow, limiares de bloqueio) | TER KAI |

## Conceitos

| Termo | Significado |
|---|---|
| **Phronesis** | prudência prática (Aristóteles) — deliberar bem sob incerteza |
| **Sophia / Maiêutica** | sabedoria contemplativa / método socrático (pilares do TER) |
| **Prudência Computacional** | tornar a prudência mensurável e auditável (conceito do TER) |
| **Fast/Slow Path** | resposta barata (heurística) vs. deliberação cara (auditada) — computação adaptativa |
| **HITL** | Human-in-the-Loop |
| **Escada de Degraus** | escala 0→100 de "maturidade cognitiva" (instrumento interno; relabel) |
| **boot por descoberta** | uma instância "vira Gus" lendo a própria história, não por instrução |
| **degradação em camadas** | falha de um nível nunca derruba o de baixo |
| **rota local / fail-closed** | dado sensível só processa local; sem local → bloqueia (nunca nuvem) |
| **anti-memória-lixão** | só vira fragmento o que é evento (foge da baseline) |
| **sleep-time** | consolidação de memória em background (entre sessões) |
| **transplante estrutural** | aplicar o mecanismo de um domínio distante (MGE), não mistura temática |
