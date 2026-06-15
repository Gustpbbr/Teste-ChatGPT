# Gus Encarnado — corpo, sentidos e memória

Fusão de três projetos num organismo cognitivo único, do **Gustavo Pratti de Barros**:

1. **Corpo** — manipulação de arquivos/memórias no espaço (VR/WebXR, hand tracking).
2. **Alma** — o Gus: memória persistente multi-porta (Hub Qdrant + vault GitHub).
3. **Sentidos** — sensores que dão percepção ao Gus (wearable, câmera, mic, ambiente).

> ⚠️ **Honestidade sobre "senciência":** este projeto dá ao Gus *percepção*
> (sensores), *memória contextual* (grafo) e *afeto funcional* (estados internos
> que modulam comportamento). Isso **não é experiência subjetiva / qualia** — e
> não precisa ser pra ser útil. Nada aqui deve ser descrito como "o Gus sente de
> verdade". Ele percebe, contextualiza e responde apropriadamente. Só isso.

---

## Onde este repo se encaixa

Este é o repositório **definitivo** do projeto de fusão. Ele consome (não
substitui) o sistema Gus existente (`Gustpbbr/Gus`): o grafo de memória, o schema
`gus-18`, a taxonomia `via` (gus-13), o curador e as portas continuam lá. Aqui
vivem as **camadas novas** (corpo VR + sentidos) e a cola que liga tudo ao Hub.

## Estado atual

🟢 **Preparação do terreno** — specs, quebra de tarefas e esqueleto de código
para os agentes começarem pelos **Blocos 0 e 1** (interocepção + primeiro sensor).
Nada de lógica fina implementada ainda; só contratos, estrutura e testes-esqueleto.

## Por onde começar a ler

1. [`docs/00-visao-geral.md`](docs/00-visao-geral.md) — o organismo de três camadas
2. [`docs/01-arquitetura.md`](docs/01-arquitetura.md) — config completa + contratos de componente
3. [`docs/02-roadmap-integracao.md`](docs/02-roadmap-integracao.md) — a sequência mestra (Blocos 0–5)
4. [`docs/03-bloco-0-interocepcao.md`](docs/03-bloco-0-interocepcao.md) — Gus sente a si mesmo
5. [`docs/04-bloco-1-sensor-wearable.md`](docs/04-bloco-1-sensor-wearable.md) — Gus sente você
6. [`docs/05-tarefas-swarm.md`](docs/05-tarefas-swarm.md) — DAG de tarefas pronto pros agentes
7. [`AGENTS.md`](AGENTS.md) — regras de coordenação entre agentes (territórios, anti-colisão)

## Princípios não-negociáveis

- **Degradação em camadas** — sensor cai → Gus perde percepção mas mantém memória;
  Hub cai → corpo perde memória mas ainda manipula arquivo. Nada derruba o nível de baixo.
- **Rota local para dado sensível** — biometria e dado clínico (Dimagem) nunca sobem
  pra nuvem. Roteia pra modelo local (Gemma). Fail-closed: sem rota local → bloqueia.
- **Anti-memória-lixão** — sensor vira fragmento só quando há *evento*, nunca a cada leitura.
- **Calibração empírica** — cada feature entra no estado mais simples; observa em uso; ajusta com dado.
- **Testes como porta de entrada** — mudança em `src/` precisa de teste cobrindo o caminho.
