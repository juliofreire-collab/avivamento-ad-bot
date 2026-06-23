import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORACAO_FILE = os.path.join(_BASE_DIR, "pedidos_oracao.json")

ORACOES_DO_DIA = [
    """🙏 *ORAÇÃO DA MANHÃ*

Senhor, neste novo dia que Tu nos concedes,
renovamos nossa fé e confiança em Ti.
Que Tua presença nos guie em cada passo,
que Teu amor nos fortaleça em cada momento.

Guarda nossas famílias, abençoa nossos projetos,
e que possamos ser instrumentos do Teu amor
onde quer que formos.

Em nome de Jesus, Amém! 🕊️""",

    """🌅 *ORAÇÃO PELA FAMÍLIA*

Pai Celestial, abençoa cada família representada aqui.
Que o amor de Cristo habite em nossos lares,
que a paz que excede todo entendimento
guarde nossos corações e mentes.

Protege nossos filhos, renova nossos casamentos,
e que cada lar seja um reflexo do Teu amor.

Em nome de Jesus, Amém! 🕊️""",

    """⚔️ *ORAÇÃO DE GUERRA ESPIRITUAL*

Senhor, vestimo-nos hoje da armadura de Deus!
Cingimos os lombos com a verdade,
colocamos a couraça da justiça,
calçamos os pés com o evangelho da paz.

Tomamos o escudo da fé, o capacete da salvação
e a espada do Espírito, que é a Palavra de Deus.

Somos mais do que vencedores em Cristo Jesus!
Em nome de Jesus, Amém! 🕊️""",

    """🌙 *ORAÇÃO DA NOITE*

Pai amoroso, encerramos mais um dia
confiando em Tua proteção.
Guarda nosso sono, afasta todo mal,
que os anjos acampem ao redor de nós.

Obrigado por mais um dia de vida,
por cada benção recebida,
por cada teste que nos fortaleceu.

Que possamos repousar em paz.
Em nome de Jesus, Amém! 🕊️""",

    """💪 *ORAÇÃO PELA SAÚDE*

Jesus, o Grande Médico,
estendemos nossas mãos a Ti pedindo cura.
Para cada irmão(ã) que enfrenta doenças,
que Tua cura se manifeste poderosamente.

Tu és o mesmo ontem, hoje e eternamente.
Os milagres de cura não cessaram!
Toca em cada corpo enfermo, restaura, cura, liberta!

Em nome de Jesus, Amém! 🕊️""",

    """🌈 *ORAÇÃO PELA PROSPERIDADE*

Senhor, Tu prometiste abrir as janelas dos céus
e derramar bênçãos sem medida.
Que esta semana seja marcada por Teu favor,
que as portas certas se abram, os negócios prosperem.

Mas acima de tudo, que busquemos primeiro o Teu reino,
e que todas as demais coisas nos sejam acrescentadas.

Em nome de Jesus, Amém! 🕊️""",
]

