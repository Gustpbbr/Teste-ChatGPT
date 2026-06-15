---
tipo: spec
bloco: 0
data: 2026-06-15
status: pronto-pra-implementar
---

# Bloco 0 — Interocepção (o Gus sente a si mesmo)

## Objetivo

Dar ao Gus a percepção do próprio estado interno. Hoje a memória pode parar de
crescer (curador quebrado, Hub fora) **sem ninguém ver por dias** — a pior falha
possível pra um sistema de memória. Interocepção = o organismo sentindo a própria dor.

## Por que primeiro

É a base de confiabilidade de tudo que vem depois. Sensores, VR, proatividade — tudo
depende de um grafo que está de fato crescendo. Não dá pra confiar em percepção do
mundo se o organismo não percebe quando está doente. E é barato.

## Escopo

1. **Health checks** do próprio sistema:
   - `hub_health()` — o Hub responde? Quando foi a última escrita?
   - `curador_heartbeat()` — o curador escreveu nas últimas N horas?
2. **Auto-fragmento** — quando a saúde degrada, emite fragmento no brain `gus`
   (`tipo=meta_reflexao`, `area=infra-hub`): *"Não formo memória há 3h — curador silencioso."*
3. **Alerta** — degradação dispara notificação (canal a definir; começar com log + stub).

## Contrato

```python
@dataclass
class Health:
    componente: str            # "hub" | "curador"
    ok: bool
    detalhe: str               # legível: "última escrita há 3h12"
    ultima_escrita: datetime | None
    severidade: Literal["ok", "warn", "erro"]

def hub_health() -> Health: ...
def curador_heartbeat(janela_horas: int = 6) -> Health: ...
def emit_self_fragment(h: Health) -> Fragmento | None:
    """Só emite se severidade != 'ok'. Fragmento user_id='gus'."""
def check_all() -> list[Health]:
    """Roda todos os checks. Usado por cron (ciclo vital) + sob demanda."""
```

## Decisões fechadas

- **Janela do heartbeat:** 6h default (parametrizável). Acima disso sem escrita = `warn`;
  acima de 12h = `erro`.
- **Onde escreve:** brain `user_id="gus"` (autobiografia), nunca `gustavo`.
- **Não spammar:** um auto-fragmento por episódio de degradação, não um por check
  (dedup por estado: só emite na *transição* ok→warn ou warn→erro).

## Definição de pronto

- `check_all()` retorna estado correto com Hub mockado (respondendo / mudo / lento).
- Degradação simulada (curador sem escrita há 7h) gera exatamente UM auto-fragmento `warn`.
- Hub fora → `hub_health()` retorna `severidade="erro"` sem levantar exceção (degradável).
- Testes verdes cobrindo: ok, warn, erro, transição (anti-spam).

## Fora de escopo (não fazer agora)

- Dashboard visual (vem no NeuroGus / Bloco 5).
- Métricas finas de custo/latência (Bloco posterior).
- Auto-cura (o Gus consertar a si mesmo) — só *perceber e avisar* por enquanto.
