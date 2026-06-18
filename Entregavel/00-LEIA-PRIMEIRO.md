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

## 🗂️ Estrutura deste dossiê

```
Entregavel/
├── 00-LEIA-PRIMEIRO.md       ← você está aqui
├── 01-visao-geral.md         ← o panorama (1 organismo, 10 ângulos)
├── 02-one-pager.md           ← pitch de 1 página + template de e-mail
├── 03-mapa-do-ecossistema.md ← todos os projetos e como formam o Gus
├── CLAUDE.md                 ← instruções para a IA-guia do tour de 20 min
├── LICENSE.md                ← licença aberta (MIT código / CC BY docs)
├── GLOSSARIO-MESTRE.md       ← todas as siglas e termos
├── MATRIZ-DE-MATURIDADE.md   ← o que roda vs. spec, por projeto/componente
├── alvos-pesquisadores.md    ← quem contatar e por quê
└── projetos/                 ← cada um: briefing.md (1 pág) + deep-dive.md (técnico)
    ├── phronesis-bench/      ← 🟢 benchmark + RESULTADOS (âncora)
    ├── mge/                  ← 🟢 motor de geração estruturada (funcional)
    ├── cex-cep/              ← 🟢/🟡 comitê de especialistas (deliberação)
    ├── gus/                  ← 🟡 a síntese (organismo de 3 camadas)
    ├── memoria-tear-ter/     ← 📄 a linha de memória (TEAR → TER → Gus)
    ├── ter-kai/              ← 📄 governança prudencial (middleware)
    ├── acee-mase/            ← 📄 percepção afetiva embarcada
    └── axon-mgx/             ← 📄 automação contextual + orquestração multiagente
```

> Para o quadro completo "o que roda vs. o que é spec", ver [`MATRIZ-DE-MATURIDADE.md`](MATRIZ-DE-MATURIDADE.md).

> ⚠️ **Antes de enviar a qualquer pessoa:** a pasta `Entregavel/` já passou por scan de PII
> (limpa). Mas o **material-fonte** (repos/dumps) contém dados pessoais/clínicos — não incluir
> sem limpar. Ver checklist no `02-one-pager.md`.

---

## 📜 O que está sendo oferecido

Este material é oferecido sob **licença aberta com atribuição** — ver [`LICENSE.md`](LICENSE.md).

- **Código** (ex.: Phronesis-Bench): **MIT** — use, modifique, distribua; mantenha o crédito.
- **Documentos/conceitos:** **CC BY 4.0** — use e adapte; cite o autor.
- **Intenção do autor:** *ceder o trabalho para que alguém leve adiante* — colaboração é
  bem-vinda, mas não exigida. O objetivo é que a ideia viva, não controlá-la.
