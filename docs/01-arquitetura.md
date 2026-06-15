---
tipo: arquitetura
data: 2026-06-15
---

# Arquitetura — configuração completa e contratos

## Fluxo de dados (sentidos → grafo → cérebro → corpo)

```
sensores ─► Sensor Gateway ─► fragmentos ─► Hub Qdrant ─► cérebro contextualiza
                                               │                    │
                                  interocepção ─┘            corpo VR renderiza
                                  (saúde do próprio sistema)  orbe fala / proatividade
```

## O Sensor Gateway (componente-chave, novo)

Sensor NÃO escreve direto no Hub. O Gateway é a camada que vira sensação em percepção:

```
sensor cru (ex: HR a cada 1s)
   → buffer/janela        (agrega em blocos temporais)
   → filtro/denoise       (descarta ruído, suaviza)
   → detector de evento   (só o que foge da baseline vira candidato)
   → scan PII             (biometria = sensível → marca rota local)
   → Fragmento (gus-18)   → Hub
```

**Regra de ouro:** só vira fragmento o que é *evento*. `HR 62,62,63...` não entra;
`HR 110 em repouso por 22min` entra.

### Contratos públicos (assinaturas que os agentes implementam)

```python
# src/gus_sense/gateway/sensors.py
class Sensor(Protocol):
    name: str                      # ex: "wearable"
    def stream(self) -> Iterator[Reading]: ...   # leituras cruas

# src/gus_sense/gateway/filters.py
def windowize(readings: Iterable[Reading], seconds: int) -> Iterator[Window]: ...
def denoise(window: Window) -> Window: ...
def detect_events(window: Window, baseline: Baseline) -> list[Event]: ...

# src/gus_sense/gateway/pipeline.py
class Gateway:
    def run_once(self) -> list[Fragmento]: ...   # 1 ciclo: coleta→filtro→evento→fragmento
```

## Interocepção (Bloco 0, novo)

```python
# src/gus_sense/interocepcao.py
def hub_health() -> Health: ...        # Hub responde? última escrita há quanto tempo?
def curador_heartbeat() -> Health: ... # curador escreveu nas últimas N horas?
def emit_self_fragment(h: Health) -> Fragmento | None:  # vira fragmento no brain "gus"
    ...
```

Quando a saúde degrada, emite fragmento `user_id="gus"`, `tipo="meta_reflexao"`,
`area="infra-hub"` — o Gus "sente" e registra o próprio mal-estar. E dispara alerta.

## Cliente do Hub (cola, novo aqui mas fino)

```python
# src/gus_sense/hub_client.py
class HubClient:
    def ingestar(self, frag: Fragmento) -> IngestResult: ...   # com retry backoff
    def health(self) -> bool: ...
    # DEGRADÁVEL: se Hub fora, NÃO levanta exceção fatal — retorna resultado
    # marcado como "pendente" e o chamador segue. Nunca derruba o nível de cima.
```

## Roteamento de modelo (reusa gus-29, contrato aqui)

```python
def route(frag: Fragmento) -> Literal["local", "cloud"]:
    # area in {dimagem} OU frag.metadata.sensivel  -> "local" (Gemma)
    # senão                                         -> "cloud" (Claude)
    # FAIL-CLOSED: rota "local" exigida e modelo local indisponível -> bloqueia.
```

## Contrato de degradação (válido em todas as camadas)

| Falha | Comportamento exigido |
|---|---|
| Sensor cai | Gus perde percepção daquele sentido; memória intacta |
| Gateway cai | sem novos fragmentos de sensor; resto opera |
| Hub cai | corpo VR ainda manipula arquivo; sem halo de memória; escrita vira "pendente" |
| Modelo local indisponível (dado sensível) | **bloqueia** o processamento daquele dado (nunca cai pra nuvem) |

## Schema do fragmento de sensor (exemplo gus-18)

```json
{
  "conteudo": "HR repouso 110bpm por 22min às 06:40 — acima da baseline (62). Sono 4h12 (ruim).",
  "tipo": "sensorial",
  "area": "saude",
  "camada_temporal": "semana",
  "confianca": 0.9,
  "via": "sensor-wearable",
  "user_id": "gustavo",
  "estado": "ativo",
  "metadata": { "sensor": "wearable", "sensivel": true }
}
```
