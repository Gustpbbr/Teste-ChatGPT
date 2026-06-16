# 📱 FASE 0 — Galaxy S20: Gus Local com IA

> **Pré-requisito:** Galaxy S20 com ~5 GB livres, Wi-Fi (só pra baixar modelo)

---

## 🚀 Instalação Simplificada (1 comando)

```bash
# 1. Instale o Termux do F-Droid: https://f-droid.org/packages/com.termux/
#    ⚠️ NÃO use a versão da Play Store (está abandonada)
#
# 2. Abra o Termux e cole este comando:

curl -sL https://raw.githubusercontent.com/Gustpbbr/Teste-ChatGPT/organizacao-autoclaw/MASE/setup.sh | bash

# 3. Aguarde ~15 minutos (download do modelo)
# 4. Pronto! Para iniciar o Gus:

cd ~/gus-local && bash iniciar.sh
```

O instalador detecta automaticamente quanta RAM seu S20 tem e escolhe o modelo ideal:
- **8+ GB RAM:** Gemma 4B (2.5 GB — qualidade alta)
- **< 8 GB RAM:** Gemma 1B (815 MB — mais rápido)

---

## 🧪 Depois de instalado

```bash
# Iniciar chat com o Gus
cd ~/gus-local && bash iniciar.sh

# Teste rápido
ollama run gemma3:4b "Olá Gus, como você está?"

# Ver modelos instalados
ollama list
```

---

## 🔧 Instalação Manual (se o script automático falhar)

### 1. Configurar o Termux

```bash
pkg update && pkg upgrade -y
pkg install -y python python-pip git wget curl proot
termux-setup-storage  # permitir acesso aos arquivos
```

### 2. Instalar Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &  # iniciar em background
sleep 5
```

### 3. Baixar o modelo e o script

```bash
ollama pull gemma3:4b  # ou gemma3:1b se pouca RAM
pip install ollama requests
mkdir -p ~/gus-local && cd ~/gus-local
curl -O https://raw.githubusercontent.com/Gustpbbr/Teste-ChatGPT/organizacao-autoclaw/MASE/setup.sh
# Extraia o script gus_chat.py manualmente do setup.sh
```

### 4. Alternativa: proot-distro (Ubuntu)

```bash
pkg install proot-distro -y
proot-distro install ubuntu
proot-distro login ubuntu
# Dentro do Ubuntu:
apt update && apt install -y curl python3 python3-pip
curl -fsSL https://ollama.com/install.sh | sh
ollama serve & && ollama pull gemma3:4b
pip install ollama requests
# Copie e execute gus_chat.py
```

---

## 🧪 Testes de validação

| # | Comando | Resultado esperado |
|---|---------|-------------------|
| 1 | `ollama list` | Mostra `gemma3:4b` (2.5 GB) |
| 2 | `ollama run gemma3:4b "Qual a capital do Brasil?"` | "Brasília" |
| 3 | Desligar Wi-Fi, repetir teste 2 | Funciona igual |
| 4 | `python3 fase0_gus_local.py` | Chat interativo com Gus |

---

## 📊 Expectativa de performance (S20)

| Modelo | RAM usada | Latência estimada |
|--------|-----------|-------------------|
| gemma3:1b | ~1 GB | 2–5s |
| gemma3:4b | ~3 GB | 3–8s |
| llama3.2:3b | ~2.5 GB | 5–10s |

Com NPU da Samsung/Qualcomm, o Gemma 4B deve responder em **3–5 segundos**. Usável em conversa.

---

## 🐣 Depois da Fase 0

Com o Gus rodando local no S20, a Fase 1 é:
- Conectar Arduino Nano via USB-C (R$40)
- Controlar fita LED pela porta serial
- Adicionar análise de tom de voz via microfone nativo
- Loop: falar → detectar emoção → mudar cor da luz
