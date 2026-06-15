---
tipo: spec
bloco: 2
data: 2026-06-15
status: scaffold-implementado
---

# Bloco 2 — Corpo lê (o orbe VR mostra a memória)

## Objetivo

O corpo (VR/WebXR) começa a **ler** o grafo: fragmentos de memória e de sensor
viram nós 3D que o Gustavo vê e pode focar pra ler. Só leitura — escrita e gestos
de manipulação são Bloco 3.

## Princípio (v1 de maior impacto / menor esforço)

Conforme o roadmap: a primeira entrega é **"só olhar em 3D"**. Roda no browser
do desktop (fallback sem headset) e no browser do Quest (botão WebXR). Zero hand
tracking — seleção por clique/ponteiro. ~80% do impacto visual com ~10% do esforço.

## Escopo desta entrega (scaffold)

1. **App WebXR** (`web/`) em Three.js: cena, luz, render loop, botão VR.
2. **Leitura do Hub** (`web/src/hub.js`): v0 lê mock estático; costura pronta pra `/hub/recent`.
3. **Grafo 3D** (`web/src/graph.js`): nós coloridos por tipo; brain `gus` com anel
   orbital branco (gus-30.1); nó sensível marcado.
4. **Painel de leitura** (`web/src/focus.js`): focar um nó mostra o conteúdo;
   **conteúdo sensível NÃO é exibido** (placeholder "rota local") — LGPD por construção.

## Degradação

Hub indisponível → `carregarFragmentos()` retorna `[]` e o app ainda abre (cena vazia).
A alma cai, o corpo continua de pé.

## Decisões

- **Stack:** Three.js via CDN + import map (sem build step). WebXR via `VRButton`.
- **Layout:** distribuição esférica determinística (Fibonacci) no v1. Força real
  (3d-force-graph) é refino posterior.
- **Seleção:** raycast por clique no desktop. Gaze/controle/mão é Bloco 3.
- **Sensível:** nó com `metadata.sensivel` não renderiza conteúdo — só tipo/área.

## Definição de pronto (v1)

- [x] App abre no desktop e desenha os nós do mock
- [x] Brain `gus` visualmente distinto (anel)
- [x] Clicar num nó abre painel; nó sensível esconde conteúdo
- [x] Hub fora → app abre vazio sem quebrar
- [ ] Validado no headset Quest (precisa do hardware — issue aberta)
- [ ] Ligado no Hub real `/hub/recent` (precisa do Hub no ar — issue aberta)

## Fora de escopo (próximos blocos)

- Hand tracking, pegar/mover, orbitar memórias ao tocar arquivo (Bloco 3).
- SSE (nó nascendo ao vivo), voz (Bloco 4). Proatividade espacial (Bloco 5).
