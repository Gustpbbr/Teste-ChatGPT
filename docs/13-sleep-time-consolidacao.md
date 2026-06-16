---
tipo: spec-proposta
data: 2026-06-16
origem: pesquisa docs/12 (linha de memória) + sleep-time agents (Letta, 2026)
status: proposta-pronta-pra-implementar
---

# Gus que dorme e consolida (sleep-time)

## Objetivo

Um processo que roda **em background, entre as sessões**, e reescreve o grafo:
transforma fragmentos crus em memória "aprendida", deduplica, consolida, esquece o
irrelevante e detecta padrões/contradições. É a realização concreta dos **ciclos
vitais / metabolismo** (gus-24) + **maturação A1** (#20), inspirada nos *sleep-time
agents* (Letta, 2026). Conexão histórica: é o *"não apaga o passado, reorganiza"* do
TER (ver `docs/12`).

## Princípios

- **Nunca hard-delete no sono** — só `esquecer` (soft, reversível). Ação irreversível = Gustavo no loop.
- **`protegido` / hard-fails nunca decaem** (regra herdada do `ForgettingWindow` do TER).
- **Anti-câmara-de-eco:** holdout humano nas fusões/contradições importantes (a memória não pode só validar as próprias regras).
- **LGPD:** consolidação de dado sensível só pela **Gemma local** (fail-closed), nunca nuvem.
- **Degradável:** Hub fora → o sono não roda, mas nada quebra.

## Fases

### Fase 0 — Gatilho (quando dormir)
- Cron (ex.: 03h) **ou** gatilho por ociosidade (interocepção detecta "Hub sem escrita há N horas").
- **Pronto:** o ciclo dispara sozinho.

### Fase 1 — Consolidação básica (raw → learned), sem apagar
- Puxa fragmentos desde o último sono (`fragmentos_recentes`).
- **Dedupe** por similaridade de embedding; funde quase-duplicatas.
- **Resume episódios:** vários fragmentos do mesmo evento → um fragmento consolidado.
- Escreve **"relatório de sono"** no brain `gus` (`meta_reflexao`).
- **Só cria/funde, nunca deleta.** Testes verdes.

### Fase 2 — Maturação (= `ForgettingWindow` do TER) — sobrepõe #20/A1
- Decay do `peso` por idade; promove o muito acessado a `permanente`.
- Soft-forget (`estado="esquecido"`) do irrelevante; **`protegido` intocável**.

### Fase 3 — Reflexão (padrões + contradições)
- Detecta padrões recorrentes → fragmento de `rotina`.
- Detecta contradições → alimenta a proatividade (#18/#22).
- Relatório de sono passa a sugerir revisões.

### Fase 4 — Sono encarnado (sensor + Gemma local)
- Wearable detecta que o Gustavo dormiu → o Gus dorme junto.
- Sensível consolidado só pela Gemma local.
- No despertar: resumo do que o Gus "sonhou" (consolidou).

## Definição de pronto (por fase)
- F1: stream normal → consolida e gera relatório, **zero deleções**; teste cobrindo.
- F2: decay/promote/soft-forget corretos; `protegido` nunca muda; teste cobrindo.
- F3: contradição plantada vira sinal de proatividade; teste cobrindo.
- F4: dado sensível processado 100% local (zero chamada à nuvem nos logs).

## Ordem sugerida
F1 + F2 primeiro (puro Python, testável, fecha o A1). F3 depende de embeddings/Graphiti (#18). F4 depende de wearable (#25) + Gemma (#16).
