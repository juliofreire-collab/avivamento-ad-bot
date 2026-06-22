import random
from PIL import Image, ImageDraw, ImageFont
import io
import os
import textwrap

VERSICULOS = [
    ("João 3:16", "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna."),
    ("Salmos 23:1", "O SENHOR é o meu pastor; nada me faltará."),
    ("Filipenses 4:13", "Posso todas as coisas em Cristo que me fortalece."),
    ("Jeremias 29:11", "Porque eu sei os planos que tenho para vocês, diz o SENHOR, planos de fazê-los prosperar e não de lhes causar dano, planos de dar a vocês esperança e um futuro."),
    ("Isaías 41:10", "Não temas, porque eu sou contigo; não te assombres, porque eu sou o teu Deus; eu te fortaleço, e te ajudo, e te sustento com a minha destra fiel."),
    ("Romanos 8:28", "Sabemos que todas as coisas cooperam para o bem daqueles que amam a Deus, daqueles que são chamados segundo o seu propósito."),
    ("Salmos 46:1", "Deus é o nosso refúgio e força, socorro bem presente na angústia."),
    ("Provérbios 3:5-6", "Confia no SENHOR de todo o teu coração e não te estribes no teu próprio entendimento. Reconhece-o em todos os teus caminhos, e ele endireitará as tuas veredas."),
    ("Mateus 11:28", "Vinde a mim, todos os que estais cansados e sobrecarregados, e eu vos darei descanso."),
    ("Salmos 27:1", "O SENHOR é a minha luz e a minha salvação; a quem temerei? O SENHOR é a força da minha vida; de quem me recearei?"),
    ("2 Coríntios 5:7", "Porque andamos por fé e não por vista."),
    ("Josué 1:9", "Não to mandei eu? Esforça-te e tem bom ânimo; não temas, nem te espantes; porque o SENHOR teu Deus é contigo por onde quer que andares."),
    ("Salmos 91:1", "Aquele que habita no esconderijo do Altíssimo, à sombra do Onipotente descansará."),
    ("Gálatas 6:9", "Não nos cansemos de fazer o bem, porque a seu tempo ceifaremos, se não desfalecermos."),
    ("1 João 4:8", "Aquele que não ama não conhece a Deus, porque Deus é amor."),
    ("Efésios 2:8", "Porque pela graça sois salvos, por meio da fé; e isso não vem de vós; é dom de Deus."),
    ("Salmos 34:18", "Perto está o SENHOR dos que têm o coração quebrantado, e salva os de espírito abatido."),
    ("Romanos 12:2", "E não sede conformados com este século, mas sede transformados pela renovação do vosso entendimento."),
    ("Marcos 11:24", "Por isso vos digo que tudo o que pedirdes, orando, crede que o recebereis, e tê-lo-eis."),
    ("Mateus 5:8", "Bem-aventurados os limpos de coração, porque eles verão a Deus."),
    ("Salmos 37:4", "Deleita-te também no SENHOR, e ele te concederá os desejos do teu coração."),
    ("Hebreus 11:1", "Ora, a fé é o firme fundamento das coisas que se esperam e a prova das coisas que se não veem."),
    ("1 Coríntios 13:4", "O amor é paciente, o amor é bondoso. Não inveja, não se vangloria, não se orgulha."),
    ("Apocalipse 21:4", "E Deus limpará de seus olhos toda a lágrima, e não haverá mais morte, nem pranto, nem clamor, nem dor."),
    ("Salmos 119:105", "Lâmpada para os meus pés é a tua palavra e luz para o meu caminho."),
    ("2 Timóteo 1:7", "Porque Deus não nos deu espírito de covardia, mas de poder, de amor e de moderação."),
    ("Mateus 6:33", "Buscai, pois, em primeiro lugar, o seu reino e a sua justiça, e todas as demais coisas vos serão acrescentadas."),
    ("Salmos 121:2", "O meu socorro vem do SENHOR, que fez o céu e a terra."),
    ("Isaías 40:31", "Mas os que esperam no SENHOR renovarão as suas forças. Voarão alto como águias; correrão e não se cansarão, caminharão e não se fatigarão."),
    ("1 Pedro 5:7", "Lançando sobre ele toda a vossa ansiedade, porque ele tem cuidado de vós."),
]

