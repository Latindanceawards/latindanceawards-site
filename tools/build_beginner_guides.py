# Beginner and support guides built only from what the schools publish on their own websites (read 10 Nov 2026) and our ranking data:
#   es/bachata-para-principiantes   ("bachata para principiantes" 320/mo, SD 32; "aprender bachata" 140)
#   it/bachata-per-principianti     ("bachata per principianti" 320/mo, SD 32)
#   fr/apprendre-la-bachata         ("apprendre la bachata" 170/mo, SD 14)
#   pl/bachata-dla-poczatkujacych   ("bachata dla początkujących" 210/mo, SD 16)
#   it/corsi-di-bachata-milano      ("corsi di bachata milano" 110/mo, SD 14)
# SERP check (10 Nov 2026): none of these shares more than 3 results with its parent keyword; "bachata kurs hamburg/münchen/köln"
# and "bachata les amsterdam" share 6-10 results with their city pages, so they are NOT separate pages.
# Run after build_es/_schools, build_it/_schools, build_fr/_schools, build_pl/_schools:  python3 tools/build_beginner_guides.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_es as BE
import build_it as BI
import build_fr as BF
import build_pl as BP
from build import T, crumbs, faq_schema

def lk(u, n): return f'<a href="{u}" rel="noopener" target="_blank">{n}</a>'

def render(t, mod, sec, blocks):
    out = ''
    for b in blocks:
        if b[0] == 'p': out += t('p', b[1], b[2])
        elif b[0] == 'h3': out += '<h3>' + t('span', b[1], b[2]) + '</h3>'
        elif b[0] == 'ul': out += '<ul>' + ''.join(f'<li>{t("span", a, e)}</li>' for a, e in b[1]) + '</ul>'
    return out

def build(mod, pagefn, fname, prefix, c):
    t = T(prefix)
    h = mod.hero(t, c['kicker'], c['h1'], c['lede'], c['facts'](t), c['cta'](t))
    body = ''
    n = len(c['sections'])
    for i, (h2, blocks) in enumerate(c['sections'], 1):
        body += mod.sec(t, i, h2, render(t, mod, None, blocks), alt=(i % 2 == 1 and i != n))
    body += mod.faq_html(t, c['faq'])
    pagefn(fname, fname, c['title'][0], c['desc'][0], c['title'][1], c['desc'][1], h + body, t.en,
           [crumbs(c['crumb0'][0], c['crumb0'][1]), crumbs(c['title'][0].split(':')[0], fname), faq_schema(c['faq'])])

