import os
import logging
import psycopg2
import psycopg2.extras
from contextlib import contextmanager

logger = logging.getLogger(__name__)

def _get_dsn() -> str:
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL não configurado nas variáveis de ambiente!")
    return dsn

@contextmanager
def db():
    """Abre conexão, entrega cursor dict-like, commita e fecha automaticamente."""
    conn = psycopg2.connect(_get_dsn())
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Cria todas as tabelas necessárias se não existirem."""
    ddl = """
    CREATE TABLE IF NOT EXISTS media (
        id        SERIAL PRIMARY KEY,
        file_id   TEXT NOT NULL UNIQUE,
        tipo      TEXT NOT NULL,
        caption   TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS ranking (
        user_id    BIGINT PRIMARY KEY,
        nome       TEXT NOT NULL,
        pontos     INTEGER DEFAULT 0,
        msgs_hoje  INTEGER DEFAULT 0,
        ultimo_dia DATE
    );

    CREATE TABLE IF NOT EXISTS oracao (
        id        SERIAL PRIMARY KEY,
        nome      TEXT NOT NULL,
        user_id   BIGINT NOT NULL,
        pedido    TEXT NOT NULL,
        data      TEXT DEFAULT '',
        orado     BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS aniversarios (
        user_id  BIGINT PRIMARY KEY,
        nome     TEXT NOT NULL,
        dia      INTEGER NOT NULL,
        mes      INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS testemunhos (
        id        SERIAL PRIMARY KEY,
        nome      TEXT NOT NULL,
        user_id   BIGINT NOT NULL,
        texto     TEXT NOT NULL,
        data      TEXT DEFAULT '',
        publicado BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS avisos (
        user_id  BIGINT PRIMARY KEY,
        avisos   INTEGER DEFAULT 0,
        ultimo   TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS palavras_bloqueadas (
        palavra  TEXT PRIMARY KEY
    );
    """
    with db() as cur:
        cur.execute(ddl)
    logger.info("✅ Banco de dados inicializado com sucesso!")
