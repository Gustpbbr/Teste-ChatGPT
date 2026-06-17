# Componentes mínimos por tipo de IA

---

## 1. IA Inquisitiva

| Componente | Função | Custo |
|-----------|--------|-------|
| LLM (Gemma 4B) | Gerar perguntas socráticas | Grátis |
| Prompt system (maior componente) | Lógica: nunca responder, sempre perguntar | 0 |
| Histórico da sessão | Saber o que já perguntou | 0 |

**Mínimo real:** Um system prompt bem escrito. Zero código extra.
```
System: "Você é Sócrates. NUNCA responda diretamente. 
Faça exatamente uma pergunta por turno que leve o usuário 
a descobrir a resposta sozinho."
```

---

## 2. IA de Esquecimento

| Componente | Função | Custo |
|-----------|--------|-------|
| Banco vetorial (Qdrant/Chroma) | Onde as memórias moram | Grátis |
| Decay function | Reduz peso de memórias com o tempo | 10 linhas |
| Classificador de relevância | Decidir o que NÃO esquecer | Modelo leve ou heurística |
| Threshold de deleção | Peso < X → deletar | 1 linha |

**Mínimo real:** Qdrant + função de decaimento exponencial + regra simples ("se peso < 0.3 e idade > 30 dias, deleta"). ~50 linhas de Python.

---

## 3. IA de Desacordo

| Componente | Função | Custo |
|-----------|--------|-------|
| 2+ LLMs (ou 1 com 2 system prompts) | Agentes com perspectivas opostas | Grátis (Ollama) |
| Prompt de persona (x2) | Definir posições divergentes | 0 |
| Orquestrador | Revelar as respostas lado a lado | 30 linhas |
| Interface de exibição | Mostrar o debate (não resolver) | HTML simples |

**Mínimo real:** Dois prompts diferentes no mesmo modelo, chamadas paralelas, exibição lado a lado. ~80 linhas.

---

## 4. IA Olfativa

| Componente | Função | Custo |
|-----------|--------|-------|
| Sensor de gás (MQ-135, BME680) | Capturar VOCs, CO2, umidade | ~R$ 30 |
| Microcontrolador (ESP32) | Ler sensor → enviar dados | ~R$ 40 |
| Normalizador | Converter leitura bruta → vetor | 20 linhas |
| Embeddings de cheiro | Mapear padrões → categorias | Treino simples ou heurística |
| Classificador | "hospital", "café", "chuva", "suor" | Modelo leve |

**Mínimo real:** ESP32 + MQ-135 + heurística de thresholds. 1 sensor resolve 80% (detecta "mudança de ambiente"). ~100 linhas Python + código Arduino.

---

## 5. IA Proprioceptiva

| Componente | Função | Custo |
|-----------|--------|-------|
| Smartwatch/smartband (qualquer) | FC, movimento, sono | Já tem? |
| Ou: câmera + OpenCV + rPPG | Extrair batimento de vídeo do rosto | Grátis |
| Agregador temporal | "Últimos 5 min: FC média, variabilidade" | 30 linhas |
| Limiares de alerta | FC > X, imóvel > Y min, padrão anômalo | 20 linhas |
| Emissor de VSE (ACEE) | Estado fisiológico → emoção inferida | Já existe (IL-Voz) |

**Mínimo real:** Câmera do S20 + rPPG (extrai FC do rosto por vídeo) + thresholds. Zero hardware extra. ~150 linhas Python.

---

## 6. IA de Silêncio

| Componente | Função | Custo |
|-----------|--------|-------|
| Agregador de eventos | Registrar última vez que X aconteceu | SQLite |
| Cron interno | Verificar periodicamente o que NÃO aconteceu | Cron job |
| Regras de ausência | "Y não acontece há Z horas → alerta" | 30 linhas |
| Limiar de relevância | Nem toda ausência importa | Heurística |

**Mínimo real:** SQLite + cron a cada 5 min + SELECT de eventos com timestamp velho. ~60 linhas Python.

---

## 7. IA Cíclica

| Componente | Função | Custo |
|-----------|--------|-------|
| Fila de entrada | Acumular eventos enquanto dorme | SQLite ou Redis |
| Trigger de despertar | Timer ou evento crítico | Cron |
| Fase de digestão | Processar fila acumulada | 1 chamada LLM |
| Fase de decisão | "Devo agir? Devo falar?" | 1 chamada LLM |
| Fase de sono | Voltar a acumular | Loop |

**Mínimo real:** Loop infinito com sleep + fila SQLite. Acumula por X minutos, processa tudo de uma vez, volta a dormir. ~100 linhas Python.

---

## 8. IA Localizada

| Componente | Função | Custo |
|-----------|--------|-------|
| Dispositivo dedicado | Onde ela "mora" | S20 (já tem) |
| Memória local (SQLite) | História específica desse dispositivo | Já existe (gus_local) |
| Sensores locais | Câmera, microfone, GPS, acelerômetro | Já tem no S20 |
| Identidade persistente | Nome, tom, memórias que não resetam | Arquivo de config |
| Sem nuvem | Tudo roda local | Ollama |

**Mínimo real:** É exatamente o gus_local + gus_voice que já criamos. Já está ~80% pronto.

---

## Resumo: ranking de dificuldade

| IA | Complexidade | Hardware extra | Tempo estimado |
|----|-------------|---------------|----------------|
| Inquisitiva | ⭐ | Nenhum | 1 dia |
| Esquecimento | ⭐ | Nenhum | 2 dias |
| Desacordo | ⭐ | Nenhum | 2 dias |
| Silêncio | ⭐⭐ | Nenhum | 2 dias |
| Cíclica | ⭐⭐ | Nenhum | 3 dias |
| Localizada | ⭐⭐ | Nenhum | Já 80% feito |
| Proprioceptiva | ⭐⭐⭐ | Câmera (já tem) | 1 semana |
| Olfativa | ⭐⭐⭐⭐ | Sensor + ESP32 | 2 semanas |
