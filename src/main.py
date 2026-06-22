import logging
import os
import sys
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, CallbackQueryHandler
)
from config import BOT_TOKEN, OWNER_ID
from comandos import (
    cmd_start, cmd_ajuda, cmd_versiculo, cmd_regras,
    cmd_status, cmd_listar_midia, cmd_limpar_videos, cmd_limpar_imagens,
    cmd_banir, cmd_silenciar, cmd_liberar, cmd_anuncio, cmd_fixar,
    cmd_postar_regras, cmd_postar_versiculo, cmd_postar_midia
)
from handlers import (
    handle_novo_membro, handle_mensagem_grupo,
    handle_midia_privado, handle_saida_membro
)
from agendador import configurar_agendamentos

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN não configurado!")
        sys.exit(1)

    logger.info("Iniciando Bot do Avivamento AD...")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("ajuda", cmd_ajuda))
    app.add_handler(CommandHandler("versiculo", cmd_versiculo))
    app.add_handler(CommandHandler("regras", cmd_regras))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("listar_midia", cmd_listar_midia))
    app.add_handler(CommandHandler("limpar_videos", cmd_limpar_videos))
    app.add_handler(CommandHandler("limpar_imagens", cmd_limpar_imagens))
    app.add_handler(CommandHandler("banir", cmd_banir))
    app.add_handler(CommandHandler("silenciar", cmd_silenciar))
    app.add_handler(CommandHandler("liberar", cmd_liberar))
    app.add_handler(CommandHandler("anuncio", cmd_anuncio))
    app.add_handler(CommandHandler("fixar", cmd_fixar))
    app.add_handler(CommandHandler("postar_regras", cmd_postar_regras))
    app.add_handler(CommandHandler("postar_versiculo", cmd_postar_versiculo))
    app.add_handler(CommandHandler("postar_midia", cmd_postar_midia))

    app.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        handle_novo_membro
    ))
    app.add_handler(MessageHandler(
        filters.StatusUpdate.LEFT_CHAT_MEMBER,
        handle_saida_membro
    ))

    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS,
        handle_mensagem_grupo
    ))

    app.add_handler(MessageHandler(
        (filters.VIDEO | filters.PHOTO | filters.Document.ALL) & filters.ChatType.PRIVATE,
        handle_midia_privado
    ))

    configurar_agendamentos(app)

    logger.info("Bot iniciado! Aguardando mensagens...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
