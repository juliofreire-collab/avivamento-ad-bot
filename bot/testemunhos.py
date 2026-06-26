import logging
from datetime import datetime
from database import db

logger = logging.getLogger(__name__)

def salvar_testemunho(nome: str, user_id: int, texto: str):
    try:
        with db() as cur:
            cur.execute("""
                INSERT INTO testemunhos (nome, user_id, texto, data, publicado)
                VALUES (%s, %s, %s, %s, FALSE)
            """, (nome, user_id, texto, datetime.now().strftime("%d/%m/%Y %H:%M")))
    except Exception as e:
        logger.error(f"Erro ao salvar testemunho: {e}")

def get_testemunhos_pendentes():
    try:
        with db() as cur:
            cur.execute("""
                SELECT id, nome, texto, data FROM testemunhos
                WHERE publicado = FALSE ORDER BY id ASC
            """)
            return [dict(r) for r in cur.fetchall()]
    except Exception as e:
        logger.error(f"Erro ao buscar testemunhos: {e}")
        return []

def get_proximo_testemunho_nao_publicado():
    try:
        with db() as cur:
            cur.execute("""
                SELECT id, nome, user_id, texto FROM testemunhos
                WHERE publicado = FALSE ORDER BY id ASC LIMIT 1
            """)
            row = cur.fetchone()
            if not row:
                return None
            t = dict(row)
            cur.execute("UPDATE testemunhos SET publicado = TRUE WHERE id = %s", (t["id"],))
            return t
    except Exception as e:
        logger.error(f"Erro ao buscar próximo testemunho: {e}")
        return None
