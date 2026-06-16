"""
Gus PWA — App Web Instalável
==============================
Interface mobile-first com suporte a voz.
Pode ser instalada como app nativo na tela inicial do Android.

Uso: python3 gus_pwa.py → Abrir http://localhost:8080 no Chrome → "Instalar app"
"""

import json, os, base64, io, wave, struct
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import requests

OLLAMA = "http://localhost:11434/api/chat"
PORT = 8080
MODEL = os.getenv("GUS_MODEL", "gemma3:4b")
HERE = os.path.dirname(os.path.abspath(__file__))

SYS = "Você é o Gus, agente pessoal do Gustavo. Responda em PT-BR, direto e conciso (1-3 frases)."

HTML = r"""<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#0f0f0f">
<link rel="manifest" href="/manifest.json">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🦾</text></svg>">
<title>Gus</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#0f0f0f;color:#e0e0e0;height:100dvh;display:flex;flex-direction:column;overscroll-behavior:none}
header{background:#1a1a1a;padding:12px 16px;border-bottom:1px solid #2a2a2a;display:flex;align-items:center;gap:10px;position:sticky;top:0;z-index:10}
header .logo{font-size:24px} header .name{font-size:18px;font-weight:600;color:#c4b5fd;flex:1}
header .st{font-size:11px;color:#666} header .st.on{color:#4ade80}
#msgs{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.msg{max-width:88%;padding:10px 14px;border-radius:16px;font-size:14px;line-height:1.5;word-break:break-word;animation:in .2s}
.msg.u{align-self:flex-end;background:#2d2254;color:#e0d0ff;border-bottom-right-radius:4px}
.msg.g{align-self:flex-start;background:#1a1a1a;border:1px solid #2a2a2a;border-bottom-left-radius:4px}
.msg .t{font-size:10px;color:#555;margin-top:4px}
.typing{color:#666;font-size:13px;padding:4px 12px;animation:pulse 1.5s infinite;display:none}
@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{opacity:.3}50%{opacity:.8}}
footer{background:#1a1a1a;padding:8px 12px;border-top:1px solid #2a2a2a;display:flex;gap:8px;align-items:flex-end}
footer textarea{flex:1;background:#0f0f0f;border:1px solid #2a2a2a;border-radius:20px;color:#e0e0e0;padding:10px 16px;font-size:14px;resize:none;max-height:100px;outline:none;font-family:inherit}
footer textarea:focus{border-color:#7c3aed}
footer button{background:#7c3aed;color:#fff;border:none;border-radius:50%;width:44px;height:44px;font-size:18px;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center}
footer button:active{background:#6d28d9}
footer button:disabled{background:#2a2a2a;color:#555}
footer button.mic{background:#1a1a1a;border:1px solid #2a2a2a}
footer button.mic.listening{background:#ef4444;border-color:#ef4444;animation:pulse .8s infinite}
.install-banner{background:#2d2254;color:#e0d0ff;padding:10px 16px;font-size:13px;text-align:center;cursor:pointer;display:none}
</style>
</head>
<body>
<header>
  <span class="logo">🦾</span>
  <span class="name">Gus</span>
  <span class="st" id="st">⏳</span>
</header>
<div class="install-banner" id="banner" onclick="install()">📲 Instalar Gus na tela inicial</div>
<div id="msgs"></div>
<div class="typing" id="typing">Gus está pensando...</div>
<footer>
  <button class="mic" id="mic" onclick="toggleMic()" title="Voz">🎤</button>
  <textarea id="inp" rows="1" placeholder="Mensagem..." autofocus></textarea>
  <button id="send" onclick="send()">➤</button>
</footer>

<script>
const M="MODELO", S=SYSTEM;
let msgs=[{role:"system",content:S}];
let recognition=null,listening=false;

// PWA install
let deferredPrompt;
window.addEventListener('beforeinstallprompt',e=>{
  e.preventDefault();deferredPrompt=e;
  document.getElementById('banner').style.display='block';
});
function install(){
  if(deferredPrompt){deferredPrompt.prompt();deferredPrompt=null}
  document.getElementById('banner').style.display='none';
}

// Voice
function toggleMic(){
  if(listening){stopMic();return}
  const mic=document.getElementById('mic');
  if(!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)){
    alert('Reconhecimento de voz não disponível neste navegador.');
    return;
  }
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  recognition=new SR();
  recognition.lang='pt-BR';recognition.interimResults=false;recognition.maxAlternatives=1;
  recognition.onstart=()=>{listening=true;mic.classList.add('listening');mic.textContent='🔴'};
  recognition.onend=()=>{listening=false;mic.classList.remove('listening');mic.textContent='🎤'};
  recognition.onresult=e=>{
    const text=e.results[0][0].transcript;
    document.getElementById('inp').value=text;send();
  };
  recognition.start();
}
function stopMic(){if(recognition){recognition.stop();recognition=null}}

function sc(){document.getElementById('msgs').scrollTop=document.getElementById('msgs').scrollHeight}
function addMsg(role,text,meta){
  const d=document.getElementById('msgs');
  const el=document.createElement('div');el.className='msg '+(role==='user'?'u':'g');
  const now=new Date().toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'});
  el.innerHTML=text.replace(/</g,'&lt;').replace(/\n/g,'<br>')+`<div class="t">${now}</div>`;
  if(meta)el.innerHTML+=`<div class="t">${meta}</div>`;
  d.appendChild(el);sc();
}
async function send(){
  const inp=document.getElementById('inp'),btn=document.getElementById('send');
  const text=inp.value.trim();if(!text)return;
  addMsg('user',text);inp.value='';inp.style.height='auto';btn.disabled=true;
  const typing=document.getElementById('typing');
  typing.style.display='block';sc();
  msgs.push({role:'user',content:text});
  if(msgs.length>12)msgs=[msgs[0],...msgs.slice(-11)];
  try{
    const t0=Date.now();
    const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:msgs})});
    const d=await r.json();const el=((Date.now()-t0)/1000).toFixed(1);
    typing.style.display='none';
    addMsg('assistant',d.content,el+'s · '+M);
    msgs.push({role:'assistant',content:d.content});
  }catch(e){
    typing.style.display='none';
    addMsg('assistant','❌ Erro: '+e.message+'\n\nOllama está rodando? ollama serve');
  }
  btn.disabled=false;inp.focus();
}
document.getElementById('inp').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send()}});
document.getElementById('inp').addEventListener('input',function(){this.style.height='auto';this.style.height=Math.min(this.scrollHeight,100)+'px'});
fetch('/api/status').then(r=>r.json()).then(d=>{
  document.getElementById('st').textContent=d.ok?'✅ online':'❌ offline';
  document.getElementById('st').classList.toggle('on',d.ok);
}).catch(()=>document.getElementById('st').textContent='❌ offline');
</script>
</body></html>""".replace("MODELO",MODEL).replace("SYSTEM",json.dumps(SYS,ensure_ascii=False))