DEVOCIONAIS = [
    {
        "titulo": "🌅 DEVOCIONAL — A Graça que Sustenta",
        "texto": (
            "📖 *Lamentações 3:22-23*\n"
            "_\"As misericórdias do Senhor são a causa de não sermos consumidos, "
            "porque as suas misericórdias não têm fim. Renovam-se cada manhã. "
            "Grande é a tua fidelidade.\"_\n\n"
            "✍️ *Reflexão:*\nCada manhã é uma nova oportunidade que Deus nos concede. "
            "Suas misericórdias se renovam todos os dias — não importa o que aconteceu ontem. "
            "Você está aqui hoje porque a graça de Deus sustentou você até este momento.\n\n"
            "🎯 *Aplicação prática:*\nAntes de começar suas atividades hoje, "
            "pare por 5 minutos e agradeça a Deus por mais um dia de vida. "
            "Declare: _\"Hoje é um dia de graça e bênção!\"_\n\n"
            "🙏 _Que Deus abençoe seu dia!_"
        )
    },
    {
        "titulo": "☀️ DEVOCIONAL — Fé em Ação",
        "texto": (
            "📖 *Tiago 2:17*\n"
            "_\"Assim também a fé, se não tiver obras, é morta em si mesma.\"_\n\n"
            "✍️ *Reflexão:*\nA fé verdadeira se manifesta em ações. "
            "Não basta apenas acreditar — precisamos agir sobre aquilo em que cremos. "
            "Quando Noé construiu a arca, quando Abraão saiu sem saber para onde ia, "
            "eles demonstraram fé em ação.\n\n"
            "🎯 *Aplicação prática:*\nQual é aquela área da sua vida onde você precisa "
            "parar de apenas orar e começar a agir com fé? "
            "Dê o primeiro passo hoje!\n\n"
            "🙏 _Que Deus dirija seus passos!_"
        )
    },
    {
        "titulo": "🌙 DEVOCIONAL — Paz que Excede",
        "texto": (
            "📖 *Filipenses 4:6-7*\n"
            "_\"Não andeis ansiosos por coisa alguma; antes em tudo, mediante oração "
            "e súplica, com ação de graças, sejam os vossos pedidos conhecidos diante de Deus. "
            "E a paz de Deus, que excede todo o entendimento, guardará os vossos corações "
            "e os vossos pensamentos em Cristo Jesus.\"_\n\n"
            "✍️ *Reflexão:*\nA ansiedade é uma das maiores batalhas do nosso tempo. "
            "Mas Deus tem uma resposta: oração + ação de graças = paz sobrenatural. "
            "Não uma paz que depende das circunstâncias, mas que as transcende!\n\n"
            "🎯 *Aplicação prática:*\nEscreva 3 coisas pelas quais você é grato hoje. "
            "Entregue suas preocupações a Deus em oração e receba a paz que excede todo entendimento.\n\n"
            "🙏 _Que a paz de Deus guarde seu coração!_"
        )
    },
    {
        "titulo": "🔥 DEVOCIONAL — Avivamento Interior",
        "texto": (
            "📖 *2 Crônicas 7:14*\n"
            "_\"Se o meu povo, que se chama pelo meu nome, se humilhar, e orar, "
            "e buscar a minha face, e se converter dos seus maus caminhos, então eu ouvirei "
            "dos céus, e perdoarei os seus pecados, e sararei a sua terra.\"_\n\n"
            "✍️ *Reflexão:*\nO avivamento começa dentro de cada um de nós. "
            "Não é um evento externo — é uma decisão de humilhação, oração e busca sincera a Deus. "
            "Quando nos rendemos completamente a Ele, o fogo do Espírito Santo nos consome!\n\n"
            "🎯 *Aplicação prática:*\nDedique hoje pelo menos 15 minutos em silêncio diante de Deus. "
            "Sem distrações. Apenas você e o Espírito Santo.\n\n"
            "🙏 _Que o fogo do avivamento arda em você!_ 🔥"
        )
    },
    {
        "titulo": "💎 DEVOCIONAL — Identidade em Cristo",
        "texto": (
            "📖 *2 Coríntios 5:17*\n"
            "_\"Se alguém está em Cristo, é nova criatura; as coisas antigas já passaram; "
            "eis que tudo se fez novo.\"_\n\n"
            "✍️ *Reflexão:*\nVocê não é definido pelo seu passado, pelos seus erros, "
            "pelas palavras que falaram sobre você. Em Cristo, você é uma nova criatura! "
            "Sua identidade está nEle, não nas circunstâncias.\n\n"
            "🎯 *Aplicação prática:*\nDeclare em voz alta hoje: "
            "_\"Eu sou filho(a) de Deus, sou amado(a), sou aceito(a), sou nova criatura em Cristo!\"_ "
            "Deixe essa verdade transformar sua mente hoje.\n\n"
            "🙏 _Que você viva plenamente sua identidade em Cristo!_"
        )
    },
]

PERGUNTAS_ENGAJAMENTO = [
    "🤔 *REFLEXÃO DO DIA*\n\nQual versículo da Bíblia mais impactou sua vida e por quê? Compartilhe conosco! 👇",
    "💬 *PERGUNTA DE FÉ*\n\nComo Deus respondeu uma oração sua recentemente? Dê um testemunho! Vai abençoar a todos! 🙏",
    "🌟 *COMPARTILHE!*\n\nQual é o maior milagre que você já presenciou ou viveu? Vamos glorificar a Deus juntos! ✝️",
    "🙏 *HORA DO TESTEMUNHO*\n\nComo foi sua semana na fé? Teve alguma vitória para compartilhar? 💪",
    "📖 *ESTUDO BÍBLICO*\n\nQual livro da Bíblia você está lendo agora? O que Deus tem falado ao seu coração? 📚",
    "❤️ *AMOR AO PRÓXIMO*\n\nComo você pode ajudar alguém hoje com o amor de Cristo? Compartilhe uma ideia! 🕊️",
    "🔥 *AVIVAMENTO*\n\nO que avivamento significa para você? Como você busca ser avivado(a) espiritualmente? ✨",
    "🌅 *BOM DIA NA FÉ!*\n\nComeçando mais um dia com Deus! Como estão seus deveres devocionais? Tem orado todo dia? 📖",
]


def carregar_pedidos():
    if os.path.exists(ORACAO_FILE):
        try:
            with open(ORACAO_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []

def salvar_pedido(user_name: str, user_id: int, pedido: str):
    pedidos = carregar_pedidos()
    pedidos.append({
        "nome": user_name,
        "user_id": user_id,
        "pedido": pedido,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "orado": False
    })
    with open(ORACAO_FILE, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, ensure_ascii=False, indent=2)

def get_pedidos_pendentes():
    return [p for p in carregar_pedidos() if not p.get("orado")]
