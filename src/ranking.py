import logging
from datetime import date
from database import db

logger = logging.getLogger(__name__)

PONTOS = {
    "testemunho": 10,
    "oracao": 5,
    "engajamento": 3,
    "mensagem": 1,
    "entrada": 2,
}

MAX_PONTOS_MENSAGEM_DIA = 5

def adicionar_pontos(user_id: int, nome: str, tipo: str) -> int:
    ganhou = PONTOS.get(tipo, 1)
    hoje = date.today()
    try:
        with db() as cur:
            # Garante que o usuário existe
            cur.execute("""
                INSERT INTO ranking (user_id, nome, pontos, msgs_hoje, ultimo_dia)
                VALUES (%s, %s, 0, 0, NULL)
                ON CONFLICT (user_id) DO UPDATE SET nome = EXCLUDED.nome
            """, (user_id, nome))

            if tipo == "mensagem":
                # Zera contador se mudou o dia
                cur.execute("""
                    UPDATE ranking
                    SET msgs_hoje = CASE WHEN ultimo_dia = %s THEN msgs_hoje ELSE 0 END,
                        ultimo_dia = %s
                    WHERE user_id = %s
                """, (hoje, hoje, user_id))

                # Verifica limite diário
                cur.execute("SELECT msgs_hoje FROM ranking WHERE user_id = %s", (user_id,))
                row = cur.fetchone()
                if row and row["msgs_hoje"] >= MAX_PONTOS_MENSAGEM_DIA:
                    cur.execute("SELECT pontos FROM ranking WHERE user_id = %s", (user_id,))
                    return cur.fetchone()["pontos"]

                cur.execute("""
                    UPDATE ranking SET msgs_hoje = msgs_hoje + 1, pontos = pontos + %s
                    WHERE user_id = %s
                """, (ganhou, user_id))
            else:
                cur.execute("""
                    UPDATE ranking SET pontos = pontos + %s WHERE user_id = %s
                """, (ganhou, user_id))

            cur.execute("SELECT pontos FROM ranking WHERE user_id = %s", (user_id,))
            total = cur.fetchone()["pontos"]

        logger.info(f"+{ganhou} pontos para {nome} ({tipo}) — total: {total}")
        return total
    except Exception as e:
        logger.error(f"Erro ao adicionar pontos: {e}")
        return 0

def get_top_ranking(limite: int = 10):
    try:
        with db() as cur:
            cur.execute(
                "SELECT user_id, nome, pontos FROM ranking ORDER BY pontos DESC LIMIT %s",
                (limite,)
            )
            rows = cur.fetchall()
        return [(str(r["user_id"]), r["nome"], r["pontos"]) for r in rows]
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
            cur.execute("UPDATE ranking SET pontos = 0")
        logger.info("Ranking mensal resetado.")
    except Exception as e:
        logger.error(f"Erro ao resetar ranking: {e}")
