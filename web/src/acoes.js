// Semântica de ações do corpo (Bloco 3). Cada gesto -> uma operação no Hub.
// Irreversível exige confirmação (Gustavo no loop; auto-execução off V1).
// O disparo por gesto de mão (WebXR) é a issue B3-3 (headset).
import { apagarFragmento, esquecerFragmento, ingestarFragmento } from "./hub.js";

export const ACOES = {
  CONECTAR: "conectar", // juntar dois nós
  ESQUECER: "esquecer", // empurrar pra longe (soft, reversível)
  APAGAR: "apagar",     // jogar na lixeira (hard, irreversível)
};

// confirmar: async (msg) => boolean. Default nega irreversível (seguro).
async function _negar() {
  return false;
}

export async function executarAcao(acao, alvo, opts = {}) {
  const base = opts.base ?? "";
  const confirmar = opts.confirmar ?? _negar;

  switch (acao) {
    case ACOES.CONECTAR:
      return ingestarFragmento(
        {
          conteudo: `Conectou "${alvo.a?.conteudo}" a "${alvo.b?.conteudo}" em VR.`,
          tipo: "episodico",
          area: alvo.a?.area ?? "",
          via: "vr",
          user_id: "gustavo",
        },
        base,
      );

    case ACOES.ESQUECER: // reversível, sem confirmação
      return esquecerFragmento(alvo.id, base);

    case ACOES.APAGAR: // irreversível -> confirma
      if (!(await confirmar("Apagar de vez? Isso é irreversível."))) {
        return { status: "cancelado" };
      }
      return apagarFragmento(alvo.id, base);

    default:
      throw new Error("ação desconhecida: " + acao);
  }
}
