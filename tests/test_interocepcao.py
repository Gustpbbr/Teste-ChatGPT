"""Testes da interocepção — Bloco 0 (tarefa T6)."""
from datetime import datetime, timedelta, timezone

from gus_sense.interocepcao import (
    Health,
    curador_heartbeat,
    emit_self_fragment,
    hub_health,
)


class FakeHub:
    def __init__(self, ok=True, ultima=None):
        self._ok = ok
        self._ultima = ultima
        self.ingeridos = []

    def health(self):
        return self._ok

    def ultima_escrita(self):
        return self._ultima

    def ingestar(self, frag):
        self.ingeridos.append(frag)


def test_hub_fora_retorna_erro_sem_excecao():
    """Degradável: Hub mudo -> severidade='erro', sem levantar exceção."""
    assert hub_health(FakeHub(ok=False)).severidade == "erro"


def test_curador_silencioso_gera_warn():
    """Sem escrita há 7h -> severidade='warn'."""
    sete_h = datetime.now(timezone.utc) - timedelta(hours=7)
    assert curador_heartbeat(FakeHub(ultima=sete_h), janela_horas=6).severidade == "warn"


def test_curador_recente_fica_ok():
    agora = datetime.now(timezone.utc) - timedelta(minutes=10)
    assert curador_heartbeat(FakeHub(ultima=agora)).severidade == "ok"


def test_anti_spam_emite_so_na_transicao():
    """Degradação contínua gera UM auto-fragmento, não um por check."""
    estado: dict[str, str] = {}
    h = Health("curador", False, "última escrita há 7h", None, "warn")
    hub = FakeHub()
    primeiro = emit_self_fragment(h, hub, estado)
    segundo = emit_self_fragment(h, hub, estado)
    assert primeiro is not None
    assert segundo is None
    assert len(hub.ingeridos) == 1


def test_auto_fragmento_vai_pro_brain_gus():
    """emit_self_fragment escreve com user_id='gus', nunca 'gustavo'."""
    h = Health("hub", False, "Hub não responde", None, "erro")
    frag = emit_self_fragment(h, FakeHub(), estado={})
    assert frag is not None
    assert frag.user_id == "gus"
    assert frag.tipo == "meta_reflexao"
