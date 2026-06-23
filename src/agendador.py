import logging
import random
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bible import gerar_imagem_versiculo, get_saudacao
from media_manager import get_proximo_video, get_proxima_imagem
from regras import REGRAS_GRUPO
from oracao import ORACOES_DO_DIA, DEVOCIONAIS, PERGUNTAS_ENGAJAMENTO
from config import CHANNEL_ID, GROUP_ID

ENQUETES_SEMANAIS = [
    {
        "pergunta": "🎵 Qual estilo de música gospel você mais ama?",
        "opcoes": ["Hinos tradicionais", "Gospel contemporâneo", "Adoração e louvor", "Música instrumental", "Sertanejo gospel"]
    },
    {
        "pergunta": "📖 Qual livro da Bíblia você mais gosta de ler?",
        "opcoes": ["Salmos", "Provérbios", "João", "Romanos", "Apocalipse"]
    },
    {
        "pergunta": "🙏 Como você costuma orar?",
        "opcoes": ["De manhã ao acordar", "À noite antes de dormir", "Durante o dia quando preciso", "Em momentos específicos", "O tempo todo"]
    },
    {
        "pergunta": "✝️ O que mais te edifica espiritualmente?",
        "opcoes": ["Orar", "Ler a Bíblia", "Louvar e adorar", "Comunhão com irmãos", "Jejum e oração"]
    },
    {
        "pergunta": "🌅 Qual é o seu versículo favorito?",
        "opcoes": ["Filipenses 4:13", "João 3:16", "Jeremias 29:11", "Salmos 23:1", "Romanos 8:28"]
    },
    {
        "pergunta": "🔥 O que significa avivamento para você?",
        "opcoes": ["Renovação espiritual pessoal", "Crescimento da Igreja", "Milagres e curas", "Conversão de almas", "Todas as opções acima"]
    },
    {
        "pergunta": "⛪ Com que frequência você vai à igreja?",
        "opcoes": ["Todo domingo", "Várias vezes por semana", "Uma vez por mês", "Em datas especiais", "Assisto online"]
    },
    {
        "pergunta": "💪 Como você enfrenta os momentos difíceis?",
        "opcoes": ["Com oração intensa", "Lendo a Palavra", "Com apoio dos irmãos", "Louvor mesmo na dor", "Todas as anteriores"]
    },
    {
        "pergunta": "🌟 Qual promessa bíblica mais te fortalece?",
        "opcoes": ["\"Tudo posso em Cristo\"", "\"Nunca te deixarei\"", "\"Sou contigo\"", "\"Planos de prosperidade\"", "\"O amor de Deus\""]
    },
    {
        "pergunta": "🕊️ Como você descreveria sua relação com Deus hoje?",
        "opcoes": ["Muito próxima e crescendo", "Boa, mas quero mais", "Passando por desafios", "Estou me reconectando", "Em constante busca"]
    },
]

logger = logging.getLogger(__name__)

LINK_CANAL = "https://t.me/avivamentoad"
LINK_GRUPO = "https://t.me/+FALJMPVXpj1kOGQx"

TEMAS_PREGACAO = [
    "A fé que move montanhas",
    "O amor de Deus é incondicional",
    "A graça transformadora",
    "Avivamento do Espírito Santo",
    "A paz que excede todo entendimento",
    "Caminhar com Deus todos os dias",
    "A esperança que não envergonha",
    "Renovação pela Palavra de Deus",
    "O poder da oração",
    "Confiança no Senhor em tempos difíceis",
    "A cura que vem do Alto",
    "Vitória em Cristo Jesus",
    "O Espírito Santo como Consolador",
    "Gratidão que transforma",
    "A Palavra que não volta vazia",
]

# ─── CANAL ───────────────────────────────────────────────────────────────────

