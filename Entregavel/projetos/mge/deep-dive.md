# MGE — Motor de Geração Estruturada · Deep-Dive Técnico

> 🟢 **Estado: FUNCIONAL** (HTML standalone + workflow n8n v3.0). O projeto mais "pronto pra
> usar" do portfólio.
> Fontes: `MGE_Documentacao_Completa.docx` (v3.0, 21/03/2026), `MGE_Arquitetura_v1.0.docx`,
> `mge-00-briefing.md`. Código: HTML standalone (API Anthropic direto do browser) + JSON n8n.

---

## 1. Tese e problema

**Problema:** modelos de linguagem treinados no conhecimento existente **gravitam para o
centro da distribuição** — geram o que já foi pensado, documentado e validado. Pedir "ideias
novas" direto a um LLM produz o óbvio.

**Tese:** *"Criatividade de alto valor não vem de liberdade total — vem de **restrições bem
colocadas combinadas com exploração guiada** em territórios não óbvios."* O MGE combate o
viés do LLM **através de estrutura, não de liberdade**: obriga o processo criativo a passar
por **estágios cognitivos distintos e sequenciais**, cada um com função e critério próprios.

**Saída:** não uma ideia "vencedora", mas um **portfólio de conceitos** com avaliações
independentes, mapa de relações entre eles e análise de coerência. *O sistema nunca escolhe
um vencedor — apresenta o conjunto e deixa o julgamento ao usuário.*

## 2. Princípios de design

1. **Divergência antes de convergência** — duas fases separadas por uma "membrana" de filtragem.
2. **Cruzamento de domínios como mecanismo central** — não mistura temática, **transplante
   estrutural** (extrair o mecanismo de um campo distante e aplicá-lo).
3. **Inversão de premissas** calibrada pelo nível de radicalidade.
4. **Novidade como critério de filtragem** (não qualidade, não viabilidade).
5. **Pesos de avaliação dinâmicos** por nível de radicalidade.
6. **Portfólio em vez de vencedor** (o "Diretor" foi removido na v2.0 — ver §6).
7. **Transparência total** — cada decisão de cada agente fica registrada no output.

## 3. Arquitetura — pipeline de 10 agentes

Duas fases (divergência → convergência) com **dois merges paralelos**:

```
Input → Reformulador → [Mapeador ‖ Expansor] → merge →
        [Transgressor ‖ Combinador] → merge →
        Membrana de Novidade →            ← (separa as 2 fases)
        Construtor → Avaliador → [Mapa de Combinações ‖ Verificador] → Output
```
(No n8n v3.0 são 18 nós, incluindo parse/merge; no standalone, 10 agentes.)

| # | Agente | Modelo | Função |
|---|---|---|---|
| 1 | **Reformulador** | Haiku | 3 reformulações do problema (ângulos: mecanismo/agente/premissa) → escolhe a mais fértil. **Muda o frame, não o objetivo.** |
| 2 | **Mapeador de Domínios** | Haiku | 5 domínios externos com estrutura **análoga** (nunca do mesmo campo); extrai mecanismo central + elemento transplantável. Micro-validador rejeita analogia superficial. |
| 3 | **Expansor** | Haiku | 7 direções, **1 por categoria** (tecnológica, comportamental, estrutural, econômica, cultural, regulatória, relacional). Sem julgar viabilidade. |
| 4 | **Transgressor** | **Sonnet** | Identifica premissas (fundamental/central/secundária) e **inverte** com especificidade; calibrado pelo nível. Único agente no Sonnet. |
| 5 | **Combinador de Domínios** | Haiku | **Transplanta** o mecanismo de cada domínio externo para ≥2 direções → conceitos híbridos. |
| 6 | **Membrana de Novidade** | Haiku | Filtra por novidade real: `reembalagem→variação→híbrido_novo→ruptura`. Só passam híbrido_novo/ruptura (máx. 5). 2 níveis de fallback. |
| 7 | **Construtor** | **Sonnet** | Torna cada ideia concreta: nome, mecanismo, quem usa, como funciona, menor passo p/ existir, "o que não é". Fallback p/ Haiku. |
| 8 | **Avaliador Independente** | Haiku | Pontua 3 dimensões (novidade_real, magnitude_problema, reversibilidade), **sem comparar** conceitos e **sem saber que há score**. Pesos dinâmicos. |
| 9 | **Mapa de Combinações** | Sonnet | Relações entre pares (sinergia / contradição produtiva / contradição real / sobreposição / sequência / independência) + combinações férteis + base mais promissora. |
| 10 | **Verificador de Coerência** | Haiku | Portfólio responde ao problema original? `coerente / desvio_parcial / desvio_total`. Campo **`dimensao_inexplorada`** = input pra 2ª rodada. |

## 4. Especificação

### Input (5 parâmetros)
| Campo | Status | Impacto |
|---|---|---|
| `objetivo` | obrigatório | o que criar/resolver |
| `contexto` | obrigatório | **o mais importante** — o que já existe/foi tentado/por que falha |
| `nivel_radicalidade` | obrigatório | `incremental \| disruptivo \| radical` — calibra inversões e pesos |
| `dominio_proibido` | opcional | **o mais poderoso** — proibir o óbvio força ir onde ninguém foi |
| `restricoes_praticas` | opcional | orçamento/prazo/limites técnicos |

### Pesos do Avaliador (variam por nível)
| Dimensão | incremental | disruptivo | radical |
|---|---|---|---|
| novidade_real | 20% | 40% | 60% |
| magnitude_problema | 40% | 40% | 30% |
| reversibilidade | 40% | 20% | 10% |
> O score composto é calculado **pelo sistema após** a avaliação — o agente não sabe que há
> score, pra não calibrar notas e criar hierarquia implícita.

