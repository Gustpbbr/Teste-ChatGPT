---
tipo: decisao-proposta
data: 2026-06-16
origem: pesquisa estado-da-arte memória de agente (jun/2026)
status: proposta-pra-avaliar
---

# Build-vs-borrow: Graphiti / Letta no Gus

## Objetivo

Decidir, com critério, se o Gus **adota** componentes OSS prontos ou **constrói**.
Princípio inegociável: **o Hub Qdrant continua a fonte da verdade — OSS entra como
peça, nunca substitui.**

## Papel de cada um (sem ilusão)

- **Graphiti** (Zep, Apache 2.0) → camada **bi-temporal / contradição** (hoje parada em #18). Maduro: lidera LongMemEval (63,8%).
- **Letta** (linhagem MemGPT) → **conceito** de memória auto-editada (core block + arquivo) → inspira o **curador**, não troca a stack.
- Nenhum substitui o Hub.

## Passos

### 1. Prova de conceito do Graphiti (isolada)
- Subir Graphiti self-hosted (graph store + embeddings/LLM **locais** — LGPD).
- Alimentar uma amostra de fragmentos como "episódios" com timestamp.
- **Teste decisivo:** a invalidação bi-temporal pega as contradições reais que importam? (5–10 casos teus.)
- **Decisão:** (a) adota a lib como índice temporal ao lado do Hub, **ou** (b) só porta o conceito — campos `valido_de`/`invalido_em` no gus-18 + checagem própria (mais leve).

### 2. Integração (se adotar)
- Graphiti **ao lado** do Hub: Hub = canônico; Graphiti = índice de consulta temporal + contradição (descartável/reconstruível).
- Fragmento novo → também vira episódio no Graphiti.
- Contradições → sinais de proatividade (fecha #18).
- LGPD: self-hosted + LLM local pra sensível.

### 3. Conceito do Letta no curador (barato)
- Curador mantém um **core block auto-editável** (`identidade_operacional`: identidade + foco atual) com o Hub como arquivo. Espelha a memória hierárquica do Letta sem adotar o framework.

## Régua de decisão
> **Adota** se: economiza trabalho real **E** roda self-hosted/local **E** encaixa no gus-18.
> **Constrói/porta o conceito** se: força nuvem, não encaixa no schema, ou manter 2 sistemas sincronizados custa mais que o ganho.

## Armadilhas
- **Sincronização Hub ⇄ Graphiti** → divergência. Mitigação: Hub manda; Graphiti é índice reconstruível.
- Self-hosting do Graphiti exige infra (graph DB + embeddings).
- Adotar só onde o encaixe é limpo — não por modismo.

## Relação com o sleep-time
O sleep-time (`docs/13`) é *quando* a consolidação roda; Graphiti/Letta é *com que
ferramenta* a contradição-temporal e a memória-auto-editada acontecem. Juntos: o Gus
dorme e, no sono, usa o grafo bi-temporal pra reinterpretar o passado.
