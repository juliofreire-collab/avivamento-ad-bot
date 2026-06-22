from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import logging
from config import OWNER_ID, CHANNEL_ID, GROUP_ID
from media_manager import carregar_media, total_videos, total_imagens, limpar_videos, limpar_imagens
from oracao import salvar_pedido, carregar_pedidos, get_pedidos_pendentes, ORACOES_DO_DIA
from avisos import resetar_avisos
import random

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

# ─── GERAIS ───────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙏 *Olá! Sou o Bot do Avivamento AD!*\n\n"
        "Estou aqui para edificar o grupo e o canal com a Palavra de Deus.\n\n"
        "📋 Use /ajuda para ver todos os comandos disponíveis.\n"
        "🙏 Use /oracao para fazer ou ver pedidos de oração.",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin = await is_admin(update, context)
    texto = "📋 *COMANDOS — AVIVAMENTO AD*\n\n"
    texto += "*Para todos:*\n"
    texto += "/versiculo — Receber um versículo com imagem\n"
    texto += "/oracao — Ver e enviar pedidos de oração\n"
    texto += "/regras — Ver as regras do grupo\n"
    texto += "/devocional — Receber um devocional\n\n"

    if admin:
        texto += "*🔧 Administração — Canal:*\n"
        texto += "/postar\\_versiculo — Postar versículo no canal agora\n"
        texto += "/postar\\_midia — Postar mídia no canal agora\n"
        texto += "/postar\\_devocional — Postar devocional no canal agora\n\n"
        texto += "*🔧 Administração — Grupo:*\n"
        texto += "/postar\\_regras — Postar regras no grupo agora\n"
        texto += "/postar\\_oracao — Postar oração no grupo agora\n"
        texto += "/postar\\_engajamento — Postar pergunta de engajamento\n"
        texto += "/banir — Banir usuário (responda à mensagem)\n"
        texto += "/silenciar — Silenciar usuário (responda à mensagem)\n"
        texto += "/liberar — Liberar usuário silenciado\n"
        texto += "/resetar\\_avisos — Zerar avisos de um usuário\n"
        texto += "/anuncio [texto] — Fazer anúncio\n"
        texto += "/fixar — Fixar mensagem\n\n"
        texto += "*📊 Estatísticas:*\n"
        texto += "/status — Ver estatísticas completas\n"
        texto += "/listar\\_midia — Ver mídias salvas\n"
        texto += "/limpar\\_videos — Limpar vídeos\n"
        texto += "/limpar\\_imagens — Limpar imagens\n"
        texto += "/ver\\_pedidos — Ver pedidos de oração pendentes\n"

    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_versiculo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bible import gerar_imagem_versiculo
    buf, referencia, texto = gerar_imagem_versiculo()
    caption = f'📖 *{referencia}*\n\n_"{texto}"_\n\n🕊️ Avivamento AD'
    await update.message.reply_photo(photo=buf, caption=caption, parse_mode=ParseMode.MARKDOWN)

async def cmd_regras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from regras import REGRAS_GRUPO
    await update.message.reply_text(REGRAS_GRUPO, parse_mode=ParseMode.MARKDOWN)

