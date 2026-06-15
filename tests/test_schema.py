"""Testes do schema gus-18 (tarefa T1). Implementação de referência."""
import pytest

from gus_sense.schema import Fragmento, validar


def test_cria_fragmento_valido():
    f = Fragmento(conteudo="oi", tipo="fato", area="saude")
    assert f.conteudo == "oi"
    assert f.tipo == "fato"


def test_rejeita_tipo_invalido():
    with pytest.raises(ValueError):
        Fragmento(conteudo="x", tipo="inexistente")  # type: ignore[arg-type]


def test_rejeita_user_id_invalido():
    with pytest.raises(ValueError):
        Fragmento(conteudo="x", user_id="alguem")  # type: ignore[arg-type]


def test_clamp_confianca():
    assert Fragmento(conteudo="x", confianca=5).confianca == 1.0
    assert Fragmento(conteudo="x", confianca=-3).confianca == 0.0


def test_conteudo_vazio_invalido():
    with pytest.raises(ValueError):
        Fragmento(conteudo="")
    with pytest.raises(ValueError):
        Fragmento(conteudo="   ")


def test_biometria_de_sensor_nasce_sensivel():
    f = Fragmento(conteudo="HR alto", area="saude", via="sensor-wearable")
    assert f.metadata["sensivel"] is True


def test_dimagem_nasce_sensivel():
    f = Fragmento(conteudo="caso X", area="dimagem", tipo="fato")
    assert f.metadata["sensivel"] is True


def test_fragmento_comum_nao_sensivel_por_default():
    f = Fragmento(conteudo="nota", area="projetos", tipo="fato", via="claude-chat")
    assert f.metadata["sensivel"] is False


def test_validar_idempotente():
    f = Fragmento(conteudo="oi", tipo="fato")
    assert validar(f).conteudo == "oi"
