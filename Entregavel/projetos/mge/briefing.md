# MGE — Motor de Geração Estruturada · briefing

> 🟢 **Estado: FUNCIONAL** (HTML standalone + n8n v3.0). O projeto mais "pronto pra usar".
> Detalhe técnico completo em [`deep-dive.md`](deep-dive.md).

## O que é
Um pipeline multiagente de **geração criativa estruturada** (10 agentes em sequência). Em vez
de pedir ideias a um LLM, obriga o processo a passar por **estágios cognitivos distintos**.

## A tese
*"Criatividade de alto valor não vem de liberdade total — vem de restrições bem colocadas
combinadas com exploração guiada."* O LLM sozinho gravita pro óbvio; a estrutura combate isso.

## Como funciona
**Divergência** (Reformulador → Mapeador de Domínios + Expansor → Transgressor + Combinador) →
**Membrana de Novidade** (filtra por novidade real) → **Convergência** (Construtor → Avaliador
→ Mapa de Combinações → Verificador). Mecanismos centrais: **transplante estrutural** de domínios
distantes + **inversão calibrada de premissas**. **Nunca escolhe um vencedor** — entrega um
portfólio e deixa o julgamento ao usuário.

## Por que importa
- Diferente do mercado multiagente (CrewAI/AutoGen, que automatizam tirando o humano), aqui o
  **humano é o juiz final** e o processo é totalmente rastreável.
- Já **funciona** (standalone + n8n) e resolve um problema real (explorar espaços de solução).

## Limitações honestas
- A Membrana avalia "novidade" com um modelo treinado no existente (contradição estrutural).
- Qualidade depende do Haiku seguir instrução estrutural complexa.
- API key exposta no browser no standalone (ok p/ uso pessoal; precisa proxy p/ público).

**Fonte:** `Segundo Cérebro/MGE` (Documentação Completa v3.0, Arquitetura v1.0, HTML, n8n JSON).
