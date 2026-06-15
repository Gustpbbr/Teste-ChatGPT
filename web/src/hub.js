// Leitura do Hub. v0: mock estático. Costura pronta pro /hub/recent real.
//
// DEGRADÁVEL: se a fonte falhar, retorna [] e o app ainda abre (alma cai,
// corpo continua de pé).

const FONTE_PADRAO = "./mock/fragmentos.json";

export async function carregarFragmentos(fonte = FONTE_PADRAO) {
  try {
    const resp = await fetch(fonte);
    if (!resp.ok) throw new Error("status " + resp.status);
    return await resp.json();
  } catch (e) {
    console.warn("[hub] falha ao carregar fragmentos — degradando:", e);
    return [];
  }
}

// Quando o Hub real estiver no ar (Bloco 2-T2):
//   const base = import.meta.env?.HUB_URL ?? "";
//   carregarFragmentos(`${base}/hub/recent?limit=200`)
// O endpoint deve filtrar estado != "esquecido" (gus-30.1).