### Output (JSON, 4 blocos)
`portfolio` (conceitos + avaliação + coerência) · `mapa_combinacoes` (relações + combinações
férteis + base) · `processo` (rastreabilidade completa: reformulações, domínios, direções,
premissas, inversões, descartadas+justificativa) · `metadados`.

## 5. Estado de implementação

- 🟢 **Standalone HTML** — roda no browser, chama API Anthropic direto. Sidebar de input +
  barra de progresso por agente + output em 5 abas (Portfólio/Combinações/Processo/JSON/Glossário).
  **Modo Guiado:** agente de elicitação conversacional (até 6 perguntas adaptativas) que
  identifica a "dimensão oculta" e preenche o form. API key só na memória do browser.
- 🟢 **n8n v3.0** — workflow importável, 18 nós, Form trigger, merges como Function (sem o bug
  do `combineByFields`), system/user prompt separados.
- **Limitações conhecidas:** qualidade depende do Haiku seguir instrução estrutural complexa
  (inconsistência silenciosa quando simplifica demais); micro-validadores só no Mapeador e
  Construtor; API key exposta no browser (ok p/ uso pessoal, precisa proxy p/ público);
  `direcoes_geradas` às vezes vazio quando a Membrana usa fallback.

## 6. Decisões de design (registradas)

- **Remoção do "Diretor" (v1→v2):** a v1.0 tinha um agente que escolhia um vencedor. Foi
  **removido** — convergir pra um conceito **perde valor** (os "perdedores" podem ser melhores
  noutro contexto). Substituído pelo portfólio + Mapa de Combinações.
- **Transgressor no Sonnet:** único agente no modelo forte — inverter premissas cruzando
  domínios **degradava visivelmente no Haiku**.
- **Separação system/user** em todos os prompts → consistência do JSON.
- **`dominio_proibido` como alavanca** — sem ele, o MGE converge pro mais documentado.
- **Modo Guiado (v3.0)** — resolve input mal formulado via elicitação.
- **Bug de chaves com acento** — Haiku às vezes retorna `direções`/`domínios` com acento;
  fix: extrair tentando sem acento → com acento → inglês.

## 7. Limitações estruturais (honestas, reconhecidas pelo autor)

1. **A Membrana avalia novidade com um modelo treinado no existente** — um conceito sem
   precedente pode ser marcado como "reembalagem" por similaridade superficial. *Contradição
   estrutural mais profunda, sem solução completa na v1.0.*
2. **O Reformulador decide sem supervisão humana** — se escolher mal o frame, todo o pipeline
   deriva (o Verificador detecta no fim, mas não previne). v2.0 prevê checkpoint humano.
3. **Ruptura real vs. de superfície** — o MGE é forte em **combinação não óbvia**; rupturas
   genuínas de paradigma exigem imersão que LLMs não têm. *Honesto sobre isso.*

## 8. Estado da arte / diferencial

- O mercado de multiagentes (CrewAI, AutoGen, Agno) foca em **automatizar pipelines tirando o
  humano**. O MGE (e o MGX, seu ecossistema) faz o oposto: **estrutura cognitiva explícita** e
  **humano como juiz final** (não escolhe vencedor).
- Diferente de ferramentas de brainstorm/IA генérica: o **transplante estrutural de domínios**
  + **inversão calibrada de premissas** + **filtro de novidade** é uma metodologia, não um prompt.

## 9. Exemplo real de output (do próprio doc)

Problema: *"novo modelo de precificação para saúde mental"*, domínio proibido *"planos/seguros"*,
nível disruptivo → 4 conceitos independentes: **Dividendo Pós-Alta**, **Consórcio de
Recuperação**, **Unidade Delta** (a moeda é o ponto de melhora funcional auditado),
**Recovery Equity**. O Mapa identificou a *Unidade Delta* como base mais promissora
(infraestrutura de medição sem a qual os outros 3 não funcionam).

## 10. Glossário (termos do MGE)

**Membrana de Novidade** (filtro divergência→convergência) · **transplante estrutural** (vs.
mistura temática) · **dimensao_inexplorada** (saída do Verificador → input da 2ª rodada) ·
**contradição produtiva vs. real** (tensão informativa vs. obstáculo) · **híbrido_novo / ruptura**
(graus de novidade que passam a Membrana).

## 11. Proveniência

Desenvolvido em paralelo ao **CEP** ("o CEP decide, o MGE cria"). Redesenhado do zero a partir
de um conceito inicial "raso" (parsers frágeis, prompts vagos). Docs: `MGE_Documentacao_Completa.docx`
(v3.0), `MGE_Arquitetura_v1.0.docx`, chats Claude/Gemini na pasta `Segundo Cérebro/MGE`.
Implementações: HTML standalone, JSON n8n v2.0/v3.0.

## 12. Citações-chave

- *"Criatividade de alto valor não vem de liberdade total — vem de restrições bem colocadas
  combinadas com exploração guiada."*
- *"O sistema nunca escolhe um vencedor: apresenta o conjunto e deixa o julgamento ao usuário."*
- *"Não mistura — transplanta."* (Combinador)
- *"'E se não precisasse de dinheiro?' é inútil. 'E se o valor fosse criado pelo fracasso?' é fértil."* (Transgressor)
- *"A Membrana usa um modelo treinado no que já existe... essa é a contradição estrutural mais profunda do sistema."*
