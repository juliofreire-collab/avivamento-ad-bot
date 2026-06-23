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

    cruz = "+"
    try:
        bbox = draw.textbbox((0, 0), cruz, font=font_grande)
        cw = bbox[2] - bbox[0]
        draw.text(((largura - cw) // 2, 120), cruz, font=font_grande, fill=(255, 255, 255, 255))
    except Exception:
        pass

    linhas = textwrap.wrap(texto, width=32)
    y_texto = 220
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
