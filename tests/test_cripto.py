"""Testes de criptografia em repouso (A4)."""
import pytest

from gus_sense.cripto import (
    CriptoIndisponivel,
    cifrar,
    decifrar,
    gerar_chave,
    proteger,
    revelar,
)
from gus_sense.schema import Fragmento


def test_roundtrip():
    k = gerar_chave()
    assert decifrar(cifrar("segredo", k), k) == "segredo"


def test_chave_errada_falha():
    with pytest.raises(CriptoIndisponivel):
        decifrar(cifrar("segredo", gerar_chave()), gerar_chave())


def test_sem_chave_fail_closed():
    with pytest.raises(CriptoIndisponivel):
        cifrar("x", key=None)  # sem env GUS_CRYPTO_KEY


def test_proteger_cifra_sensivel():
    k = gerar_chave()
    f = Fragmento(conteudo="HR alto", area="saude", via="sensor-wearable")  # sensivel=True
    proteger(f, k)
    assert f.metadata["cifrado"] is True
    assert f.conteudo != "HR alto"


def test_revelar_so_na_rota_local():
    k = gerar_chave()
    f = proteger(Fragmento(conteudo="HR alto", area="saude", via="sensor-wearable"), k)
    with pytest.raises(CriptoIndisponivel):
        revelar(f, "cloud", k)
    assert revelar(f, "local", k) == "HR alto"


def test_nao_sensivel_nao_cifra():
    k = gerar_chave()
    f = Fragmento(conteudo="nota", area="projetos", via="telegram")  # sensivel=False
    proteger(f, k)
    assert f.metadata.get("cifrado") is not True
    assert revelar(f, "cloud") == "nota"
