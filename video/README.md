# video/ — Explainer do Gus Encarnado (Remotion)

Vídeo-código: a animação é definida em React/TypeScript (`src/GusEncarnado.tsx`),
versionável e reproduzível. ~27s, 1920x1080, 30fps.

## Rodar (na tua máquina)

```bash
cd video
npm install            # baixa Remotion (traz compositor próprio + chromium headless)
npm run studio         # abre o preview interativo no navegador
npm run render         # gera out/gus-encarnado.mp4
npm run still          # gera 1 frame (out/frame.png) — teste rápido
```

## Requisitos
- Node 18+ (testado no 22). O `npm install` da Remotion baixa o que precisa
  (compositor Rust + chromium headless) — não precisa de ffmpeg do sistema.

## Estrutura
```
src/index.ts        ← registerRoot
src/Root.tsx        ← Composition "GusEncarnado" (810 frames @ 30fps)
src/GusEncarnado.tsx ← as 6 cenas (orbe, camadas, tese, fluxo, blocos, fecho)
remotion.config.ts  ← config de render
```

## Editar
Mexa em `src/GusEncarnado.tsx` — cada `<Sequence>` é uma cena. `npm run studio`
mostra ao vivo. Pra mudar duração total, ajuste `durationInFrames` no `Root.tsx`.
