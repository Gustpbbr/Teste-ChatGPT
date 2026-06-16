# 06 — Roadmap MASE: Da Prova de Conceito ao Protótipo

> Plano de prototipagem progressiva do dispositivo multissensorial.
> Cada fase gera um vídeo demonstrável como ativo independente.

---

## 🥚 Fase 0 — Prova de Software (R$0, 1–2 semanas)

**O que prova:** O Gus funciona offline com IA local.

| Item | Especificação |
|------|--------------|
| Hardware | Qualquer laptop ou celular existente (Galaxy S20 ideal) |
| Modelo | Gemma3:1b (815 MB) ou Gemma3:4b (2.5 GB) via Ollama |
| Software | Gus + Gemma local |
| Interface | Terminal (Termux) ou Web (Chrome → localhost:8080) |

**Métrica de sucesso:** Resposta coerente em PT-BR, com identidade Gus, **sem internet**.

**Arquivos:** `MASE/setup.sh`, `MASE/gus_web.py`, `MASE/fase0_gus_local.py`

✅ **Validado em 17/06/2026:** Servidor 4GB RAM, Gemma 1B, 29s de latência. No S20 com NPU: 3–8s.

---

## 🐣 Fase 1 — 1 Sensor + 1 Atuador (R$200–400, 2–4 semanas)

**O que prova:** Loop fechado: percepção → emoção → ação física.

| Componente | Especificação | Custo |
|-----------|---------------|-------|
| Cérebro | Galaxy S20 (existente) | R$0 |
| Entrada | Microfone nativo do S20 | R$0 |
| Ponte GPIO | Arduino Nano | R$40 |
| Saída | Fita LED RGB WS2812B (1m, 30 LEDs) | R$40 |
| Cabos | USB-C OTG + jumpers | R$30 |
| **Total** | | **~R$110** |

**Software:** VAD (detecção de voz) + análise de tom (Librosa) + Gemma local. Tom tenso → luz vermelha. Tom calmo → azul. Silêncio → laranja quente.

**Métrica de sucesso:** 1 vídeo de 60s mostrando fala → mudança de cor por emoção, offline.

---

## 🐤 Fase 2 — Sentidos Expandidos (R$500–1000, 1–2 meses)

**O que prova:** Múltiplos canais sensoriais + resposta coordenada.

| Componente | Especificação | Custo |
|-----------|---------------|-------|
| Sensor presença | PIR HC-SR501 ou ToF VL53L1X | R$15–60 |
| Ambiente | DHT22 (temp/umidade) + BH1750 (luz) | R$35 |
| LED ring | Anel 24 LEDs WS2812B | R$50 |
| Som | Speaker 3W + amplificador MAX98357A | R$60 |
| Display | OLED 128x64 | R$30 |
| Hub USB | Hub USB-C com power delivery | R$80 |
| **Total** | | **~R$300–400** |

**Software:** ACEE simplificado — cada sensor alimenta peso de humor. Gemma recebe contexto enriquecido. Resposta coordenada luz + som ambiente.

**Métrica de sucesso:** Chegar em casa → sensor PIR detecta → LED acende quente + speaker toca som relaxante. Automático.

---

## 🐔 Fase 3 — Projeção + Interface Avançada (R$2000–4000, 2–3 meses)

**O que prova:** Experiência visual/espacial — o "efeito uau".

| Componente | Especificação | Custo |
|-----------|---------------|-------|
| Projetor | Mini DLP (AnyBeam Pico ou similar) | R$1000–1500 |
| Névoa | Umidificador ultrassônico modificado | R$80 |
| Câmera | Webcam USB com IR | R$150 |
| Plataforma | Servo MG996R + base impressa 3D | R$100 |
| Áudio | Upgrade: 2 speakers para beamforming | R$100 |
| Opcional | Chip aroma (PTC + essência sólida) | R$50 |
| **Total** | | **~R$1500–2000** |

**Software:** OpenCV tracking facial + correção keystone + sincronização áudio-visual. Projeção segue o rosto.

**Métrica de sucesso:** Vídeo mostrando projeção flutuante que segue o rosto, som direcional, luz sincronizada.

---

## 🦅 Fase 4 — Dispositivo Integrado (R$5000–15000, 4–6 meses)

**O que prova:** MASE completo em formato de protótipo apresentável.

| Componente | Especificação |
|-----------|---------------|
| Carcaça | Impressão 3D (PLA/PETG) ou CNC alumínio |
| Computação | Jetson Orin Nano ou mini PC x86 |
| Sensores | Array microfones 4ch, câmera RGB+IR, sensores ambientais |
| Atuadores | Projetor DLP/Laser, LED ring, speaker array, chip aroma, servo |
| Conectividade | WiFi + BLE + Zigbee (casa inteligente) |
| Software | Gus + ACEE + MASE integrados (pipeline completo) |

**Métrica de sucesso:** 1 unidade funcional demonstrável em eventos (Maker Faire, CES, etc.).

---

## 📊 Visão Consolidada

```
FASE 0 ──── FASE 1 ──── FASE 2 ──── FASE 3 ──── FASE 4
  R$0        R$110       R$400       R$2000      R$15000
  2 sem      4 sem       2 meses     3 meses     6 meses

  [POC]     [prova]     [sentidos]  [projeção]  [completo]
  software  percepção   expandidos  espacial    protótipo
  roda      + ação      multi-      visual      evento
  offline   física      sensor                 pronto
```

**Regra de ouro:** Cada fase só começa quando a anterior está validada. Cada fase gera um vídeo. Cada vídeo é um ativo independente para captação de recursos ou parcerias.

---

## 🔑 Diferencial do Galaxy S20

| Especificação | S20 | Raspberry Pi 5 |
|---------------|-----|----------------|
| RAM | 8–12 GB | 8 GB |
| NPU | ✅ Dedicada (5–10x mais rápida) | ❌ |
| Câmeras | 3–4 (wide, zoom, ToF) | ❌ (comprar) |
| Microfones | Array stereo (3+) | ❌ (comprar) |
| Sensores | Acelerômetro, giroscópio, prox, barômetro, batimento | ❌ (comprar) |
| Tela | 6.2" AMOLED | ❌ (comprar) |
| Bateria | ✅ Integrada | ❌ |
| Custo adicional | R$0 (hardware existente) | R$500–800 |

O S20 cobre **Fases 0–2 sem hardware adicional** (exceto Arduino + LED). Ideal como plataforma de prototipagem.
