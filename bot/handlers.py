import logging
import re
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import OWNER_ID, GROUP_ID, PALAVROES_EXATOS

logger = logging.getLogger(__name__)

PALAVRAS_CUSTOM_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "palavras_custom.json")

BOAS_VINDAS = [
    "🙏 Seja bem-vindo(a) à família *Avivamento AD*, {nome}!\n\nEstamos felizes em ter você aqui. Leia as regras e participe com amor e respeito! 🔥",
    "🔥 Olá, {nome}! Bem-vindo(a) ao grupo *Avivamento AD*!\n\nQue Deus te abençoe e edifique sua vida através desta comunidade! 🙏",
    "🕊️ {nome}, bem-vindo(a) à nossa família espiritual!\n\nAqui compartilhamos a Palavra de Deus, orações e testemunhos. Participe com amor! 🔥",
]

def carregar_palavras_custom():
    if os.path.exists(PALAVRAS_CUSTOM_FILE):
        try:
            with open(PALAVRAS_CUSTOM_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []

async def is_admin_chat(context, chat_id, user_id):
    if user_id == OWNER_ID:
        return True
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

async def handle_novo_membro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        for membro in update.message.new_chat_members:
            if membro.is_bot:
                continue
            nome = membro.first_name or "Membro"
            import random
            boas_vindas = random.choice(BOAS_VINDAS).format(nome=nome)
            teclado = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Li e aceito as regras!", callback_data=f"aceitar_regras:{membro.id}")]
            ])
            await update.message.reply_text(
                f"{boas_vindas}\n\n📋 Por favor, leia e aceite as regras do grupo clicando no botão abaixo!",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=teclado
            )
            logger.info(f"Novo membro: {nome} ({membro.id})")
    except Exception as e:
        logger.error(f"Erro ao dar boas-vindas: {e}")

async def handle_saida_membro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        membro = update.message.left_chat_member
        if membro and not membro.is_bot:
            nome = membro.first_name or "Membro"
            await update.message.reply_text(
                f"🕊️ *{nome}* saiu do grupo.\n\n_Que Deus o(a) abençoe e guarde onde quer que vá._",
                parse_mode=ParseMode.MARKDOWN
            )
    except Exception as e:
        logger.error(f"Erro ao processar saída: {e}")

async def handle_aceitar_regras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        partes = query.data.split(":")
        user_id_alvo = int(partes[1])
        if query.from_user.id != user_id_alvo:
            await query.answer("⚠️ Estas regras são para outro membro.", show_alert=True)
            return
        await query.answer()
        nome = query.from_user.first_name or "Membro"
        await query.edit_message_text(
            f"✅ *{nome}* aceitou as regras do grupo!\n\n"
            f"Seja muito bem-vindo(a) à família Avivamento AD! 🙏🔥\n\n"
            f"_\"Onde não há visão, o povo perece.\"_ — Provérbios 29:18",
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"{nome} ({user_id_alvo}) aceitou as regras.")
    except Exception as e:
        logger.error(f"Erro ao processar aceitação de regras: {e}")

