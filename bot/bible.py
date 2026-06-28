import random
import io
import os
import logging
import subprocess
from datetime import datetime

logger = logging.getLogger(__name__)

# ── Caminho do logo AD ───────────────────────────────────────────────────────
_LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ad_logo.png")

# ── Helpers de fonte ─────────────────────────────────────────────────────────
def _encontrar_fonte(nome_arquivo: str) -> str | None:
    candidatos = [
        f"/usr/share/fonts/truetype/dejavu/{nome_arquivo}",
        f"/usr/share/fonts/truetype/DejaVu/{nome_arquivo}",
        f"/usr/share/fonts/dejavu/{nome_arquivo}",
        f"/usr/local/share/fonts/{nome_arquivo}",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", nome_arquivo),
    ]
    try:
        familia = "DejaVu Sans:style=Bold" if "Bold" in nome_arquivo else "DejaVu Sans:style=Book"
        resultado = subprocess.run(
            ["fc-list", f":{familia}", "--format=%{{file}}\n"],
            capture_output=True, text=True, timeout=5,
        )
        for linha in resultado.stdout.strip().split("\n"):
            linha = linha.strip()
            if linha and os.path.exists(linha):
                candidatos.insert(0, linha)
    except Exception:
        pass
    for path in candidatos:
        if path and os.path.exists(path):
            return path
    return None

def _carregar_fonte(path: str | None, tamanho: int):
    from PIL import ImageFont
    if path:
        try:
            return ImageFont.truetype(path, tamanho)
        except Exception:
            pass
    return ImageFont.load_default()

# ── Dados ────────────────────────────────────────────────────────────────────
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

# ── Fonte adaptativa ─────────────────────────────────────────────────────────
def _calcular_layout_texto(texto_completo: str, bold_path, regular_path,
                            largura_max: int, altura_max: int):
    """
    Escolhe o maior tamanho de fonte que faz o texto caber em altura_max.
    Retorna (font_texto, font_ref, linhas, line_h).
    """
    import textwrap
    from PIL import ImageFont, ImageDraw, Image

    # Configurações candidatas: (font_size, chars_por_linha, line_height)
    configs = [
        (62, 22, 80),
        (54, 24, 72),
        (46, 28, 62),
        (40, 32, 55),
        (35, 36, 50),
        (30, 40, 45),
    ]

    # Imagem temporária para medir textbbox
    tmp = Image.new("RGB", (largura_max, altura_max))
    draw_tmp = ImageDraw.Draw(tmp)

    for font_size, chars, line_h in configs:
        font_t = _carregar_fonte(regular_path, font_size)
        linhas = textwrap.wrap(f'"{texto_completo}"', width=chars)
        total_h = len(linhas) * line_h
        if total_h <= altura_max:
            font_r = _carregar_fonte(bold_path, max(font_size - 4, 28))
            return font_t, font_r, linhas, line_h

    # fallback mínimo
    font_t = _carregar_fonte(regular_path, 28)
    font_r = _carregar_fonte(bold_path, 26)
    linhas = textwrap.wrap(f'"{texto_completo}"', width=44)
    return font_t, font_r, linhas, 42


