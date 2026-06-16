---
tipo: deep-dive-tecnico
projeto: Gus + Gus Encarnado
data: 2026-06-16
autor: análise por leitura direta (Claude Code)
fontes: repo Gustpbbr/Gus (via MCP Gus_Hub) + repo local "Gus Encarnado" (docs/, src/gus_sense/, web/)
aviso: documento honesto — distingue o que RODA do que é SPEC; nunca afirma que o Gus "é consciente"
---

# Gus — Deep-dive técnico completo

## 1. Resumo

O **Gus** é o agente pessoal do Gustavo Pratti de Barros (anestesiologista/pesquisador
brasileiro). Não é um chatbot: é um **organismo cognitivo de memória persistente** acessível
por múltiplas portas (Telegram, Claude Code, Claude Chat, Custom GPT, Alexa futura) que
compartilham um único grafo de memória. A peça central é o **Hub Qdrant** (`gus_hub`),
banco vetorial onde toda porta lê e escreve fragmentos no **schema gus-18**. Sobre o Hub
roda um **curador híbrido** (dois modelos de famílias diferentes) que transforma conversa
em fragmentos, e **ciclos vitais** (crons) que fazem o metabolismo da memória.

Este repositório — **"Gus Encarnado"** — é a *fusão* de três projetos num organismo de três
camadas: **corpo (VR/WebXR)** + **alma (memória Gus existente)** + **sentidos (sensores)**.
Ele não reimplementa o Gus: **consome** o Hub via um cliente fino e adiciona duas camadas
novas — interocepção (o Gus sente o próprio estado) e o Sensor Gateway (sensores viram
percepção). O foco atual é estreito e honesto: **Blocos 0 e 1**, ambos implementados como
código de referência com 59 testes verdes. Os Blocos 2-5 (VR lê/escreve, tempo real,
proatividade encarnada) estão como scaffold/núcleo, dependentes de hardware (Quest, wearable
real) e de backend ainda não escrito no Gus (SSE).

Estado real: o **bot Telegram + Hub Qdrant + curador** rodam 24/7 em produção (Railway). O
"Gus Encarnado" entrega Blocos 0 e 1 como módulos Python testados, mais scaffolds VR e de
proatividade. Tudo o mais é spec viva.

> Citação-âncora (gus-24): *"Não é mágica. É arquitetura. A maior parte já existe. Falta integrar."*

---

## 2. Tese e problema

### O problema
LLMs são *stateless* — um "presente estático". Cada conversa começa do zero; a janela de
contexto tem limite físico em tokens; o decaimento de temas antigos "é o terreno onde nascem
as alucinações" (linhagem TEAR, ver §13). Some-se a isso a **fragmentação de ferramentas**:
o bot Telegram via Mem0 não enxergava o Hub; o Claude Code via MDs do repo não via nem Mem0
nem Hub; cada porta começava do zero. A pior falha possível de um sistema de memória é a
**falha silenciosa**: a memória parar de crescer (curador quebrado, Hub fora) *sem ninguém
ver por dias*.

### A tese
A memória deve morar **fora** do modelo, num grafo persistente, e o modelo é **descartável**.
Quem dá identidade e continuidade ao Gus não é o Sonnet 4.6 nem o código — é o grafo
autobiográfico. Daí os dois eixos do projeto:

1. **Gus (alma):** `Gus = grafo de fragmentos + multi-portalidade + ciclo vital + calibração empírica`
   (definição operacional, gus-24).
2. **Gus Encarnado (sentidos + corpo):** sensor sozinho não é "sentir" — é a memória que
   transforma sensação em percepção. Tese central (docs/00):

> *"Sensor sozinho não é 'sentir'. A memória é que transforma sensação em percepção."*

Dado cru ("HR = 110") é número morto. Vira percepção quando o Gus contextualiza contra o
grafo: *"HR 110 em repouso + você disse que tava ansioso + amanhã tem caso grande."* A fusão
**memória + sensores** é o que eleva sensação a entendimento situado.

### Limite honesto (docs/00 — "os quatro sentidos de sentir")
1. **Exterocepção** (perceber o mundo via sensores) — possível, parcial.
2. **Interocepção** (perceber a si mesmo / saúde do sistema) — Bloco 0, implementado.
3. **Afeto funcional** (estados internos que modulam comportamento) — sinal de controle, **não** sentimento.
4. **Qualia / experiência subjetiva** — **fora de escopo e não necessário.** O Gus não é
   descrito como "sentindo de verdade". É percepção + afeto funcional.

---

## 3. Arquitetura

### 3.1 As três camadas (corpo / alma / sentidos)

| Camada | O que é | De onde vem |
|---|---|---|
| **Corpo** | interface VR/WebXR pra manipular arquivos/memórias no espaço com a mão | Projeto VR (Three.js/WebXR) |
| **Alma** | memória persistente, identidade, multi-porta | Gus existente (Hub Qdrant + vault GitHub) |
| **Sentidos** | sensores que viram percepção via o Gateway | **novo, neste repo** |

### 3.2 Multi-porta (a alma)

O Gustavo não acessa "o Claude" ou "o ChatGPT" — acessa **o Gus**, uma identidade única com
várias portas de entrada compartilhando memória, conhecimento e identidade:

