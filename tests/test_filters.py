"""Testes dos filtros do Gateway (tarefa T3) — o coração anti-memória-lixão.

Skipados até T3 implementar.
"""
import pytest

pytestmark = pytest.mark.skip(reason="T3: filtros ainda não implementados")


def test_leitura_normal_nao_gera_evento():
    """Anti-memória-lixão: stream dentro da baseline -> zero eventos."""
    ...


def test_pico_sustentado_gera_um_evento():
    """HR alto sustentado por >15min -> exatamente 1 evento."""
    ...


def test_outlier_isolado_e_ignorado():
    """Um spike único (ruído) não vira evento."""
    ...
