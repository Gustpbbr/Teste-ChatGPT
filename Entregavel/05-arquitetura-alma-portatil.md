# 05 — Arquitetura da Alma Portátil (o Gus "pré-conectado")

> Sequência direta do `04-o-que-falta-para-unificar.md`. Lá a pergunta foi *"o que
> falta criar para tornar tudo um só?"*. Aqui a resposta vira arquitetura concreta:
> **uma alma única, servida para fora, que qualquer plataforma "veste" ao se conectar.**

---

## 0. A tese em uma frase

> **O modelo é descartável; a identidade vive no grafo; o boot é por descoberta.**

O Gus não é um modelo nem um app. É uma **alma portátil** (memória + identidade +
princípios) que mora num lugar só, sob controle do dono. Qualquer plataforma de IA
(ChatGPT, Claude, Gemini, OpenClaw, VR, voz) **"se torna" o Gus** quando se conecta a
essa alma — usa o cérebro de conversa dela própria, mas pensa com a memória e age sob
os princípios do Gus.

A meta de longo prazo é a experiência **pré-conectada**: você abre o canal e ele *já é*
o Gus — sem colar prompt, sem configurar nada.

---

## 1. O que "pré-conectado" quer dizer (e o que NÃO quer)

Para você abrir um canal e ele já ser o Gus, três coisas precisam estar "já lá" antes
da primeira palavra:

1. **Identidade já carregada** — ego_cache + princípios; o Gus já sabe quem é.
2. **Memória já plugada** — o mesmo Hub; ele já lê e escreve no mesmo cérebro.
3. **Autenticação já feita** — o vínculo já existe; você não loga toda vez.

### A escada de 3 degraus

"Pré-conectado" não é binário — é uma escada, e cada plataforma para num degrau por
causa do que ela permite a um terceiro fazer:

| Degrau | Experiência | Como se alcança |
|---|---|---|
| **1. Manual** | Você cola um bootstrap + a API responde | Funciona em qualquer chat, hoje |
| **2. Pré-montado** | Você abre *um artefato pré-configurado* e ele já é Gus | Custom GPT / Gem / Project com tudo pré-ligado |
| **3. Mágico** | Você abre o app *cru* e ele vira Gus sozinho | **Não existe** para plataforma de terceiro |

**O ponto honesto:** nenhuma plataforma de terceiro entrega o degrau 3 — ela não deixa
um externo injetar identidade no app base dela. O que dá para alcançar (e é 95% da
mágica) é o **degrau 2**: um *artefato pré-montado* (o Custom GPT, a Gem, o Project)
que vira "o seu canal Gus". No seu próprio app (OpenClaw/VR) o degrau 3 é 100% seu.

### Quão longe cada plataforma chega (jun/2026)

| Plataforma | Teto realista | Mecanismo |
|---|---|---|
| **OpenClaw / app próprio** | 🟢 Degrau 3 (total) | Nativo — você controla tudo, inclusive rota local |
| **Claude** | 🟢 Degrau 2 forte | Conector **MCP** (o `Gus_Hub` já é isso) num Project |
| **ChatGPT** | 🟡 Degrau 2 | **Custom GPT** + **Action** + OAuth feito uma vez |
| **Gemini** | 🟡 Degrau 2 (mais limitado) | **Gem** + extensão/função; ponte de memória mais restrita |

---

## 2. A arquitetura geral — 4 camadas