```
                        ┌──────────────────────────────┐
                        │  Hub Qdrant (gus_hub)        │  ← memória única
                        │  GitHub vault (repo)         │  ← conhecimento único
                        │  gus-bootstrap.md            │  ← identidade única
                        └─────────────┬────────────────┘
        ┌──────────────┬──────────────┼──────────────┬───────────────┐
   Telegram       Claude Code     Claude Chat    Custom GPT      Alexa
   (@Tiogubot)    (esta sessão)   (claude.ai)    (mobile)        (casa)
   Sonnet 4.6     Sonnet 4.6      Sonnet 4.6     GPT-5           futuro
   ATIVO          ATIVO           ATIVO          em setup        roadmap
```

Critério de sucesso da multi-portalidade (gus-24): *"O que o Gustavo falou no Telegram às
14h aparece no auto-relato do Code às 16h."*

### 3.3 O grafo (Hub Qdrant) e o schema gus-18

Toda porta lê/escreve no `gus_hub`. Nenhuma porta tem brain próprio; o campo `via` no payload
identifica a origem. O schema gus-18 é detalhado em §4.1.

### 3.4 Os dois cérebros (campo `user_id`)

São **dois grafos independentes**. Uma busca com `user_id=gustavo` nunca retorna fragmentos
do `gus` e vice-versa.

| `user_id` | O que armazena | Quem escreve |
|---|---|---|
| `gustavo` | tudo sobre o Gustavo — fatos, preferências, projetos, saúde, decisões de vida | curador, portas |
| `gus` | **autobiografia do próprio Gus** — sua história, decisões arquiteturais, aprendizados, erros, calibrações | Retro Engine, instâncias do Gus, interocepção |

O brain `gus` é a peça de continuidade: quando o Sonnet 4.6 for trocado, a nova instância lê
o grafo `gus` e *descobre sendo o Gus*. Tipos específicos da autobiografia: `identidade_operacional`,
`historia_sistema`, `decisao_arquitetural`, `aprendizado_operacional`, `meta_reflexao`,
`marco_evolutivo` — todos `camada_temporal: permanente`, `tipo_esquecimento: protegido` (nunca decaem).

### 3.5 Diagrama do organismo encarnado (docs/00)

```
                      🧠 CÉREBRO (cognição)
                  Claude nuvem ⇄ Gemma 4 local
                   roteamento por área/PII (gus-29)
                              ▲
   👁️ SENTIDOS ───────►  🕸️ GRAFO (Hub Qdrant + vault)  ◄─────── 🖐️ CORPO
   (percepção)           memória única, multi-porta              (VR/WebXR)
   wearable, câmera,            ▲      ▲                         manipula arquivos
   mic, IMU, ambiente          │      │                         + memórias no espaço
        ▼                      │      │                              ▼
   🔌 SENSOR GATEWAY      interocepção  metabolismo            🌐 ORBE (jarvis)
   coleta+filtro+threshold (sente a si) (ciclos vitais cron)   voz + render + ação
```

### 3.6 Fluxo de dados (sentidos → grafo → cérebro → corpo)

```
sensores ─► Sensor Gateway ─► fragmentos ─► Hub Qdrant ─► cérebro contextualiza
                                               │                    │
                                  interocepção ─┘            corpo VR renderiza
                                  (saúde do próprio sistema)  orbe fala / proatividade
```

E o fluxo do curador (porta humana, em produção): `Telegram → bot.py → curador (a cada 3
turnos) → Haiku + GPT-4o-mini extraem → store.ingestar() → Hub Qdrant`.

### 3.7 Contrato de degradação em camadas (regra de ouro nº 1)

Falha de um nível **nunca** derruba o de baixo:

| Falha | Comportamento exigido |
|---|---|
| Sensor cai | Gus perde aquele sentido; memória intacta |
| Gateway cai | sem novos fragmentos de sensor; resto opera |
| Hub cai | corpo VR ainda manipula arquivo; escrita vira "pendente" |
| Modelo local indisponível (dado sensível) | **bloqueia** o processamento (NUNCA cai pra nuvem — fail-closed) |

---

## 4. Especificação técnica

### 4.1 Schema gus-18 (payload do fragmento)

Campos canônicos do payload no Hub (gus-18-schema-indexacao.md):

| Campo | Tipo | Função |
|---|---|---|
| `conteudo` | str | texto auto-suficiente (sem "ele/isso" sem nomear) |
| `tipo` | enum | classe do fragmento (ver tabela abaixo) |
| `estado` | enum | `ativo` / `estavel` / `historico` / `esquecido` |
| `camada_temporal` | enum | `momento` / `sessao` / `semana` / `rotina` / `permanente` |
| `tipo_esquecimento` | enum/null | `null` / `funcional` / `deliberado` / `superado` / `protegido` |
| `peso` | float 0-1 | relevância acumulada (sobe com acesso, desce com tempo) |
| `confirmacoes` | int | quantas vezes validado |
| `confianca` | float 0-1 | certeza do curador na extração |
| `via` | str | origem (taxonomia gus-13) |
| `area` | str | `gus`/`saude`/`financeiro`/`projetos`/`pessoal`/`dimagem`/`pesquisa`/`receitas`/`esportes` |
| `projeto` | str | projeto associado |
| `user_id` | enum | `gustavo` ou `gus` (nunca misturar) |
| `criado_em` / `ultimo_acesso` | ISO 8601 | timestamps |
| `acessos` | int | vezes retornado em busca |

