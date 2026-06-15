// Leitura E escrita do Hub. v0 leitura: mock estático. Escrita: degradável
// (falha -> "pendente", nunca quebra a interação). Costura pro Hub real pronta.

const FONTE_PADRAO = "./mock/fragmentos.json";

// ---- Leitura (Bloco 2) ----
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

// ---- Escrita (Bloco 3) — degradável ----
export async function ingestarFragmento(frag, base = "") {
  return _enviar("POST", `${base}/hub/ingestar`, frag);
}

export async function esquecerFragmento(id, base = "") {
  return _enviar("PATCH", `${base}/hub/fragmento/${encodeURIComponent(id)}/esquecer`);
}

export async function apagarFragmento(id, base = "") {
  return _enviar("DELETE", `${base}/hub/fragmento/${encodeURIComponent(id)}`);
}

async function _enviar(metodo, url, corpo) {
  try {
    const opts = { method: metodo, headers: { "Content-Type": "application/json" } };
    if (corpo !== undefined) opts.body = JSON.stringify(corpo);
    const resp = await fetch(url, opts);
    return resp.ok ? { status: "ok" } : { status: "pendente", detalhe: "status " + resp.status };
  } catch (e) {
    console.warn("[hub] escrita falhou — pendente:", e);
    return { status: "pendente", detalhe: String(e) };
  }
}
