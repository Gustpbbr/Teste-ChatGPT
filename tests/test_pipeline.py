"""Testes do pipeline do Gateway — Bloco 1 (tarefa T7).

Skipados até T7 implementar.
"""
import pytest

pytestmark = pytest.mark.skip(reason="T7: pipeline ainda não implementado")


def test_stream_normal_zero_fragmentos():
    """Leituras normais -> Gateway.run_once() retorna []."""
    ...


def test_evento_gera_fragmento_sensivel():
    """Evento -> 1 fragmento gus-18 válido com metadata.sensivel=True."""
    ...


def test_hub_fora_vira_pendente_sem_quebrar():
    """Hub indisponível -> ingest 'pendente', pipeline não levanta."""
    ...
