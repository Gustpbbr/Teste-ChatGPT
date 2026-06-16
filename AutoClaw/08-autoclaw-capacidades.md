# 08 — AutoClaw: Capacidades e Limitações

> Análise do próprio assistente — o que pode e não pode fazer.
> Relevante para entender o que delegar e o que esperar.

---

## 🧠 Modelo e Infraestrutura

| Característica | Valor |
|---------------|-------|
| **Motor** | Z.AI / GLM-5.x (Zhipu AI / AutoGLM) |
| **Fabricante** | Chinês (Tsinghua) |
| **Servidor** | Asia/Shanghai |
| **RAM** | 4 GB |
| **CPU** | 2 cores x86_64 |
| **GPU** | Nenhuma |
| **Disco** | ~30 GB |

---

## ✅ Capacidades

### Sistema de Arquivos
- ✅ Leitura e escrita de arquivos no workspace
- ✅ Criação de diretórios, scripts, documentos
- ✅ Git (clone, commit, push, pull)

### Execução
- ✅ Shell e Python (síncrono e background)
- ✅ Sub-agentes (spawn de tarefas isoladas)
- ✅ Cron jobs (tarefas agendadas)

### Rede
- ✅ Web fetch (URLs específicas)
- ❌ Busca web (bloqueada pelo admin)
- ❌ Navegador (bloqueado pelo admin)
- ✅ Download de arquivos (Google Drive, etc.)

### Mensageria
- ✅ Envio de mensagens (Telegram, Discord, etc.)
- ✅ Notificações proativas

### Memória e Identidade
- ✅ Diário (`memory/YYYY-MM-DD.md`)
- ✅ Memória de longo prazo (`MEMORY.md`)
- ✅ Personalidade (`SOUL.md`, `IDENTITY.md`)
- ✅ Preferências do usuário (`USER.md`, `TOOLS.md`)
- ✅ Heartbeats (verificações periódicas)

### Interface
- ✅ Chat web (OpenClaw Control UI)
- ✅ Canvas/embeds
- ✅ TTS (text-to-speech)

### Nodes (dispositivos pareados)
- ✅ Câmera, localização, notificações (se pareado)

---

## ❌ Limitações

| Limitação | Impacto |
|-----------|---------|
| Sem busca web | Não pesquisa no Google, não acessa notícias em tempo real |
| Sem navegador | Não renderiza páginas, não interage com web apps |
| Sem GPU | Inferência local lenta (~29s para Gemma 1B) |
| 4 GB RAM | Modelos locais limitados a ~1B parâmetros |
| Modelo chinês | Pode ter vieses diferentes de GPT/Claude |
| Config travada | Web search e browser bloqueados pelo admin |

---

## 🆚 Comparação com Outros Assistentes

| Capacidade | AutoClaw | ChatGPT | Claude.ai |
|-----------|----------|---------|-----------|
| Shell/execução | ✅ | ❌ | ❌ |
| Sub-agentes | ✅ | ❌ | ❌ |
| Cron/agendamento | ✅ | ❌ | ❌ |
| Memória em arquivos | ✅ | Limitado | ❌ |
| Sistema de arquivos | ✅ | Limitado | Via MCP |
| Mensagens multiplataforma | ✅ | ❌ | ❌ |
| Busca web | ❌ | ✅ | ✅ (MCP) |
| Navegador | ❌ | ✅ | ❌ |
| Canvas/embeds | ✅ | ✅ (artifacts) | ✅ (artifacts) |
| Nodes (celular) | ✅ | ❌ | ❌ |

---

## 🤖 IA Local (Ollama)

Instalamos Ollama + Gemma 1B no servidor como prova de conceito:

| Modelo | Tamanho | Latência |
|--------|---------|----------|
| Gemma3:1b | 815 MB | ~29s (CPU only) |
| Gemma3:4b | 2.5 GB | Não testado (RAM insuficiente) |

⚠️ O servidor atual (4 GB RAM, sem GPU) é inadequado para inferência local em produção. O Galaxy S20 (12 GB + NPU) é ~5–10x mais rápido.

---

## 📝 Recomendações de Uso

**Delegar para o AutoClaw:**
- Análise de código e documentação
- Criação de arquivos, scripts, configurações
- Organização de repositórios
- Pesquisa em URLs específicas
- Download e processamento de arquivos
- Geração de documentação
- Git e versionamento

**Não delegar:**
- Tarefas que exigem busca web ampla
- Navegação em sites interativos
- Inferência local pesada
- Ações que exigem credenciais não fornecidas