def gerar_imagem_versiculo():
    try:
        from PIL import Image, ImageDraw, ImageFont
        import textwrap

        ref, texto = get_versiculo_texto()

        cor1, cor2 = random.choice(CORES_GRADIENTE)
        W, H = 1080, 1080
        img = Image.new("RGB", (W, H))
        draw = ImageDraw.Draw(img)

        # ── Gradiente de fundo ───────────────────────────────────────────
        for y in range(H):
            ratio = y / H
            r = int(cor1[0] + (cor2[0] - cor1[0]) * ratio)
            g = int(cor1[1] + (cor2[1] - cor1[1]) * ratio)
            b = int(cor1[2] + (cor2[2] - cor1[2]) * ratio)
            draw.line([(0, y), (W, y)], fill=(r, g, b))

        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 70))
        img = img.convert("RGBA")
        img = Image.alpha_composite(img, overlay)
        img = img.convert("RGB")
        draw = ImageDraw.Draw(img)

        # ── Borda ────────────────────────────────────────────────────────
        draw.rectangle([(55, 55), (W - 55, H - 55)], outline=(255, 255, 255), width=3)

        # ── Logo da Assembleia de Deus ───────────────────────────────────
        LOGO_H = 290          # altura reservada para o logo na imagem
        logo_y_start = 72

        if os.path.exists(_LOGO_PATH):
            logo = Image.open(_LOGO_PATH).convert("RGBA")
            # Redimensionar mantendo proporção para caber em LOGO_H
            logo_w_orig, logo_h_orig = logo.size
            scale = LOGO_H / logo_h_orig
            logo_w = int(logo_w_orig * scale)
            logo = logo.resize((logo_w, LOGO_H), Image.LANCZOS)
            # Colar centralizado
            paste_x = (W - logo_w) // 2
            img_rgba = img.convert("RGBA")
            img_rgba.paste(logo, (paste_x, logo_y_start), logo)
            img = img_rgba.convert("RGB")
            draw = ImageDraw.Draw(img)
        else:
            # Fallback: texto se logo não encontrado
            bold_path_fb = _encontrar_fonte("DejaVuSans-Bold.ttf")
            fb_font = _carregar_fonte(bold_path_fb, 38)
            draw.text((W // 2, logo_y_start + LOGO_H // 2), "Assembleia de Deus",
                      font=fb_font, fill=(255, 225, 100), anchor="mm")

        # ── Separador após logo ──────────────────────────────────────────
        sep1_y = logo_y_start + LOGO_H + 16
        draw.line([(100, sep1_y), (W - 100, sep1_y)], fill=(255, 255, 255), width=2)

        # ── Área de texto disponível ─────────────────────────────────────
        BOTTOM_RESERVE = 130   # espaço para referência + rodapé + separador
        texto_y_start = sep1_y + 22
        texto_y_end   = H - 55 - BOTTOM_RESERVE
        texto_area_h  = texto_y_end - texto_y_start   # pixels disponíveis

        # ── Fontes adaptativas ───────────────────────────────────────────
        bold_path    = _encontrar_fonte("DejaVuSans-Bold.ttf")
        regular_path = _encontrar_fonte("DejaVuSans.ttf")

        font_verso, font_ref, linhas, line_h = _calcular_layout_texto(
            texto, bold_path, regular_path,
            W - 140, texto_area_h
        )
        font_rodape = _carregar_fonte(regular_path, 28)

        # Centralizar bloco de texto verticalmente no espaço disponível
        bloco_h = len(linhas) * line_h
        y_offset = texto_y_start + max(0, (texto_area_h - bloco_h) // 2)

        # ── Versículo ────────────────────────────────────────────────────
        for linha in linhas:
            bbox = draw.textbbox((0, 0), linha, font=font_verso)
            w = bbox[2] - bbox[0]
            draw.text(((W - w) / 2, y_offset), linha, font=font_verso, fill=(255, 255, 255))
            y_offset += line_h

        # ── Separador antes da referência ────────────────────────────────
        sep2_y = H - 55 - BOTTOM_RESERVE + 10
        draw.line([(100, sep2_y), (W - 100, sep2_y)], fill=(255, 255, 255), width=2)

        # ── Referência bíblica ───────────────────────────────────────────
        ref_text = f"— {ref}"
        bbox = draw.textbbox((0, 0), ref_text, font=font_ref)
        w = bbox[2] - bbox[0]
        draw.text(((W - w) / 2, sep2_y + 18), ref_text, font=font_ref, fill=(255, 255, 180))

        # ── Rodapé ───────────────────────────────────────────────────────
        rodape = "Avivamento AD  |  Palavra de Vida"
        bbox = draw.textbbox((0, 0), rodape, font=font_rodape)
        w = bbox[2] - bbox[0]
        draw.text(((W - w) / 2, H - 55 - 42), rodape, font=font_rodape, fill=(220, 220, 255))

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
        from PIL import Image, ImageDraw
        import textwrap
        W, H = 800, 600
        img = Image.new("RGB", (W, H), color=(41, 128, 185))
        draw = ImageDraw.Draw(img)
        bold_path = _encontrar_fonte("DejaVuSans-Bold.ttf")
        regular_path = _encontrar_fonte("DejaVuSans.ttf")
        font = _carregar_fonte(regular_path, 30)
        font_ref = _carregar_fonte(bold_path, 34)

        if os.path.exists(_LOGO_PATH):
            from PIL import Image as PILImage
            logo = PILImage.open(_LOGO_PATH).convert("RGBA")
            logo = logo.resize((140, 140), PILImage.LANCZOS)
            img_rgba = img.convert("RGBA")
            img_rgba.paste(logo, ((W - 140) // 2, 20), logo)
            img = img_rgba.convert("RGB")
            draw = ImageDraw.Draw(img)

        linhas = textwrap.wrap(f'"{texto}"', width=40)
        y = 175
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
        return io.BytesIO(b"")
