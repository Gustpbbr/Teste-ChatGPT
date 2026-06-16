# 07 — Análise de Equipes e Substituição por IA

> Quem seria necessário para construir o ecossistema completo — e quais papéis a IA já cobre hoje (Junho 2026).

---

## 👥 Equipes Completas (Cenário Máximo)

### Software & IA (3–5 pessoas)

| Papel | Skills | Custo PJ/mês (BR) |
|-------|--------|-------------------|
| Senior Backend/AI | Python, LLMs, APIs assíncronas, Anthropic/OpenAI | R$15–25K |
| ML/Data Engineer | Qdrant/Pinecone, embeddings, RAG, NLP | R$15–22K |
| Frontend/WebXR | Three.js, WebXR, VR/AR, JS/TS | R$12–18K |
| DevOps/Infra | Docker, Railway/AWS, CI/CD, monitoramento | R$10–15K (part-time) |
| QA/Testes | Testes automatizados, regressão, fail-closed | R$8–12K (part-time) |

### Hardware & Embarcados (2–4 pessoas)

| Papel | Skills | Custo PJ/mês (BR) |
|-------|--------|-------------------|
| Engenheiro Eletrônico | PCB design, componentes, sensores, atuadores | R$15–25K |
| Firmware/Embarcados | C/C++, RTOS, Linux embarcado, drivers | R$15–22K |
| Designer Industrial | CAD 3D, ergonomia, materiais, prototipagem | R$10–18K (consultoria) |
| Especialista Áudio/Óptica | Acústica, óptica, projeção, DSP | Consultor |

### Pesquisa & Publicação (1–2 pessoas)

| Papel | Skills | Custo PJ/mês (BR) |
|-------|--------|-------------------|
| Tech Lead/Arquiteto | **Você (Gustavo)** — visão, arquitetura, revisão, papers | — |
| Cientista de Dados | Estatística, metodologia, redação acadêmica | R$8–12K (part-time) |

### 💰 Total: 6–8 pessoas / R$95–150K/mês

---

## 🤖 O Que a IA Já Substitui (Junho 2026)

### 🟢 80–95% coberto — IA + 1 humano revisando

| Papel | O que IA faz | Limite |
|-------|-------------|--------|
| Backend/AI Engineer | Código Python, APIs, debug, otimização | Revisão final, deploy prod |
| ML/Data Engineer | Pipelines Qdrant, embeddings, queries vetoriais | Ajuste de thresholds |
| DevOps | Dockerfiles, CI/CD, scripts, monitoramento | Aprovar deploy, outage real |
| QA/Testes | Testes unitários, integração, borda | Priorização |
| Frontend/WebXR | Three.js, shaders, animações, UI | Teste em headset real |
| Pesquisador | Paper, gráficos, análises estatísticas | Revisão acadêmica, submissão |

### 🟡 40–60% coberto — IA escreve, hardware valida

| Papel | O que IA faz | O que não faz |
|-------|-------------|---------------|
| Firmware/Embarcados | C/C++, drivers, RTOS config | Testar na placa, debugar osciloscópio |
| Designer Industrial | Conceitos visuais, specs técnicas | CAD paramétrico preciso, teste físico |

### 🔴 Não substituível — precisa de humano com laboratório

| Papel | Por quê |
|-------|---------|
| Engenheiro Eletrônico | PCB, solda, multímetro, osciloscópio |
| Especialista Áudio/Óptica | Calibração acústica, lentes, medição |
| Prototipagem física | Impressão 3D, montagem, fiação, segurança |

---

## 💡 Cenário Realista (2026)

**Com 1 pessoa (você) + IA, é possível cobrir:**

```
✅ Backend       ─┐
✅ ML/Data       ─┤
✅ DevOps        ─┼── Claude/GPT/Codex + Gustavo revisando
✅ QA            ─┤
✅ Frontend      ─┘
⚠️  Firmware      ─── IA escreve, precisa testar em placa
⚠️  Pesquisa      ─── IA escreve paper, humano revisa e assina
❌ Eletrônica     ─── Precisa de engenheiro físico
❌ Industrial     ─── Precisa de designer com CAD + protótipo
```

**Software → viável com IA.** É 80% do valor do ecossistema.  
**Hardware → precisa de contratação.** São os 20% que exigem mãos e laboratório.

---

## ⏱️ Timeline com Equipe Completa

| Marco | Tempo |
|-------|-------|
| Gus multi-porta estável + Hub | 3–4 meses |
| Phronesis publicado | 2 meses |
| ACEE MVP (1 IL) | 3 meses |
| MASE protótipo Fase 3 | 6 meses |
| VR corpo funcional | 6 meses |
| **Ecossistema integrado** | **12–18 meses** |

---

## 🎯 Recomendação

1. **Fase 0–2 do MASE:** Faça sozinho com IA (S20 + Arduino)
2. **Software completo (Gus, Hub, Phronesis):** IA + você revisando
3. **Hardware (Fase 3+):** Considere contratar 1 engenheiro eletrônico PJ quando o software estiver maduro
4. **Patente:** Contrate advogado especializado em PI para o método de projeção emocional

**Jamais contrate time de software antes de validar com IA.** É queimar dinheiro. O Gus já provou que IA + 1 humano builda software de produção.
