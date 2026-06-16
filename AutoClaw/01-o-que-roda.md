# 01 — O Que Roda (Código Funcional)

> Matriz de maturidade real — separando o que é código verificado do que é especificação.

---

## 🟢 Funcional / Em Produção

| Projeto | O que é | Evidência | Stack |
|---------|---------|-----------|-------|
| **Gus** | Bot Telegram multi-porta | 24/7 no Railway, 21 tools, Hub Qdrant, curador híbrido | Python, Qdrant, Anthropic API, OpenAI API |
| **Gus Encarnado** | Blocos 0+1 (interocepção + gateway) | ~59 testes verdes em `src/gus_sense/` | Python 3.11+ |
| **Phronesis-Bench v1** | API FastAPI de benchmark | corpora A–D, métricas ACC/ECE/CS/RAS→PPS | Python, FastAPI |
| **Phronesis-Bench v2** | Motor standalone HTML | corpora A–G, 8 motores HTML, resultados Claude vs GPT-4o | HTML/JS, Anthropic API |
| **MGE v2.1** | Motor de Geração Estruturada | HTML standalone, 10 agentes, transplante estrutural | HTML/JS, Anthropic API |
| **CEX v1.1** | Comitê de Especialistas Universais | HTML standalone, 11 etapas, cross-examination | HTML/JS, Anthropic API |
| **CEP v3.9** | Comitê de Especialistas Prudentes | Workflow n8n, 21 nós, código auditado | n8n, JavaScript |

---

## 🟡 Parcial / Scaffold

| Projeto | O que tem | O que falta |
|---------|-----------|-------------|
| **Gus VR (NeuroGus)** | Three.js/WebXR com mock data | Headset Quest, Hub real, hand tracking |
| **Gus Bloco 2** | Scaffold de leitura VR (`web/`) | Ligar no Hub real (`/hub/recent`) |
| **Gus Bloco 3** | Router fail-closed + funções de escrita | Hand tracking, servidor Gemma |
| **Gus Bloco 5** | Núcleo de proatividade testável | Render espacial no VR |

---

## 📄 Especificação (sem código verificado)

| Projeto | Tipo de spec | Volume |
|---------|-------------|--------|
| **ACEE** | IA afetiva embarcada | 9 ILs, CMA→NCAC→MOR, 46 MDs |
| **MASE** | Sistema efetor/físico | 3 ODTs (existente no Drive, não indexado antes) |
| **TER KAI** | Middleware de governança | 7 módulos, δψρω, PoP-L, rascunho patente |
| **TER** | Framework filosófico | Chats densos, spec de arquitetura |
| **MGX** | Orquestração MGE+CEX+MEX | Conceito + design de fases |
| **Axon** | Automação contextual | Blueprint + crítica multi-especialista |
| **MEX** | Motor de Execução | Conceitual |

---

## 🧪 Cobertura de Testes

| Projeto | Testes |
|---------|--------|
| **Gus** (bot + hub) | ~163 testes (pytest) |
| **Gus Encarnado** | ~59 testes (8 arquivos) |
| **Phronesis-Bench** | Testado manualmente com Claude + GPT-4o |

---

## ⚠️ Pré-requisitos pra rodar

| Projeto | Precisa de |
|---------|-----------|
| Gus (bot) | Railway, Qdrant Cloud, Anthropic API key, OpenAI API key, Telegram Bot Token |
| Gus Encarnado | Python 3.11, Hub Qdrant (ou mock) |
| Phronesis | Anthropic API key (motor HTML) ou OpenAI/Anthropic (API) |
| MGE / CEX | Anthropic API key (roda no navegador) |
| ACEE / TER KAI | Nada — é spec, não código |