async def cmd_devocional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from oracao import DEVOCIONAIS
    devocional = random.choice(DEVOCIONAIS)
    await update.message.reply_text(
        f'✨ *{devocional["titulo"]}*\n\n{devocional["texto"]}',
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_oracao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        pedido = " ".join(context.args)
        nome = update.effective_user.first_name or "Membro"
        user_id = update.effective_user.id
        salvar_pedido(nome, user_id, pedido)

        await update.message.reply_text(
            f"🙏 *Pedido de oração registrado!*\n\n"
            f"_{pedido}_\n\n"
            f"Os irmãos vão interceder por você!\n"
            f"_\"Confessai as vossas ofensas uns aos outros e orai uns pelos outros.\"_ — Tiago 5:16",
            parse_mode=ParseMode.MARKDOWN
        )

        # Notificar o grupo se o comando for no privado
        if update.effective_chat.type == "private":
            try:
                await context.bot.send_message(
                    GROUP_ID,
                    f"🙏 *PEDIDO DE ORAÇÃO*\n\n"
                    f"*{nome}* pede a intercessão dos irmãos:\n\n"
                    f"_{pedido}_\n\n"
                    f"Vamos orar juntos! Use /oracao para ver todos os pedidos.",
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                pass
    else:
        pedidos = get_pedidos_pendentes()
        if not pedidos:
            await update.message.reply_text(
                "🙏 *Nenhum pedido de oração pendente no momento.*\n\n"
                "Para fazer um pedido use:\n/oracao [seu pedido]\n\n"
                "_Exemplo: /oracao Ore pela cura da minha mãe_",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        texto = "🙏 *PEDIDOS DE ORAÇÃO ATIVOS*\n\n"
        for i, p in enumerate(pedidos[-10:], 1):
            texto += f"*{i}. {p['nome']}* ({p['data']}):\n_{p['pedido']}_\n\n"
        texto += "_\"Orai uns pelos outros para serdes curados.\"_ — Tiago 5:16"
        await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

# ─── ADMIN — CANAL ────────────────────────────────────────────────────────────

async def cmd_postar_versiculo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    from agendador import postar_versiculo_canal
    class Ctx:
        bot = context.bot
    await postar_versiculo_canal(Ctx())
    await update.message.reply_text("✅ Versículo postado no canal!")

async def cmd_postar_midia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    from agendador import postar_midia_no_canal
    class Ctx:
        bot = context.bot
    resultado = await postar_midia_no_canal(Ctx())
    if resultado:
        await update.message.reply_text("✅ Mídia postada no canal!")
    else:
        await update.message.reply_text("⚠️ Nenhuma mídia salva. Envie vídeos ou imagens no privado do bot.")

async def cmd_postar_devocional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    from agendador import postar_devocional_canal
    class Ctx:
        bot = context.bot
    await postar_devocional_canal(Ctx())
    await update.message.reply_text("✅ Devocional postado no canal!")

# ─── ADMIN — GRUPO ────────────────────────────────────────────────────────────

async def cmd_postar_regras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    from regras import REGRAS_GRUPO
    await context.bot.send_message(GROUP_ID, REGRAS_GRUPO, parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text("✅ Regras postadas no grupo!")

async def cmd_postar_oracao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    from agendador import postar_oracao_grupo
    class Ctx:
        bot = context.bot
    await postar_oracao_grupo(Ctx())
    await update.message.reply_text("✅ Oração postada no grupo!")

async def cmd_postar_engajamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    from agendador import postar_engajamento_grupo
    class Ctx:
        bot = context.bot
    await postar_engajamento_grupo(Ctx())
    await update.message.reply_text("✅ Pergunta de engajamento postada!")

async def cmd_banir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Responda à mensagem do usuário que deseja banir.")
        return
    alvo = update.message.reply_to_message.from_user
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, alvo.id)
        await update.message.reply_text(
            f"🚫 *{alvo.first_name}* foi removido(a) do grupo.\n"
            f"_Que Deus o(a) alcance com Seu amor._",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao banir: {e}")

async def cmd_silenciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Responda à mensagem do usuário.")
        return
    alvo = update.message.reply_to_message.from_user
    try:
        perms = ChatPermissions(can_send_messages=False, can_send_media_messages=False,
                                can_send_polls=False, can_send_other_messages=False)
        await context.bot.restrict_chat_member(update.effective_chat.id, alvo.id, perms)
        await update.message.reply_text(f"🔇 *{alvo.first_name}* foi silenciado(a).", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")

async def cmd_liberar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Responda à mensagem do usuário.")
        return
    alvo = update.message.reply_to_message.from_user
    try:
        perms = ChatPermissions(can_send_messages=True, can_send_media_messages=True,
                                can_send_polls=True, can_send_other_messages=True)
        await context.bot.restrict_chat_member(update.effective_chat.id, alvo.id, perms)
        resetar_avisos(alvo.id)
        await update.message.reply_text(f"✅ *{alvo.first_name}* foi liberado(a).", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")

async def cmd_resetar_avisos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Responda à mensagem do usuário.")
        return
    alvo = update.message.reply_to_message.from_user
    resetar_avisos(alvo.id)
    await update.message.reply_text(f"✅ Avisos de *{alvo.first_name}* foram zerados.", parse_mode=ParseMode.MARKDOWN)

async def cmd_anuncio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    if not context.args:
        await update.message.reply_text("⚠️ Use: /anuncio [texto]")
        return
    texto = " ".join(context.args)
    msg = f"📢 *ANÚNCIO OFICIAL*\n\n{texto}\n\n🕊️ _Administração — Avivamento AD_"
    await context.bot.send_message(update.effective_chat.id, msg, parse_mode=ParseMode.MARKDOWN)

async def cmd_fixar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Responda à mensagem que deseja fixar.")
        return
    try:
        await context.bot.pin_chat_message(update.effective_chat.id, update.message.reply_to_message.message_id)
        await update.message.reply_text("📌 Mensagem fixada!")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    pedidos = len(get_pedidos_pendentes())
    texto = (
        "📊 *STATUS — AVIVAMENTO AD*\n\n"
        f"🎥 Vídeos salvos: *{total_videos()}*\n"
        f"🖼️ Imagens salvas: *{total_imagens()}*\n"
        f"🙏 Pedidos de oração: *{pedidos}*\n\n"
        "⏰ *Posts automáticos:*\n"
        "  📺 *CANAL:*\n"
        "  • Devocional: 06h e 18h\n"
        "  • Versículo: 07h, 12h e 21h\n"
        "  • Sua mídia: 09h e 19h\n\n"
        "  👥 *GRUPO:*\n"
        "  • Oração da manhã: 06h05\n"
        "  • Versículo: 07h10, 13h, 21h10\n"
        "  • Devocional: 08h e 20h\n"
        "  • Engajamento: 10h e 15h\n"
        "  • Oração da noite: 22h\n"
        "  • Regras: a cada 4h\n\n"
        "✅ Bot funcionando 24/7 na nuvem!\n"
        "🕊️ _Que Deus abençoe este ministério!_"
    )
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_listar_midia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    await update.message.reply_text(
        f"📦 *Mídias armazenadas:*\n\n🎥 Vídeos: *{total_videos()}*\n🖼️ Imagens: *{total_imagens()}*\n\n"
        f"_Envie vídeos/imagens no privado do bot para adicionar._",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_limpar_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    limpar_videos()
    await update.message.reply_text("✅ Vídeos removidos.")

async def cmd_limpar_imagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    limpar_imagens()
    await update.message.reply_text("✅ Imagens removidas.")

async def cmd_enquete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores podem enviar enquetes.")
        return
    from agendador import postar_enquete_grupo
    class Ctx:
        bot = context.bot
    await postar_enquete_grupo(Ctx())
    if update.effective_chat.id != int(GROUP_ID):
        await update.message.reply_text("✅ Enquete enviada ao grupo!")

async def cmd_chatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    await update.message.reply_text(
        f"📋 *Informações do Chat*\n\n"
        f"🆔 Chat ID: `{chat.id}`\n"
        f"📝 Nome: {chat.title or chat.first_name}\n"
        f"🔹 Tipo: {chat.type}\n"
        f"👤 Seu ID: `{user.id}`",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_ver_pedidos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Apenas administradores.")
        return
    pedidos = get_pedidos_pendentes()
    if not pedidos:
        await update.message.reply_text("🙏 Nenhum pedido de oração pendente.")
        return
    texto = f"🙏 *{len(pedidos)} PEDIDOS DE ORAÇÃO PENDENTES*\n\n"
    for i, p in enumerate(pedidos, 1):
        texto += f"*{i}. {p['nome']}* — {p['data']}\n_{p['pedido']}_\n\n"
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)
