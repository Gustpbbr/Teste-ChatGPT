"""Testes do HubClient degradável (tarefa T2)."""
from gus_sense.hub_client import HubClient
from gus_sense.schema import Fragmento


def _frag():
    return Fragmento(conteudo="x", tipo="fato", area="projetos", via="claude-chat")


def test_sem_url_e_sem_transport_retorna_pendente():
    res = HubClient(url="").ingestar(_frag())
    assert res.status == "pendente"
    assert res.id is None


def test_transport_ok_marca_ultima_escrita():
    hub = HubClient(transport=lambda frag: "frag-123")
    res = hub.ingestar(_frag())
    assert res.status == "ok"
    assert res.id == "frag-123"
    assert hub.ultima_escrita() is not None


def test_transport_falha_vira_pendente_e_tenta_4x():
    tentativas = {"n": 0}

    def transporte_quebrado(frag):
        tentativas["n"] += 1
        raise ConnectionError("hub fora")

    hub = HubClient(transport=transporte_quebrado, sleep=lambda _d: None)
    res = hub.ingestar(_frag())
    assert res.status == "pendente"
    assert tentativas["n"] == 4          # retry 4x, sem propagar exceção
    assert hub.ultima_escrita() is None


def test_health_com_probe():
    assert HubClient(health_probe=lambda: True).health() is True
    assert HubClient(health_probe=lambda: False).health() is False


def test_health_nunca_levanta():
    def probe_quebrado():
        raise RuntimeError("boom")

    assert HubClient(health_probe=probe_quebrado).health() is False
