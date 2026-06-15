"""Testes da interocepção — Bloco 0 (tarefa T6).

Skipados até T6 implementar.
"""
import pytest

pytestmark = pytest.mark.skip(reason="T6: interocepção ainda não implementada")


def test_hub_fora_retorna_erro_sem_excecao():
    """Degradável: Hub mudo -> severidade='erro', sem levantar exceção."""
    ...


def test_curador_silencioso_gera_warn():
    """Sem escrita há 7h -> severidade='warn'."""
    ...


def test_anti_spam_emite_so_na_transicao():
    """Degradação contínua gera UM auto-fragmento, não um por check."""
    ...


def test_auto_fragmento_vai_pro_brain_gus():
    """emit_self_fragment escreve com user_id='gus', nunca 'gustavo'."""
    ...
