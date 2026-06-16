#!/usr/bin/env python3
"""Transforma a aula HTML (conteúdo do <main>) em slides navegáveis.

Pagina o conteúdo do <main> em slides no navegador (quebra em cada
h1/h2/h3/eyebrow). Usa um CSS PRÓPRIO, limpo e explícito (preto no branco) —
NÃO reaproveita o CSS original da aula, que tinha temas/animações que deixavam
o texto invisível. Uso:

    python build_aula_slides.py <origem.html> <saida.html>
"""
import re
import sys

origem, saida = sys.argv[1], sys.argv[2]
html = open(origem, encoding="utf-8").read()

m = re.search(r"<title>(.*?)</title>", html, re.S)
titulo = (m.group(1).strip() if m else "Aula — Slides")

mm = re.search(r"<main[^>]*>(.*?)</main>", html, re.S)
main_html = mm.group(1) if mm else html

CSS = """
<style>
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:#fff;color:#1a1a1a;line-height:1.7;
  font-family:"EB Garamond",Georgia,"Times New Roman",serif;font-size:18px;
  -webkit-font-smoothing:antialiased}
#source{display:none}
#deck{position:fixed;left:0;right:0;top:0;bottom:66px}
.slide{position:absolute;inset:0;overflow-y:auto;-webkit-overflow-scrolling:touch;
  opacity:0;pointer-events:none;transform:translateX(34px);
  transition:opacity .4s ease,transform .4s ease;padding:48px 20px 90px}
.slide.active{opacity:1;pointer-events:auto;transform:none}
.slide .inner{max-width:760px;margin:0 auto;color:#1a1a1a}
h1,h2,h3{font-family:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#000;line-height:1.2}
h1{font-weight:800;font-size:clamp(1.7rem,1.2rem+2vw,2.3rem);margin:.1em 0 .3em;letter-spacing:-.02em}
h2{font-weight:800;font-size:clamp(1.35rem,1rem+1.4vw,1.7rem);margin:.2em 0 .35em}
h3{font-weight:700;font-size:1.22rem;margin:.5em 0 .3em}
p{margin:0 0 1em}
ul,ol{margin:0 0 1em;padding-left:1.4em}
li{margin:.35em 0}
strong{font-weight:700;color:#000}
em{font-style:italic}
a{color:#9A6B00}
.eyebrow{display:block;font-family:"Inter",sans-serif;font-weight:700;font-size:.72rem;
  letter-spacing:.2em;text-transform:uppercase;color:#9A6B00;margin:0 0 .5em}
.subtit{font-style:italic;color:#9A6B00;margin:-.2em 0 1.1em}
.subhead{font-weight:700;color:#000;margin:1.1em 0 .2em}
.box{background:#FFFDF5;border:1px solid #E7E1CC;border-left:4px solid #DAA520;
  border-radius:12px;padding:1rem 1.2rem;margin:1.2em 0}
.box.armadilha{border-left-color:#C0392B;background:#FFF8F7}
.box.lei{border-left-color:#5E7355;background:#F7FAF4}
.box .tag{display:block;font-family:"Inter",sans-serif;font-weight:800;font-size:.62rem;
  letter-spacing:.14em;text-transform:uppercase;color:#9A6B00;margin-bottom:.4em}
.box.armadilha .tag{color:#C0392B}
.box.lei .tag{color:#5E7355}
.box .ic{margin-right:.4em}
.box p{margin:0;font-size:.96em}
.popup-q{display:flex;gap:.8rem;align-items:flex-start;background:#F7F8F4;border:1px solid #E2E2D6;
  border-left:4px solid #5E7355;border-radius:12px;padding:1rem 1.1rem;margin:1.2em 0}
.popup-q .avatar{font-size:1.6rem}
.popup-q .quem{display:block;font-family:"Inter",sans-serif;font-weight:800;font-size:.62rem;
  letter-spacing:.12em;text-transform:uppercase;color:#5E7355;margin-bottom:.3em}
.popup-q .fala{font-size:.94em}
.citacao{font-style:italic;font-size:1.1em;border-left:3px solid #DAA520;margin:1.2em 0;
  padding:.2em 0 .2em 1em;color:#333}
.tbl{margin:1.4em 0;border:2px solid #222;border-radius:6px;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.9em;text-align:left;color:#1a1a1a}
th{font-family:"Inter",sans-serif;font-weight:700;font-size:.66rem;text-transform:uppercase;
  letter-spacing:.06em;background:#F2F2F2;color:#000;padding:.7rem .9rem;border-bottom:2px solid #222}
td{padding:.7rem .9rem;border-bottom:1px solid #E5E5E5;vertical-align:top}
tr:last-child td{border-bottom:0}
.mt-amarelo{background:#FFEC9B;color:#1a1a1a;padding:.04em .26em;border-radius:3px;font-weight:600}
.mt-rosa{background:#FFC9CF;color:#1a1a1a;padding:.04em .26em;border-radius:3px;font-weight:600}
.mt-verde{background:#CDEBB4;color:#1a1a1a;padding:.04em .26em;border-radius:3px;font-weight:600}
.numfoco{display:flex;align-items:baseline;gap:.5em;margin:1em 0}
.numfoco .nf-num{font-weight:800;font-size:1.9rem;line-height:1;background:#FFEC9B;color:#1a1a1a;
  padding:.02em .2em;border-radius:.1em}
.nota{font-family:"Inter",sans-serif;font-size:.84em;color:#5a5a5a;border-left:3px solid #E5E5E5;
  padding-left:.9em;margin:1em 0}
.pensamento{font-style:italic;color:#9A6B00}
.desafio{background:#FAFAF6;border:1px solid #E6E6E6;border-left:4px solid #9A6B00;
  border-radius:12px;padding:1.1rem 1.2rem;margin:1.4em 0}
.dtag{display:block;font-family:"Inter",sans-serif;font-weight:800;font-size:.64rem;
  letter-spacing:.1em;text-transform:uppercase;color:#9A6B00;margin-bottom:.5em}
.alts{display:flex;flex-direction:column;gap:.4rem;margin:.6em 0}
.alts.julgue{flex-direction:row;flex-wrap:wrap}
.alt-d{background:#fff;border:1px solid #E0E0E0;border-radius:9px;padding:.6em .95em;font-size:.94em;cursor:pointer}
.gab summary{font-family:"Inter",sans-serif;font-weight:800;font-size:.7rem;text-transform:uppercase;
  letter-spacing:.06em;color:#fff;background:#222;display:inline-block;border-radius:99px;
  padding:.55em 1.05em;cursor:pointer;margin-top:.6em;list-style:none}
.gab p{margin:.6em 0 0;font-size:.92em}
.ftag{display:inline-block;font-family:"Inter",sans-serif;font-weight:700;font-size:.56rem;
  letter-spacing:.08em;text-transform:uppercase;color:#C0392B;border:1px dashed #C0392B;
  border-radius:6px;padding:.15em .5em;margin:.2em 0 1em}
.todo-img{font-family:"Inter",sans-serif;font-size:.85em;color:#5a5a5a;background:#F7F7F7;
  border:1px dashed #ccc;border-radius:10px;padding:.8em 1em;margin:1.2em 0}
.grifo-leitor{background:linear-gradient(180deg,transparent 55%,#FFE08A 55%)}
/* navegação */
.seta{position:fixed;top:0;bottom:66px;width:60px;display:grid;place-items:center;z-index:60;
  border:0;background:transparent;color:#9A6B00;font-size:2rem;cursor:pointer;opacity:.4}
.seta:hover{opacity:1;background:rgba(0,0,0,.04)}
#setaDir{right:0}#setaEsq{left:0}
#progwrap{position:fixed;top:0;left:0;right:0;height:4px;background:#eee;z-index:70}
#prog{height:100%;width:0;background:linear-gradient(90deg,#9A6B00,#DAA520,#FFD86B);transition:width .3s}
#controles2{position:fixed;left:0;right:0;bottom:0;height:66px;z-index:70;display:flex;align-items:center;
  justify-content:center;gap:10px;background:#fff;border-top:1px solid #E5E5E5}
#controles2 button{font-family:"Inter",sans-serif;font-weight:700;font-size:.8rem;color:#1a1a1a;
  border:1px solid #ddd;background:#F7F7F7;border-radius:99px;padding:.6em 1.1em;cursor:pointer;min-height:40px}
#controles2 button:hover{border-color:#DAA520}
#contador{font-family:"Inter",sans-serif;font-weight:700;font-size:.78rem;color:#9A6B00;min-width:74px;text-align:center}
#dica2{position:fixed;right:12px;top:12px;z-index:70;font-family:"Inter",sans-serif;font-size:.66rem;color:#9A6B00;opacity:.7}
</style>
"""

