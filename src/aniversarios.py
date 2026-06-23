import logging
from datetime import datetime
from database import db

logger = logging.getLogger(__name__)

def registrar_aniversario(user_id: int, nome: str, dia: int, mes: int):
    try:
        with db() as cur:
            cur.execute("""
                INSERT INTO aniversarios (user_id, nome, dia, mes)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                    SET nome = EXCLUDED.nome,
                        dia  = EXCLUDED.dia,
                        mes  = EXCLUDED.mes
            """, (user_id, nome, dia, mes))
        logger.info(f"Aniversário registrado: {nome} {dia}/{mes}")
    except Exception as e:
        logger.error(f"Erro ao registrar aniversário: {e}")

def get_aniversariantes_hoje():
    hoje = datetime.now()
    try:
        with db() as cur:
            cur.execute(
                "SELECT user_id, nome, dia, mes FROM aniversarios WHERE dia = %s AND mes = %s",
                (hoje.day, hoje.month)
            )
            rows = cur.fetchall()
        return [(str(r["user_id"]), r["nome"], r["dia"], r["mes"]) for r in rows]
    except Exception as e:
        logger.error(f"Erro ao buscar aniversariantes: {e}")
        return []

def get_aniversario(user_id: int):
    try:
        with db() as cur:
            cur.execute(
                "SELECT nome, dia, mes FROM aniversarios WHERE user_id = %s",
                (user_id,)
            )
            row = cur.fetchone()
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Erro ao buscar aniversário: {e}")
        return None

def total_cadastrados() -> int:
    try:
        with db() as cur:
            cur.execute("SELECT COUNT(*) AS n FROM aniversarios")
            return cur.fetchone()["n"]
    except Exception as e:
        logger.error(f"Erro ao contar aniversários: {e}")
        return 0