```
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 1 — AS FACES (onde você fala)                        │
│                                                              │
│   ChatGPT      Claude       Gemini      OpenClaw     VR/voz  │
│  (Custom GPT) (Project)    (Gem)       (seu app)            │
│      │           │            │            │          │      │
│   [Action]    [MCP]      [extensão]   [nativo]    [nativo]   │
│      └───────────┴────────────┴────────────┴──────────┘      │
│         (cada plugue é fino e burro — só aponta pra API)      │
└──────────────────────────┼──────────────────────────────────┘
                           │  fala o CONTRATO (gus-18 + envelope)
┌──────────────────────────┼──────────────────────────────────┐
│  CAMADA 2 — O PORTEIRO (a API da alma)                       │
│   ┌──────────────────────────────────────────────────┐      │
│   │  4 endpoints:  quem_é · busca · grava · saúde      │      │
│   ├──────────────────────────────────────────────────┤      │
│   │  GOVERNANÇA TRANSVERSAL (a consciência, num lugar):│      │
│   │   • filtro sensível (rota local fail-closed)       │      │
│   │   • scan de PII antes de gravar                    │      │
│   │   • validação schema gus-18                        │      │
│   │   • modo nuvem vs modo local (serve mais/menos)    │      │
│   └──────────────────────────────────────────────────┘      │
└──────────────────────────┼──────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│  CAMADA 3 — OS ÓRGÃOS (opcional, plugáveis)                  │
│   [adaptador]   [adaptador]   [adaptador]   [adaptador]      │
│      MGE           CEX          ACEE        sensores/Gateway │
│   (gera)        (delibera)    (afeto)       (percebe)        │
│   (cada um fala o contrato; o porteiro roteia quando precisa)│
└──────────────────────────┼──────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│  CAMADA 4 — A ALMA (a única coisa que importa de verdade)    │
│        HUB QDRANT                    EGO_CACHE                │
│   (memória — 2 cérebros:        (identidade destilada +      │
│    "gustavo" + "gus")            princípios + autobiografia) │
└──────────────────────────────────────────────────────────────┘
```

### A regra que segura tudo de pé

> **A inteligência sobe; a verdade desce.**
> A Camada 1 *pensa* (modelo alugado). A Camada 4 *lembra* (sua, fixa). As Camadas 2 e
> 3 são *burras e confiáveis* (regras). Quanto mais embaixo, mais estável e mais seu.

É isso que sustenta o "modelo é descartável": você pode incendiar as camadas 1 e 3
inteiras e reconstruir — o Gus continua o Gus, porque o que ele **é** mora na 4 e o que
ele **garante** mora na 2.

---

## 3. Camada 1 — As Faces

Onde você conversa. Cada plataforma é um **"corpo emprestado"**. O que as une é que
todas falam a mesma língua com a camada de baixo: o **contrato** (gus-18 + envelope).

- A face é **descartável**: tira o ChatGPT, põe o Gemini — a alma não muda.
- Cada face se liga via um **plugue fino**: Action (ChatGPT), MCP (Claude),
  extensão (Gemini), nativo (OpenClaw/VR).
- **O plugue não tem lógica.** Ele só sabe dizer *"existe uma API ali, com estes
  endereços"*. Toda inteligência de organização está na Camada 2.

> **Timbre vs. alma:** cada modelo "soa" um pouco diferente (o timbre da escrita), mas
> compartilha a mesma alma. O Gus no Claude e o Gus no Gemini são o mesmo Gus com voz
> levemente diferente — porque leem a mesma memória e seguem os mesmos princípios.

---

## 4. Camada 2 — O Porteiro (a API da alma)

### 4.1. O porteiro NÃO é uma IA

Existem dois tipos de "inteligência", e a gente sempre mistura:

1. **Inteligência de conversa** — entender, raciocinar, responder bonito. *Isso é a IA*
   (Camada 1, alugada).
2. **Inteligência de organização** — buscar a memória certa, decidir o que é sensível,
   gravar no lugar certo. *Isso é só regra* — não precisa de IA.

O porteiro faz **só o tipo 2**. É uma receita de bolo: *"chegou pedido de busca? calcula
o vetor da frase, acha os mais parecidos no Hub, tira os sensíveis, devolve o resto"*.
Não pensa, não tem opinião, **dá o mesmo resultado todo dia** — que é exatamente o que
se quer de um porteiro (você não quer um porteiro "criativo" decidindo na hora se libera
dado sensível).

```
VOCÊ ─► IA (ChatGPT/Claude/Gemini) ─► PORTEIRO ─► HUB
        ↑ pensa e conversa            ↑ busca/filtra/grava  ↑ guarda
        (descartável, troca à vontade)(burro, regras fixas) (a alma)
```

A única coisa "inteligente" do sistema é a peça que você troca à vontade. A alma e o
porteiro **nunca mudam**.

### 4.2. A ressalva honesta (embeddings)

