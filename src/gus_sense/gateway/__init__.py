"""Sensor Gateway — transforma stream cru em fragmentos significativos.

90% filtro: só vira fragmento o que é EVENTO (foge da baseline), nunca leitura crua.
Ver docs/04-bloco-1-sensor-wearable.md.
"""
