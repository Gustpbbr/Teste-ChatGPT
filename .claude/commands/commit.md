---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*)
description: Cria um commit git a partir das mudanças atuais
---

## Contexto

- Status atual: !`git status`
- Diff (staged e não-staged): !`git diff HEAD`
- Branch atual: !`git branch --show-current`
- Commits recentes: !`git log --oneline -10`

## Sua tarefa

Com base nas mudanças acima, crie **um único** commit git com mensagem clara e
descritiva (em português, no imperativo, ex: "Adiciona validação de PII no gateway").
Faça o stage e o commit numa única leva de chamadas de ferramenta. Não faça push.

<!--
PEÇA PRONTA — copiada de Biblioteca-Claude-code/building-blocks/commands/commit.md
O que faz: slash command que monta um commit a partir do diff atual.
A sintaxe `!`comando`` injeta a saída do comando no contexto antes do Claude ler.
Adaptado de: anthropics/claude-plugins-official → plugins/commit-commands (MIT).
-->
