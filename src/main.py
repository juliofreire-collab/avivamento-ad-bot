import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
import time
import threading
import traceback
import urllib.request
import urllib.parse
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

_ADMIN_CHAT = "8725437154"

def _tg_send(token: str, text: str):
    if not token:
        return
    try:
        payload = json.dumps({"chat_id": _ADMIN_CHAT, "text": text[:4000]}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"[_tg_send ERRO] {e}", flush=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

_bot_status = {"state": "starting", "uptime_start": time.time(), "db": "pending"}

class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = (f"state={_bot_status['state']} db={_bot_status['db']} "
                f"uptime={int(time.time()-_bot_status['uptime_start'])}s "
                f"py={sys.version.split()[0]}").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args):
        pass

def _start_health_server(port: int):
    try:
        server = HTTPServer(("0.0.0.0", port), _HealthHandler)
        logger.info(f"[HEALTH] OK na porta {port}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"[HEALTH] FALHOU na porta {port}: {e}")

def _init_db_background():
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url or "usuario" in db_url or "nome_do_banco" in db_url:
        logger.warning("[DB] DATABASE_URL e placeholder ou ausente — banco desabilitado.")
        _bot_status["db"] = "disabled"
        return
    tentativa = 0
    while True:
        try:
            from database import init_db
            init_db()
            logger.info("[DB] Banco inicializado!")
            _bot_status["db"] = "ok"
            return
        except Exception as e:
            tentativa += 1
            espera = min(tentativa * 10, 120)
            logger.error(f"[DB] Falha tentativa {tentativa}: {e}. Retry em {espera}s...")
            _bot_status["db"] = f"retry_{tentativa}"
            time.sleep(espera)

# ── Imports do bot ────────────────────────────────────────────────────────────
_import_error = None
BOT_TOKEN = ""
try:
    from config import BOT_TOKEN
    from telegram import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeDefault
    from telegram.ext import (Application, CommandHandler, MessageHandler,
                               CallbackQueryHandler, filters)
    from comandos import (
        cmd_start, cmd_ping, cmd_ajuda, cmd_versiculo, cmd_regras, cmd_devocional, cmd_oracao,
        cmd_horarios, cmd_fila, cmd_proxima, cmd_testar,
        cmd_postar, cmd_postar_versiculo, cmd_postar_midia, cmd_postar_devocional,
        cmd_postar_regras, cmd_postar_oracao, cmd_postar_engajamento,
        cmd_banir, cmd_kick, cmd_silenciar, cmd_liberar,
        cmd_avisar, cmd_perdoar, cmd_resetar_avisos, cmd_advertencias, cmd_info,
        cmd_anuncio, cmd_fixar, cmd_bloquear, cmd_desbloquear, cmd_listanegra,
        cmd_status, cmd_listar_midia, cmd_limpar_videos, cmd_limpar_imagens, cmd_ver_pedidos,
        cmd_chatid, cmd_enquete, cmd_testemunho, cmd_ver_testemunhos, cmd_postar_testemunho,
        cmd_ranking, cmd_postar_ranking, cmd_aniversario, cmd_importar
    )
    from handlers import (handle_novo_membro, handle_mensagem_grupo, handle_midia_privado,
                          handle_saida_membro, handle_texto_privado, handle_aceitar_regras)
    from agendador import configurar_agendamentos
except Exception as _ie:
    _import_error = traceback.format_exc()

if not _import_error:
    async def post_init(app):
        try:
            cmds_user = [BotCommand("start","Iniciar"), BotCommand("ping","Status"),
                         BotCommand("ajuda","Ajuda"), BotCommand("versiculo","Versículo"),
                         BotCommand("devocional","Devocional"), BotCommand("regras","Regras"),
                         BotCommand("oracao","Oração"), BotCommand("testemunho","Testemunho"),
                         BotCommand("ranking","Ranking"), BotCommand("aniversario","Aniversário")]
            await app.bot.set_my_commands(cmds_user, scope=BotCommandScopeDefault())
        except Exception as e:
            logger.error(f"[post_init] {e}")

    def build_app():
        app = (Application.builder().token(BOT_TOKEN)
               .connect_timeout(30).read_timeout(30).write_timeout(30)
               .pool_timeout(30).post_init(post_init).build())
        for cmd, fn in [
            ("start",cmd_start),("ping",cmd_ping),("ajuda",cmd_ajuda),
            ("versiculo",cmd_versiculo),("regras",cmd_regras),("devocional",cmd_devocional),
            ("oracao",cmd_oracao),("testemunho",cmd_testemunho),("postar",cmd_postar),
            ("postar_versiculo",cmd_postar_versiculo),("postar_midia",cmd_postar_midia),
            ("postar_devocional",cmd_postar_devocional),("fila",cmd_fila),
            ("horarios",cmd_horarios),("proxima",cmd_proxima),
            ("postar_regras",cmd_postar_regras),("postar_oracao",cmd_postar_oracao),
            ("postar_engajamento",cmd_postar_engajamento),("enquete",cmd_enquete),
            ("anuncio",cmd_anuncio),("fixar",cmd_fixar),("banir",cmd_banir),
            ("kick",cmd_kick),("silenciar",cmd_silenciar),("liberar",cmd_liberar),
            ("avisar",cmd_avisar),("perdoar",cmd_perdoar),
            ("resetar_avisos",cmd_resetar_avisos),("advertencias",cmd_advertencias),
            ("info",cmd_info),("bloquear",cmd_bloquear),("desbloquear",cmd_desbloquear),
            ("listanegra",cmd_listanegra),("ver_testemunhos",cmd_ver_testemunhos),
            ("postar_testemunho",cmd_postar_testemunho),("ranking",cmd_ranking),
            ("postar_ranking",cmd_postar_ranking),("aniversario",cmd_aniversario),
            ("status",cmd_status),("listar_midia",cmd_listar_midia),
            ("limpar_videos",cmd_limpar_videos),("limpar_imagens",cmd_limpar_imagens),
            ("ver_pedidos",cmd_ver_pedidos),("chatid",cmd_chatid),
            ("importar",cmd_importar),("testar",cmd_testar),
        ]:
            app.add_handler(CommandHandler(cmd, fn))
        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_novo_membro))
        app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_saida_membro))
        app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_mensagem_grupo))
        app.add_handler(MessageHandler(
            (filters.VIDEO | filters.PHOTO | filters.Document.ALL) & filters.ChatType.PRIVATE,
            handle_midia_privado))
        app.add_handler(MessageHandler(
            filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, handle_texto_privado))
        app.add_handler(CallbackQueryHandler(handle_aceitar_regras, pattern=r"^aceitar_regras:"))
        configurar_agendamentos(app)
        return app


