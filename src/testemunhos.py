import logging
from datetime import datetime
from database import db

logger = logging.getLogger(__name__)

def salvar_testemunho(user_name: str, user_id: int, texto: str) -> bool:
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    try:
        with db() as cur:
            cur.execute("""
                INSERT INTO testemunhos (nome, user_id, texto, data, publicado)
                VALUES (%s, %s, %s, %s, FALSE)
            """, (user_name, user_id, texto, data))
        logger.info(f"Testemunho salvo de {user_name}")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar testemunho: {e}")
        return False

def get_testemunhos_pendentes():
    try:
        with db() as cur:
            cur.execute(
                "SELECT id, nome, user_id, texto, data FROM testemunhos WHERE publicado = FALSE ORDER BY id"
            )
            rows = cur.fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"Erro ao buscar testemunhos pendentes: {e}")
        return []

def marcar_publicado(index: int):
    """Marca o N-ésimo testemunho pendente (0-indexado) como publicado."""
    try:
        with db() as cur:
            cur.execute(
                "SELECT id FROM testemunhos WHERE publicado = FALSE ORDER BY id LIMIT 1 OFFSET %s",
                (index,)
            )
            row = cur.fetchone()
            if row:
                cur.execute("UPDATE testemunhos SET publicado = TRUE WHERE id = %s", (row["id"],))
    except Exception as e:
        logger.error(f"Erro ao marcar testemunho como publicado: {e}")

def get_proximo_testemunho_nao_publicado():
    """Retorna o próximo testemunho pendente e o marca como publicado."""
    try:
        with db() as cur:
            cur.execute(
                "SELECT id, nome, user_id, texto, data FROM testemunhos WHERE publicado = FALSE ORDER BY id LIMIT 1"
            )
            row = cur.fetchone()
            if not row:
                return None
            cur.execute("UPDATE testemunhos SET publicado = TRUE WHERE id = %s", (row["id"],))
        return dict(row)
    except Exception as e:
        logger.error(f"Erro ao buscar próximo testemunho: {e}")
        return None