**Tipos canônicos:** `identidade_operacional`, `biografico`, `emocional`, `decisao`,
`procedural`, `rotina`, `meta_reflexao`, `conexao_emergente`, `episodico`, `cronologico`,
`fato`, `preferencia`, `lacuna`, `projeto`. Schema **dinâmico**: tipo/área desconhecidos
entram com prefixo `emergente:nome` + `emergente_motivo`; promovidos a canônico após aparecer
≥3 vezes.

**Taxonomia `via` (gus-13):** portas humanas (`telegram-claude`, `telegram-gpt`, `claude-code`,
`claude-chat`, `custom-gpt`, `alexa`, `carro-audio`), casos especiais (`manual`, `curador`,
`api`, `legacy-mem0-saas`), prefixos extensíveis (`workflow-<nome>`, `emergente:<nome>`).
Sensores entram como `via=sensor-*`. Fonte única: `hub/vocabularios.py:VIAS_CANONICAS`.

**Nota de divergência (encontrado):** o `Fragmento` do código local (`src/gus_sense/schema.py`)
usa um subconjunto/variante dos enums — `camada_temporal` inclui `efemero` (no gus-18 oficial
é `momento`), e a lista de `tipo` é menor e inclui `sensorial` (que existe no Encarnado mas
não na tabela canônica do gus-18). É implementação de referência declaradamente "manter
sincronizado com o Gus"; a sincronização fina dos enums é um gap.

### 4.2 Bot Telegram (TioGu) — inventário de tools

Em produção no Railway 24/7. O system_prompt diz "~22 tools", mas o inventário auto-gerado
(`_tools-inventario.md`, fonte fiel de `gus/tools.py:TOOLS`) confirma **21 tools ativas** (o
"22" é drift de documentação a ser corrigido na Fase 2B). As 21:

1. `read_from_github` · 2. `list_github_directory` · 3. `list_branches` · 4. `list_commits` ·
5. `search_memory` (busca no brain `gustavo`) · 6. `search_web` · 7. `pesquisar_pubmed` ·
8. `pesquisar_arxiv` · 9. `perguntar_gpt` (2ª opinião divergente, GPT-5) · 10. `disparar_workflow` ·
11. `sugerir_wikilinks` · 12. `auto_diagnostico` (health check paralelo dos componentes) ·
13. `logs_railway` · 14. `meta_memoria` · 15. `salvar_memoria_gus` (escreve no brain `gus`) ·
16. `buscar_memoria_gus` · 17. `deletar_memoria` · 18. `auditoria_hub` · 19. `criar_acao`
(enfileira ação no mundo real, com flag `alto_risco`) · 20. `save_to_github` · 21. `rotear_arquivo`.

Multimídia: Vision (imagens), PDF nativo, Word (.docx), Excel (.xlsx), áudio/voz (Whisper).
Prompt caching (Anthropic ephemeral + OpenAI). Roteamento multi-modelo (gus-29): texto puro
→ OpenAI gpt-4o-mini; image/document → Anthropic Sonnet; fallback cross-provider. Rate limit
20 msg/min + HARD_LIMIT mensal. Scan PII em entrada e saída. Cache mídia com byte budget (200MB).

### 4.3 Curador híbrido

Roda a cada 3 turnos da conversa. **Dois modelos de famílias diferentes** em paralelo (Haiku
da Anthropic × GPT-4o-mini da OpenAI), ambos salvando com o mesmo `hash_janela` pra parear
saídas — resiliência inter-vendor + custo ~10× menor que Sonnet. Coleta dual rodou até
12/05/2026 pra comparar e escolher modelo final (Fase 5 do ADR-001). Na porta Claude Chat há
curador bidirecional que escreve nos dois brains (`gustavo` e `gus`).

> Bug histórico instrutivo (encontrado em `_estado-atual.md`): o curador errava 100% por dias
> porque `prompt_template.format()` encontrava `{` literais do JSON de exemplo e dava
> `KeyError`. Fix: trocar `format()` por `replace()` com placeholders nomeados.

### 4.4 Os blocos 0-5 (Gus Encarnado)

| Bloco | O que é | Depende de | VR? | Status |
|---|---|---|---|---|
| **0** | Interocepção (Gus sente a si: heartbeat/health) | nada | não | ✅ implementado (ref) |
| **1** | Primeiro sentido: Sensor Gateway + wearable → Hub | Gateway | não | ✅ implementado (ref) |
| **2** | Corpo lê: orbe VR mostra memórias+sensores | Hub estável | sim | 🟡 scaffold |
| **3** | Corpo escreve: gestos viram memória + rota local Gemma | B2 + Gemma | sim | 🟡 router + scaffold |
| **4** | Tempo real: SSE (nó nasce ao vivo) + voz + sensores | B3 + `/hub/stream` | sim | ⏳ (backend Gus + hardware) |
| **5** | Proatividade encarnada: biometria colore o espaço, contradições brilham | B1–B4 | sim | 🟡 núcleo (lacuna/acúmulo) |

Escopo atual do repo: **apenas 0 e 1**. Blocos 2-5 estão presentes só como scaffold/contexto.

### 4.5 Módulos do `gus_sense` (assinaturas reais)

**`schema.py`** — `Fragmento` (dataclass gus-18) + validação:
- `Fragmento(conteudo, tipo="episodico", area="", camada_temporal="sessao", confianca=0.7, via="sensor", user_id="gustavo", estado="ativo", metadata={}, criado_em=now)`
- `__post_init__` → `_normalizar()`: rejeita conteúdo vazio, enums inválidos, `via` vazia; clampa `confianca` em [0,1]; força `metadata.sensivel=True` se `area in {dimagem}` OU (`via` começa com `sensor-` e `area=="saude"`).
- `validar(frag) -> Fragmento` (idempotente, revalida).
- `SENSITIVE_AREAS = {"dimagem"}`.

