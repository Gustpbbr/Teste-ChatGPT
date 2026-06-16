# 🚀 Primeiros Passos — Como rodar o Gus

> Guia rápido do zero ao Gus funcionando no Galaxy S20.
> Tempo total: ~30 min (maior parte é download).

---

## 📱 O que instalar no celular

| App | Onde | Pra quê |
|-----|------|---------|
| **F-Droid** | [f-droid.org](https://f-droid.org) | Loja de apps open-source |
| **Termux** | F-Droid (buscar "Termux") | Terminal Linux no Android |
| **Termux:API** | F-Droid (buscar "Termux:API") | Acesso a microfone, câmera, TTS |
| **Termux:Widget** | F-Droid (opcional) | Atalho na tela inicial |

⚠️ **NÃO use a versão do Termux da Play Store** — está abandonada e quebrada.

---

## 🔐 Cadastros (quase nenhum)

| Serviço | Obrigatório? | Custo |
|---------|-------------|-------|
| **GitHub** | ✅ Já tem (`Gustpbbr`) | Grátis |
| **F-Droid** | ✅ Só instalar o app | Grátis |
| Anthropic Console | ❌ Opcional (API paga) | Pay-per-use |
| OpenAI Platform | ❌ Opcional (API paga) | Pay-per-use |
| Google AI Studio | ❌ Opcional | Grátis (cota) |
| Railway | ❌ Opcional (deploy 24/7) | ~$5/mês |
| Qdrant Cloud | ❌ Opcional (memória) | Grátis (1 cluster) |
| Picovoice | ❌ Opcional (wake word) | Grátis |

---

## ⚡ Instalação (1 comando)

```bash
# 1. Instale Termux e Termux:API do F-Droid
# 2. Abra o Termux
# 3. Cole este comando:

curl -sL https://raw.githubusercontent.com/Gustpbbr/Teste-ChatGPT/organizacao-autoclaw/MASE/setup.sh | bash
```

O instalador:
- Detecta RAM e escolhe Gemma 4B (12 GB) ou 1B (<8 GB)
- Instala Python, Ollama, dependências
- Baixa o modelo (~2.5 GB, só na primeira vez)
- Cria atalhos `iniciar.sh` e `iniciar_web.sh`

⏱️ Aguarde ~15 min (download do modelo).

---

## 🎮 Como usar depois de instalado

```bash
# Chat no terminal
bash ~/gus-local/iniciar.sh

# App web (abrir no Chrome → "Instalar app")
bash ~/gus-local/iniciar_web.sh
# Depois abra: http://localhost:8080

# Comandos extras (se baixou o repo completo):
cd ~/gus-voice
python3 gus_full.py        # Voz: fale "Gus" + comando
python3 gus_pwa.py         # PWA com microfone
```

---

## 📂 Estrutura depois de instalado

```
~/gus-local/
├── iniciar.sh          ← Atalho chat
├── iniciar_web.sh      ← Atalho web
├── gus_chat.py         ← Chat terminal
├── gus_web.py          ← Servidor web
└── gus_memory.db       ← Memória local (SQLite)

Ollama:
  Modelo: gemma3:4b (~2.5 GB)
  Servidor: http://localhost:11434
```

---

## 🧪 Testar se funciona

```bash
ollama run gemma3:4b "Qual a capital do Brasil?"
# Deve responder: Brasília

# Depois desliga o Wi-Fi e testa de novo
# Deve funcionar igual — 100% offline
```
