"""Testes dos filtros do Gateway (tarefa T3) — o coração anti-memória-lixão."""
from datetime import datetime, timedelta, timezone

from gus_sense.gateway.filters import Baseline, Window, denoise, detect_events, windowize
from gus_sense.gateway.sensors import Reading

_BASE = datetime(2026, 6, 15, 6, 0, tzinfo=timezone.utc)


def _hr(valores):
    return [Reading("hr", v, _BASE + timedelta(seconds=i), "bpm") for i, v in enumerate(valores)]


def test_leitura_normal_nao_gera_evento():
    """Anti-memória-lixão: stream dentro da baseline -> zero eventos."""
    w = denoise(Window("hr", _hr([61, 62, 63, 62, 61])))
    assert detect_events(w, Baseline("hr", media_7d=62)) == []


def test_pico_sustentado_gera_um_evento():
    """HR alto sustentado -> exatamente 1 evento."""
    w = denoise(Window("hr", _hr([109, 110, 111, 110, 112])))
    eventos = detect_events(w, Baseline("hr", media_7d=62))
    assert len(eventos) == 1
    assert eventos[0].severidade == "atencao"


def test_outlier_isolado_e_ignorado():
    """Um spike único (ruído) é descartado pelo denoise e não vira evento."""
    w = denoise(Window("hr", _hr([62, 61, 63, 200, 62])))
    assert detect_events(w, Baseline("hr", media_7d=62)) == []


def test_sono_curto_gera_evento():
    w = denoise(Window("sleep", [Reading("sleep", 4.2, _BASE, "h")]))
    assert len(detect_events(w, Baseline("sleep", media_7d=7))) == 1


def test_windowize_separa_por_metrica():
    readings = _hr([62, 63]) + [Reading("sleep", 7.0, _BASE, "h")]
    janelas = list(windowize(readings, seconds=60))
    metricas = {j.metric for j in janelas}
    assert metricas == {"hr", "sleep"}
