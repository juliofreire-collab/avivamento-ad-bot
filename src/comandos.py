from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import logging
import json
import os
import random
from config import OWNER_ID, CHANNEL_ID, GROUP_ID
from media_manager import total_videos, total_imagens, limpar_videos, limpar_imagens
from oracao import salvar_pedido, get_pedidos_pendentes
from avisos import resetar_avisos, get_avisos

logger = logging.getLogger(__name__)

PALAVRAS_CUSTOM_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "palavras_custom.json")

def carregar_palavras_custom():
    if os.path.exists(PALAVRAS_CUSTOM_FILE):
        try:
            with open(PALAVRAS_CUSTOM_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []

def salvar_palavras_custom(palavras):
    with open(PALAVRAS_CUSTOM_FILE, "w", encoding="utf-8") as f:
        json.dump(palavras, f, ensure_ascii=False, indent=2)

# ─── ADMIN CHECK (corrigido: sempre verifica o GRUPO, não o chat atual) ───────

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    if user_id == OWNER_ID:
        return True
    # Sempre verifica admin no GRUPO, funciona mesmo de chat privado
    try:
        member = await context.bot.get_chat_member(int(GROUP_ID), user_id)
        if member.status in ["administrator", "creator"]:
            return True
    except:
        pass
    # Se estiver em um grupo/supergrupo, verifica o chat atual também
    if update.effective_chat and update.effective_chat.type in ["group", "supergroup"]:
        try:
            member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
            if member.status in ["administrator", "creator"]:
                return True
        except:
            pass
    return False

async def deletar_comando(update: Update):
    """Apaga mensagem de comando no grupo para manter o chat limpo"""
    if update.effective_chat and update.effective_chat.type in ["group", "supergroup"]:
        try:
            await update.message.delete()
        except:
            pass

# ─── GERAIS ───────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin = await is_admin(update, context)
    texto = (
        "🙏 *Olá! Sou o Bot do Avivamento AD!*\n\n"
        "Estou aqui para edificar o grupo e o canal com a Palavra de Deus.\n\n"
        "📋 Use /ajuda para ver todos os comandos disponíveis.\n"
        "🙏 Use /oracao para fazer ou ver pedidos de oração.\n"
        "🌟 Use /testemunho para compartilhar um testemunho."
    )
    if admin:
        texto += "\n\n🔧 *Você é administrador!* Use /ajuda para ver todos os seus comandos."
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    await update.message.reply_text(
        "✅ *Bot online e funcionando!*\n\n"
        "🤖 Status: Ativo 24/7\n"
        "⚡ Resposta: Normal\n"
        "🕊️ _Avivamento AD_",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin = await is_admin(update, context)
    texto = "📋 *COMANDOS — AVIVAMENTO AD*\n\n"
    texto += "*Para todos os membros:*\n"
    texto += "/versiculo — Receber um versículo com imagem\n"
    texto += "/oracao — Ver e enviar pedidos de oração\n"
    texto += "/regras — Ver as regras do grupo\n"
    texto += "/devocional — Receber um devocional\n"
    texto += "/testemunho — Enviar um testemunho\n"
    texto += "/ping — Verificar se o bot está online\n\n"

    if admin:
        texto += "🔧 *Administração — Canal:*\n"
        texto += "/postar — Postar versículo no canal agora\n"
        texto += "/postar\\_versiculo — Postar versículo no canal\n"
        texto += "/postar\\_midia — Postar mídia no canal agora\n"
        texto += "/postar\\_devocional — Postar devocional no canal\n"
        texto += "/fila — Ver mídias na fila do canal\n"
        texto += "/horarios — Ver horários de postagem\n"
        texto += "/proxima — Prévia da próxima mensagem agendada\n\n"

        texto += "🔧 *Administração — Grupo:*\n"
        texto += "/postar\\_regras — Postar regras no grupo\n"
        texto += "/postar\\_oracao — Postar oração no grupo\n"
        texto += "/postar\\_engajamento — Postar pergunta de engajamento\n"
        texto += "/enquete — Enviar enquete semanal\n"
        texto += "/anuncio [texto] — Fazer anúncio oficial\n"
        texto += "/fixar — Fixar mensagem (responda à msg)\n\n"

        texto += "🔨 *Moderação:*\n"
        texto += "/banir — Banir membro (responda à mensagem)\n"
        texto += "/kick — Expulsar sem banir (responda à mensagem)\n"
        texto += "/silenciar — Mutar membro (responda à mensagem)\n"
        texto += "/liberar — Liberar membro silenciado\n"
        texto += "/avisar — Advertir membro (responda à mensagem)\n"
        texto += "/perdoar — Zerar avisos (responda à mensagem)\n"
        texto += "/advertencias — Ver avisos de um membro\n"
        texto += "/info — Informações de um membro\n\n"

        texto += "🚫 *Palavras Bloqueadas:*\n"
        texto += "/bloquear [palavra] — Adicionar palavra à lista\n"
        texto += "/desbloquear [palavra] — Remover da lista\n"
        texto += "/listanegra — Ver palavras bloqueadas\n\n"

        texto += "🌟 *Testemunhos:*\n"
        texto += "/ver\\_testemunhos — Ver testemunhos pendentes\n"
        texto += "/postar\\_testemunho — Publicar testemunho no canal\n\n"

        texto += "📊 *Estatísticas:*\n"
        texto += "/status — Estatísticas completas\n"
        texto += "/listar\\_midia — Ver mídias salvas\n"
        texto += "/ver\\_pedidos — Ver pedidos de oração\n"
        texto += "/testar — Diagnóstico do bot\n"
        texto += "/chatid — Ver ID do chat/usuário\n"

    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_horarios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    texto = (
        "⏰ *HORÁRIOS DE POSTAGEM — AVIVAMENTO AD*\n\n"
        "📺 *CANAL (@avivamentoad):*\n"
        "• 06h00 — Devocional\n"
        "• 07h00 — Versículo com imagem\n"
        "• 09h00 — Sua mídia (vídeo/foto)\n"
        "• 12h00 — Versículo com imagem\n"
        "• 17h00 _(sexta)_ — Testemunho da semana\n"
        "• 18h00 — Devocional\n"
        "• 19h00 — Sua mídia (vídeo/foto)\n"
        "• 21h00 — Versículo com imagem\n\n"
        "👥 *GRUPO:*\n"
        "• 06h05 — Oração da manhã\n"
        "• 07h10 — Versículo bíblico\n"
        "• 08h00 — Devocional\n"
        "• 10h00 — Pergunta de engajamento\n"
        "• 10h30 _(seg)_ — Enquete semanal\n"
        "• 13h00 — Versículo bíblico\n"
        "• 15h00 — Pergunta de engajamento\n"
        "• 19h00 _(qui)_ — Enquete extra\n"
        "• 20h00 — Devocional\n"
        "• 21h10 — Versículo bíblico\n"
        "• 22h00 — Oração da noite\n"
        "• A cada 4h — Regras do grupo\n\n"
        "🕊️ _Todos os horários no fuso de Brasília_"
    )
    await context.bot.send_message(update.effective_user.id, texto, parse_mode=ParseMode.MARKDOWN) if update.effective_chat.type in ["group", "supergroup"] else await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_versiculo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        from bible import gerar_imagem_versiculo
        buf, referencia, texto = gerar_imagem_versiculo()
        caption = f'📖 *{referencia}*\n\n_"{texto}"_\n\n🕊️ Avivamento AD'
        await update.message.reply_photo(photo=buf, caption=caption, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Erro ao gerar imagem versículo: {e}")
        from bible import get_versiculo_texto
        referencia, texto = get_versiculo_texto()
        await update.message.reply_text(
            f'📖 *{referencia}*\n\n_"{texto}"_\n\n🕊️ Avivamento AD',
            parse_mode=ParseMode.MARKDOWN
        )

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

async def cmd_aniversario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from aniversarios import registrar_aniversario, get_aniversario, total_cadastrados
    user = update.effective_user
    user_id = user.id
    nome = user.first_name or "Membro"

    if not context.args:
        aniv = get_aniversario(user_id)
        if aniv:
            await update.message.reply_text(
                f"🎂 *Seu aniversário cadastrado:* {aniv['dia']:02d}/{aniv['mes']:02d}\n\n"
                f"Para alterar: /aniversario DD/MM\n"
                f"_Ex: /aniversario 25/12_",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "🎂 *Cadastre seu aniversário!*\n\n"
                "Use: /aniversario DD/MM\n"
                "_Ex: /aniversario 25/12_\n\n"
                "O bot enviará uma mensagem especial no grupo e no seu privado no dia! 🎉",
                parse_mode=ParseMode.MARKDOWN
            )
        return

    entrada = context.args[0].strip()
    try:
        partes = entrada.split("/")
        dia = int(partes[0])
        mes = int(partes[1])
        if not (1 <= dia <= 31 and 1 <= mes <= 12):
            raise ValueError
    except:
        await update.message.reply_text(
            "❌ Formato inválido. Use: /aniversario DD/MM\n_Ex: /aniversario 25/12_",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    registrar_aniversario(user_id, nome, dia, mes)
    total = total_cadastrados()
    await update.message.reply_text(
        f"🎂 *Aniversário cadastrado!*\n\n"
        f"📅 Data: *{dia:02d}/{mes:02d}*\n"
        f"👤 Nome: *{nome}*\n\n"
        f"No seu aniversário o bot vai:\n"
        f"• 🎉 Celebrar com você no grupo\n"
        f"• 💌 Enviar mensagem especial no seu privado\n\n"
        f"_Já são {total} membros cadastrados!_ 🙏",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from ranking import get_top_ranking, get_pontos_usuario
    top = get_top_ranking(10)
    meu_id = str(update.effective_user.id)
    meus_pontos = get_pontos_usuario(update.effective_user.id)
    medalhas = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    if not top or all(p == 0 for _, _, p in top):
        await update.message.reply_text(
            "🏆 *RANKING DE ENGAJAMENTO*\n\n"
            "Ainda não há pontuação registrada.\n\n"
            "🌟 *Como ganhar pontos:*\n"
            "• Enviar testemunho: +10 pts\n"
            "• Pedido de oração: +5 pts\n"
            "• Participar de perguntas: +3 pts\n"
            "• Mensagens no grupo: +1 pt/dia\n\n"
            "_Comece participando agora!_ 🙏",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    texto = "🏆 *RANKING DE ENGAJAMENTO*\n\n"
    for i, (uid, nome, pontos) in enumerate(top):
        medalha = medalhas[i] if i < len(medalhas) else f"{i+1}."
        destaque = " ◀️ você" if uid == meu_id else ""
        texto += f"{medalha} *{nome}* — {pontos} pts{destaque}\n"

    texto += (
        f"\n📊 Seus pontos: *{meus_pontos} pts*\n\n"
        "🌟 *Como ganhar pontos:*\n"
        "• /testemunho → +10 pts\n"
        "• /oracao → +5 pts\n"
        "• Participar de perguntas → +3 pts\n"
        "• Mensagens no grupo → +1 pt/dia\n\n"
        "_\"Portanto, encorajai-vos uns aos outros.\"_ — 1 Tessalonicenses 5:11"
    )
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_postar_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from agendador import postar_ranking_grupo
    class Ctx:
        bot = context.bot
    await postar_ranking_grupo(Ctx())
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(destino, "✅ Ranking postado no grupo!")

async def cmd_oracao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        pedido = " ".join(context.args)
        nome = update.effective_user.first_name or "Membro"
        user_id = update.effective_user.id
        salvar_pedido(nome, user_id, pedido)
        try:
            from ranking import adicionar_pontos
            adicionar_pontos(user_id, nome, "oracao")
        except:
            pass
        await update.message.reply_text(
            f"🙏 *Pedido de oração registrado!*\n\n"
            f"_{pedido}_\n\n"
            f"Os irmãos vão interceder por você!\n"
            f"_\"Confessai as vossas ofensas uns aos outros e orai uns pelos outros.\"_ — Tiago 5:16",
            parse_mode=ParseMode.MARKDOWN
        )
        if update.effective_chat.type == "private":
            try:
                await context.bot.send_message(
                    GROUP_ID,
                    f"🙏 *PEDIDO DE ORAÇÃO*\n\n*{nome}* pede a intercessão dos irmãos:\n\n_{pedido}_\n\nVamos orar juntos! Use /oracao para ver todos os pedidos.",
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                pass
    else:
        pedidos = get_pedidos_pendentes()
        if not pedidos:
            await update.message.reply_text(
                "🙏 *Nenhum pedido de oração pendente no momento.*\n\nPara fazer um pedido use:\n`/oracao [seu pedido]`\n\n_Exemplo: /oracao Ore pela cura da minha mãe_",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        texto = "🙏 *PEDIDOS DE ORAÇÃO ATIVOS*\n\n"
        for i, p in enumerate(pedidos[-10:], 1):
            texto += f"*{i}. {p['nome']}* ({p['data']}):\n_{p['pedido']}_\n\n"
        texto += "_\"Orai uns pelos outros para serdes curados.\"_ — Tiago 5:16"
        await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_proxima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from bible import get_versiculo_texto
    from oracao import DEVOCIONAIS
    import datetime, pytz
    tz = pytz.timezone("America/Sao_Paulo")
    agora = datetime.datetime.now(tz)
    hora = agora.hour
    ref, texto = get_versiculo_texto()
    dev = random.choice(DEVOCIONAIS)
    resposta = (
        f"📅 *PRÉVIA — PRÓXIMAS POSTAGENS*\n\n"
        f"🕐 Agora são *{agora.strftime('%H:%M')}*\n\n"
        f"📖 *Próximo versículo:*\n_{ref}_ — \"{texto[:80]}...\"\n\n"
        f"✨ *Próximo devocional:*\n_{dev['titulo']}_\n\n"
        f"🕊️ _Avivamento AD_"
    )
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(destino, resposta, parse_mode=ParseMode.MARKDOWN)

async def cmd_testar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    resultados = []
    # Testa geração de imagem
    try:
        from bible import gerar_imagem_versiculo
        buf, ref, txt = gerar_imagem_versiculo()
        resultados.append("✅ Geração de imagem — OK")
    except Exception as e:
        resultados.append(f"❌ Geração de imagem — ERRO: {str(e)[:50]}")
    # Testa acesso ao canal
    try:
        chat = await context.bot.get_chat(CHANNEL_ID)
        resultados.append(f"✅ Canal — OK ({chat.title})")
    except Exception as e:
        resultados.append(f"❌ Canal — ERRO: {str(e)[:50]}")
    # Testa acesso ao grupo
    try:
        chat = await context.bot.get_chat(int(GROUP_ID))
        resultados.append(f"✅ Grupo — OK ({chat.title})")
    except Exception as e:
        resultados.append(f"❌ Grupo — ERRO: {str(e)[:50]}")
    # Testa mídias
    try:
        v = total_videos()
        i = total_imagens()
        resultados.append(f"✅ Mídias — {v} vídeos, {i} imagens")
    except Exception as e:
        resultados.append(f"❌ Mídias — ERRO: {str(e)[:50]}")
    # Testa pedidos de oração
    try:
        p = len(get_pedidos_pendentes())
        resultados.append(f"✅ Orações — {p} pedidos")
    except Exception as e:
        resultados.append(f"❌ Orações — ERRO: {str(e)[:50]}")

    texto = "🔧 *DIAGNÓSTICO DO BOT*\n\n" + "\n".join(resultados) + "\n\n🕊️ _Avivamento AD_"
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(destino, texto, parse_mode=ParseMode.MARKDOWN)

# ─── ADMIN — CANAL ────────────────────────────────────────────────────────────

async def cmd_postar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from agendador import postar_versiculo_canal
    class Ctx:
        bot = context.bot
    await postar_versiculo_canal(Ctx())
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(destino, "✅ Versículo postado no canal!")

async def cmd_postar_versiculo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from agendador import postar_versiculo_canal
    class Ctx:
        bot = context.bot
    await postar_versiculo_canal(Ctx())
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(destino, "✅ Versículo postado no canal!")

async def cmd_postar_midia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from agendador import postar_midia_no_canal
    class Ctx:
        bot = context.bot
    resultado = await postar_midia_no_canal(Ctx())
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    if resultado:
        await context.bot.send_message(destino, "✅ Mídia postada no canal!")
    else:
        await context.bot.send_message(destino, "⚠️ Nenhuma mídia salva. Envie vídeos ou imagens no privado do bot.")

async def cmd_postar_devocional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from agendador import postar_devocional_canal
    class Ctx:
        bot = context.bot
    await postar_devocional_canal(Ctx())
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(destino, "✅ Devocional postado no canal!")

async def cmd_fila(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    v = total_videos()
    i = total_imagens()
    texto = (
        f"📦 *FILA DE MÍDIAS — CANAL*\n\n"
        f"🎥 Vídeos na fila: *{v}*\n"
        f"🖼️ Imagens na fila: *{i}*\n\n"
        f"📅 Postagem automática: *09h e 19h*\n\n"
        f"_Envie vídeos/fotos no privado do bot para adicionar à fila._\n"
        f"_Admins do grupo também podem enviar!_"
    )
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(destino, texto, parse_mode=ParseMode.MARKDOWN)

# ─── ADMIN — GRUPO ────────────────────────────────────────────────────────────

async def cmd_postar_regras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from regras import REGRAS_GRUPO
    await context.bot.send_message(GROUP_ID, REGRAS_GRUPO, parse_mode=ParseMode.MARKDOWN)

async def cmd_postar_oracao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from agendador import postar_oracao_grupo
    class Ctx:
        bot = context.bot
    await postar_oracao_grupo(Ctx())

async def cmd_postar_engajamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from agendador import postar_engajamento_grupo
    class Ctx:
        bot = context.bot
    await postar_engajamento_grupo(Ctx())

async def cmd_anuncio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not context.args:
        destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
        await context.bot.send_message(destino, "⚠️ Use: /anuncio [texto do anúncio]")
        return
    texto = " ".join(context.args)
    msg = f"📢 *ANÚNCIO OFICIAL*\n\n{texto}\n\n🕊️ _Administração — Avivamento AD_"
    await context.bot.send_message(GROUP_ID, msg, parse_mode=ParseMode.MARKDOWN)

async def cmd_fixar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
        await context.bot.send_message(destino, "⚠️ Responda à mensagem que deseja fixar.")
        return
    try:
        await context.bot.pin_chat_message(update.effective_chat.id, update.message.reply_to_message.message_id)
    except Exception as e:
        logger.error(f"Erro ao fixar: {e}")

# ─── MODERAÇÃO ─────────────────────────────────────────────────────────────────

async def cmd_banir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return
    alvo = update.message.reply_to_message.from_user
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, alvo.id)
        await context.bot.send_message(
            update.effective_chat.id,
            f"🚫 *{alvo.first_name}* foi removido(a) do grupo.\n_Que Deus o(a) alcance com Seu amor._",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Erro ao banir: {e}")

async def cmd_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Expulsa sem banir — pode voltar com convite"""
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return
    alvo = update.message.reply_to_message.from_user
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, alvo.id)
        await context.bot.unban_chat_member(update.effective_chat.id, alvo.id)
        await context.bot.send_message(
            update.effective_chat.id,
            f"👢 *{alvo.first_name}* foi expulso(a) do grupo.\n_Poderá voltar com um convite. Que Deus o(a) guie._",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Erro ao expulsar: {e}")

async def cmd_silenciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return
    alvo = update.message.reply_to_message.from_user
    # Verifica se tem tempo especificado (ex: /silenciar 30m)
    from datetime import datetime, timedelta
    until = None
    if context.args:
        arg = context.args[0].lower()
        try:
            if arg.endswith("m"):
                until = datetime.now() + timedelta(minutes=int(arg[:-1]))
            elif arg.endswith("h"):
                until = datetime.now() + timedelta(hours=int(arg[:-1]))
            elif arg.endswith("d"):
                until = datetime.now() + timedelta(days=int(arg[:-1]))
        except:
            pass
    try:
        perms = ChatPermissions(can_send_messages=False, can_send_media_messages=False,
                                can_send_polls=False, can_send_other_messages=False)
        kwargs = {"until_date": until} if until else {}
        await context.bot.restrict_chat_member(update.effective_chat.id, alvo.id, perms, **kwargs)
        duracao = f" por {context.args[0]}" if context.args and until else " indefinidamente"
        await context.bot.send_message(
            update.effective_chat.id,
            f"🔇 *{alvo.first_name}* foi silenciado(a){duracao}.\n_\"A língua que fala a verdade estabelece a justiça.\"_ — Provérbios 12:17",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Erro ao silenciar: {e}")

async def cmd_liberar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return
    alvo = update.message.reply_to_message.from_user
    try:
        perms = ChatPermissions(
            can_send_messages=True, can_send_media_messages=True,
            can_send_polls=True, can_send_other_messages=True,
            can_add_web_page_previews=True, can_invite_users=True
        )
        await context.bot.restrict_chat_member(update.effective_chat.id, alvo.id, perms)
        resetar_avisos(alvo.id)
        await context.bot.send_message(
            update.effective_chat.id,
            f"✅ *{alvo.first_name}* foi liberado(a) e pode participar normalmente. 🙏",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Erro ao liberar: {e}")

async def cmd_avisar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Advertência manual para um membro"""
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return
    alvo = update.message.reply_to_message.from_user
    from avisos import registrar_aviso
    total = registrar_aviso(alvo.id)
    motivo = " ".join(context.args) if context.args else "Comportamento inadequado"
    await context.bot.send_message(
        update.effective_chat.id,
        f"⚠️ *Aviso para {alvo.first_name}*\n\n"
        f"Motivo: _{motivo}_\n\n"
        f"Este é o seu *{total}º aviso*.\n"
        f"{'🚫 No próximo aviso você será removido do grupo.' if total >= 2 else ''}\n\n"
        f"_\"Não saia da vossa boca nenhuma palavra torpe.\"_ — Efésios 4:29",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_perdoar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Zera avisos de um membro"""
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return
    alvo = update.message.reply_to_message.from_user
    resetar_avisos(alvo.id)
    await context.bot.send_message(
        update.effective_chat.id,
        f"✅ Os avisos de *{alvo.first_name}* foram zerados.\n\n"
        f"_\"Sede uns para com os outros benignos, misericordiosos, perdoando-vos uns aos outros.\"_ — Efésios 4:32",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_resetar_avisos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_perdoar(update, context)

async def cmd_advertencias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver advertências de um membro"""
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
        await context.bot.send_message(destino, "⚠️ Responda à mensagem do membro.")
        return
    alvo = update.message.reply_to_message.from_user
    total = get_avisos(alvo.id)
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(
        destino,
        f"📋 *Advertências de {alvo.first_name}*\n\n"
        f"Total de avisos: *{total}/3*\n\n"
        f"{'🟢 Sem advertências' if total == 0 else '🟡 1 aviso' if total == 1 else '🟠 2 avisos — próximo é banido' if total == 2 else '🔴 Banido na próxima'}",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Informações de um membro"""
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not update.message.reply_to_message:
        return
    alvo = update.message.reply_to_message.from_user
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, alvo.id)
        status_map = {"member": "Membro", "administrator": "Admin", "creator": "Criador", "restricted": "Restrito", "left": "Saiu", "kicked": "Banido"}
        status = status_map.get(member.status, member.status)
        total_avisos = get_avisos(alvo.id)
        texto = (
            f"👤 *INFORMAÇÕES DO MEMBRO*\n\n"
            f"Nome: *{alvo.first_name} {alvo.last_name or ''}*\n"
            f"Username: @{alvo.username or 'sem username'}\n"
            f"ID: `{alvo.id}`\n"
            f"Status: *{status}*\n"
            f"⚠️ Avisos: *{total_avisos}/3*\n"
            f"🤖 Bot: {'Sim' if alvo.is_bot else 'Não'}"
        )
        destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
        await context.bot.send_message(destino, texto, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Erro ao buscar info: {e}")

# ─── PALAVRAS BLOQUEADAS ───────────────────────────────────────────────────────

async def cmd_bloquear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not context.args:
        destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
        await context.bot.send_message(destino, "⚠️ Use: /bloquear [palavra]")
        return
    palavra = " ".join(context.args).lower().strip()
    palavras = carregar_palavras_custom()
    if palavra not in palavras:
        palavras.append(palavra)
        salvar_palavras_custom(palavras)
        destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
        await context.bot.send_message(destino, f"🚫 Palavra *\"{palavra}\"* adicionada à lista negra.", parse_mode=ParseMode.MARKDOWN)
    else:
        destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
        await context.bot.send_message(destino, f"⚠️ A palavra *\"{palavra}\"* já está bloqueada.", parse_mode=ParseMode.MARKDOWN)

async def cmd_desbloquear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    if not context.args:
        destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
        await context.bot.send_message(destino, "⚠️ Use: /desbloquear [palavra]")
        return
    palavra = " ".join(context.args).lower().strip()
    palavras = carregar_palavras_custom()
    if palavra in palavras:
        palavras.remove(palavra)
        salvar_palavras_custom(palavras)
        destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
        await context.bot.send_message(destino, f"✅ Palavra *\"{palavra}\"* removida da lista negra.", parse_mode=ParseMode.MARKDOWN)
    else:
        destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
        await context.bot.send_message(destino, f"⚠️ A palavra *\"{palavra}\"* não estava bloqueada.", parse_mode=ParseMode.MARKDOWN)

async def cmd_listanegra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    palavras = carregar_palavras_custom()
    from config import PALAVROES_EXATOS
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    if not palavras:
        await context.bot.send_message(
            destino,
            f"🚫 *LISTA NEGRA*\n\n"
            f"Palavrões padrão bloqueados: *{len(PALAVROES_EXATOS)}*\n"
            f"Palavras personalizadas: *0*\n\n"
            f"_Use /bloquear [palavra] para adicionar._",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        lista = "\n".join([f"• {p}" for p in palavras])
        await context.bot.send_message(
            destino,
            f"🚫 *LISTA NEGRA*\n\n"
            f"Palavrões padrão: *{len(PALAVROES_EXATOS)}*\n"
            f"Palavras personalizadas: *{len(palavras)}*\n\n"
            f"{lista}",
            parse_mode=ParseMode.MARKDOWN
        )

# ─── TESTEMUNHOS ───────────────────────────────────────────────────────────────

async def cmd_testemunho(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        texto = " ".join(context.args)
        if len(texto) < 20:
            await update.message.reply_text("⚠️ O testemunho está muito curto. Escreva mais detalhes! 🙏")
            return
        from testemunhos import salvar_testemunho
        nome = update.effective_user.first_name or "Membro"
        user_id = update.effective_user.id
        salvar_testemunho(nome, user_id, texto)
        try:
            from ranking import adicionar_pontos
            adicionar_pontos(user_id, nome, "testemunho")
        except:
            pass
        await update.message.reply_text(
            f"🌟 *Testemunho registrado, {nome}!*\n\nSerá publicado no canal em breve! 🙏\n\n_\"E venceram-no pelo sangue do Cordeiro e pela palavra do seu testemunho.\"_ — Apocalipse 12:11",
            parse_mode=ParseMode.MARKDOWN
        )
        if OWNER_ID:
            try:
                await context.bot.send_message(
                    OWNER_ID,
                    f"🌟 *Novo testemunho!*\nDe: *{nome}*\n\n_{texto[:300]}_",
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                pass
    else:
        await update.message.reply_text(
            "🌟 *SISTEMA DE TESTEMUNHOS*\n\n"
            "Para enviar seu testemunho, você tem 2 opções:\n\n"
            "1️⃣ Use o comando:\n`/testemunho [seu testemunho]`\n\n"
            "2️⃣ Envie uma mensagem de texto direto no privado do bot *@Avivamento_bot*\n\n"
            "Seu testemunho será publicado no canal toda *sexta-feira às 17h*! 🕊️\n\n"
            "_\"E venceram-no pelo sangue do Cordeiro e pela palavra do seu testemunho.\"_ — Apocalipse 12:11",
            parse_mode=ParseMode.MARKDOWN
        )

async def cmd_ver_testemunhos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from testemunhos import get_testemunhos_pendentes
    pendentes = get_testemunhos_pendentes()
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    if not pendentes:
        await context.bot.send_message(destino, "🌟 Nenhum testemunho pendente no momento.")
        return
    texto = f"🌟 *{len(pendentes)} TESTEMUNHOS PENDENTES*\n\n"
    for i, t in enumerate(pendentes[:5], 1):
        texto += f"*{i}. {t['nome']}* ({t['data']}):\n_{t['texto'][:150]}{'...' if len(t['texto']) > 150 else ''}_\n\n"
    if len(pendentes) > 5:
        texto += f"_...e mais {len(pendentes)-5} testemunhos._\n\n"
    texto += "Use /postar_testemunho para publicar o próximo no canal."
    await context.bot.send_message(destino, texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_postar_testemunho(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from agendador import postar_testemunho_canal
    class Ctx:
        bot = context.bot
    await postar_testemunho_canal(Ctx())
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(destino, "✅ Testemunho postado no canal!")

async def cmd_enquete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from agendador import postar_enquete_grupo
    class Ctx:
        bot = context.bot
    await postar_enquete_grupo(Ctx())

# ─── ESTATÍSTICAS / UTILITÁRIOS ───────────────────────────────────────────────

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    from testemunhos import get_testemunhos_pendentes
    pedidos = len(get_pedidos_pendentes())
    testemunhos = len(get_testemunhos_pendentes())
    palavras_custom = len(carregar_palavras_custom())
    texto = (
        "📊 *STATUS — AVIVAMENTO AD*\n\n"
        f"🎥 Vídeos na fila: *{total_videos()}*\n"
        f"🖼️ Imagens na fila: *{total_imagens()}*\n"
        f"🙏 Pedidos de oração: *{pedidos}*\n"
        f"🌟 Testemunhos pendentes: *{testemunhos}*\n"
        f"🚫 Palavras extras bloqueadas: *{palavras_custom}*\n\n"
        "⏰ *Posts automáticos ativos:*\n"
        "  📺 Canal: versículos, devocionais, mídias\n"
        "  👥 Grupo: orações, engajamento, enquetes\n"
        "  🌟 Testemunho: toda sexta 17h\n\n"
        "✅ Bot funcionando 24/7 na nuvem!\n"
        "🕊️ _Que Deus abençoe este ministério!_"
    )
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(destino, texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_listar_midia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(
        destino,
        f"📦 *Mídias armazenadas:*\n\n🎥 Vídeos: *{total_videos()}*\n🖼️ Imagens: *{total_imagens()}*\n\n_Envie vídeos/imagens no privado do bot para adicionar._",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_limpar_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    limpar_videos()
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(destino, "✅ Vídeos removidos.")

async def cmd_limpar_imagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    limpar_imagens()
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    await context.bot.send_message(destino, "✅ Imagens removidas.")

async def cmd_ver_pedidos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await deletar_comando(update)
    if not await is_admin(update, context):
        return
    pedidos = get_pedidos_pendentes()
    destino = update.effective_user.id if update.effective_chat.type in ["group", "supergroup"] else update.effective_chat.id
    if not pedidos:
        await context.bot.send_message(destino, "🙏 Nenhum pedido de oração pendente.")
        return
    texto = f"🙏 *{len(pedidos)} PEDIDOS DE ORAÇÃO PENDENTES*\n\n"
    for i, p in enumerate(pedidos, 1):
        texto += f"*{i}. {p['nome']}* — {p['data']}\n_{p['pedido']}_\n\n"
    await context.bot.send_message(destino, texto, parse_mode=ParseMode.MARKDOWN)

async def cmd_chatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    await update.message.reply_text(
        f"📋 *Informações do Chat*\n\n"
        f"🆔 Chat ID: `{chat.id}`\n"
        f"📝 Nome: {chat.title or chat.first_name}\n"
        f"🔹 Tipo: {chat.type}\n"
        f"👤 Seu ID: `{user.id}`\n"
        f"🔑 Dono registrado: `{OWNER_ID}`",
        parse_mode=ParseMode.MARKDOWN
    )
