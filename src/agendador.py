import logging
import random
from telegram import Bot
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bible import gerar_imagem_versiculo, get_saudacao
from media_manager import get_proximo_video, get_proxima_imagem
from regras import REGRAS_GRUPO
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
]

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
            CHANNEL_ID,
            photo=buf,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Versículo postado no canal com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao postar versículo: {e}")

async def postar_midia_no_canal(context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        saudacao = get_saudacao()
        tema = random.choice(TEMAS_PREGACAO)

        video = get_proximo_video()
        imagem = get_proxima_imagem()

        if not video and not imagem:
            logger.warning("Nenhuma mídia salva para postar.")
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
                CHANNEL_ID,
                video=midia["file_id"],
                caption=caption_base,
                parse_mode=ParseMode.MARKDOWN,
                supports_streaming=True
            )
        else:
            await context.bot.send_photo(
                CHANNEL_ID,
                photo=midia["file_id"],
                caption=caption_base,
                parse_mode=ParseMode.MARKDOWN
            )

        logger.info(f"Mídia ({tipo}) postada no canal.")
        return True

    except Exception as e:
        logger.error(f"Erro ao postar mídia: {e}")
        return False

async def postar_regras_grupo(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(
            GROUP_ID,
            REGRAS_GRUPO,
            parse_mode=ParseMode.MARKDOWN
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
            GROUP_ID,
            photo=buf,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Mensagem bíblica postada no grupo.")
    except Exception as e:
        logger.error(f"Erro ao postar no grupo: {e}")

def configurar_agendamentos(app):
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    import pytz

    tz = pytz.timezone("America/Sao_Paulo")
    scheduler = AsyncIOScheduler(timezone=tz)

    async def job_versiculo():
        class FakeContext:
            bot = app.bot
        await postar_versiculo_canal(FakeContext())

    async def job_midia():
        class FakeContext:
            bot = app.bot
        await postar_midia_no_canal(FakeContext())

    async def job_regras():
        class FakeContext:
            bot = app.bot
        await postar_regras_grupo(FakeContext())

    async def job_biblica_grupo():
        class FakeContext:
            bot = app.bot
        await postar_mensagem_biblica_grupo(FakeContext())

    scheduler.add_job(job_versiculo, CronTrigger(hour=7, minute=0))
    scheduler.add_job(job_versiculo, CronTrigger(hour=13, minute=0))
    scheduler.add_job(job_versiculo, CronTrigger(hour=21, minute=0))

    scheduler.add_job(job_midia, CronTrigger(hour=9, minute=0))
    scheduler.add_job(job_midia, CronTrigger(hour=19, minute=0))

    scheduler.add_job(job_regras, CronTrigger(hour="*/4", minute=0))

    scheduler.add_job(job_biblica_grupo, CronTrigger(hour=7, minute=5))
    scheduler.add_job(job_biblica_grupo, CronTrigger(hour=13, minute=5))
    scheduler.add_job(job_biblica_grupo, CronTrigger(hour=21, minute=5))

    scheduler.start()
    logger.info("Agendamentos configurados com sucesso!")
    return scheduler
