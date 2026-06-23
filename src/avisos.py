import logging
from datetime import datetime
from database import db

logger = logging.getLogger(__name__)

def registrar_aviso(user_id: int) -> int:
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    try:
        with db() as cur:
            cur.execute("""
                INSERT INTO avisos (user_id, avisos, ultimo)
                VALUES (%s, 1, %s)
                ON CONFLICT (user_id) DO UPDATE
                    SET avisos = avisos.avisos + 1,
                        ultimo = EXCLUDED.ultimo
                RETURNING avisos
            """, (user_id, agora))
            return cur.fetchone()["avisos"]
    except Exception as e:
        logger.error(f"Erro ao registrar aviso: {e}")
        return 0

def get_avisos(user_id: int) -> int:
    try:
        with db() as cur:
            cur.execute("SELECT avisos FROM avisos WHERE user_id = %s", (user_id,))
            row = cur.fetchone()
        return row["avisos"] if row else 0
    except Exception as e:
        logger.error(f"Erro ao buscar avisos: {e}")
        return 0

def resetar_avisos(user_id: int):
    try:
        with db() as cur:
            cur.execute("UPDATE avisos SET avisos = 0 WHERE user_id = %s", (user_id,))
        logger.info(f"Avisos de {user_id} resetados.")
    except Exception as e:
        logger.error(f"Erro ao resetar avisos: {e}")
