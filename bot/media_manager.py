import logging
from database import db

logger = logging.getLogger(__name__)

def salvar_midia(file_id: str, tipo: str, caption: str = ""):
    try:
        with db() as cur:
            cur.execute("""
                INSERT INTO media (file_id, tipo, caption)
                VALUES (%s, %s, %s)
                ON CONFLICT (file_id) DO NOTHING
            """, (file_id, tipo, caption))
    except Exception as e:
        logger.error(f"Erro ao salvar mídia: {e}")

def get_proximo_video():
    try:
        with db() as cur:
            cur.execute("SELECT file_id, caption FROM media WHERE tipo = 'video' ORDER BY id ASC LIMIT 1")
            row = cur.fetchone()
            return dict(row) if row else None
    except Exception as e:
        logger.error(f"Erro ao buscar vídeo: {e}")
        return None

def get_proxima_imagem():
    try:
        with db() as cur:
            cur.execute("SELECT file_id, caption FROM media WHERE tipo = 'imagem' ORDER BY id ASC LIMIT 1")
            row = cur.fetchone()
            return dict(row) if row else None
    except Exception as e:
        logger.error(f"Erro ao buscar imagem: {e}")
        return None

def remover_midia(file_id: str):
    try:
        with db() as cur:
            cur.execute("DELETE FROM media WHERE file_id = %s", (file_id,))
    except Exception as e:
        logger.error(f"Erro ao remover mídia: {e}")

def total_videos() -> int:
    try:
        with db() as cur:
            cur.execute("SELECT COUNT(*) as total FROM media WHERE tipo = 'video'")
            row = cur.fetchone()
            return row["total"] if row else 0
    except Exception as e:
        logger.error(f"Erro ao contar vídeos: {e}")
        return 0

def total_imagens() -> int:
    try:
        with db() as cur:
            cur.execute("SELECT COUNT(*) as total FROM media WHERE tipo = 'imagem'")
            row = cur.fetchone()
            return row["total"] if row else 0
    except Exception as e:
        logger.error(f"Erro ao contar imagens: {e}")
        return 0

def limpar_videos():
    try:
        with db() as cur:
            cur.execute("DELETE FROM media WHERE tipo = 'video'")
    except Exception as e:
        logger.error(f"Erro ao limpar vídeos: {e}")

def limpar_imagens():
    try:
        with db() as cur:
            cur.execute("DELETE FROM media WHERE tipo = 'imagem'")
    except Exception as e:
        logger.error(f"Erro ao limpar imagens: {e}")
