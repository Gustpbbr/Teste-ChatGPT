# 03 — Inventário Completo

> Onde está cada coisa. Mapa de todos os repositórios e pastas.

---

## 📦 Repositórios GitHub (6 públicos)

### 1. `Gustpbbr/Gus` — O sistema multi-porta em produção
```
Gus/
├── gus/                    ← Bot Telegram (24/7 Railway)
│   ├── main.py             ← entry point
│   ├── bot.py              ← handlers (texto, foto, PDF, áudio, comandos)
│   ├── llm.py              ← Claude API com tool loop, retry, prompt caching
│   ├── memory.py           ← busca/salva/delete no Hub Qdrant
│   ├── tools/              ← 21 tools (web, github, memória, pubmed, arxiv...)
│   ├── handlers/           ← responder, texto, foto, documento, voz, comandos
│   ├── integrations/       ← diagnóstico, pesquisa, wikilinks, openai_chat, railway
│   ├── system_prompt.md    ← personalidade do Gus (804 linhas!)
│   └── patterns_sensiveis.py ← regex PII (fonte única)
├── hub/                    ← Hub Qdrant
│   ├── store.py            ← ingestar, lembrar, listar, deletar, auditar, stats
│   ├── curador.py          ← curador híbrido Haiku + GPT-4o-mini em paralelo
│   ├── routes.py           ← endpoints FastAPI
│   ├── schemas.py          ← validators Pydantic gus-18
│   └── vocabularios.py      ← enums canônicos (fonte única)
├── tests/                  ← 163 testes (pytest)
├── .github/workflows/      ← 16 workflows cron
├── apps-script/            ← GitHub ⇄ Google Drive sync
├── dialogos/               ← protocolo de comunicação entre portas
├── _indices/               ← MOCs por área + auditorias
├── _log/                   ← curador, retro-engine, sessões
└── pastas de conteúdo: pessoal/, dimagem/, esportes/, projetos/, ...
```

### 2. `Gustpbbr/Teste-ChatGPT` — Gus Encarnado + dossiê
```
Teste-ChatGPT/
├── src/gus_sense/          ← Blocos 0+1 (13 .py)
│   ├── schema.py           ← Fragmento gus-18
│   ├── hub_client.py       ← Cliente Hub degradável
│   ├── interocepcao.py     ← Bloco 0 (heartbeat)
│   ├── routing.py          ← Rota local fail-closed
│   ├── proatividade.py     ← Bloco 5 (núcleo)
│   └── gateway/            ← Bloco 1 (sensors, filters, pipeline)
├── web/                    ← VR frontend (Three.js/WebXR)
├── tests/                  ← 59 testes
├── docs/                   ← Specs Blocos 0–5
├── Entregavel/             ← Dossiê pra pesquisadores
└── AutoClaw/               ← ESTA PASTA — organização consolidada
```

### 3. `Gustpbbr/phronesis` — Phronesis-Bench v1
```
phronesis/
├── backend/main.py         ← API FastAPI
├── backend/corpus_*.json   ← Corpora A, BC, D, Dext
└── chat claude completo phronesis inicial.txt  ← Chat de origem
```

### 4. `Gustpbbr/phronesisfinal` — Phronesis-Bench v2
```
phronesisfinal/
├── corpus_*_public.json    ← Split público (A, BC, D, Dext, Amc, E, F, G)
├── corpus_*_final.json     ← Split privado
├── phronesis_v2 (4).html   ← Motor standalone unificado (364 linhas)
├── phronesis-tipo-*.html   ← Motores por corpus (7 HTMLs)
├── conversa gemini *.txt   ← Chats Gemini (criação dos corpora)
└── chat claude completo phronesis.txt  ← Chat Claude (927K chars)
```

### 5. `Gustpbbr/Projetos` — ACEE specs
```
Projetos/
├── Processo de Analise/ACEE/
│   ├── Cap-04/             ← Natureza e princípios arquitetônicos
│   ├── Cap-05/             ← Embodiments e plataformas
│   ├── Cap-06/             ← CMA + 9 ILs (Voz, Facial, Pupilar, etc.)
│   ├── Cap-07/             ← NCAC (núcleo cognitivo-afetivo)
│   ├── Cap-08/             ← MOR (orquestração de respostas)
│   ├── Cap-09/             ← Segurança e ética
│   ├── Transversal/        ← Índices, pendências, funcionalidades
│   └── Arquivo/            ← Compilações brutas
└── ACEE-Textos-Limpos.zip  ← Versão consolidada
```

### 6. `Gustpbbr/Organiza-o-de-projetos` — TER KAI + chats
```
Organiza-o-de-projetos/
├── TEAR Chatgtp.odt        ← O chat original (~6.5MB XML)
├── TEAR BN.odt             ← Registro Biblioteca Nacional
├── TER FULL passo para degrau 100.odt  ← TER completo (~3.7MB XML)
├── TER KAI v1 para patente - brutos/   ← J1–J12, A1–A9
├── cap 01 02 - intro e arquitetura geral.odt
├── 06 Plano Científico e de Métricas.odt
├── 07 Especificações Criptográficas.odt
├── 08 módulos e arquitetura.odt
└── + ~130 ODTs adicionais
```

---

## ☁️ Google Drive (4 pastas principais)

### Pasta 1 — Misto
- 📁 ACEE (20 arquivos)
- 📁 Criação IA (21 arquivos)
- 📁 Dispositivo (23 arquivos)
- 📁 TEAR antigo (27 arquivos)
- 📁 TER (52 arquivos)
- 📁 TER NO (30 arquivos)
- 📁 Testes app (3 arquivos)
- 📄 MASE.odt, MASEx.odt, MASEXX.odt

### Pasta 2 — Segundo Cérebro (14 arquivos)
- Índice, perfil Gustavo, manual do Claude, conexões
- Briefings: Phronesis, MGE, TER, Axon, CEX, MGX
- Análise financeira imobiliária

### Pasta 3 — Chats Brutos (27 ODTs)
- TEAR Chatgtp, TEAR BN, TEAR final
- TER 6, TER 7, TER 8, TER FULL
- TER KAI 1, 2, 98

### Pasta 4 — TEAR (9 itens)
- 📁 TEAR, 📁 Ter v6 final, + documentos

---

## 📊 Totais

| Tipo | Quantidade |
|------|-----------|
| Arquivos Python | ~104 |
| Arquivos de teste Python | ~163 |
| Documentos Markdown | ~100+ |
| ODTs (chats brutos) | ~165+ |
| HTML standalone (Phronesis/MGE/CEX) | ~10 |
| Workflows GitHub Actions | 16 |
| Ferramentas ativas (bot Gus) | 21 |
| Pastas Google Drive | 4 + 7 subpastas |

---

## 🔗 Acesso rápido

| O que | Link |
|-------|------|
| Gus (sistema) | https://github.com/Gustpbbr/Gus |
| Gus Encarnado | https://github.com/Gustpbbr/Teste-ChatGPT |
| Phronesis v1 | https://github.com/Gustpbbr/phronesis |
| Phronesis v2 | https://github.com/Gustpbbr/phronesisfinal |
| Projetos (ACEE) | https://github.com/Gustpbbr/Projetos |
| Organização (TER KAI) | https://github.com/Gustpbbr/Organiza-o-de-projetos |
