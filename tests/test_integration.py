"""Testes de integração — fluxo end-to-end Blocos 0+1 (tarefa T8).

Cobre os critérios de sucesso dos docs 03 e 04 com componentes reais ligados.
"""
from gus_sense.gateway.filters import Baseline
from gus_sense.gateway.pipeline import Gateway
from gus_sense.gateway.sensors import WearableSensor
from gus_sense.hub_client import HubClient
from gus_sense.interocepcao import check_all, emit_self_fragment

_BASELINES = {
    "hr": Baseline("hr", media_7d=62),
    "sleep": Baseline("sleep", media_7d=7),
    "hrv": Baseline("hrv", media_7d=60),
}
_EVENTO = "tests/fixtures/wearable-evento.json"
_NORMAL = "tests/fixtures/wearable-mock.json"


def _ident(s: str) -> str:
    return s


def test_fluxo_sensor_ate_hub_com_evento():
    """sensor (evento) -> gateway -> hub: fragmento sensível chega no Hub."""
    capturados = []

    def transporte(frag):
        capturados.append(frag)
        return "id-1"

    hub = HubClient(transport=transporte)
    g = Gateway([WearableSensor(_EVENTO)], hub, _ident, _BASELINES)
    frags = g.run_once()
    assert len(frags) == 1
    assert frags[0].metadata["sensivel"] is True
    assert len(capturados) == 1            # de fato ingerido


def test_fluxo_silencio_nao_polui_hub():
    """sensor (normal) -> gateway -> hub: zero fragmentos (anti-memória-lixão)."""
    capturados = []

    def transporte(frag):
        capturados.append(frag)
        return "x"

    g = Gateway([WearableSensor(_NORMAL)], HubClient(transport=transporte), _ident, _BASELINES)
    assert g.run_once() == []
    assert capturados == []


def test_fluxo_degrada_com_hub_fora():
    """Hub fora -> pipeline não quebra, fragmento ainda é produzido."""
    g = Gateway([WearableSensor(_EVENTO)], HubClient(url=""), _ident, _BASELINES)
    assert len(g.run_once()) == 1


def test_interocepcao_detecta_degradacao_e_registra_no_brain_gus():
    """Hub doente -> check_all acusa -> auto-fragmentos no brain 'gus'."""
    capturados = []

    class HubDoente:
        def health(self):
            return False

        def ultima_escrita(self):
            return None

        def ingestar(self, frag):
            capturados.append(frag)

    hub = HubDoente()
    estado: dict[str, str] = {}
    emitidos = [emit_self_fragment(h, hub, estado) for h in check_all(hub)]
    emitidos = [e for e in emitidos if e is not None]
    assert emitidos
    assert all(e.user_id == "gus" for e in emitidos)
    assert len(capturados) == len(emitidos)
