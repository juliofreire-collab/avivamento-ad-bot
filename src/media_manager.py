import logging
from database import db

logger = logging.getLogger(__name__)

def adicionar_video(file_id: str, caption: str = "") -> bool:
    try:
        with db() as cur:
            cur.execute(
                "INSERT INTO media (file_id, tipo, caption) VALUES (%s, 'video', %s) ON CONFLICT (file_id) DO NOTHING",
                (file_id, caption)
            )
            adicionado = cur.rowcount > 0
        if adicionado:
            logger.info(f"Vídeo salvo: {file_id}")
        return adicionado
    except Exception as e:
        logger.error(f"Erro ao salvar vídeo: {e}")
        return False

def adicionar_imagem(file_id: str, caption: str = "") -> bool:
    try:
        with db() as cur:
            cur.execute(
                "INSERT INTO media (file_id, tipo, caption) VALUES (%s, 'imagem', %s) ON CONFLICT (file_id) DO NOTHING",
                (file_id, caption)
            )
            adicionado = cur.rowcount > 0
        if adicionado:
            logger.info(f"Imagem salva: {file_id}")
        return adicionado
    except Exception as e:
        logger.error(f"Erro ao salvar imagem: {e}")
        return False

def get_proximo_video():
    try:
        with db() as cur:
            cur.execute("SELECT file_id, caption, tipo FROM media WHERE tipo = 'video' ORDER BY RANDOM() LIMIT 1")
            row = cur.fetchone()
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Erro ao buscar vídeo: {e}")
        return None

def get_proxima_imagem():
    try:
        with db() as cur:
            cur.execute("SELECT file_id, caption, tipo FROM media WHERE tipo = 'imagem' ORDER BY RANDOM() LIMIT 1")
            row = cur.fetchone()
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Erro ao buscar imagem: {e}")
        return None

def total_videos() -> int:
    try:
        with db() as cur:
            cur.execute("SELECT COUNT(*) AS n FROM media WHERE tipo = 'video'")
            return cur.fetchone()["n"]
    except Exception as e:
        logger.error(f"Erro ao contar vídeos: {e}")
        return 0

def total_imagens() -> int:
    try:
        with db() as cur:
            cur.execute("SELECT COUNT(*) AS n FROM media WHERE tipo = 'imagem'")
            return cur.fetchone()["n"]
    except Exception as e:
        logger.error(f"Erro ao contar imagens: {e}")
        return 0

def limpar_videos():
    try:
        with db() as cur:
            cur.execute("DELETE FROM media WHERE tipo = 'video'")
        logger.info("Vídeos removidos do banco.")
    except Exception as e:
        logger.error(f"Erro ao limpar vídeos: {e}")

def limpar_imagens():
    try:
        with db() as cur:
            cur.execute("DELETE FROM media WHERE tipo = 'imagem'")
        logger.info("Imagens removidas do banco.")
    except Exception as e:
        logger.error(f"Erro ao limpar imagens: {e}")

def carregar_media() -> dict:
    """Compatibilidade: retorna {'videos': [...], 'imagens': [...]}."""
    try:
        with db() as cur:
            cur.execute("SELECT file_id, tipo, caption FROM media ORDER BY id")
            rows = cur.fetchall()
        videos = [dict(r) for r in rows if r["tipo"] == "video"]
        imagens = [dict(r) for r in rows if r["tipo"] == "imagem"]
        return {"videos": videos, "imagens": imagens}
    except Exception as e:
        logger.error(f"Erro ao carregar mídia: {e}")
        return {"videos": [], "imagens": []}