def main():
    token = BOT_TOKEN or os.getenv("BOT_TOKEN", "")
    port = int(os.getenv("PORT", "8080"))

    # ── 1. Startup diagnostics enviado via Telegram ──────────────────────────
    diag = (
        f"[BOT STARTUP]\n"
        f"PORT={port}\n"
        f"BOT_TOKEN={'SIM' if token else 'NAO'}\n"
        f"DATABASE_URL={'SIM' if os.getenv('DATABASE_URL') else 'NAO'}\n"
        f"Python={sys.version.split()[0]}\n"
        f"import_error={'SIM - '+_import_error[:200] if _import_error else 'NAO'}"
    )
    logger.info(diag)
    _tg_send(token, diag)

    # ── 2. Health-check em background ────────────────────────────────────────
    threading.Thread(target=_start_health_server, args=(port,), daemon=True).start()

    # ── 3. Banco em background ────────────────────────────────────────────────
    threading.Thread(target=_init_db_background, daemon=True).start()

    # ── 4. Se import falhou, fica vivo mas não faz polling ───────────────────
    if _import_error:
        msg = f"[ERRO IMPORT]\n{_import_error[-1500:]}"
        logger.error(msg)
        _tg_send(token, msg)
        _bot_status["state"] = "import_error"
        while True:
            time.sleep(60)

    if not token:
        msg = "[ERRO] BOT_TOKEN vazio!"
        logger.error(msg)
        _tg_send(token, msg)
        _bot_status["state"] = "no_token"
        while True:
            time.sleep(60)

    # ── 5. Polling ────────────────────────────────────────────────────────────
    _bot_status["state"] = "polling"
    retry_delay = 5
    n_erros = 0
    while True:
        try:
            logger.info(f"[POLLING] tentativa {n_erros+1}...")
            app = build_app()
            n_erros = 0
            logger.info("[POLLING] run_polling iniciando...")
            app.run_polling(drop_pending_updates=True, allowed_updates=None,
                            timeout=30, poll_interval=1.0)
            retry_delay = 5
        except Exception as e:
            n_erros += 1
            tb = traceback.format_exc()
            _bot_status["state"] = "error"
            logger.error(f"[POLLING] Erro #{n_erros}: {tb}")
            if n_erros <= 3:
                _tg_send(token,
                    f"[ERRO POLLING #{n_erros}]\n{type(e).__name__}: {str(e)[:300]}\n\n{tb[-800:]}")
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)
            _bot_status["state"] = "polling"


if __name__ == "__main__":
    main()