CORES_FUNDO = [
    [(44, 62, 80), (52, 152, 219)],
    [(26, 26, 46), (22, 160, 133)],
    [(44, 44, 84), (155, 89, 182)],
    [(30, 60, 80), (41, 128, 185)],
    [(60, 20, 20), (192, 57, 43)],
    [(20, 60, 40), (39, 174, 96)],
    [(80, 60, 0), (241, 196, 15)],
    [(20, 20, 60), (52, 73, 94)],
]

def get_saudacao():
    import datetime
    import pytz
    tz = pytz.timezone("America/Sao_Paulo")
    hora = datetime.datetime.now(tz).hour
    if 5 <= hora < 12:
        return "🌅 Bom dia!"
    elif 12 <= hora < 18:
        return "☀️ Boa tarde!"
    else:
        return "🌙 Boa noite!"

def gerar_imagem_versiculo():
    referencia, texto = random.choice(VERSICULOS)
    cores = random.choice(CORES_FUNDO)

    largura, altura = 1080, 1080
    img = Image.new("RGB", (largura, altura), cores[0])
    draw = ImageDraw.Draw(img)

    for i in range(altura):
        ratio = i / altura
        r = int(cores[0][0] + (cores[1][0] - cores[0][0]) * ratio)
        g = int(cores[0][1] + (cores[1][1] - cores[0][1]) * ratio)
        b = int(cores[0][2] + (cores[1][2] - cores[0][2]) * ratio)
        draw.line([(0, i), (largura, i)], fill=(r, g, b))

    for _ in range(8):
        x = random.randint(0, largura)
        y = random.randint(0, altura)
        r = random.randint(30, 120)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, 10) if hasattr(draw, 'ellipse') else (255,255,255))

    draw.rectangle([60, 60, largura-60, altura-60], outline=(255, 255, 255, 120), width=3)
    draw.rectangle([70, 70, largura-70, altura-70], outline=(255, 255, 255, 60), width=1)

    try:
        font_grande = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 52)
        font_texto = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 38)
        font_ref = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 42)
        font_pequena = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 28)
    except:
        font_grande = ImageFont.load_default()
        font_texto = font_grande
        font_ref = font_grande
        font_pequena = font_grande

    cruz = "✝"
    try:
        bbox = draw.textbbox((0, 0), cruz, font=font_grande)
        cw = bbox[2] - bbox[0]
        draw.text(((largura - cw) // 2, 120), cruz, font=font_grande, fill=(255, 255, 255))
    except:
        pass

    linhas = textwrap.wrap(texto, width=32)
    y_texto = 220
    espacamento = 55

    for linha in linhas:
        try:
            bbox = draw.textbbox((0, 0), linha, font=font_texto)
            lw = bbox[2] - bbox[0]
        except:
            lw = len(linha) * 20
        x = (largura - lw) // 2

        draw.text((x+2, y_texto+2), linha, font=font_texto, fill=(0, 0, 0, 100))
        draw.text((x, y_texto), linha, font=font_texto, fill=(255, 255, 255))
        y_texto += espacamento

    draw.line([200, y_texto + 20, largura - 200, y_texto + 20], fill=(255, 255, 255, 150), width=2)

    try:
        bbox = draw.textbbox((0, 0), referencia, font=font_ref)
        rw = bbox[2] - bbox[0]
    except:
        rw = len(referencia) * 25
    draw.text(((largura - rw) // 2 + 2, y_texto + 42), referencia, font=font_ref, fill=(0, 0, 0, 100))
    draw.text(((largura - rw) // 2, y_texto + 40), referencia, font=font_ref, fill=(255, 215, 0))

    rodape = "🕊️ Avivamento AD"
    try:
        bbox = draw.textbbox((0, 0), rodape, font=font_pequena)
        pw = bbox[2] - bbox[0]
    except:
        pw = len(rodape) * 14
    draw.text(((largura - pw) // 2, altura - 110), rodape, font=font_pequena, fill=(255, 255, 255, 200))

    buf = io.BytesIO()
    img.save(buf, format="PNG", quality=95)
    buf.seek(0)
    return buf, referencia, texto

def get_versiculo_texto():
    referencia, texto = random.choice(VERSICULOS)
    return referencia, texto
