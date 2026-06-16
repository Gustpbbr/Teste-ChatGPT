# 01 — Visão Geral

> Panorama honesto do corpo de trabalho. Tempo de leitura: ~10 min.

## A tese central (uma frase)

> **A memória é o centro; o modelo é descartável.** Uma IA pessoal útil precisa de uma
> identidade que persiste num grafo externo, percebe o usuário, raciocina de forma prudente
> e auditável, e age por múltiplos canais — preferencialmente local, por privacidade.

Tudo aqui orbita essa ideia. Ela foi formulada por conta própria em 2025 e, em 2026, é
exatamente para onde o campo convergiu (memória de agente: Letta, Mem0, Zep/Graphiti).

## O insight de organização: 10 projetos = 1 organismo

O autor explorou a mesma visão por muitos ângulos, gerando projetos com nomes diferentes.
Vistos juntos, eles **não são concorrentes — são órgãos de um mesmo organismo cognitivo:**

| Projeto(s) | Função (o órgão) | Estado honesto |
|---|---|---|
| **TEAR → TER** | 🧠 memória + metacognição/ética | spec + chats; tese madura |
| **Segundo Cérebro** | 🧠 base de conhecimento pessoal (PKM/boot) | estrutura de briefings |
| **TER KAI** | ⚖️ governança prudencial (middleware, auditoria) | spec grau-patente |
| **ACEE / MASE** | 👁️ percepção afetiva embarcada (sentidos, offline-first) | spec detalhada |
| **Phronesis-Bench** | 📐 avaliação de prudência de LLMs | **código que roda** ✅ |
| **MGE / MGX, Axon** | ⚙️ multiagente / automação | exploratório |
| **Gus** | 🫀 a síntese: corpo (VR) + alma (memória) + sentidos | em construção |

```
                  ⚖️ CONSCIÊNCIA (prudência, auditoria)
                     TER KAI · Phronesis
                            ▲
   👁️ SENTIDOS ──►  🕸️ MEMÓRIA (centro)  ◄── 🖐️ CORPO
   ACEE / MASE        TEAR·TER·Seg.Cérebro      Gus (VR) / dispositivo
                            ▲
                  ⚙️ AGÊNCIA: MGE/MGX · Axon
                  🫀 metabolismo: consolidação contínua
```

## O que é REAL vs. ASPIRACIONAL (sem rodeios)

- ✅ **Real / roda:** o **Phronesis-Bench** — benchmark FastAPI que mede prudência de LLMs
  (corpora A–G com armadilhas, indeterminação, dilemas profissionais; métricas ACC/ECE/CS/RAS;
  split público/privado; LLM-as-judge). É a âncora de credibilidade.
- 🟡 **Parcial:** o **Gus** (organismo de 3 camadas) tem base de código + testes para os
  primeiros blocos (interocepção, gateway de sensores), mas é início.
- 📄 **Aspiracional / spec:** ACEE, TER KAI e o grosso do TER são **especificações detalhadas
  (grau de patente)**, não implementações. Documentos ricos, código mínimo.

## Por que isto pode interessar a um pesquisador

1. **A tese memória-cêntrica** antecipou a direção do campo — e tem um recorte próprio
   (prudência + afeto + local), não só "mais um framework de memória".
2. **A camada de prudência/Phronesis** é rara: medir e tornar *auditável* a "sabedoria
   prática" (phronesis) de um LLM, com benchmark próprio. Pouca gente ataca isso.
3. **Ângulo de domínio:** o autor é anestesiologista — há um caso de uso clínico real
   (decisão sob incerteza, LGPD, dado sensível) que a maioria dos projetos de IA pessoal ignora.
4. **Privacidade por design / offline-first** atravessa todos os projetos.

## Limitações honestas (o que NÃO esperar)

- Não é um produto, nem um sistema integrado funcionando ponta a ponta.
- Escopo grande e fragmentado — o trabalho de consolidação ainda está por fazer.
- Specs antigas têm linguagem grandiosa e métricas não-validadas (sinalizadas como tal).
- Construído por um autor que **não programa** (todo código via IA), o que limita maturidade de engenharia.

## Em uma frase

> Um corpo de pesquisa coerente sobre **IA pessoal centrada em memória, prudente e
> sensível** — com uma tese forte, um benchmark funcional, e muito potencial ainda
> não-implementado. Oferecido a quem queira levar adiante.