async def handle_mensagem_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.text:
            return
        user = update.effective_user
        if not user or user.is_bot:
            return

        texto = update.message.text.lower()

        # Verificar palavrões padrão
        for padrao in PALAVROES_EXATOS:
            if re.search(padrao, texto, re.IGNORECASE):
                try:
                    await update.message.delete()
                except:
                    pass
                from avisos import registrar_aviso
                total = registrar_aviso(user.id)
                nome = user.first_name or "Membro"
                if total >= 3:
                    try:
                        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
                        await context.bot.send_message(
                            update.effective_chat.id,
                            f"🚫 *{nome}* foi removido(a) do grupo após 3 avisos por linguagem inadequada.\n_\"Não saia da vossa boca nenhuma palavra torpe.\"_ — Efésios 4:29",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except Exception as e:
                        logger.error(f"Erro ao banir: {e}")
                elif total == 2:
                    try:
                        from datetime import datetime, timedelta
                        from telegram import ChatPermissions
                        perms = ChatPermissions(can_send_messages=False)
                        until = datetime.now() + timedelta(hours=1)
                        await context.bot.restrict_chat_member(update.effective_chat.id, user.id, perms, until_date=until)
                        await context.bot.send_message(
                            update.effective_chat.id,
                            f"🔇 *{nome}* — 2º aviso. Silenciado por 1h.\n_Este é um grupo cristão. Respeite os irmãos._",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except Exception as e:
                        logger.error(f"Erro ao silenciar: {e}")
                else:
                    await context.bot.send_message(
                        update.effective_chat.id,
                        f"⚠️ *{nome}* — 1º aviso. Mensagem removida por linguagem inadequada.\n_\"Não saia da vossa boca nenhuma palavra torpe.\"_ — Efésios 4:29",
                        parse_mode=ParseMode.MARKDOWN
                    )
                return

        # Verificar palavras personalizadas bloqueadas
        palavras_custom = carregar_palavras_custom()
        for palavra in palavras_custom:
            if palavra.lower() in texto:
                try:
                    await update.message.delete()
                except:
                    pass
                await context.bot.send_message(
                    update.effective_chat.id,
                    f"⚠️ Mensagem removida por conter palavra bloqueada.",
                )
                return

        # Atualizar ranking por participação
        try:
            from ranking import adicionar_pontos
            nome = user.first_name or "Membro"
            adicionar_pontos(user.id, nome, "mensagem")
        except Exception as e:
            logger.debug(f"Erro ao atualizar ranking: {e}")

    except Exception as e:
        logger.error(f"Erro em handle_mensagem_grupo: {e}")

async def handle_midia_privado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        if not user:
            return

        # Só aceita mídia do dono ou admins do grupo
        eh_admin = False
        if user.id == OWNER_ID:
            eh_admin = True
        else:
            try:
                member = await context.bot.get_chat_member(int(GROUP_ID), user.id)
                if member.status in ["administrator", "creator"]:
                    eh_admin = True
            except:
                pass

        if not eh_admin:
            await update.message.reply_text(
                "⚠️ Apenas administradores podem enviar mídias para o canal.\n\n🙏 Use /testemunho para compartilhar seu testemunho!",
            )
            return

        from media_manager import salvar_midia
        caption = update.message.caption or ""

        if update.message.video:
            file_id = update.message.video.file_id
            salvar_midia(file_id, "video", caption)
            await update.message.reply_text(
                f"✅ *Vídeo salvo na fila do canal!*\n\n📅 Será postado automaticamente às 09h ou 19h.\n\n_Use /fila para ver a fila._",
                parse_mode=ParseMode.MARKDOWN
            )
        elif update.message.photo:
            file_id = update.message.photo[-1].file_id
            salvar_midia(file_id, "imagem", caption)
            await update.message.reply_text(
                f"✅ *Imagem salva na fila do canal!*\n\n📅 Será postada automaticamente às 09h ou 19h.\n\n_Use /fila para ver a fila._",
                parse_mode=ParseMode.MARKDOWN
            )
        elif update.message.document:
            file_id = update.message.document.file_id
            salvar_midia(file_id, "documento", caption)
            await update.message.reply_text("✅ Documento salvo na fila.")
        else:
            await update.message.reply_text("⚠️ Tipo de mídia não suportado. Envie vídeo ou foto.")

        logger.info(f"Mídia recebida de {user.first_name} ({user.id})")
    except Exception as e:
        logger.error(f"Erro em handle_midia_privado: {e}")

async def handle_texto_privado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        if not user or user.is_bot:
            return
        texto = update.message.text
        if not texto or len(texto) < 20:
            await update.message.reply_text(
                "🙏 *Olá!*\n\nSe quiser enviar um testemunho, use:\n`/testemunho [seu testemunho]`\n\nOu escreva aqui um texto com pelo menos 20 caracteres que será registrado como testemunho.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        from testemunhos import salvar_testemunho
        nome = user.first_name or "Membro"
        salvar_testemunho(nome, user.id, texto)
        try:
            from ranking import adicionar_pontos
            adicionar_pontos(user.id, nome, "testemunho")
        except:
            pass
        await update.message.reply_text(
            f"🌟 *Testemunho recebido, {nome}!*\n\nSeu testemunho foi registrado e será publicado no canal em breve! 🙏\n\n_\"E venceram-no pelo sangue do Cordeiro e pela palavra do seu testemunho.\"_ — Apocalipse 12:11",
            parse_mode=ParseMode.MARKDOWN
        )
        if OWNER_ID:
            try:
                await context.bot.send_message(
                    OWNER_ID,
                    f"🌟 *Novo testemunho (privado)!*\nDe: *{nome}* (`{user.id}`)\n\n_{texto[:300]}_",
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                pass
        logger.info(f"Testemunho recebido de {nome} ({user.id}) via privado.")
    except Exception as e:
        logger.error(f"Erro em handle_texto_privado: {e}")
