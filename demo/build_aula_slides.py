#!/usr/bin/env python3
"""Transforma a aula HTML (conteúdo do <main>) em slides navegáveis.

Reaproveita o <style> original (boxes, tabelas, grifos) e pagina o conteúdo
em slides no próprio navegador (quebra em cada h1/h2/h3/eyebrow). Uso:

    python build_aula_slides.py <origem.html> <saida.html>
"""
import re
import sys

origem, saida = sys.argv[1], sys.argv[2]
html = open(origem, encoding="utf-8").read()

# título
m = re.search(r"<title>(.*?)</title>", html, re.S)
titulo = (m.group(1).strip() if m else "Aula — Slides")

# estilos originais (todos os blocos <style>) e os <link> de fonte
estilos = "\n".join(re.findall(r"<style.*?</style>", html, re.S))
links = "\n".join(re.findall(r'<link[^>]*fonts[^>]*>', html))

# conteúdo do <main>
mm = re.search(r"<main[^>]*>(.*?)</main>", html, re.S)
main_html = mm.group(1) if mm else html

DECK_CSS = """
<style id="deck-css">
  html,body{height:100%;margin:0}
  body{overflow:hidden;background:var(--bg);color:var(--fg)}
  #source{display:none}
  #deck{position:fixed;left:0;right:0;top:0;bottom:66px}
  .slide{position:absolute;inset:0;overflow-y:auto;-webkit-overflow-scrolling:touch;
    opacity:0;pointer-events:none;transform:translateX(34px);
    transition:opacity .45s ease,transform .45s ease;padding:44px 18px 90px}
  .slide.active{opacity:1;pointer-events:auto;transform:none}
  .slide .inner{max-width:760px;margin:0 auto}
  .slide h1,.slide h2,.slide h3{margin-top:.2em}
  /* setas laterais */
  .seta{position:fixed;top:0;bottom:66px;width:64px;display:grid;place-items:center;z-index:60;
    border:0;background:transparent;color:var(--bronze);font-size:2rem;cursor:pointer;opacity:.45;
    transition:opacity .2s,background .2s}
  .seta:hover{opacity:1;background:linear-gradient(90deg,rgba(0,0,0,.06),transparent)}
  #setaDir{right:0}.seta#setaDir:hover{background:linear-gradient(270deg,rgba(0,0,0,.06),transparent)}
  #setaEsq{left:0}
  /* progresso */
  #progwrap{position:fixed;top:0;left:0;right:0;height:4px;background:rgba(140,105,18,.15);z-index:70}
  #prog{height:100%;width:0;background:linear-gradient(90deg,var(--bronze),var(--ouro),var(--ouro-claro));
    transition:width .3s ease}
  /* barra inferior */
  #controles2{position:fixed;left:0;right:0;bottom:0;height:66px;z-index:70;display:flex;align-items:center;
    justify-content:center;gap:10px;background:var(--card);border-top:1px solid var(--linha);
    padding-bottom:env(safe-area-inset-bottom)}
  #controles2 button{font-family:var(--sans,sans-serif);font-weight:700;font-size:.8rem;color:var(--fg);
    border:1px solid var(--linha);background:var(--bg2);border-radius:99px;padding:.6em 1.1em;cursor:pointer;
    min-height:40px}
  #controles2 button:hover{border-color:var(--ouro)}
  #contador{font-family:var(--sans,sans-serif);font-weight:700;font-size:.78rem;color:var(--bronze);
    min-width:74px;text-align:center}
  #dica2{position:fixed;right:12px;top:12px;z-index:70;font-family:var(--sans,sans-serif);font-size:.66rem;
    color:var(--bronze);opacity:.7}
</style>
"""

