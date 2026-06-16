# ACEE / MASE — briefing

> 📄 **Estado: SPEC DETALHADA (grau de patente), código mínimo.**
> Fonte: GitHub `Gustpbbr/Projetos` (ACEE organizado por capítulos) e Drive "PROJETO MASE E ACEE".

## O que é

**ACEE — Arquitetura Cognitiva Emocional Embarcada:** uma **IA afetiva *embarcada*
(edge/on-device), offline-first, explicável e ética**. O objetivo é dotar dispositivos da
capacidade de perceber e responder ao estado **emocional e situacional** humano, localmente.
É a camada de **sentidos/afeto** do ecossistema.

**MASE** é o projeto **irmão** (embarcado/dispositivo — tem módulos de câmera, técnicos e de
custos). Sempre pareado com o ACEE.

## Arquitetura (resumo)

```
CMA (percepção) → NCAC (núcleo simbólico) → MOR (resposta)
   │                  │
 ILs → VSEs        MIS → EAGS         + MAL (memória) + PEE (ética)
```
- **CMA** — camada de percepção multimodal, feita de **ILs (Interpretadores Leves)**: Voz,
  Facial, Pupilar, Texto, Postural, **Fisio (HRV/EDA/SpO2)**, Contexto, Língua de Sinais, Tátil.
  Cada IL transforma sinal bruto em **VSE (Vetor Simbólico de Emoção)**.
- **NCAC/MIS** — núcleo **simbólico** (regras + ontologias) que funde VSEs num **EAGS**
  (Estado Afetivo Global) — explicável por design.
- **MAL** memória afetiva local · **ASIC** aprendizado incremental reversível · **PEE**
  protocolo ético embarcado.
- **Híbrido:** ILs usam ML leve (TinyML); o núcleo é simbólico (para explicabilidade/governança).

## Por que importa

- **Afeto + local + explicável + edge** é um nicho real e pouco atacado (a maioria de afeto
  é nuvem/black-box).
- O design **IL → VSE** é uma forma elegante e modular da "camada de sentidos" — diretamente
  reutilizável como a percepção do organismo (Gus Bloco 1).
- **Privacy-by-design / LGPD** no núcleo (dado emocional é sensível por definição).

## Limitações honestas

- É **especificação**, não implementação — documentos ricos (capítulos 4–9), código mínimo.
- Muito ambiciosa (dezenas de "Funcionalidades", latências-alvo, ontologias EMONT/OWL2):
  tratar números como metas de projeto.
- MASE: o documento principal não foi totalmente extraído ainda — caracterizado por contexto
  (dispositivo embarcado ligado ao ACEE).
