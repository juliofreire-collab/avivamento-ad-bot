import random
import io
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

VERSICULOS = [
    ("Filipenses 4:13", "Tudo posso naquele que me fortalece."),
    ("João 3:16", "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna."),
    ("Jeremias 29:11", "Porque sou eu que conheço os planos que tenho para vocês, diz o Senhor, planos de fazê-los prosperar e não de causar dano, planos de dar a vocês esperança e um futuro."),
    ("Salmos 23:1", "O Senhor é o meu pastor; nada me faltará."),
    ("Romanos 8:28", "Sabemos que todas as coisas cooperam para o bem daqueles que amam a Deus, daqueles que são chamados segundo o seu propósito."),
    ("Isaías 40:31", "Mas os que esperam no Senhor renovarão as suas forças; subirão com asas como águias; correrão e não se cansarão; caminharão e não se fatigarão."),
    ("Salmos 46:1", "Deus é o nosso refúgio e fortaleza, socorro bem presente na angústia."),
    ("Provérbios 3:5-6", "Confia no Senhor de todo o teu coração e não te estribes no teu próprio entendimento. Reconhece-o em todos os teus caminhos, e ele endireitará as tuas veredas."),
    ("Mateus 6:33", "Buscai primeiro o reino de Deus e a sua justiça, e todas essas coisas vos serão acrescentadas."),
    ("Salmos 91:1", "Aquele que habita no esconderijo do Altíssimo e descansa à sombra do Onipotente."),
    ("João 14:6", "Eu sou o caminho, a verdade e a vida. Ninguém vem ao Pai a não ser por mim."),
    ("Romanos 8:37", "Em todas estas coisas somos mais que vencedores, por meio daquele que nos amou."),
    ("2 Coríntios 5:17", "Se alguém está em Cristo, é nova criação. As coisas antigas já passaram; eis que tudo se tornou novo!"),
    ("Efésios 2:8", "Porque pela graça sois salvos, por meio da fé; e isso não vem de vós; é dom de Deus."),
    ("Gálatas 5:22", "O fruto do Espírito é: amor, alegria, paz, longanimidade, benignidade, bondade, fidelidade, mansidão, domínio próprio."),
    ("Josué 1:9", "Não to mandei eu? Sê forte e corajoso! Não te atemorizes nem te apavores, porque o Senhor, teu Deus, é contigo em todos os lugares para onde fores."),
    ("1 Coríntios 13:4", "O amor é paciente, é benigno; o amor não arde em ciúmes, não se ostenta orgulhoso, não se conduz inconvenientemente."),
    ("Mateus 11:28", "Vinde a mim, todos os que estais cansados e sobrecarregados, e eu vos darei descanso."),
    ("Salmos 119:105", "Lâmpada para os meus pés é a tua palavra e luz para o meu caminho."),
    ("Apocalipse 21:4", "E Deus limpará de seus olhos toda lágrima, e não haverá mais morte, nem pranto, nem lamento, nem dor."),
    ("Tiago 1:2-3", "Meus irmãos, tende por motivo de toda alegria quando experimentardes várias provações, sabendo que a prova da vossa fé produz perseverança."),
    ("1 Pedro 5:7", "Lançai sobre ele toda a vossa ansiedade, porque ele tem cuidado de vós."),
    ("Mateus 5:9", "Bem-aventurados os pacificadores, pois eles serão chamados filhos de Deus."),
    ("Salmos 37:4", "Deleita-te também no Senhor, e ele te concederá os desejos do teu coração."),
    ("Números 6:24-26", "O Senhor te abençoe e te guarde; o Senhor faça resplandecer o seu rosto sobre ti e tenha misericórdia de ti; o Senhor sobre ti levante o seu rosto e te dê a paz."),
    ("2 Timóteo 1:7", "Porque Deus não nos deu espírito de covardia, mas de poder, de amor e de moderação."),
    ("João 15:5", "Eu sou a videira, vós sois os ramos. Quem permanece em mim e eu nele, esse dá muito fruto."),
    ("Romanos 10:9", "Se com a tua boca confessares Jesus como Senhor e em teu coração creres que Deus o ressuscitou dentre os mortos, serás salvo."),
    ("Efésios 3:20", "Ora, àquele que é poderoso para fazer infinitamente mais do que tudo quanto pedimos ou pensamos, conforme o seu poder que opera em nós."),
    ("Salmos 27:1", "O Senhor é a minha luz e a minha salvação; a quem temerei? O Senhor é a força da minha vida; de quem me recearei?"),
]