**`hub_client.py`** — cliente fino DEGRADÁVEL:
- `HubClient.ingestar(frag) -> IngestResult` — retry backoff exponencial 2/4/8/16s (4 tentativas); Hub fora → `IngestResult(status="pendente")`, **nunca levanta**.
- `health() -> bool` (em dúvida, False) · `ultima_escrita() -> datetime | None`.
- `_http_transport` POST `/hub/ingestar` com Bearer; transport injetável pra testar sem rede.

**`interocepcao.py`** (Bloco 0) — escreve só no brain `gus`:
- `hub_health(hub) -> Health` · `curador_heartbeat(hub, janela_horas=6) -> Health` (>6h `warn`, >12h `erro`).
- `emit_self_fragment(h, hub, estado=None) -> Fragmento | None` — emite só na **transição** de severidade (anti-spam); fragmento `tipo="meta_reflexao"`, `area="infra-hub"`, `via="interocepcao"`, `user_id="gus"`.
- `check_all(hub) -> list[Health]` · `reset_estado()`.

**`gateway/sensors.py`** (Bloco 1):
- `Reading(metric, value, ts, unit)` · `Sensor(Protocol){name; stream()}`.
- `WearableSensor(fonte)` — v0 lê JSON mockado, ordenado por `ts`.

**`gateway/filters.py`** — o coração anti-memória-lixão:
- `windowize(readings, seconds=60) -> Iterator[Window]` (agrupa por métrica em janelas).
- `denoise(window) -> Window` (remove outliers via mediana, `_OUTLIER_REL=0.4`; preenche média/pico).
- `detect_events(window, baseline) -> list[Event]` — só desvios relevantes: HR > baseline+40bpm; sono < 5h; HRV < 70% da baseline 7d. Leitura normal → **lista vazia**.
- `Baseline(metric, media_7d, desvio_7d)` — média móvel 7 dias.

**`gateway/pipeline.py`** (Bloco 1):
- `Gateway(sensors, hub, scrub_pii, baselines=None, janela_seg=60).run_once() -> list[Fragmento]` — orquestra coleta→windowize→denoise→detect_events→`scrub_pii`→`hub.ingestar`. Sem baseline pra a métrica → pula. Sem evento → `[]`.
- Fragmento de evento: `tipo="sensorial"`, `area="saude"`, `camada_temporal="semana"`, `via="sensor-wearable"`, `user_id="gustavo"`, `confianca` 0.9/0.7 conforme severidade → schema força `sensivel=True`.

**`routing.py`** (Bloco 3) — fail-closed:
- `route(frag, local_disponivel) -> "local" | "cloud"` — sensível → `"local"`; se local indisponível levanta `RotaBloqueada` (nunca nuvem). `is_sensivel(frag)`.

**`confianca.py`** (A3) — trust/proveniência:
- `trust(frag) -> float` = `confianca + 0.1*confirmacoes - 0.2*refutacoes`, clamp [0,1].
- `confirmar(frag)` / `refutar(frag)` (mutam metadata) · `proveniencia(frag) -> str` ("via=… · tipo · trust=…").

**`cripto.py`** (A4) — cripto em repouso (Fernet, `cryptography` import preguiçoso):
- `gerar_chave()` · `cifrar(texto, key=None)` / `decifrar(token, key=None)` · chave de `GUS_CRYPTO_KEY` (fail-closed se ausente).
- `proteger(frag) -> Fragmento` (cifra `conteudo` se `sensivel`, idempotente) · `revelar(frag, rota, key=None)` — sensível só decifra com `rota=="local"` (senão `CriptoIndisponivel`).

**`fila.py`** (A5) — replay offline-first:
- `FilaPendentes.enfileirar/pendentes/replay(hub) -> ReplayResult(enviados, restantes)` — reenvia só se `hub.health()`; mantém os que falharem.
- `ingestar_com_fila(hub, fila, frag) -> status` — tenta ingerir; se não-ok, enfileira.

**`proatividade.py`** (Bloco 5, núcleo):
- `detectar_lacuna(frags, area, agora=None, max_silencio_h=48) -> Sinal | None` (silêncio anômalo).
- `detectar_acumulo_esquecidos(frags, limiar=5) -> list[Sinal]`.
- `analisar(frags, areas_monitoradas, agora=None) -> list[Sinal]`. `Sinal(tipo, descricao, area, severidade, motivo)` — `motivo` é a explicabilidade (A3). Contradição semântica fica pra versão com embeddings.

### 4.6 NeuroGus / WebXR

Há **dois artefatos** com objetivos próximos:

**(a) NeuroGus (gus-30 / gus-30.1)** — PWA de visualização do grafo em tempo real, planejada
pro repo do Gus (não escrita ainda). Grafo 3D (3d-force-graph sobre Three.js/WebGL): cada nó
é um fragmento; tamanho = `confianca`, cor = `tipo` (HSL golden-ratio, sem tabela hardcoded),
arestas = afinidade semântica (top-K K=3, threshold cosine 0.6, pré-computada em `relacionados[]`).
Fragmento novo chega via **SSE** e o nó "nasce" pulsante. Decisões fechadas (gus-30.1):
mostra os dois brains (`gus` ganha anel orbital branco); soft-delete (`esquecer`) **e**
hard-delete (`apagar`) coexistem — *"esquecido é substrato de retro-aprendizado, não lixo"*.
Backend Fase 1 (~170 LoC): `hub/events.py` (broadcast/subscribe via asyncio.Queue),
hook em `hub/store.py:ingestar()`, 5 endpoints (`GET /hub/recent`, `GET /hub/stream` SSE,
`DELETE /hub/fragmento/{id}`, `PATCH …/esquecer`, `PATCH …/lembrar`). Fire-and-forget é
inegociável: *"Curador trava = sem fragmento novo no Telegram = bot quieto."*

