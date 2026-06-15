# web/ — NeuroGus (Bloco 2: o corpo lê o Hub)

App WebXR read-only que desenha os fragmentos do Gus como nós 3D. Roda no
desktop (fallback sem headset) e no browser do Quest (botão "Enter VR").

## Rodar (local)

Precisa de um servidor estático (módulos ES não abrem via `file://`):

```bash
cd web
python -m http.server 8000
# abre http://localhost:8000
```

## O que dá pra fazer

- Ver os nós: arquivos (azul claro), memórias (azul), sensoriais (vermelho),
  identidade (verde). Nós do brain `gus` têm anel orbital branco.
- **Clicar num nó** abre o painel de leitura. Conteúdo **sensível** não é exibido
  (só metadados) — LGPD por construção; decifrar é rota local (Bloco 3+).
- **Enter VR** (no Quest) entra no modo imersivo.

## Limites honestos (v1)

- Dados são **mockados** (`mock/fragmentos.json`). Ligar no Hub real é a issue B2-2
  (trocar a fonte em `src/hub.js` por `/hub/recent`).
- Hand tracking, pegar/mover, orbitar memórias ao tocar arquivo → **Bloco 3**.
- Layout é esférico fixo; força real (3d-force-graph) é refino (B2-3).
- **Não foi validado no headset** neste ambiente (sem hardware). Precisa do teu Quest.

## Estrutura

```
index.html        ← import map (Three.js via CDN) + monta o app
src/main.js       ← liga hub -> grafo -> cena -> seleção
src/hub.js        ← leitura do Hub (mock; costura pro /hub/recent)
src/graph.js      ← nós 3D, cores, anel do brain gus
src/scene.js      ← Three.js + WebXR (VRButton)
src/focus.js      ← painel de leitura (esconde sensível)
mock/fragmentos.json ← dados de exemplo
```
