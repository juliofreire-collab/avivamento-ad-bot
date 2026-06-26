import logging
from datetime import datetime
from database import db

logger = logging.getLogger(__name__)

ORACOES_DO_DIA = [
    "🙏 *ORAÇÃO DA MANHÃ*\n\nPai Celestial, obrigado por mais um dia de vida!\nQue Tua presença nos guie em cada passo.\nGuarda-nos de todo mal e enche nossos corações de paz.\n\n_\"Esta é a manhã que o Senhor fez; regozijemo-nos e alegremo-nos nela.\"_ — Salmos 118:24",
    "🌅 *ORAÇÃO DO AMANHECER*\n\nSenhor, ao despertar confio meu dia em Tuas mãos.\nSeja Tu a luz que ilumina meu caminho.\nQue eu seja instrumento do Teu amor hoje.\n\n_\"As misericórdias do Senhor não têm fim; as suas bondades nunca cessam.\"_ — Lamentações 3:22",
    "🌙 *ORAÇÃO DA NOITE*\n\nSenhor, obrigado por mais um dia de bênçãos.\nCobre-nos com Teu manto protetor enquanto descansamos.\nQue amanhã acordemos renovados em Tua graça.\n\n_\"Em paz me deito e logo adormeço, porque só Tu, ó Senhor, me fazes habitar em segurança.\"_ — Salmos 4:8",
    "☀️ *ORAÇÃO DA TARDE*\n\nPai, no meio deste dia venho a Ti.\nRenova minhas forças e minha fé.\nQue Tua Palavra seja lâmpada aos meus pés.\n\n_\"O Senhor é o meu pastor e nada me faltará.\"_ — Salmos 23:1",
    "🕊️ *ORAÇÃO PELA FAMÍLIA*\n\nSenhor, abençoa cada família representada aqui.\nProtege nossas casas e fortalece nossos laços.\nQue o amor de Cristo habite em cada lar.\n\n_\"Quanto a mim e à minha casa, serviremos ao Senhor.\"_ — Josué 24:15",
    "💪 *ORAÇÃO DE FORÇA*\n\nDeus poderoso, em Ti encontro minha força.\nNos momentos de fraqueza, sou forte em Cristo.\nNão me desampares, Senhor, pois em Ti confio.\n\n_\"Tudo posso naquele que me fortalece.\"_ — Filipenses 4:13",
    "🌟 *ORAÇÃO DE GRATIDÃO*\n\nPai, meu coração transborda de gratidão.\nObrigado pelas bênçãos visíveis e invisíveis.\nQue eu nunca esqueça da Tua bondade em minha vida.\n\n_\"Em tudo dai graças, porque esta é a vontade de Deus.\"_ — 1 Tessalonicenses 5:18",
]

DEVOCIONAIS = [
    {
        "titulo": "A Fé que Move Montanhas",
        "texto": (
            "📖 *Mateus 17:20* — _\"Se tiverdes fé como um grão de mostarda, direis a este monte: Passa daqui para lá, e ele passará; e nada vos será impossível.\"_\n\n"
            "A fé não precisa ser perfeita para ser poderosa. Ela precisa estar depositada no Deus perfeito.\n\n"
            "Hoje, qual é a montanha na sua vida? Entregue-a ao Senhor. Com fé, mesmo pequena, Deus opera maravilhas!\n\n"
            "🙏 _Oração: Senhor, aumenta a minha fé e me ajuda a confiar em Ti mesmo quando não consigo ver o caminho._"
        )
    },
    {
        "titulo": "A Paz que Excede o Entendimento",
        "texto": (
            "📖 *Filipenses 4:7* — _\"A paz de Deus, que excede todo entendimento, guardará os vossos corações e as vossas mentes em Cristo Jesus.\"_\n\n"
            "Em um mundo cheio de ansiedade, Deus oferece uma paz sobrenatural.\n\n"
            "Essa paz não depende das circunstâncias — ela vem de saber que Deus está no controle de tudo.\n\n"
            "🙏 _Oração: Senhor, que Tua paz guarde meu coração hoje. Ajuda-me a descansar em Ti._"
        )
    },
    {
        "titulo": "Renove Suas Forças no Senhor",
        "texto": (
            "📖 *Isaías 40:31* — _\"Mas os que esperam no Senhor renovarão as suas forças; subirão com asas como águias; correrão e não se cansarão; caminharão e não se fatigarão.\"_\n\n"
            "Quando nos sentimos esgotados, o Senhor é nossa fonte de renovação.\n\n"
            "Não tente carregar o fardo sozinho. Venha ao Senhor e encontre descanso para sua alma.\n\n"
            "🙏 _Oração: Renova minhas forças hoje, Senhor. Que eu voe como águia sobre cada desafio._"
        )
    },
    {
        "titulo": "Planos de Prosperidade",
        "texto": (
            "📖 *Jeremias 29:11* — _\"Porque sou eu que conheço os planos que tenho para vocês, diz o Senhor, planos de fazê-los prosperar e não de causar dano, planos de dar a vocês esperança e um futuro.\"_\n\n"
            "Deus tem um plano específico para a sua vida — um plano de esperança e futuro!\n\n"
            "Mesmo quando não entendemos o presente, podemos confiar no Deus que conhece o amanhã.\n\n"
            "🙏 _Oração: Senhor, confio nos Teus planos para minha vida. Guia-me pelo Teu caminho perfeito._"
        )
    },
    {
        "titulo": "O Amor de Deus é Incondicional",
        "texto": (
            "📖 *João 3:16* — _\"Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna.\"_\n\n"
            "O maior ato de amor da história: Deus enviou Seu filho para nos salvar.\n\n"
            "Nada pode separar-nos do amor de Deus — nem altura, nem profundidade, nem nenhuma outra criatura.\n\n"
            "🙏 _Oração: Obrigado, Pai, pelo Teu amor incondicional. Que eu reflita esse amor em tudo que faço._"
        )
    },
    {
        "titulo": "Deus é Nosso Refúgio",
        "texto": (
            "📖 *Salmos 46:1* — _\"Deus é o nosso refúgio e fortaleza, socorro bem presente na angústia.\"_\n\n"
            "Não importa o tamanho da tempestade — Deus é maior!\n\n"
            "Quando o mundo ao redor parece desabar, corra para o refúgio seguro nos braços do Pai.\n\n"
            "🙏 _Oração: Senhor, Tu és meu refúgio. Em Ti encontro segurança e paz em meio às tempestades._"
        )
    },
    {
        "titulo": "Gratidão Transforma o Coração",
        "texto": (
            "📖 *1 Tessalonicenses 5:18* — _\"Em tudo dai graças, porque esta é a vontade de Deus em Cristo Jesus para convosco.\"_\n\n"
            "A gratidão não espera as circunstâncias perfeitas — ela é uma escolha diária!\n\n"
            "Quando somos gratos, nosso coração se abre para receber ainda mais bênçãos de Deus.\n\n"
            "🙏 _Oração: Pai, obrigado por todas as bênçãos em minha vida. Que eu seja sempre grato(a)._"
        )
    },
    {
        "titulo": "O Poder da Oração",
        "texto": (
            "📖 *Tiago 5:16* — _\"Orai uns pelos outros para serdes curados. A oração eficaz do justo pode muito.\"_\n\n"
            "A oração é a linha direta com Deus — use-a sempre!\n\n"
            "Quando oramos uns pelos outros, Deus age de maneiras poderosas. A intercessão é um ato de amor.\n\n"
            "🙏 _Oração: Senhor, ensina-me a orar com fé e perseverança. Que minhas orações movam o Teu coração._"
        )
    },
]

