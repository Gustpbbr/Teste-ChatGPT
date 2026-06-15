# AGENTS.md — Coordenação entre agentes (swarm)

Este projeto foi quebrado pra ser construído por **vários agentes em paralelo**
(padrão orchestrator-worker). Estas são as regras pra eles não pisarem um no outro.

## Modelo de trabalho

- Um **orquestrador** lê `docs/05-tarefas-swarm.md`, distribui as tarefas e costura os resultados.
- Cada **worker** pega UMA tarefa (= uma issue), trabalha no seu **território exclusivo** e devolve um resumo.
- Dependências estão no DAG de `docs/05-tarefas-swarm.md`. Não comece uma tarefa cujas dependências não fecharam.

## Territórios (escrita exclusiva — evita conflito por construção)

| Território | Dono (1 worker por vez) | Arquivos |
|---|---|---|
| Schema | T-SCHEMA | `src/gus_sense/schema.py` + teste |
| Hub client | T-HUB | `src/gus_sense/hub_client.py` + teste |
| Interocepção | T-INTERO | `src/gus_sense/interocepcao.py` + teste |
| Filtros | T-FILTER | `src/gus_sense/gateway/filters.py` + teste |
| Sensores | T-SENSOR | `src/gus_sense/gateway/sensors.py` + teste |
| Pipeline | T-PIPE | `src/gus_sense/gateway/pipeline.py` + teste |
| Infra/CI | T-INFRA | `pyproject.toml`, `requirements.txt`, `.github/` |

**Regra:** se sua tarefa precisa editar arquivo de outro território, NÃO edite —
sinalize a dependência pro orquestrador. Cada arquivo tem um dono por vez.

## Contrato de PR de cada worker

1. Branch própria por tarefa: `agente/<id-tarefa>` (ex: `agente/t-filter-janela`).
2. Só toca o território da tarefa.
3. Inclui teste cobrindo o caminho (porta de entrada — sem teste não mergeia).
4. Resumo curto no PR: o que mudou, qual contrato expõe, o que o próximo precisa saber.
5. Respeita as regras de ouro do `CLAUDE.md` (degradação, rota local, anti-lixão, gus-18, fail-closed).

## Definição de pronto (global)

- `pytest` verde.
- Sem dado sensível em arquivo versionado (PII scan).
- Contratos (assinaturas públicas) batem com o que a spec do bloco define.
- Nada hard-coded que devesse ser env var (ver `.env.example`).
