# One-Pager — pitch para pesquisadores

> Use isto como base do e-mail/DM. Tom: honesto, curto, sem hype. Lidere com o que roda.

---

## O pitch (1 parágrafo)

Sou Gustavo Pratti, anestesiologista e pesquisador independente. Ao longo de 2025–2026
desenvolvi — em conversa com várias IAs — um corpo de trabalho sobre **IA pessoal centrada
em memória, prudente e sensível**. A peça mais concreta é um **benchmark funcional que mede
a "prudência" (phronesis) de LLMs** (calibração, armadilhas de over-correction, indeterminação,
dilemas clínicos/ai-safety). Em volta dele há uma tese — *"memória é o centro, modelo é
descartável"* — que antecipou a direção do campo (Letta/Mem0/Zep), com um recorte próprio:
**prudência auditável + percepção afetiva local + caso de uso clínico**. Não quero mais tocar
o projeto sozinho; **ofereço tudo sob licença aberta** para quem veja potencial e queira levar
adiante.

## O gancho (o diferencial do contato)

Não precisa ler 100 arquivos: **abra o repositório com uma IA Claude** — ela está instruída
a dar uma **visita honesta de 20 minutos**, separando o que é código que roda do que é só
especificação. Pergunte à vontade: *"o que é real aqui?"*, *"qual a parte publicável?"*.

## O que tem dentro (resumo)

| Camada | Projeto | Estado |
|---|---|---|
| 📐 Avaliação | **Phronesis-Bench** (benchmark de prudência) | 🟢 roda |
| 🧠 Memória | TEAR → TER → Gus (tese memória-cêntrica) | tese + parcial |
| 👁️ Sentidos | ACEE / MASE (IA afetiva embarcada, local) | spec detalhada |
| ⚖️ Governança | TER KAI (middleware prudencial auditável) | spec |
| 🫀 Síntese | Gus (organismo: corpo+alma+sentidos) | parcial (bot + Hub reais) |

## Por que pode interessar

- **Prudência mensurável** (phronesis como benchmark) — raro e ligado a alinhamento/segurança.
- **Ângulo clínico** (autor médico): decisão sob incerteza, LGPD, dado sensível.
- **Memória + privacidade local** como espinha — convergente com o estado da arte, com recorte próprio.

## O que ofereço / o que peço

- **Ofereço:** licença aberta (MIT código / CC BY docs) — use, publique, construa em cima, com crédito.
- **Peço:** se ver valor, me diga — colaboração é bem-vinda (não exigida). Mesmo um "não, mas
  o Phronesis tem potencial" já é útil.

---

## Template de e-mail/DM (copiar e adaptar)

> **Assunto:** Benchmark de "prudência" de LLMs + tese de memória — oferecendo sob licença aberta
>
> Olá [nome],
>
> Acompanho seu trabalho em [memória de agente / affective computing / eval / alinhamento].
> Sou médico (anestesiologista) e pesquisador independente. Construí um corpo de trabalho
> sobre IA pessoal centrada em memória e raciocínio prudente; a parte concreta é um
> **benchmark que mede a prudência (phronesis) de LLMs** — calibração, armadilhas de
> over-correction, indeterminação e dilemas clínicos/ai-safety.
>
> Não quero tocá-lo sozinho e **ofereço tudo sob licença aberta**. Em vez de te mandar 100
> arquivos: o repositório tem uma IA-guia que dá uma **visita honesta de 20 min** (separando
> o que roda do que é spec). Link: [repo]
>
> Se quiser dar uma olhada e me dizer se vê potencial, agradeço demais. Mesmo um feedback
> curto ajuda.
>
> Abraço,
> Gustavo Pratti de Barros

---

## ⚠️ Checklist ANTES de enviar (bloqueante)

- [x] **PII scrub da pasta `Entregavel/`:** ✅ varredura feita (2026-06-16) — sem CPF, e-mails,
      telefones ou dados de terceiros. Só o nome do autor (atribuição). **Esta pasta está limpa.**
- [ ] **PII scrub do material-fonte** (se for incluí-lo): os repos/dumps brutos e o Phronesis-Bench
      contêm dados pessoais (CPF, referências clínicas, perfil). **Não incluir sem limpar.**
      Recomendação: publicar **só `Entregavel/`** + o Phronesis-Bench já revisado.
- [ ] Confirmar a licença no `LICENSE.md` (e decidir patente: manter ou abrir via Apache).
- [ ] Tornar público só o que for revisado (de preferência, **só a pasta `Entregavel/` + o
      Phronesis-Bench limpo**, não os dumps brutos de 100 MB).
- [ ] Testar o tour: abrir o repo com uma Claude e ver se a visita sai honesta.
