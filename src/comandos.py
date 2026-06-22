from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import logging
from config import OWNER_ID, CHANNEL_ID
from media_manager import (
    carregar_media, total_videos, total_imagens,
    limpar_videos, limpar_imagens
)

logger = logging.getLogger(__name__)

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if user_id == OWNER_ID:
        return True
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙏 *Olá! Sou o Bot do Avivamento AD!*\n\n"
        "Estou aqui para abençoar o grupo e o canal com a Palavra de Deus.\n\n"
        "Use /ajuda para ver os comandos disponíveis.",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin = await is_admin(update, context)
    texto = "📋 *COMANDOS DISPONÍVEIS*\n\n"
    texto += "*Comandos gerais:*\n"
    texto += "/start — Iniciar o bot\n"
    texto += "/ajuda — Ver esta lista\n"
    texto += "/versiculo — Receber um versículo\n"
    texto += "/regras — Ver as regras do grupo\n\n"

    if admin:
        texto += "*🔧 Comandos de Admin/Dono:*\n"
        texto += "/postar_versiculo — Postar versículo no canal agora\n"
        texto += "/postar_midia — Postar mídia salva no canal agora\n"
        texto += "/status — Ver status e estatísticas do bot\n"
        texto += "/listar_midia — Ver quantas mídias estão salvas\n"
        texto += "/limpar_videos — Limpar todos os vídeos salvos\n"
        texto += "/limpar_imagens — Limpar todas as imagens salvas\n"
        texto += "/banir — Banir usuário (responda a mensagem)\n"
        texto += "/silenciar — Silenciar usuário (responda a mensagem)\n"
        texto += "/liberar — Liberar usuário silenciado\n"
        texto += "/anuncio [texto] — Enviar anúncio ao grupo\n"
        texto += "/fixar — Fixar mensagem (responda a mensagem)\n"
        texto += "/postar_regras — Postar regras no grupo agora\n"

    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_versiculo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bible import get_versiculo_texto, gerar_imagem_versiculo
    buf, referencia, texto = gerar_imagem_versiculo()
    caption = f'📖 *{referencia}*\n\n_"{texto}"_\n\n🕊️ Avivamento AD'
    await update.message.reply_photo(photo=buf, caption=caption, parse_mode=ParseMode.MARKDOWN)

async def cmd_regras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from regras import REGRAS_GRUPO
    await update.message.reply_text(REGRAS_GRUPO, parse_mode=ParseMode.MARKDOWN)

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores podem usar este comando.")
        return
    videos = total_videos()
    imagens = total_imagens()
    texto = (
        "📊 *STATUS DO BOT — AVIVAMENTO AD*\n\n"
        f"🎥 Vídeos salvos: *{videos}*\n"
        f"🖼️ Imagens salvas: *{imagens}*\n\n"
        "✅ Bot funcionando normalmente!\n"
        "⏰ Posts automáticos ativos:\n"
        "  • Mídias suas: 09h e 19h\n"
        "  • Versículos: 07h, 13h e 21h\n"
        "  • Regras no grupo: a cada 4h\n\n"
        "🕊️ _Que Deus abençoe este ministério!_"
    )
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_listar_midia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores podem usar este comando.")
        return
    videos = total_videos()
    imagens = total_imagens()
    await update.message.reply_text(
        f"📦 *Mídias armazenadas:*\n\n"
        f"🎥 Vídeos: *{videos}*\n"
        f"🖼️ Imagens: *{imagens}*\n\n"
        f"_Para adicionar, envie no privado do bot._",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_limpar_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    limpar_videos()
    await update.message.reply_text("✅ Todos os vídeos foram removidos.")

async def cmd_limpar_imagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    limpar_imagens()
    await update.message.reply_text("✅ Todas as imagens foram removidas.")

async def cmd_banir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores podem banir.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Responda à mensagem do usuário que deseja banir.")
        return
    alvo = update.message.reply_to_message.from_user
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, alvo.id)
        await update.message.reply_text(
            f"🚫 *{alvo.first_name}* foi banido(a) do grupo.\n"
            f"_Que Deus o(a) alcance com seu amor._",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao banir: {e}")

async def cmd_silenciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores podem silenciar.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Responda à mensagem do usuário que deseja silenciar.")
        return
    alvo = update.message.reply_to_message.from_user
    try:
        perms = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
        )
        await context.bot.restrict_chat_member(update.effective_chat.id, alvo.id, perms)
        await update.message.reply_text(
            f"🔇 *{alvo.first_name}* foi silenciado(a).",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao silenciar: {e}")

async def cmd_liberar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores podem liberar.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Responda à mensagem do usuário que deseja liberar.")
        return
    alvo = update.message.reply_to_message.from_user
    try:
        perms = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
        )
        await context.bot.restrict_chat_member(update.effective_chat.id, alvo.id, perms)
        await update.message.reply_text(
            f"✅ *{alvo.first_name}* foi liberado(a) para falar.",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao liberar: {e}")

async def cmd_anuncio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores podem fazer anúncios.")
        return
    if not context.args:
        await update.message.reply_text("⚠️ Use: /anuncio [texto do anúncio]")
        return
    texto = " ".join(context.args)
    mensagem = f"📢 *ANÚNCIO OFICIAL*\n\n{texto}\n\n🕊️ _Administração — Avivamento AD_"
    await context.bot.send_message(update.effective_chat.id, mensagem, parse_mode=ParseMode.MARKDOWN)

async def cmd_fixar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores podem fixar mensagens.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Responda à mensagem que deseja fixar.")
        return
    try:
        await context.bot.pin_chat_message(update.effective_chat.id, update.message.reply_to_message.message_id)
        await update.message.reply_text("📌 Mensagem fixada com sucesso!")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao fixar: {e}")

async def cmd_postar_regras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    from regras import REGRAS_GRUPO
    from config import GROUP_ID
    await context.bot.send_message(GROUP_ID, REGRAS_GRUPO, parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text("✅ Regras postadas no grupo!")

async def cmd_postar_versiculo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    from bible import gerar_imagem_versiculo
    from config import CHANNEL_ID
    buf, referencia, texto = gerar_imagem_versiculo()
    link_canal = "https://t.me/avivamentoad"
    caption = (
        f'📖 *{referencia}*\n\n_"{texto}"_\n\n'
        f'🕊️ *Avivamento AD*\n\n'
        f'[📤 Compartilhe esta bênção]({link_canal})'
    )
    await context.bot.send_photo(CHANNEL_ID, photo=buf, caption=caption, parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text("✅ Versículo postado no canal!")

async def cmd_postar_midia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    from agendador import postar_midia_no_canal
    resultado = await postar_midia_no_canal(context)
    if resultado:
        await update.message.reply_text("✅ Mídia postada no canal!")
    else:
        await update.message.reply_text("⚠️ Nenhuma mídia salva. Envie vídeos ou imagens no privado do bot.")