NOV = 'noviembre de 2026'
# ===================================================================== ESPAÑA
def es():
    P = BE.P; N = len(P.SCHOOLS); NC = len(P.CITIES)
    big = ['madrid', 'barcelona', 'valencia', 'malaga']
    cl_es = ', '.join(f'<a href="/es/bachata-{k}">{P.CITIES[k][0]}</a> ({len(BE.by_city(k))})' for k in big)
    cl_en = ', '.join(f'<a href="/es/bachata-{k}">{P.CITIES[k][1]}</a> ({len(BE.by_city(k))})' for k in big)
    c = dict(
        kicker=('Guía · Bachata para principiantes', 'Guide · Bachata for beginners'),
        h1=('Bachata para principiantes: cómo empezar, qué nivel elegir y qué cuesta', 'Bachata for beginners: how to start, which level to pick and what it costs'),
        lede=('Qué nivel buscar si nunca has bailado, si hace falta ir en pareja, cómo funcionan las clases de prueba y qué publican las escuelas sobre el precio de empezar. Solo datos de sus propias webs.',
              'Which level to look for if you have never danced, whether you need a partner, how trial classes work and what schools publish about the cost of starting. Only data from their own websites.'),
        facts=lambda t: [('check', 'Webs revisadas en <b>noviembre de 2026</b>', 'Websites checked in <b>November 2026</b>'), ('cal', f'<b>{N} escuelas</b> en {NC} ciudades', f'<b>{N} schools</b> in {NC} cities')],
        cta=lambda t: f'<a class="btn btn-gold" href="/es/clases-de-bachata">{t("span", "Guía de clases en España", "Class guide for Spain")}</a>',
        sections=[
            (('Qué nivel elegir si nunca has bailado', 'Which level to pick if you have never danced'), [
                ('p', 'Cada escuela pone nombre propio a su primer nivel, y conviene buscarlo en la web antes de reservar. ' + lk('https://bailale.es/', 'Bailalé') + ' (Huesca) publica un curso de «Iniciación» dentro de Salsa y Bachata y habla de un grupo para «empezar de cero, de cero de verdad». Salsabachata (Madrid) lo llama Nivel 0 Básico y Salsaragón (Zaragoza), «inicio 0». ' + lk('http://www.clasesdesalsaybachata.com/', 'Premiumdance') + ' (Madrid) anuncia «4 niveles diferenciados» de salsa y bachata, con grupos «desde iniciación hasta avanzado», y ' + lk('https://www.bailaparaserfeliz.es', 'Academia de Baile Guararé') + ' (Almería) dice que sus clases están diferenciadas por niveles, sin dar los nombres.',
                       'Each school names its first level differently, so look for it on the website before booking. ' + lk('https://bailale.es/', 'Bailalé') + ' (Huesca) lists an "Iniciación" course within Salsa and Bachata and mentions a group to "start from zero, truly from zero". Salsabachata (Madrid) calls it Level 0 Basic and Salsaragón (Zaragoza) "inicio 0". ' + lk('http://www.clasesdesalsaybachata.com/', 'Premiumdance') + ' (Madrid) advertises "4 distinct levels" of salsa and Bachata, with groups "from beginner to advanced", and ' + lk('https://www.bailaparaserfeliz.es', 'Academia de Baile Guararé') + ' (Almería) says its classes are separated by level without naming them.'),
                ('p', 'Los niveles no son equivalentes entre escuelas y la bachata de cada una puede ser moderna, sensual o tradicional. Por eso, antes de pagar, pregunta qué se enseña exactamente en el primer nivel.',
                      'Levels are not equivalent between schools, and each school\'s Bachata may be moderna, sensual or traditional. So before paying, ask what exactly is taught at the first level.')]),
            (('¿Hace falta ir en pareja?', 'Do you need to come with a partner?'), [
                ('p', 'Es la duda más habitual y varias escuelas la contestan en su web. Premiumdance escribe «No hace falta que vengas con pareja» y explica que las clases se equilibran por número de hombres y mujeres. Academia de Baile Guararé dice que se puede aprender «sin necesidad de traer pareja». Salsaragón ofrece grupos sin pareja y Salsabachata rota las parejas durante la clase. Bailalé no lo indica en la página que leímos.',
                      'It is the most common doubt and several schools answer it on their website. Premiumdance writes "you do not need to come with a partner" and explains that classes are balanced by the number of men and women. Academia de Baile Guararé says you can learn "without bringing a partner". Salsaragón offers groups without a partner and Salsabachata rotates partners during class. Bailalé does not say on the page we read.')]),
            (('Clase de prueba y precio de empezar', 'Trial class and the cost of starting'), [
                ('p', 'Esto es lo que publican las escuelas sobre probar y pagar, tal cual; los importes cambian cada temporada.',
                      'This is what schools publish about trying and paying, as stated; amounts change every season.'),
                ('ul', [('<strong>Premiumdance (Madrid):</strong> ofrece clase de prueba, sin precio en la página que leímos, y matrícula gratuita en algunas promociones, sin importes.', '<strong>Premiumdance (Madrid):</strong> offers a trial class, with no price on the page we read, and free enrolment in some promotions, without amounts.'),
                        ('<strong>Academia de Baile Guararé (Almería):</strong> invita a «Prueba una clase» sin precio y anuncia «Por sólo 45 € al mes» en clases grupales de salsa y bachata, sin precisar el nivel.', '<strong>Academia de Baile Guararé (Almería):</strong> invites you to "try a class" with no price and advertises "only €45 a month" for group salsa and Bachata classes, without stating the level.'),
                        ('<strong>Salsaragón (Zaragoza):</strong> clase de prueba de 10 €, que se descuenta de la primera mensualidad.', '<strong>Salsaragón (Zaragoza):</strong> €10 trial class, deducted from the first monthly fee.'),
                        ('<strong>Salsabachata (Madrid) y Baila con Sandra y Quique (Málaga):</strong> primera clase gratis; Salsabachata anuncia clases desde 4,75 € con créditos.', '<strong>Salsabachata (Madrid) and Baila con Sandra y Quique (Málaga):</strong> first class free; Salsabachata advertises classes from €4.75 with credits.'),
                        ('<strong>Bailalé (Huesca):</strong> no publica prueba ni precios en la página que leímos.', '<strong>Bailalé (Huesca):</strong> publishes no trial or prices on the page we read.')]),
                ('p', 'Es una muestra pequeña, no un precio medio. Pide siempre el precio mensual del grupo, las horas que incluye y si la clase de prueba se descuenta.',
                      'It is a small sample, not an average price. Always ask for the monthly group price, the hours it includes and whether the trial class is deducted.')]),
            (('Cómo elegir tu primer grupo', 'How to choose your first group'), [
                ('ul', [('Busca en la web el nombre del primer nivel (Iniciación, Nivel 0, inicio 0) y, si no aparece, pregunta cuál es.', 'Look on the website for the name of the first level (Iniciación, Level 0, inicio 0) and, if it does not appear, ask which it is.'),
                        ('Pregunta si el grupo se equilibra por número de hombres y mujeres o si se rotan parejas.', 'Ask whether the group is balanced by number of men and women or whether partners rotate.'),
                        ('Reserva la clase de prueba antes de pagar mensualidad o matrícula.', 'Book the trial class before paying a monthly fee or enrolment.'),
                        ('Comprueba la dirección: Bailalé indica C. J. Antonio Llanas Almudévar 12 (Huesca), Premiumdance Calle Ambros 34 (Madrid) y Guararé C/ Hermanos Pinzón 64 (Almería).', 'Check the address: Bailalé states C. J. Antonio Llanas Almudévar 12 (Huesca), Premiumdance Calle Ambros 34 (Madrid) and Guararé C/ Hermanos Pinzón 64 (Almería).')])]),
            (('Escuelas por ciudad', 'Schools by city'), [
                ('p', f'En nuestra lista hay {N} escuelas en {NC} ciudades españolas; las que más tienen son {cl_es}. Para direcciones, clases de prueba y precios por ciudad, consulta las guías de <a href="/es/clases-de-bachata-madrid">Madrid</a>, <a href="/es/clases-de-bachata-barcelona">Barcelona</a>, <a href="/es/clases-de-bachata-valencia">Valencia</a> y <a href="/es/clases-de-bachata-sevilla">Sevilla</a>, o la <a href="/es/clases-de-bachata">guía de clases de bachata en España</a>.',
                      f'Our list has {N} schools in {NC} Spanish cities; the ones with the most are {cl_en}. For addresses, trial classes and prices by city, see the guides for <a href="/es/clases-de-bachata-madrid">Madrid</a>, <a href="/es/clases-de-bachata-barcelona">Barcelona</a>, <a href="/es/clases-de-bachata-valencia">Valencia</a> and <a href="/es/clases-de-bachata-sevilla">Seville</a>, or the <a href="/es/clases-de-bachata">Bachata class guide for Spain</a>.')]),
            (('Cómo hemos preparado esta guía', 'How we prepared this guide'), [
                ('p', f'En {NOV} leímos las webs de Bailalé, Premiumdance, Academia de Baile Guararé y Txiki Bastida (Terrassa), y usamos datos de nuestras guías anteriores para Salsabachata, Salsaragón y Baila con Sandra y Quique. De Txiki Bastida no citamos nada: su página anuncia clases para todos los niveles de lunes a domingo, pero no publica niveles con nombre ni precios. No incluimos ningún dato que no hayamos podido comprobar. ¿Tienes una escuela y falta algo? <a href="/bewerbung.html?lang=en">Inscríbela gratis</a> o escríbenos.',
                      f'In November 2026 we read the websites of Bailalé, Premiumdance, Academia de Baile Guararé and Txiki Bastida (Terrassa), and we use data from our earlier guides for Salsabachata, Salsaragón and Baila con Sandra y Quique. We cite nothing from Txiki Bastida: its page advertises classes for all levels Monday to Sunday but publishes no named levels or prices. We include nothing we could not check. Run a school and something is missing? <a href="/bewerbung.html?lang=en">Enter it for free</a> or write to us.')]),
        ],
        faq=[
            ('¿Qué nivel elijo si nunca he bailado?', 'Which level should I pick if I have never danced?', 'El primero de la escuela: Iniciación en Bailalé, Nivel 0 Básico en Salsabachata o «inicio 0» en Salsaragón. Los nombres varían, así que pregunta qué se enseña en él.', 'The school\'s first level: Iniciación at Bailalé, Level 0 Basic at Salsabachata or "inicio 0" at Salsaragón. Names vary, so ask what is taught in it.'),
            ('¿Necesito pareja para empezar?', 'Do I need a partner to start?', 'No en las escuelas que lo indican: Premiumdance y Academia de Baile Guararé lo dicen en su web, y Salsaragón y Salsabachata lo permiten con grupos sin pareja o rotación.', 'Not at the schools that say so: Premiumdance and Academia de Baile Guararé state it on their website, and Salsaragón and Salsabachata allow it with groups without a partner or rotation.'),
            ('¿Puedo probar una clase gratis?', 'Can I try a class for free?', 'En algunas sí: Salsabachata y Baila con Sandra y Quique regalan la primera clase según sus webs. Salsaragón cobra 10 € y lo descuenta de la primera mensualidad.', 'At some, yes: Salsabachata and Baila con Sandra y Quique give the first class free according to their websites. Salsaragón charges €10 and deducts it from the first monthly fee.'),
            ('¿Cuánto cuesta empezar?', 'How much does it cost to start?', 'Pocas escuelas publican precios. Guararé anuncia 45 € al mes en clases grupales de salsa y bachata y Salsabachata, clases desde 4,75 € con créditos. Pregunta siempre antes de pagar.', 'Few schools publish prices. Guararé advertises €45 a month for group salsa and Bachata classes and Salsabachata classes from €4.75 with credits. Always ask before paying.'),
            ('¿Dónde hay clases para principiantes?', 'Where can I find beginner classes?', 'En las ciudades con más escuelas de nuestra lista: Madrid, Barcelona, Valencia y Málaga. Cada una tiene su página con las escuelas y su clasificación provisional.', 'In the cities with the most schools on our list: Madrid, Barcelona, Valencia and Málaga. Each has its page with the schools and their interim standing.'),
        ],
        title=('Bachata para principiantes: niveles, parejas y precios', 'Bachata for beginners: levels, partners and prices'),
        desc=('Bachata para principiantes: qué nivel elegir, si hace falta pareja, clases de prueba y precios publicados por Bailalé, Premiumdance, Guararé y otras escuelas.',
              'Bachata for beginners: which level to pick, whether you need a partner, trial classes and prices published by Bailalé, Premiumdance, Guararé and other schools.'),
        crumb0=('Bachata España', 'es/index.html'))
    build(BE, BE.es_page, 'es/bachata-para-principiantes.html', 'bg1', c)

