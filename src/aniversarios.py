import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANIV_FILE = os.path.join(_BASE_DIR, "aniversarios.json")

def carregar():
    if os.path.exists(ANIV_FILE):
        try:
            with open(ANIV_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}

def salvar(data):
    with open(ANIV_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def registrar_aniversario(user_id: int, nome: str, dia: int, mes: int):
    data = carregar()
    data[str(user_id)] = {"nome": nome, "dia": dia, "mes": mes}
    salvar(data)

def get_aniversariantes_hoje():
    hoje = datetime.now()
    data = carregar()
    return [
        (uid, info["nome"], info["dia"], info["mes"])
        for uid, info in data.items()
        if info["dia"] == hoje.day and info["mes"] == hoje.month
    ]

def get_aniversario(user_id: int):
    data = carregar()
    return data.get(str(user_id))

def total_cadastrados():
    return len(carregar())
