import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

RANKING_FILE = "ranking.json"

PONTOS = {
    "testemunho": 10,
    "oracao": 5,
    "engajamento": 3,
    "mensagem": 1,
    "entrada": 2,
}

MAX_PONTOS_MENSAGEM_DIA = 5

def carregar_ranking():
    if os.path.exists(RANKING_FILE):
        try:
            with open(RANKING_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}

def salvar_ranking(data):
    with open(RANKING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def adicionar_pontos(user_id: int, nome: str, tipo: str) -> int:
    data = carregar_ranking()
    uid = str(user_id)
    hoje = datetime.now().strftime("%Y-%m-%d")

    if uid not in data:
        data[uid] = {"nome": nome, "pontos": 0, "msgs_hoje": 0, "ultimo_dia": "", "historico": {}}

    data[uid]["nome"] = nome

    # Limite de pontos por mensagem por dia
    if tipo == "mensagem":
        if data[uid].get("ultimo_dia") != hoje:
            data[uid]["msgs_hoje"] = 0
            data[uid]["ultimo_dia"] = hoje
        if data[uid]["msgs_hoje"] >= MAX_PONTOS_MENSAGEM_DIA:
            return data[uid]["pontos"]
        data[uid]["msgs_hoje"] = data[uid].get("msgs_hoje", 0) + 1

    ganhou = PONTOS.get(tipo, 1)
    data[uid]["pontos"] = data[uid].get("pontos", 0) + ganhou

    mes = datetime.now().strftime("%Y-%m")
    if "historico" not in data[uid]:
        data[uid]["historico"] = {}
    data[uid]["historico"][mes] = data[uid]["historico"].get(mes, 0) + ganhou

    salvar_ranking(data)
    logger.info(f"+{ganhou} pontos para {nome} ({tipo}) — total: {data[uid]['pontos']}")
    return data[uid]["pontos"]

def get_top_ranking(limite=10):
    data = carregar_ranking()
    ordenado = sorted(data.items(), key=lambda x: x[1].get("pontos", 0), reverse=True)
    return [(uid, info["nome"], info.get("pontos", 0)) for uid, info, in ordenado[:limite]]

def get_pontos_usuario(user_id: int) -> int:
    data = carregar_ranking()
    return data.get(str(user_id), {}).get("pontos", 0)

def resetar_ranking_mensal():
    data = carregar_ranking()
    for uid in data:
        data[uid]["pontos"] = 0
    salvar_ranking(data)
    logger.info("Ranking mensal resetado.")
