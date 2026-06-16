# 00 — Visão Geral do Ecossistema

## O que é

Um corpo de pesquisa de P&D sobre **IA pessoal centrada em memória, percepção afetiva e raciocínio prudente**, construído por Gustavo Pratti de Barros (anestesiologista, pesquisador independente) ao longo de 2025–2026, em conversa com múltiplas IAs.

## A tese central

> **A memória é o centro; o modelo é descartável.** Uma IA pessoal útil precisa de uma identidade que persiste num grafo externo, percebe o usuário, raciocina de forma prudente e auditável, e age por múltiplos canais.

Formulada em 2025, convergente com a direção do campo em 2026 (Letta, Mem0, Zep/Graphiti).

## O organismo (13 projetos = 1 sistema)

```
                  ⚖️ CONSCIÊNCIA / PRUDÊNCIA
              TER (filosofia) → TER KAI (middleware) ⇄ Phronesis (mede)
                            ▲
   👁️ SENTIDOS ───►  🧠 MEMÓRIA (centro)  ◄─── 🖐️ CORPO
   ACEE / MASE        TEAR·TER·Gus              Gus (VR) / MASE
                            ▲
                  ⚙️ AGÊNCIA / ORQUESTRAÇÃO
              MGE (gera) → CEX (delibera) → MEX (executa)
              orquestrados por MGX (humano no loop) · Axon (automação)
```

## As três camadas

| Camada | Projetos | Função |
|--------|----------|--------|
| **Alma (Memória)** | TEAR → TER → Gus | Grafo de memória persistente multi-porta |
| **Sentidos (Percepção)** | ACEE, MASE, Sensor Gateway | Sensores viram percepção contextualizada |
| **Corpo (Ação)** | Gus VR/NeuroGus, MGE, CEX, MGX, Axon | Interface espacial + geração + deliberação + execução |
| **Consciência (Governança)** | TER KAI, Phronesis-Bench | Middleware prudencial + métricas de avaliação |

## Principais princípios

1. **Degradação em camadas** — falha de um nível nunca derruba o de baixo
2. **Rota local pra dado sensível** — biometria/Dimagem nunca vão pra nuvem (fail-closed)
3. **Anti-memória-lixão** — só vira fragmento o que é evento, nunca leitura crua
4. **Calibração empírica** — cada feature entra no estado mais simples; ajusta com dado
5. **Boot por descoberta** — uma instância "vira Gus" lendo a própria história, não por instrução

## O que realmente funciona hoje

- ✅ **Gus multi-porta** — bot Telegram 24/7, Hub Qdrant, curador híbrido, 21 tools
- ✅ **Phronesis-Bench v1 + v2** — API FastAPI + HTML standalone, corpora A–G
- ✅ **MGE** — HTML standalone com 10 agentes de geração criativa
- ✅ **CEX v1.1** — HTML standalone com 11 etapas de deliberação adversarial

## O que é spec (não implementado)

- 📄 ACEE (IA afetiva embarcada)
- 📄 TER KAI (middleware de governança)
- 📄 MGX (orquestração MGE+CEX+MEX)
- 📄 Axon (automação contextual)
- 📄 MEX (motor de execução)

## Onde está tudo

| Local | Conteúdo |
|-------|----------|
| `Gustpbbr/Gus` | Sistema multi-porta em produção |
| `Gustpbbr/Teste-ChatGPT` | Gus Encarnado + dossiê Entregavel |
| `Gustpbbr/phronesis` | Phronesis-Bench v1 (API) |
| `Gustpbbr/phronesisfinal` | Phronesis-Bench v2 (HTML + corpora G) |
| `Gustpbbr/Projetos` | ACEE specs (46 MDs) |
| `Gustpbbr/Organiza-o-de-projetos` | TER/TER KAI ODTs (138) |
| Google Drive (4 pastas) | Chats brutos + Segundo Cérebro + subpastas |
