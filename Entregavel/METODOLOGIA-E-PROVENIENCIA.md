# Metodologia e Proveniência

> Como este corpo de trabalho foi construído. Transparência aqui é credibilidade — um
> pesquisador precisa saber a natureza do material antes de avaliá-lo.

## Como foi feito

Todo o material nasceu de **conversas extensas com múltiplas IAs**, ao longo de 2025–2026:
- **ChatGPT** (frequentemente sob a persona "Kai") — co-criação do TER, TER KAI, CEX.
- **Gemini** — ACEE (vários capítulos), avaliações críticas.
- **Claude** — MGE, Gus, organização, análise.
- **DeepSeek** — contribuições pontuais.

O autor **não programa**: descreve intenções, revisa e aprova; o código e os documentos são
gerados pela IA. Os originais (ODT/DOCX/chats) foram depois convertidos para Markdown e
organizados por um **pipeline de 5 passagens** (indexar → mapa de cobertura → eleição de
versão → merge → verificação reversa).

## Os dois registros (importante para ler o material)

O trabalho opera em **dois registros de linguagem** que às vezes se misturam:
- **Registro A** — *como uma IA deveria pensar* (filosófico/cognitivo: TEAR, TER).
- **Registro B** — *como um sistema externo prova/governa* o comportamento (engenharia: TER KAI).

Quando o mesmo termo (ex.: "mede ψ") aparece, vale perguntar: é propriedade do modelo (A) ou
métrica calculada por um middleware sobre o output (B)? São coisas diferentes.

## Limites de fidelidade (o que ter em mente)

1. **Confabulação ocasional:** modelos geram detalhes plausíveis mas falsos (ex.: o ChatGPT
   justificou o nome "Kai" como "apelido que muitos usam" — não há tal comunidade).
2. **Métricas grandiosas = metas, não medições** (ECI≈0.94, latências, etc.). Exceção: os
   resultados do Phronesis (medições preliminares, com seus caveats).
3. **Linguagem histórica de "consciência/pré-AGI"** é aspiração, não afirmação técnica — o
   próprio material reconhece isso em vários pontos.
4. **Relabels entre fontes:** δψρω, "Escada de Degraus", "Phronesis Digitalis", MEM-LOG aparecem
   como rótulos de consolidação que nem sempre constam nos chats brutos (ver `GLOSSARIO-MESTRE.md`).
5. **Curadoria automática pode errar:** há registro de um fragmento gerado por curador automático
   marcado como incorreto pelo autor — descrições devem ser ancoradas nas fontes, não em resumos.

## Como verificar

Cada `deep-dive.md` traz **citações verbatim** (algumas com âncora `arquivo:linha`) e marca o que
é `NÃO ENCONTRADO`. A `MATRIZ-DE-MATURIDADE.md` separa o que roda do que é spec.