async def postar_versiculo_canal(context: ContextTypes.DEFAULT_TYPE):
    try:
        buf, referencia, texto = gerar_imagem_versiculo()
        caption = (
            f'📖 *{referencia}*\n\n'
            f'_"{texto}"_\n\n'
            f'🕊️ *Avivamento AD*\n\n'
            f'[📤 Toque para compartilhar esta bênção]({LINK_CANAL})'
        )
        await context.bot.send_photo(
            CHANNEL_ID, photo=buf, caption=caption, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Versículo postado no canal.")
    except Exception as e:
        logger.error(f"Erro ao postar versículo no canal: {e}")

async def postar_midia_no_canal(context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        saudacao = get_saudacao()
        tema = random.choice(TEMAS_PREGACAO)
        video = get_proximo_video()
        imagem = get_proxima_imagem()

        if not video and not imagem:
            logger.warning("Nenhuma mídia salva. Postando versículo no lugar.")
            await postar_versiculo_canal(context)
            return False

        opcoes = []
        if video:
            opcoes.append(("video", video))
        if imagem:
            opcoes.append(("imagem", imagem))

        tipo, midia = random.choice(opcoes)
        caption_base = (
            f'{saudacao} 🙏\n\n'
            f'✝️ *{tema}*\n\n'
            f'{midia.get("caption", "")}\n\n'
            f'🕊️ *Avivamento AD*\n\n'
            f'[📤 Compartilhe esta mensagem]({LINK_CANAL})'
        ).strip()

        if tipo == "video":
            await context.bot.send_video(
                CHANNEL_ID, video=midia["file_id"], caption=caption_base,
                parse_mode=ParseMode.MARKDOWN, supports_streaming=True
            )
        else:
            await context.bot.send_photo(
                CHANNEL_ID, photo=midia["file_id"], caption=caption_base,
                parse_mode=ParseMode.MARKDOWN
            )
        logger.info(f"Mídia ({tipo}) postada no canal.")
        return True
    except Exception as e:
        logger.error(f"Erro ao postar mídia no canal: {e}")
        return False

async def postar_devocional_canal(context: ContextTypes.DEFAULT_TYPE):
    try:
        devocional = random.choice(DEVOCIONAIS)
        texto = (
            f'✨ *{devocional["titulo"]}*\n\n'
            f'{devocional["texto"]}\n\n'
            f'🕊️ *Avivamento AD*\n\n'
            f'[📤 Compartilhe este devocional]({LINK_CANAL})'
        )
        await context.bot.send_message(
            CHANNEL_ID, text=texto, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Devocional postado no canal.")
    except Exception as e:
        logger.error(f"Erro ao postar devocional no canal: {e}")

# ─── GRUPO ────────────────────────────────────────────────────────────────────

async def postar_regras_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(
            GROUP_ID, REGRAS_GRUPO, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Regras postadas no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar regras: {e}")

async def postar_mensagem_biblica_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        buf, referencia, texto = gerar_imagem_versiculo()
        caption = (
            f'📖 *{referencia}*\n\n'
            f'_"{texto}"_\n\n'
            f'🕊️ *Avivamento AD*\n\n'
            f'[📤 Compartilhe]({LINK_GRUPO})'
        )
        await context.bot.send_photo(
            GROUP_ID, photo=buf, caption=caption, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Mensagem bíblica postada no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar bíblica no grupo: {e}")

async def postar_oracao_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        oracao = random.choice(ORACOES_DO_DIA)
        await context.bot.send_message(
            GROUP_ID, oracao, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Oração postada no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar oração no grupo: {e}")

async def postar_engajamento_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        pergunta = random.choice(PERGUNTAS_ENGAJAMENTO)
        await context.bot.send_message(
            GROUP_ID, pergunta, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Pergunta de engajamento postada no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar engajamento no grupo: {e}")

async def postar_devocional_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        devocional = random.choice(DEVOCIONAIS)
        texto = (
            f'✨ *{devocional["titulo"]}*\n\n'
            f'{devocional["texto"]}'
        )
        await context.bot.send_message(
            GROUP_ID, texto, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Devocional postado no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar devocional no grupo: {e}")

async def verificar_aniversarios(context: ContextTypes.DEFAULT_TYPE):
    try:
        from aniversarios import get_aniversariantes_hoje
        aniversariantes = get_aniversariantes_hoje()
        if not aniversariantes:
            logger.info("Nenhum aniversariante hoje.")
            return

        mensagens_bolo = [
            "🎂🎉 Que o Senhor te abençoe ricamente neste dia especial!",
            "🎈🙏 Que Deus continue escrevendo uma história linda em sua vida!",
            "🎁✝️ Que este ano seja repleto das bênçãos do Senhor!",
            "🥳🌟 Feliz aniversário! Que a graça de Deus cubra cada passo seu!",
        ]

        for uid, nome, dia, mes in aniversariantes:
            mensagem_bolo = random.choice(mensagens_bolo)

            texto_grupo = (
                f"🎂 *FELIZ ANIVERSÁRIO, {nome.upper()}!* 🎉\n\n"
                f"{mensagem_bolo}\n\n"
                f"_\"O Senhor te abençoe e te guarde; o Senhor faça resplandecer o Seu rosto sobre ti.\"_\n"
                f"— Números 6:24-25\n\n"
                f"Toda a família Avivamento AD celebra com você! 🙏🎊"
            )
            await context.bot.send_message(GROUP_ID, texto_grupo, parse_mode=ParseMode.MARKDOWN)

            try:
                texto_privado = (
                    f"🎂 *Feliz Aniversário, {nome}!*\n\n"
                    f"A família Avivamento AD te deseja um dia abençoado! ✝️🎉\n\n"
                    f"_\"Porque sou eu que conheço os planos que tenho para vocês, diz o Senhor, planos de fazê-los prosperar e não de causar dano, planos de dar a vocês esperança e um futuro.\"_\n"
                    f"— Jeremias 29:11"
                )
                await context.bot.send_message(int(uid), texto_privado, parse_mode=ParseMode.MARKDOWN)
                logger.info(f"Mensagem privada de aniversário enviada para {nome} ({uid})")
            except Exception:
                logger.info(f"Não foi possível enviar privado para {nome} ({uid}) — sem conversa iniciada com o bot.")

        logger.info(f"Aniversários processados: {len(aniversariantes)} membro(s).")
    except Exception as e:
        logger.error(f"Erro ao verificar aniversários: {e}")

async def postar_ranking_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        from ranking import get_top_ranking
        top = get_top_ranking(10)
        if not top:
            logger.info("Nenhum dado de ranking para postar.")
            return

        medalhas = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        texto = "🏆 *RANKING DE ENGAJAMENTO — SEMANA*\n\n"
        texto += "_Membros mais ativos que edificam nossa família!_\n\n"

        for i, (uid, nome, pontos) in enumerate(top):
            medalha = medalhas[i] if i < len(medalhas) else f"{i+1}."
            texto += f"{medalha} *{nome}* — {pontos} pontos\n"

        texto += (
            "\n🌟 *Como ganhar pontos:*\n"
            "• Enviar testemunho: +10 pts\n"
            "• Pedido de oração: +5 pts\n"
            "• Participar de perguntas: +3 pts\n"
            "• Mensagens no grupo: +1 pt/dia\n\n"
            f"[📢 Acesse o canal]({LINK_CANAL})\n\n"
            "_\"Portanto, encorajai-vos uns aos outros.\"_ — 1 Tessalonicenses 5:11"
        )

        await context.bot.send_message(GROUP_ID, texto, parse_mode=ParseMode.MARKDOWN)
        logger.info("Ranking semanal postado no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar ranking: {e}")

async def postar_testemunho_canal(context: ContextTypes.DEFAULT_TYPE):
    try:
        from testemunhos import get_proximo_testemunho_nao_publicado
        t = get_proximo_testemunho_nao_publicado()
        if not t:
            logger.info("Nenhum testemunho pendente para postar.")
            return
        texto = (
            f'🌟 *TESTEMUNHO DA SEMANA*\n\n'
            f'_{t["texto"]}_\n\n'
            f'✝️ — *{t["nome"]}*\n\n'
            f'🕊️ *Avivamento AD*\n\n'
            f'[📤 Compartilhe esta bênção]({LINK_CANAL})'
        )
        await context.bot.send_message(CHANNEL_ID, texto, parse_mode=ParseMode.MARKDOWN)
        await context.bot.send_message(
            GROUP_ID,
            f'🌟 *TESTEMUNHO DA SEMANA no canal!*\n\n'
            f'Acesse o canal para ler e se edificar!\n'
            f'[👉 Ver no canal]({LINK_CANAL})',
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"Testemunho de {t['nome']} postado no canal.")
    except Exception as e:
        logger.error(f"Erro ao postar testemunho: {e}")

async def postar_enquete_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        enquete = random.choice(ENQUETES_SEMANAIS)
        await context.bot.send_poll(
            chat_id=GROUP_ID,
            question=enquete["pergunta"],
            options=enquete["opcoes"],
            is_anonymous=False,
            allows_multiple_answers=False,
        )
        await context.bot.send_message(
            GROUP_ID,
            "🗳️ *ENQUETE DA SEMANA!*\n\n"
            "Participe e compartilhe sua opinião! Adoramos conhecer melhor nossa família espiritual. 🙏\n\n"
            "_\"Onde não há sábios conselheiros, o povo perece; mas havendo muitos conselheiros, há prosperidade.\"_ — Provérbios 11:14\n\n"
            f"[📤 Convide alguém para participar]({LINK_GRUPO})",
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Enquete semanal postada no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar enquete: {e}")

# ─── AGENDAMENTOS ─────────────────────────────────────────────────────────────

def configurar_agendamentos(app):
    import pytz
    from datetime import time as dtime

    tz = pytz.timezone("America/Sao_Paulo")
    jq = app.job_queue

    # ── CANAL ──
    # Versículos: 07h, 12h, 21h
    jq.run_daily(postar_versiculo_canal, time=dtime(7, 0, tzinfo=tz))
    jq.run_daily(postar_versiculo_canal, time=dtime(12, 0, tzinfo=tz))
    jq.run_daily(postar_versiculo_canal, time=dtime(21, 0, tzinfo=tz))

    # Mídias (vídeos/fotos): 09h e 19h
    jq.run_daily(postar_midia_no_canal, time=dtime(9, 0, tzinfo=tz))
    jq.run_daily(postar_midia_no_canal, time=dtime(19, 0, tzinfo=tz))

    # Devocional no canal: 06h e 18h
    jq.run_daily(postar_devocional_canal, time=dtime(6, 0, tzinfo=tz))
    jq.run_daily(postar_devocional_canal, time=dtime(18, 0, tzinfo=tz))

    # ── GRUPO ──
    # Oração da manhã: 06h05
    jq.run_daily(postar_oracao_grupo, time=dtime(6, 5, tzinfo=tz))

    # Versículo/bíblica no grupo: 07h10, 13h, 21h10
    jq.run_daily(postar_mensagem_biblica_grupo, time=dtime(7, 10, tzinfo=tz))
    jq.run_daily(postar_mensagem_biblica_grupo, time=dtime(13, 0, tzinfo=tz))
    jq.run_daily(postar_mensagem_biblica_grupo, time=dtime(21, 10, tzinfo=tz))

    # Devocional no grupo: 08h e 20h
    jq.run_daily(postar_devocional_grupo, time=dtime(8, 0, tzinfo=tz))
    jq.run_daily(postar_devocional_grupo, time=dtime(20, 0, tzinfo=tz))

    # Pergunta de engajamento: 10h e 15h
    jq.run_daily(postar_engajamento_grupo, time=dtime(10, 0, tzinfo=tz))
    jq.run_daily(postar_engajamento_grupo, time=dtime(15, 0, tzinfo=tz))

    # Oração da noite: 22h
    jq.run_daily(postar_oracao_grupo, time=dtime(22, 0, tzinfo=tz))

    # Regras a cada 4 horas (06:30, 10:30, 14:30, 18:30, 22:30)
    for h in [6, 10, 14, 18, 22]:
        jq.run_daily(postar_regras_grupo, time=dtime(h, 30, tzinfo=tz))

    # Enquete semanal: segunda-feira às 10h
    jq.run_daily(postar_enquete_grupo, time=dtime(10, 0, tzinfo=tz), days=(0,))
    # Enquete extra: quinta-feira às 19h
    jq.run_daily(postar_enquete_grupo, time=dtime(19, 0, tzinfo=tz), days=(3,))

    # Testemunho no canal: sexta-feira às 17h
    jq.run_daily(postar_testemunho_canal, time=dtime(17, 0, tzinfo=tz), days=(4,))

    # Ranking semanal: domingo às 20h
    jq.run_daily(postar_ranking_grupo, time=dtime(20, 0, tzinfo=tz), days=(6,))

    # Aniversários: todo dia às 08h30
    jq.run_daily(verificar_aniversarios, time=dtime(8, 30, tzinfo=tz))

    logger.info("✅ Todos os agendamentos configurados!")# ─── GRUPO ────────────────────────────────────────────────────────────────────

async def postar_regras_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(
            GROUP_ID, REGRAS_GRUPO, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Regras postadas no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar regras: {e}")

async def postar_mensagem_biblica_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        buf, referencia, texto = gerar_imagem_versiculo()
        caption = (
            f'📖 *{referencia}*\n\n'
            f'_"{texto}"_\n\n'
            f'🕊️ *Avivamento AD*\n\n'
            f'[📤 Compartilhe]({LINK_GRUPO})'
        )
        await context.bot.send_photo(
            GROUP_ID, photo=buf, caption=caption, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Mensagem bíblica postada no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar bíblica no grupo: {e}")

async def postar_oracao_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        oracao = random.choice(ORACOES_DO_DIA)
        await context.bot.send_message(
            GROUP_ID, oracao, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Oração postada no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar oração no grupo: {e}")

async def postar_engajamento_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        pergunta = random.choice(PERGUNTAS_ENGAJAMENTO)
        await context.bot.send_message(
            GROUP_ID, pergunta, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Pergunta de engajamento postada no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar engajamento no grupo: {e}")

async def postar_devocional_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        devocional = random.choice(DEVOCIONAIS)
        texto = (
            f'✨ *{devocional["titulo"]}*\n\n'
            f'{devocional["texto"]}'
        )
        await context.bot.send_message(
            GROUP_ID, texto, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Devocional postado no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar devocional no grupo: {e}")

async def verificar_aniversarios(context: ContextTypes.DEFAULT_TYPE):
    try:
        from aniversarios import get_aniversariantes_hoje
        aniversariantes = get_aniversariantes_hoje()
        if not aniversariantes:
            logger.info("Nenhum aniversariante hoje.")
            return

        mensagens_bolo = [
            "🎂🎉 Que o Senhor te abençoe ricamente neste dia especial!",
            "🎈🙏 Que Deus continue escrevendo uma história linda em sua vida!",
            "🎁✝️ Que este ano seja repleto das bênçãos do Senhor!",
            "🥳🌟 Feliz aniversário! Que a graça de Deus cubra cada passo seu!",
        ]

        for uid, nome, dia, mes in aniversariantes:
            mensagem_bolo = random.choice(mensagens_bolo)

            # Mensagem no grupo
            texto_grupo = (
                f"🎂 *FELIZ ANIVERSÁRIO, {nome.upper()}!* 🎉\n\n"
                f"{mensagem_bolo}\n\n"
                f"_\"O Senhor te abençoe e te guarde; o Senhor faça resplandecer o Seu rosto sobre ti.\"_\n"
                f"— Números 6:24-25\n\n"
                f"Toda a família Avivamento AD celebra com você! 🙏🎊"
            )
            await context.bot.send_message(GROUP_ID, texto_grupo, parse_mode=ParseMode.MARKDOWN)

            # Mensagem privada ao aniversariante
            try:
                texto_privado = (
                    f"🎂 *Feliz Aniversário, {nome}!*\n\n"
                    f"A família Avivamento AD te deseja um dia abençoado! ✝️🎉\n\n"
                    f"_\"Porque sou eu que conheço os planos que tenho para vocês, diz o Senhor, planos de fazê-los prosperar e não de causar dano, planos de dar a vocês esperança e um futuro.\"_\n"
                    f"— Jeremias 29:11"
                )
                await context.bot.send_message(int(uid), texto_privado, parse_mode=ParseMode.MARKDOWN)
                logger.info(f"Mensagem privada de aniversário enviada para {nome} ({uid})")
            except Exception:
                logger.info(f"Não foi possível enviar privado para {nome} ({uid}) — sem conversa iniciada com o bot.")

        logger.info(f"Aniversários processados: {len(aniversariantes)} membro(s).")
    except Exception as e:
        logger.error(f"Erro ao verificar aniversários: {e}")

async def postar_ranking_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        from ranking import get_top_ranking
        top = get_top_ranking(10)
        if not top:
            logger.info("Nenhum dado de ranking para postar.")
            return

        medalhas = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        texto = "🏆 *RANKING DE ENGAJAMENTO — SEMANA*\n\n"
        texto += "_Membros mais ativos que edificam nossa família!_\n\n"

        for i, (uid, nome, pontos) in enumerate(top):
            medalha = medalhas[i] if i < len(medalhas) else f"{i+1}."
            texto += f"{medalha} *{nome}* — {pontos} pontos\n"

        texto += (
            "\n🌟 *Como ganhar pontos:*\n"
            "• Enviar testemunho: +10 pts\n"
            "• Pedido de oração: +5 pts\n"
            "• Participar de perguntas: +3 pts\n"
            "• Mensagens no grupo: +1 pt/dia\n\n"
            f"[📢 Acesse o canal]({LINK_CANAL})\n\n"
            "_\"Portanto, encorajai-vos uns aos outros.\"_ — 1 Tessalonicenses 5:11"
        )

        await context.bot.send_message(GROUP_ID, texto, parse_mode=ParseMode.MARKDOWN)
        logger.info("Ranking semanal postado no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar ranking: {e}")

async def postar_testemunho_canal(context: ContextTypes.DEFAULT_TYPE):
    try:
        from testemunhos import get_proximo_testemunho_nao_publicado
        t = get_proximo_testemunho_nao_publicado()
        if not t:
            logger.info("Nenhum testemunho pendente para postar.")
            return
        texto = (
            f'🌟 *TESTEMUNHO DA SEMANA*\n\n'
            f'_{t["texto"]}_\n\n'
            f'✝️ — *{t["nome"]}*\n\n'
            f'🕊️ *Avivamento AD*\n\n'
            f'[📤 Compartilhe esta bênção]({LINK_CANAL})'
        )
        await context.bot.send_message(CHANNEL_ID, texto, parse_mode=ParseMode.MARKDOWN)
        # Avisar o grupo também
        await context.bot.send_message(
            GROUP_ID,
            f'🌟 *TESTEMUNHO DA SEMANA no canal!*\n\n'
            f'Acesse o canal para ler e se edificar!\n'
            f'[👉 Ver no canal]({LINK_CANAL})',
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"Testemunho de {t['nome']} postado no canal.")
    except Exception as e:
        logger.error(f"Erro ao postar testemunho: {e}")

async def postar_enquete_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        enquete = random.choice(ENQUETES_SEMANAIS)
        await context.bot.send_poll(
            chat_id=GROUP_ID,
            question=enquete["pergunta"],
            options=enquete["opcoes"],
            is_anonymous=False,
            allows_multiple_answers=False,
        )
        # Mensagem de incentivo junto com a enquete
        await context.bot.send_message(
            GROUP_ID,
            "🗳️ *ENQUETE DA SEMANA!*\n\n"
            "Participe e compartilhe sua opinião! Adoramos conhecer melhor nossa família espiritual. 🙏\n\n"
            "_\"Onde não há sábios conselheiros, o povo perece; mas havendo muitos conselheiros, há prosperidade.\"_ — Provérbios 11:14\n\n"
            f"[📤 Convide alguém para participar]({LINK_GRUPO})",
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Enquete semanal postada no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar enquete: {e}")

# ─── AGENDAMENTOS ─────────────────────────────────────────────────────────────

def configurar_agendamentos(app):
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    import pytz

    tz = pytz.timezone("America/Sao_Paulo")
    scheduler = AsyncIOScheduler(timezone=tz)

    def ctx():
        class FakeContext:
            bot = app.bot
        return FakeContext()

    # ── CANAL ──
    # Versículos: 07h, 12h, 21h
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_versiculo_canal(ctx())), CronTrigger(hour=7, minute=0))
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_versiculo_canal(ctx())), CronTrigger(hour=12, minute=0))
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_versiculo_canal(ctx())), CronTrigger(hour=21, minute=0))

    # Mídias (vídeos/fotos do dono): 09h e 19h
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_midia_no_canal(ctx())), CronTrigger(hour=9, minute=0))
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_midia_no_canal(ctx())), CronTrigger(hour=19, minute=0))

    # Devocional no canal: 06h e 18h
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_devocional_canal(ctx())), CronTrigger(hour=6, minute=0))
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_devocional_canal(ctx())), CronTrigger(hour=18, minute=0))

    # ── GRUPO ──
    # Oração da manhã: 06h05
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_oracao_grupo(ctx())), CronTrigger(hour=6, minute=5))

    # Versículo/bíblica no grupo: 07h10, 13h, 21h10
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_mensagem_biblica_grupo(ctx())), CronTrigger(hour=7, minute=10))
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_mensagem_biblica_grupo(ctx())), CronTrigger(hour=13, minute=0))
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_mensagem_biblica_grupo(ctx())), CronTrigger(hour=21, minute=10))

    # Devocional no grupo: 08h e 20h
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_devocional_grupo(ctx())), CronTrigger(hour=8, minute=0))
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_devocional_grupo(ctx())), CronTrigger(hour=20, minute=0))

    # Pergunta de engajamento: 10h e 15h
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_engajamento_grupo(ctx())), CronTrigger(hour=10, minute=0))
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_engajamento_grupo(ctx())), CronTrigger(hour=15, minute=0))

    # Oração da noite: 22h
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_oracao_grupo(ctx())), CronTrigger(hour=22, minute=0))

    # Regras a cada 4 horas
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_regras_grupo(ctx())), CronTrigger(hour="*/4", minute=30))

    # Enquete semanal: toda segunda-feira às 10h
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_enquete_grupo(ctx())), CronTrigger(day_of_week="mon", hour=10, minute=0))
    # Enquete extra: toda quinta-feira às 19h
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_enquete_grupo(ctx())), CronTrigger(day_of_week="thu", hour=19, minute=0))

    # Testemunho no canal: toda sexta-feira às 17h
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_testemunho_canal(ctx())), CronTrigger(day_of_week="fri", hour=17, minute=0))

    # Ranking semanal: todo domingo às 20h
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(postar_ranking_grupo(ctx())), CronTrigger(day_of_week="sun", hour=20, minute=0))

    # Aniversários: verificar todo dia às 08h30
    scheduler.add_job(lambda: __import__('asyncio').ensure_future(verificar_aniversarios(ctx())), CronTrigger(hour=8, minute=30))

    scheduler.start()
    logger.info("✅ Todos os agendamentos configurados!")
    return scheduler