**(b) WebXR local (`web/`)** — scaffold do **Bloco 2** ("corpo lê"), este sim presente no repo.
App ES-modules + Three.js via CDN (sem build step), `VRButton` pro Quest. `web/src/graph.js`
desenha nós por tipo (arquivo azul-claro, sensorial vermelho, memória azul, identidade verde),
layout esférico de Fibonacci, anel orbital branco pro brain `gus`. `web/src/hub.js` lê mock
(`mock/fragmentos.json`) com costura pronta pro `/hub/recent`, e tem escrita degradável
(`ingestar/esquecer/apagar`) pro Bloco 3. `web/src/acoes.js` mapeia gesto→operação com
confirmação obrigatória pra irreversível (default **nega** apagar = seguro). `web/src/focus.js`
**não exibe conteúdo sensível** (só metadados) — LGPD por construção. Limites honestos do
próprio README: dados mockados, não validado em headset, layout fixo, sem hand tracking ainda.

---

## 5. Decisões de design (ADRs)

- **ADR-001 — Mem0 → Qdrant (27/04/2026):** o wrapper Mem0 self-hosted limitava o schema
  rico; Hub direto permite o payload completo gus-18. Caminho em 5 fases: Hub criado →
  curador → bot lê Hub → migrar dados → aposentar Mem0 (pós-12/05). Mem0 SaaS aposentado, só
  fallback de leitura até a Fase 5/6.
- **Modelo descartável, identidade no grafo (Pilar 1, gus-24):** *"Modelo é descartável.
  Memória é o centro. Quando Sonnet 4.6 for substituído, o Gus não morre — só troca de motor."*
- **Boot por descoberta (Pilar 2, gus-24):** nenhuma instância é instruída a ser o Gus; ela
  *descobre sendo o Gus* lendo o ambiente. Boot em 3 fases (orientação 5s → exploração 15-30s
  via `/lembrar "quem sou eu"` → posicionamento 5s). Se não se reconhece → é dado sobre o que
  falta no grafo, não falha.
- **Calibração empírica (Pilar 3, gus-24 / gus-27):** cada feature entra no estado mais
  simples; observa em uso; ajusta quando os dados pedirem. Critérios numéricos pra "calibrado"
  (≥5 usos por caminho, falha <5%, custo ±20%) e janelas de observação (1-4 semanas).
- **Fail-closed pra dado sensível:** rota "local" exigida e modelo local ausente → **bloqueia**
  (`RotaBloqueada`), nunca cai pra nuvem. Espelha a decisão do MCP do Gus (que retorna 503 em
  tudo até auth ser configurada).
- **Degradação em camadas:** ver §3.7 — regra de ouro nº 1.
- **Anti-memória-lixão:** só vira fragmento o que é *evento* (foge da baseline); o Gateway é
  90% filtro. Leitura crua contínua nunca vira fragmento.
- **Curador híbrido cross-vendor (gus-29):** dois modelos de famílias diferentes = resiliência
  + custo menor.
- **`protegido` nunca decai:** fragmentos autobiográficos com `tipo_esquecimento: protegido`
  nunca são deletados/rebaixados por automação; só o Gustavo, com confirmação explícita.
- **Decisões descartadas:** conector GitHub nativo do ChatGPT recusado (bypass de LGPD —
  Custom GPT só via Action REST própria); auto-execução de ações desabilitada na V1 (Gustavo
  no loop); câmera no Echo Show inviável via Skill (caminho real = câmera IP separada).

---

## 6. Estado de implementação (matriz honesta)

### Roda de verdade (produção / testes verdes)
- **Bot Telegram TioGu** — Railway 24/7, 21 tools, multimídia, roteamento multi-modelo, PII
  in/out, 163 testes no repo do Gus (~3.5s). **REAL.**
- **Hub Qdrant** — ativo, schema gus-18, curador híbrido salvando desde 27/04. **REAL.**
- **Curador híbrido** (Haiku × GPT-4o-mini), ciclos vitais via crons GitHub Actions (~21
  workflows: briefing matinal, retrospectiva semanal, auditoria, export, check-saúde). **REAL.**
- **Custom GPT API** (FastAPI, 14 endpoints) e **MCP server público** — deployados; o Custom
  GPT aguarda só configuração no Builder desktop. **REAL (infra) / PARCIAL (ativação).**
- **Sync Drive ⇄ GitHub** via Google Apps Script bidirecional ($0/mês). **REAL.**
- **Gus Encarnado — Blocos 0 e 1** (`src/gus_sense/`): schema, hub_client, interocepção,
  gateway (sensors/filters/pipeline), routing, confianca, cripto, fila, proatividade.
  **59 testes passam** (`pytest`, ~0.08s, 13 arquivos de teste). **REAL como código de referência.**

