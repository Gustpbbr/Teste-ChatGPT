"""
Gus Local — Memória Persistente
================================
Armazenamento local de memórias (substituto offline do Hub Qdrant).
Usa SQLite como backend leve, schema compatível com gus-18.

Sem dependência de Qdrant Cloud — roda 100% offline.
"""

import sqlite3
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

DB_PATH = Path(__file__).parent / "gus_memory.db"


def _conn() -> sqlite3.Connection:
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    return db


def init_db():
    """Cria tabelas se não existirem."""
    db = _conn()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS memorias (
            id TEXT PRIMARY KEY,
            tipo TEXT NOT NULL DEFAULT 'fragmento',
            texto TEXT NOT NULL,
            fonte TEXT DEFAULT 'gus-local',
            tags TEXT DEFAULT '[]',
            importância REAL DEFAULT 0.5,
            criado_em TEXT NOT NULL,
            acessos INTEGER DEFAULT 0,
            checksum TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_tipo ON memorias(tipo);
        CREATE INDEX IF NOT EXISTS idx_criado ON memorias(criado_em);
        CREATE INDEX IF NOT EXISTS idx_importancia ON memorias(importância);
        CREATE TABLE IF NOT EXISTS contexto (
            chave TEXT PRIMARY KEY,
            valor TEXT,
            atualizado_em TEXT
        );
    """)
    db.commit()
    db.close()


def _checksum(texto: str) -> str:
    return hashlib.sha256(texto.encode()).hexdigest()[:16]


def lembrar(texto: str, tipo: str = "fragmento", tags: list = None,
            fonte: str = "gus-local", importancia: float = 0.5) -> str:
    """Armazena uma memória. Retorna o ID."""
    init_db()
    db = _conn()
    ck = _checksum(texto)
    
    # Evita duplicata exata
    existing = db.execute("SELECT id FROM memorias WHERE checksum = ?", (ck,)).fetchone()
    if existing:
        db.close()
        return existing["id"]
    
    mid = f"mem-{int(time.time()*1000)}-{ck[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    
    db.execute(
        """INSERT INTO memorias (id, tipo, texto, fonte, tags, importância, criado_em, checksum)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (mid, tipo, texto, fonte, json.dumps(tags or []), importancia, now, ck)
    )
    db.commit()
    db.close()
    return mid


def recordar(query: str = None, tipo: str = None, limite: int = 10) -> list[dict]:
    """Busca memórias. Se query, busca por palavra-chave no texto."""
    init_db()
    db = _conn()
    
    if query:
        # Busca simples por LIKE (substituto do embedding search)
        termos = query.lower().split()
        conditions = " OR ".join(["texto LIKE ?" for _ in termos])
        params = [f"%{t}%" for t in termos]
        
        if tipo:
            sql = f"SELECT * FROM memorias WHERE tipo = ? AND ({conditions}) ORDER BY importância DESC, criado_em DESC LIMIT ?"
            params = [tipo] + params + [limite]
        else:
            sql = f"SELECT * FROM memorias WHERE {conditions} ORDER BY importância DESC, criado_em DESC LIMIT ?"
            params = params + [limite]
    else:
        if tipo:
            sql = "SELECT * FROM memorias WHERE tipo = ? ORDER BY criado_em DESC LIMIT ?"
            params = [tipo, limite]
        else:
            sql = "SELECT * FROM memorias ORDER BY criado_em DESC LIMIT ?"
            params = [limite]
    
    rows = db.execute(sql, params).fetchall()
    
    # Atualiza contador de acesso
    ids = [r["id"] for r in rows]
    if ids:
        db.executemany("UPDATE memorias SET acessos = acessos + 1 WHERE id = ?", [(i,) for i in ids])
        db.commit()
    
    db.close()
    return [dict(r) for r in rows]


def contexto_set(chave: str, valor: str):
    """Armazena valor de contexto."""
    init_db()
    db = _conn()
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT OR REPLACE INTO contexto (chave, valor, atualizado_em) VALUES (?, ?, ?)",
        (chave, valor, now)
    )
    db.commit()
    db.close()


def contexto_get(chave: str) -> Optional[str]:
    """Recupera valor de contexto."""
    init_db()
    db = _conn()
    row = db.execute("SELECT valor FROM contexto WHERE chave = ?", (chave,)).fetchone()
    db.close()
    return row["valor"] if row else None


def stats() -> dict:
    """Estatísticas da memória local."""
    init_db()
    db = _conn()
    total = db.execute("SELECT COUNT(*) as n FROM memorias").fetchone()["n"]
    por_tipo = db.execute(
        "SELECT tipo, COUNT(*) as n FROM memorias GROUP BY tipo ORDER BY n DESC"
    ).fetchall()
    db.close()
    return {
        "total_memorias": total,
        "por_tipo": [{"tipo": r["tipo"], "quantidade": r["n"]} for r in por_tipo],
        "db_path": str(DB_PATH),
        "db_size_kb": round(DB_PATH.stat().st_size / 1024, 1) if DB_PATH.exists() else 0,
    }
