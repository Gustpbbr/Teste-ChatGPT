# 03 — Mapa do Ecossistema: todos os projetos e como formam o Gus

> Inventário completo + como cada peça se interconecta. Baseado no mapa de conexões do
> próprio autor (`Segundo Cérebro / base-conexoes.md`) e nos briefings de cada projeto.

## A tese que une tudo (DNA compartilhado)

Nas palavras do autor:
> **"Capacidade sem prudência é perigosa."**
> Narrativa unificadora: *"Sistemas inteligentes que **sabem o que não sabem**, **agem com
> cautela diante de irreversibilidade**, e **melhoram sua deliberação ao longo do tempo**."*

Todo projeto é uma manifestação disso por um ângulo diferente.

## Inventário completo

| Projeto | O que é | Camada | Estado honesto |
|---|---|---|---|
| **TEAR** | protocolo reflexivo (origem, pedagógico→metacognição) | 🧠 memória | registrado BN; spec/chats |
| **TER** | framework filosófico de deliberação ética (Aristóteles: phronesis/sophia/maiêutica), co-criado com "Kai" | ⚖️ consciência (base) | conceitual denso; sem PoC |
| **TER KAI / EUPHONIA** | middleware de governança prudencial (métricas, ledger PoP-L) | ⚖️ governança | spec grau-patente |
| **Phronesis-Bench** | benchmark que **mede** prudência de LLMs | 📐 avaliação | **código + resultados preliminares** ✅ |
| **ACEE** | IA afetiva embarcada (CMA/ILs/VSE/NCAC) | 👁️ sentidos | spec detalhada |
| **MASE** | dispositivo/embarcado irmão do ACEE | 👁️🖐️ sentidos/corpo | spec |
| **MGE** | Motor de Geração Estruturada (multiagente criativo, 10 agentes) | ⚙️ geração | **HTML standalone funcional** ✅ |
| **CEX** (← CEP) | Comitê de Especialistas Universais (deliberação adversarial, 11 etapas) | ⚙️ validação | **v1.1 funcional** (limitada) |
| **MEX** | Motor de Execução (materialização) | ⚙️ execução | conceitual |
| **MGX** | MGE+CEX+MEX + **humano no loop** | ⚙️ orquestração | design completo, sem código |
| **Axon** | governança contextual de automação (nicho: famílias neurodivergentes) | ⚙️ automação | conceitual; sem implementação |
| **SMI / CEP** | memória prudencial / deliberação multiagente | 🧠 memória | **pausado** |
| **Segundo Cérebro** | PKM/índice que indexa todos os projetos (boot) | 🧩 meta | ativo |
| **Gus** | a **síntese encarnada**: corpo (VR) + alma (memória) + sentidos | 🫀 organismo | parcial (bot + Hub reais) |

## Mapa de influências (do autor, reproduzido)

```
TER (base filosófica)
 ├──→ Phronesis-Bench   (operacionaliza phronesis como métricas; o nome vem daqui)
 ├──→ Axon              (governança contextual usa deliberação prudente)
 ├──→ MGE / CEX         (membrana de novidade e avaliação usam princípios epistêmicos)
 └──→ SMI / CEP         (memória prudencial, deliberação multiagente)

Phronesis-Bench
 ├──← TER               (prudência computacional; nome phronesis)
 ├──← TER KAI / EUPHONIA(métricas de assimetria de reversibilidade → RAS)
 └──→ Benchmark-as-a-Service (potencial comercial)

MGE ──→ CEX ──→ MEX     (linha de geração→validação→execução)
 └──→ MGX               (ecossistema integrado MGE+CEX+MEX, humano no centro)

CEP ──→ CEX             (evolução: comitê fixo → banca dinâmica)
ACEE ──→ MASE           (spec afetiva → dispositivo)
```

## Como tudo forma o Gus (o organismo)

> Nota honesta: o **Gus é uma síntese de 2026** — ele *não* aparece no mapa de março do
> Segundo Cérebro. É a camada-guarda-chuva que **absorve** os projetos anteriores como órgãos.

```
                  ⚖️ CONSCIÊNCIA / PRUDÊNCIA
              TER (filosofia) → TER KAI (middleware) ⇄ Phronesis (mede)
                            ▲
   👁️ SENTIDOS ───►  🧠 MEMÓRIA (centro)  ◄─── 🖐️ CORPO
   ACEE / MASE        TEAR·TER·SMI → Hub Qdrant      Gus (VR) / MASE
   (percebe, afeto)   Segundo Cérebro = boot/índice
                            ▲
                  ⚙️ AGÊNCIA / ORQUESTRAÇÃO
              MGE (gera) → CEX (delibera) → MEX (executa)
              orquestrados por MGX (humano no loop) · Axon (automação prudente)
                            ▲
                  🫀 METABOLISMO: curador / sleep-time / ciclos vitais
```

**Os fluxos, em palavras:**
1. **Sentidos → Memória:** ACEE/MASE percebem (VSEs/eventos) → filtro → fragmentos no Hub.
2. **Memória → Consciência:** o grafo alimenta o raciocínio, **governado** pelo TER KAI
   (prudência/auditoria) e **medido/calibrado** pelo Phronesis (o par enforce⇄measure).
3. **Consciência → Agência:** decisões prudentes viram ação via MGE→CEX→MEX (gerar/validar/
   executar) ou via Axon (automação no mundo). Toda ação volta ao ledger (memória).
4. **Boot:** o Segundo Cérebro/`gus-bootstrap` faz uma instância nova **"virar Gus"** ao ler
   a própria história — *"modelo é descartável; identidade vive no grafo"*.
5. **Metabolismo:** consolidação contínua (curador/sleep-time) mantém o grafo vivo.

## As três linhagens (genealogia)

- **Memória/ética:** TEAR → TER → TER KAI → (Hub do Gus).
- **Agência/geração:** CEP → CEX; MGE → CEX → MEX → MGX.
- **Sentidos:** ACEE → MASE.
- **Avaliação** (transversal): Phronesis-Bench mede a prudência que TER propõe e TER KAI tenta garantir.

## O que é mais maduro vs. mais conceitual (para priorização)

- 🟢 **Funcional hoje:** Phronesis-Bench (+ resultados), MGE (standalone), CEX v1.1, bot/Hub do Gus.
- 🟡 **Parcial:** Gus (fusão), CEP (pausado).
- 📄 **Conceitual:** TER, TER KAI, ACEE, MASE, MEX, MGX, Axon, SMI.

> Conclusão prática (alinhada à avaliação do próprio autor): o ecossistema é grande e
> fragmentado, mas converge num organismo coerente. O caminho de produto é o **Gus como
> guarda-chuva**, plugando um órgão maduro de cada vez — não construir os 13 em paralelo.
