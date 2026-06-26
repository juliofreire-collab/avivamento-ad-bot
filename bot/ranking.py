import logging
from datetime import date
from database import db

logger = logging.getLogger(__name__)

PONTOS = {
    "testemunho": 10,
    "oracao": 5,
    "engajamento": 3,
    "mensagem": 1,
}

def adicionar_pontos(user_id: int, nome: str, tipo: str):
    try:
        pts = PONTOS.get(tipo, 1)
        hoje = date.today()
        with db() as cur:
            if tipo == "mensagem":
                cur.execute("""
                    INSERT INTO ranking (user_id, nome, pontos, msgs_hoje, ultimo_dia)
                    VALUES (%s, %s, %s, 1, %s)
                    ON CONFLICT (user_id) DO UPDATE SET
                        nome = EXCLUDED.nome,
                        pontos = CASE
                            WHEN ranking.ultimo_dia = EXCLUDED.ultimo_dia THEN ranking.pontos
                            ELSE ranking.pontos + EXCLUDED.pontos
                        END,
                        msgs_hoje = CASE
                            WHEN ranking.ultimo_dia = EXCLUDED.ultimo_dia THEN ranking.msgs_hoje + 1
                            ELSE 1
                        END,
                        ultimo_dia = EXCLUDED.ultimo_dia
                """, (user_id, nome, pts, hoje))
            else:
                cur.execute("""
                    INSERT INTO ranking (user_id, nome, pontos, msgs_hoje, ultimo_dia)
                    VALUES (%s, %s, %s, 0, %s)
                    ON CONFLICT (user_id) DO UPDATE SET
                        nome = EXCLUDED.nome,
                        pontos = ranking.pontos + EXCLUDED.pontos
                """, (user_id, nome, pts, hoje))
    except Exception as e:
        logger.error(f"Erro ao adicionar pontos: {e}")

def get_top_ranking(limite: int = 10):
    try:
        with db() as cur:
            cur.execute("""
                SELECT user_id, nome, pontos FROM ranking
                ORDER BY pontos DESC LIMIT %s
            """, (limite,))
            return [(str(r["user_id"]), r["nome"], r["pontos"]) for r in cur.fetchall()]
    except Exception as e:
        logger.error(f"Erro ao buscar ranking: {e}")
        return []

def get_pontos_usuario(user_id: int) -> int:
    try:
        with db() as cur:
            cur.execute("SELECT pontos FROM ranking WHERE user_id = %s", (user_id,))
            row = cur.fetchone()
            return row["pontos"] if row else 0
    except Exception as e:
        logger.error(f"Erro ao buscar pontos: {e}")
        return 0

def resetar_ranking_mensal():
    try:
        with db() as cur:
            cur.execute("UPDATE ranking SET pontos = 0, msgs_hoje = 0")
        logger.info("Ranking mensal resetado.")
    except Exception as e:
        logger.error(f"Erro ao resetar ranking: {e}")
