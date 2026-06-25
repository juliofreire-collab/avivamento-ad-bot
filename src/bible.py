import random
from PIL import Image, ImageDraw, ImageFont
import io
import os
import textwrap

VERSICULOS = [
    # Genesis
    ("Gênesis 1:1", "No princípio criou Deus os céus e a terra."),
    ("Gênesis 1:27", "E criou Deus o homem à sua imagem; à imagem de Deus o criou; homem e mulher os criou."),
    ("Gênesis 2:24", "Portanto, deixará o homem o seu pai e a sua mãe, e se unirá à sua mulher, e serão ambos uma só carne."),
    ("Gênesis 12:2", "E far-te-ei uma grande nação, e abençoar-te-ei e engrandecerei o teu nome; e tu serás uma bênção."),
    ("Gênesis 15:6", "E creu ele no SENHOR, e isso lhe foi imputado por justiça."),
    ("Gênesis 28:15", "Porque estou contigo e te guardarei por onde quer que andares."),
    ("Gênesis 50:20", "Vós, na verdade, intentastes o mal contra mim, mas Deus o tornou em bem."),
    # Exodo
    ("Êxodo 14:14", "O SENHOR pelejará por vós, e vós vos calareis."),
    ("Êxodo 15:2", "O SENHOR é a minha força e o meu cântico, e ele é a minha salvação."),
    ("Êxodo 20:12", "Honra a teu pai e a tua mãe, para que os teus dias se prolonguem na terra."),
    # Deuteronomio
    ("Deuteronômio 6:4", "Ouve, ó Israel: O SENHOR nosso Deus é o único SENHOR."),
    ("Deuteronômio 7:9", "Sabe, pois, que o SENHOR teu Deus é o Deus fiel que guarda a aliança e a misericórdia até mil gerações."),
    ("Deuteronômio 28:6", "Bendito serás na tua entrada, e bendito serás na tua saída."),
    ("Deuteronômio 31:8", "O SENHOR é quem vai adiante de ti; ele será contigo, não te deixará, nem te desamparará; não temas, nem te espantes."),
    # Josue
    ("Josué 1:7", "Tão somente esforça-te e tem muito bom ânimo, para teres cuidado de fazer conforme toda a lei."),
    ("Josué 1:8", "Este livro da lei não se apartará da tua boca; antes, meditarás nele dia e noite."),
    ("Josué 1:9", "Não to mandei eu? Esforça-te e tem bom ânimo; não temas, nem te espantes; porque o SENHOR teu Deus é contigo por onde quer que andares."),
    ("Josué 24:15", "Escolhei hoje a quem servireis. Eu, porém, e a minha casa serviremos ao SENHOR."),
    # 1 Samuel
    ("1 Samuel 16:7", "O homem vê o que está diante dos olhos, porém o SENHOR vê o coração."),
    # 2 Cronicas
    ("2 Crônicas 7:14", "Se o meu povo, que se chama pelo meu nome, se humilhar, e orar, e buscar a minha face, e se converter dos seus maus caminhos, então eu ouvirei dos céus."),
    # Neemias
    ("Neemias 8:10", "A alegria do SENHOR é a vossa força."),
    # Salmos
    ("Salmos 1:1", "Bem-aventurado o homem que não anda no conselho dos ímpios, nem se detém no caminho dos pecadores."),
    ("Salmos 1:3", "E ele será como a árvore plantada junto a ribeiros de águas, a qual dá o seu fruto na estação própria."),
    ("Salmos 4:8", "Em paz me deito e logo adormeço, porque só tu, SENHOR, me fazes habitar em segurança."),
    ("Salmos 16:8", "Tenho posto o SENHOR sempre diante de mim; porque ele está à minha mão direita, não serei abalado."),
    ("Salmos 16:11", "Tu me farás ver o caminho da vida; na tua presença há plenitude de alegria."),
    ("Salmos 18:2", "O SENHOR é a minha rocha, e a minha força, e o meu libertador; o meu Deus, o meu rochedo, em quem me refugio."),
    ("Salmos 19:14", "Sejam as palavras da minha boca e a meditação do meu coração agradáveis à tua presença."),
    ("Salmos 23:1", "O SENHOR é o meu pastor; nada me faltará."),
    ("Salmos 23:4", "Ainda que eu andasse pelo vale da sombra da morte, não temeria mal nenhum, porque tu és comigo."),
    ("Salmos 25:4", "SENHOR, faze-me conhecer os teus caminhos; ensina-me as tuas veredas."),
    ("Salmos 27:1", "O SENHOR é a minha luz e a minha salvação; a quem temerei? O SENHOR é a força da minha vida; de quem me recearei?"),
    ("Salmos 27:4", "Uma coisa pedi ao SENHOR, e a buscarei: que possa morar na casa do SENHOR todos os dias da minha vida."),
    ("Salmos 27:14", "Espera no SENHOR; tem bom ânimo, e ele fortalecerá o teu coração; espera, pois, no SENHOR."),
    ("Salmos 28:7", "O SENHOR é a minha força e o meu escudo; nele confiou o meu coração, e fui socorrido."),
    ("Salmos 30:5", "O choro pode durar uma noite, mas a alegria vem pela manhã."),
    ("Salmos 31:24", "Sede fortes, e ele fortalecerá o vosso coração, todos vós que esperais no SENHOR."),
    ("Salmos 32:8", "Instruir-te-ei e ensinar-te-ei o caminho que deves seguir; guiar-te-ei com os meus olhos."),
    ("Salmos 34:4", "Busquei o SENHOR, e ele me ouviu, e me livrou de todos os meus temores."),
    ("Salmos 34:8", "Provai e vede que o SENHOR é bom; bem-aventurado o homem que nele se refugia."),
    ("Salmos 34:18", "Perto está o SENHOR dos que têm o coração quebrantado, e salva os de espírito abatido."),
    ("Salmos 34:19", "Muitas são as aflições do justo, mas o SENHOR o livra de todas elas."),
    ("Salmos 37:4", "Deleita-te também no SENHOR, e ele te concederá os desejos do teu coração."),
    ("Salmos 37:5", "Entrega o teu caminho ao SENHOR; confia nele, e ele o fará."),
    ("Salmos 37:7", "Descansa no SENHOR e espera nele."),
    ("Salmos 37:23", "O SENHOR firma os passos do homem bom e se agrada do seu caminho."),
    ("Salmos 40:3", "E pôs um novo cântico na minha boca, um hino de louvor ao nosso Deus."),
    ("Salmos 42:1", "Como o cervo anseia pelas correntes das águas, assim, ó Deus, a minha alma anseia por ti."),
    ("Salmos 42:11", "Espera em Deus, pois ainda o louvarei, ele é a salvação do meu semblante e o meu Deus."),
    ("Salmos 46:1", "Deus é o nosso refúgio e força, socorro bem presente na angústia."),
    ("Salmos 46:10", "Aquietai-vos e sabei que eu sou Deus; serei exaltado entre as nações, serei exaltado na terra."),
    ("Salmos 51:10", "Cria em mim, ó Deus, um coração puro, e renova dentro de mim um espírito reto."),
    ("Salmos 55:22", "Lança o teu cuidado sobre o SENHOR, e ele te susterá; jamais permitirá que o justo seja abalado."),
    ("Salmos 56:3", "No dia em que eu tiver medo, porei em ti a minha confiança."),
    ("Salmos 62:1", "A minha alma espera somente em Deus; dele vem a minha salvação."),
    ("Salmos 62:8", "Confiai nele em todo o tempo, ó povo; derramai diante dele o vosso coração; Deus é o nosso refúgio."),
    ("Salmos 63:3", "Porque a tua benignidade é melhor do que a vida, os meus lábios te louvarão."),
    ("Salmos 84:11", "O SENHOR dará graça e glória; não retirará o bem aos que andam em integridade."),
    ("Salmos 86:5", "Pois tu, Senhor, és bom e pronto a perdoar; e de grande misericórdia para com todos os que te invocam."),
    ("Salmos 91:1", "Aquele que habita no esconderijo do Altíssimo, à sombra do Onipotente descansará."),
    ("Salmos 91:2", "Direi do SENHOR: Ele é o meu refúgio, e a minha fortaleza, o meu Deus em quem confio."),
    ("Salmos 91:4", "Com as suas penas te cobrirá, e sob as suas asas te abrigarás."),
    ("Salmos 91:11", "Porque aos seus anjos dará ordens a teu respeito, para te guardarem em todos os teus caminhos."),
    ("Salmos 91:15", "Ele me invocará, e eu lhe responderei; na angústia estarei com ele; livrar-lo-ei e o glorificarei."),
    ("Salmos 100:3", "Sabei que o SENHOR é Deus; foi ele que nos fez, e dele somos; somos seu povo e rebanho do seu pasto."),
    ("Salmos 100:4", "Entrai pelas suas portas com ações de graças, e nos seus átrios com louvor."),
    ("Salmos 100:5", "Porque o SENHOR é bom, e eterna é a sua misericórdia; a sua fidelidade dura por todas as gerações."),
    ("Salmos 103:2", "Bendize, ó minha alma, ao SENHOR, e não te esqueças de nenhum de seus benefícios."),
    ("Salmos 103:3", "Ele é quem perdoa todas as tuas iniquidades, quem sara todas as tuas enfermidades."),
    ("Salmos 103:12", "Assim como o oriente está distante do ocidente, assim ele se distanciou de nós as nossas transgressões."),
    ("Salmos 107:1", "Rendei graças ao SENHOR, porque ele é bom, porque a sua misericórdia dura para sempre."),
    ("Salmos 116:1", "Amo o SENHOR, porque ele ouviu a minha voz e as minhas súplicas."),
    ("Salmos 118:6", "O SENHOR é por mim; não temerei; que pode o homem fazer-me?"),
    ("Salmos 118:14", "O SENHOR é a minha força e o meu cântico, e é ele a minha salvação."),
    ("Salmos 118:24", "Este é o dia que o SENHOR fez; regozijemo-nos e alegremo-nos nele."),
    ("Salmos 119:11", "Escondi a tua palavra no meu coração, para não pecar contra ti."),
    ("Salmos 119:18", "Abre os meus olhos, para que eu contemple as maravilhas da tua lei."),
    ("Salmos 119:105", "Lâmpada para os meus pés é a tua palavra e luz para o meu caminho."),
    ("Salmos 119:114", "Tu és o meu esconderijo e o meu escudo; espero na tua palavra."),
    ("Salmos 121:1-2", "Levantarei os meus olhos para os montes. De onde vem o meu socorro? O meu socorro vem do SENHOR, que fez o céu e a terra."),
    ("Salmos 121:7", "O SENHOR te guardará de todo o mal; ele guardará a tua alma."),
    ("Salmos 121:8", "O SENHOR guardará a tua saída e a tua entrada, desde agora e para sempre."),
    ("Salmos 125:1", "Os que confiam no SENHOR são como o monte Sião, que não se abala, mas permanece para sempre."),
    ("Salmos 126:3", "O SENHOR fez grandes coisas por nós, e por isso estávamos alegres."),
    ("Salmos 127:1", "Se o SENHOR não edificar a casa, em vão trabalham os que a edificam."),
    ("Salmos 130:4", "Mas em ti há perdão, para que sejas temido."),
    ("Salmos 133:1", "Como é bom e agradável que os irmãos vivam em união!"),
    ("Salmos 136:1", "Rendei graças ao SENHOR, porque ele é bom, porque a sua misericórdia dura para sempre."),
    ("Salmos 138:3", "No dia em que clamei, tu me respondeste; animaste-me com força na minha alma."),
    ("Salmos 139:14", "Graças te dou porque de um modo assombrosamente maravilhoso me formaste; maravilhosas são as tuas obras."),
    ("Salmos 143:8", "Faze-me ouvir a tua benignidade pela manhã, porque em ti confio."),
    ("Salmos 145:18", "Perto está o SENHOR de todos os que o invocam, de todos os que o invocam em verdade."),
    ("Salmos 147:3", "Ele sara os de coração quebrantado e lhes ata as feridas."),
    ("Salmos 150:6", "Todo ser que tem fôlego louve ao SENHOR. Aleluia!"),
    # Proverbios
    ("Provérbios 1:7", "O temor do SENHOR é o princípio da sabedoria."),
    ("Provérbios 2:6", "Porque o SENHOR dá a sabedoria; da sua boca procedem o conhecimento e o entendimento."),
    ("Provérbios 3:5-6", "Confia no SENHOR de todo o teu coração e não te estribes no teu próprio entendimento. Reconhece-o em todos os teus caminhos, e ele endireitará as tuas veredas."),
    ("Provérbios 3:24", "Quando te deitares, não te aterrorizarás; e, quando te reclinares, o teu sono será suave."),
    ("Provérbios 4:23", "Sobre tudo o que se deve guardar, guarda o teu coração, porque dele procedem as fontes da vida."),
    ("Provérbios 10:22", "A bênção do SENHOR enriquece, e ele não acrescenta tristeza com ela."),
    ("Provérbios 12:25", "A ansiedade no coração do homem o abate, mas a boa palavra o alegra."),
    ("Provérbios 14:26", "No temor do SENHOR há forte confiança, e os seus filhos terão um refúgio."),
    ("Provérbios 15:1", "A resposta branda desvia o furor, mas a palavra dura suscita a ira."),
    ("Provérbios 15:3", "Os olhos do SENHOR estão em todo lugar, observando os maus e os bons."),
    ("Provérbios 16:3", "Confia ao SENHOR as tuas obras, e os teus pensamentos serão estabelecidos."),
    ("Provérbios 16:9", "O coração do homem planeja o seu caminho, mas o SENHOR lhe dirige os passos."),
    ("Provérbios 17:17", "Em todo o tempo ama o amigo, e o irmão é nascido para o tempo da angústia."),
    ("Provérbios 17:22", "O coração alegre é um bom remédio, mas o espírito abatido seca os ossos."),
    ("Provérbios 18:10", "O nome do SENHOR é uma torre forte; para ela corre o justo e está seguro."),
    ("Provérbios 18:24", "O homem que tem amigos deve mostrar-se amigo; e há um amigo mais chegado do que um irmão."),
    ("Provérbios 19:21", "Muitos pensamentos há no coração do homem, mas o conselho do SENHOR permanecerá."),
    ("Provérbios 22:6", "Ensina a criança no caminho em que deve andar; e, até quando envelhecer, não se desviará dele."),
    ("Provérbios 23:18", "Porque, certamente, há um futuro, e a tua esperança não será frustrada."),
    ("Provérbios 24:16", "Porque o justo cai sete vezes e torna a levantar-se, mas os ímpios tropeçam na adversidade."),
    ("Provérbios 28:13", "O que encobre as suas transgressões não prosperará, mas o que as confessa e abandona alcançará misericórdia."),
    ("Provérbios 29:25", "O temor do homem arma laço, mas o que confia no SENHOR estará seguro."),
    # Eclesiastes
    ("Eclesiastes 3:1", "Tudo tem o seu tempo determinado; há tempo para todo o propósito debaixo do céu."),
    ("Eclesiastes 3:11", "Ele fez tudo formoso no seu devido tempo; também pôs a eternidade no coração do homem."),
    # Isaias
    ("Isaías 9:6", "Um menino nos nasceu, um filho se nos deu; e o seu nome será: Maravilhoso, Conselheiro, Deus Forte, Pai da Eternidade, Príncipe da Paz."),
    ("Isaías 26:3", "Tu conservarás em paz aquele cujo propósito é firme; porque ele confia em ti."),
    ("Isaías 40:29", "Ele dá força ao cansado e multiplica as forças ao que não tem nenhum vigor."),
    ("Isaías 40:31", "Mas os que esperam no SENHOR renovarão as suas forças. Voarão alto como águias; correrão e não se cansarão, caminharão e não se fatigarão."),
    ("Isaías 41:10", "Não temas, porque eu sou contigo; não te assombres, porque eu sou o teu Deus; eu te fortaleço, e te ajudo, e te sustento com a minha destra fiel."),
    ("Isaías 41:13", "Porque eu, o SENHOR teu Deus, te seguro pela tua mão direita; e te digo: Não temas; eu te ajudarei."),
    ("Isaías 43:1", "Agora, assim diz o SENHOR que te criou: Não temas, porque eu te remi; chamei-te pelo teu nome, tu és meu."),
    ("Isaías 43:2", "Quando passares pelas águas, eu serei contigo; e pelos rios, eles não te submergirão."),
    ("Isaías 43:18-19", "Não vos lembreis das coisas anteriores, nem considereis as coisas antigas. Eis que faço coisa nova."),
    ("Isaías 46:4", "Até à vossa velhice eu serei o mesmo, e até às vossas cãs vos sustentarei."),
    ("Isaías 49:16", "Eis que nas palmas das minhas mãos te gravei."),
    ("Isaías 53:5", "Ele foi ferido pelas nossas transgressões e moído pelas nossas iniquidades; o castigo que nos traz a paz estava sobre ele, e pelas suas pisaduras fomos sarados."),
    ("Isaías 54:10", "A minha benignidade não se apartará de ti, nem a aliança da minha paz vacilará, diz o SENHOR que tem misericórdia de ti."),
    ("Isaías 55:8-9", "Porque os meus pensamentos não são os vossos pensamentos, nem os vossos caminhos os meus caminhos, diz o SENHOR."),
    ("Isaías 58:11", "O SENHOR te guiará continuamente, e, nos lugares secos, fartará a tua alma."),
    ("Isaías 60:1", "Levanta-te, resplandece, porque veio a tua luz, e a glória do SENHOR se levantou sobre ti."),
    ("Isaías 65:24", "E será que antes de clamarem eu responderei; estando eles ainda falando, eu os ouvirei."),
    # Jeremias
    ("Jeremias 17:7", "Bendito o homem que confia no SENHOR e cuja esperança é o SENHOR."),
    ("Jeremias 29:11", "Porque eu sei os planos que tenho para vocês, diz o SENHOR, planos de fazê-los prosperar e não de lhes causar dano, planos de dar a vocês esperança e um futuro."),
    ("Jeremias 29:12", "Então vocês clamarão a mim e virão orar a mim, e eu os ouvirei."),
    ("Jeremias 29:13", "Vocês me procurarão e me encontrarão quando me procurarem de todo o coração."),
    ("Jeremias 31:3", "Amei-te com amor eterno; por isso, com benignidade te atraí."),
    ("Jeremias 33:3", "Clama a mim, e eu te responderei, e anunciarei coisas grandes e ocultas que não conheces."),
    # Lamentacoes
    ("Lamentações 3:22-23", "As misericórdias do SENHOR são a causa de não sermos consumidos, porque as suas misericórdias não têm fim; renovam-se cada manhã."),
    ("Lamentações 3:25", "Bom é o SENHOR para os que esperam nele, para a alma que o busca."),
    # Ezequiel
    ("Ezequiel 36:26", "Dar-vos-ei um coração novo, e porei dentro de vós um espírito novo; tirarei de vós o coração de pedra e vos darei um coração de carne."),
    # Joel
    ("Joel 2:25", "Restituir-vos-ei os anos que a lagarta consumiu."),
    ("Joel 2:28", "E acontecerá depois que derramarei o meu Espírito sobre toda a carne."),
    # Naum
    ("Naum 1:7", "O SENHOR é bom, uma força no dia da angústia, e conhece os que nele confiam."),
    # Habacuque
    ("Habacuque 2:4", "O justo viverá pela sua fé."),
    ("Habacuque 3:19", "O Senhor DEUS é a minha força; ele me dá pés como os da corça e me faz andar sobre os meus lugares altos."),
    # Sofonias
    ("Sofonias 3:17", "O SENHOR teu Deus está no meio de ti, poderoso para salvar; ele se deleitará em ti com alegria."),
    # Zacarias
    ("Zacarias 4:6", "Não por força nem por poder, mas pelo meu Espírito, diz o SENHOR dos Exércitos."),
    # Mateus
    ("Mateus 4:4", "Nem só de pão viverá o homem, mas de toda palavra que sai da boca de Deus."),
    ("Mateus 5:3", "Bem-aventurados os pobres de espírito, porque deles é o reino dos céus."),
    ("Mateus 5:4", "Bem-aventurados os que choram, porque serão consolados."),
    ("Mateus 5:6", "Bem-aventurados os que têm fome e sede de justiça, porque serão fartos."),
    ("Mateus 5:7", "Bem-aventurados os misericordiosos, porque eles alcançarão misericórdia."),
    ("Mateus 5:8", "Bem-aventurados os limpos de coração, porque eles verão a Deus."),
    ("Mateus 5:9", "Bem-aventurados os pacificadores, porque eles serão chamados filhos de Deus."),
    ("Mateus 5:16", "Assim resplandeça a vossa luz diante dos homens, para que vejam as vossas boas obras e glorifiquem a vosso Pai que está nos céus."),
    ("Mateus 5:44", "Amai os vossos inimigos, bendizei os que vos maldizem, fazei bem aos que vos odeiam."),
    ("Mateus 6:6", "Tu, porém, quando orares, entra no teu quarto e, fechando a tua porta, ora a teu Pai que está em secreto."),
    ("Mateus 6:25", "Por isso vos digo: Não andeis ansiosos pela vossa vida, quanto ao que haveis de comer ou beber."),
    ("Mateus 6:26", "Olhai para as aves do céu: não semeiam, não colhem, nem ajuntam em celeiros, e vosso Pai celestial as alimenta."),
    ("Mateus 6:33", "Buscai, pois, em primeiro lugar, o seu reino e a sua justiça, e todas as demais coisas vos serão acrescentadas."),
    ("Mateus 6:34", "Portanto, não vos preocupeis com o dia de amanhã, pois o amanhã cuidará de si mesmo."),
    ("Mateus 7:7", "Pedi, e dar-se-vos-á; buscai, e encontrareis; batei, e abrir-se-vos-á."),
    ("Mateus 7:8", "Porque todo o que pede recebe; o que busca encontra; e ao que bate abrir-se-á."),
    ("Mateus 7:12", "Tudo o que quereis que os homens vos façam, fazei-o vós também a eles."),
    ("Mateus 11:28", "Vinde a mim, todos os que estais cansados e sobrecarregados, e eu vos darei descanso."),
    ("Mateus 11:29", "Tomai sobre vós o meu jugo, e aprendei de mim, que sou manso e humilde de coração."),
    ("Mateus 17:20", "Se tiverdes fé como um grão de mostarda, direis a este monte: Passa daqui para acolá, e ele passará."),
    ("Mateus 18:20", "Porque onde dois ou três estiverem reunidos em meu nome, ali estou no meio deles."),
    ("Mateus 19:26", "Para Deus, tudo é possível."),
    ("Mateus 22:37", "Amarás o Senhor, teu Deus, de todo o teu coração, de toda a tua alma e de todo o teu entendimento."),
    ("Mateus 22:39", "Amarás o teu próximo como a ti mesmo."),
    ("Mateus 28:19", "Portanto, ide, fazei discípulos de todas as nações, batizando-os em nome do Pai, e do Filho, e do Espírito Santo."),
    ("Mateus 28:20", "Eis que estou convosco todos os dias, até a consumação dos séculos."),
    # Marcos
    ("Marcos 1:15", "O reino de Deus está próximo; arrependei-vos e crede no evangelho."),
    ("Marcos 9:23", "Se tu podes! Tudo é possível ao que crê."),
    ("Marcos 10:27", "Para os homens isso é impossível, mas não para Deus; porque para Deus todas as coisas são possíveis."),
    ("Marcos 11:22", "Tende fé em Deus."),
    ("Marcos 11:24", "Por isso vos digo que tudo o que pedirdes, orando, crede que o recebereis, e tê-lo-eis."),
    # Lucas
    ("Lucas 1:37", "Porque para Deus nenhuma coisa é impossível."),
    ("Lucas 1:45", "Bem-aventurada a que creu, pois hão de cumprir-se as coisas que lhe foram ditas da parte do Senhor."),
    ("Lucas 1:49", "Porque o Poderoso fez grandes coisas por mim, e o seu nome é santo."),
    ("Lucas 6:31", "E, como quereis que os homens vos façam, fazei-o vós também da mesma maneira."),
    ("Lucas 6:38", "Dai, e dar-se-vos-á; boa medida, recalcada, sacudida e transbordante."),
    ("Lucas 11:9", "Pedi, e dar-se-vos-á; buscai e encontrareis; batei e abrir-se-vos-á."),
    ("Lucas 15:7", "Digo-vos que assim haverá mais alegria no céu por um pecador que se arrepende."),
    ("Lucas 18:27", "O que é impossível para os homens é possível para Deus."),
    # Joao
    ("João 1:1", "No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus."),
    ("João 1:12", "Mas, a todos quantos o receberam, deu-lhes o poder de serem feitos filhos de Deus."),
    ("João 3:16", "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna."),
    ("João 3:17", "Porque Deus enviou o seu Filho ao mundo, não para que julgasse o mundo, mas para que o mundo fosse salvo por ele."),
    ("João 4:24", "Deus é Espírito, e importa que os que o adoram o adorem em espírito e em verdade."),
    ("João 6:35", "Eu sou o pão da vida; aquele que vem a mim nunca terá fome, e aquele que crê em mim nunca terá sede."),
    ("João 8:12", "Eu sou a luz do mundo; aquele que me segue não andará em trevas, mas terá a luz da vida."),
    ("João 8:32", "E conhecereis a verdade, e a verdade vos libertará."),
    ("João 8:36", "Se, pois, o Filho vos libertar, verdadeiramente sereis livres."),
    ("João 10:10", "Eu vim para que tenham vida e a tenham em abundância."),
    ("João 10:14", "Eu sou o bom pastor; conheço as minhas ovelhas, e elas me conhecem a mim."),
    ("João 10:28", "E eu lhes dou a vida eterna, e nunca perecerão, e ninguém as arrebatará da minha mão."),
    ("João 11:25", "Eu sou a ressurreição e a vida; quem crê em mim, ainda que esteja morto, viverá."),
    ("João 13:34", "Um novo mandamento vos dou: que vos ameis uns aos outros; como eu vos amei, que também vos ameis uns aos outros."),
    ("João 14:1", "Não se turbe o vosso coração; credes em Deus, crede também em mim."),
    ("João 14:6", "Eu sou o caminho, e a verdade, e a vida; ninguém vem ao Pai senão por mim."),
    ("João 14:13", "E tudo quanto pedirdes em meu nome, eu o farei, para que o Pai seja glorificado no Filho."),
    ("João 14:27", "Deixo-vos a paz, a minha paz vos dou; não vo-la dou como o mundo a dá. Não se turbe o vosso coração, nem se atemorize."),
    ("João 15:5", "Eu sou a videira, vós sois os ramos. Quem permanece em mim e eu nele, esse dá muito fruto; porque sem mim nada podeis fazer."),
    ("João 15:7", "Se permanecerdes em mim, e as minhas palavras permanecerem em vós, pedireis tudo o que quiserdes, e vos será feito."),
    ("João 15:13", "Ninguém tem maior amor do que este: de dar alguém a sua vida pelos seus amigos."),
    ("João 16:33", "No mundo passais tribulações, mas tende bom ânimo; eu venci o mundo."),
    # Atos
    ("Atos 1:8", "Mas recebereis a virtude do Espírito Santo, que há de vir sobre vós; e ser-me-eis testemunhas."),
    ("Atos 4:12", "E em nenhum outro há salvação; porque debaixo do céu nenhum outro nome há dado entre os homens pelo qual devamos ser salvos."),
    # Romanos
    ("Romanos 1:16", "Porque não me envergonho do evangelho de Cristo, pois é o poder de Deus para a salvação de todo aquele que crê."),
    ("Romanos 5:1", "Sendo, pois, justificados pela fé, temos paz com Deus, por nosso Senhor Jesus Cristo."),
    ("Romanos 5:5", "E a esperança não traz confusão, porque o amor de Deus está derramado em nossos corações pelo Espírito Santo."),
    ("Romanos 5:8", "Mas Deus prova o seu amor para conosco em que Cristo morreu por nós, sendo nós ainda pecadores."),
    ("Romanos 6:23", "Porque o salário do pecado é a morte, mas o dom gratuito de Deus é a vida eterna, em Cristo Jesus nosso Senhor."),
    ("Romanos 8:1", "Portanto, agora nenhuma condenação há para os que estão em Cristo Jesus."),
    ("Romanos 8:14", "Porque todos os que são guiados pelo Espírito de Deus, esses são filhos de Deus."),
    ("Romanos 8:26", "O Espírito nos ajuda em nossa fraqueza; pois não sabemos o que havemos de pedir como convém."),
    ("Romanos 8:28", "Sabemos que todas as coisas cooperam para o bem daqueles que amam a Deus, daqueles que são chamados segundo o seu propósito."),
    ("Romanos 8:31", "Que diremos, pois, a estas coisas? Se Deus é por nós, quem será contra nós?"),
    ("Romanos 8:37", "Mas em todas estas coisas somos mais do que vencedores, por meio daquele que nos amou."),
    ("Romanos 8:38-39", "Estou persuadido de que nem a morte, nem a vida, nem os anjos, nem os principados, nem as potestades, nem o presente, nem o porvir nos poderá separar do amor de Deus."),
    ("Romanos 10:9", "Se com a tua boca confessares ao Senhor Jesus, e em teu coração creres que Deus o ressuscitou dos mortos, serás salvo."),
    ("Romanos 10:13", "Porque todo aquele que invocar o nome do Senhor será salvo."),
    ("Romanos 12:2", "E não sede conformados com este século, mas sede transformados pela renovação do vosso entendimento."),
    ("Romanos 12:12", "Alegrai-vos na esperança, sede pacientes na tribulação, perseverade na oração."),
    ("Romanos 12:21", "Não sejas vencido do mal, mas vence o mal com o bem."),
    ("Romanos 15:13", "Ora, o Deus de esperança vos encha de todo o gozo e paz em crença."),
    # 1 Corintios
    ("1 Coríntios 2:9", "As coisas que o olho não viu, e o ouvido não ouviu, e não subiram ao coração do homem, são as que Deus preparou para os que o amam."),
    ("1 Coríntios 6:19-20", "Ou não sabeis que o vosso corpo é o templo do Espírito Santo? Porque fostes comprados por bom preço; glorificai, pois, a Deus no vosso corpo."),
    ("1 Coríntios 10:13", "Não veio sobre vós tentação que não fosse humana; mas fiel é Deus, que não vos deixará tentar acima do que podeis suportar."),
    ("1 Coríntios 13:4-5", "O amor é sofredor, é benigno; o amor não é invejoso; o amor não trata com leviandade, não se ensoberbece."),
    ("1 Coríntios 13:7", "Tudo sofre, tudo crê, tudo espera, tudo suporta."),
    ("1 Coríntios 13:8", "O amor nunca falha."),
    ("1 Coríntios 13:13", "Agora, pois, permanecem a fé, a esperança e o amor, estes três; mas o maior destes é o amor."),
    ("1 Coríntios 15:57", "Mas graças a Deus que nos dá a vitória por nosso Senhor Jesus Cristo."),
    ("1 Coríntios 16:13", "Velai, estai firmes na fé, portai-vos varonilmente, fortalecei-vos."),
    # 2 Corintios
    ("2 Coríntios 1:3-4", "Bendito seja o Deus e Pai de nosso Senhor Jesus Cristo, o Pai das misericórdias e o Deus de toda a consolação, que nos consola em todas as nossas tribulações."),
    ("2 Coríntios 4:17", "Porque o que é leve e momentâneo da nossa tribulação nos produz um eterno peso de glória."),
    ("2 Coríntios 5:7", "Porque andamos por fé e não por vista."),
    ("2 Coríntios 5:17", "Assim que, se alguém está em Cristo, nova criatura é; as coisas velhas já passaram; eis que tudo se fez novo."),
    ("2 Coríntios 9:8", "E Deus é poderoso para fazer que toda a graça abunde em vós, a fim de que, tendo sempre em tudo plena suficiência, abundeis em toda a boa obra."),
    ("2 Coríntios 12:9", "A minha graça te basta, porque o meu poder se aperfeiçoa na fraqueza."),
    # Galatas
    ("Gálatas 2:20", "Já estou crucificado com Cristo; e vivo, não mais eu, mas Cristo vive em mim."),
    ("Gálatas 5:1", "Estai, pois, firmes na liberdade com que Cristo nos libertou."),
    ("Gálatas 5:22", "Mas o fruto do Espírito é: amor, gozo, paz, longanimidade, benignidade, bondade, fidelidade."),
    ("Gálatas 6:7", "Não vos enganeis; Deus não se deixa escarnecer; porque tudo o que o homem semear, isso também ceifará."),
    ("Gálatas 6:9", "Não nos cansemos de fazer o bem, porque a seu tempo ceifaremos, se não desfalecermos."),
    # Efesios
    ("Efésios 1:3", "Bendito seja o Deus e Pai de nosso Senhor Jesus Cristo, que nos abençoou com todas as bênçãos espirituais nos lugares celestiais em Cristo."),
    ("Efésios 2:8", "Porque pela graça sois salvos, por meio da fé; e isso não vem de vós; é dom de Deus."),
    ("Efésios 2:10", "Porque somos feitura sua, criados em Cristo Jesus para as boas obras."),
    ("Efésios 3:20", "Ora, àquele que é poderoso para fazer tudo muito mais abundantemente além daquilo que pedimos ou pensamos."),
    ("Efésios 4:32", "Antes, sede uns para com os outros benignos, misericordiosos, perdoando-vos uns aos outros, como também Deus vos perdoou em Cristo."),
    ("Efésios 6:10", "Finalmente, irmãos, fortalecei-vos no Senhor e na força do seu poder."),
    ("Efésios 6:11", "Revesti-vos de toda a armadura de Deus, para que possais ficar firmes contra as astutas ciladas do diabo."),
    # Filipenses
    ("Filipenses 1:6", "Tendo por certo que aquele que em vós começou a boa obra a aperfeiçoará até ao dia de Jesus Cristo."),
    ("Filipenses 3:13", "Esquecendo-me das coisas que atrás ficam e avançando para as que estão adiante."),
    ("Filipenses 4:4", "Alegrai-vos sempre no Senhor; outra vez digo, alegrai-vos."),
    ("Filipenses 4:6", "Não estejais ansiosos de coisa alguma; em tudo, porém, sejam conhecidas as vossas petições diante de Deus."),
    ("Filipenses 4:7", "E a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos sentidos em Cristo Jesus."),
    ("Filipenses 4:8", "Tudo o que é verdadeiro, tudo o que é honesto, tudo o que é justo, tudo o que é puro, tudo o que é amável, nisso pensai."),
    ("Filipenses 4:11", "Aprendi a estar contente em qualquer estado em que me encontre."),
    ("Filipenses 4:13", "Posso todas as coisas em Cristo que me fortalece."),
    ("Filipenses 4:19", "O meu Deus, segundo as suas riquezas em glória, suprirá todas as vossas necessidades em Cristo Jesus."),
    # Colossenses
    ("Colossenses 3:15", "E a paz de Deus governe em vossos corações; para isso fostes chamados num mesmo corpo; e sede agradecidos."),
    ("Colossenses 3:16", "A palavra de Cristo habite em vós ricamente, em toda a sabedoria."),
    ("Colossenses 3:23", "E tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor."),
    # 1 Tessalonicenses
    ("1 Tessalonicenses 5:16", "Alegrai-vos sempre."),
    ("1 Tessalonicenses 5:17", "Orai sem cessar."),
    ("1 Tessalonicenses 5:18", "Em tudo dai graças, porque esta é a vontade de Deus em Cristo Jesus para convosco."),
    # 2 Tessalonicenses
    ("2 Tessalonicenses 3:3", "Mas o Senhor é fiel; ele vos confirmará e guardará do maligno."),
    # 2 Timoteo
    ("2 Timóteo 1:7", "Porque Deus não nos deu espírito de covardia, mas de poder, de amor e de moderação."),
    ("2 Timóteo 2:15", "Procura apresentar-te a Deus aprovado, como obreiro que não tem de que se envergonhar."),
    ("2 Timóteo 3:16-17", "Toda a Escritura é divinamente inspirada, e proveitosa para ensinar, para repreender, para corrigir, para instruir em justiça."),
    ("2 Timóteo 4:7", "Combati o bom combate, acabei a carreira, guardei a fé."),
    # Hebreus
    ("Hebreus 4:12", "Porque a palavra de Deus é viva e eficaz, e mais penetrante do que qualquer espada de dois gumes."),
    ("Hebreus 4:16", "Cheguemo-nos, pois, com confiança ao trono da graça, para que possamos alcançar misericórdia e achar graça."),
    ("Hebreus 10:23", "Retenhamos firmes a confissão da nossa esperança, porque fiel é o que prometeu."),
    ("Hebreus 11:1", "Ora, a fé é o firme fundamento das coisas que se esperam e a prova das coisas que se não veem."),
    ("Hebreus 11:6", "Mas sem fé é impossível agradar-lhe; porque é necessário que aquele que se aproxima de Deus creia que ele existe."),
    ("Hebreus 12:1", "Portanto, também nós, pois que estamos rodeados de uma tão grande nuvem de testemunhas, deixemos todo o embaraço e o pecado que tão de perto nos rodeia."),
    ("Hebreus 12:2", "Olhando para Jesus, o Autor e Consumador da fé."),
    ("Hebreus 13:5", "Contentar-me-ei com o que tenho; porque ele disse: Não te deixarei, nem te abandonarei."),
    ("Hebreus 13:8", "Jesus Cristo é o mesmo, ontem, e hoje, e eternamente."),
    # Tiago
    ("Tiago 1:5", "E, se algum de vós tem falta de sabedoria, peça-a a Deus, que a todos dá liberalmente e não o lança em rosto; e ser-lhe-á dada."),
    ("Tiago 4:7", "Sujeitai-vos, pois, a Deus; resisti ao diabo, e ele fugirá de vós."),
    ("Tiago 4:8", "Chegai-vos a Deus, e ele se chegará a vós."),
    ("Tiago 5:16", "A oração feita por um justo pode muito em seus efeitos."),
    # 1 Pedro
    ("1 Pedro 1:15", "Assim como é santo aquele que vos chamou, sede vós também santos em toda a vossa maneira de viver."),
    ("1 Pedro 2:9", "Mas vós sois a geração eleita, o sacerdócio real, a nação santa, o povo adquirido."),
    ("1 Pedro 2:24", "Pelas suas feridas fostes sarados."),
    ("1 Pedro 5:6", "Humilhai-vos, pois, sob a poderosa mão de Deus, para que ele vos exalte no devido tempo."),
    ("1 Pedro 5:7", "Lançando sobre ele toda a vossa ansiedade, porque ele tem cuidado de vós."),
    ("1 Pedro 5:10", "E o Deus de toda a graça, que em Cristo Jesus vos chamou para a sua eterna glória, depois de haverdes sofrido um pouco de tempo, ele mesmo vos aperfeiçoará."),
    # 1 Joao
    ("1 João 1:9", "Se confessarmos os nossos pecados, ele é fiel e justo para nos perdoar os pecados e nos purificar de toda a injustiça."),
    ("1 João 3:1", "Vede que amor nos concedeu o Pai, que fôssemos chamados filhos de Deus."),
    ("1 João 4:7", "Amados, amemo-nos uns aos outros, porque o amor é de Deus."),
    ("1 João 4:8", "Aquele que não ama não conhece a Deus, porque Deus é amor."),
    ("1 João 4:16", "Deus é amor; e quem permanece em amor permanece em Deus, e Deus nele."),
    ("1 João 4:18", "No amor não há medo; antes, o perfeito amor lança fora o medo."),
    ("1 João 4:19", "Nós o amamos porque ele nos amou primeiro."),
    ("1 João 5:4", "Porque tudo o que é nascido de Deus vence o mundo; e esta é a vitória que vence o mundo, a nossa fé."),
    ("1 João 5:14", "E esta é a confiança que temos nele: que, se pedirmos alguma coisa segundo a sua vontade, ele nos ouve."),
    # Apocalipse
    ("Apocalipse 1:8", "Eu sou o Alfa e o Ômega, o princípio e o fim, diz o Senhor."),
    ("Apocalipse 3:20", "Eis que estou à porta e bato; se alguém ouvir a minha voz e abrir a porta, entrarei em sua casa e cearei com ele."),
    ("Apocalipse 21:4", "E Deus limpará de seus olhos toda a lágrima, e não haverá mais morte, nem pranto, nem clamor, nem dor."),
    ("Apocalipse 21:5", "Eis que faço novas todas as coisas."),
    ("Apocalipse 22:20", "Certamente venho sem demora. Amém! Vem, Senhor Jesus."),

    # --- NOVOS VERSICULOS ---

    # Genesis (mais)
    ("Gênesis 16:13", "Tu és o Deus que me vê."),
    ("Gênesis 22:14", "O SENHOR proverá."),
    ("Gênesis 32:28", "O teu nome não será mais chamado Jacó, mas Israel; porque lutaste com Deus e com os homens e prevaleceste."),
    ("Gênesis 39:23", "O SENHOR estava com ele; e tudo o que ele fazia, o SENHOR prosperava."),

    # Exodo (mais)
    ("Êxodo 3:14", "EU SOU O QUE SOU. Assim dirás aos filhos de Israel: EU SOU me enviou a vós."),
    ("Êxodo 33:14", "A minha presença irá contigo, e eu te darei descanso."),
    ("Êxodo 34:6", "O SENHOR, o SENHOR Deus misericordioso e piedoso, tardio em irar-se, e grande em benignidade e verdade."),

    # Numeros
    ("Números 6:24-26", "O SENHOR te abençoe e te guarde; o SENHOR faça resplandecer o seu rosto sobre ti e tenha misericórdia de ti; o SENHOR erga o seu rosto sobre ti e te dê a paz."),
    ("Números 23:19", "Deus não é homem, para que minta; nem filho de homem, para que se arrependa. Porventura diria ele uma coisa e não a faria?"),

    # Deuteronomio (mais)
    ("Deuteronômio 4:29", "Mas, se dali buscardes ao SENHOR vosso Deus, o achareis, quando o buscardes com todo o vosso coração e com toda a vossa alma."),
    ("Deuteronômio 8:3", "Nem só de pão viverá o homem, mas de tudo o que sai da boca do SENHOR."),
    ("Deuteronômio 33:27", "O Deus eterno é o teu refúgio, e por baixo estão os braços eternos."),

    # Josue (mais)
    ("Josué 3:5", "Santificai-vos, porque amanhã o SENHOR fará maravilhas no meio de vós."),

    # 1 Samuel (mais)
    ("1 Samuel 2:2", "Não há santo como o SENHOR, porque não há outro além de ti; nem há rocha como o nosso Deus."),
    ("1 Samuel 7:12", "Até aqui nos ajudou o SENHOR."),
    ("1 Samuel 12:24", "Temei somente ao SENHOR e servi-o com toda a verdade, de todo o vosso coração."),
    ("1 Samuel 17:47", "O SENHOR não salva com espada nem com lança; porque do SENHOR é a guerra."),

    # 2 Samuel
    ("2 Samuel 22:3", "O meu Deus, o meu rochedo em que me refugio, o meu escudo, e o corno da minha salvação, o meu alto refúgio e o meu refúgio; tu és o meu Salvador."),
    ("2 Samuel 22:33", "Deus é a minha força e o meu poder; e ele fez perfeito o meu caminho."),

    # 1 Reis
    ("1 Reis 8:56", "Bendito seja o SENHOR, que deu descanso ao seu povo Israel, conforme tudo o que tinha prometido."),

    # 1 Cronicas
    ("1 Crônicas 16:11", "Buscai ao SENHOR e a sua força; buscai a sua face continuamente."),
    ("1 Crônicas 16:34", "Rendei graças ao SENHOR, porque ele é bom; porque a sua misericórdia dura para sempre."),
    ("1 Crônicas 29:11", "Tua, ó SENHOR, é a grandeza, e o poder, e a glória, e a vitória, e a majestade."),

    # 2 Cronicas (mais)
    ("2 Crônicas 15:4", "Mas quando em sua angústia se converteram ao SENHOR Deus de Israel e o buscaram, foi achado por eles."),
    ("2 Crônicas 20:15", "Não temais, nem vos atemorizeis, por causa desta grande multidão; porque a guerra não é vossa, mas de Deus."),
    ("2 Crônicas 20:17", "Não precisareis pelear nesta batalha; ponde-vos, estai quietos e vede a salvação do SENHOR."),

    # Esdras
    ("Esdras 8:22", "A mão do nosso Deus é sobre todos os que o buscam para o bem deles."),

    # Jo
    ("Jó 19:25", "Eu sei que o meu Redentor vive, e que por fim se levantará sobre o pó."),
    ("Jó 42:2", "Eu sei que tudo podes, e que nenhum dos teus propósitos pode ser frustrado."),

    # Salmos (mais)
    ("Salmos 2:8", "Pede-me, e eu te darei as nações como herança tua."),
    ("Salmos 5:3", "De manhã ouvirás a minha voz; de manhã me apresentarei a ti e esperarei."),
    ("Salmos 8:1", "Ó SENHOR, Senhor nosso, quão glorioso é o teu nome em toda a terra!"),
    ("Salmos 9:9", "O SENHOR também será um alto refúgio para o oprimido, um refúgio nos tempos de angústia."),
    ("Salmos 18:32", "Deus é quem me cinge de força e torna perfeito o meu caminho."),
    ("Salmos 20:7", "Uns confiam em carros, e outros, em cavalos; mas nós nos lembramos do nome do SENHOR nosso Deus."),
    ("Salmos 22:24", "Porque não desprezou nem abominou a aflição do aflito, nem escondeu dele o seu rosto; mas quando ele clamou, o ouviu."),
    ("Salmos 23:6", "Certamente que a bondade e a misericórdia me seguirão todos os dias da minha vida."),
    ("Salmos 24:1", "Do SENHOR é a terra e a sua plenitude; o mundo e os que nele habitam."),
    ("Salmos 29:11", "O SENHOR dará força ao seu povo; o SENHOR abençoará o seu povo com paz."),
    ("Salmos 33:12", "Bem-aventurada a nação cujo Deus é o SENHOR; o povo que ele escolheu para sua herança."),
    ("Salmos 33:18", "Eis que os olhos do SENHOR estão sobre os que o temem, sobre os que esperam na sua misericórdia."),
    ("Salmos 36:7", "Quão preciosa é, ó Deus, a tua benignidade! Por isso, os filhos dos homens se acolhem à sombra das tuas asas."),
    ("Salmos 43:5", "Por que te abates, ó minha alma, e te perturbas dentro de mim? Espera em Deus, porque ainda o hei de louvar."),
    ("Salmos 47:1", "Batei palmas, todos os povos; celebrai a Deus com voz de triunfo."),
    ("Salmos 48:14", "Este Deus é o nosso Deus eternamente e para sempre; ele nos guiará até à morte."),
    ("Salmos 50:15", "E invoca-me no dia da angústia; eu te livrarei, e tu me glorificarás."),
    ("Salmos 57:10", "Porque a tua misericórdia é grande até aos céus, e a tua verdade até às nuvens."),
    ("Salmos 66:20", "Bendito seja Deus, que não rejeitou a minha oração, nem removeu de mim a sua misericórdia."),
    ("Salmos 68:19", "Bendito seja o Senhor, que dia a dia nos sobrecarrega de benefícios."),
    ("Salmos 71:5", "Porque tu és a minha esperança, Senhor DEUS; és a minha confiança desde a minha mocidade."),
    ("Salmos 73:26", "A minha carne e o meu coração desfalecem, mas Deus é a força do meu coração e a minha porção para sempre."),
    ("Salmos 80:3", "Restaura-nos, ó Deus; faze resplandecer o teu rosto, e seremos salvos."),
    ("Salmos 89:1", "As misericórdias do SENHOR cantarei para sempre; de geração em geração farei conhecida a tua fidelidade com a minha boca."),
    ("Salmos 92:4", "Pois tu, SENHOR, me fazes alegrar com as tuas obras; exultarei nas obras das tuas mãos."),
    ("Salmos 94:14", "Porque o SENHOR não abandonará o seu povo, nem desamparará a sua herança."),
    ("Salmos 95:6", "Vinde, adoremos e prostremos; ajoelhemos perante o SENHOR que nos criou."),
    ("Salmos 96:4", "Porque o SENHOR é grande e muito digno de ser louvado; é mais temível do que todos os deuses."),
    ("Salmos 103:17", "Mas a misericórdia do SENHOR é desde a eternidade até a eternidade sobre os que o temem."),
    ("Salmos 104:33", "Cantarei ao SENHOR enquanto viver; cantarei louvores ao meu Deus enquanto existir."),
    ("Salmos 111:10", "O temor do SENHOR é o princípio da sabedoria; bom entendimento têm todos os que fazem os seus preceitos."),
    ("Salmos 112:7", "Não se aterrorizará com más notícias; o seu coração está firme, confiante no SENHOR."),
    ("Salmos 115:1", "Não a nós, SENHOR, não a nós, mas ao teu nome dá glória, por amor da tua misericórdia e da tua verdade."),
    ("Salmos 119:50", "Este é o meu consolo na minha angústia; que a tua palavra me deu vida."),
    ("Salmos 119:89", "Para sempre, ó SENHOR, a tua palavra está firmemente estabelecida nos céus."),
    ("Salmos 119:130", "A exposição das tuas palavras dá luz; dá entendimento aos simples."),
    ("Salmos 138:7", "Ainda que eu andasse no meio da angústia, tu me revivificarás."),
    ("Salmos 139:5", "Tu me cercas por detrás e pela frente, e sobre mim pões a tua mão."),
    ("Salmos 142:3", "Quando o meu espírito estava angustiado dentro de mim, tu conhecias o meu caminho."),
    ("Salmos 146:5", "Feliz aquele que tem por ajudante o Deus de Jacó, e cuja esperança está no SENHOR seu Deus."),
    ("Salmos 147:11", "O SENHOR se agrada dos que o temem, dos que esperam na sua misericórdia."),
    ("Salmos 148:13", "Louvem o nome do SENHOR; porque só o seu nome é excelso; a sua glória está acima da terra e do céu."),

    # Proverbios (mais)
    ("Provérbios 8:17", "Eu amo os que me amam, e os que me procuram diligentemente me acharão."),
    ("Provérbios 11:2", "Com a soberba vem a vergonha, mas com os humildes está a sabedoria."),
    ("Provérbios 11:14", "Onde não há sábio conselho, o povo cai; mas na multidão de conselheiros há segurança."),
    ("Provérbios 13:20", "Anda com os sábios e serás sábio; mas o companheiro dos tolos será destruído."),
    ("Provérbios 14:30", "O coração tranquilo é a vida do corpo."),
    ("Provérbios 16:24", "As palavras agradáveis são como favos de mel, doces para a alma e saúde para os ossos."),
    ("Provérbios 21:21", "O que segue a justiça e a misericórdia achará a vida, a justiça e a honra."),
    ("Provérbios 27:1", "Não te glories do dia de amanhã, porque não sabes o que trará o dia."),
    ("Provérbios 31:30", "Enganosa é a graça e vã é a formosura, mas a mulher que teme ao SENHOR, essa sim será louvada."),

    # Isaias (mais)
    ("Isaías 12:2", "Eis que Deus é a minha salvação; confiarei, e não me recearei; porque o SENHOR DEUS é a minha força e o meu cântico."),
    ("Isaías 25:1", "SENHOR, tu és o meu Deus; exaltar-te-ei, louvarei o teu nome, porque fizeste maravilhas."),
    ("Isaías 30:15", "Na conversão e no repouso, nisto sereis salvos; na quietação e na confiança está a vossa força."),
    ("Isaías 33:22", "Porque o SENHOR é o nosso Juiz, o SENHOR é o nosso Legislador, o SENHOR é o nosso Rei; ele nos salvará."),
    ("Isaías 40:8", "Seca-se a erva, cai a flor, mas a palavra do nosso Deus subsiste para sempre."),
    ("Isaías 44:22", "Apaguei as tuas transgressões como a névoa, e os teus pecados como a nuvem; volta-te para mim, porque eu te redimi."),
    ("Isaías 45:2", "Eu irei adiante de ti, e farei que os lugares tortuosos se endireitem."),
    ("Isaías 48:17", "Eu sou o SENHOR teu Deus, que te ensina o que é proveitoso, e te guia pelo caminho em que deves andar."),
    ("Isaías 54:17", "Nenhuma arma forjada contra ti prosperará."),

    # Jeremias (mais)
    ("Jeremias 1:5", "Antes que te formasse no ventre materno, eu te conheci; antes que saísses do ventre, eu te santifiquei."),
    ("Jeremias 17:14", "Cura-me, ó SENHOR, e serei curado; salva-me, e serei salvo; porque tu és o meu louvor."),
    ("Jeremias 31:34", "Porque eu perdoarei a sua iniquidade e não me lembrarei mais dos seus pecados."),
    ("Jeremias 32:27", "Eis que eu sou o SENHOR, o Deus de toda a carne; haverá alguma coisa demasiado difícil para mim?"),

    # Lamentacoes (mais)
    ("Lamentações 3:26", "Bom é aguardar em silêncio a salvação do SENHOR."),
    ("Lamentações 3:40", "Sondemos e provemos os nossos caminhos e voltemos para o SENHOR."),

    # Daniel
    ("Daniel 2:20", "Bendito seja o nome de Deus para todo o sempre, porque o poder e a sabedoria são seus."),
    ("Daniel 6:26", "Porque ele é o Deus vivo e permanece para sempre, e o seu reino jamais será destruído."),
    ("Daniel 10:19", "Não temas; sê forte; sê forte! E, enquanto ele me falava, cobrei forças."),

    # Oseas
    ("Oséias 6:3", "Conheçamos, e sigamos a conhecer o SENHOR; a sua saída é certa como a alva da manhã."),
    ("Oséias 14:4", "Sararei a sua apostasia, amarei-os livremente; porque a minha ira se desviou deles."),

    # Joel (mais)
    ("Joel 2:13", "Rasgai o vosso coração, e não as vossas vestes, e convertei-vos ao SENHOR vosso Deus; porque ele é misericordioso e compassivo."),

    # Amos
    ("Amós 5:4", "Assim diz o SENHOR à casa de Israel: Buscai-me, e vivereis."),

    # Miqueias
    ("Miquéias 7:7", "Mas eu olharei para o SENHOR; esperarei o Deus da minha salvação; o meu Deus me ouvirá."),
    ("Miquéias 7:18", "Quem é Deus como tu, que perdoa a iniquidade e passa por alto a transgressão do remanescente da sua herança?"),

    # Malaquias
    ("Malaquias 3:6", "Porque eu, o SENHOR, não mudo; por isso vós, ó filhos de Jacó, não sois consumidos."),
    ("Malaquias 3:10", "Trazei todos os dízimos à casa do tesouro, para que haja mantimento na minha casa; e provai-me nisto, diz o SENHOR dos Exércitos."),

    # Mateus (mais)
    ("Mateus 5:14", "Vós sois a luz do mundo; não se pode esconder uma cidade edificada sobre um monte."),
    ("Mateus 9:29", "Segundo a vossa fé, vos seja feito."),
    ("Mateus 10:30-31", "Ora, até os cabelos todos da vossa cabeça estão contados. Não temais, pois; sois de mais valor do que muitos pardais."),
    ("Mateus 11:30", "Porque o meu jugo é suave e o meu fardo é leve."),
    ("Mateus 24:35", "O céu e a terra passarão, mas as minhas palavras de modo algum passarão."),

    # Marcos (mais)
    ("Marcos 5:36", "Não temas, crê somente."),
    ("Marcos 10:45", "Porque o Filho do Homem veio, não para ser servido, mas para servir e dar a sua vida em resgate de muitos."),
    ("Marcos 16:15", "Ide por todo o mundo e pregai o evangelho a toda criatura."),

    # Lucas (mais)
    ("Lucas 4:18", "O Espírito do Senhor está sobre mim, pelo que me ungiu para evangelizar os pobres."),
    ("Lucas 10:19", "Eis que vos dou poder para pisar serpentes e escorpiões, e toda a força do inimigo; e nada vos poderá fazer dano."),
    ("Lucas 10:27", "Amarás ao Senhor teu Deus de todo o teu coração, de toda a tua alma, de todas as tuas forças e de todo o teu entendimento; e ao teu próximo como a ti mesmo."),
    ("Lucas 12:7", "Ora, até os cabelos da vossa cabeça estão todos contados. Não temais."),
    ("Lucas 17:6", "Se tiverdes fé como um grão de mostarda, direis a esta amoreira: Arranca-te e transplanta-te no mar; e ela vos obedeceria."),
    ("Lucas 21:33", "O céu e a terra passarão, mas as minhas palavras não passarão."),

    # Joao (mais)
    ("João 1:14", "E o Verbo se fez carne e habitou entre nós, e vimos a sua glória."),
    ("João 1:16", "Porque da sua plenitude todos nós recebemos, e graça por graça."),
    ("João 5:24", "Na verdade, na verdade vos digo que aquele que ouve a minha palavra e crê naquele que me enviou tem a vida eterna."),
    ("João 6:37", "Todo o que o Pai me dá virá a mim; e o que vem a mim de maneira nenhuma o lançarei fora."),
    ("João 7:37", "Se alguém tem sede, venha a mim e beba."),
    ("João 9:4", "É necessário que façamos as obras daquele que me enviou, enquanto é dia."),
    ("João 11:35", "Jesus chorou."),
    ("João 14:3", "E quando eu for e vos preparar lugar, voltarei e vos tomarei para mim mesmo."),
    ("João 14:16", "E eu rogarei ao Pai, e ele vos dará outro Consolador, para que fique convosco para sempre."),
    ("João 15:16", "Não me escolhestes vós a mim, mas eu vos escolhi a vós."),
    ("João 17:17", "Santifica-os na verdade; a tua palavra é a verdade."),
    ("João 20:29", "Bem-aventurados os que não viram e creram."),

    # Atos (mais)
    ("Atos 2:21", "E todo aquele que invocar o nome do Senhor será salvo."),
    ("Atos 2:38", "Arrependei-vos e cada um de vós seja batizado em nome de Jesus Cristo, para remissão dos pecados."),
    ("Atos 3:6", "Prata e ouro não tenho; porém o que tenho te dou: em nome de Jesus Cristo de Nazaré, levanta-te e anda."),
    ("Atos 4:31", "E, havendo orado, o lugar onde estavam reunidos tremeu; e todos foram cheios do Espírito Santo."),
    ("Atos 16:31", "Crê no Senhor Jesus Cristo e serás salvo, tu e a tua casa."),

    # Romanos (mais)
    ("Romanos 10:13", "Todo aquele que invocar o nome do Senhor será salvo."),
    ("Romanos 11:36", "Porque dele e por meio dele e para ele são todas as coisas; glória, pois, a ele eternamente."),
    ("Romanos 12:1", "Rogo-vos, irmãos, pela compaixão de Deus, que apresenteis os vossos corpos em sacrifício vivo, santo e agradável a Deus."),
    ("Romanos 12:2", "E não vos conformeis com este século, mas transformai-vos pela renovação da vossa mente."),
    ("Romanos 12:10", "Amai-vos cordialmente uns aos outros com amor fraternal; preferindo-vos em honra uns aos outros."),
    ("Romanos 12:12", "Regozijai-vos na esperança, sede pacientes na tribulação, perseverantes na oração."),
    ("Romanos 15:13", "Ora, o Deus de esperança vos encha de todo o gozo e paz no crer, para que abundeis em esperança pelo poder do Espírito Santo."),

    # 1 Corintios (mais)
    ("1 Coríntios 2:9", "O que os olhos não viram, nem os ouvidos ouviram, nem o coração do homem imaginou, isso Deus preparou para os que o amam."),
    ("1 Coríntios 3:16", "Não sabeis que sois o templo de Deus e que o Espírito de Deus habita em vós?"),
    ("1 Coríntios 10:13", "Não veio sobre vós tentação que não fosse humana; mas Deus é fiel, e não permitirá que sejais tentados além do que podeis suportar."),
    ("1 Coríntios 13:4-5", "O amor é paciente, é benigno; o amor não arde em ciúmes, não se ufana, não se ensoberbece; não se conduz inconvenientemente."),
    ("1 Coríntios 13:7", "Tudo sofre, tudo crê, tudo espera, tudo suporta."),
    ("1 Coríntios 13:13", "Agora, pois, permanecem a fé, a esperança e o amor, estes três; mas o maior destes é o amor."),
    ("1 Coríntios 15:57", "Mas graças a Deus, que nos dá a vitória por nosso Senhor Jesus Cristo."),
    ("1 Coríntios 16:13", "Vigiai, permanecei firmes na fé, portai-vos varonilmente, fortalecei-vos."),

    # 2 Corintios (mais)
    ("2 Coríntios 1:3-4", "Bendito seja o Deus e Pai de nosso Senhor Jesus Cristo, o Pai de misericórdias e Deus de toda a consolação; o qual nos consola em toda a nossa tribulação."),
    ("2 Coríntios 4:7", "Mas temos este tesouro em vasos de barro, para que a excelência do poder seja de Deus e não de nós."),
    ("2 Coríntios 4:17", "Porque este momentâneo e leve peso de tribulação nos produz uma eterna e excelente glória."),
    ("2 Coríntios 5:7", "Porque andamos por fé e não por vista."),
    ("2 Coríntios 5:17", "Assim que, se alguém está em Cristo, nova criatura é; as coisas antigas já passaram; eis que tudo se fez novo."),
    ("2 Coríntios 5:21", "Porque aquele que não conheceu pecado, por nós o fez pecado, para que, nele, fôssemos feitos justiça de Deus."),
    ("2 Coríntios 6:2", "Eis o momento favorável; eis o dia da salvação!"),
    ("2 Coríntios 9:7", "Deus ama quem dá com alegria."),
    ("2 Coríntios 12:9", "A minha graça te basta, porque o meu poder se aperfeiçoa na fraqueza."),

    # Galatas (mais)
    ("Gálatas 2:20", "Já estou crucificado com Cristo; e vivo, não mais eu, mas Cristo vive em mim."),
    ("Gálatas 5:1", "Foi para a liberdade que Cristo nos libertou. Permanecei, pois, firmes, e não vos submetais novamente ao jugo da escravidão."),
    ("Gálatas 5:22-23", "Mas o fruto do Espírito é: amor, alegria, paz, longanimidade, benignidade, bondade, fidelidade, mansidão, domínio próprio."),
    ("Gálatas 6:9", "E não nos cansemos de fazer o bem, porque a seu tempo ceifaremos, se não tivermos desanimado."),

    # Efesios (mais)
    ("Efésios 1:7", "Em quem temos a redenção pelo seu sangue, a remissão das ofensas, segundo as riquezas da sua graça."),
    ("Efésios 1:17", "Para que o Deus de nosso Senhor Jesus Cristo, o Pai de glória, vos dê o espírito de sabedoria e de revelação no pleno conhecimento dele."),
    ("Efésios 2:8", "Porque pela graça sois salvos, por meio da fé; e isso não vem de vós; é dom de Deus."),
    ("Efésios 3:16", "Para que vos conceda que sejais corroborados com poder pelo seu Espírito no homem interior."),
    ("Efésios 3:20", "Ora, àquele que é poderoso para fazer tudo muito mais abundantemente além do que pedimos ou pensamos."),
    ("Efésios 4:32", "Sede bondosos e compassivos uns para com os outros, perdoando-vos mutuamente."),
    ("Efésios 6:10", "Finalmente, irmãos, fortalecei-vos no Senhor e na força do seu poder."),
    ("Efésios 6:11", "Revesti-vos de toda a armadura de Deus, para que possais ficar firmes contra as ciladas do diabo."),

    # Filipenses (mais)
    ("Filipenses 1:6", "Tendo por certo que o que em vós começou a boa obra a aperfeiçoará até ao dia de Jesus Cristo."),
    ("Filipenses 2:5", "Haja em vós o mesmo sentimento que houve em Cristo Jesus."),
    ("Filipenses 4:6", "Não andeis ansiosos por coisa alguma; antes em tudo, pela oração e pela súplica com ação de graças, apresentai as vossas petições a Deus."),
    ("Filipenses 4:7", "E a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos pensamentos em Cristo Jesus."),

    # Colossenses (mais)
    ("Colossenses 1:16", "Porque nele foram criadas todas as coisas, nos céus e na terra, as visíveis e as invisíveis."),
    ("Colossenses 3:1", "Portanto, se fostes ressuscitados com Cristo, buscai as coisas que são lá do alto."),
    ("Colossenses 3:2", "Pensai nas coisas que são lá do alto, não nas que são da terra."),
    ("Colossenses 3:17", "E tudo quanto fizerdes, seja em palavra ou em obra, fazei tudo em nome do Senhor Jesus."),
    ("Colossenses 3:23", "E tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor e não aos homens."),

    # 1 Tessalonicenses (mais)
    ("1 Tessalonicenses 4:16", "Porque o mesmo Senhor descerá do céu com alarido, com voz de arcanjo e com a trombeta de Deus."),
    ("1 Tessalonicenses 5:16-18", "Regozijai-vos sempre. Orai sem cessar. Em tudo dai graças, porque esta é a vontade de Deus em Cristo Jesus para convosco."),

    # 2 Tessalonicenses (mais)
    ("2 Tessalonicenses 3:3", "Mas o Senhor é fiel, que vos confirmará e guardará do mal."),

    # 1 Timoteo
    ("1 Timóteo 1:17", "Ao Rei dos séculos, immortal, invisível, o único e sábio Deus, sejam honra e glória pelos séculos dos séculos."),
    ("1 Timóteo 2:5", "Porque há um só Deus e um só Mediador entre Deus e os homens, Jesus Cristo homem."),
    ("1 Timóteo 6:6", "Mas é grande ganho a piedade com contentamento."),
    ("1 Timóteo 6:12", "Combate o bom combate da fé, lança mão da vida eterna."),

    # 2 Timoteo (mais)
    ("2 Timóteo 1:7", "Porque Deus não nos deu o espírito de temor, mas de poder, de amor e de moderação."),
    ("2 Timóteo 2:13", "Se somos infiéis, ele permanece fiel; ele não pode negar-se a si mesmo."),
    ("2 Timóteo 3:16-17", "Toda a Escritura é divinamente inspirada e útil para ensinar, para repreender, para corrigir, para instruir em justiça."),
    ("2 Timóteo 4:7", "Combati o bom combate, acabei a carreira, guardei a fé."),

    # Hebreus (mais)
    ("Hebreus 2:18", "Porque, tendo ele mesmo sido tentado e sofrido, é poderoso para socorrer os que são tentados."),
    ("Hebreus 6:10", "Porque Deus não é injusto para se esquecer da vossa obra e do trabalho do amor."),
    ("Hebreus 6:19", "A qual esperança temos como âncora da alma, segura e firme."),
    ("Hebreus 7:25", "Pelo que também pode salvar perfeitamente os que por ele se aproximam de Deus."),
    ("Hebreus 9:14", "Quanto mais o sangue de Cristo, que pelo Espírito eterno se ofereceu a si mesmo imaculado a Deus, purificará a vossa consciência."),
    ("Hebreus 10:35-36", "Não abandoneis, pois, a vossa confiança, a qual tem grande galardão. Porque necessitais de paciência."),
    ("Hebreus 11:3", "Pela fé entendemos que os mundos foram criados pela palavra de Deus."),
    ("Hebreus 12:28", "Assim, recebendo um reino que não pode ser abalado, retenhamos a graça, pela qual sirvamos a Deus agradavelmente."),
    ("Hebreus 13:6", "Assim que, podemos dizer com toda a confiança: O Senhor é o meu ajudador; não temerei o que me possa fazer o homem."),

    # Tiago (mais)
    ("Tiago 1:2-3", "Meus irmãos, tende grande alegria quando cairdes em diversas tentações, sabendo que a prova da vossa fé produz a paciência."),
    ("Tiago 1:17", "Todo o bom donativo e todo o dom perfeito vêm do alto, descendo do Pai das luzes."),
    ("Tiago 2:17", "Assim também a fé, se não tiver obras, é morta em si mesma."),
    ("Tiago 4:10", "Humilhai-vos perante o Senhor, e ele vos exaltará."),
    ("Tiago 5:11", "Eis que chamamos bem-aventurados os que sofreram; ouvistes da paciência de Jó e vistes o fim que o Senhor lhe deu."),
    ("Tiago 5:15", "E a oração da fé salvará o enfermo."),

    # 1 Pedro (mais)
    ("1 Pedro 1:3", "Bendito seja o Deus e Pai de nosso Senhor Jesus Cristo que, segundo a sua grande misericórdia, nos regenerou para uma viva esperança."),
    ("1 Pedro 1:25", "A palavra do Senhor permanece para sempre."),
    ("1 Pedro 3:9", "Não tornando o mal pelo mal, nem injúria por injúria; antes, pelo contrário, bendizendo."),
    ("1 Pedro 4:8", "Mas, sobretudo, tende ardente amor uns para com os outros; porque o amor cobre uma multidão de pecados."),
    ("1 Pedro 4:10", "Administrai uns aos outros, cada um conforme o dom que recebeu, como bons despenseiros da multiforme graça de Deus."),

    # 2 Pedro
    ("2 Pedro 1:3", "Como o seu divino poder nos tem dado tudo o que diz respeito à vida e à piedade."),
    ("2 Pedro 1:4", "Pelos quais nos foram dadas grandíssimas e preciosas promessas, para que por elas sejais participantes da natureza divina."),
    ("2 Pedro 3:9", "O Senhor não retarda a sua promessa, ainda que alguns a têm por tardança; mas é longânimo para convosco."),
    ("2 Pedro 3:18", "Crescei na graça e no conhecimento de nosso Senhor e Salvador Jesus Cristo."),

    # 1 Joao (mais)
    ("1 João 2:1", "Meus filhinhos, estas coisas vos escrevo para que não pequeis; e, se alguém pecar, temos um Advogado junto ao Pai, Jesus Cristo, o justo."),
    ("1 João 2:17", "O mundo passa, e a sua concupiscência; mas aquele que faz a vontade de Deus permanece para sempre."),
    ("1 João 3:18", "Meus filhinhos, não amemos de palavra, nem de língua, mas por obra e em verdade."),
    ("1 João 5:11", "E este é o testemunho: que Deus nos deu a vida eterna, e esta vida está em seu Filho."),

    # 2 Joao
    ("2 João 1:6", "E este é o amor: que andemos segundo os seus mandamentos."),

    # 3 Joao
    ("3 João 1:2", "Amado, desejo que te vá bem em tudo e que tenhas saúde, assim como bem vai a tua alma."),

    # Judas
    ("Judas 1:20-21", "Vós, porém, amados, edificando-vos na vossa santíssima fé, orando no Espírito Santo, conservai-vos no amor de Deus."),
    ("Judas 1:24-25", "Ora, àquele que é poderoso para vos guardar de tropeçardes e vos apresentar com grandes alegrias diante da sua glória, ao único sábio Deus, nosso Salvador, seja glória e majestade."),

    # Apocalipse (mais)
    ("Apocalipse 2:10", "Sê fiel até à morte, e dar-te-ei a coroa da vida."),
    ("Apocalipse 3:10", "Porque guardaste a palavra da minha paciência, também eu te guardarei da hora da tentação."),
    ("Apocalipse 4:8", "Santo, Santo, Santo é o Senhor Deus, o Todo-Poderoso, que era, e que é, e que há de vir."),
    ("Apocalipse 5:12", "Digno é o Cordeiro que foi morto de receber o poder, e riquezas, e sabedoria, e força, e honra, e glória, e louvor."),
    ("Apocalipse 7:17", "Porque o Cordeiro que está no meio do trono os apascentará e os guiará para as fontes das águas da vida."),
    ("Apocalipse 11:15", "Os reinos do mundo vieram a ser de nosso Senhor e do seu Cristo, e ele reinará pelos séculos dos séculos."),
    ("Apocalipse 12:11", "E eles o venceram pelo sangue do Cordeiro e pela palavra do seu testemunho."),
    ("Apocalipse 19:6", "Aleluia! Pois reina o Senhor Deus, o Todo-Poderoso."),
    ("Apocalipse 21:3", "Eis o tabernáculo de Deus com os homens. Ele habitará com eles, e eles serão o seu povo."),
    ("Apocalipse 22:13", "Eu sou o Alfa e o Ômega, o primeiro e o último, o princípio e o fim."),
    ("Apocalipse 22:17", "E o Espírito e a esposa dizem: Vem. E o que ouve diga: Vem."),
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
    [(50, 20, 60), (142, 68, 173)],
    [(10, 50, 50), (26, 188, 156)],
    [(70, 30, 10), (211, 84, 0)],
    [(10, 30, 60), (41, 128, 185)],
]

