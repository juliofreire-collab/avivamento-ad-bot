import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram import ChatPermissions
from datetime import datetime, timedelta
from config import OWNER_ID, GROUP_ID, PALAVROES_EXATOS
from regras import REGRAS_GRUPO
from media_manager import adicionar_video, adicionar_imagem
from avisos import registrar_aviso, get_avisos
from oracao import salvar_pedido

logger = logging.getLogger(__name__)

LINK_CANAL = "https://t.me/avivamentoad"
LINK_GRUPO = "https://t.me/+FALJMPVXpj1kOGQx"

# Guarda mensagens de verificação pendentes: {user_id: message_id}
_verificacoes_pendentes: dict = {}

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
    except Exception as e:
        logger.warning(f"is_group_admin: não foi possível verificar {user_id} no grupo {GROUP_ID}: {e}")
        return False

async def _auto_kick_pendente(context: ContextTypes.DEFAULT_TYPE):
    """Expulsa membro que não clicou no botão dentro do prazo"""
    data = context.job.data
    user_id = data["user_id"]
    chat_id = data["chat_id"]
    msg_id = data["msg_id"]
    nome = data["nome"]

    if user_id not in _verificacoes_pendentes:
        return  # Já aceitou, não faz nada

    try:
        await context.bot.delete_message(chat_id, msg_id)
    except:
        pass

    try:
        await context.bot.ban_chat_member(chat_id, user_id)
        await context.bot.unban_chat_member(chat_id, user_id)
        await context.bot.send_message(
            chat_id,
            f"⏰ *{nome}* não aceitou as regras em 5 minutos e foi removido(a).\n"
            f"_Poderá voltar pelo link de convite quando estiver pronto(a)._",
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"Membro {nome} ({user_id}) removido por não aceitar as regras.")
    except Exception as e:
        logger.error(f"Erro ao expulsar membro inativo: {e}")

    _verificacoes_pendentes.pop(user_id, None)

async def handle_novo_membro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        for membro in update.message.new_chat_members:
            if membro.is_bot:
                continue

            nome = membro.first_name or "Irmão(ã)"
            chat_id = update.effective_chat.id

            # 1. Restringir imediatamente até aceitar as regras
            try:
                perms_bloqueado = ChatPermissions(
                    can_send_messages=False,
                    can_send_audios=False,
                    can_send_documents=False,
                    can_send_photos=False,
                    can_send_videos=False,
                    can_send_video_notes=False,
                    can_send_voice_notes=False,
                    can_send_polls=False,
                    can_send_other_messages=False
                )
                await context.bot.restrict_chat_member(chat_id, membro.id, perms_bloqueado)
            except Exception as e:
                logger.warning(f"Não foi possível restringir {nome}: {e}")

            # 2. Buscar foto de perfil
            foto_id = None
            try:
                fotos = await context.bot.get_user_profile_photos(membro.id, limit=1)
                if fotos.photos:
                    foto_id = fotos.photos[0][-1].file_id
            except:
                pass

            # 3. Montar mensagem de boas-vindas com botão
            texto = (
                f"🙏 *Seja muito bem-vindo(a), {nome}!*\n\n"
                f"Você entrou na família *Avivamento AD*! ✝️\n\n"
                f"Para participar do grupo, por favor *leia e aceite as regras* clicando no botão abaixo.\n\n"
                f"⏰ _Você tem 5 minutos para aceitar, ou será removido(a) automaticamente._\n\n"
                f"📖 _\"Porque onde estiverem dois ou três reunidos em meu nome, ali estou eu no meio deles.\"_ — Mateus 18:20"
            )

            botao = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "✅ Li e Aceito as Regras",
                    callback_data=f"aceitar_regras:{membro.id}"
                )
            ]])

            # 4. Enviar boas-vindas com ou sem foto
            if foto_id:
                msg = await context.bot.send_photo(
                    chat_id, photo=foto_id,
                    caption=texto, parse_mode=ParseMode.MARKDOWN,
                    reply_markup=botao
                )
            else:
                msg = await context.bot.send_message(
                    chat_id, texto,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=botao
                )

            # 5. Registrar verificação pendente
            _verificacoes_pendentes[membro.id] = msg.message_id

            # 6. Agendar auto-kick em 5 minutos
            context.job_queue.run_once(
                _auto_kick_pendente,
                when=300,
                data={"user_id": membro.id, "chat_id": chat_id, "msg_id": msg.message_id, "nome": nome},
                name=f"kick_{membro.id}"
            )

            logger.info(f"Boas-vindas com verificação enviadas para: {nome} ({membro.id})")

    except Exception as e:
        logger.error(f"Erro ao receber novo membro: {e}")