# ===================================================================== ITALIA
def it():
    P = BI.P; N = len(P.SCHOOLS); NC = len(P.CITIES)
    big = ['roma', 'milano', 'torino', 'napoli', 'bologna']
    cl_it = ', '.join(f'<a href="/it/bachata-{k}">{P.CITIES[k][0]}</a> ({len(BI.by_city(k))})' for k in big)
    cl_en = ', '.join(f'<a href="/it/bachata-{k}">{P.CITIES[k][1]}</a> ({len(BI.by_city(k))})' for k in big)
    c = dict(
        kicker=('Guida · Bachata per principianti', 'Guide · Bachata for beginners'),
        h1=('Bachata per principianti: da che livello partire, partner e lezione di prova', 'Bachata for beginners: which level to start at, partners and the trial lesson'),
        lede=('Che livello scegliere se non hai mai ballato, se serve il partner, come funzionano le lezioni di prova e cosa pubblicano le scuole italiane sui loro siti. Solo dati dai siti delle scuole.',
              'Which level to choose if you have never danced, whether you need a partner, how trial lessons work and what Italian schools publish on their websites. Only data from the schools\' own sites.'),
        facts=lambda t: [('check', 'Siti consultati a <b>novembre 2026</b>', 'Websites checked in <b>November 2026</b>'), ('cal', f'<b>{N} scuole</b> in {NC} città', f'<b>{N} schools</b> in {NC} cities')],
        cta=lambda t: f'<a class="btn btn-gold" href="/it/corsi-di-bachata">{t("span", "Guida ai corsi in Italia", "Class guide for Italy")}</a>',
        sections=[
            (('Da che livello partire', 'Which level to start at'), [
                ('p', lk('https://bailacalienteasd.it/', 'Baila Caliente') + ' (Caserta) cita per gli adulti i livelli «principianti, intermedio e avanzato», ma la pagina non li riferisce in modo specifico alla bachata. Alla Timba Tumba di Torino il corso Principiante Salsa&Bachata dura 4 mesi (16 lezioni) e i corsi di bachata successivi, come Bachata Style, Bachata Moderna e Bachata Sensual, sono più brevi (8 lezioni). ' + lk('https://www.overdance.it', 'Over Dance') + ' (Villorba, Treviso) e ' + lk('https://aztecanacademy.it', 'Aztecan Academy') + ' (San Dorligo della Valle, Trieste) hanno una pagina dedicata al corso di bachata ma non indicano i livelli.',
                       lk('https://bailacalienteasd.it/', 'Baila Caliente') + ' (Caserta) cites the adult levels "beginners, intermediate and advanced", but the page does not tie them specifically to Bachata. At Timba Tumba in Turin the Beginner Salsa&Bachata course lasts 4 months (16 lessons) and the later Bachata courses, such as Bachata Style, Bachata Moderna and Bachata Sensual, are shorter (8 lessons). ' + lk('https://www.overdance.it', 'Over Dance') + ' (Villorba, Treviso) and ' + lk('https://aztecanacademy.it', 'Aztecan Academy') + ' (San Dorligo della Valle, Trieste) have a dedicated Bachata course page but do not state levels.'),
                ('p', 'Prima di iscriverti verifica se il corso è solo di bachata o misto con la salsa, e quante lezioni di bachata contiene davvero.',
                      'Before enrolling, check whether the course is Bachata only or mixed with salsa, and how many Bachata lessons it really contains.')]),
            (('Serve il partner?', 'Do you need a partner?'), [
                ('p', 'Over Dance scrive nella pagina dei corsi che le lezioni si possono prenotare «single o in coppia» e che i single vengono abbinati per compatibilità di età; la pagina non lo riferisce solo alla bachata. Baila Caliente e Aztecan Academy non lo indicano nelle pagine che abbiamo letto: chiedilo prima della prima lezione.',
                      'Over Dance writes on its courses page that lessons can be booked "single or as a couple" and that singles are paired by age compatibility; the page does not tie this to Bachata alone. Baila Caliente and Aztecan Academy do not say on the pages we read: ask before the first lesson.')]),
            (('Lezione di prova e prezzi', 'Trial lesson and prices'), [
                ('ul', [('<strong>Baila Caliente (Caserta):</strong> «prova gratuita», da prenotare via WhatsApp o telefono; ha sei sedi (Caserta, Santa Maria Capua Vetere, Vitulazio, Lusciano, Marcianise e Santa Maria a Vico).', '<strong>Baila Caliente (Caserta):</strong> "free trial", to be booked by WhatsApp or phone; it has six locations (Caserta, Santa Maria Capua Vetere, Vitulazio, Lusciano, Marcianise and Santa Maria a Vico).'),
                        ('<strong>Timba Tumba (Torino):</strong> la lezione di prova è gratuita, dura un\'ora ed è disponibile a qualsiasi livello.', '<strong>Timba Tumba (Turin):</strong> the trial lesson is free, lasts an hour and is available at any level.'),
                        ('<strong>Scuola di Ballo Sampaoli (Torino):</strong> indica sul sito una lezione di prova gratuita.', '<strong>Scuola di Ballo Sampaoli (Turin):</strong> lists a free trial lesson on its website.'),
                        ('<strong>Over Dance (Villorba):</strong> «Si pagano solamente le presenze» come regola generale e, nella sezione Open Day, «provare non costa nulla», senza riferirlo alla bachata.', '<strong>Over Dance (Villorba):</strong> "you only pay for attendances" as a general rule and, in the Open Day section, "trying costs nothing", without tying it to Bachata.'),
                        ('<strong>Aztecan Academy (Trieste):</strong> nessuna informazione su prova o prezzi nella pagina letta.', '<strong>Aztecan Academy (Trieste):</strong> no information on trial or prices on the page read.')]),
                ('p', 'Nessuna delle pagine lette riporta il prezzo di un corso di bachata. Chiedi il prezzo mensile, le lezioni incluse e se la prova viene scalata.',
                      'None of the pages read states the price of a Bachata course. Ask for the monthly price, the lessons included and whether the trial is deducted.')]),
            (('Come scegliere il primo corso', 'How to choose your first course'), [
                ('ul', [('Controlla se il corso principianti è solo bachata o misto e quante lezioni dura.', 'Check whether the beginner course is Bachata only or mixed and how many lessons it lasts.'),
                        ('Prenota la lezione di prova prima di pagare l\'iscrizione.', 'Book the trial lesson before paying the enrolment.'),
                        ('Verifica la sede: Over Dance indica Via F.lli Rosselli 17/24 (Villorba) e Aztecan Academy Via Josip Ressel 5 (San Dorligo della Valle).', 'Check the venue: Over Dance states Via F.lli Rosselli 17/24 (Villorba) and Aztecan Academy Via Josip Ressel 5 (San Dorligo della Valle).'),
                        ('Chiedi se il programma settimanale è aggiornato: alcune scuole lo pubblicano solo come PDF o immagine.', 'Ask whether the weekly timetable is up to date: some schools publish it only as a PDF or image.')])]),
            (('Prima della prima lezione', 'Before the first lesson'), [
                ('p', 'Timba Tumba (Via Arnaldo da Brescia 63, Torino) dichiara corsi di salsa, bachata e bachata sensual per tutti i livelli, in presenza e online: se non abiti vicino, chiedi quale formato include il corso principianti. Alcune domande utili da fare a qualsiasi scuola:',
                      'Timba Tumba (Via Arnaldo da Brescia 63, Turin) states courses in salsa, Bachata and Bachata sensual for all levels, in person and online: if you do not live nearby, ask which format the beginner course includes. Some useful questions to ask any school:'),
                ('ul', [('Quante lezioni dura il corso principianti e quante sono di bachata?', 'How many lessons does the beginner course last and how many are Bachata?'),
                        ('La prova è gratuita e si può fare a qualsiasi livello?', 'Is the trial free and can it be done at any level?'),
                        ('Il corso parte con un numero minimo di iscritti?', 'Does the course start with a minimum number of enrolments?')])]),
            (('Scuole per città', 'Schools by city'), [
                ('p', f'Nel nostro elenco ci sono {N} scuole in {NC} città italiane; quelle con più scuole sono {cl_it}. Per i corsi di una singola città consulta la <a href="/it/corsi-di-bachata-milano">guida ai corsi di bachata a Milano</a> o la <a href="/it/corsi-di-bachata">guida ai corsi di bachata in Italia</a>. I risultati definitivi saranno pubblicati in primavera 2027; fino ad allora mostriamo una classifica provvisoria basata su dati pubblici di ottobre 2026.',
                      f'Our list has {N} schools in {NC} Italian cities; the ones with the most are {cl_en}. For classes in a single city see the <a href="/it/corsi-di-bachata-milano">Bachata class guide for Milan</a> or the <a href="/it/corsi-di-bachata">Bachata class guide for Italy</a>. Final results follow in spring 2027; until then we show an interim standing based on public data from October 2026.')]),
            (('Come abbiamo preparato questa guida', 'How we prepared this guide'), [
                ('p', 'A novembre 2026 abbiamo letto i siti di Baila Caliente, Over Dance, Aztecan Academy e L\'officina della Salsa, e usiamo dati delle nostre guide precedenti per Timba Tumba e Sampaoli. Dell\'officina della Salsa non citiamo nulla: il sito nomina «Bachata Base» solo nelle recensioni dei clienti, non in un elenco ufficiale dei corsi. Non inseriamo dati che non abbiamo potuto verificare. Hai una scuola e manca qualcosa? <a href="/bewerbung.html?lang=en">Iscrivila gratis</a> o scrivici.',
                      'In November 2026 we read the websites of Baila Caliente, Over Dance, Aztecan Academy and L\'officina della Salsa, and use data from our earlier guides for Timba Tumba and Sampaoli. We cite nothing from L\'officina della Salsa: its site names "Bachata Base" only in customer reviews, not in an official course list. We include nothing we could not check. Run a school and something is missing? <a href="/bewerbung.html?lang=en">Enter it for free</a> or write to us.')]),
        ],
        faq=[
            ('Da che livello devo partire se non ho mai ballato?', 'Which level should I start at if I have never danced?', 'Dal corso principianti: alla Timba Tumba è il Principiante Salsa&Bachata, 4 mesi e 16 lezioni. Altre scuole non indicano il livello nella pagina: chiedilo.', 'From the beginner course: at Timba Tumba it is Beginner Salsa&Bachata, 4 months and 16 lessons. Other schools do not state the level on the page: ask.'),
            ('Serve il partner per iniziare?', 'Do I need a partner to start?', 'Over Dance indica che si può prenotare da soli o in coppia, e che i single vengono abbinati. Le altre scuole lette non lo specificano: chiedilo prima di iscriverti.', 'Over Dance states you can book alone or as a couple and that singles are paired. The other schools read do not specify: ask before enrolling.'),
            ('Posso provare una lezione gratis?', 'Can I try a lesson for free?', 'Sì in molte scuole: Baila Caliente, Timba Tumba e Sampaoli indicano una prova gratuita sui loro siti. Over Dance parla di Open Day in cui «provare non costa nulla».', 'Yes at many schools: Baila Caliente, Timba Tumba and Sampaoli state a free trial on their websites. Over Dance mentions an Open Day where "trying costs nothing".'),
            ('Quanto costa un corso di bachata?', 'How much does a Bachata course cost?', 'Le pagine che abbiamo letto non riportano il prezzo dei corsi di bachata. Chiedi sempre il prezzo mensile e le lezioni incluse prima di pagare.', 'The pages we read do not state Bachata course prices. Always ask for the monthly price and included lessons before paying.'),
            ('In quali città ci sono più scuole?', 'Which cities have the most schools?', f'Nel nostro elenco: Roma ({len(BI.by_city("roma"))}), Milano ({len(BI.by_city("milano"))}), Torino ({len(BI.by_city("torino"))}), Napoli ({len(BI.by_city("napoli"))}) e Bologna ({len(BI.by_city("bologna"))}). Alcune scuole hanno più sedi.', f'On our list: Rome ({len(BI.by_city("roma"))}), Milan ({len(BI.by_city("milano"))}), Turin ({len(BI.by_city("torino"))}), Naples ({len(BI.by_city("napoli"))}) and Bologna ({len(BI.by_city("bologna"))}). Some schools have several locations.'),
        ],
        title=('Bachata per principianti: livelli, partner e prova', 'Bachata for beginners: levels, partners and trial lessons'),
        desc=('Bachata per principianti: da che livello partire, se serve il partner, lezioni di prova e corsi pubblicati da Baila Caliente, Timba Tumba, Over Dance e altre scuole.',
              'Bachata for beginners: which level to start at, whether you need a partner, trial lessons and courses published by Baila Caliente, Timba Tumba, Over Dance and other schools.'),
        crumb0=('Bachata Italia', 'it/index.html'))
    build(BI, BI.it_page, 'it/bachata-per-principianti.html', 'bg2', c)

