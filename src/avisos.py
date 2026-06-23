import json
import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AVISOS_FILE = os.path.join(_BASE_DIR, "avisos_usuarios.json")

def carregar_avisos():
    if os.path.exists(AVISOS_FILE):
        try:
            with open(AVISOS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

def salvar_avisos(data):
    with open(AVISOS_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def registrar_aviso(user_id: int) -> int:
    data = carregar_avisos()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"avisos": 0, "ultimo": ""}
    data[uid]["avisos"] += 1
    data[uid]["ultimo"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    salvar_avisos(data)
    return data[uid]["avisos"]

def get_avisos(user_id: int) -> int:
    data = carregar_avisos()
    return data.get(str(user_id), {}).get("avisos", 0)

def resetar_avisos(user_id: int):
    data = carregar_avisos()
    uid = str(user_id)
    if uid in data:
        data[uid]["avisos"] = 0
        salvar_avisos(data)
