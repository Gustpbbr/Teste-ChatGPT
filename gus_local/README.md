# Gus Local v1.0

> Gus completo offline: IA local + memória persistente + API REST.

## Instalar

```bash
pip install fastapi uvicorn requests
ollama pull gemma3:4b
```

## Executar

```bash
bash start.sh
# → http://localhost:8080
# → http://localhost:8080/docs (Swagger)
```

## Endpoints

| Método | Rota | Função |
|--------|------|--------|
| GET | `/health` | Status (Ollama + memória) |
| POST | `/chat` | Chat com memória automática |
| POST | `/memory/add` | Adicionar memória |
| GET | `/memory/search?q=` | Buscar memórias |
| GET | `/memory/stats` | Estatísticas |
| POST | `/config` | Salvar configuração |
| GET | `/config/{chave}` | Ler configuração |

## Diferenciais

- Memória automática: cada conversa gera fatos extraídos
- Busca por palavra-chave (substituto do embedding search)
- Zero APIs externas após download do modelo
- Schema compatível com gus-18

## Arquivos

- `server.py` — API FastAPI
- `memory.py` — Banco SQLite local
- `start.sh` — Inicializador unificado
