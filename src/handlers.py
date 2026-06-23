import logging
import re
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram import ChatPermissions
from datetime import datetime, timedelta
from config import OWNER_ID, GROUP_ID, PALAVROES_EXATOS
from regras import BOAS_VINDAS_TEMPLATE, REGRAS_GRUPO
from media_manager import adicionar_video, adicionar_imagem
from avisos import registrar_aviso, get_avisos
from oracao import salvar_pedido

logger = logging.getLogger(__name__)

LINK_CANAL = "https://t.me/avivamentoad"
LINK_GRUPO = "https://t.me/+FALJMPVXpj1kOGQx"

def contem_palavrao(texto: str) -> bool:
    texto_lower = texto.lower()
    for padrao in PALAVROES_EXATOS:
        if re.search(padrao, texto_lower):
            return True
    # Verifica palavras personalizadas
    try:
        from comandos import carregar_palavras_custom
        for palavra in carregar_palavras_custom():
            if palavra.lower() in texto_lower:
                return True
    except:
        pass
    return False

async def is_group_admin(bot, user_id: int) -> bool:
    """Verifica se o usuário é admin do grupo"""
    if user_id == OWNER_ID:
        return True
    try:
        member = await bot.get_chat_member(int(GROUP_ID), user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

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

            logger.info(f"Boas-vindas enviadas para: {nome} ({membro.id})")

    except Exception as e:
        logger.error(f"Erro ao receber novo membro: {e}")

async def handle_mensagem_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    if update.effective_chat.id != int(GROUP_ID):
        return

    texto = update.message.text
    user = update.effective_user
    user_id = user.id

    # Admins e dono ficam livres do filtro
    if user_id == OWNER_ID:
        return
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        if member.status in ["administrator", "creator"]:
            return
    except:
        pass

    # Detectar pedido de oração via texto livre
    texto_lower = texto.lower()
    if any(kw in texto_lower for kw in ["pedido de oração", "peço oração", "preciso de oração", "ore por mim"]):
        salvar_pedido(user.first_name or "Membro", user_id, texto)
        await update.message.reply_text(
            f"🙏 *{user.first_name}*, seu pedido de oração foi registrado!\n\n"
            f"Os irmãos do grupo vão interceder por você. "
            f"_\"Confessai as vossas ofensas uns aos outros e orai uns pelos outros.\"_ — Tiago 5:16",
            parse_mode=ParseMode.MARKDOWN
        )

    # Filtro de palavrões
    if contem_palavrao(texto):
        try:
            await update.message.delete()
        except Exception as e:
            logger.error(f"Erro ao deletar mensagem: {e}")

        total_avisos = registrar_aviso(user_id)

        if total_avisos == 1:
            await context.bot.send_message(
                update.effective_chat.id,
                f"⚠️ *Atenção, {user.first_name}!*\n\n"
                f"Sua mensagem foi removida por conter linguagem inapropriada.\n"
                f"Este é seu *1º aviso*. Por favor, respeite as regras do grupo.\n\n"
                f"_\"Não saia da vossa boca nenhuma palavra torpe.\"_ — Efésios 4:29",
                parse_mode=ParseMode.MARKDOWN
            )
        elif total_avisos == 2:
            try:
                until = datetime.now() + timedelta(hours=1)
                perms = ChatPermissions(can_send_messages=False)
                await context.bot.restrict_chat_member(
                    update.effective_chat.id, user_id, perms, until_date=until
                )
                await context.bot.send_message(
                    update.effective_chat.id,
                    f"🔇 *{user.first_name}*, você foi silenciado(a) por *1 hora*.\n\n"
                    f"Este é seu *2º aviso*. Mais um e você será removido do grupo.\n\n"
                    f"_\"O homem sábio cala a boca diante do mal.\"_",
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                logger.error(f"Erro ao silenciar: {e}")
        else:
            try:
                await context.bot.ban_chat_member(update.effective_chat.id, user_id)
                await context.bot.send_message(
                    update.effective_chat.id,
                    f"🚫 *{user.first_name}* foi removido(a) do grupo.\n\n"
                    f"Após *3 avisos*, a remoção é necessária para manter a paz do grupo.\n"
                    f"Que Deus o(a) alcance com Seu amor. 🙏\n\n"
                    f"_\"Afasta-te do mal e pratica o bem; busca a paz e segue-a.\"_ — Salmos 34:14",
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                logger.error(f"Erro ao banir: {e}")

async def handle_texto_privado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return
    user_id = update.effective_user.id
    texto = update.message.text or ""
    if texto.startswith("/"):
        return

    # Se não é o dono nem admin, trata como possível testemunho
    admin = await is_group_admin(context.bot, user_id)
    if not admin and len(texto) > 20:
        from testemunhos import salvar_testemunho
        nome = update.effective_user.first_name or "Membro"
        salvar_testemunho(nome, user_id, texto)
        await update.message.reply_text(
            f"🌟 *Testemunho recebido, {nome}!*\n\n"
            f"_{texto[:100]}{'...' if len(texto) > 100 else ''}_\n\n"
            f"Seu testemunho foi registrado e será publicado no canal em breve! 🙏\n\n"
            f"_\"E venceram-no pelo sangue do Cordeiro e pela palavra do seu testemunho.\"_ — Apocalipse 12:11",
            parse_mode=ParseMode.MARKDOWN
        )
        if OWNER_ID:
            try:
                await context.bot.send_message(
                    OWNER_ID,
                    f"🌟 *Novo testemunho recebido!*\n\nDe: *{nome}*\n\n_{texto[:200]}{'...' if len(texto) > 200 else ''}_\n\nUse /ver_testemunhos para ver todos os pendentes.",
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                pass
    elif not admin:
        await update.message.reply_text(
            "🙏 Olá! Para enviar um testemunho, escreva seu texto com mais de 20 caracteres.\n\n"
            "Para pedidos de oração, use /oracao no grupo ou aqui.",
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_midia_privado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Aceita DONO e qualquer ADMIN do grupo
    admin = await is_group_admin(context.bot, user_id)
    if not admin:
        await update.message.reply_text(
            "❌ Apenas administradores podem enviar mídias para postagem no canal.\n\n"
            "💬 Se quiser enviar um *testemunho* para ser publicado no canal, "
            "basta digitar o texto aqui! 🙏",
            parse_mode=ParseMode.MARKDOWN
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
        import media_manager as mm
        media = mm.carregar_media()
        total_v = len(media["videos"])
        total_i = len(media["imagens"])
        await update.message.reply_text(
            f"✅ *{tipo} salvo com sucesso!*\n\n"
            f"📊 Total armazenado:\n"
            f"🎥 Vídeos: {total_v}\n"
            f"🖼️ Imagens: {total_i}\n\n"
            f"Será postado no canal às 09h ou 19h.\n"
            f"Use /fila para ver a fila ou /postar_midia para postar agora.",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text("⚠️ Esta mídia já estava salva anteriormente.")

async def handle_saida_membro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        membro = update.message.left_chat_member
        if membro and not membro.is_bot:
            nome = membro.first_name or "Um membro"
            await context.bot.send_message(
                update.effective_chat.id,
                f"🙏 *{nome}* saiu do grupo.\n"
                f"Que Deus o(a) guie e abençoe sempre!\n"
                f"_\"O Senhor abençoe você e te guarde.\"_ — Números 6:24",
                parse_mode=ParseMode.MARKDOWN
            )
    except Exception as e:
        logger.error(f"Erro ao processar saída de membro: {e}")
