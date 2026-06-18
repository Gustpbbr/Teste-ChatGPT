# 04 — O que falta criar para tornar tudo UM só

> A pergunta certa. Todo produto começa como peças isoladas; o que o torna **um** é uma
> camada de conexão criada *a posteriori* — não mais peças.

## O padrão (iPhone, GitHub, Mem0)

| Produto | As peças isoladas | O que foi criado *a posteriori* para unir |
|---|---|---|
| iPhone | tela, bateria, rádio, câmera, CPU | **iOS** + integração industrial + a forma de "um aparelho só" |
| GitHub | git (já existia) | **plataforma**: hosting + API + colaboração + UX em volta do git |
| Mem0 | bancos vetoriais + LLMs (já existiam) | **uma API/SDK simples** que embrulha tudo num "memory layer" |

A lição: o unificador é quase sempre uma **camada de plataforma** — modelo de dados comum +
runtime + API + UX única. **Não é uma nova feature; é tecido conjuntivo.**

## O diagnóstico honesto de hoje

Os projetos compartilham **conceitos** (prudência, memória, percepção) — mas **zero
infraestrutura comum**. Cada um tem:
- **memória própria** (MEM-LOG, PMM, mgxState, MAL, snapshots, Hub...),
- **formato próprio** (JSON ad-hoc por projeto),
- **runtime próprio** (HTML standalone, n8n, spec, chat).

Eles "se comunicam" **só nos documentos**, não tecnicamente. É aí que mora a fragmentação.

## O que CRIAR (o tecido conjuntivo = o "kernel do Gus")

1. **Contrato comum (a língua).** Um schema único (**gus-18**) + um formato de evento/mensagem
   que **todo órgão fala**. É o "HTTP/USB" do sistema — sem ele, nada interopera.
2. **Memória única (a espinha).** *Um* store (Hub Qdrant) que todos leem/escrevem, no lugar das
   5+ memórias ad-hoc. O sistema nervoso central.
3. **Kernel / runtime (o maestro / o "iOS").** O loop que recebe input, **roteia para o(s)
   órgão(s) certo(s)**, costura a memória e aplica governança. O MGX já é um kernel *parcial*
   (de 3 motores); o Gus é o kernel *amplo*.
4. **Adaptadores (os encaixes).** Um wrapper fino por projeto (MGE, CEX, ACEE, Phronesis...) que
   o faz **falar o contrato** e plugar no kernel — transformando ferramenta isolada em **órgão
   plugável**. É o trabalho mais difícil e mais valioso.
5. **Governança transversal (a consciência).** Prudência/Phronesis + rota-local/LGPD aplicadas
   **a todos os órgãos centralmente**, não reimplementadas em cada um.
6. **Face única (o produto).** Um "Gus" com quem o usuário fala em qualquer porta — ele invoca
   MGE/CEX/sensores **sem saber** qual órgão fez o trabalho.

E mais dois conectores: um **registro de órgãos** (catálogo do que cada um faz e seu contrato —
como um registro de plugins) e o **boot** (Segundo Cérebro/bootstrap) que faz uma instância
nova "virar Gus" ao ler a própria história.

```
            FACE ÚNICA (multi-porta: Telegram, VR, voz...)
                          │
                  KERNEL / RUNTIME  ──── governança transversal (prudência + local)
                  (roteia, costura)
              ┌────────────┼────────────┐
        [adaptador]   [adaptador]   [adaptador]   ...  ← órgãos plugáveis
           MGE          CEX           ACEE         (Phronesis, Axon, sensores...)
              └────────────┴────────────┘
                  CONTRATO COMUM (gus-18 + eventos)
                  MEMÓRIA ÚNICA (Hub Qdrant)
```

## A boa notícia: o Gus já é o embrião disso

O Gus **não é mais um projeto** — é justamente a tentativa de kernel: já tem Hub Qdrant
(memória única), schema gus-18 (contrato), multi-porta (face) e o gateway (entrada). Então o
caminho não é começar do zero — é **fazer crescer o kernel + escrever os adaptadores** dos
outros projetos.

## A virada honesta (a parte difícil)

Isto é **trabalho de plataforma/integração** — menos glamouroso que desenhar projetos novos, e
é exatamente onde você precisa **parar de começar coisas novas**. O unificador não é uma ideia
a mais; é a cola entre as que já existem.

## Prova mínima (o teste que vale)

Kernel + contrato (gus-18) + Hub + **2 órgãos** plugados ponta a ponta — ex.: **MGE** (órgão de
"geração") escrevendo no Hub, e a **memória** sendo lida por outra porta. Se **dois órgãos
plugam limpo**, o padrão está provado e o resto é repetição. Se não plugam, o contrato precisa
mudar antes de escalar.

> Em uma frase: **criar o kernel (contrato + memória + runtime + governança + face) e escrever
> um adaptador por projeto.** É isso que transforma 13 peças em 1 organismo.
