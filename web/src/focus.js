// Painel de leitura. Conteúdo sensível NÃO é exibido (LGPD por construção):
// só metadados. Renderizar/decifrar dado sensível é rota local (Bloco 3+).

function meta(f) {
  return [f.tipo, f.area, f.via, f.user_id].filter(Boolean).join(" · ");
}

export function mostrarPainel(f, sensivel) {
  const p = document.getElementById("painel");
  if (sensivel) {
    p.innerHTML = `<b>🔒 conteúdo sensível — rota local</b><br><small>${meta(f)}</small>`;
  } else {
    p.innerHTML = `${f.conteudo ?? "(sem conteúdo)"}<br><small>${meta(f)}</small>`;
  }
  p.hidden = false;
}

export function esconderPainel() {
  document.getElementById("painel").hidden = true;
}
