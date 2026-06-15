---
tipo: roadmap
data: 2026-06-15
---

# Roadmap de integração — a sequência mestra

Ordenado por **dependência e custo**, não por empolgação. Cada bloco entrega valor sozinho.

| Bloco | O que é | Depende de | VR? | Status |
|---|---|---|---|---|
| **0** | Interocepção (Gus sente a si mesmo: heartbeat/health) | nada | não | ✅ implementado (ref) |
| **1** | Primeiro sentido: Sensor Gateway + wearable → Hub | Gateway | não | ✅ implementado (ref) |
| **2** | Corpo lê: orbe VR mostra memórias+sensores orbitando arquivos | Hub estável (B0) | sim | 🟡 scaffold |
| **3** | Corpo escreve: gestos viram memória + rota local Gemma obrigatória | B2 + Gemma local | sim | 🟡 router + scaffold |
| **4** | Tempo real: SSE (nó nasce ao vivo) + voz + mais sensores | B3 + `/hub/stream` | sim | ⏳ (backend Gus + hardware) |
| **5** | Proatividade encarnada: estado biométrico colore o espaço, contradições brilham | B1–B4 + métricas | sim | 🟡 núcleo (lacuna/acúmulo) |

## Por que esta ordem

- **Bloco 0 primeiro, sempre.** Não adianta dar sentidos a um organismo que não
  percebe quando adoece. Resolve a falha silenciosa (curador parar sem ninguém ver)
  e vira a base de confiabilidade de tudo. É barato.
- **Bloco 1 cedo e em paralelo.** Valida o pipeline sensor→gateway→Hub sem depender
  de VR. Maior retorno por menor esforço (wearable → `saude/`).
- **Blocos 2–4** são quase só cola sobre o que já existe/está especificado no NeuroGus.
- **Bloco 5** é a única parte com componente novo pesado dependente (proatividade + render).

## Escopo deste repo agora

Apenas **Blocos 0 e 1**. Os blocos 2–5 estão aqui só pra contexto; serão destravados
quando 0 e 1 estiverem verdes e calibrados em uso.

## Critério de sucesso dos Blocos 0+1

> "Quando o curador para de escrever, o Gus avisa em minutos (interocepção). E quando
> seu sono foi ruim, isso aparece como fragmento no `saude/` e o Gus comenta na próxima
> interação — sem você ter contado."

## Riscos que a camada de sensor adiciona

1. **LGPD vira eixo central** — biometria de médico é dado ultrassensível. Rota local é arquitetura, não feature.
2. **Acoplamento em cascata** — 3 sistemas que podem cair. Contrato de degradação em camadas é obrigatório.
3. **Ruído × volume** — sensor é a maior fonte de poluição de grafo. O filtro do Gateway é o que faz ou quebra.
4. **Custo contínuo** — sensor não dorme. Filtro agressivo + processamento local pro contínuo.
