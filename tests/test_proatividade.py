"""Testes do núcleo de proatividade (Bloco 5)."""
from datetime import datetime, timedelta, timezone

from gus_sense.proatividade import (
    analisar,
    detectar_acumulo_esquecidos,
    detectar_lacuna,
)
from gus_sense.schema import Fragmento

_AGORA = datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc)


def _frag(area, estado="ativo", idade_h=0):
    f = Fragmento(conteudo="x", tipo="fato", area=area, via="telegram")
    f.estado = estado
    f.criado_em = _AGORA - timedelta(hours=idade_h)
    return f


def test_lacuna_quando_area_vazia():
    s = detectar_lacuna([], "saude", _AGORA)
    assert s is not None and s.tipo == "lacuna"


def test_lacuna_quando_silencio_longo():
    frags = [_frag("saude", idade_h=72)]
    s = detectar_lacuna(frags, "saude", _AGORA, max_silencio_h=48)
    assert s is not None


def test_sem_lacuna_com_registro_recente():
    frags = [_frag("saude", idade_h=2)]
    assert detectar_lacuna(frags, "saude", _AGORA, max_silencio_h=48) is None


def test_acumulo_esquecidos():
    frags = [_frag("capturado", estado="esquecido") for _ in range(5)]
    sinais = detectar_acumulo_esquecidos(frags, limiar=5)
    assert len(sinais) == 1
    assert sinais[0].area == "capturado"


def test_acumulo_abaixo_do_limiar_nao_sinaliza():
    frags = [_frag("capturado", estado="esquecido") for _ in range(3)]
    assert detectar_acumulo_esquecidos(frags, limiar=5) == []


def test_analisar_combina_detectores():
    frags = [_frag("esportes", idade_h=200)] + [
        _frag("capturado", estado="esquecido") for _ in range(5)
    ]
    sinais = analisar(frags, ["esportes", "saude"], _AGORA)
    tipos = {s.tipo for s in sinais}
    assert "lacuna" in tipos
    assert "acumulo_esquecidos" in tipos
