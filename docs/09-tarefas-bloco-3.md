---
tipo: tarefas-swarm
bloco: 3
data: 2026-06-15
---

# Tarefas do swarm — Bloco 3

| ID | Tarefa | Território | Status |
|---|---|---|---|
| B3-1 | Router fail-closed (`route()`) — rota local obrigatória p/ sensível | `src/gus_sense/routing.py` | ✅ feito |
| B3-2 | Escrita pelo corpo: funções de Hub + semântica de ações + confirmação | `web/src/hub.js`, `web/src/acoes.js` | ✅ scaffold |
| B3-3 | Input de mão (WebXR hand tracking) ligando gesto→ação | `web/` | ⏳ aberta (headset) |
| B3-4 | Servidor Gemma local + rota "local" processando de fato | infra + `routing.py` | ⏳ aberta (modelo) |

## Notas

- **B3-1** é a espinha do "rota local obrigatória" e está testado (fail-closed coberto).
- **B3-2** entrega a lógica (ação→Hub, confirma irreversível); falta o disparo por gesto.
- **B3-3/B3-4** dependem de hardware (Quest) e do modelo local (Gemma) — só o Gustavo fecha.
