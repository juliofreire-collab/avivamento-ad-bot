import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import OWNER_ID, GROUP_ID, PALAVROES
from regras import BOAS_VINDAS_TEMPLATE, REGRAS_GRUPO
from media_manager import adicionar_video, adicionar_imagem

logger = logging.getLogger(__name__)

LINK_CANAL = "https://t.me/avivamentoad"
LINK_GRUPO = "https://t.me/+FALJMPVXpj1kOGQx"

async def handle_novo_membro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        for membro in update.message.new_chat_members:
            if membro.is_bot:
                continue

            nome = membro.first_name or "Irmão(ã)"
            boas_vindas = BOAS_VINDAS_TEMPLATE.format(nome=nome)

            foto_id = None
            try:
                fotos = await context.bot.get_user_profile_photos(membro.id, limit=1)
                if fotos.photos:
                    foto_id = fotos.photos[0][-1].file_id
            except:
                pass

            if foto_id:
                await context.bot.send_photo(
                    update.effective_chat.id,
                    photo=foto_id,
                    caption=boas_vindas,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await context.bot.send_message(
                    update.effective_chat.id,
                    boas_vindas,
                    parse_mode=ParseMode.MARKDOWN
                )

            await context.bot.send_message(
                update.effective_chat.id,
                REGRAS_GRUPO,
                parse_mode=ParseMode.MARKDOWN
            )

            logger.info(f"Boas-vindas enviadas para: {nome} ({membro.id})")

    except Exception as e:
        logger.error(f"Erro ao receber novo membro: {e}")

async def handle_mensagem_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    if update.effective_chat.id != int(GROUP_ID):
        return

    texto = update.message.text.lower()
    user = update.effective_user
    user_id = user.id

    if user_id == OWNER_ID:
        return
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        if member.status in ["administrator", "creator"]:
            return
    except:
        pass

    for palavrao in PALAVROES:
        if palavrao in texto:
            try:
                await update.message.delete()
                logger.info(f"Mensagem com palavrão deletada de {user.first_name}")
            except Exception as e:
                logger.error(f"Erro ao deletar mensagem: {e}")

            try:
                await context.bot.ban_chat_member(update.effective_chat.id, user_id)
                aviso = (
                    f"🚫 *{user.first_name}* foi banido(a) por usar linguagem inapropriada.\n\n"
                    f"_Este é um grupo cristão. Respeito é fundamental._\n\n"
                    f"_\"Não saia da vossa boca nenhuma palavra torpe.\"_ — Efésios 4:29"
                )
                await context.bot.send_message(
                    update.effective_chat.id,
                    aviso,
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                logger.error(f"Erro ao banir usuário: {e}")
            break

async def handle_midia_privado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != OWNER_ID:
        await update.message.reply_text(
            "❌ Apenas o dono do bot pode enviar mídias para postagem."
        )
        return

    caption = update.message.caption or ""
    salvo = False
    tipo = ""

    if update.message.video:
        file_id = update.message.video.file_id
        salvo = adicionar_video(file_id, caption)
        tipo = "🎥 Vídeo"
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
        salvo = adicionar_imagem(file_id, caption)
        tipo = "🖼️ Imagem"
    elif update.message.document:
        mime = update.message.document.mime_type or ""
        if mime.startswith("video"):
            file_id = update.message.document.file_id
            salvo = adicionar_video(file_id, caption)
            tipo = "🎥 Vídeo (documento)"
        elif mime.startswith("image"):
            file_id = update.message.document.file_id
            salvo = adicionar_imagem(file_id, caption)
            tipo = "🖼️ Imagem (documento)"
        else:
            await update.message.reply_text("⚠️ Formato não suportado. Envie vídeos ou imagens.")
            return
    else:
        return

    if salvo:
        await update.message.reply_text(
            f"✅ *{tipo} salvo com sucesso!*\n\n"
            f"Será postado aleatoriamente no canal às 09h ou 19h.\n"
            f"Use /listar_midia para ver o total salvo.",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(
            f"⚠️ Esta mídia já estava salva anteriormente."
        )

async def handle_saida_membro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        membro = update.message.left_chat_member
        if membro and not membro.is_bot:
            nome = membro.first_name or "Um membro"
            await context.bot.send_message(
                update.effective_chat.id,
                f"🙏 *{nome}* saiu do grupo. Que Deus o(a) guie sempre!\n"
                f"_\"O Senhor abençoe você e te guarde.\"_ — Números 6:24",
                parse_mode=ParseMode.MARKDOWN
            )
    except Exception as e:
        logger.error(f"Erro ao processar saída de membro: {e}")