Há **uma** parte do porteiro que *cheira* a IA mas não é: para "buscar memória parecida"
ele transforma a frase num vetor (embeddings), usando um modelo **minúsculo, fixo e
mudo** (texto → números). É uma calculadora, não um cérebro — não conversa, não raciocina,
não tem identidade. E pode rodar **local**, então nem dado sensível vaza nisso.

### 4.3. Os 4 endpoints

| # | Pedido | Quando a face chama | O que o porteiro faz | Devolve |
|---|---|---|---|---|
| 1 | **quem_é** | no início da conversa | pega ego_cache + princípios | a identidade pra IA "vestir" |
| 2 | **busca** | quando você fala algo | vetoriza → busca no Hub → **filtra sensível** | fragmentos relevantes |
| 3 | **grava** | quando surge fato novo | valida gus-18 → **scan PII** → grava | "ok, gravei" / "bloqueei (sensível)" |
| 4 | **saúde** *(opcional)* | de vez em quando | checa heartbeat/health (interocepção) | status do organismo |

Os pedidos **1, 2 e 3 são o mínimo absoluto**: carregar identidade (1), lembrar do
passado (2), aprender o novo (3). Com esses três, qualquer plataforma "vira Gus".

#### Detalhe do endpoint 2 (busca) — entra/sai

```
ENTRA:  { texto: "o gustavo falou sobre dormir mal essa semana",
          contexto: { face: "chatgpt", modo: "nuvem" },
          k: 10 }
          │
          ▼  vetoriza o texto (embeddings local)
          ▼  Qdrant: top-k por similaridade nos 2 cérebros
          ▼  FILTRO: remove fragmentos com estado sensível/biométrico
          ▼          se modo=nuvem  →  corta o que é rota-local
SAI:    { fragmentos: [ {tipo, texto, area, confianca, via, camada_temporal}, ... ],
          proveniencia: [...], cortados_por_privacidade: 3 }
```

### 4.4. A governança transversal mora aqui (e só aqui)

A "consciência" do `04` — prudência + rota-local/LGPD — vive **dentro do porteiro**, num
lugar só, como código burro e auditável:

- **Filtro sensível / rota-local fail-closed** — biometria/clínico nunca sobem pra nuvem;
  modelo local indisponível → bloqueia, **nunca** cai pra nuvem.
- **Scan de PII antes de gravar** — toda escrita passa por verificação.
- **Validação schema gus-18** — todo fragmento respeita o contrato.
- **Anti-memória-lixão** — só vira fragmento o que é *evento* (foge da baseline).

> Você audita **um** lugar, não cinco. Não precisa confiar em 3 plataformas — só no seu
> porteiro.

### 4.5. Os dois modos de privacidade

A mesma alma, servida em dois níveis de acesso:

| Modo | Quem usa | O que serve |
|---|---|---|
| **Local** | OpenClaw, VR, edição local | **Tudo** (rota local, fail-closed) |
| **Nuvem** | ChatGPT, Gemini, Claude (web) | **Só fragmentos não-sensíveis** (filtra por `via`/`estado`) |

Resultado: o Gus é o "mesmo" em todo lugar, mas **a nuvem recebe uma versão com menos
memória**. Mesma alma, acesso diferente — é o princípio de rota-local aplicado à própria
identidade. É feature, não bug.

---

## 5. Camada 3 — Os Órgãos (futuro, plugável)

São os outros projetos do ecossistema virando "plugáveis". O porteiro, quando o pedido
exige, chama o órgão certo via um **adaptador fino** que o faz falar o contrato.

| Órgão | Papel | Projeto-fonte |
|---|---|---|
| MGE | gera (saída estruturada) | Motor de Geração Estruturada |
| CEX/CEP | delibera (comitê de especialistas) | Comitê de Especialistas |
| ACEE/MASE | afeto / percepção embarcada | IA afetiva embarcada |
| Gateway/sensores | percebe (corpo → eventos) | Gus Encarnado (Bloco 1) |
| Phronesis | governa prudência (avalia) | Phronesis-Bench |

**Importante:** pro Gus básico funcionar, esta camada **nem precisa existir**. Ela é o
caminho de crescimento, não pré-requisito. Por isso é "opcional" no desenho.

