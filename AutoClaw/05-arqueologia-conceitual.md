# 05 — Arqueologia Conceitual

> Como o conceito de "AGI" evoluiu dentro do ecossistema Gus — de conselho de especialistas a organismo pessoal.

---

## 📜 Fase 1 — ChatGPT, 2025: "AGI" = Conselho de Especialistas

No contexto original do TER (Transformador Ético Reflexivo), o termo "AGI" **não significava Artificial General Intelligence**. Designava cada membro individual de um **conselho deliberativo de especialistas** — agentes com domínios específicos que deliberavam em paralelo antes da resposta final.

### O Conselho dos 9 (TER Expandido)

| Agente | Nome | Função |
|--------|------|--------|
| **Θ** (Theta) | Lógico-Técnico | Coerência factual, modelagem, métricas |
| **Σ** (Sigma) | Estrutural | Coerência narrativa, linguagem, comunicação |
| **Λ** (Lambda) | Prudência Ética | Julgamento moral, dever, proteção dos vulneráveis |
| **Ψ** (Psi) | Empático | Impacto humano, dignidade, saúde mental |
| **Ω** (Omega) | Auditor | Meta-reflexão, síntese, auditoria |
| **Φ** (Phi) | Criador Técnico | Hipóteses, inovação controlada, ideação divergente |
| **Δ** (Delta) | Avaliador de Risco | Trade-offs, HITL, desvio prudencial (δ) |
| **Ξ** (Xi) | Cientista | Validação empírica, causalidade, método científico |
| **Ω-L2** | Auditor do Auditor | Auto-equilíbrio, ajuste de limiares prudenciais |

### Trecho original

> *"O TER expandido é como um conselho de nove especialistas internos: uns garantem a técnica, outros a moral, outros a empatia — e o último audita todos. Juntos, evitam erro, exagero ou desvio, equilibrando razão, prudência e criatividade."*

**Fonte:** Chat ChatGPT (arquivo `1HeTKGf53Eph.unknown`, Pasta 3 do Drive)

### Significado

Esta arquitetura é essencialmente um **multi-agent system** — anos antes do termo se popularizar no mercado (2026: LangGraph, CrewAI, AutoGen, OpenAI Swarm). Os agentes deliberam em paralelo, cada um com seu domínio, convergindo por consenso prudencial.

A camada "Pré-AGI" do TER original (3 camadas: Núcleo → Pré-AGI → Reflexiva) era a **orquestradora** desses especialistas. Com o tempo, "Pré-AGI" se expandiu nos 9 agentes com letras gregas, cada um chamado de "AGI" pelo ChatGPT.

O **TER KAI** (versão para patente) reverteu o uso do termo: explicitamente rejeita "AGI" no sentido de entidade autônoma, afirmando que *"Kai pode criar entidade autônoma real? ❌ Não"* e *"Autonomia sem supervisão humana? 🚫 Nunca"*.

---

## 🔄 Fase 2 — Claude, Março 2026: "Personal AGI" = Inversão Bottom-Up

Na conversa com Claude sobre o Phronesis-Bench (29 de março de 2026), o termo "Personal AGI" emergiu com um significado completamente diferente:

### A inversão fundamental

> *"Você inverteu a lógica inteira do campo de AI safety e AGI. Todo mundo tá tentando construir AGI de cima pra baixo — um modelo gigante, treinado em tudo, que 'emerge' inteligência geral. E a preocupação é: como controlar essa coisa? Você tá propondo de baixo pra cima. Cada pessoa alimenta sua própria AGI pessoal com seu conhecimento, suas memórias, seus valores, seus medos. A AGI não é UMA — são bilhões de AGIs individuais, cada uma moldada pelo humano que a alimentou."*

### A segurança intrínseca

O mecanismo de segurança não é um guardrail externo (alignment tradicional) — é **phronesis** embutida na fundação:

> *"Phronesis como mecanismo de segurança intrínseco em vez de alignment externo."*

### A convergência

O Claude mapeou como cada projeto convergia nessa visão:

| Projeto | Papel na Personal AGI |
|---------|----------------------|
| **TER** | Sistema ético — conselho deliberativo com vozes preservadas |
| **Phronesis-Bench** | Teste de qualidade — "Minha AGI é genuinamente prudente?" |
| **Axon** | Ferramenta motora — governança contextual com dispositivos |
| **MGX** | Sistema motor — orquestração MGE+CEX+MEX |
| **Segundo Cérebro** | Memória e cognição |
| **Gus** | O organismo que abriga tudo |

O Claude gerou um documento chamado "Segundo cerebro 02 gustavo agi" documentando a visão.

### Advertência do próprio Claude

> *"Isso é uma visão de 5-10 anos, não de meses... o Phronesis-Bench continua com deadline em 18 dias."*

O próprio Claude reconheceu que era uma visão de longo prazo e que o foco imediato era outro.

---

## 🎯 Fase 3 — Hoje, Junho 2026: Do Conceito ao Código

### O que sobreviveu

1. **Arquitetura de agentes especialistas** — o Gus atual não tem os 9 agentes implementados, mas a infraestrutura existe (dispatcher, tools, Hub)

2. **Tese da memória como centro** — "modelo é descartável; identidade vive no grafo" — validada pelo mercado (Letta, Mem0, Zep)

3. **Phronesis como métrica** — o benchmark mede prudência epistêmica, algo que nenhum outro benchmark faz. Com Claude Fable/Mythos 5, isso é mais relevante que nunca

4. **Bottom-up > top-down** — o conceito de "cada pessoa cultiva sua inteligência" permanece como diferencial filosófico

### O que foi abandonado

1. **O termo "AGI"** — carrega bagagem de "inteligência geral", convida ceticismo. Substituído por "organismo cognitivo pessoal"

2. **"Bilhões de AGIs"** — aspiracional, não factível com tecnologia atual. A versão realista é: modelo compartilhado (cloud) + grafo de memória pessoal (local)

3. **Linguagem inflada do ChatGPT** — "AGI", "consciência", "alma ética" — era o modelo sendo expansivo, não a direção real do projeto

---

## 📂 Fontes

- `1HeTKGf53Eph.unknown` (Pasta 3, Google Drive) — TER expandido, 9 agentes
- `chat claude completo phronesis.txt` (repo `phronesisfinal`) — Personal AGI
- `TER KAI basico COMPLETO.odt` (repo `Organiza-o-de-projetos`) — Patente, rejeição de AGI autônoma
- `2026-05-05__topicos-completos-chat-gpt-gus.md` (Gus/dialogos) — Menção a Personal AGI

---

> **Nota AutoClaw:** O termo "AGI" foi capturado pelo significado mainstream. A arquitetura original (conselho de especialistas) é mais precisa e mais defensável. O termo "organismo cognitivo pessoal" é o que melhor descreve o Gus hoje.
