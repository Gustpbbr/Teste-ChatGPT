"""Testes do schema gus-18 (tarefa T1).

Skipados até T1 implementar. Cada teste documenta a Definição de Pronto.
"""
import pytest

pytestmark = pytest.mark.skip(reason="T1: schema ainda não implementado")


def test_cria_fragmento_valido():
    from gus_sense.schema import Fragmento
    f = Fragmento(conteudo="oi", tipo="fato", area="saude")
    assert f.conteudo == "oi"


def test_rejeita_tipo_invalido():
    from gus_sense.schema import Fragmento
    with pytest.raises(ValueError):
        Fragmento(conteudo="x", tipo="inexistente")  # type: ignore[arg-type]


def test_clamp_confianca():
    from gus_sense.schema import Fragmento
    assert Fragmento(conteudo="x", confianca=5).confianca == 1.0


def test_conteudo_vazio_invalido():
    from gus_sense.schema import Fragmento
    with pytest.raises(ValueError):
        Fragmento(conteudo="")
