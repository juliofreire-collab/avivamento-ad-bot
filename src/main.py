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

# ─── Telegram error reporter (raw HTTP — sem depender do PTB) ─────────────────
_ADMIN_CHAT = "8725437154"

def _tg_send(text: str):
    """Envia mensagem ao admin via HTTP direto (funciona mesmo se PTB falhar)."""
    token = os.getenv("BOT_TOKEN", "")
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
    except Exception:
        pass


# ─── Logging ──────────────────────────────────────────────────────────────────
_log_handlers = [logging.StreamHandler(sys.stdout)]
try:
    _log_handlers.append(logging.FileHandler("bot.log", encoding="utf-8"))
except Exception:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=_log_handlers
)
logger = logging.getLogger(__name__)

# ─── Status global (health-check) ─────────────────────────────────────────────
_bot_status = {"state": "starting", "uptime_start": time.time(), "db": "pending", "last_error": "none"}


class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = (
            f"state={_bot_status['state']} "
            f"db={_bot_status['db']} "
            f"uptime={int(time.time()-_bot_status['uptime_start'])}s "
            f"py={sys.version.split()[0]}"
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def _start_health_server():
    port = int(os.getenv("PORT", "8080"))
    logger.info(f"Tentando iniciar health-check na porta {port}...")
    for attempt_port in [port, 8080, 3000, 5000]:
        try:
            server = HTTPServer(("0.0.0.0", attempt_port), _HealthHandler)
            logger.info(f"Health-check HTTP OK na porta {attempt_port}")
            server.serve_forever()
            return
        except OSError as e:
            logger.warning(f"Porta {attempt_port} falhou: {e}")
    logger.error("Nao foi possivel iniciar health-check em nenhuma porta!")


def _init_db_background():
    """Inicializa banco em background — nunca bloqueia o polling."""
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url or "usuario" in db_url:
        logger.warning("DATABASE_URL nao configurado ou eh placeholder! DB desabilitado.")
        _bot_status["db"] = "disabled"
        return

    tentativa = 0
    while True:
        try:
            from database import init_db
            init_db()
            logger.info("Banco de dados inicializado com sucesso!")
            _bot_status["db"] = "ok"
            return
        except Exception as e:
            tentativa += 1
            espera = min(tentativa * 10, 120)
            logger.error(f"Falha ao inicializar banco (tentativa {tentativa}): {e}. Tentando em {espera}s...")
            _bot_status["db"] = f"retry_{tentativa}"
            time.sleep(espera)


# ─── Imports dos módulos do bot (feito aqui para capturar erros) ──────────────
_import_error = None
try:
    logger.info("Importando modulos do bot...")
    from config import BOT_TOKEN
    logger.info(f"config.py OK | BOT_TOKEN={'SIM' if BOT_TOKEN else 'NAO'}")

    from telegram import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeDefault
    from telegram.ext import (
        Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
    )
    logger.info("python-telegram-bot OK")

    from comandos import (
        cmd_start, cmd_ping, cmd_ajuda, cmd_versiculo, cmd_regras, cmd_devocional, cmd_oracao,
        cmd_horarios, cmd_fila, cmd_proxima, cmd_testar,
        cmd_postar, cmd_postar_versiculo, cmd_postar_midia, cmd_postar_devocional,
        cmd_postar_regras, cmd_postar_oracao, cmd_postar_engajamento,
        cmd_banir, cmd_kick, cmd_silenciar, cmd_liberar,
        cmd_avisar, cmd_perdoar, cmd_resetar_avisos, cmd_advertencias, cmd_info,
        cmd_anuncio, cmd_fixar,
        cmd_bloquear, cmd_desbloquear, cmd_listanegra,
        cmd_status, cmd_listar_midia, cmd_limpar_videos, cmd_limpar_imagens, cmd_ver_pedidos,
        cmd_chatid, cmd_enquete,
        cmd_testemunho, cmd_ver_testemunhos, cmd_postar_testemunho,
        cmd_ranking, cmd_postar_ranking,
        cmd_aniversario,
        cmd_importar
    )
    logger.info("comandos.py OK")

    from handlers import (
        handle_novo_membro, handle_mensagem_grupo,
        handle_midia_privado, handle_saida_membro, handle_texto_privado,
        handle_aceitar_regras
    )
    logger.info("handlers.py OK")

    from agendador import configurar_agendamentos
    logger.info("agendador.py OK")

except Exception as _ie:
    _import_error = traceback.format_exc()
    logger.error(f"ERRO NO IMPORT: {_import_error}")


# ─── BotCommands ──────────────────────────────────────────────────────────────
if not _import_error:
    COMANDOS_USUARIOS = [
        BotCommand("start", "Iniciar o bot"),
        BotCommand("ajuda", "Ver todos os comandos"),
        BotCommand("ping", "Verificar se o bot esta online"),
        BotCommand("versiculo", "Receber um versiculo com imagem"),
        BotCommand("devocional", "Receber um devocional"),
        BotCommand("regras", "Ver as regras do grupo"),
        BotCommand("oracao", "Ver e enviar pedidos de oracao"),
        BotCommand("testemunho", "Enviar um testemunho para o canal"),
        BotCommand("ranking", "Ver ranking de engajamento do grupo"),
        BotCommand("aniversario", "Cadastrar seu aniversario: /aniversario DD/MM"),
    ]

    COMANDOS_ADMINS = COMANDOS_USUARIOS + [
        BotCommand("horarios", "Horarios de postagem no canal"),
        BotCommand("fila", "Ver midias na fila do canal"),
        BotCommand("postar", "Postar versiculo no canal agora"),
        BotCommand("proxima", "Previa da proxima mensagem agendada"),
        BotCommand("testar", "Diagnostico: canal e grupo"),
        BotCommand("info", "Info de um membro (responda a mensagem)"),
        BotCommand("avisar", "Advertir membro (responda a mensagem)"),
        BotCommand("perdoar", "Remover advertencias (responda a mensagem)"),
        BotCommand("advertencias", "Ver advertencias de um membro"),
        BotCommand("silenciar", "Mutar membro: /silenciar 10m (responda)"),
        BotCommand("liberar", "Desmutar membro (responda a mensagem)"),
        BotCommand("banir", "Banir membro (responda a mensagem)"),
        BotCommand("kick", "Expulsar membro sem banir (responda)"),
        BotCommand("fixar", "Fixar mensagem no grupo (responda)"),
        BotCommand("bloquear", "Bloquear palavra: /bloquear palavra"),
        BotCommand("desbloquear", "Desbloquear palavra: /desbloquear palavra"),
        BotCommand("listanegra", "Ver lista de palavras bloqueadas"),
        BotCommand("enquete", "Enviar enquete semanal no grupo"),
        BotCommand("anuncio", "Fazer anuncio oficial no grupo"),
        BotCommand("ver_testemunhos", "Ver testemunhos pendentes"),
        BotCommand("postar_testemunho", "Publicar testemunho no canal"),
        BotCommand("status", "Estatisticas completas do bot"),
        BotCommand("ver_pedidos", "Ver pedidos de oracao pendentes"),
        BotCommand("listar_midia", "Ver midias salvas na fila"),
        BotCommand("chatid", "Ver ID do chat ou usuario"),
        BotCommand("ranking", "Ver ranking de engajamento do grupo"),
        BotCommand("postar_ranking", "Postar ranking agora no grupo"),
        BotCommand("aniversario", "Cadastrar seu aniversario: /aniversario DD/MM"),
    ]

    async def post_init(app):
        try:
            await app.bot.set_my_commands(COMANDOS_USUARIOS, scope=BotCommandScopeDefault())
            await app.bot.set_my_commands(COMANDOS_ADMINS, scope=BotCommandScopeAllPrivateChats())
            logger.info("Comandos do BotFather configurados!")
        except Exception as e:
            logger.error(f"Erro ao configurar comandos: {e}")

    def build_app():
        logger.info("Construindo Application...")
        app = (
            Application.builder()
            .token(BOT_TOKEN)
            .connect_timeout(30)
            .read_timeout(30)
            .write_timeout(30)
            .pool_timeout(30)
            .post_init(post_init)
            .build()
        )
        logger.info("Application criada. Adicionando handlers...")

        app.add_handler(CommandHandler("start", cmd_start))
        app.add_handler(CommandHandler("ping", cmd_ping))
        app.add_handler(CommandHandler("ajuda", cmd_ajuda))
        app.add_handler(CommandHandler("versiculo", cmd_versiculo))
        app.add_handler(CommandHandler("regras", cmd_regras))
        app.add_handler(CommandHandler("devocional", cmd_devocional))
        app.add_handler(CommandHandler("oracao", cmd_oracao))
        app.add_handler(CommandHandler("testemunho", cmd_testemunho))
        app.add_handler(CommandHandler("postar", cmd_postar))
        app.add_handler(CommandHandler("postar_versiculo", cmd_postar_versiculo))
        app.add_handler(CommandHandler("postar_midia", cmd_postar_midia))
        app.add_handler(CommandHandler("postar_devocional", cmd_postar_devocional))
        app.add_handler(CommandHandler("fila", cmd_fila))
        app.add_handler(CommandHandler("horarios", cmd_horarios))
        app.add_handler(CommandHandler("proxima", cmd_proxima))
        app.add_handler(CommandHandler("postar_regras", cmd_postar_regras))
        app.add_handler(CommandHandler("postar_oracao", cmd_postar_oracao))
        app.add_handler(CommandHandler("postar_engajamento", cmd_postar_engajamento))
        app.add_handler(CommandHandler("enquete", cmd_enquete))
        app.add_handler(CommandHandler("anuncio", cmd_anuncio))
        app.add_handler(CommandHandler("fixar", cmd_fixar))
        app.add_handler(CommandHandler("banir", cmd_banir))
        app.add_handler(CommandHandler("kick", cmd_kick))
        app.add_handler(CommandHandler("silenciar", cmd_silenciar))
        app.add_handler(CommandHandler("liberar", cmd_liberar))
        app.add_handler(CommandHandler("avisar", cmd_avisar))
        app.add_handler(CommandHandler("perdoar", cmd_perdoar))
        app.add_handler(CommandHandler("resetar_avisos", cmd_resetar_avisos))
        app.add_handler(CommandHandler("advertencias", cmd_advertencias))
        app.add_handler(CommandHandler("info", cmd_info))
        app.add_handler(CommandHandler("bloquear", cmd_bloquear))
        app.add_handler(CommandHandler("desbloquear", cmd_desbloquear))
        app.add_handler(CommandHandler("listanegra", cmd_listanegra))
        app.add_handler(CommandHandler("ver_testemunhos", cmd_ver_testemunhos))
        app.add_handler(CommandHandler("postar_testemunho", cmd_postar_testemunho))
        app.add_handler(CommandHandler("ranking", cmd_ranking))
        app.add_handler(CommandHandler("postar_ranking", cmd_postar_ranking))
        app.add_handler(CommandHandler("aniversario", cmd_aniversario))
        app.add_handler(CommandHandler("status", cmd_status))
        app.add_handler(CommandHandler("listar_midia", cmd_listar_midia))
        app.add_handler(CommandHandler("limpar_videos", cmd_limpar_videos))
        app.add_handler(CommandHandler("limpar_imagens", cmd_limpar_imagens))
        app.add_handler(CommandHandler("ver_pedidos", cmd_ver_pedidos))
        app.add_handler(CommandHandler("chatid", cmd_chatid))
        app.add_handler(CommandHandler("importar", cmd_importar))
        app.add_handler(CommandHandler("testar", cmd_testar))

        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_novo_membro))
        app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_saida_membro))
        app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_mensagem_grupo))
        app.add_handler(MessageHandler(
            (filters.VIDEO | filters.PHOTO | filters.Document.ALL) & filters.ChatType.PRIVATE,
            handle_midia_privado
        ))
        app.add_handler(MessageHandler(
            filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND,
            handle_texto_privado
        ))
        app.add_handler(CallbackQueryHandler(handle_aceitar_regras, pattern=r"^aceitar_regras:"))

        logger.info("Handlers adicionados. Configurando agendamentos...")
        configurar_agendamentos(app)
        logger.info("build_app() concluido com sucesso!")
        return app


