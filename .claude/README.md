# `.claude/` — configuração do Claude Code no Gus Encarnado

Peças reutilizáveis trazidas (e adaptadas) da **Biblioteca-Claude-code**
(`Gustpbbr/Biblioteca-Claude-code`), encaixadas no contexto deste projeto.

## O que tem aqui

| Peça | Arquivo | O que faz |
|---|---|---|
| **Settings + permissões** | `settings.json` | Libera pytest/ruff/git de leitura; **blinda** `.env`, `data/` e `*.sensor.json` (regra rota-local/LGPD); pede confirmação em `git push`; registra o hook de segurança. |
| **Hook de segurança** | `hooks/bloquear-comandos-perigosos.sh` | `PreToolUse` em `Bash` — bloqueia `rm -rf /`, fork bomb, `mkfs`, `dd` sobre device, etc. (exit 2). |
| **Slash command** | `commands/commit.md` | `/commit` — monta um commit a partir do diff atual (PT-BR, imperativo). |
| **Subagent revisor** | `agents/revisor-de-codigo.md` | Revisa o diff com filtro de confiança ≥75, checando as **7 regras de ouro** do projeto (schema gus-18, PII scan, rota-local, retry backoff, testes). |

## Notas

- `settings.local.json` (overrides pessoais) deve ir no `.gitignore` se você criar um.
- O `deny` de leitura em `data/` e `*.sensor.json` reforça, no nível da ferramenta, o
  princípio de que **dado de sensor/biométrico não entra no contexto**.
- Procedência completa e documentação de cada recurso: ver a Biblioteca-Claude-code
  (`docs/03` settings, `docs/05` subagents, `docs/06` hooks, `docs/04` slash commands).
