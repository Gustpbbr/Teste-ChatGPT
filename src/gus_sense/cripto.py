"""A4 — Criptografia em repouso para fragmentos sensíveis.

Rota local protege o processamento; isto protege o ARMAZENAMENTO (LGPD).
Conteúdo sensível é cifrado antes de gravar e só decifra na rota local.

Chave vem de env `GUS_CRYPTO_KEY` (Fernet, base64 urlsafe de 32 bytes). NUNCA
versionar a chave. `cryptography` é importado preguiçosamente (só quem cifra precisa).
"""
from __future__ import annotations

import os

from .schema import Fragmento


class CriptoIndisponivel(Exception):
    """Chave ausente, token inválido, ou tentativa de decifrar fora da rota local."""


def gerar_chave() -> str:
    from cryptography.fernet import Fernet

    return Fernet.generate_key().decode()


def _fernet(key: str | None):
    from cryptography.fernet import Fernet

    k = key or os.getenv("GUS_CRYPTO_KEY")
    if not k:
        raise CriptoIndisponivel("GUS_CRYPTO_KEY ausente — fail-closed")
    return Fernet(k.encode() if isinstance(k, str) else k)


def cifrar(texto: str, key: str | None = None) -> str:
    return _fernet(key).encrypt(texto.encode()).decode()


def decifrar(token: str, key: str | None = None) -> str:
    from cryptography.fernet import InvalidToken

    try:
        return _fernet(key).decrypt(token.encode()).decode()
    except InvalidToken as e:
        raise CriptoIndisponivel("token inválido ou chave errada") from e


def proteger(frag: Fragmento, key: str | None = None) -> Fragmento:
    """Cifra o conteúdo se o fragmento for sensível. Idempotente."""
    if frag.metadata.get("sensivel") and not frag.metadata.get("cifrado"):
        frag.conteudo = cifrar(frag.conteudo, key)
        frag.metadata["cifrado"] = True
    return frag


def revelar(frag: Fragmento, rota: str, key: str | None = None) -> str:
    """Retorna o conteúdo em claro. Sensível só decifra na rota 'local' (fail-closed)."""
    if not frag.metadata.get("cifrado"):
        return frag.conteudo
    if rota != "local":
        raise CriptoIndisponivel("conteúdo sensível só decifra na rota local")
    return decifrar(frag.conteudo, key)