def main():
    # 1. Health-check em background
    threading.Thread(target=_start_health_server, daemon=True).start()

    # 2. Banco em background
    threading.Thread(target=_init_db_background, daemon=True).start()

    logger.info("=== BOT AVIVAMENTO AD INICIANDO ===")
    logger.info(f"Python: {sys.version}")
    logger.info(f"DIR: {os.getcwd()}")
    logger.info(f"PORT: {os.getenv('PORT', 'nao definida')}")
    logger.info(f"BOT_TOKEN: {'SIM' if os.getenv('BOT_TOKEN') else 'NAO'}")
    logger.info(f"DATABASE_URL: {'SIM' if os.getenv('DATABASE_URL') else 'NAO'}")

    # Se houve erro de import, notifica e fica vivo para health-check
    if _import_error:
        msg = f"ERRO DE IMPORT NO BOT:\n\n{_import_error}"
        logger.error(msg)
        _tg_send(msg)
        _bot_status["state"] = "import_error"
        while True:
            time.sleep(60)

    if not BOT_TOKEN:
        msg = "ERRO: BOT_TOKEN nao configurado no Railway!"
        logger.error(msg)
        _tg_send(msg)
        _bot_status["state"] = "no_token"
        while True:
            time.sleep(60)

    # 3. Polling
    _bot_status["state"] = "polling"
    retry_delay = 5
    consecutive_errors = 0
    while True:
        try:
            logger.info(f"Tentativa de polling #{consecutive_errors + 1}...")
            app = build_app()
            consecutive_errors = 0
            app.run_polling(
                drop_pending_updates=True,
                allowed_updates=None,
                timeout=30,
                poll_interval=1.0,
            )
            retry_delay = 5
        except Exception as e:
            consecutive_errors += 1
            tb = traceback.format_exc()
            _bot_status["state"] = "error"
            _bot_status["last_error"] = str(e)[:100]
            logger.error(f"Erro no polling (tentativa {consecutive_errors}): {tb}")

            # Notifica admin via Telegram a cada 3 erros consecutivos
            if consecutive_errors <= 3:
                _tg_send(
                    f"ERRO no bot (tentativa {consecutive_errors}):\n\n"
                    f"{type(e).__name__}: {str(e)[:500]}\n\n"
                    f"Traceback:\n{tb[-1000:]}"
                )

            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)
            _bot_status["state"] = "polling"


if __name__ == "__main__":
    main()