PERGUNTAS_ENGAJAMENTO = [
    "🌟 *PERGUNTA DO DIA*\n\nQual versículo bíblico tem sido mais especial para você nesta semana? Compartilhe! 📖\n\n_\"A tua palavra é lâmpada que ilumina os meus passos.\"_ — Salmos 119:105",
    "🙏 *REFLITA E COMPARTILHE*\n\nComo você começa seu dia com Deus? Tem alguma prática de devoção que gostaria de compartilhar com a família? ✝️",
    "💪 *TESTEMUNHO DO DIA*\n\nQue tal compartilhar uma situação em que viu a mão de Deus agir na sua vida? Encoraje nossos irmãos! 🌟",
    "📖 *ESTUDO DA PALAVRA*\n\nQual livro da Bíblia você está lendo agora? O que Deus tem falado ao seu coração através dele? 🕊️",
    "🎵 *LOUVOR E ADORAÇÃO*\n\nQual música gospel tem ministrado mais ao seu coração ultimamente? Compartilhe o nome! 🎶",
    "🌅 *BOM DIA, FAMÍLIA!*\n\nQuem aqui já fez sua oração de manhã? Vamos começar este dia juntos na presença do Senhor! 🙏\n\n_\"Esta é a manhã que o Senhor fez!\"_ — Salmos 118:24",
    "✝️ *PALAVRA DE FÉ*\n\nQual promessa de Deus você está crendo hoje? Declare aqui para fortalecer sua fé e a dos irmãos! 💪",
    "🤝 *COMUNHÃO*\n\nO que você mais aprecia em fazer parte desta família espiritual? Compartilhe! 🕊️",
    "🌟 *ORAÇÃO COLETIVA*\n\nVamos fazer um mural de gratidão! Escreva aqui: _Hoje sou grato(a) por..._ 🙏",
    "📢 *DESAFIO DO DIA*\n\nHoje, faça uma gentileza para alguém e volte aqui para contar! _\"Sede bons uns para com os outros.\"_ — Efésios 4:32 💙",
]

def salvar_pedido(nome: str, user_id: int, pedido: str):
    try:
        with db() as cur:
            cur.execute("""
                INSERT INTO oracao (nome, user_id, pedido, data, orado)
                VALUES (%s, %s, %s, %s, FALSE)
            """, (nome, user_id, pedido, datetime.now().strftime("%d/%m/%Y %H:%M")))
    except Exception as e:
        logger.error(f"Erro ao salvar pedido: {e}")

def get_pedidos_pendentes():
    try:
        with db() as cur:
            cur.execute("""
                SELECT nome, pedido, data FROM oracao
                WHERE orado = FALSE
                ORDER BY id DESC LIMIT 20
            """)
            return [dict(r) for r in cur.fetchall()]
    except Exception as e:
        logger.error(f"Erro ao buscar pedidos: {e}")
        return []
