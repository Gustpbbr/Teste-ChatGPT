# FAQ do Pesquisador

> Respostas diretas às perguntas mais prováveis. (Estende o `CLAUDE.md`, que instrui a IA-guia.)

**O que aqui realmente funciona (roda)?**
Phronesis-Bench (+ resultados preliminares), MGE (HTML standalone + n8n), CEP v3.9 (n8n), CEX v1.1
(HTML), e o Gus parcial (bot Telegram + Hub Qdrant + `gus_sense` com testes). O resto é spec rica.
Ver `MATRIZ-DE-MATURIDADE.md`.

**Isso já existe no mercado?**
As peças sim (memória: Letta/Mem0/Zep; afeto: Hume; guardrails: NeMo/Lakera; multiagente:
CrewAI/AutoGen). O **organismo integrado** (memória + prudência + afeto + local + médico) **não**
existe como produto único. Ver `01-visao-geral.md` e `03-mapa-do-ecossistema.md`.

**Qual a parte mais publicável / defensável?**
1) O **achado do Phronesis**: modelos de fronteira **perdem prudência quando se identificam como
IA** (G3' < G3) — efeito do RLHF; e M2 (saber o que não sabe) é o ponto fraco. 2) A combinação
**prudência mensurável + memória persistente**. 3) O **ângulo clínico** (decisão sob incerteza).

**As métricas grandiosas são reais?**
Não — números como ECI≈0.94, latências 60/150ms são **metas de projeto**. A exceção são os
resultados do Phronesis (medições preliminares, 2 modelos, com caveats de instrumentação).

**Por que tantos projetos?**
São a mesma intuição rederivada por ângulos diferentes (memória, prudência, percepção). O valor
está em **convergir** num organismo (Gus) — ver `04-o-que-falta-para-unificar.md`.

**Posso pegar só o benchmark (Phronesis)?**
Sim — licença aberta. É a peça mais autônoma e a âncora científica. `projetos/phronesis-bench/`.

**Como rodo algo?**
Phronesis: backend FastAPI (`/run` com chave de API). MGE/CEX: HTML standalone que chama a API
Anthropic direto do browser. Ver os respectivos `deep-dive.md`.

**Qual o estado do "produto único" (Gus)?**
Embrião: tem o kernel parcial (Hub + schema gus-18 + multi-porta). Falta o tecido conjuntivo
(contrato comum + adaptadores por projeto + governança transversal). Roadmap em `04-o-que-falta-para-unificar.md`.

**Qual a licença? O que o autor quer?**
Aberta (MIT código / CC BY docs), com atribuição. O autor quer **ceder para alguém levar adiante**;
colaboração é bem-vinda, não exigida. Mesmo um feedback curto ajuda.

**Foi construído por quem? Posso confiar nos detalhes?**
Por um médico-pesquisador **não-programador**, via conversa com IAs. Trate os detalhes com o
ceticismo adequado — cada `deep-dive.md` traz citações verbatim e marca `NÃO ENCONTRADO`.
Ver `METODOLOGIA-E-PROVENIENCIA.md`.
