#!/usr/bin/env bash
# Hook PreToolUse (Claude Code) — bloqueia comandos Bash perigosos.
# Lê o evento (JSON) via stdin. Sai com código 2 para BLOQUEAR a chamada.
# Registrado em .claude/settings.json (matcher "Bash").
# Origem: Biblioteca-Claude-code/building-blocks/hooks/bloquear-comandos-perigosos.
set -euo pipefail

input="$(cat)"

# Extrai tool_input.command do payload do evento.
command="$(printf '%s' "$input" | python3 -c \
  "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" \
  2>/dev/null || true)"

# Padrões considerados perigosos (regex estendida). Ajuste conforme necessário.
patterns=(
  'rm[[:space:]]+-[a-zA-Z]*r[a-zA-Z]*f?[[:space:]]+(/|~|\$HOME)'  # rm -rf em raiz/home
  ':\(\)[[:space:]]*\{[[:space:]]*:[[:space:]]*\|[[:space:]]*:'    # fork bomb
  'mkfs'                                                          # formatar filesystem
  'dd[[:space:]]+if=.*of=/dev/'                                   # dd sobre device
  '>[[:space:]]*/dev/(sd|nvme|hd)'                                # sobrescrever disco
  'chmod[[:space:]]+-R[[:space:]]+777[[:space:]]+/'              # permissão ampla na raiz
)

for p in "${patterns[@]}"; do
  if printf '%s' "$command" | grep -Eq "$p"; then
    echo "🚫 Comando bloqueado pelo hook de seguranca (padrao: $p)." >&2
    echo "   Comando: $command" >&2
    exit 2
  fi
done

exit 0
