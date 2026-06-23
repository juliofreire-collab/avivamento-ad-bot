import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN não configurado nas variáveis de ambiente!")

CHANNEL_ID = os.getenv("CHANNEL_ID", "@avivamentoad")
GROUP_ID = os.getenv("GROUP_ID", "-1003537178026")
OWNER_ID = int(os.getenv("OWNER_ID", "8725437154"))

# Palavrões detectados apenas como PALAVRAS COMPLETAS (não dentro de outras palavras)
# Ex: "cu" NÃO vai bloquear "acupuntura", "recuperar", etc.
# Usa regex com \b (word boundary) no handlers.py
PALAVROES_EXATOS = [
    r"\bmerda\b",
    r"\bporra\b",
    r"\bcaralho\b",
    r"\bfdp\b",
    r"\bviado\b",
    r"\bputa\b",
    r"\bvadia\b",
    r"\bidiota\b",
    r"\bimbecil\b",
    r"\bcorno\b",
    r"\bbuceta\b",
    r"\bcu\b",
    r"\bfoder\b",
    r"\barrombado\b",
    r"\bbabaca\b",
    r"\bbosta\b",
    r"\bcuz[aã]o\b",
    r"\bvai se foder\b",
    r"\bfilho da puta\b",
    r"\bseu merda\b",
    r"\bvai tomar no\b",
    r"\bpqp\b",
    r"\bvsf\b",
    r"\bkct\b",
]

# Sistema de avisos antes de banir
# 1º aviso: apaga mensagem e avisa
# 2º aviso: apaga + silencia por 1h
# 3º aviso: apaga + bane

HORARIOS_CANAL_MEDIA = ["09:00", "19:00"]
HORARIOS_VERSICULOS = ["07:00", "13:00", "21:00"]
HORARIO_REGRAS_GRUPO = 4

TIMEZONE = "America/Sao_Paulo"