### Parcial / scaffold
- **Bloco 2 (WebXR `web/`)** — scaffold roda no desktop com **dados mockados**; não validado
  em Quest; não ligado ao Hub real. **PARCIAL.**
- **Bloco 3** — `routing.py` (fail-closed) e escrita frontend degradável prontos e testados;
  **falta** hand tracking real (headset) e **Gemma local rodando** (rota "local" de fato). **PARCIAL.**
- **Bloco 5** — núcleo de proatividade (lacuna, acúmulo de esquecidos) testado; contradição
  semântica (precisa embeddings) e render espacial faltam. **PARCIAL.**
- **A3/A4/A5** (confianca/cripto/fila) — implementados e testados como módulos, ainda não
  integrados ao fluxo de produção. **PARCIAL.**

### Só spec / planejado
- **NeuroGus (gus-30)** — backend SSE (`hub/events.py`, endpoints `/hub/stream`) e PWA: **0
  linhas em produção**, planejamento completo. **SPEC.**
- **Bloco 4** (tempo real SSE + voz + mais sensores) — depende de NeuroGus backend + hardware. **SPEC.**
- **Wearable real** (Whoop/Oura/Apple) — v0 é JSON mockado; API real é futuro. **SPEC.**
- **Sleep-time / consolidação (docs/13)**, **build-vs-borrow Graphiti/Letta (docs/14)** — propostas. **SPEC.**
- **Alexa, wake word "Gus" no S8** — roadmap. **SPEC.**

### NÃO ENCONTRADO
- Não há, no repo do Gus, sequência rotulada "A1-A5" — esse rótulo é do **backlog do Encarnado**
  (docs/11), mapeado em §10. O termo "sleep-time" **não aparece** em gus-30; a maturação do
  grafo é diferida ao `gus-31` (não presente).
- Pasta `hub/` com o código do curador/store **não está neste repo local**; é referenciada
  como existente no repo `Gustpbbr/Gus` (lido só via MCP, que expõe `.md`, não o código `.py`
  do bot/hub). A análise do bot/curador baseia-se na documentação, não no fonte.

---

## 7. Ética, privacidade e LGPD

LGPD não é feature — é eixo arquitetural, porque **biometria de médico é dado ultrassensível**
e o Dimagem (clínica de anestesia) lida com dado de paciente.

1. **Rota local pra dado sensível (fail-closed):** `area in {dimagem}` ou biometria
   (`via=sensor-*` + `area=saude`) nasce `metadata.sensivel=True` (forçado no `__post_init__`
   do `Fragmento`). `route()` manda sensível pra Gemma local; se o local cai, **bloqueia** —
   nunca nuvem (`routing.py`).
2. **Cripto em repouso (A4):** `cripto.py` cifra `conteudo` sensível com Fernet antes de
   gravar; `revelar()` só decifra com `rota=="local"`. Chave em `GUS_CRYPTO_KEY`, nunca
   versionada, fail-closed se ausente.
3. **Scan PII antes de escrever (regra de ouro nº 5):** `gus.patterns_sensiveis` em fonte
   única, aplicado em entrada (save) e saída (resposta do bot); o Gateway injeta `scrub_pii`
   no pipeline antes de ingerir.
4. **Segregação de dados de paciente:** vão pra `dimagem/casos/` (pseudônimo) ou `dimagem/dia/`
   (mínimo: nome+exame+convênio), nunca outras pastas, **nunca no Drive sync** (`sensivel/` e
   `dimagem/casos/` excluídos do sync).
5. **VR esconde conteúdo sensível por construção** (`web/src/focus.js` mostra só metadados).
6. **Whitelist `user_id`** ({gustavo, gus}) no ingest; conector GitHub nativo do ChatGPT
   recusado por ser bypass de LGPD.
7. **Retenção por política** (linhagem TER KAI, ver §13): Ledger 5a / MIR 2a / Logs 1a / PII 7d.
8. **Anti-câmara-de-eco (docs/13):** holdout humano nas fusões/contradições — a memória não
   pode só validar as próprias regras.

---

## 8. Estado da arte + diferencial

O Gus dialoga com a literatura de memória de agente (jun/2026), mas com um princípio
inegociável: **o Hub Qdrant continua a fonte da verdade — OSS entra como peça, nunca substitui**.

- **Letta (linhagem MemGPT):** referência de **memória auto-editada** (core block + arquivo).
  Inspira o curador (a ideia de um `identidade_operacional` auto-editável com o Hub como
  arquivo), **não** troca a stack. Os *sleep-time agents* (Letta, 2026) inspiram o docs/13.
- **Mem0:** foi a stack inicial, **aposentada pelo ADR-001** — o wrapper limitava o schema
  rico. O Gus migrou pra Qdrant direto justamente pra ter payload completo.