# ===================================================================== FRANCE
def fr():
    P = BF.P; N = len(P.SCHOOLS); NC = len(P.CITIES)
    big = ['paris', 'lyon', 'marseille', 'toulouse', 'montpellier']
    cl_fr = ', '.join(f'<a href="/fr/bachata-{k}">{P.CITIES[k][0]}</a> ({len(BF.by_city(k))})' for k in big)
    cl_en = ', '.join(f'<a href="/fr/bachata-{k}">{P.CITIES[k][1]}</a> ({len(BF.by_city(k))})' for k in big)
    c = dict(
        kicker=('Guide · Apprendre la bachata', 'Guide · Learning Bachata'),
        h1=('Apprendre la bachata : quel niveau choisir, partenaire et cours d’essai', 'Learning Bachata: which level to choose, partners and the trial class'),
        lede=('Quel niveau choisir si vous n’avez jamais dansé, s’il faut un partenaire, comment fonctionnent les cours d’essai et ce que les écoles publient sur les tarifs. Uniquement d’après leurs propres sites.',
              'Which level to choose if you have never danced, whether you need a partner, how trial classes work and what schools publish about prices. Only from their own websites.'),
        facts=lambda t: [('check', 'Sites consultés en <b>novembre 2026</b>', 'Websites checked in <b>November 2026</b>'), ('cal', f'<b>{N} écoles</b> dans {NC} villes', f'<b>{N} schools</b> in {NC} cities')],
        cta=lambda t: f'<a class="btn btn-gold" href="/fr/cours-de-bachata">{t("span", "Guide des cours en France", "Class guide for France")}</a>',
        sections=[
            (('Quel niveau choisir quand on débute', 'Which level to choose as a beginner'), [
                ('p', lk('https://urbanlatinoacademy.com', 'Urban Latino Dance Studio') + ' (Montpellier) propose « Bachata Niveau 1 (initiation) » le lundi de 19 h 30 à 20 h 30, plus un atelier « Bachata Atelier Technique Tous niveaux » le mardi. ' + lk('https://danselyon.fr', 'Cindy Martin Danseuse') + ' (Lyon) indique un cours collectif de bachata « NIVEAU : DÉBUTANT et INTERMÉDIAIRE » tous les vendredis de 20 h à 22 h. ' + lk('https://www.bachatafusionstrasbourg.fr', 'Bachata Fusion Strasbourg') + ' n’a pas de cours « débutant » nommé : son cours de bachata est ouvert à tous les niveaux et un « cours technique » est accessible après un an de danse.',
                       lk('https://urbanlatinoacademy.com', 'Urban Latino Dance Studio') + ' (Montpellier) offers "Bachata Level 1 (initiation)" on Mondays from 7:30 to 8:30 pm, plus a "Bachata Technical Workshop, all levels" on Tuesdays. ' + lk('https://danselyon.fr', 'Cindy Martin Danseuse') + ' (Lyon) lists a group Bachata class "LEVEL: BEGINNER and INTERMEDIATE" every Friday from 8 to 10 pm. ' + lk('https://www.bachatafusionstrasbourg.fr', 'Bachata Fusion Strasbourg') + ' has no named "beginner" class: its Bachata class is open to all levels and a "technical class" is accessible after one year of dancing.'),
                ('p', 'Les niveaux d’une école à l’autre ne se valent pas : avant de payer, demandez ce qui est enseigné dans le premier niveau et si le cours mélange débutants et intermédiaires.',
                      'Levels are not equivalent from one school to another: before paying, ask what is taught at the first level and whether the class mixes beginners and intermediates.')]),
            (('Faut-il un partenaire ?', 'Do you need a partner?'), [
                ('p', 'Bachata Fusion Strasbourg répond clairement : il n’est « pas nécessaire de venir accompagné pour commencer la bachata ». Les pages d’Urban Latino Dance Studio, de Cindy Martin, du Studio Garlisi (Saint-Martin-d’Hères) et de Kosta Danse (Grenoble) ne précisent pas si un partenaire est requis ; Kosta Danse classe la bachata parmi ses « danses en couple ». Posez la question avant le premier cours.',
                      'Bachata Fusion Strasbourg answers clearly: it is "not necessary to come accompanied to start Bachata". The pages of Urban Latino Dance Studio, Cindy Martin, Studio Garlisi (Saint-Martin-d’Hères) and Kosta Danse (Grenoble) do not say whether a partner is required; Kosta Danse lists Bachata among its "couple dances". Ask before the first class.')]),
            (('Cours d’essai et tarifs publiés', 'Trial classes and published prices'), [
                ('ul', [('<strong>Bachata Fusion Strasbourg :</strong> hors portes ouvertes de septembre, un essai coûte 15 € par heure et par personne ; les formules sont de 1 h, 2 h ou 3 h.', '<strong>Bachata Fusion Strasbourg:</strong> outside the September open days, a trial costs €15 per hour per person; formulas are 1, 2 or 3 hours.'),
                        ('<strong>Urban Latino Dance Studio :</strong> une « séance découverte » sans prix indiqué ; abonnement 1 cours par semaine à 31 € par mois (280 € par an, plus frais de dossier), 47 € pour 2 cours, 60 € pour 3 cours et 73 € le Full Pass illimité.', '<strong>Urban Latino Dance Studio:</strong> a "discovery session" with no price stated; one class a week at €31 a month (€280 a year, plus a file fee), €47 for 2 classes, €60 for 3 classes and €73 for the unlimited Full Pass.'),
                        ('<strong>Cindy Martin Danseuse (Lyon) :</strong> « 10 €/cours + conso », sans autre précision sur l’essai.', '<strong>Cindy Martin Danseuse (Lyon):</strong> "€10/class + drink", with no further detail on a trial.'),
                        ('<strong>Kosta Danse (Grenoble) :</strong> cours d’essai gratuit « dans la limite des places disponibles », sans le rattacher à la bachata.', '<strong>Kosta Danse (Grenoble):</strong> free trial class "subject to available places", without tying it to Bachata.'),
                        ('<strong>Studio Garlisi (Saint-Martin-d’Hères) :</strong> un cours d’essai est proposé à tous les nouveaux élèves, prix non indiqué.', '<strong>Studio Garlisi (Saint-Martin-d’Hères):</strong> a trial class is offered to all new students, price not stated.'),
                        ('<strong>SalsaNueva et Salsa con Elegua (Paris) :</strong> offre découverte à 99 € avec pack d’essai de huit cours sur 30 jours ; premier cours gratuit chez Elegua.', '<strong>SalsaNueva and Salsa con Elegua (Paris):</strong> €99 discovery offer with a trial pack of eight classes over 30 days; first class free at Elegua.')]),
                ('p', 'C’est un échantillon, pas un prix moyen. Demandez le prix mensuel, les heures incluses et si l’essai est déduit.',
                      'It is a sample, not an average price. Ask for the monthly price, the hours included and whether the trial is deducted.')]),
            (('Comment choisir son premier cours', 'How to choose your first class'), [
                ('ul', [('Cherchez le nom du premier niveau (initiation, débutant) et sa durée : 1 h par séance à Montpellier, 2 h à Lyon.', 'Look for the name of the first level (initiation, beginner) and its length: 1 hour per session in Montpellier, 2 hours in Lyon.'),
                        ('Réservez le cours d’essai avant de payer cotisation ou frais de dossier.', 'Book the trial class before paying a membership or file fee.'),
                        ('Vérifiez l’adresse : Bachata Fusion Strasbourg indique 1 rue de Bourgogne (Strasbourg), Urban Latino 200 allée Jean François Lesueur (Montpellier) et Kosta Danse 80 rue des Alliés (Grenoble).', 'Check the address: Bachata Fusion Strasbourg states 1 rue de Bourgogne (Strasbourg), Urban Latino 200 allée Jean François Lesueur (Montpellier) and Kosta Danse 80 rue des Alliés (Grenoble).'),
                        ('Demandez si le planning est à jour : certaines écoles le publient sur une page séparée.', 'Ask whether the timetable is up to date: some schools publish it on a separate page.')])]),
            (('Écoles par ville', 'Schools by city'), [
                ('p', f'Notre liste compte {N} écoles dans {NC} villes françaises ; celles qui en ont le plus sont {cl_fr}. Pour une ville, voyez le <a href="/fr/cours-de-bachata-paris">guide des cours de bachata à Paris</a> ou le <a href="/fr/cours-de-bachata">guide des cours de bachata en France</a>.',
                      f'Our list has {N} schools in {NC} French cities; the ones with the most are {cl_en}. For a single city see the <a href="/fr/cours-de-bachata-paris">Bachata class guide for Paris</a> or the <a href="/fr/cours-de-bachata">Bachata class guide for France</a>.')]),
            (('Comment nous avons préparé ce guide', 'How we prepared this guide'), [
                ('p', 'En novembre 2026, nous avons lu les sites d’Urban Latino Dance Studio, de Cindy Martin Danseuse, de Bachata Fusion Strasbourg, du Studio Garlisi, de Kosta Danse, de L’Atelier Danse Club et de Studio 7, et nous reprenons des données de nos guides précédents pour SalsaNueva et Salsa con Elegua. Nous ne citons rien de L’Atelier Danse Club (la bachata n’y est pas listée comme cours), ni de Studio 7 (fermé temporairement, réouverture annoncée en septembre 2027), ni d’Alma Dance, dont le site n’a pas pu être lu automatiquement. Nous n’incluons aucune donnée que nous n’avons pas pu vérifier. Vous dirigez une école ? <a href="/bewerbung.html?lang=en">Inscrivez-la gratuitement</a> ou écrivez-nous.',
                      'In November 2026 we read the websites of Urban Latino Dance Studio, Cindy Martin Danseuse, Bachata Fusion Strasbourg, Studio Garlisi, Kosta Danse, L’Atelier Danse Club and Studio 7, and we reuse data from our earlier guides for SalsaNueva and Salsa con Elegua. We cite nothing from L’Atelier Danse Club (Bachata is not listed as a class there), nor from Studio 7 (temporarily closed, reopening announced for September 2027), nor from Alma Dance, whose site could not be read automatically. We include nothing we could not check. Run a school? <a href="/bewerbung.html?lang=en">Enter it for free</a> or write to us.')]),
        ],
        faq=[
            ('Quel niveau choisir si je n’ai jamais dansé ?', 'Which level should I choose if I have never danced?', 'Le premier niveau : « Bachata Niveau 1 (initiation) » à Urban Latino Dance Studio, ou « débutant et intermédiaire » chez Cindy Martin à Lyon. Demandez ce qui y est enseigné.', 'The first level: "Bachata Level 1 (initiation)" at Urban Latino Dance Studio, or "beginner and intermediate" at Cindy Martin in Lyon. Ask what is taught there.'),
            ('Faut-il un partenaire pour commencer la bachata ?', 'Do I need a partner to start Bachata?', 'Non à Strasbourg : l’école écrit qu’il n’est pas nécessaire de venir accompagné. Les autres écoles lues ne le précisent pas ; posez la question.', 'Not in Strasbourg: the school writes that coming accompanied is not necessary. The other schools read do not say; ask.'),
            ('Peut-on essayer un cours gratuitement ?', 'Can I try a class for free?', 'Parfois : Kosta Danse (Grenoble) annonce un essai gratuit dans la limite des places, et Salsa con Elegua (Paris) offre le premier cours. Bachata Fusion Strasbourg facture 15 € l’essai hors portes ouvertes.', 'Sometimes: Kosta Danse (Grenoble) announces a free trial subject to places, and Salsa con Elegua (Paris) gives the first class. Bachata Fusion Strasbourg charges €15 for a trial outside open days.'),
            ('Combien coûte un cours de bachata ?', 'How much does a Bachata class cost?', 'Peu d’écoles publient leurs tarifs. Urban Latino à Montpellier annonce 31 € par mois pour 1 cours par semaine et Cindy Martin à Lyon 10 € le cours plus une consommation.', 'Few schools publish their prices. Urban Latino in Montpellier advertises €31 a month for one class a week and Cindy Martin in Lyon €10 a class plus a drink.'),
            ('Où apprendre la bachata en France ?', 'Where can I learn Bachata in France?', 'Dans les villes qui comptent le plus d’écoles dans notre liste : Paris, Lyon, Marseille, Toulouse et Montpellier. Chacune a sa page avec le classement provisoire.', 'In the cities with the most schools on our list: Paris, Lyon, Marseille, Toulouse and Montpellier. Each has its page with the interim standing.'),
        ],
        title=('Apprendre la bachata : niveaux, partenaire et essai', 'Learning Bachata: levels, partners and trial classes'),
        desc=('Apprendre la bachata : quel niveau choisir, faut-il un partenaire, cours d’essai et tarifs publiés par Urban Latino, Bachata Fusion Strasbourg, Cindy Martin et d’autres écoles.',
              'Learning Bachata: which level to choose, whether you need a partner, trial classes and prices published by Urban Latino, Bachata Fusion Strasbourg, Cindy Martin and other schools.'),
        crumb0=('Bachata France', 'fr/index.html'))
    build(BF, BF.fr_page, 'fr/apprendre-la-bachata.html', 'bg3', c)

