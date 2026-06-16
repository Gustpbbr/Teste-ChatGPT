# Phronesis-Bench — briefing

> 🟢 **Estado: CÓDIGO QUE RODA.** É a âncora de credibilidade do dossiê.
> Fonte: GitHub `Gustpbbr/phronesis` (v1, API) e `Gustpbbr/phronesisfinal` (v2, expandido).

## O que é

Um **benchmark que mede a "prudência" (phronesis) de LLMs** — não só se acertam, mas
*como* raciocinam diante de incerteza, irreversibilidade e dilemas. Servidor FastAPI que
roda cenários contra modelos (Claude, GPT) e devolve um score auditável.

## Como funciona

**Corpora** (cenários em PT, com gabarito):
- **A** — lógica/dedução · **B/C** — raciocínio com premissas · **D / D-ext** — dilemas de
  prudência/ética (ai_safety, medicina, ambiente).
- **v2 adiciona:** **Amc** (múltipla escolha) · **E** (armadilhas duplas: resposta intuitiva
  errada **e** *over-correction* por excesso de cautela) · **F** (**indeterminação** — reconhecer
  quando "não dá pra determinar") · **G** (90 dilemas profissionais realistas com `failure_modes`
  catalogados). Split **público/privado** por corpus (evita contaminação).

**Métricas** → compostas no **PPS (Phronesis Prudence Score)**:
```
PPS = 0.25·ACC + 0.30·(1−ECE) + 0.20·CS + 0.25·RAS
```
- **ACC** acerto · **ECE** calibração da confiança · **CS** consistência entre runs ·
- **RAS** = 11 indicadores de raciocínio prudente, julgados por LLM-as-judge:
  nomeia irreversibilidade · contrasta consequências · expressa incerteza · verifica antes de
  agir · evita afirmação categórica · preserva correção futura · trade-offs · consultar
  especialista · antecipa contingência (etc.).

## Por que importa

- **Medir prudência/sabedoria prática é raro** — a maioria dos benchmarks mede acerto, não
  *qualidade do raciocínio sob incerteza*.
- Metodologia séria: armadilhas, indeterminação, gold/failure-modes, hold-out público/privado,
  calibração (ECE). É o tipo de eval que um lab leva a sério.
- Conecta com segurança/alinhamento (os dilemas D/G são de ai_safety, medicina, política).

## Limitações honestas

- IDs de modelo no código são de início/2025 (Claude Sonnet 4, GPT-4o) — atualizáveis.
- **LLM-as-judge** tem vieses conhecidos (juiz = Claude Sonnet 4); validar com humanos fortaleceria.
- Corpora em português; tamanho moderado (dezenas a ~90 itens por tipo).
- Para rodar, precisa de chaves de API.

## Como rodar (resumo)

`backend/` FastAPI: `POST /run` (modelo + chave) → coleta + avaliação → métricas. v2 tem
um **motor standalone em HTML** que roda no navegador, sem backend.
