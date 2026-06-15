"""Testes da fila de pendentes + replay (A5)."""
from gus_sense.fila import FilaPendentes, ingestar_com_fila
from gus_sense.hub_client import HubClient
from gus_sense.schema import Fragmento


def _frag():
    return Fragmento(conteudo="x", tipo="fato", area="projetos", via="telegram")


def test_hub_fora_enfileira():
    fila = FilaPendentes()
    status = ingestar_com_fila(HubClient(url=""), fila, _frag())  # sem URL -> pendente
    assert status == "pendente"
    assert len(fila.pendentes()) == 1


def test_replay_nao_envia_com_hub_fora():
    fila = FilaPendentes([_frag(), _frag()])
    hub = HubClient(health_probe=lambda: False)
    res = fila.replay(hub)
    assert res.enviados == 0
    assert res.restantes == 2


def test_replay_drena_com_hub_no_ar():
    fila = FilaPendentes([_frag(), _frag()])
    hub = HubClient(health_probe=lambda: True, transport=lambda f: "id")
    res = fila.replay(hub)
    assert res.enviados == 2
    assert res.restantes == 0
    assert fila.pendentes() == []


def test_replay_mantem_os_que_falham():
    fila = FilaPendentes([_frag()])
    # health ok, mas transport quebra -> ingest vira pendente -> permanece na fila
    def quebra(f):
        raise ConnectionError("boom")

    hub = HubClient(health_probe=lambda: True, transport=quebra, sleep=lambda _d: None)
    res = fila.replay(hub)
    assert res.enviados == 0
    assert res.restantes == 1