DECK_JS = """
<script>
(function(){
  var source=document.getElementById('source');
  var deck=document.getElementById('deck');

  // 1) achata os blocos de conteúdo (filhos de .wrap, ignorando containers)
  var crus=[].slice.call(source.querySelectorAll('.wrap > *'));
  var blocos=crus.filter(function(el){
    return !el.classList.contains('parte') && el.tagName!=='SECTION' && !el.querySelector('.wrap');
  });
  if(!blocos.length){ blocos=[].slice.call(source.children); }

  // 2) agrupa em slides: novo slide em h1/h2/h3/.eyebrow (runs consecutivos juntos)
  function ehQuebra(el){
    return /^H[123]$/.test(el.tagName) || el.classList.contains('eyebrow');
  }
  var slides=[], atual=null, quebrouAntes=false;
  blocos.forEach(function(el){
    if(ehQuebra(el)){
      if(!quebrouAntes||atual===null){
        atual=document.createElement('section');atual.className='slide';
        var inner=document.createElement('div');inner.className='inner';
        atual.appendChild(inner);slides.push(atual);deck.appendChild(atual);
      }
      quebrouAntes=true;
    } else { quebrouAntes=false; if(atual===null){
      atual=document.createElement('section');atual.className='slide';
      var inr=document.createElement('div');inr.className='inner';
      atual.appendChild(inr);slides.push(atual);deck.appendChild(atual);
    }}
    atual.querySelector('.inner').appendChild(el);
  });

  // 3) navegação
  var idx=0;
  var prog=document.getElementById('prog');
  var contador=document.getElementById('contador');
  function mostra(i){
    idx=Math.max(0,Math.min(slides.length-1,i));
    slides.forEach(function(s,j){ s.classList.toggle('active',j===idx); });
    slides[idx].scrollTop=0;
    prog.style.width=((idx+1)/slides.length*100)+'%';
    contador.textContent=(idx+1)+' / '+slides.length;
  }
  document.getElementById('prox').onclick=function(){mostra(idx+1)};
  document.getElementById('ant').onclick=function(){mostra(idx-1)};
  document.getElementById('setaDir').onclick=function(){mostra(idx+1)};
  document.getElementById('setaEsq').onclick=function(){mostra(idx-1)};
  addEventListener('keydown',function(e){
    if(e.code==='ArrowRight'||e.code==='Space'||e.code==='PageDown'){e.preventDefault();mostra(idx+1);}
    else if(e.code==='ArrowLeft'||e.code==='PageUp'){e.preventDefault();mostra(idx-1);}
    else if(e.code==='Home'){mostra(0);}
    else if(e.code==='End'){mostra(slides.length-1);}
  });
  // swipe (toque)
  var x0=null;
  addEventListener('touchstart',function(e){x0=e.touches[0].clientX;},{passive:true});
  addEventListener('touchend',function(e){
    if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;
    if(Math.abs(dx)>60){ mostra(idx+(dx<0?1:-1)); } x0=null;
  },{passive:true});

  mostra(0);
})();
</script>
"""

TEMPLATE = """<!doctype html>
<html lang="pt-BR" data-theme="claro">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITULO} — slides</title>
{LINKS}
{ESTILOS}
{DECK_CSS}
</head>
<body>
<div id="progwrap"><div id="prog"></div></div>
<div id="dica2">← → ou espaço · swipe no toque</div>
<button class="seta" id="setaEsq" aria-label="anterior">‹</button>
<button class="seta" id="setaDir" aria-label="próximo">›</button>

<div id="source"><main>{MAIN}</main></div>
<div id="deck"></div>

<div id="controles2">
  <button id="ant">‹ Anterior</button>
  <span id="contador">1 / 1</span>
  <button id="prox">Próximo ›</button>
</div>
{DECK_JS}
</body>
</html>
"""

out = (TEMPLATE
       .replace("{TITULO}", titulo)
       .replace("{LINKS}", links)
       .replace("{ESTILOS}", estilos)
       .replace("{DECK_CSS}", DECK_CSS)
       .replace("{MAIN}", main_html)
       .replace("{DECK_JS}", DECK_JS))

open(saida, "w", encoding="utf-8").write(out)
print("slides gerados:", saida, "(", len(out), "bytes )")
