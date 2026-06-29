import logging
import os
import sys
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeDefault
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
)
from config import BOT_TOKEN
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
from handlers import (
    handle_novo_membro, handle_mensagem_grupo,
    handle_midia_privado, handle_saida_membro, handle_texto_privado,
    handle_aceitar_regras
)
from agendador import configurar_agendamentos

_handlers = [logging.StreamHandler(sys.stdout)]
try:
    _handlers.append(logging.FileHandler("bot.log", encoding="utf-8"))
except Exception:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=_handlers
)
logger = logging.getLogger(__name__)

# Status global do bot (para health-check)
_bot_status = {"state": "starting", "uptime_start": time.time()}

class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = f"state={_bot_status['state']} uptime={int(time.time()-_bot_status['uptime_start'])}s".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args):
        pass  # silencia logs HTTP

def _start_health_server():
    port = int(os.getenv("PORT", "8080"))
    try:
        server = HTTPServer(("0.0.0.0", port), _HealthHandler)
        logger.info(f"🌐 Health-check HTTP iniciado na porta {port}")
        server.serve_forever()
    except Exception as e:
        logger.warning(f"Health-check HTTP não pôde iniciar: {e}")

COMANDOS_USUARIOS = [
    BotCommand("start", "Iniciar o bot"),
    BotCommand("ajuda", "Ver todos os comandos"),
    BotCommand("ping", "Verificar se o bot está online"),
    BotCommand("versiculo", "Receber um versículo com imagem"),
    BotCommand("devocional", "Receber um devocional"),
    BotCommand("regras", "Ver as regras do grupo"),
    BotCommand("oracao", "Ver e enviar pedidos de oração"),
    BotCommand("testemunho", "Enviar um testemunho para o canal"),
    BotCommand("ranking", "Ver ranking de engajamento do grupo"),
    BotCommand("aniversario", "Cadastrar seu aniversário: /aniversario DD/MM"),
]

COMANDOS_ADMINS = [
    BotCommand("start", "Iniciar o bot"),
    BotCommand("ajuda", "Ver todos os comandos"),
    BotCommand("ping", "Verificar se o bot está online"),
    BotCommand("versiculo", "Receber um versículo com imagem"),
    BotCommand("devocional", "Receber um devocional"),
    BotCommand("regras", "Ver as regras do grupo"),
    BotCommand("oracao", "Ver e enviar pedidos de oração"),
    BotCommand("testemunho", "Enviar um testemunho"),
    BotCommand("horarios", "Horários de postagem no canal"),
    BotCommand("fila", "Ver mídias na fila do canal"),
    BotCommand("postar", "Postar versículo no canal agora"),
    BotCommand("proxima", "Prévia da próxima mensagem agendada"),
    BotCommand("testar", "Diagnóstico: canal e grupo"),
    BotCommand("info", "Info de um membro (responda à mensagem)"),
    BotCommand("avisar", "Advertir membro (responda à mensagem)"),
    BotCommand("perdoar", "Remover advertências (responda à mensagem)"),
    BotCommand("advertencias", "Ver advertências de um membro"),
    BotCommand("silenciar", "Mutar membro: /silenciar 10m (responda)"),
    BotCommand("liberar", "Desmutar membro (responda à mensagem)"),
    BotCommand("banir", "Banir membro (responda à mensagem)"),
    BotCommand("kick", "Expulsar membro sem banir (responda)"),
    BotCommand("fixar", "Fixar mensagem no grupo (responda)"),
    BotCommand("bloquear", "Bloquear palavra: /bloquear palavra"),
    BotCommand("desbloquear", "Desbloquear palavra: /desbloquear palavra"),
    BotCommand("listanegra", "Ver lista de palavras bloqueadas"),
    BotCommand("enquete", "Enviar enquete semanal no grupo"),
    BotCommand("anuncio", "Fazer anúncio oficial no grupo"),
    BotCommand("ver_testemunhos", "Ver testemunhos pendentes"),
    BotCommand("postar_testemunho", "Publicar testemunho no canal"),
    BotCommand("status", "Estatísticas completas do bot"),
    BotCommand("ver_pedidos", "Ver pedidos de oração pendentes"),
    BotCommand("listar_midia", "Ver mídias salvas na fila"),
    BotCommand("chatid", "Ver ID do chat ou usuário"),
    BotCommand("ranking", "Ver ranking de engajamento do grupo"),
    BotCommand("postar_ranking", "Postar ranking agora no grupo"),
    BotCommand("aniversario", "Cadastrar seu aniversário: /aniversario DD/MM"),
]

async def post_init(app):
    try:
        await app.bot.set_my_commands(COMANDOS_USUARIOS, scope=BotCommandScopeDefault())
        await app.bot.set_my_commands(COMANDOS_ADMINS, scope=BotCommandScopeAllPrivateChats())
        logger.info("✅ Comandos do BotFather configurados!")
    except Exception as e:
        logger.error(f"Erro ao configurar comandos: {e}")

def build_app():
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

    configurar_agendamentos(app)
    return app

def main():
    # Inicia health-check HTTP antes de tudo (Railway precisa de resposta HTTP)
    threading.Thread(target=_start_health_server, daemon=True).start()

    logger.info("🚀 Iniciando Bot Avivamento AD...")
    logger.info(f"   BOT_TOKEN configurado: {'✅' if BOT_TOKEN else '❌'}")
    logger.info(f"   DATABASE_URL configurado: {'✅' if os.getenv('DATABASE_URL') else '❌'}")

    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN não configurado! Defina nas variáveis de ambiente do Railway.")
        while True:
            time.sleep(60)

    # Inicializar banco com retry — nunca sys.exit para não esgotar restarts do Railway
    _bot_status["state"] = "db_init"
    db_tentativa = 0
    while True:
        try:
            from database import init_db
            init_db()
            logger.info("✅ Banco de dados inicializado!")
            break
        except Exception as e:
            db_tentativa += 1
            espera = min(db_tentativa * 10, 120)
            logger.error(f"❌ Falha ao inicializar banco (tentativa {db_tentativa}): {e}. Tentando em {espera}s...")
            time.sleep(espera)

    # Loop de polling com retry automático
    _bot_status["state"] = "polling"
    retry_delay = 5
    while True:
        try:
            logger.info("▶️  Construindo e iniciando polling...")
            app = build_app()
            app.run_polling(
                drop_pending_updates=False,
                allowed_updates=None,
                timeout=30,
                poll_interval=1.0,
            )
            logger.info("Polling encerrado normalmente.")
            retry_delay = 5
        except Exception as e:
            _bot_status["state"] = "error"
            logger.error(f"❌ Erro no polling: {e}. Reiniciando em {retry_delay}s...")
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)
            _bot_status["state"] = "polling"

if __name__ == "__main__":
    main()
