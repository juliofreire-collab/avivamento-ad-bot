import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTEMUNHOS_FILE = os.path.join(_BASE_DIR, "testemunhos.json")

def carregar_testemunhos():
    if os.path.exists(TESTEMUNHOS_FILE):
        try:
            with open(TESTEMUNHOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []

def salvar_testemunho(user_name: str, user_id: int, texto: str) -> bool:
    testemunhos = carregar_testemunhos()
    novo = {
        "nome": user_name,
        "user_id": user_id,
        "texto": texto,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "publicado": False
    }
    testemunhos.append(novo)
    with open(TESTEMUNHOS_FILE, "w", encoding="utf-8") as f:
        json.dump(testemunhos, f, ensure_ascii=False, indent=2)
    logger.info(f"Testemunho salvo de {user_name}")
    return True

def get_testemunhos_pendentes():
    return [t for t in carregar_testemunhos() if not t.get("publicado")]

def marcar_publicado(index: int):
    todos = carregar_testemunhos()
    pendentes = [i for i, t in enumerate(todos) if not t.get("publicado")]
    if index < len(pendentes):
        todos[pendentes[index]]["publicado"] = True
        with open(TESTEMUNHOS_FILE, "w", encoding="utf-8") as f:
            json.dump(todos, f, ensure_ascii=False, indent=2)

def get_proximo_testemunho_nao_publicado():
    todos = carregar_testemunhos()
    for i, t in enumerate(todos):
        if not t.get("publicado"):
            todos[i]["publicado"] = True
            with open(TESTEMUNHOS_FILE, "w", encoding="utf-8") as f:
                json.dump(todos, f, ensure_ascii=False, indent=2)
            return t
    return None
