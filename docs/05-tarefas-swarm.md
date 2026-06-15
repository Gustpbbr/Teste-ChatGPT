---
tipo: tarefas-swarm
data: 2026-06-15
---

# Tarefas do swarm — Blocos 0 e 1

Quebra pronta pra distribuir entre agentes em paralelo. **Cada tarefa = uma issue =
um worker.** Territórios isolados (ver `AGENTS.md`) pra evitar conflito de escrita.

## DAG de dependências

```
T1 schema ──┬─► T2 hub_client ──┬─► T6 interocepção (Bloco 0)
            │                   └─► T7 pipeline (Bloco 1)
            ├─► T3 filtros ─────────► T7
            └─► T4 sensores ────────► T7
T0 infra/CI ─ (paralelo a tudo, sem dependência)
T8 testes integração ─► depende de T6 e T7
```

Nível 0 (começa já, em paralelo): **T0, T1**
Nível 1 (após T1): **T2, T3, T4**
Nível 2 (após nível 1): **T6, T7**
Nível 3 (após T6+T7): **T8**

---

## Tarefas

### T0 — Infra/CI · território T-INFRA
- Finalizar `pyproject.toml`, `requirements.txt`, workflow `pytest` no `.github/`.
- **Pronto:** `pytest` roda no CI e na máquina; lint configurado.

### T1 — Schema do fragmento · território T-SCHEMA · dep: nenhuma
- Implementar `Fragmento` (dataclass) + validação gus-18 em `src/gus_sense/schema.py`.
- Enums: `tipo`, `camada_temporal`, `estado`; `confianca` clamp [0,1]; `via` validado.
- **Pronto:** cria fragmento válido; rejeita tipo/área inválidos; `sensivel` default coerente. Teste cobrindo.

### T2 — Hub client degradável · território T-HUB · dep: T1
- `HubClient.ingestar()` com retry backoff (2/4/8/16s) + `health()`.
- **Degradável:** Hub fora → retorna `IngestResult(status="pendente")`, NÃO levanta fatal.
- **Pronto:** ingest ok (mock), ingest com Hub fora → pendente sem exceção. Teste cobrindo.

### T3 — Filtros · território T-FILTER · dep: T1
- `windowize`, `denoise`, `detect_events` em `gateway/filters.py`.
- Baseline = média móvel 7d. Anti-lixão: leitura normal → zero evento.
- **Pronto:** janela normal → 0 eventos; pico sustentado → 1 evento; outlier isolado → ignorado. Teste cobrindo.

### T4 — Sensores · território T-SENSOR · dep: T1
- `Sensor` (Protocol), `Reading`, `WearableSensor` lendo fonte mockada (JSON).
- **Pronto:** `stream()` emite `Reading`s válidos da fonte mock. Teste cobrindo.

### T6 — Interocepção (Bloco 0) · território T-INTERO · dep: T2
- `hub_health`, `curador_heartbeat`, `emit_self_fragment`, `check_all` em `interocepcao.py`.
- Anti-spam: emite só na transição de severidade. Escreve no brain `gus`.
- **Pronto:** estados ok/warn/erro corretos; degradação gera 1 auto-fragmento; sem exceção com Hub fora. Teste cobrindo.

### T7 — Pipeline do Gateway (Bloco 1) · território T-PIPE · dep: T2,T3,T4
- `Gateway.run_once()` orquestra coleta→filtro→evento→scrub PII→ingest.
- Todo fragmento biométrico sai `sensivel=true`.
- **Pronto:** stream normal → 0 fragmentos; evento → 1 fragmento gus-18 válido com `sensivel=true`; Hub fora → pendente. Teste cobrindo.

### T8 — Testes de integração · território (compartilhado, read-mostly) · dep: T6,T7
- Fluxo end-to-end mockado: sensor → gateway → hub (pendente quando fora); heartbeat → auto-fragmento.
- **Pronto:** suíte de integração verde; cobre os critérios de sucesso dos docs 03 e 04.

---

## Notas pro orquestrador

- Comece despachando **T0 e T1** (nível 0). Só libere o resto quando T1 fechar (todos dependem do schema).
- Cada worker abre branch `agente/<id>` e PR isolado no seu território.
- Sem teste, não mergeia. Suíte verde é a porta de entrada (regra do `CLAUDE.md`).
- Conflito de escrita = decomposição errada: sinalize, não force edição fora do território.
