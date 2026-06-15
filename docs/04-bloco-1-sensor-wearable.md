---
tipo: spec
bloco: 1
data: 2026-06-15
status: pronto-pra-implementar
---

# Bloco 1 — Primeiro sentido: Sensor Gateway + wearable

## Objetivo

O Gus passa a **perceber o corpo do Gustavo**. Um wearable (HR, HRV, sono) alimenta
o Gateway, que filtra ruído e transforma *eventos* em fragmentos no `saude/`. Sem VR —
o valor já aparece nas portas existentes (Telegram: *"sono ruim, HR matinal alto, pega leve hoje"*).

## Por que o wearable primeiro

- Contínuo, pessoal, alto sinal — e já existe a área `saude/` no vault.
- Independe de VR. Valida o pipeline sensor→Gateway→Hub end-to-end barato.

## O Sensor Gateway (coração do bloco)

```
wearable.stream() → windowize(60s) → denoise() → detect_events(baseline) → Fragmento → Hub
```

**Regra de ouro (anti-memória-lixão):** só vira fragmento o que é **evento** (foge da
baseline). Leitura crua contínua NUNCA vira fragmento. O Gateway é 90% filtro.

## Contratos

```python
# sensors.py
@dataclass
class Reading:
    metric: str            # "hr" | "hrv" | "sleep"
    value: float
    ts: datetime
    unit: str

class Sensor(Protocol):
    name: str
    def stream(self) -> Iterator[Reading]: ...

class WearableSensor:
    """Adaptador. v0 lê de fonte mockada/arquivo; depois pluga API real."""
    name = "wearable"
    def stream(self) -> Iterator[Reading]: ...

# filters.py
def windowize(readings, seconds=60) -> Iterator[Window]: ...
def denoise(window) -> Window: ...          # remove outliers grosseiros, suaviza
def detect_events(window, baseline) -> list[Event]: ...   # só desvios relevantes

# pipeline.py
class Gateway:
    def __init__(self, sensors, hub, scrub_pii): ...
    def run_once(self) -> list[Fragmento]: ...
```

## Eventos que viram fragmento (exemplos)

| Evento detectado | Fragmento (resumo) |
|---|---|
| HR repouso > baseline+40 por >15min | "HR repouso elevado: 110bpm/22min. Estresse ou esforço?" |
| Sono < 5h | "Sono curto: 4h12. Atenção à carga hoje." |
| HRV cai >30% vs média 7d | "HRV baixa hoje — recuperação ruim." |

## Decisões fechadas

- **Janela:** 60s. **Baseline:** média móvel dos últimos 7 dias por métrica.
- **Área:** `saude`. **`via`:** `sensor-wearable`. **`user_id`:** `gustavo`.
- **camada_temporal:** `semana` (evento de sensor decai; não polui memória permanente).
- **Sensível:** todo fragmento de biometria nasce com `metadata.sensivel=true` → rota local.
- **Fonte v0:** mockada (arquivo JSON de leituras) pra validar o pipeline sem API real.

## Definição de pronto

- `Gateway.run_once()` com stream mockado de leituras normais → **zero fragmentos** (filtro funciona).
- Stream com um pico de HR sustentado → **exatamente um** fragmento de evento, schema gus-18 válido.
- Todo fragmento de biometria sai com `sensivel=true`.
- Hub fora → fragmentos viram "pendente", Gateway não quebra (degradável).
- Testes verdes: normal (silêncio), evento (1 frag), ruído isolado (ignorado), Hub fora.

## Fora de escopo (não fazer agora)

- API real do wearable (Whoop/Oura/Apple) — v0 é mockado. Plugar depois.
- Render no VR (Bloco 2). Câmera/mic/ambiente (Bloco 4). Proatividade (Bloco 5).
