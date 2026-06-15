---
tipo: spec
bloco: 3
data: 2026-06-15
status: parcial-router-e-scaffold
---

# Bloco 3 — Corpo escreve (gestos viram memória) + rota local obrigatória

## Objetivo

O corpo passa a **escrever**: gestos no VR viram operações no Hub (criar associação,
esquecer, apagar). E o dado sensível ganha **rota local obrigatória** — biometria e
Dimagem nunca sobem pra nuvem. É aqui que a Gemma local deixa de ser opcional.

## Duas frentes

### 1. Roteamento (a peça crítica — testável, Python)
`route(frag) -> "local" | "cloud"`:
- `metadata.sensivel` OU `area in {dimagem}` → **"local"**
- senão → **"cloud"**
- **FAIL-CLOSED:** rota "local" exigida e modelo local indisponível → **bloqueia**
  (`RotaBloqueada`), NUNCA cai pra nuvem. Espelha a decisão fail-closed do MCP do Gus.

### 2. Escrita pelo corpo (frontend)
Gestos → operações, com **confirmação pra irreversível** (Gustavo no loop; auto-execução off V1):

| Gesto | Operação | Reversível? |
|---|---|---|
| juntar dois nós | criar associação (wikilink) + fragmento episódico | sim |
| empurrar pra longe | `esquecer` (soft, vira fantasma) | sim |
| jogar na lixeira | `apagar de vez` (hard) | **não → confirma** |

## Escopo desta entrega

- ✅ **Router** (`src/gus_sense/routing.py`) + testes (fail-closed coberto).
- ✅ **Escrita no frontend** (`web/src/hub.js`): `ingestar/esquecer/apagar`, degradável.
- ✅ **Semântica de ações** (`web/src/acoes.js`): mapeia ação→Hub, confirma irreversível.
- ⏳ **Input de mão/controle** (WebXR hand tracking) — precisa do headset (issue aberta).
- ⏳ **Servidor Gemma local** — precisa do modelo rodando na máquina (issue aberta).

## Degradação

- Escrita com Hub fora → "pendente", não quebra a interação.
- Modelo local exigido e ausente → **bloqueia o processamento daquele dado** (fail-closed).

## Definição de pronto (parcial)

- [x] `route()` decide local/cloud; sensível + sem local → `RotaBloqueada`
- [x] frontend tem funções de escrita degradáveis + confirmação pra apagar
- [ ] gesto de mão real dispara ação (headset)
- [ ] Gemma local plugada e rota "local" de fato processando

## Fora de escopo (Blocos 4–5)

- SSE (nó nascendo ao vivo), voz. Proatividade espacial / contradições brilhando.
