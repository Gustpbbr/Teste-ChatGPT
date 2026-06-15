"""Testes de confiança/trust (A3)."""
from gus_sense.confianca import confirmar, proveniencia, refutar, trust
from gus_sense.schema import Fragmento


def _frag(conf=0.7):
    return Fragmento(conteudo="x", tipo="fato", area="projetos", via="telegram", confianca=conf)


def test_trust_parte_da_confianca():
    assert trust(_frag(0.7)) == 0.7


def test_confirmar_sobe_trust():
    f = _frag(0.5)
    confirmar(f)
    confirmar(f)
    assert trust(f) > 0.5


def test_refutar_baixa_trust():
    f = _frag(0.8)
    refutar(f)
    assert trust(f) < 0.8


def test_trust_clamped():
    f = _frag(0.9)
    for _ in range(10):
        confirmar(f)
    assert trust(f) == 1.0


def test_proveniencia_tem_via_e_trust():
    p = proveniencia(_frag())
    assert "via=" in p and "trust=" in p
