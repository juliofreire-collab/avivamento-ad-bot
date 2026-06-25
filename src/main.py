import logging
import sys
from telegram import BotCommand, BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats, BotCommandScopeDefault
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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

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
    """Configura os comandos no BotFather automaticamente"""
    try:
        # Comandos padrão (para todos)
        await app.bot.set_my_commands(COMANDOS_USUARIOS, scope=BotCommandScopeDefault())
        # Comandos para chat privado (admins vêem mais)
        await app.bot.set_my_commands(COMANDOS_ADMINS, scope=BotCommandScopeAllPrivateChats())
        logger.info("✅ Comandos do BotFather configurados!")
    except Exception as e:
        logger.error(f"Erro ao configurar comandos: {e}")

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN não configurado!")
        sys.exit(1)

    logger.info("🚀 Iniciando Bot Avivamento AD...")

    try:
        from database import init_db
        init_db()
    except Exception as e:
        logger.error(f"❌ Falha ao inicializar banco de dados: {e}")
        sys.exit(1)

    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # ── Comandos para todos ──
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("ping", cmd_ping))
    app.add_handler(CommandHandler("ajuda", cmd_ajuda))
    app.add_handler(CommandHandler("versiculo", cmd_versiculo))
    app.add_handler(CommandHandler("regras", cmd_regras))
    app.add_handler(CommandHandler("devocional", cmd_devocional))
    app.add_handler(CommandHandler("oracao", cmd_oracao))
    app.add_handler(CommandHandler("testemunho", cmd_testemunho))

    # ── Canal ──
    app.add_handler(CommandHandler("postar", cmd_postar))
    app.add_handler(CommandHandler("postar_versiculo", cmd_postar_versiculo))
    app.add_handler(CommandHandler("postar_midia", cmd_postar_midia))
    app.add_handler(CommandHandler("postar_devocional", cmd_postar_devocional))
    app.add_handler(CommandHandler("fila", cmd_fila))
    app.add_handler(CommandHandler("horarios", cmd_horarios))
    app.add_handler(CommandHandler("proxima", cmd_proxima))

    # ── Grupo ──
    app.add_handler(CommandHandler("postar_regras", cmd_postar_regras))
    app.add_handler(CommandHandler("postar_oracao", cmd_postar_oracao))
    app.add_handler(CommandHandler("postar_engajamento", cmd_postar_engajamento))
    app.add_handler(CommandHandler("enquete", cmd_enquete))
    app.add_handler(CommandHandler("anuncio", cmd_anuncio))
    app.add_handler(CommandHandler("fixar", cmd_fixar))

    # ── Moderação ──
    app.add_handler(CommandHandler("banir", cmd_banir))
    app.add_handler(CommandHandler("kick", cmd_kick))
    app.add_handler(CommandHandler("silenciar", cmd_silenciar))
    app.add_handler(CommandHandler("liberar", cmd_liberar))
    app.add_handler(CommandHandler("avisar", cmd_avisar))
    app.add_handler(CommandHandler("perdoar", cmd_perdoar))
    app.add_handler(CommandHandler("resetar_avisos", cmd_resetar_avisos))
    app.add_handler(CommandHandler("advertencias", cmd_advertencias))
    app.add_handler(CommandHandler("info", cmd_info))

    # ── Palavras bloqueadas ──
    app.add_handler(CommandHandler("bloquear", cmd_bloquear))
    app.add_handler(CommandHandler("desbloquear", cmd_desbloquear))
    app.add_handler(CommandHandler("listanegra", cmd_listanegra))

    # ── Testemunhos ──
    app.add_handler(CommandHandler("ver_testemunhos", cmd_ver_testemunhos))
    app.add_handler(CommandHandler("postar_testemunho", cmd_postar_testemunho))

    # ── Ranking ──
    app.add_handler(CommandHandler("ranking", cmd_ranking))
    app.add_handler(CommandHandler("postar_ranking", cmd_postar_ranking))

    # ── Aniversários ──
    app.add_handler(CommandHandler("aniversario", cmd_aniversario))

    # ── Estatísticas ──
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("listar_midia", cmd_listar_midia))
    app.add_handler(CommandHandler("limpar_videos", cmd_limpar_videos))
    app.add_handler(CommandHandler("limpar_imagens", cmd_limpar_imagens))
    app.add_handler(CommandHandler("ver_pedidos", cmd_ver_pedidos))
    app.add_handler(CommandHandler("chatid", cmd_chatid))
    app.add_handler(CommandHandler("importar", cmd_importar))
    app.add_handler(CommandHandler("testar", cmd_testar))

    # ── Eventos de grupo ──
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_novo_membro))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_saida_membro))

    # ── Mensagens do grupo (filtro de palavrões + pedidos de oração) ──
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_mensagem_grupo))

    # ── Mídias no privado (dono e admins do grupo) ──
    app.add_handler(MessageHandler(
        (filters.VIDEO | filters.PHOTO | filters.Document.ALL) & filters.ChatType.PRIVATE,
        handle_midia_privado
    ))

    # ── Texto no privado — testemunhos de membros ──
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND,
        handle_texto_privado
    ))

    # ── Botão "Aceito as Regras" — verificação de novo membro ──
    app.add_handler(CallbackQueryHandler(handle_aceitar_regras, pattern=r"^aceitar_regras:"))

    # ── Agendamentos ──
    configurar_agendamentos(app)

    logger.info("✅ Bot iniciado! Aguardando mensagens 24/7...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
