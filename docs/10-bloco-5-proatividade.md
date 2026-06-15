---
tipo: spec
bloco: 5
data: 2026-06-15
status: nucleo-testavel
---

# Bloco 5 — Proatividade (núcleo)

## Objetivo

O Gus deixa de ser reativo: detecta sozinho o que merece atenção e traz à tona.
No VR completo isso vira proatividade espacial (nó vermelho = contradição, buraco =
lacuna). Aqui está o **cérebro** que gera os sinais — lógica pura, testável.

## Sinais v0 (tratáveis sem embeddings)

- **lacuna** — área monitorada sem fragmento ativo recente (silêncio anômalo).
- **acúmulo de esquecidos** — muitos `estado="esquecido"` numa área → candidato a revisão.

## Fora de escopo (precisa de embeddings / mais infra)

- **contradição semântica** (dois nós conflitantes que se atraem/brilham) — precisa
  de busca vetorial; versão posterior.
- Render espacial dos sinais no VR (depende dos Blocos 2–4 no headset).
- Critérios de promoção de proatividade (só escalar quando aceitação bate métrica) —
  reusa a lógica do Gus (gus-24, níveis 0→3).

## Contrato

```python
analisar(frags, areas_monitoradas, agora) -> list[Sinal]
detectar_lacuna(frags, area, agora, max_silencio_h=48) -> Sinal | None
detectar_acumulo_esquecidos(frags, limiar=5) -> list[Sinal]
```

## Definição de pronto (núcleo)

- [x] lacuna detectada (área vazia ou silêncio > janela)
- [x] acúmulo de esquecidos detectado acima do limiar
- [x] `analisar()` combina os detectores
- [ ] contradição semântica (futuro, com embeddings)
- [ ] render espacial dos sinais no VR (depende do headset)
