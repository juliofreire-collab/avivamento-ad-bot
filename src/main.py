import logging
import sys
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters
)
from config import BOT_TOKEN
from comandos import (
    cmd_start, cmd_ajuda, cmd_versiculo, cmd_regras, cmd_devocional, cmd_oracao,
    cmd_postar_versiculo, cmd_postar_midia, cmd_postar_devocional,
    cmd_postar_regras, cmd_postar_oracao, cmd_postar_engajamento,
    cmd_banir, cmd_silenciar, cmd_liberar, cmd_resetar_avisos,
    cmd_anuncio, cmd_fixar,
    cmd_status, cmd_listar_midia, cmd_limpar_videos, cmd_limpar_imagens, cmd_ver_pedidos,
    cmd_chatid, cmd_enquete,
    cmd_testemunho, cmd_ver_testemunhos, cmd_postar_testemunho
)
from handlers import (
    handle_novo_membro, handle_mensagem_grupo,
    handle_midia_privado, handle_saida_membro, handle_texto_privado
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

    logger.info("🚀 Iniciando Bot Avivamento AD...")

    app = Application.builder().token(BOT_TOKEN).build()

    # Comandos gerais
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("ajuda", cmd_ajuda))
    app.add_handler(CommandHandler("versiculo", cmd_versiculo))
    app.add_handler(CommandHandler("regras", cmd_regras))
    app.add_handler(CommandHandler("devocional", cmd_devocional))
    app.add_handler(CommandHandler("oracao", cmd_oracao))

    # Admin — Canal
    app.add_handler(CommandHandler("postar_versiculo", cmd_postar_versiculo))
    app.add_handler(CommandHandler("postar_midia", cmd_postar_midia))
    app.add_handler(CommandHandler("postar_devocional", cmd_postar_devocional))

    # Admin — Grupo
    app.add_handler(CommandHandler("postar_regras", cmd_postar_regras))
    app.add_handler(CommandHandler("postar_oracao", cmd_postar_oracao))
    app.add_handler(CommandHandler("postar_engajamento", cmd_postar_engajamento))
    app.add_handler(CommandHandler("banir", cmd_banir))
    app.add_handler(CommandHandler("silenciar", cmd_silenciar))
    app.add_handler(CommandHandler("liberar", cmd_liberar))
    app.add_handler(CommandHandler("resetar_avisos", cmd_resetar_avisos))
    app.add_handler(CommandHandler("anuncio", cmd_anuncio))
    app.add_handler(CommandHandler("fixar", cmd_fixar))

    # Testemunhos
    app.add_handler(CommandHandler("testemunho", cmd_testemunho))
    app.add_handler(CommandHandler("ver_testemunhos", cmd_ver_testemunhos))
    app.add_handler(CommandHandler("postar_testemunho", cmd_postar_testemunho))

    # Utilitários
    app.add_handler(CommandHandler("chatid", cmd_chatid))
    app.add_handler(CommandHandler("enquete", cmd_enquete))

    # Estatísticas
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("listar_midia", cmd_listar_midia))
    app.add_handler(CommandHandler("limpar_videos", cmd_limpar_videos))
    app.add_handler(CommandHandler("limpar_imagens", cmd_limpar_imagens))
    app.add_handler(CommandHandler("ver_pedidos", cmd_ver_pedidos))

    # Eventos de grupo
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_novo_membro))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_saida_membro))

    # Mensagens do grupo (filtro de palavrões + pedidos de oração)
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_mensagem_grupo))

    # Mídias no privado (apenas dono)
    app.add_handler(MessageHandler(
        (filters.VIDEO | filters.PHOTO | filters.Document.ALL) & filters.ChatType.PRIVATE,
        handle_midia_privado
    ))

    # Texto no privado — recebe testemunhos de membros
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND,
        handle_texto_privado
    ))

    # Agendamentos
    configurar_agendamentos(app)

    logger.info("✅ Bot iniciado! Aguardando mensagens 24/7...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
