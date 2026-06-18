# Axon / MGX · briefing

> 📄 **Axon: conceitual.** 🟡 **MGX: design completo** (MGE/CEX funcionais; orquestração e MEX não).
> Detalhe técnico completo em [`deep-dive.md`](deep-dive.md).

## Axon — governança contextual de automação
Um "guardião prudente" entre o usuário e seus apps/dispositivos. Antes de executar uma automação,
avalia: *o contexto justifica? o risco é aceitável dado o estado do usuário? a ação é reversível?*
Diferente de IFTTT/Shortcuts (regras rígidas) por incluir uma **camada de deliberação**.
- **Nicho prioritário:** famílias com crianças neurodivergentes (necessidade real + disposição a pagar).
- **Estado:** blueprint conceitual + crítica multi-especialista + roadmap 12 meses. **Implementação: zero.**
- **Riscos:** biometria (LGPD/GDPR), monitoramento de menores, classificação como dispositivo médico.

## MGX — orquestração multiagente com humano no loop
Integra três motores — **MGE** (gera) + **CEX** (delibera) + **MEX** (executa) — com **deliberação
humana ativa entre cada fase**. Grafo de decisão (Fases 0→3.5, transições bidirecionais, snapshots
imutáveis), 3 camadas de memória (estado vivo / snapshots / diário de decisões), compilador de contexto.
- **Diferencial:** o oposto de CrewAI/AutoGen — coloca o **humano no centro** como co-decisor, não o remove.
- **Estado:** MGE v2.0 e CEX v1.1 funcionais; **MEX só conceito**; a camada de orquestração MGX **não construída**.
- Framework-base mapeado: Agno.

## Por que importa
Ambos materializam a tese "capacidade sem prudência é perigosa": Axon no mundo físico/automação,
MGX no fluxo criativo-decisório.

**Fonte:** Drive (`axon-00-briefing`, `mgx-001` a `004`, conversa-origem MEX).