async def handle_aceitar_regras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback quando membro clica em 'Aceito as Regras'"""
    query = update.callback_query
    data = query.data

    if not data.startswith("aceitar_regras:"):
        return

    user_id_alvo = int(data.split(":")[1])
    user_clicou = query.from_user.id
    nome = query.from_user.first_name or "Membro"
    chat_id = query.message.chat_id

    # Só o próprio membro pode clicar no seu botão
    if user_clicou != user_id_alvo:
        await query.answer("⚠️ Este botão é apenas para o novo membro.", show_alert=True)
        return

    # Responder ao callback imediatamente para evitar spinner eterno no Telegram
    await query.answer("✅ Bem-vindo(a) ao Avivamento AD! 🙏")

    # Liberar permissões completas
    try:
        perms_livre = ChatPermissions(
            can_send_messages=True,
            can_send_audios=True,
            can_send_documents=True,
            can_send_photos=True,
            can_send_videos=True,
            can_send_video_notes=True,
            can_send_voice_notes=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_invite_users=True
        )
        await context.bot.restrict_chat_member(chat_id, user_id_alvo, perms_livre)
    except Exception as e:
        logger.error(f"Erro ao liberar {nome}: {e}")

    # Remover da lista de pendentes
    _verificacoes_pendentes.pop(user_id_alvo, None)

    # Cancelar o job de auto-kick
    jobs = context.job_queue.get_jobs_by_name(f"kick_{user_id_alvo}")
    for job in jobs:
        job.schedule_removal()

    # Apagar a mensagem com o botão
    try:
        await query.message.delete()
    except:
        pass

    # Confirmar e dar boas-vindas completas com as regras
    await context.bot.send_message(
        chat_id,
        f"✅ *{nome} aceitou as regras e já pode participar!*\n\n"
        f"🙏 Que Deus abençoe sua participação em nossa família!\n\n"
        f"📢 Conheça também nosso canal: [Avivamento AD]({LINK_CANAL})\n\n"
        f"_\"Tão bom e tão agradável é que os irmãos vivam em união!\"_ — Salmos 133:1",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

    # Enviar regras em seguida
    await context.bot.send_message(chat_id, REGRAS_GRUPO, parse_mode=ParseMode.MARKDOWN)

    # Pontuar entrada
    try:
        from ranking import adicionar_pontos
        adicionar_pontos(user_id_alvo, nome, "entrada")
    except:
        pass

    logger.info(f"{nome} ({user_id_alvo}) aceitou as regras e foi liberado.")

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

    # Detectar palavrão antes de pontuar (quem manda palavrão não ganha ponto)
    tem_palavrao = contem_palavrao(texto)

    # Pontuar participação no grupo (máx 5x/dia, apenas mensagens limpas)
    if not tem_palavrao:
        try:
            from ranking import adicionar_pontos
            adicionar_pontos(user_id, user.first_name or "Membro", "mensagem")
        except:
            pass

    # Detectar pedido de oração via texto livre
    texto_lower = texto.lower()
    nome = user.first_name or "Membro"
    if any(kw in texto_lower for kw in ["pedido de oração", "peço oração", "preciso de oração", "ore por mim"]):
        salvar_pedido(nome, user_id, texto)
        try:
            from ranking import adicionar_pontos
            adicionar_pontos(user_id, nome, "oracao")
        except:
            pass
        await update.message.reply_text(
            f"🙏 *{nome}*, seu pedido de oração foi registrado!\n\n"
            f"Os irmãos do grupo vão interceder por você. "
            f"_\"Confessai as vossas ofensas uns aos outros e orai uns pelos outros.\"_ — Tiago 5:16",
            parse_mode=ParseMode.MARKDOWN
        )

    # Filtro de palavrões
    if tem_palavrao:
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
    nome_user = update.effective_user.first_name or "Usuário"

    # Aceita DONO e qualquer ADMIN do grupo
    admin = await is_group_admin(context.bot, user_id)
    logger.info(f"handle_midia_privado: user={user_id} ({nome_user}) admin={admin}")

    if not admin:
        await update.message.reply_text(
            "❌ Apenas administradores do grupo podem enviar mídias para postagem no canal.\n\n"
            "💬 Se quiser enviar um *testemunho* para ser publicado no canal, "
            "basta digitar o texto aqui! 🙏",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    caption = update.message.caption or ""
    file_id = None
    tipo = ""

    if update.message.video:
        file_id = update.message.video.file_id
        tipo = "🎥 Vídeo"
        salvo = adicionar_video(file_id, caption)
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
        tipo = "🖼️ Imagem"
        salvo = adicionar_imagem(file_id, caption)
    elif update.message.document:
        mime = update.message.document.mime_type or ""
        file_id = update.message.document.file_id
        if mime.startswith("video"):
            tipo = "🎥 Vídeo (documento)"
            salvo = adicionar_video(file_id, caption)
        elif mime.startswith("image"):
            tipo = "🖼️ Imagem (documento)"
            salvo = adicionar_imagem(file_id, caption)
        else:
            await update.message.reply_text(
                "⚠️ Formato não suportado. Envie vídeos (MP4) ou imagens (JPG/PNG).\n"
                "Você também pode enviar arquivos de vídeo como documento."
            )
            return
    else:
        await update.message.reply_text(
            "📎 Tipo de mídia não reconhecido.\n\n"
            "Envie:\n• 🎥 Vídeos (MP4)\n• 🖼️ Fotos (JPG/PNG)\n• 📄 Arquivos de vídeo como documento"
        )
        return

    from media_manager import total_videos, total_imagens
    total_v = total_videos()
    total_i = total_imagens()

    if salvo:
        logger.info(f"Mídia salva por {nome_user} ({user_id}): tipo={tipo} file_id={file_id[:20]}...")
        await update.message.reply_text(
            f"✅ *{tipo} adicionado à fila do canal!*\n\n"
            f"📊 *Fila atual:*\n"
            f"🎥 Vídeos: {total_v}\n"
            f"🖼️ Imagens: {total_i}\n\n"
            f"⏰ *Postagem automática:* 09h e 19h (horário de Brasília)\n\n"
            f"💡 Para postar *agora*, use o comando /postar\\_midia\n"
            f"📋 Para ver a fila completa, use /fila",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(
            f"⚠️ *Esta mídia já está na fila.*\n\n"
            f"📊 *Fila atual:*\n"
            f"🎥 Vídeos: {total_v}\n"
            f"🖼️ Imagens: {total_i}\n\n"
            f"💡 Use /postar\\_midia para postar agora ou /fila para ver a fila.",
            parse_mode=ParseMode.MARKDOWN
        )

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
