"""Testes do roteamento fail-closed (Bloco 3, B3-1)."""
import pytest

from gus_sense.routing import RotaBloqueada, route
from gus_sense.schema import Fragmento


def _frag(**kw):
    base = dict(conteudo="x", tipo="fato", area="projetos", via="claude-chat")
    base.update(kw)
    return Fragmento(**base)


def test_nao_sensivel_vai_pra_cloud():
    assert route(_frag(), local_disponivel=True) == "cloud"


def test_sensivel_com_local_disponivel_vai_pra_local():
    frag = _frag(area="saude", via="sensor-wearable")  # schema marca sensivel=True
    assert route(frag, local_disponivel=True) == "local"


def test_sensivel_sem_local_bloqueia_fail_closed():
    frag = _frag(area="dimagem")  # sensível por área
    with pytest.raises(RotaBloqueada):
        route(frag, local_disponivel=False)


def test_local_disponivel_aceita_callable():
    frag = _frag(area="dimagem")
    assert route(frag, local_disponivel=lambda: True) == "local"


def test_nunca_cai_pra_cloud_com_dado_sensivel():
    """Garantia central: sensível JAMAIS retorna 'cloud'."""
    frag = _frag(area="dimagem")
    try:
        rota = route(frag, local_disponivel=False)
    except RotaBloqueada:
        rota = "bloqueado"
    assert rota != "cloud"
