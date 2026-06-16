#!/usr/bin/env python3
"""
🦾 GUS WEB — Interface de chat via navegador
=============================================
Roda no Termux + Ollama. Acesse pelo Chrome do celular em localhost:8080.
Totalmente offline após primeiro setup.

Uso:  python3 gus_web.py
      → Abra http://localhost:8080 no Chrome
"""

import http.server
import json
import requests
import os
from urllib.parse import urlparse, parse_qs

OLLAMA = "http://localhost:11434/api/chat"
MODEL = os.getenv("GUS_MODEL", "gemma3:4b")
PORT = 8080

SYSTEM = """Você é o Gus, agente pessoal do Gustavo Pratti de Barros.
Responda em português brasileiro de forma direta, informal e útil.
Você é um organismo cognitivo com memória persistente, múltiplas portas de acesso,
e ajuda com tarefas diárias, pesquisa, código e conversas.
Seja conciso, inteligente e com personalidade própria."""

HTML = r"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>🦾 Gus</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f0f0f;color:#e0e0e0;height:100dvh;display:flex;flex-direction:column}
header{background:#1a1a1a;padding:12px 16px;border-bottom:1px solid #2a2a2a;display:flex;align-items:center;gap:10px}
header h1{font-size:18px;font-weight:600;color:#c4b5fd}
header .status{font-size:11px;color:#888;margin-left:auto}
#messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}
.msg{max-width:85%;padding:10px 14px;border-radius:16px;font-size:15px;line-height:1.5;word-break:break-word;animation:fadeIn .2s}
.msg.user{align-self:flex-end;background:#2d2254;color:#e0d0ff;border-bottom-right-radius:4px}
.msg.gus{align-self:flex-start;background:#1a1a1a;color:#d0d0d0;border:1px solid #2a2a2a;border-bottom-left-radius:4px}
.msg .time{font-size:10px;color:#666;margin-top:4px}
.msg .meta{font-size:10px;color:#555}
.typing{color:#666;font-size:13px;padding:4px 14px;animation:pulse 1.5s infinite}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{opacity:.3}50%{opacity:.8}}
footer{background:#1a1a1a;padding:8px;border-top:1px solid #2a2a2a;display:flex;gap:8px}
footer textarea{flex:1;background:#0f0f0f;border:1px solid #2a2a2a;border-radius:12px;color:#e0e0e0;padding:10px 14px;font-size:15px;resize:none;max-height:120px;outline:none;font-family:inherit}
footer textarea:focus{border-color:#7c3aed}
footer button{background:#7c3aed;color:#fff;border:none;border-radius:12px;padding:10px 16px;font-size:14px;font-weight:600;cursor:pointer;min-width:60px}
footer button:active{background:#6d28d9}
footer button:disabled{background:#3a3a3a;color:#777}
</style>
</head>
<body>
<header>
  <span style="font-size:24px">🦾</span>
  <h1>Gus</h1>
  <span class="status" id="status">⏳ conectando...</span>
</header>
<div id="messages"></div>
<div id="typing" class="typing" style="display:none">Gus está pensando...</div>
<footer>
  <textarea id="input" rows="1" placeholder="Fale com o Gus..." autofocus></textarea>
  <button id="send" onclick="enviar()">Enviar</button>
</footer>
<script>
const MODEL="MODELO";
let msgs=[{role:"system",content:SYSTEM_CONTENT}];

function scroll(){const m=document.getElementById("messages");m.scrollTop=m.scrollHeight}

function addMsg(role,text,meta){
  const d=document.getElementById("messages");
  const el=document.createElement("div");
  el.className="msg "+role;
  const t=new Date().toLocaleTimeString("pt-BR",{hour:"2-digit",minute:"2-digit"});
  el.innerHTML=text.replace(/</g,"&lt;").replace(/\n/g,"<br>")+`<div class="time">${t}</div>`;
  if(meta) el.innerHTML+=`<div class="meta">${meta}</div>`;
  d.appendChild(el);scroll();
}

async function enviar(){
  const inp=document.getElementById("input");
  const btn=document.getElementById("send");
  const text=inp.value.trim();
  if(!text) return;
  
  addMsg("user",text);
  inp.value="";inp.style.height="auto";
  btn.disabled=true;
  
  const typing=document.getElementById("typing");
  typing.style.display="block";scroll();
  
  msgs.push({role:"user",content:text});
  if(msgs.length>12) msgs=[msgs[0]].concat(msgs.slice(-11));
  
  try{
    const t0=Date.now();
    const r=await fetch("/api/chat",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({messages:msgs})
    });
    const data=await r.json();
    const elapsed=((Date.now()-t0)/1000).toFixed(1);
    
    typing.style.display="none";
    if(data.error) throw new Error(data.error);
    
    addMsg("gus",data.content,`${elapsed}s · ${data.tokens||0} tokens · ${MODEL}`);
    msgs.push({role:"assistant",content:data.content});
  }catch(e){
    typing.style.display="none";
    addMsg("gus","❌ Erro: "+e.message+"\n\nOllama está rodando? Execute: ollama serve");
  }
  btn.disabled=false;inp.focus();
}

document.getElementById("input").addEventListener("keydown",e=>{
  if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();enviar()}
});
document.getElementById("input").addEventListener("input",function(){
  this.style.height="auto";this.style.height=Math.min(this.scrollHeight,120)+"px"
});

// Check status
fetch("/api/status").then(r=>r.json()).then(d=>{
  document.getElementById("status").textContent=d.ok?"✅ online":"❌ offline";
}).catch(()=>{
  document.getElementById("status").textContent="❌ offline";
});
</script>
</body>
</html>
""".replace("MODELO", MODEL).replace("SYSTEM_CONTENT", json.dumps(SYSTEM))


class GusHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # silêncio
    
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))
        elif self.path == "/api/status":
            try:
                r = requests.get("http://localhost:11434/api/tags", timeout=3)
                self._send_json({"ok": True, "models": r.json().get("models", [])})
            except:
                self._send_json({"ok": False, "error": "Ollama offline"}, 503)
        else:
            self._send_json({"error": "not found"}, 404)
    
    def do_POST(self):
        if self.path == "/api/chat":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length))
                messages = body.get("messages", [])
                
                r = requests.post(OLLAMA, json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 350}
                }, timeout=120)
                data = r.json()
                
                self._send_json({
                    "content": data.get("message", {}).get("content", ""),
                    "tokens": data.get("eval_count", 0),
                    "model": MODEL,
                })
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
        else:
            self._send_json({"error": "not found"}, 404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════╗
║   🦾 GUS WEB — {MODEL}                     ║
║                                          ║
║   🌐 http://localhost:{PORT}                 ║
║                                          ║
║   Abra no Chrome do seu celular.         ║
║   Ctrl+C para encerrar.                  ║
╚══════════════════════════════════════════╝
""")
    http.server.HTTPServer(("0.0.0.0", PORT), GusHandler).serve_forever()
