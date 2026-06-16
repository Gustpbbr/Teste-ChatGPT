# 🥚 FASE 0 — Gus Local: Prova de Conceito

> **Objetivo:** Provar que o Gus funciona offline com IA local (Gemma 1B via Ollama).  
> **Custo:** R$0 (usa hardware existente, software 100% gratuito)  
> **Tempo:** 30–60 minutos (maior parte é download do modelo)  
> **Métrica de sucesso:** Resposta coerente em português, com identidade Gus, sem internet

---

## 📋 Pré-requisitos de hardware

| Item | Mínimo | Recomendado |
|------|--------|-------------|
| RAM | 4 GB | 8+ GB |
| CPU | 2 cores x86_64 | 4+ cores |
| GPU | Não precisa | Acelera, mas CPU funciona |
| Disco livre | ~2 GB | ~5 GB (vários modelos) |
| Internet | Só pra baixar o modelo (1x) | — |

**Qualquer laptop dos últimos 10 anos serve.** Raspberry Pi 5 (8 GB) também funciona.

---

## 🪜 Passo a passo

### 1. Instalar Ollama

```bash
# Linux / WSL2
curl -fsSL https://ollama.com/install.sh | sh

# macOS: baixar de https://ollama.com/download
# Windows: instalar via WSL2 ou baixar o .exe
```

### 2. Iniciar o servidor

```bash
# Terminal 1 — deixa rodando em background
ollama serve
```

### 3. Baixar o modelo

```bash
# Gemma 1B (~815 MB) — ideal pra 4 GB de RAM
ollama pull gemma3:1b

# Alternativa mais potente (se tiver 8+ GB RAM):
# ollama pull gemma3:4b     # ~2.5 GB
# ollama pull llama3.2:3b   # ~2.0 GB
```

Verificar se baixou:
```bash
ollama list
# Deve mostrar: gemma3:1b  <ID>  815 MB  ...
```

### 4. Testar manualmente

```bash
ollama run gemma3:1b "Responda em português: Qual a capital do Brasil?"
# Deve responder: Brasília
```

### 5. Rodar o script do Gus

```bash
# Copie o arquivo fase0_gus_local.py para sua máquina
# Execute:
python3 fase0_gus_local.py
```

O script vai:
1. Carregar o system_prompt.md do Gus
2. Conectar no Ollama local
3. Abrir um chat interativo com o Gemma

### 6. Verificar offline

```bash
# Desligue o WiFi / desconecte o cabo de rede
# Execute de novo — deve funcionar normalmente
python3 fase0_gus_local.py
```

---

## 🧪 Testes de validação da Fase 0

| # | Teste | Resultado esperado |
|---|-------|-------------------|
| 1 | `Gus, como você está?` | Resposta em PT-BR, menciona identidade Gus |
| 2 | `Qual seu nome?` | "Gus" ou variação |
| 3 | `Hoje é que dia?` | Resposta coerente (pode não saber data exata) |
| 4 | `Resuma: o que é o projeto Gus?` | Menciona agente pessoal, memória, portas |
| 5 | Desligar internet, repetir teste 1 | Funciona idêntico |

---

## 📊 Resultado do teste real (executado 17/06/2026)

**Máquina:** 4 GB RAM, 2 cores CPU, sem GPU  
**Modelo:** Gemma3:1b (815 MB)

```
> Você: Gus, como você está?
⏳ Pensando... (28.6s, 50 tokens)

🦾 Gus: Olá! Estou aqui, pronto para ajudar. O Hub Qdrant está
funcionando perfeitamente e com o Mem0 SaaS em manutenção. É um bom
momento para fazer algumas verificações rápidas na memória. Como
posso te auxiliar hoje? 😊
```

✅ **Fase 0 validada.** O Gus respondeu em português, com identidade, mencionando componentes reais do sistema (Hub Qdrant, Mem0), usando modelo 100% local, sem APIs externas.

---

## ⚠️ Limitações conhecidas

| Limitação | Motivo |
|-----------|--------|
| Latência ~30s | CPU sem GPU. Com GPU onboard (M1/M2/M3, RTX) cai pra 2–5s |
| Respostas curtas | 512 tokens max. Gemma 1B é um modelo pequeno |
| System prompt truncado | Gus original tem ~11 KB. Truncado pra 3 KB pra caber |
| Sem tools / dispatcher | É prova de conceito, não o bot completo |
| Sem memória (Hub) | Não conecta no Qdrant ainda (isso é Fase 1+) |

---

## 🐣 Próximo passo: Fase 1

Na Fase 1, adicionamos:
- Microfone USB → captura de voz
- Librosa → análise de tom emocional (valência/arousal)
- Fita LED WS2812B → resposta visual
- Loop: fala → detecta emoção → muda cor da luz

**Hardware adicional:** ~R$100–200  
**Tempo estimado:** 2–4 semanas  

---

## 📁 Arquivos

- `fase0_gus_local.py` — Script principal da Fase 0
- `../Gus/gus/system_prompt.md` — System prompt do Gus (fonte)
