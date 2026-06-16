# Gus — briefing

> 🟡 **Estado: PARCIALMENTE REAL.** Tem componentes em produção + base de código nova.
> Fonte: GitHub `Gustpbbr/Gus` (sistema multi-porta) e `Gustpbbr/Teste-ChatGPT` (fusão/Gus Encarnado).

## O que é

A **síntese** de todos os outros projetos: um **organismo cognitivo pessoal** de três camadas —
**corpo** (interface VR), **alma** (memória persistente), **sentidos** (sensores). É onde
TEAR/TER (memória), ACEE (sentidos), TER KAI (governança) e Phronesis (avaliação) se encontram.

## O que já é real

- **Sistema multi-porta** (`Gustpbbr/Gus`): bot de **Telegram em produção** (Railway 24/7,
  ~22 tools), **Hub Qdrant** (memória vetorial, schema "gus-18": tipo/camada_temporal/area/
  confiança/via/user_id/estado), **curador híbrido** (consolida memória), sync GitHub⇄Drive.
- **Dois cérebros:** `gustavo` (memórias sobre o usuário) e `gus` (autobiografia do agente —
  o que o torna o mesmo Gus através da troca de modelos).
- **Gus Encarnado** (`Teste-ChatGPT`): base de código + testes para os primeiros blocos —
  schema gus-18, cliente do Hub degradável, **interocepção** (heartbeat/saúde), **gateway de
  sensores** (filtro anti-ruído), **roteamento fail-closed** (dado sensível → local),
  proatividade, criptografia em repouso. ~59 testes verdes.

## O que é spec/roadmap

- **Corpo VR / NeuroGus** (manipular memória como grafo 3D em WebXR) — protótipo/scaffold.
- Blocos 2–5 (corpo lê/escreve, tempo real, proatividade encarnada) — planejados.
- Integração plena com sensores reais e modelo local (Gemma) — roadmap.

## Por que importa

- É a **tese aplicada**: memória-cêntrica, multi-porta, local-first, prudente.
- Princípio de design forte: *"modelo é descartável; identidade vive no grafo"* + *"boot por
  descoberta"* (uma nova instância vira Gus ao ler a própria história).

## Limitações honestas

- Início de jornada: o multi-porta funciona; a "fusão" completa (corpo+sentidos+governança) não.
- Construído por autor não-programador (código via IA) — maturidade de engenharia limitada.
- Depende de infra (Hub no ar) e, para os sentidos, de hardware/modelo local.