MANIFEST = json.dumps({
    "name":"Gus","short_name":"Gus","start_url":"/","display":"standalone",
    "background_color":"#0f0f0f","theme_color":"#0f0f0f",
    "icons":[{"src":"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🦾</text></svg>","sizes":"100x100","type":"image/svg+xml"}]
}, ensure_ascii=False)


class Handler(BaseHTTPRequestHandler):
    def log_message(self,*a):pass
    def _send(self,data,ct='application/json',status=200):
        body=data.encode() if isinstance(data,str) else json.dumps(data,ensure_ascii=False).encode()
        self.send_response(status);self.send_header('Content-Type',ct+f'; charset=utf-8' if 'json' in ct else '');
        self.send_header('Access-Control-Allow-Origin','*');self.send_header('Content-Length',str(len(body)));self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p=urlparse(self.path).path
        if p=='/':self._send(HTML,'text/html')
        elif p=='/manifest.json':self._send(MANIFEST,'application/json')
        elif p=='/api/status':
            try:r=requests.get('http://localhost:11434/api/tags',timeout=3);self._send({'ok':True,'model':MODEL,'models':len(r.json().get('models',[]))})
            except:self._send({'ok':False},status=503)
        else:self._send({'error':'not found'},status=404)

    def do_POST(self):
        if urlparse(self.path).path=='/api/chat':
            try:
                length=int(self.headers.get('Content-Length',0))
                body=json.loads(self.rfile.read(length))
                r=requests.post(OLLAMA,json={'model':MODEL,'messages':body.get('messages',[]),'stream':False,'options':{'temperature':0.7,'num_predict':300}},timeout=120)
                d=r.json()
                self._send({'content':d.get('message',{}).get('content',''),'tokens':d.get('eval_count',0),'model':MODEL})
            except Exception as e:self._send({'error':str(e)},status=500)
        else:self._send({'error':'not found'},status=404)
    def do_OPTIONS(self):
        self.send_response(200);self.send_header('Access-Control-Allow-Origin','*');self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS');self.send_header('Access-Control-Allow-Headers','Content-Type');self.end_headers()

if __name__=='__main__':
    print(f'\n🦾 Gus PWA — http://localhost:{PORT}\n📲 Abra no Chrome → Menu → "Instalar app"\n')
    HTTPServer(('0.0.0.0',PORT),Handler).serve_forever()