DECK_JS = """
<script>
(function(){
  var source=document.getElementById('source');
  var deck=document.getElementById('deck');

  // achata blocos-folha em ordem de documento (robusto ao aninhamento bagunçado)
  var sel='h1,h2,h3,p,ul,ol,table,.box,.tbl,.popup-q,.desafio,.citacao,'+
          '.figura,.eyebrow,.subtit,.nota,.todo-img,.pensamento,blockquote,.numfoco';
  var todos=[].slice.call(source.querySelectorAll(sel));
  var blocos=todos.filter(function(el){
    return !todos.some(function(o){return o!==el && o.contains(el);});
  });
  if(!blocos.length){ blocos=[].slice.call(source.children); }

  function ehQuebra(el){ return /^H[123]$/.test(el.tagName) || el.classList.contains('eyebrow'); }
  var slides=[], atual=null, quebrouAntes=false;
  function novoSlide(){
    atual=document.createElement('section');atual.className='slide';
    var inner=document.createElement('div');inner.className='inner';
    atual.appendChild(inner);slides.push(atual);deck.appendChild(atual);
  }
  blocos.forEach(function(el){
    if(ehQuebra(el)){ if(!quebrouAntes||atual===null){novoSlide();} quebrouAntes=true; }
    else { quebrouAntes=false; if(atual===null){novoSlide();} }
    atual.querySelector('.inner').appendChild(el);
  });

  var idx=0;
  var prog=document.getElementById('prog');
  var contador=document.getElementById('contador');
  function mostra(i){
    idx=Math.max(0,Math.min(slides.length-1,i));
    slides.forEach(function(s,j){ s.classList.toggle('active',j===idx); });
    if(slides[idx]) slides[idx].scrollTop=0;
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
    else if(e.code==='Home'){mostra(0);} else if(e.code==='End'){mostra(slides.length-1);}
  });
  var x0=null;
  addEventListener('touchstart',function(e){x0=e.touches[0].clientX;},{passive:true});
  addEventListener('touchend',function(e){
    if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;
    if(Math.abs(dx)>60){mostra(idx+(dx<0?1:-1));}x0=null;
  },{passive:true});

  mostra(0);
})();
</script>
"""

TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITULO} — slides</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
{CSS}
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
       .replace("{CSS}", CSS)
       .replace("{MAIN}", main_html)
       .replace("{DECK_JS}", DECK_JS))

open(saida, "w", encoding="utf-8").write(out)
print("slides gerados:", saida, "(", len(out), "bytes )")
