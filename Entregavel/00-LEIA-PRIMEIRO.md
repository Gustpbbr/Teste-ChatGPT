# 📂 Entregável — Dossiê de Pesquisa

> **Autor:** Gustavo Pratti de Barros — anestesiologista e pesquisador independente (Brasil).
> **O que é isto:** um corpo de trabalho exploratório de P&D sobre **IA pessoal centrada
> em memória, percepção afetiva e raciocínio prudente/auditável**. Não é um produto pronto —
> é um conjunto de protótipos, specs e um benchmark funcional, oferecido a pesquisadores
> que possam ver valor e levar adiante.

---

## ⏱️ Você tem 20 minutos? Comece por aqui

Não leia 100 arquivos. Escolha um caminho:

1. **Leitura rápida (10 min):** [`01-visao-geral.md`](01-visao-geral.md) — o panorama: o que existe,
   o que é real vs. aspiracional, e a tese central.
2. **Tour com IA (20 min):** abra este repositório com uma IA Claude (Claude Code, ou um
   Projeto no claude.ai com estes arquivos). Ela está instruída por [`CLAUDE.md`](CLAUDE.md)
   a te dar uma **visita honesta** — explicando, respondendo perguntas e **sinalizando o que
   é código que roda vs. o que é só especificação**. Pergunte à vontade: *"o que é real aqui?"*,
   *"qual a parte mais defensável?"*, *"isso já existe no mercado?"*.

---

## 🧭 Postura honesta (leia antes de julgar)

Este material foi construído ao longo de meses, em conversas com várias IAs. Por isso:

- **Mistura registros:** há **código que funciona** (ex.: o benchmark Phronesis), **specs em
  grau de patente** (aspiracionais) e **logs de conversa** (matéria-prima).
- **Há exagero histórico:** versões antigas usam linguagem grandiosa ("consciência", "pré-AGI")
  e métricas não-auditáveis. Isto está **sinalizado** e **não** deve ser levado ao pé da letra.
- **O valor real** está na *tese* (memória como centro; prudência auditável; percepção afetiva
  local) e em **um artefato concreto** (o Phronesis-Bench).

Se em algum ponto soar como hype, confie no ceticismo — e pergunte à IA-guia "isto é real?".

---

## 🗂️ Estrutura deste dossiê (em construção)

```
Entregavel/
├── 00-LEIA-PRIMEIRO.md      ← você está aqui
├── 01-visao-geral.md        ← o panorama (1 organismo, 10 ângulos)
├── 02-one-pager.md          ← pitch de 1 página para o pesquisador  [a fazer]
├── CLAUDE.md                ← instruções para a IA-guia do tour     [a fazer]
├── projetos/                ← 1 briefing honesto por projeto         [a fazer]
│   ├── phronesis-bench/     ← o artefato funcional (âncora de credibilidade)
│   ├── memoria-tear-ter/    ← a linha de memória (TEAR → TER → Gus)
│   ├── acee-mase/           ← percepção afetiva embarcada
│   ├── ter-kai/             ← governança prudencial (middleware)
│   └── gus/                 ← a síntese (organismo de 3 camadas)
└── alvos-pesquisadores.md   ← quem contatar e por quê               [a fazer]
```

> ⚠️ **Antes de enviar a qualquer pessoa:** passar tudo por um **scan de PII** (este corpo
> de trabalho contém dados pessoais/clínicos do autor). Ver checklist no fim do `02-one-pager.md`.

---

## 📜 O que está sendo oferecido

Este material é oferecido sob **licença aberta com atribuição** — ver [`LICENSE.md`](LICENSE.md).

- **Código** (ex.: Phronesis-Bench): **MIT** — use, modifique, distribua; mantenha o crédito.
- **Documentos/conceitos:** **CC BY 4.0** — use e adapte; cite o autor.
- **Intenção do autor:** *ceder o trabalho para que alguém leve adiante* — colaboração é
  bem-vinda, mas não exigida. O objetivo é que a ideia viva, não controlá-la.

> ⚠️ **Nota sobre IP registrado:** o TEAR tem registro de anterioridade (Biblioteca Nacional)
> e o TER KAI tem rascunho de patente. As licenças acima cobrem **direito autoral/uso** e
> **não concedem explicitamente direitos de patente**. Se o autor quiser também abrir patentes,
> a via seria Apache 2.0 — decisão consciente a tomar antes do envio.