# ===================================================================== POLSKA
def pl():
    P = BP.P; N = len(P.SCHOOLS); NC = len(P.CITIES)
    names = {'warszawa': 'Warszawa', 'krakow': 'Kraków', 'wroclaw': 'Wrocław', 'poznan': 'Poznań', 'gdansk': 'Gdańsk'}
    cl_pl = ', '.join(f'<a href="/pl/bachata-{k}">{v}</a> ({len(BP.by_city(k))})' for k, v in names.items())
    c = dict(
        kicker=('Poradnik · Bachata dla początkujących', 'Guide · Bachata for beginners'),
        h1=('Bachata dla początkujących: jaki poziom wybrać, partner i lekcja próbna', 'Bachata for beginners: which level to choose, partners and the trial lesson'),
        lede=('Jaki poziom wybrać, jeśli nigdy nie tańczyłeś, czy potrzebny jest partner, jak wyglądają lekcje próbne i co szkoły podają o cenach. Tylko dane z ich własnych stron.',
              'Which level to choose if you have never danced, whether you need a partner, how trial lessons work and what schools say about prices. Only data from their own websites.'),
        facts=lambda t: [('check', 'Strony sprawdzone w <b>listopadzie 2026</b>', 'Websites checked in <b>November 2026</b>'), ('cal', f'<b>{N} szkół</b> w {NC} miastach', f'<b>{N} schools</b> in {NC} cities')],
        cta=lambda t: f'<a class="btn btn-gold" href="/pl/">{t("span", "Zobacz ranking Polski", "See the Poland ranking")}</a>',
        sections=[
            (('Jaki poziom wybrać na start', 'Which level to pick to start'), [
                ('p', lk('https://loftodance.pl', 'LOFToDANCE') + ' (Kraków) podaje we wtorki o 18:00–19:50 dwa kursy: „Bachata: Witaj szkoło :)” na poziomie podstawowym oraz „Bachata od zera” na poziomie „Od zera”. ' + 'Prowadzącymi są według strony Claudio Mineo i Aleksandra Zych (kurs podstawowy) oraz Łukasz Raś i Ewa Jankowska (kurs „od zera”); recepcja pracuje od poniedziałku do piątku w godzinach 17:30–22:30. ' + lk('https://www.nolimits.art.pl', 'No Limits') + ' (Wrocław) ma w sekcji „Taniec w parach” kurs „Bachata od podstaw” w środy o 18:30. ' + lk('https://salsalibre.pl', 'Salsa Libre') + ' (Warszawa) wymienia ogólny poziom „Starter” dla osób zaczynających, ale nie wskazuje konkretnego kursu bachaty. ' + lk('https://art-dance.com.pl', 'Art Dance') + ' (Poznań) opisuje trzy odmiany bachaty (Dominicana, Moderna i Sensual) i nie podaje poziomów.',
                       lk('https://loftodance.pl', 'LOFToDANCE') + ' (Kraków) lists two courses on Tuesdays at 6:00–7:50 pm: "Bachata: Witaj szkoło :)" at basic level and "Bachata od zera" at "from scratch" level. ' + 'According to the page, the instructors are Claudio Mineo and Aleksandra Zych (basic course) and Łukasz Raś and Ewa Jankowska ("from scratch" course); reception is open Monday to Friday, 5:30–10:30 pm. ' + lk('https://www.nolimits.art.pl', 'No Limits') + ' (Wrocław) has a "Bachata od podstaw" (Bachata from the basics) course on Wednesdays at 6:30 pm in its "Couple dance" section. ' + lk('https://salsalibre.pl', 'Salsa Libre') + ' (Warsaw) mentions a general "Starter" level for beginners but names no specific Bachata course. ' + lk('https://art-dance.com.pl', 'Art Dance') + ' (Poznań) describes three varieties of Bachata (Dominicana, Moderna and Sensual) and states no levels.'),
                ('p', 'Terminy zmieniają się co sezon, więc sprawdź aktualny grafik. Zapytaj też, której odmiany bachaty uczy się na pierwszym poziomie.',
                      'Dates change every season, so check the current timetable. Also ask which variety of Bachata is taught at the first level.')]),
            (('Czy potrzebny jest partner?', 'Do you need a partner?'), [
                ('p', 'Salsa Libre pisze, że na zajęciach w parach nie trzeba mieć partnera, bo można go znaleźć na sali; zapisy są indywidualne, a kurs może się nie odbyć, jeśli zgłosi się mniej niż 8 par lub 6 osób solo. Art Dance prowadzi zajęcia salsy i bachaty dla par i singli. LOFToDANCE i No Limits nie podają tego na odczytanych stronach.',
                      'Salsa Libre writes that in partner classes you do not need a partner because you can find one in the room; enrolment is individual and a course may not run if fewer than 8 couples or 6 solo dancers sign up. Art Dance runs salsa and Bachata classes for couples and singles. LOFToDANCE and No Limits do not state this on the pages read.')]),
            (('Lekcja próbna i ceny', 'Trial lesson and prices'), [
                ('p', 'Na odczytanych stronach żadna z czterech szkół nie podaje ceny lekcji próbnej ani kursu: LOFToDANCE, Art Dance i Salsa Libre odsyłają do osobnego cennika, a No Limits nie podaje cen na stronie głównej. Salsa Libre pisze ogólnie, że wiele kursów regularnych trwa dwie godziny, a kursy weekendowe zwykle trzy.',
                      'On the pages read, none of the four schools states the price of a trial lesson or a course: LOFToDANCE, Art Dance and Salsa Libre point to a separate price list, and No Limits shows no prices on its main page. Salsa Libre says in general that many regular courses last two hours and weekend courses usually three.'),
                ('p', 'Zapytaj więc o cenę miesięczną, liczbę godzin i to, czy lekcja próbna jest płatna.',
                      'So ask for the monthly price, the number of hours and whether the trial lesson is paid.')]),
            (('Jak wybrać pierwszą grupę', 'How to choose your first group'), [
                ('ul', [('Poszukaj nazwy pierwszego poziomu („podstawowy”, „od zera”, „od podstaw”, „Starter”) i zapytaj, co obejmuje.', 'Look for the name of the first level ("basic", "from scratch", "from the basics", "Starter") and ask what it covers.'),
                        ('Zapytaj, czy kurs ma minimalną liczbę osób: w Salsa Libre to 8 par lub 6 osób solo.', 'Ask whether the course has a minimum number of participants: at Salsa Libre it is 8 couples or 6 solo dancers.'),
                        ('Sprawdź adres: LOFToDANCE podaje Kamienna 2-4 (Kraków), a Art Dance ul. Promienista 104 (Poznań).', 'Check the address: LOFToDANCE states Kamienna 2-4 (Kraków) and Art Dance ul. Promienista 104 (Poznań).'),
                        ('Zarezerwuj lekcję próbną przed wpłatą za kurs.', 'Book the trial lesson before paying for a course.')])]),
            (('Pytania do zadania szkole przed zapisem', 'Questions to ask the school before enrolling'), [
                ('ul', [('Który kurs jest pierwszym poziomem i jakiej odmiany bachaty uczy (Dominicana, Moderna, Sensual)?', 'Which course is the first level and which variety of Bachata does it teach (Dominicana, Moderna, Sensual)?'),
                        ('Kto prowadzi zajęcia i ile osób musi się zapisać, żeby kurs ruszył?', 'Who teaches the class and how many people must enrol for the course to run?'),
                        ('Czy lekcja próbna jest płatna i czy cena jest odliczana od kursu?', 'Is the trial lesson paid and is its price deducted from the course?'),
                        ('Ile trwa zajęcie i ile godzin w miesiącu obejmuje opłata?', 'How long is a class and how many hours a month does the fee include?')])]),
            (('Szkoły według miast', 'Schools by city'), [
                ('p', f'W naszym zestawieniu jest {N} szkół w {NC} polskich miastach; najwięcej mają {cl_pl}. Każde miasto ma własną stronę z wynikami tymczasowymi. Wyniki końcowe rankingu opublikujemy wiosną 2027 roku; do tego czasu pokazujemy zestawienie tymczasowe oparte na danych publicznych z października 2026.',
                      f'Our list has {N} schools in {NC} Polish cities; the cities with the most are ' + ', '.join(f'<a href="/pl/bachata-{k}">{v}</a> ({len(BP.by_city(k))})' for k, v in names.items()) + '. Each city has its own page with the interim standing. Final results follow in spring 2027; until then we show an interim standing based on public data from October 2026.')]),
            (('Jak przygotowaliśmy ten poradnik', 'How we prepared this guide'), [
                ('p', 'W listopadzie 2026 przeczytaliśmy strony LOFToDANCE, No Limits, Art Dance, Salsa Libre i Dance Flow. Z Dance Flow nie cytujemy nic: strona wymaga JavaScriptu i nie udało się jej odczytać automatycznie. Nie podajemy danych, których nie mogliśmy sprawdzić. Prowadzisz szkołę i czegoś brakuje? <a href="/bewerbung.html?lang=en">Zgłoś ją za darmo</a> lub napisz do nas.',
                      'In November 2026 we read the websites of LOFToDANCE, No Limits, Art Dance, Salsa Libre and Dance Flow. We cite nothing from Dance Flow: its page requires JavaScript and could not be read automatically. We state nothing we could not check. Run a school and something is missing? <a href="/bewerbung.html?lang=en">Enter it for free</a> or write to us.')]),
        ],
        faq=[
            ('Jaki poziom wybrać, jeśli nigdy nie tańczyłem?', 'Which level should I pick if I have never danced?', 'Pierwszy poziom szkoły: w LOFToDANCE to „Bachata od zera” lub kurs podstawowy, w No Limits „Bachata od podstaw”, w Salsa Libre ogólny „Starter”. Zapytaj, co obejmuje.', 'The school\'s first level: at LOFToDANCE it is "Bachata od zera" or the basic course, at No Limits "Bachata od podstaw", at Salsa Libre the general "Starter". Ask what it covers.'),
            ('Czy muszę przyjść z partnerem?', 'Do I have to come with a partner?', 'Nie w szkołach, które to podają: Salsa Libre pisze, że partnera można znaleźć na sali, a Art Dance prowadzi zajęcia dla par i singli.', 'Not at the schools that say so: Salsa Libre writes that you can find a partner in the room, and Art Dance runs classes for couples and singles.'),
            ('Ile kosztuje kurs bachaty?', 'How much does a Bachata course cost?', 'Odczytane strony nie podają cen: odsyłają do osobnych cenników. Zapytaj o cenę miesięczną i liczbę godzin przed wpłatą.', 'The pages read state no prices: they point to separate price lists. Ask for the monthly price and number of hours before paying.'),
            ('Czy można spróbować zajęć za darmo?', 'Can I try classes for free?', 'Odczytane strony nie podają zasad lekcji próbnych. Zapytaj szkołę, czy lekcja próbna jest płatna i czy cena jest odliczana od kursu.', 'The pages read state no trial-lesson rules. Ask the school whether the trial is paid and whether the price is deducted from the course.'),
            ('W których miastach jest najwięcej szkół?', 'Which cities have the most schools?', f'W naszym zestawieniu: Warszawa ({len(BP.by_city("warszawa"))}), Kraków ({len(BP.by_city("krakow"))}), Wrocław ({len(BP.by_city("wroclaw"))}), Poznań ({len(BP.by_city("poznan"))}) i Gdańsk ({len(BP.by_city("gdansk"))}).', f'On our list: Warsaw ({len(BP.by_city("warszawa"))}), Kraków ({len(BP.by_city("krakow"))}), Wrocław ({len(BP.by_city("wroclaw"))}), Poznań ({len(BP.by_city("poznan"))}) and Gdańsk ({len(BP.by_city("gdansk"))}).'),
        ],
        title=('Bachata dla początkujących: poziomy, partner, lekcja próbna', 'Bachata for beginners: levels, partners and trial lessons'),
        desc=('Bachata dla początkujących: jaki poziom wybrać, czy potrzebny jest partner, lekcje próbne i kursy podane przez LOFToDANCE, No Limits, Art Dance i Salsa Libre.',
              'Bachata for beginners: which level to pick, whether you need a partner, trial lessons and courses published by LOFToDANCE, No Limits, Art Dance and Salsa Libre.'),
        crumb0=('Bachata Polska', 'pl/index.html'))
    build(BP, BP.pl_page, 'pl/bachata-dla-poczatkujacych.html', 'bg4', c)