_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
_FONTS_DIR = os.path.join(_SRC_DIR, "fonts")
_LOGO_PATH = os.path.join(_SRC_DIR, "logo_ad.png")

def _carregar_logo(tamanho=200):
    """Carrega o logo da AD, remove fundo branco/claro, converte para branco puro e redimensiona."""
    try:
        logo = Image.open(_LOGO_PATH).convert("RGBA")
        dados = logo.getdata()
        novos = []
        for r, g, b, a in dados:
            if r > 215 and g > 215 and b > 215:
                # Fundo branco/claro → totalmente transparente
                novos.append((0, 0, 0, 0))
            else:
                # Todo pixel visível do logo → branco puro (garante visibilidade em qualquer fundo escuro)
                novos.append((255, 255, 255, min(a, 255)))
        logo.putdata(novos)
        logo = logo.resize((tamanho, tamanho), Image.LANCZOS)
        return logo
    except Exception:
        return None

_URL_BOLD   = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSerif-Bold.ttf"
_URL_NORMAL = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSerif.ttf"

def _garantir_fontes_locais():
    """Baixa fontes DejaVu para a pasta src/fonts/ se não existirem."""
    import urllib.request
    os.makedirs(_FONTS_DIR, exist_ok=True)
    pares = [
        (os.path.join(_FONTS_DIR, "DejaVuSerif-Bold.ttf"), _URL_BOLD),
        (os.path.join(_FONTS_DIR, "DejaVuSerif.ttf"), _URL_NORMAL),
    ]
    for destino, url in pares:
        if not os.path.exists(destino):
            try:
                urllib.request.urlretrieve(url, destino)
            except Exception as e:
                logging.getLogger(__name__).warning(f"Não foi possível baixar fonte {url}: {e}")

