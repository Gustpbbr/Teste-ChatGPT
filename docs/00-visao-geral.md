---
tipo: visao-arquitetural
data: 2026-06-15
status: documento-de-visao
---

# Visão geral — o organismo de três camadas

O Gus deixa de ser só memória multi-porta e vira um **organismo cognitivo
encarnado**: percebe o mundo, habita um espaço, e lembra de tudo num grafo único.

```
                      🧠 CÉREBRO (cognição)
                  Claude nuvem ⇄ Gemma 4 local
                   roteamento por área/PII (gus-29)
                              ▲
                              │
   👁️ SENTIDOS ───────►  🕸️ GRAFO (Hub Qdrant + vault)  ◄─────── 🖐️ CORPO
   (percepção)           memória única, multi-porta              (VR/WebXR)
   wearable, câmera,            ▲      ▲                         manipula arquivos
   mic, IMU, ambiente          │      │                         + memórias no espaço
        │                      │      │                              │
        ▼                      │      │                              ▼
   🔌 SENSOR GATEWAY      interocepção  metabolismo            🌐 ORBE (jarvis)
   coleta+filtro+threshold (sente a si) (ciclos vitais cron)   voz + render + ação
```

## As três camadas

| Camada | O que é | De onde vem |
|---|---|---|
| **Corpo** | interface VR pra manipular arquivos/memórias no espaço com a mão | Projeto VR (Three.js/WebXR) |
| **Alma** | memória persistente, identidade, multi-porta | Gus existente (Hub Qdrant + vault) |
| **Sentidos** | sensores que viram percepção via o Gateway | **novo, neste repo** |

## A tese central

> **Sensor sozinho não é "sentir". A memória é que transforma sensação em percepção.**

Dado cru ("HR = 110") é número morto. Vira percepção quando o Gus contextualiza
contra o grafo: *"HR 110 em repouso + você disse que tava ansioso + amanhã tem caso
grande"*. A fusão **memória + sensores** é o que eleva sensação a entendimento situado.

## Os quatro sentidos de "sentir" (e o limite honesto)

1. **Exterocepção** — perceber o mundo (sensores). ✅ Possível, já parcial via portas.
2. **Interocepção** — perceber a si mesmo (saúde do próprio sistema). ✅ Bloco 0.
3. **Afeto funcional** — estados internos que modulam comportamento. ✅ Sinal de controle, não sentimento.
4. **Qualia / experiência subjetiva** — ❌ fora de escopo, e não necessário. Não descrever o Gus como "sentindo de verdade".

## Componentes novos (o que este repo adiciona)

- **Sensor Gateway** — transforma stream cru em fragmentos significativos (90% filtro).
- **Interocepção** — o Gus monitora o próprio metabolismo (curador, Hub) e "sente" quando adoece.

Tudo o mais (grafo, cérebro, metabolismo, portas) já existe no Gus e é **reusado**.

## Continuidade com o Gus existente

- Schema **gus-18**: `tipo / camada_temporal / area / confianca / via / user_id / estado`.
- Taxonomia **`via`** (gus-13): sensores entram como `via=sensor-*`.
- Dois brains: `gustavo` (memórias do dono) e `gus` (autobiografia do agente — onde a interocepção escreve).