# ===================================================================== MILANO
def milano():
    ss = BI.by_city('milano'); n = len(ss)
    rated = [s for s in ss if s[2] is not None]
    top = rated[:4]
    top_it = '; '.join(f'{s[0]} ({BI.f1(s[2])} ★, {s[3]} recensioni)' for s in top)
    top_en = '; '.join(f'{s[0]} ({BI.f1en(s[2])} ★, {s[3]} reviews)' for s in top)
    c = dict(
        kicker=('Guida · Corsi di bachata Milano', 'Guide · Bachata classes in Milan'),
        h1=('Corsi di bachata a Milano: scuole, livelli e come scegliere', 'Bachata classes in Milan: schools, levels and how to choose'),
        lede=('Quali scuole di Milano e dintorni insegnano bachata, cosa pubblicano su livelli, lezioni di prova e sedi, e come scegliere. Solo dati dai siti delle scuole.',
              'Which schools in Milan and its surroundings teach Bachata, what they publish about levels, trial lessons and venues, and how to choose. Only data from the schools\' own websites.'),
        facts=lambda t: [('cal', f'<b>{n} scuole</b> nel nostro elenco', f'<b>{n} schools</b> on our list'), ('check', 'Siti consultati a <b>novembre 2026</b>', 'Websites checked in <b>November 2026</b>')],
        cta=lambda t: f'<a class="btn btn-gold" href="/it/bachata-milano">{t("span", "Vedi la classifica di Milano", "See the Milan ranking")}</a>',
        sections=[
            (('Corsi di bachata a Milano a colpo d\'occhio', 'Bachata classes in Milan at a glance'), [
                ('p', f'Nel nostro elenco ci sono {n} scuole per Milano. Tra quelle con il voto Google più alto: {top_it} (ottobre 2026). La classifica è provvisoria; i risultati definitivi saranno pubblicati in primavera 2027. Nell\'elenco «Milano» comprende anche scuole dell\'hinterland, quindi controlla sempre l\'indirizzo.',
                      f'Our list has {n} schools for Milan. Among those with the highest Google rating: {top_en} (October 2026). The standing is interim; final results follow in spring 2027. On the list "Milan" also includes schools in the surrounding area, so always check the address.'),
                ('p', 'La lista completa con punteggi e link è in <a href="/it/bachata-milano">Bachata Milano: le migliori scuole di ballo 2027</a>. Qui spieghiamo cosa pubblicano le scuole sui corsi.',
                      'The full list with scores and links is on <a href="/it/bachata-milano">Bachata Milan: the best dance schools 2027</a>. Here we explain what schools publish about their classes.')]),
            (('Cinque scuole, secondo i loro siti', 'Five schools, according to their websites'), [
                ('p', 'Abbiamo letto i siti a novembre 2026. Ecco cosa dicono, così com\'è; orari e prezzi cambiano ogni anno, quindi confermali con la scuola.',
                      'We read the websites in November 2026. This is what they say, as stated; timetables and prices change every year, so confirm them with the school.'),
                ('h3', lk('https://www.phoenixstudiodance.com', 'Phoenix Studio Dance') + ' (Via Andrea Maria Ampère 103, Milano)', lk('https://www.phoenixstudiodance.com', 'Phoenix Studio Dance') + ' (Via Andrea Maria Ampère 103, Milan)'),
                ('ul', [('La Bachata Dominicana compare tra le «altre discipline di danza» con la nota che questi corsi non sono disponibili per l\'anno accademico corrente.', 'Bachata Dominicana appears among the "other dance disciplines" with a note that these courses are not available for the current academic year.'),
                        ('La pagina non riporta livelli, orari o prezzi della bachata; rimanda a pagine generali di calendario e listino.', 'The page gives no Bachata levels, timetable or prices; it points to general timetable and price pages.')]),
                ('h3', lk('https://redlatin.it/', 'Red Latin Studio') + ' (Via Fabio Filzi 17, Cinisello Balsamo)', lk('https://redlatin.it/', 'Red Latin Studio') + ' (Via Fabio Filzi 17, Cinisello Balsamo)'),
                ('ul', [('Sede a Cinisello Balsamo, fuori dal comune di Milano. I corsi di salsa e bachata sono organizzati in tre livelli: base, intermedio e avanzato.', 'Located in Cinisello Balsamo, outside the municipality of Milan. Salsa and Bachata courses are organised in three levels: base, intermediate and advanced.'),
                        ('Offre una «lezione di prova gratuita»; orari e prezzi non sono nel testo che abbiamo letto.', 'It offers a "free trial lesson"; timetable and prices are not in the text we read.')]),
                ('h3', lk('https://bailaconmigomilano.it/', 'Baila Conmigo Milano') + ' (Via Fortezza 13, Milano)', lk('https://bailaconmigomilano.it/', 'Baila Conmigo Milano') + ' (Via Fortezza 13, Milan)'),
                ('ul', [('Un annuncio sul sito, datato 2023–2024, presenta un «Nuovo corso Salsa e Bachata base»; conferma con la scuola che sia ancora attivo.', 'A post on the site, dated 2023–2024, announces a "New Salsa and Bachata base course"; confirm with the school that it is still running.'),
                        ('La home dice «La prova è gratis non ti costa niente», senza riferirlo alla bachata. I prezzi indicati sul sito riguardano l\'affitto sale, non i corsi.', 'The home page says the trial is free, without tying it to Bachata. The prices shown on the site refer to hall rental, not classes.')]),
                ('h3', lk('https://sangrelatino.it/', 'Sangre Latino') + ' (Via Roma 74, Cassina de\' Pecchi)', lk('https://sangrelatino.it/', 'Sangre Latino') + ' (Via Roma 74, Cassina de\' Pecchi)'),
                ('ul', [('Sede nell\'hinterland milanese. Offre corsi di salsa cubana, bachata e balli latinoamericani «per tutti i livelli»; la bachata è tra i corsi collettivi e c\'è anche un corso separato di Bachata Dominicana.', 'Located in the Milan hinterland. It offers courses in Cuban salsa, Bachata and Latin American dances "for all levels"; Bachata is among the group courses and there is also a separate Bachata Dominicana course.'),
                        ('Il sito riporta gli orari di apertura generali, non quelli della bachata, e non indica prezzi.', 'The site lists general opening hours, not Bachata hours, and gives no prices.')]),
                ('h3', lk('https://akademialatina.it', 'AKADEMIA LATINA'), lk('https://akademialatina.it', 'AKADEMIA LATINA')),
                ('ul', [('La bachata è tra le discipline, con salsa e «Gestualità Femminile»; il sito parla di lezioni di gruppo e private per tutti gli stili e livelli.', 'Bachata is among the disciplines, with salsa and "feminine styling"; the site mentions group and private lessons for all styles and levels.'),
                        ('Nella pagina letta non compaiono indirizzo, orari o prezzi.', 'No address, timetable or prices appear on the page read.')])]),
            (('Prova gratuita e prezzi: cosa è pubblicato', 'Free trial and prices: what is published'), [
                ('p', 'Red Latin Studio dichiara una prova gratuita e Baila Conmigo scrive che la prova è gratis in generale. Nessuna delle cinque pagine riporta il prezzo di un corso di bachata. Chiedi sempre il prezzo mensile, le lezioni incluse e se la prova viene scalata.',
                      'Red Latin Studio states a free trial and Baila Conmigo writes that the trial is free in general. None of the five pages states the price of a Bachata course. Always ask for the monthly price, the lessons included and whether the trial is deducted.')]),
            (('Come scegliere a Milano', 'How to choose in Milan'), [
                ('ul', [('Controlla l\'indirizzo: Red Latin Studio e Sangre Latino sono nell\'hinterland, Phoenix e Baila Conmigo in città.', 'Check the address: Red Latin Studio and Sangre Latino are in the surrounding area, Phoenix and Baila Conmigo in the city.'),
                        ('Chiedi se il corso di bachata è attivo quest\'anno: Phoenix segnala che la Bachata Dominicana non è disponibile per l\'anno accademico corrente.', 'Ask whether the Bachata course is running this year: Phoenix says Bachata Dominicana is not available for the current academic year.'),
                        ('Se il sito non indica l\'indirizzo (come per AKADEMIA LATINA nella pagina letta), contatta la scuola prima di spostarti: sede, giorno e orario del corso di bachata vanno confermati.', 'If the site does not state the address (as with AKADEMIA LATINA on the page read), contact the school before travelling: venue, day and time of the Bachata class must be confirmed.'),
                        ('Per Red Latin Studio, il sito elenca come date di prova gratuite martedì 15 e giovedì 17 settembre 2026, ormai passate: chiedi le prossime.', 'For Red Latin Studio, the site lists Tuesday 15 and Thursday 17 September 2026 as free trial dates, which have now passed: ask for the next ones.'),
                        ('Se parti da zero, cerca il livello «base» (Red Latin, Baila Conmigo) e leggi la <a href="/it/bachata-per-principianti">guida alla bachata per principianti</a>.', 'If you start from zero, look for the "base" level (Red Latin, Baila Conmigo) and read the <a href="/it/bachata-per-principianti">Bachata for beginners guide</a>.')])]),
            (('Come abbiamo preparato questa guida', 'How we prepared this guide'), [
                ('p', 'A novembre 2026 abbiamo letto i siti di Phoenix Studio Dance, Red Latin Studio, Baila Conmigo Milano, Sangre Latino e AKADEMIA LATINA; usiamo le cifre del nostro elenco di ottobre 2026. Il sito di La Vuelta non può essere letto automaticamente, quindi non ne citiamo nulla. Altre cinque scuole sono nel nostro elenco senza voto Google (ABC Studios Milano, Bandits Dance Studio Milano, Dance 2Be Milano, Studio Gem Milano e Vinci Dance Academy Bonola). Non inseriamo dati che non abbiamo potuto verificare. Hai una scuola e manca qualcosa? <a href="/bewerbung.html?lang=en">Iscrivila gratis</a> o scrivici.',
                      'In November 2026 we read the websites of Phoenix Studio Dance, Red Latin Studio, Baila Conmigo Milano, Sangre Latino and AKADEMIA LATINA; we use the figures from our October 2026 list. La Vuelta\'s site cannot be read automatically, so we cite nothing from it. Five more schools are on our list without a Google rating (ABC Studios Milano, Bandits Dance Studio Milano, Dance 2Be Milano, Studio Gem Milano and Vinci Dance Academy Bonola). We include nothing we could not check. Run a school and something is missing? <a href="/bewerbung.html?lang=en">Enter it for free</a> or write to us.')]),
        ],
        faq=[
            ('Dove si fanno corsi di bachata a Milano?', 'Where can I take Bachata classes in Milan?', f'Nel nostro elenco ci sono {n} scuole per Milano, tra cui Phoenix Studio Dance, Red Latin Studio, Baila Conmigo Milano, Sangre Latino e AKADEMIA LATINA. Alcune sono nell\'hinterland.', f'Our list has {n} schools for Milan, including Phoenix Studio Dance, Red Latin Studio, Baila Conmigo Milano, Sangre Latino and AKADEMIA LATINA. Some are in the surrounding area.'),
            ('Qual è la migliore scuola di bachata a Milano?', 'What is the best Bachata school in Milan?', f'Per ora, secondo i nostri dati, in testa per voto Google c\'è {top[0][0]} ({BI.f1(top[0][2])} ★, {top[0][3]} recensioni). La classifica è provvisoria fino ai risultati della primavera 2027.', f'For now, according to our data, {top[0][0]} leads on Google rating ({BI.f1en(top[0][2])} ★, {top[0][3]} reviews). The standing is interim until the spring 2027 results.'),
            ('Posso provare una lezione gratis?', 'Can I try a lesson for free?', 'Red Latin Studio indica una lezione di prova gratuita e Baila Conmigo scrive che la prova è gratis. Gli altri siti letti non specificano.', 'Red Latin Studio states a free trial lesson and Baila Conmigo writes that the trial is free. The other sites read do not specify.'),
            ('Quanto costa un corso di bachata a Milano?', 'How much does a Bachata class cost in Milan?', 'Le pagine che abbiamo letto non riportano prezzi dei corsi di bachata. Chiedi alla scuola il prezzo mensile e le lezioni incluse.', 'The pages we read state no Bachata course prices. Ask the school for the monthly price and included lessons.'),
            ('Serve il partner?', 'Do I need a partner?', 'Le pagine lette non lo specificano per la bachata. Chiedilo alla scuola prima della prima lezione.', 'The pages read do not specify this for Bachata. Ask the school before the first lesson.'),
        ],
        title=('Corsi di bachata Milano: scuole, livelli e come scegliere', 'Bachata classes Milan: schools, levels and how to choose'),
        desc=('Corsi di bachata a Milano: cosa pubblicano Phoenix Studio Dance, Red Latin Studio, Baila Conmigo e Sangre Latino su livelli, prova gratuita e sedi, e come scegliere.',
              'Bachata classes in Milan: what Phoenix Studio Dance, Red Latin Studio, Baila Conmigo and Sangre Latino publish about levels, free trials and venues, and how to choose.'),
        crumb0=('Bachata Italia', 'it/index.html'))
    build(BI, BI.it_page, 'it/corsi-di-bachata-milano.html', 'bg5', c)

if __name__ == '__main__':
    es(); it(); fr(); pl(); milano()
