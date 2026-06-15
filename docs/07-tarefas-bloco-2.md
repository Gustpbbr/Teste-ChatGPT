---
tipo: tarefas-swarm
bloco: 2
data: 2026-06-15
---

# Tarefas do swarm — Bloco 2

| ID | Tarefa | Território | Status |
|---|---|---|---|
| B2-1 | Frontend WebXR read-only: cena + grafo 3D + painel de leitura | `web/` | ✅ scaffold |
| B2-2 | Ligar no Hub real (`/hub/recent`, `/hub/relacionados`) | `web/src/hub.js` + backend Gus | ⏳ aberta |
| B2-3 | Validar no headset Quest + layout de força (3d-force-graph) | `web/` | ⏳ aberta |

## Notas

- **B2-1** entregue como scaffold rodável com dados mockados (esta branch).
- **B2-2** depende do Hub no ar (estava 404). Quando voltar: implementar endpoint
  `/hub/relacionados` (busca semântica filtrando `estado != esquecido`, K=3,
  threshold=0.6 — gus-30.1) e trocar a fonte mock pela real em `hub.js`.
- **B2-3** precisa do hardware (não dá pra validar headless) + refino do layout.
