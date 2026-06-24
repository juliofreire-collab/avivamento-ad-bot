"""
Teste ao vivo — CANAL exclusivamente
Testa todos os posts automáticos que vão para o canal @avivamentoad.
Nenhuma mensagem é enviada ao grupo neste script.
Execute: cd telegram-bot && python test_canal.py
"""
import sys, os, asyncio, traceback, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from telegram import Bot
from telegram.constants import ParseMode

BOT_TOKEN  = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@avivamentoad")
OWNER_ID   = int(os.environ.get("OWNER_ID", "8725437154"))

VERDE   = "\033[92m"
VERMELHO = "\033[91m"
AZUL    = "\033[94m"
NEGRITO = "\033[1m"
RESET   = "\033[0m"

resultados = []

def ok(label, detalhe=""):
    print(f"  {VERDE}✅ {label}{RESET}" + (f" — {detalhe}" if detalhe else ""))
    resultados.append(("ok", label))

def falha(label, erro):
    print(f"  {VERMELHO}❌ {label}{RESET} — {str(erro)[:150]}")
    traceback.print_exc()
    resultados.append(("falha", label))

def secao(titulo):
    print(f"\n{NEGRITO}{AZUL}{'═'*60}{RESET}")
    print(f"{NEGRITO}{AZUL}  {titulo}{RESET}")
    print(f"{NEGRITO}{AZUL}{'═'*60}{RESET}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    me = await bot.get_me()

    print(f"\n{NEGRITO}📺  TESTE AO VIVO — CANAL {CHANNEL_ID}{RESET}")
    print(f"Bot: @{me.username}  |  Destino: {CHANNEL_ID}")
    print(f"⚠️  Nenhuma mensagem será enviada ao grupo neste teste.\n")

    # ══════════════════════════════════════════════════════════
    secao("1. VERSÍCULO COM IMAGEM  (automático: 07h · 12h · 21h)")
    # ══════════════════════════════════════════════════════════
    try:
        from bible import gerar_imagem_versiculo
        from agendador import LINK_CANAL
        buf, ref, txt = gerar_imagem_versiculo()
        caption = (
            f"📖 *{ref}*\n\n"
            f'_"{txt}"_\n\n'
            f"🕊️ *Avivamento AD*\n\n"
            f"[📤 Toque para compartilhar esta bênção]({LINK_CANAL})"
        )
        msg = await bot.send_photo(
            chat_id=CHANNEL_ID, photo=buf,
            caption=caption, parse_mode=ParseMode.MARKDOWN
        )
        ok("Versículo com imagem postado no CANAL", f"ref={ref} | msg_id={msg.message_id}")
    except Exception as e:
        falha("Versículo com imagem", e)

    await asyncio.sleep(1)

    # ══════════════════════════════════════════════════════════
    secao("2. DEVOCIONAL  (automático: 06h · 18h)")
    # ══════════════════════════════════════════════════════════
    try:
        from oracao import DEVOCIONAIS
        from agendador import LINK_CANAL
        dev = random.choice(DEVOCIONAIS)
        texto = (
            f'✨ *{dev["titulo"]}*\n\n'
            f'{dev["texto"]}\n\n'
            f"🕊️ *Avivamento AD*\n\n"
            f"[📤 Compartilhe este devocional]({LINK_CANAL})"
        )
        msg = await bot.send_message(
            chat_id=CHANNEL_ID, text=texto, parse_mode=ParseMode.MARKDOWN
        )
        ok("Devocional postado no CANAL", f"{dev['titulo'][:45]} | msg_id={msg.message_id}")
    except Exception as e:
        falha("Devocional", e)

    await asyncio.sleep(1)

    # ══════════════════════════════════════════════════════════
    secao("3. MÍDIA DA FILA  (automático: 09h · 19h)")
    # ══════════════════════════════════════════════════════════
    try:
        from media_manager import get_proximo_video, get_proxima_imagem, total_videos, total_imagens
        from bible import get_saudacao
        from agendador import TEMAS_PREGACAO, LINK_CANAL
        v = total_videos()
        i = total_imagens()
        video = get_proximo_video()
        imagem = get_proxima_imagem()
        if not video and not imagem:
            ok("Fila de mídias vazia — sem post",
               f"0 vídeos · 0 imagens | Envie arquivos no privado do bot para preencher a fila")
        else:
            saudacao = get_saudacao()
            tema = random.choice(TEMAS_PREGACAO)
            opcoes = []
            if video:  opcoes.append(("video", video))
            if imagem: opcoes.append(("imagem", imagem))
            tipo, midia = random.choice(opcoes)
            caption_base = (
                f"{saudacao} 🙏\n\n"
                f"✝️ *{tema}*\n\n"
                f'{midia.get("caption","")}\n\n'
                f"🕊️ *Avivamento AD*\n\n"
                f"[📤 Compartilhe esta mensagem]({LINK_CANAL})"
            ).strip()
            if tipo == "video":
                msg = await bot.send_video(
                    chat_id=CHANNEL_ID, video=midia["file_id"],
                    caption=caption_base, parse_mode=ParseMode.MARKDOWN,
                    supports_streaming=True
                )
            else:
                msg = await bot.send_photo(
                    chat_id=CHANNEL_ID, photo=midia["file_id"],
                    caption=caption_base, parse_mode=ParseMode.MARKDOWN
                )
            ok(f"Mídia ({tipo}) postada no CANAL", f"{v} vídeo(s) · {i} imagem(ns) na fila | msg_id={msg.message_id}")
    except Exception as e:
        falha("Mídia da fila", e)

    await asyncio.sleep(1)

    # ══════════════════════════════════════════════════════════
    secao("4. TESTEMUNHO  (automático: toda sexta 17h)")
    # ══════════════════════════════════════════════════════════
    try:
        from testemunhos import get_testemunhos_pendentes, salvar_testemunho, get_proximo_testemunho_nao_publicado
        from agendador import LINK_CANAL
        pendentes = get_testemunhos_pendentes()
        if not pendentes:
            print(f"  ℹ️  Nenhum testemunho pendente — inserindo um de demonstração...")
            salvar_testemunho(
                "Membro Demonstração", 99000002,
                "Testemunho de demonstração: a graça de Deus tem sido suficiente "
                "em cada etapa da minha jornada. Sou grato(a) por cada vitória e "
                "cada desafio que me aproximou mais dEle. Aleluia! 🙏"
            )
        t = get_proximo_testemunho_nao_publicado()
        if t:
            # ── posta SOMENTE no canal (sem notificação de grupo) ──
            texto = (
                f"🌟 *TESTEMUNHO DA SEMANA*\n\n"
                f'_{t["texto"]}_\n\n'
                f'✝️ — *{t["nome"]}*\n\n'
                f"🕊️ *Avivamento AD*\n\n"
                f"[📤 Compartilhe esta bênção]({LINK_CANAL})"
            )
            msg = await bot.send_message(
                chat_id=CHANNEL_ID, text=texto, parse_mode=ParseMode.MARKDOWN
            )
            ok("Testemunho postado no CANAL", f"de: {t['nome']} | msg_id={msg.message_id}")
        else:
            ok("Nenhum testemunho disponível para post", "")
    except Exception as e:
        falha("Testemunho", e)

    await asyncio.sleep(1)

    # ══════════════════════════════════════════════════════════
    secao("5. SEGUNDA IMAGEM BÍBLICA  (automático: 13h · 21h10)")
    # ══════════════════════════════════════════════════════════
    try:
        from bible import gerar_imagem_versiculo
        from agendador import LINK_CANAL
        buf2, ref2, txt2 = gerar_imagem_versiculo()
        caption2 = (
            f"📖 *{ref2}*\n\n"
            f'_"{txt2}"_\n\n'
            f"🕊️ *Avivamento AD*\n\n"
            f"[📤 Toque para compartilhar]({LINK_CANAL})"
        )
        msg2 = await bot.send_photo(
            chat_id=CHANNEL_ID, photo=buf2,
            caption=caption2, parse_mode=ParseMode.MARKDOWN
        )
        ok("Segunda imagem bíblica no CANAL", f"ref={ref2} | msg_id={msg2.message_id}")
    except Exception as e:
        falha("Segunda imagem bíblica", e)

    await asyncio.sleep(1)

    # ══════════════════════════════════════════════════════════
    secao("6. VERIFICAÇÃO DE PERMISSÕES NO CANAL")
    # ══════════════════════════════════════════════════════════
    try:
        chat = await bot.get_chat(CHANNEL_ID)
        member = await bot.get_chat_member(CHANNEL_ID, me.id)
        ok(f"Canal: «{chat.title}»", f"bot é {member.status}")
        inscritos = chat.linked_chat_id
        if inscritos:
            ok("Grupo vinculado detectado", str(inscritos))
    except Exception as e:
        falha("Verificação do canal", e)

    # ══════════════════════════════════════════════════════════
    secao("RESULTADO FINAL")
    # ══════════════════════════════════════════════════════════
    total_ok   = sum(1 for r in resultados if r[0] == "ok")
    total_fail = sum(1 for r in resultados if r[0] == "falha")

    print()
    if total_fail == 0:
        print(f"{VERDE}{NEGRITO}  🎉 {total_ok} OK  |  {total_fail} FALHAS — Canal 100% funcional!{RESET}")
    else:
        falhas_lista = [r[1] for r in resultados if r[0] == "falha"]
        print(f"{VERMELHO}{NEGRITO}  {total_ok} OK  |  {total_fail} FALHAS{RESET}")
        for f in falhas_lista:
            print(f"  {VERMELHO}• {f}{RESET}")

    # Resumo no privado do dono
    try:
        resumo = (
            f"📺 *TESTE DO CANAL — CONCLUÍDO*\n\n"
            f"✅ Passou: *{total_ok}*\n"
            f"❌ Falhou: *{total_fail}*\n\n"
            f"*Posts testados exclusivamente no canal:*\n"
            f"• 📖 Versículo com imagem\n"
            f"• ✨ Devocional\n"
            f"• 🎥 Mídia da fila\n"
            f"• 🌟 Testemunho\n"
            f"• 📖 Segunda imagem bíblica\n\n"
            f"{'🎉 Canal 100% operacional!' if total_fail == 0 else '⚠️ Verifique as falhas acima.'}\n"
            f"🕊️ _Avivamento AD_"
        )
        await bot.send_message(OWNER_ID, resumo, parse_mode=ParseMode.MARKDOWN)
        print(f"\n  {VERDE}✅ Resumo enviado ao dono no Telegram.{RESET}")
    except Exception as e:
        print(f"\n  ⚠️  Não foi possível enviar resumo: {e}")

    print()
    return total_fail

if __name__ == "__main__":
    falhas = asyncio.run(main())
    sys.exit(0 if falhas == 0 else 1)
