# 📱 FASE 0 — Galaxy S20: Gus Local com IA

> **Pré-requisito:** Galaxy S20 com ~5 GB livres, Wi-Fi (só pra baixar modelo)

---

## 🪜 Passo a Passo

### 1. Instalar o Termux (versão correta)

⚠️ **A versão da Play Store está abandonada.** Use a do F-Droid:

```
1. Abra o navegador do S20
2. Vá em: https://f-droid.org/packages/com.termux/
3. Baixe o APK e instale
4. Abra o Termux
```

### 2. Configurar o Termux

No Termux, digite:

```bash
# Atualizar pacotes
pkg update && pkg upgrade -y

# Instalar dependências
pkg install -y python python-pip git wget curl proot

# Dar permissão de armazenamento (pra acessar arquivos do celular)
termux-setup-storage
# (vai aparecer pop-up — permitir)
```

### 3. Instalar Ollama

```bash
# Baixar e instalar Ollama (ARM64, compatível com S20)
curl -fsSL https://ollama.com/install.sh | sh

# Iniciar o servidor (em background)
ollama serve &
# Aguarda ~5s pra iniciar
sleep 5
```

### 4. Baixar o modelo

```bash
# Com 8+ GB RAM livre:
ollama pull gemma3:4b    # ~2.5 GB — melhor qualidade

# Se estiver com pouca RAM:
# ollama pull gemma3:1b  # ~815 MB — mais rápido, menos capaz
```

### 5. Instalar Python e lib do Ollama

```bash
pip install ollama requests
```

### 6. Copiar o script

```bash
# Criar pasta do projeto
mkdir -p ~/gus-local && cd ~/gus-local

# Baixar o script da Fase 0
curl -O https://raw.githubusercontent.com/Gustpbbr/Teste-ChatGPT/organizacao-autoclaw/MASE/fase0_gus_local.py

# OU copie manualmente do computador pro celular
# (pasta Downloads do celular → acessível em ~/storage/downloads/)
```

### 7. Rodar

```bash
python3 fase0_gus_local.py
```

---

## 🔧 Se o Ollama não instalar via script oficial

Alternativa com `proot-distro` (Ubuntu dentro do Termux):

```bash
pkg install proot-distro -y
proot-distro install ubuntu
proot-distro login ubuntu

# Dentro do Ubuntu no Termux:
apt update && apt install -y curl python3 python3-pip
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull gemma3:4b
pip install ollama requests
python3 fase0_gus_local.py
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