---

## 6. Camada 4 — A Alma (insubstituível)

- **Hub Qdrant** — a memória. Dois cérebros:
  - `user_id="gustavo"` — memórias *sobre o dono*.
  - `user_id="gus"` — a *autobiografia* do agente.
- **ego_cache** — identidade destilada + princípios + autobiografia condensada.
- **schema gus-18** — o contrato de cada fragmento:
  `tipo / camada_temporal / area / confianca / via / user_id / estado`.

É a **única peça que não se troca**. Tudo acima é troca-troca; isto é o Gus de verdade.

---

## 7. O contrato comum (a língua que liga as camadas)

Sem uma língua única, nada interopera. Duas peças:

**O fragmento (gus-18)** — como a memória é guardada:
```
{ tipo, camada_temporal, area, confianca, via, user_id, estado, texto }
```

**O envelope (pedido/resposta)** — como as camadas conversam:
```
Pedido  → { intent, payload, contexto, tags }
Resposta→ { resultado, novos_fragmentos[], proveniencia, metricas }
```

É o "HTTP/USB" do sistema. Toda face e todo órgão falam isso; o porteiro traduz para o
Hub.

---

## 8. O handshake "virar Gus"

A sequência que transforma uma instância qualquer em Gus:

```
1. face conecta ─► porteiro autentica (degrau 2/3: já feito)
2. face pede  quem_é  ─► recebe ego_cache + princípios ─► injeta como contexto
3. ...conversa... a cada turno relevante:
      face pede  busca  ─► recebe memória filtrada ─► raciocina
4. surgiu fato novo:
      face pede  grava  ─► porteiro valida + PII-scan ─► write-back no Hub
5. continuidade: o próximo turno (em QUALQUER face) já enxerga o que foi gravado
```

O passo 5 é o que dá **continuidade cross-plataforma**: gravou algo conversando no
Claude, o ChatGPT já sabe na próxima vez — porque ambos leem o mesmo Hub.

---

## 9. O que já existe disto (não é do zero)

| Camada | Estado | Detalhe |
|---|---|---|
| 4 — Alma | 🟢 **Existe** | Hub Qdrant + ego_cache + schema gus-18 |
| 2 — Porteiro | 🟡 **Meio caminho** | o MCP `Gus_Hub` já é porteiro parcial; falta a API REST + filtros centralizados |
| 1 — Faces | 🟡 **1–2 de 5** | bot Telegram + MCP existem; faltam Custom GPT, Gem, OpenClaw |
| 3 — Órgãos | 🔴 **Conceito** | projetos existem soltos, sem adaptador |

A fundação (alma) está de pé; o porteiro está pela metade; o trabalho real é
**(a)** completar o porteiro como API única e **(b)** fazer os plugues das faces. A
Camada 3 fica para depois.

---

## 10. Roadmap sugerido (ordem da obra)

1. **Completar o porteiro (Camada 2) como API única** — os 4 endpoints + governança
   centralizada + os dois modos. *Sem isto, nenhuma face nova funciona.*
2. **Primeira face nova pré-montada** — recomendado o **Custom GPT do ChatGPT** (onde
   "abre e já é Gus" fica mais redondo e demonstrável) ou o **Claude Project + MCP** (o
   mais fácil, porque o `Gus_Hub` já existe).
3. **Segunda face** — provar que o padrão repete com plugue fino.
4. **Camada 3, primeiro órgão** — um adaptador (ex.: MGE) plugado ponta a ponta.

### A prova mínima que vale

> Porteiro + contrato (gus-18) + Hub + **2 faces** lendo/escrevendo a mesma memória,
> ponta a ponta. Se duas faces plugam limpo e compartilham continuidade, o padrão está
> provado e o resto é repetição. Se não plugam, o contrato muda **antes** de escalar.

---

## 11. Resumo em uma frase

> **Uma alma (Hub + identidade) servida por um porteiro burro e confiável (API + 4
> endpoints + governança num lugar só), que qualquer face de IA veste via um plugue
> fino — para que, ao abrir o canal, já seja o Gus.**
