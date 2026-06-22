import json
import os
import logging

logger = logging.getLogger(__name__)

MEDIA_FILE = "media_storage.json"

def carregar_media():
    if os.path.exists(MEDIA_FILE):
        try:
            with open(MEDIA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"videos": [], "imagens": [], "ultimo_indice_video": 0, "ultimo_indice_imagem": 0}

def salvar_media(data):
    with open(MEDIA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def adicionar_video(file_id: str, caption: str = ""):
    data = carregar_media()
    entrada = {"file_id": file_id, "caption": caption, "tipo": "video"}
    if not any(v["file_id"] == file_id for v in data["videos"]):
        data["videos"].append(entrada)
        salvar_media(data)
        logger.info(f"Vídeo salvo: {file_id}")
        return True
    return False

def adicionar_imagem(file_id: str, caption: str = ""):
    data = carregar_media()
    entrada = {"file_id": file_id, "caption": caption, "tipo": "imagem"}
    if not any(i["file_id"] == file_id for i in data["imagens"]):
        data["imagens"].append(entrada)
        salvar_media(data)
        logger.info(f"Imagem salva: {file_id}")
        return True
    return False

def get_proximo_video():
    data = carregar_media()
    if not data["videos"]:
        return None
    import random
    video = random.choice(data["videos"])
    return video

def get_proxima_imagem():
    data = carregar_media()
    if not data["imagens"]:
        return None
    import random
    img = random.choice(data["imagens"])
    return img

def total_videos():
    return len(carregar_media()["videos"])

def total_imagens():
    return len(carregar_media()["imagens"])

def limpar_videos():
    data = carregar_media()
    data["videos"] = []
    salvar_media(data)

def limpar_imagens():
    data = carregar_media()
    data["imagens"] = []
    salvar_media(data)
