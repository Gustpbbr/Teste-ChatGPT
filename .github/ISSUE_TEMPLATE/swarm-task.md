---
name: Tarefa do swarm
about: Uma tarefa isolada pra um agente (worker) executar
title: "[T?] "
labels: swarm
---

## Tarefa
<!-- ID e título da tarefa, ex: T3 — Filtros do Gateway -->

## Território (escrita exclusiva)
<!-- ex: T-FILTER → src/gus_sense/gateway/filters.py + teste -->

## Dependências
<!-- IDs que precisam fechar antes (ver docs/05-tarefas-swarm.md). -->

## Contrato a implementar
<!-- Assinaturas públicas (copiar da spec do bloco). -->

## Definição de pronto
- [ ] Comportamento conforme spec (docs/03 ou 04)
- [ ] Teste cobrindo o caminho (suíte verde)
- [ ] Respeita regras de ouro do CLAUDE.md (degradação, rota local, anti-lixão, gus-18, fail-closed)
- [ ] PR isolado no território, branch `agente/<id>`