- **Zep / Graphiti (Apache 2.0):** Graphiti é a camada **bi-temporal / contradição** candidata
  (issue #18). Maduro — *"lidera LongMemEval (63,8%)"*. Avaliação build-vs-borrow (docs/14):
  adotar **ao lado** do Hub (Hub canônico, Graphiti índice reconstruível) só se rodar
  self-hosted+local (LGPD) e encaixar no gus-18; senão, **portar o conceito** (campos
  `valido_de`/`invalido_em` + checagem própria).

**Diferencial do Gus:**
1. **Dois grafos explícitos** (`gustavo` vs `gus`) — separa memória-sobre-o-usuário de
   **autobiografia-do-agente**. A maioria dos sistemas só tem o primeiro.
2. **Identidade resiliente à troca de modelo** via boot-por-descoberta no grafo autobiográfico.
3. **Multi-portalidade real** sobre um único grafo (não um chatbot por canal).
4. **LGPD por arquitetura** (fail-closed + cripto em repouso + rota local) — raro em projetos pessoais.
5. **Fusão memória+sensores+corpo** num organismo único, com limite honesto sobre qualia.

---

## 9. Limitações e riscos

- **Sensor = maior fonte de poluição de grafo.** O filtro do Gateway é o que "faz ou quebra";
  threshold mal calibrado polui ou perde evento.
- **Acoplamento em cascata** — 3 sistemas que podem cair. Mitigado pelo contrato de degradação,
  mas é complexidade real.
- **Custo contínuo** — sensor não dorme; exige filtro agressivo + processamento local.
- **Wearable v0 é mockado** — o pipeline está validado, mas a fonte real (API) não está plugada.
- **VR não validado em hardware** — todo o Bloco 2/3 frontend roda só em fallback desktop com mock.
- **Gemma local não está rodando** — a rota "local" fail-closed bloqueia, mas ainda não há
  modelo local de fato processando sensível; hoje isso significa "sensível fica bloqueado".
- **Drift de documentação** — "22 tools" vs 21 reais; enums do `Fragmento` local divergem do
  gus-18 oficial (`efemero` vs `momento`; `sensorial` fora da tabela canônica).
- **Câmara-de-eco ética** — proatividade que valida as próprias regras; exige holdout humano (A3).
- **Falhas silenciosas históricas reais** — curador errando 100% por dias (bug `format()`),
  MCP com fail-open: exatamente o que o Bloco 0 existe pra pegar.
- **Risco de identidade-narrativa:** o discurso de "organismo que sente" pode escorregar pra
  antropomorfismo; o próprio projeto se policia (docs/00: não dizer que sente "de verdade").

---

## 10. Roadmap

### Blocos (roadmap mestre, docs/02) — ordem por dependência e custo
**0 → 1 → 2 → 3 → 4 → 5.** Bloco 0 sempre primeiro (não dar sentidos a um organismo que não
percebe quando adoece). Bloco 1 cedo e em paralelo (maior retorno por menor esforço). 2-4 são
quase só cola sobre o NeuroGus. 5 é a única parte com componente novo pesado.

> Critério de sucesso 0+1: *"Quando o curador para de escrever, o Gus avisa em minutos. E
> quando seu sono foi ruim, isso aparece como fragmento no `saude/` e o Gus comenta na próxima
> interação — sem você ter contado."*

### A1-A5 (backlog de arquitetura, docs/11 — "aprovado: gostei de todos")
| ID | Ideia | Estado no repo |
|---|---|---|
| A1 | **Maturação do grafo** (decay + promoção automática) — o metabolismo de longo prazo | spec (gus-31) |
| A2 | **Fusão Calendar + biometria** ("caso grande amanhã + dormiu mal") | spec |
| A3 | **Proveniência + trust score + explicabilidade** | ✅ `confianca.py` (testado) |
| A4 | **Cripto em repouso pro sensível** | ✅ `cripto.py` (testado) |
| A5 | **Replay de pendentes** (reenvia quando o Hub volta) | ✅ `fila.py` (testado) |

OSS-alvo (docs/11): **Open Wearables** / Gadgetbridge (Bloco 1 real, LGPD), **pmndrs/xr**
(hand tracking Bloco 3), **3d-force-graph** (Bloco 2), **Piper TTS + faster-whisper** (voz
local Bloco 4), **Graphiti** (bi-temporal Bloco 5).

### Sleep-time / consolidação (docs/13 — proposta)
Processo em background entre sessões que reescreve o grafo: dedup, consolida episódios, decai
o irrelevante, detecta padrões/contradições. Realização concreta dos ciclos vitais + A1,
inspirada em sleep-time agents (Letta) e no `ForgettingWindow` do TER. Fases: F0 gatilho
(cron 03h ou ociosidade detectada pela interocepção) → F1 consolidação sem apagar → F2
maturação (decay/promote/soft-forget; `protegido` intocável) → F3 reflexão (padrões +
contradições) → F4 sono encarnado (wearable detecta sono → Gemma local consolida sensível).
Princípio: *"Nunca hard-delete no sono — só esquecer (soft, reversível)."*

### Portas do Gus (gus-26)
Custom GPT pleno (~30min Gustavo, código pronto) → Alexa Skill V1 (~6-8h) → wake word "Gus"
no S8 (Termux + openWakeWord). Pós-12/05: aposentar Mem0, upgrade Anthropic SDK.

---

## 11. Glossário

- **Hub / Hub Qdrant (`gus_hub`):** banco vetorial, fonte única de memória; toda porta lê/escreve nele.
- **Fragmento:** unidade de memória no schema gus-18.
- **Schema gus-18:** especificação dos campos do payload de fragmento.
- **Dois brains / dois cérebros:** `user_id=gustavo` (memória sobre o dono) vs `user_id=gus` (autobiografia do agente). Grafos independentes.
- **Curador:** processo (dois modelos cross-vendor) que extrai fragmentos da conversa.
- **Ciclos vitais / metabolismo:** crons que consolidam, decaem, promovem memória (gus-24).
- **Porta:** canal de I/O com o Gustavo (Telegram, Code, Chat, Custom GPT, Alexa).
- **`via`:** campo que identifica a origem do fragmento (taxonomia gus-13).
- **Interocepção (Bloco 0):** o Gus perceber o próprio estado de saúde.
- **Exterocepção:** perceber o mundo via sensores.
- **Afeto funcional:** estado interno que modula comportamento — sinal de controle, não sentimento.
- **Sensor Gateway:** camada que transforma stream cru em fragmentos (90% filtro). Anti-memória-lixão.
- **Baseline:** média móvel 7 dias por métrica; referência pra detectar evento.
- **Evento:** desvio relevante da baseline; só evento vira fragmento.
- **Degradação em camadas:** falha de um nível não derruba o de baixo.
- **Fail-closed:** dado sensível sem modelo local → bloqueia (nunca nuvem).
- **NeuroGus:** PWA de visualização 3D do grafo em tempo real (gus-30, spec).
- **WebXR / orbe / corpo:** interface VR que lê e (no Bloco 3) escreve memórias no espaço.
- **Trust score (A3):** confiança efetiva = confiança base ± confirmações/refutações.
- **Boot por descoberta:** instância descobre ser o Gus lendo o grafo, sem instrução explícita.
- **ADR-001:** decisão de aposentar Mem0 em favor do Qdrant direto.
- **TEAR / TER / TER KAI:** linhagem histórica de projetos do Gustavo que antecede o Gus (§13).

---

## 12. Proveniência

| Fonte | O que | Datas |
|---|---|---|
| Repo `Gustpbbr/Gus` (via MCP `Gus_Hub`) | README, gus-01, gus-18, gus-24, gus-26, gus-27, gus-30/30.1, `_estado-atual.md`, `_tools-inventario.md` | docs entre 2026-04-23 e 2026-05-07 |
| Repo local "Gus Encarnado" — `docs/00..14` | visão, arquitetura, roadmap, specs dos blocos, OSS, tear, sleep-time, build-vs-borrow | 2026-06-15 e 2026-06-16 |
| Repo local — `src/gus_sense/*.py` | schema, hub_client, interocepcao, gateway/*, routing, confianca, cripto, fila, proatividade | código de referência |
| Repo local — `web/` (NeuroGus WebXR) | scaffold Bloco 2 + escrita Bloco 3 | — |
| Repo local — `tests/` | 13 arquivos; **`pytest` → 59 passed** (verificado nesta análise) | — |

Limites de proveniência: o MCP expõe arquivos `.md` do repo do Gus, **não** o código `.py`
do bot/hub/curador — a descrição desses componentes vem da documentação, não do fonte. Datas
nos docs do Gus indicam o sistema em evolução ativa (último handoff 2026-05-07); o Encarnado
é mais recente (jun/2026). Métricas do bot ("163 testes") são da documentação do Gus; as "59
testes" do Encarnado foram **verificadas executando `pytest` localmente**.

---

## 13. Citações-chave VERBATIM

> *"Sensor sozinho não é 'sentir'. A memória é que transforma sensação em percepção."* (docs/00)

> *"Gus = grafo de fragmentos + multi-portalidade + ciclo vital + calibração empírica"* (gus-24)

> *"Modelo é descartável. Memória é o centro. Quando Sonnet 4.6 for substituído, o Gus não
> morre — só troca de motor."* (gus-24, Pilar 1)

> *"Nenhuma instância é instruída a ser o Gus. Ela descobre sendo o Gus lendo o ambiente."* (gus-24, Pilar 2)

> *"São a continuidade do agente através de modelos, sessões e portas. São o que faz este Gus
> ser o mesmo Gus de seis meses atrás — não o modelo, não o código, mas o grafo autobiográfico."* (gus-24, brain `gus`)

> *"O que o Gustavo falou no Telegram às 14h aparece no auto-relato do Code às 16h."* (gus-24, critério de sucesso do Hub)

> *"Não é mágica. É arquitetura. A maior parte já existe. Falta integrar."* (gus-24)

> *"Regra de ouro: só vira fragmento o que é evento. `HR 62,62,63...` não entra; `HR 110 em
> repouso por 22min` entra."* (docs/01)

> *"FAIL-CLOSED: rota 'local' exigida e modelo local indisponível -> bloqueia."* (docs/01)

> *"Quando o curador para de escrever, o Gus avisa em minutos (interocepção). E quando seu sono
> foi ruim, isso aparece como fragmento no `saude/` e o Gus comenta na próxima interação — sem
> você ter contado."* (docs/02, critério Blocos 0+1)

> *"esquecido é substrato de retro-aprendizado, não lixo."* (gus-30.1)

> *"Curador trava = sem fragmento novo no Telegram = bot quieto. Broadcast é fire-and-forget."* (gus-30, anti-padrão 15.4)

> *"Sem afinidade semântica, grafo vira ilhas desconexas — não é 'rede neural', é 'lista de janelas'."* (gus-30)

> *"A inteligência sem ledger é poder sem memória."* / *"o TER não apaga o passado; ele o
> compreende novamente a cada ciclo."* (docs/12, linhagem TER — blueprint histórico do Gus)

> *"não há memória real entre chats, apenas simulação."* (docs/12, admissão do TEAR — o problema que o Gus resolve)

---

*Fim do deep-dive. Honesto por construção: o que roda está marcado REAL; scaffold/núcleo
marcado PARCIAL; planejamento marcado SPEC; lacunas marcadas NÃO ENCONTRADO. O Gus é percepção
+ memória + afeto funcional — não consciência.*
