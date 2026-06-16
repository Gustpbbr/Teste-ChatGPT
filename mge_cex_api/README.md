# MGE/CEX API v2.0

> Motor de Geração Estruturada + Comitê de Especialistas Universais.
> Versão FastAPI — substitui os HTML standalone.

## Instalação

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Executar

```bash
uvicorn server:app --host 0.0.0.0 --port 8765
```

## Endpoints

| Método | Rota | Função |
|--------|------|--------|
| GET | `/health` | Status do serviço |
| POST | `/mge/generate` | Geração multi-agente (5-10 agentes) |
| POST | `/cex/review` | Cross-examination (até 6 dimensões) |

## Exemplo MGE

```bash
curl -X POST http://localhost:8765/mge/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Proponha ideias para IA em educação","num_agentes":5}'
```

## Exemplo CEX

```bash
curl -X POST http://localhost:8765/cex/review \
  -H "Content-Type: application/json" \
  -d '{"texto":"texto a ser revisado...","criterios":["factual","logico","etico"]}'
```

## Agentes MGE

criativo, critico, sintetizador, pratico, etico, tecnico, empatico, estrategista, curador, provocador

## Dimensões CEX

factual, logico, etico, clareza, criativo, tecnico

## Teste

```bash
python3 test_client.py
```
