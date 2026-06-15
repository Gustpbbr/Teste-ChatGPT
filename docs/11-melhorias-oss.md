---
tipo: backlog-melhorias
data: 2026-06-15
status: aprovado-pelo-gustavo
---

# Melhorias futuras + OSS pra aproveitar

Backlog de ideias além do roadmap dos 6 blocos, e projetos open-source que
encaixam. Aprovado em conversa de 15/06/2026 ("gostei de todos").

> Princípio: o Hub/grafo do Gus é construído de propósito (Mem0 foi aposentado).
> OSS entra como **componente** que poupa trabalho, **nunca** substituindo o Hub.

## A) Melhorias de arquitetura (novas)

| ID | Ideia | Porquê | Encaixa em |
|---|---|---|---|
| A1 | **Maturação do grafo** (decay + promoção automática) | anti-lixão de longo prazo; o "metabolismo" do organismo | Hub / ciclos vitais (gus-31) |
| A2 | **Fusão Calendar + biometria** | percepção real nasce do cruzamento ("caso grande amanhã + dormiu mal") | Bloco 1 + cérebro |
| A3 | **Proveniência + trust score + explicabilidade** | proatividade que diz "por que trouxe isso?"; sem isso vira ruído | Bloco 5 |
| A4 | **Cripto em repouso pro sensível** | rota local protege processamento; falta proteger armazenamento (LGPD médico) | schema / Hub |
| A5 | **Replay de pendentes** | reenviar sozinho quando o Hub volta; resiliência offline-first | hub_client |

## B) OSS pra aproveitar (verificado jun/2026)

| Projeto | O que resolve | Bloco / issue |
|---|---|---|
| **Open Wearables** (`the-momentum/open-wearables`) | API única self-hosted pra wearables; dado na tua infra | Bloco 1 real |
| **Gadgetbridge** (`Freeyourgadget/Gadgetbridge`) | lê wearables sem nuvem/conta do fabricante | Bloco 1 (alternativa) |
| **pmndrs/xr** (`@react-three/xr`) | hand tracking, gestos, anchors prontos | Bloco 3 (#15) |
| **3d-force-graph** (vasturiano) | layout de força 3D | Bloco 2 (#12) |
| **Piper TTS** + **faster-whisper** | voz local offline (PT), zero nuvem | Bloco 4 (#19) |
| **Graphiti** (`getzep/graphiti`, Apache 2.0) | grafo bi-temporal: fato muda → invalida o antigo; base da contradição | Bloco 5 (#18) |
| **Cognee / Letta** | referências de memória agêntica (comparar, não trocar Hub) | — |

## Apostas prioritárias

1. **Open Wearables** — destrava Bloco 1 real já respeitando LGPD (maior retorno).
2. **pmndrs/xr + 3d-force-graph** — scaffold VR vira app de verdade.
3. **Graphiti (conceito bi-temporal)** — a peça que falta pra contradição/revisão automática.

## Links

- Graphiti — https://github.com/getzep/graphiti
- Open Wearables — https://github.com/the-momentum/open-wearables
- Gadgetbridge — https://github.com/Freeyourgadget/Gadgetbridge
- pmndrs/xr — https://github.com/pmndrs/xr
- Cognee — https://github.com/topoteretes/cognee · Khoj — https://github.com/khoj-ai/khoj
- Local Voice (Whisper+Piper) — https://github.com/m15-ai/Local-Voice
