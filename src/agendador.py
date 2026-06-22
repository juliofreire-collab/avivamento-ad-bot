import logging
import random
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bible import gerar_imagem_versiculo, get_saudacao
from media_manager import get_proximo_video, get_proxima_imagem
from regras import REGRAS_GRUPO
from oracao import ORACOES_DO_DIA, DEVOCIONAIS, PERGUNTAS_ENGAJAMENTO
from config import CHANNEL_ID, GROUP_ID

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

    scheduler.start()
    logger.info("✅ Todos os agendamentos configurados!")
    return scheduler