try:
    _garantir_fontes_locais()
except Exception:
    pass

CAMINHOS_FONTE_BOLD = [
    os.path.join(_FONTS_DIR, "DejaVuSerif-Bold.ttf"),
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
    "/usr/share/fonts/TTF/DejaVuSerif-Bold.ttf",
]

CAMINHOS_FONTE_NORMAL = [
    os.path.join(_FONTS_DIR, "DejaVuSerif.ttf"),
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
    "/usr/share/fonts/TTF/DejaVuSerif.ttf",
]

def _carregar_fonte(caminhos, tamanho):
    for caminho in caminhos:
        if os.path.exists(caminho):
            try:
                return ImageFont.truetype(caminho, tamanho)
            except Exception:
                continue
    # Pillow 10+ aceita size= no load_default — muito melhor que sem parâmetro
    try:
        return ImageFont.load_default(size=tamanho)
    except TypeError:
        return ImageFont.load_default()

def get_saudacao():
    import datetime
    import pytz
    tz = pytz.timezone("America/Sao_Paulo")
    hora = datetime.datetime.now(tz).hour
    if 5 <= hora < 12:
        return "Bom dia!"
    elif 12 <= hora < 18:
        return "Boa tarde!"
    else:
        return "Boa noite!"

def gerar_imagem_versiculo():
    referencia, texto = random.choice(VERSICULOS)
    cores = random.choice(CORES_FUNDO)

    largura, altura = 1080, 1080

    img = Image.new("RGBA", (largura, altura), (*cores[0], 255))
    draw = ImageDraw.Draw(img)

    for i in range(altura):
        ratio = i / altura
        r = int(cores[0][0] + (cores[1][0] - cores[0][0]) * ratio)
        g = int(cores[0][1] + (cores[1][1] - cores[0][1]) * ratio)
        b = int(cores[0][2] + (cores[1][2] - cores[0][2]) * ratio)
        draw.line([(0, i), (largura, i)], fill=(r, g, b, 255))

    overlay = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for _ in range(8):
        x = random.randint(0, largura)
        y = random.randint(0, altura)
        r = random.randint(30, 120)
        overlay_draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 18))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    draw.rectangle([60, 60, largura - 60, altura - 60], outline=(255, 255, 255, 120), width=3)
    draw.rectangle([70, 70, largura - 70, altura - 70], outline=(255, 255, 255, 60), width=1)

    font_grande  = _carregar_fonte(CAMINHOS_FONTE_BOLD, 52)
    font_texto   = _carregar_fonte(CAMINHOS_FONTE_NORMAL, 38)
    font_ref     = _carregar_fonte(CAMINHOS_FONTE_BOLD, 42)
    font_pequena = _carregar_fonte(CAMINHOS_FONTE_NORMAL, 28)

    logo = _carregar_logo(tamanho=200)
    if logo:
        lx = (largura - logo.width) // 2
        ly = 95
        img.paste(logo, (lx, ly), logo)
    else:
        cruz = "✝"
        try:
            bbox = draw.textbbox((0, 0), cruz, font=font_grande)
            cw = bbox[2] - bbox[0]
            draw.text(((largura - cw) // 2, 120), cruz, font=font_grande, fill=(255, 255, 255, 255))
        except Exception:
            pass

    linhas = textwrap.wrap(texto, width=32)
    y_texto = 320
    espacamento = 55

    for linha in linhas:
        try:
            bbox = draw.textbbox((0, 0), linha, font=font_texto)
            lw = bbox[2] - bbox[0]
        except Exception:
            lw = len(linha) * 20
        x = (largura - lw) // 2
        draw.text((x + 2, y_texto + 2), linha, font=font_texto, fill=(0, 0, 0, 120))
        draw.text((x, y_texto), linha, font=font_texto, fill=(255, 255, 255, 255))
        y_texto += espacamento

    draw.line([200, y_texto + 20, largura - 200, y_texto + 20], fill=(255, 255, 255, 150), width=2)

    try:
        bbox = draw.textbbox((0, 0), referencia, font=font_ref)
        rw = bbox[2] - bbox[0]
    except Exception:
        rw = len(referencia) * 25
    draw.text(((largura - rw) // 2 + 2, y_texto + 42), referencia, font=font_ref, fill=(0, 0, 0, 120))
    draw.text(((largura - rw) // 2, y_texto + 40), referencia, font=font_ref, fill=(255, 215, 0, 255))

    rodape = "Avivamento AD"
    try:
        bbox = draw.textbbox((0, 0), rodape, font=font_pequena)
        pw = bbox[2] - bbox[0]
    except Exception:
        pw = len(rodape) * 14
    draw.text(((largura - pw) // 2, altura - 110), rodape, font=font_pequena, fill=(255, 255, 255, 200))

    img_rgb = img.convert("RGB")
    buf = io.BytesIO()
    img_rgb.save(buf, format="PNG")
    buf.seek(0)
    return buf, referencia, texto

def get_versiculo_texto():
    referencia, texto = random.choice(VERSICULOS)
    return referencia, texto