CORES_GRADIENTE = [
    ((41, 128, 185), (109, 213, 237)),
    ((142, 68, 173), (228, 122, 161)),
    ((39, 174, 96), (109, 213, 170)),
    ((231, 76, 60), (243, 156, 18)),
    ((44, 62, 80), (52, 152, 219)),
    ((22, 160, 133), (46, 204, 113)),
    ((155, 89, 182), (52, 152, 219)),
]

def get_versiculo_texto():
    ref, texto = random.choice(VERSICULOS)
    return ref, texto

def get_saudacao():
    hora = datetime.now().hour
    if hora < 12:
        return "🌅 Bom dia, família!"
    elif hora < 18:
        return "☀️ Boa tarde, família!"
    else:
        return "🌙 Boa noite, família!"

def gerar_imagem_versiculo():
    try:
        from PIL import Image, ImageDraw, ImageFont
        import textwrap

        ref, texto = get_versiculo_texto()

        cor1, cor2 = random.choice(CORES_GRADIENTE)
        largura, altura = 1080, 1080
        img = Image.new("RGB", (largura, altura))
        draw = ImageDraw.Draw(img)

        for y in range(altura):
            ratio = y / altura
            r = int(cor1[0] + (cor2[0] - cor1[0]) * ratio)
            g = int(cor1[1] + (cor2[1] - cor1[1]) * ratio)
            b = int(cor1[2] + (cor2[2] - cor1[2]) * ratio)
            draw.line([(0, y), (largura, y)], fill=(r, g, b))

        overlay = Image.new("RGBA", (largura, altura), (0, 0, 0, 80))
        img = img.convert("RGBA")
        img = Image.alpha_composite(img, overlay)
        img = img.convert("RGB")
        draw = ImageDraw.Draw(img)

        try:
            font_titulo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
            font_texto = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
            font_ref = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
            font_marca = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            font_titulo = ImageFont.load_default()
            font_texto = ImageFont.load_default()
            font_ref = ImageFont.load_default()
            font_marca = ImageFont.load_default()

        draw.rectangle([(60, 60), (largura-60, altura-60)], outline=(255, 255, 255, 150), width=3)

        titulo = "🔥  Avivamento AD  🔥"
        bbox = draw.textbbox((0, 0), titulo, font=font_titulo)
        w = bbox[2] - bbox[0]
        draw.text(((largura - w) / 2, 110), titulo, font=font_titulo, fill=(255, 255, 255))

        draw.line([(150, 190), (largura-150, 190)], fill=(255, 255, 255, 180), width=2)

        linhas = textwrap.wrap(f'"{texto}"', width=32)
        y_texto = 240
        for linha in linhas:
            bbox = draw.textbbox((0, 0), linha, font=font_texto)
            w = bbox[2] - bbox[0]
            draw.text(((largura - w) / 2, y_texto), linha, font=font_texto, fill=(255, 255, 255))
            y_texto += 55

        draw.line([(150, y_texto + 20), (largura-150, y_texto + 20)], fill=(255, 255, 255, 180), width=2)

        bbox = draw.textbbox((0, 0), f"— {ref}", font=font_ref)
        w = bbox[2] - bbox[0]
        draw.text(((largura - w) / 2, y_texto + 45), f"— {ref}", font=font_ref, fill=(255, 255, 220))

        marca = "🕊️  Palavra de Vida  🕊️"
        bbox = draw.textbbox((0, 0), marca, font=font_marca)
        w = bbox[2] - bbox[0]
        draw.text(((largura - w) / 2, altura - 130), marca, font=font_marca, fill=(255, 255, 255, 200))

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95)
        buf.seek(0)
        return buf, ref, texto

    except Exception as e:
        logger.error(f"Erro ao gerar imagem: {e}")
        ref, texto = get_versiculo_texto()
        buf = _gerar_imagem_simples(ref, texto)
        return buf, ref, texto

def _gerar_imagem_simples(ref: str, texto: str) -> io.BytesIO:
    try:
        from PIL import Image, ImageDraw, ImageFont
        import textwrap
        img = Image.new("RGB", (800, 600), color=(41, 128, 185))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
            font_ref = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
        except:
            font = ImageFont.load_default()
            font_ref = ImageFont.load_default()
        linhas = textwrap.wrap(f'"{texto}"', width=40)
        y = 100
        for linha in linhas:
            draw.text((50, y), linha, font=font, fill=(255, 255, 255))
            y += 45
        draw.text((50, y + 20), f"— {ref}", font=font_ref, fill=(255, 255, 200))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
        buf.seek(0)
        return buf
    except Exception as e:
        logger.error(f"Erro ao gerar imagem simples: {e}")
        buf = io.BytesIO(b"")
        return buf
