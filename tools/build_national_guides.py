# National "how to find a class" guides for markets that have city pages but no learning guide:
#   es/clases-de-bachata  (keyword "clases de bachata", 720/mo, SD 13; + bachata para principiantes 320, aprender bachata 140)
#   fr/cours-de-bachata   (keyword "cours de bachata", 1000/mo, SD 27; + apprendre la bachata 170)
# Facts come from the schools' own websites (read 9 Nov 2026) and our ranking data. Nothing is invented.
# Run after build_es.py / build_fr.py (and their *_schools.py):  python3 tools/build_national_guides.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_es as BE
import build_fr as BF
from build import T, crumbs, faq_schema

NOV = 'noviembre de 2026'

def ul(t, items):
    return '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in items) + '</ul>'

def lk(u, n):
    return f'<a href="{u}" rel="noopener" target="_blank">{n}</a>'

# ===================================================================== ESPAÑA
def espana():
    mod = BE; P = BE.P
    N = len(P.SCHOOLS); NC = len(P.CITIES)
    t = T('ng1')
    big = ['madrid', 'barcelona', 'valencia', 'malaga', 'zaragoza', 'las-palmas', 'sevilla', 'murcia', 'cordoba']
    city_links_es = ', '.join(f'<a href="/es/bachata-{k}">{P.CITIES[k][0]}</a> ({len(BE.by_city(k))})' for k in big)
    city_links_en = ', '.join(f'<a href="/es/bachata-{k}">{P.CITIES[k][1]}</a> ({len(BE.by_city(k))})' for k in big)
    h = BE.hero(t, ('Guía · Clases de bachata en España', 'Guide · Bachata classes in Spain'),
        ('Clases de bachata en España: ciudades, niveles y precios', 'Bachata classes in Spain: cities, levels and prices'),
        (f'Cómo funcionan las clases de bachata en España, qué publican las escuelas sobre niveles, clases de prueba y precios, y qué preguntar antes de apuntarte. Con datos de las webs de las escuelas, sin inventar nada.',
         'How Bachata classes work in Spain, what schools publish about levels, trial classes and prices, and what to ask before you sign up. Based on the schools\' own websites, nothing invented.'),
        [('cal', f'<b>{N} escuelas</b> en {NC} ciudades', f'<b>{N} schools</b> in {NC} cities'), ('check', 'Webs revisadas en <b>noviembre de 2026</b>', 'Websites checked in <b>November 2026</b>')],
        f'<a class="btn btn-gold" href="/es/">{t("span", "Ver el ranking de España", "See the Spain ranking")}</a>')
    body = ''
    body += BE.sec(t, 1, ('Clases de bachata en España de un vistazo', 'Bachata classes in Spain at a glance'),
        t('p', f'En nuestra lista hay {N} escuelas (algunas con varias sedes) repartidas en {NC} ciudades españolas. Las ciudades con más escuelas son {city_links_es}. Cada una tiene su propia página con la clasificación provisional, basada en datos de octubre de 2026; los resultados finales se publicarán en primavera de 2027.',
               f'Our list has {N} schools (some with several locations) in {NC} Spanish cities. The cities with the most schools are {city_links_en}. Each has its own page with the interim standing, based on October 2026 data; final results follow in spring 2027.')
        + t('p', 'Para dos ciudades hemos preparado además guías de clases con direcciones y precios publicados: <a href="/es/clases-de-bachata-valencia">clases de bachata en Valencia</a> y <a href="/es/clases-de-bachata-sevilla">clases de bachata en Sevilla y Dos Hermanas</a>.',
                 'For two cities we have also prepared class guides with published addresses and prices: <a href="/es/clases-de-bachata-valencia">Bachata classes in Valencia</a> and <a href="/es/clases-de-bachata-sevilla">Bachata classes in Seville and Dos Hermanas</a>.'), alt=False)
    body += BE.sec(t, 2, ('Cómo se organizan las clases: cuatro ejemplos reales', 'How classes are organised: four real examples'),
        t('p', f'Hemos leído las webs de varias escuelas ({NOV}). Esto es lo que publican, tal cual; los horarios y las tarifas cambian cada temporada.',
               'We read the websites of several schools (November 2026). This is what they publish, as stated; timetables and rates change every season.')
        + '<h3>' + t('span', lk('https://salsabachata.es/', 'Salsabachata') + ' (Madrid)', lk('https://salsabachata.es/', 'Salsabachata') + ' (Madrid)') + '</h3>'
        + ul(t, [('Cuatro sedes en Madrid: Quevedo, Avenida de América, Sol y Ventas.', 'Four locations in Madrid: Quevedo, Avenida de América, Sol and Ventas.'),
                 ('La primera clase es gratis, en cualquier estilo. Las clases sueltas no tienen horario ni grupo fijo y se pagan por clase, "desde solo 4,75 € por clase" según su web, con packs de créditos.', 'The first class is free, in any style. Regular classes have no fixed timetable or group and are paid per class, "from only €4.75 per class" according to its website, with credit packs.'),
                 ('Los niveles son generales para todos los estilos: Nivel 0 Básico, Nivel 1 Principiante, Nivel 2 Intermedio, Nivel 3 Avanzado y un Nivel Único abierto a todos.', 'Levels are general for all styles: Level 0 Basic, Level 1 Beginner, Level 2 Intermediate, Level 3 Advanced and a Nivel Único open to all.'),
                 ('Se rotan las parejas durante la clase y el sistema equilibra líderes y seguidores. Hay grupos cerrados con plaza fija semanal y cuota mensual. Las clases privadas cuestan 50 € la hora (60 € en pareja).', 'Partners rotate during class and the system balances leaders and followers. Closed groups with a fixed weekly slot have a monthly fee. Private classes cost €50 an hour (€60 for a couple).')])
        + '<h3>' + t('span', lk('http://www.salsaragon.es/', 'Salsaragón') + ' (Zaragoza)', lk('http://www.salsaragon.es/', 'Salsaragón') + ' (Zaragoza)') + '</h3>'
        + ul(t, [('Sede principal en la calle Hermanos Gambra 8; otras salas dependen de que se forme un grupo.', 'Main school at Calle Hermanos Gambra 8; other rooms depend on a group forming.'),
                 ('Publica clases de "BACHATA iniciación", "BACHATA FUSION Y MUSICALIDAD" (nivel medio) y "LADY STYLE BACHATA", además de grupos combinados de salsa y bachata, con niveles desde "inicio 0" hasta medio-avanzado.', 'Publishes "BACHATA iniciación", "BACHATA FUSION Y MUSICALIDAD" (intermediate) and "LADY STYLE BACHATA" classes, plus combined salsa and Bachata groups, with levels from "inicio 0" to medio-avanzado.'),
                 ('Ofrece clases sin pareja. La clase de prueba cuesta 10 € y se descuenta de la primera mensualidad si formalizas el curso.', 'Offers classes without a partner. The trial class costs €10, deducted from the first monthly fee if you enrol.')])
        + '<h3>' + t('span', lk('https://www.sandracarbonell.es', 'Baila con Sandra y Quique') + ' (Málaga)', lk('https://www.sandracarbonell.es', 'Baila con Sandra y Quique') + ' (Málaga)') + '</h3>'
        + ul(t, [('Clases de grupo en Teatinos, Churriana y San Julián, además de clases particulares, solo o en pareja, y preparación de baile nupcial.', 'Group classes in Teatinos, Churriana and San Julián, plus private classes, alone or as a couple, and wedding-dance preparation.'),
                 ('La primera clase es gratuita y, si ya tienes experiencia, puedes probar varios niveles. La inscripción es gratuita; no publica tarifas, que se piden por teléfono.', 'The first class is free and, if you have experience, you can try several levels. Enrolment is free; it does not publish rates, which you ask for by phone.')])
        + '<h3>' + t('span', lk('https://www.bailongu.com', 'Bailongu') + ' (Barcelona)', lk('https://www.bailongu.com', 'Bailongu') + ' (Barcelona)') + '</h3>'
        + ul(t, [('Passatge d\'Utset 11-13, junto a la Sagrada Família, con cinco salas. La bachata aparece en su social dominical "Salsongu-Bachatongu" (19–22 h, entrada 10 € con refrescos).', 'Passatge d\'Utset 11-13, next to the Sagrada Família, with five studios. Bachata appears in its Sunday social "Salsongu-Bachatongu" (19–22 h, €10 entry with soft drinks).'),
                 ('Los talleres de domingo tienen entrada gratuita. No hemos encontrado niveles de bachata ni tarifas de curso en la página principal.', 'The Sunday workshops are free to enter. We found no Bachata levels or course rates on the main page.')]))
    body += BE.sec(t, 3, ('Bachata para principiantes: por dónde empezar', 'Bachata for beginners: where to start'),
        t('p', 'Si nunca has bailado, busca el primer nivel de cada escuela (Nivel 0, inicio 0, Iniciación) y reserva la clase de prueba. Los niveles, la pareja y los precios de empezar están en nuestra guía <a href="/es/bachata-para-principiantes">Bachata para principiantes</a>.', 'If you have never danced, look for each school\'s first level (Level 0, inicio 0, Iniciación) and book the trial class. Levels, partners and the cost of starting are in our guide <a href="/es/bachata-para-principiantes">Bachata for beginners</a>.'))
    body += BE.sec(t, 4, ('Precios: qué se publica y qué no', 'Prices: what is published and what is not'),
        t('p', 'Tras leer las webs, lo más repetido es lo que falta. Esto es todo lo que encontramos publicado:',
               'After reading the websites, what is missing is the most repeated finding. This is everything we found published:')
        + ul(t, [('Salsabachata (Madrid): clases "desde solo 4,75 € por clase" con créditos; privadas 50 € la hora y 60 € en pareja.', 'Salsabachata (Madrid): classes "from only €4.75 per class" with credits; private classes €50 an hour and €60 for a couple.'),
                 ('Salsaragón (Zaragoza): clase de prueba de 10 €, que se descuenta de la primera mensualidad.', 'Salsaragón (Zaragoza): €10 trial class, deducted from the first monthly fee.'),
                 ('Bailongu (Barcelona): social de domingo a 10 € con refrescos; talleres de domingo gratuitos.', 'Bailongu (Barcelona): Sunday social at €10 with soft drinks; free Sunday workshops.'),
                 ('Baila con Sandra y Quique (Málaga), Seven Dance (Barcelona) y otras: sin tarifas en la página principal; hay que preguntar.', 'Baila con Sandra y Quique (Málaga), Seven Dance (Barcelona) and others: no rates on the main page; you have to ask.')])
        + t('p', 'Por eso, antes de pagar, pide el precio mensual del grupo, cuántas horas incluye y si la clase de prueba se descuenta.', 'So before paying, ask for the monthly group price, how many hours it includes and whether the trial class is deducted.'))
    body += BE.sec(t, 5, ('Qué preguntar antes de apuntarte', 'What to ask before you sign up'),
        ul(t, [('<strong>¿Hay clase de prueba y se paga?</strong> Algunas escuelas la regalan (Salsabachata, Baila con Sandra y Quique) y otras la cobran y la descuentan (Salsaragón).', '<strong>Is there a trial class and is it paid?</strong> Some schools give it away (Salsabachata, Baila con Sandra y Quique) and others charge and deduct it (Salsaragón).'),
               ('<strong>¿Pago por clase o mensualidad?</strong> Un sistema de créditos da libertad de horario; un grupo cerrado asegura tu plaza y tu pareja de baile.', '<strong>Pay per class or monthly?</strong> A credit system gives schedule freedom; a closed group secures your slot and your dance partners.'),
               ('<strong>¿Qué estilo de bachata se enseña?</strong> Tradicional, sensual, fusión o lady style son clases distintas; Salsaragón, por ejemplo, las separa por nombre.', '<strong>Which Bachata style is taught?</strong> Traditional, sensual, fusion or lady style are different classes; Salsaragón, for example, separates them by name.'),
               ('<strong>¿Dónde y cuándo?</strong> Comprueba sede y horario: algunas escuelas tienen varias salas y solo abren un grupo si hay inscritos suficientes.', '<strong>Where and when?</strong> Check location and timetable: some schools have several rooms and only open a group if enough people sign up.')]))
    body += BE.sec(t, 6, ('Cómo hemos preparado esta guía', 'How we prepared this guide'),
        t('p', f'En {NOV} leímos las webs de Salsabachata, Salsaragón, Baila con Sandra y Quique, Bailongu y Seven Dance, y usamos las cifras de nuestra lista de octubre de 2026. De Seven Dance la página principal no publica niveles ni tarifas, por lo que no los damos. No incluimos ningún dato que no hayamos podido comprobar. ¿Tienes una escuela y falta algo? <a href="/bewerbung.html?lang=en">Inscríbela gratis</a> o escríbenos.',
               'In November 2026 we read the websites of Salsabachata, Salsaragón, Baila con Sandra y Quique, Bailongu and Seven Dance, and we use the figures from our October 2026 list. Seven Dance\'s main page publishes no levels or rates, so we do not state them. We include nothing we could not check. Run a school and something is missing? <a href="/bewerbung.html?lang=en">Enter it for free</a> or write to us.'), alt=False)
    faq = [
        ('¿Cuánto cuesta una clase de bachata en España?', 'How much does a Bachata class in Spain cost?',
         'Depende de la escuela, y muchas no publican precios. Salsabachata, en Madrid, anuncia clases desde 4,75 € por clase con créditos; Salsaragón, en Zaragoza, cobra 10 € por la clase de prueba. Pide siempre el precio del grupo antes de pagar.',
         'It depends on the school, and many do not publish prices. Salsabachata in Madrid advertises classes from €4.75 per class with credits; Salsaragón in Zaragoza charges €10 for the trial class. Always ask for the group price before paying.'),
        ('¿Puedo probar una clase de bachata gratis?', 'Can I try a Bachata class for free?',
         'Sí, en algunas escuelas: Salsabachata (Madrid) y Baila con Sandra y Quique (Málaga) ofrecen la primera clase gratuita según sus webs. Salsaragón (Zaragoza) cobra 10 € y lo descuenta de la primera mensualidad.',
         'Yes, at some schools: Salsabachata (Madrid) and Baila con Sandra y Quique (Málaga) offer the first class free according to their websites. Salsaragón (Zaragoza) charges €10 and deducts it from the first monthly fee.'),
        ('¿Necesito pareja para ir a clase de bachata?', 'Do I need a partner for a Bachata class?',
         'No. Salsabachata rota las parejas durante la clase y Salsaragón ofrece grupos sin pareja. Pregúntalo antes de la primera clase.',
         'No. Salsabachata rotates partners during class and Salsaragón offers groups without a partner. Ask before the first class.'),
        ('¿Qué nivel elijo si no he bailado nunca?', 'Which level should I pick if I have never danced?',
         'El más básico: Nivel 0 Básico en Salsabachata o "inicio 0" en Salsaragón. Aunque hayas bailado otros estilos, el nivel básico te enseña el paso y la guía de la bachata.',
         'The most basic one: Level 0 Basic at Salsabachata or "inicio 0" at Salsaragón. Even if you have danced other styles, the basic level teaches you the Bachata step and lead.'),
        ('¿En qué ciudades hay más escuelas de bachata?', 'Which cities have the most Bachata schools?',
         f'En nuestra lista, Madrid ({len(BE.by_city("madrid"))}), Barcelona ({len(BE.by_city("barcelona"))}), Valencia y Málaga ({len(BE.by_city("valencia"))} cada una) y Zaragoza ({len(BE.by_city("zaragoza"))}). Algunas escuelas cuentan con varias sedes.',
         f'On our list, Madrid ({len(BE.by_city("madrid"))}), Barcelona ({len(BE.by_city("barcelona"))}), Valencia and Málaga ({len(BE.by_city("valencia"))} each) and Zaragoza ({len(BE.by_city("zaragoza"))}). Some schools have several locations.'),
        ('¿Cuándo se publica el ranking de escuelas de España?', 'When is the Spain ranking published?',
         'En primavera de 2027. Hasta entonces mostramos una clasificación provisional basada en datos públicos de octubre de 2026.',
         'In spring 2027. Until then we show an interim standing based on public data from October 2026.'),
    ]
    body += BE.faq_html(t, faq)
    BE.es_page('es/clases-de-bachata.html', 'es/clases-de-bachata.html',
        'Clases de bachata en España: ciudades, niveles y precios',
        'Clases de bachata en España: cómo funcionan niveles, clases de prueba y precios en Salsabachata, Salsaragón y otras escuelas, y qué preguntar antes de apuntarte.',
        'Bachata classes in Spain: cities, levels and prices',
        'Bachata classes in Spain: how levels, trial classes and prices work at Salsabachata, Salsaragón and other schools, and what to ask before you sign up.',
        h + body, t.en, [crumbs('Bachata España', 'es/index.html'), crumbs('Clases de bachata', 'es/clases-de-bachata.html'), faq_schema(faq)])

# ===================================================================== FRANCE
def france():
    P = BF.P
    N = len(P.SCHOOLS); NC = len(P.CITIES)
    t = T('ng2')
    big = ['paris', 'toulouse', 'marseille', 'strasbourg', 'nantes', 'bordeaux', 'montpellier', 'lyon']
    cl_fr = ', '.join(f'<a href="/fr/bachata-{k}">{P.CITIES[k][0]}</a> ({len(BF.by_city(k))})' for k in big)
    cl_en = ', '.join(f'<a href="/fr/bachata-{k}">{P.CITIES[k][1]}</a> ({len(BF.by_city(k))})' for k in big)
    h = BF.hero(t, ('Guide · Cours de bachata en France', 'Guide · Bachata classes in France'),
        ('Cours de bachata en France : écoles, niveaux et tarifs', 'Bachata classes in France: schools, levels and prices'),
        ('Comment fonctionnent les cours de bachata en France, ce que les écoles publient sur les niveaux, les cours d’essai et les tarifs, et quoi demander avant de vous inscrire. D’après les sites des écoles, sans rien inventer.',
         'How Bachata classes work in France, what schools publish about levels, trial classes and prices, and what to ask before you sign up. Based on the schools\' own websites, nothing invented.'),
        [('cal', f'<b>{N} écoles</b> dans {NC} villes', f'<b>{N} schools</b> in {NC} cities'), ('check', 'Sites consultés en <b>novembre 2026</b>', 'Websites checked in <b>November 2026</b>')],
        f'<a class="btn btn-gold" href="/fr/">{t("span", "Voir le classement de la France", "See the France ranking")}</a>')
    body = ''
    body += BF.sec(t, 1, ('Cours de bachata en France en un coup d’œil', 'Bachata classes in France at a glance'),
        t('p', f'Notre liste compte {N} écoles (certaines avec plusieurs adresses) réparties dans {NC} villes françaises. Les villes les mieux fournies sont {cl_fr}. Chacune a sa propre page avec le classement provisoire, fondé sur des données d’octobre 2026 ; les résultats définitifs seront publiés au printemps 2027.',
               f'Our list has {N} schools (some with several locations) in {NC} French cities. The best-served cities are {cl_en}. Each has its own page with the interim standing, based on October 2026 data; final results follow in spring 2027.'), alt=False)
    body += BF.sec(t, 2, ('Comment les cours sont organisés : trois exemples réels', 'How classes are organised: three real examples'),
        t('p', 'Nous avons lu les sites de plusieurs écoles (novembre 2026). Voici ce qu’elles publient, tel quel ; les plannings et les tarifs changent chaque saison.',
               'We read the websites of several schools (November 2026). This is what they publish, as stated; timetables and rates change every season.')
        + '<h3>' + t('span', lk('https://www.salsanueva.fr', 'SalsaNueva') + ' (Paris)', lk('https://www.salsanueva.fr', 'SalsaNueva') + ' (Paris)') + '</h3>'
        + ul(t, [('Deux adresses à Paris : 10 rue Érard (12e) et 32 rue du Capitaine Marchal (20e).', 'Two addresses in Paris: 10 rue Érard (12th) and 32 rue du Capitaine Marchal (20th).'),
                 ('Les cours durent 1 heure et ont lieu sept jours sur sept ; des séances d’initiation pour débutants ont lieu chaque dimanche.', 'Classes last 1 hour and run seven days a week; beginner introduction sessions take place every Sunday.'),
                 ('Le site met en avant une « offre découverte » à 99 € et un pack d’essai de huit cours sur 30 jours. On réserve un cours d’essai directement sur le planning. Des stages mensuels sont annoncés.', 'The site highlights a "discovery offer" at €99 and a trial pack of eight classes over 30 days. You book a trial class directly on the timetable. Monthly workshops (stages) are announced.')])
        + '<h3>' + t('span', lk('https://www.elegua.fr', 'Salsa con Elegua') + ' (Paris 14e, Lieusaint)', lk('https://www.elegua.fr', 'Salsa con Elegua') + ' (Paris 14th, Lieusaint)') + '</h3>'
        + ul(t, [('Cours à la Fondation des États-Unis (15 boulevard Jourdan, Paris 14e) et à Lucky Folks à Lieusaint (Sénart).', 'Classes at the Fondation des États-Unis (15 boulevard Jourdan, Paris 14th) and at Lucky Folks in Lieusaint (Sénart).'),
                 ('Bachata en niveaux débutant, intermédiaire et avancé, du mardi au jeudi ; tous les niveaux ne sont pas proposés sur les deux sites.', 'Bachata at beginner, intermediate and advanced levels, Tuesday to Thursday; not every level runs at both sites.'),
                 ('Le premier cours est gratuit et sans engagement : pas d’inscription, il suffit d’arriver 5 minutes avant. Paiement possible en trois fois sans frais.', 'The first class is free and without commitment: no registration, just arrive 5 minutes early. Payment in three instalments without fees is possible.')])
        + '<h3>' + t('span', lk('https://www.encas-danses.com', 'Encas-Danses Studio') + ' (Toulouse)', lk('https://www.encas-danses.com', 'Encas-Danses Studio') + ' (Toulouse)') + '</h3>'
        + ul(t, [('Dans le quartier de Purpan, 82 route de Bayonne, à environ 15 minutes du centre-ville ; parking de 250 places.', 'In the Purpan district, 82 route de Bayonne, about 15 minutes from the city centre; parking for 250 cars.'),
                 ('Deux cours de bachata sont listés : « Bachata » avec Morgane & Bastien et « Bachata Lady Style » avec Morgane. Le planning 2026-2027 et les tarifs se trouvent sur des pages séparées ; un cours d’essai est proposé.', 'Two Bachata classes are listed: "Bachata" with Morgane & Bastien and "Bachata Lady Style" with Morgane. The 2026-2027 timetable and rates are on separate pages; a trial class is offered.')])
        + t('p', 'À Toulouse, <a href="https://amandadanse.com/" rel="noopener" target="_blank">Amanda Bachata</a> propose des cours collectifs hebdomadaires, des cours particuliers (une personne, un couple ou deux personnes), des stages et des camps féminins ; aucun tarif n’est publié sur la page principale.',
                 'In Toulouse, <a href="https://amandadanse.com/" rel="noopener" target="_blank">Amanda Bachata</a> offers weekly group classes, private classes (one person, a couple or two people), workshops and women-only camps; no rates are published on the main page.'))
    body += BF.sec(t, 3, ('Apprendre la bachata quand on débute', 'Learning Bachata as a beginner'),
        t('p', 'Si vous n’avez jamais dansé, cherchez le premier niveau de chaque école et réservez le cours d’essai. Niveaux, partenaire et tarifs pour débuter : voir notre guide <a href="/fr/apprendre-la-bachata">Apprendre la bachata</a>.', 'If you have never danced, look for each school’s first level and book the trial class. Levels, partners and prices to start are in our guide <a href="/fr/apprendre-la-bachata">Learning Bachata</a>.'))
    body += BF.sec(t, 4, ('Tarifs : ce qui est publié', 'Prices: what is published'),
        t('p', 'Après lecture des sites, le plus frappant est ce qui manque. Voici tout ce que nous avons trouvé :', 'After reading the websites, what is missing is the most striking finding. This is everything we found:')
        + ul(t, [('SalsaNueva (Paris) : « offre découverte » à 99 € ; pack d’essai de huit cours sur 30 jours ; les autres tarifs sont sur une page « Tarifs ».', 'SalsaNueva (Paris): "discovery offer" at €99; trial pack of eight classes over 30 days; other rates are on a "Tarifs" page.'),
                 ('Salsa con Elegua : premier cours gratuit ; paiement en trois fois sans frais ; les tarifs sont sur une page séparée.', 'Salsa con Elegua: first class free; payment in three instalments without fees; rates are on a separate page.'),
                 ('Encas-Danses (Toulouse) et Amanda Bachata : aucun tarif sur la page principale.', 'Encas-Danses (Toulouse) and Amanda Bachata: no rates on the main page.')])
        + t('p', 'Avant de payer, demandez le prix mensuel du groupe, le nombre d’heures incluses et si le cours d’essai est déduit.', 'Before paying, ask for the monthly group price, the number of hours included and whether the trial class is deducted.'))
    body += BF.sec(t, 5, ('Quoi demander avant de vous inscrire', 'What to ask before you sign up'),
        ul(t, [('<strong>Un cours d’essai est-il possible ?</strong> Salsa con Elegua offre le premier cours ; SalsaNueva propose un pack d’essai ; Encas-Danses propose un cours d’essai sans détail public.', '<strong>Is a trial class possible?</strong> Salsa con Elegua offers the first class; SalsaNueva has a trial pack; Encas-Danses offers a trial class without public details.'),
               ('<strong>Quel style de bachata ?</strong> Classique, sensuelle ou lady style sont des cours différents ; Encas-Danses sépare par exemple « Bachata » et « Bachata Lady Style ».', '<strong>Which Bachata style?</strong> Traditional, sensual or lady style are different classes; Encas-Danses, for example, separates "Bachata" and "Bachata Lady Style".'),
               ('<strong>Où et quand ?</strong> Vérifiez l’adresse et le planning : certaines écoles ont plusieurs sites et ne proposent pas tous les niveaux partout.', '<strong>Where and when?</strong> Check the address and timetable: some schools have several sites and do not offer every level everywhere.'),
               ('<strong>Stages et soirées ?</strong> Plusieurs écoles annoncent des stages et des soirées ; ils prolongent le cours et aident à progresser.', '<strong>Workshops and parties?</strong> Several schools announce workshops and parties; they extend the class and help you progress.')]))
    body += BF.sec(t, 6, ('Comment nous avons préparé ce guide', 'How we prepared this guide'),
        t('p', 'En novembre 2026, nous avons lu les sites de SalsaNueva, Salsa con Elegua, Encas-Danses Studio et Amanda Bachata, et nous utilisons les chiffres de notre liste d’octobre 2026. Le site d’une école de Lyon n’a pas pu être lu automatiquement : nous n’en citons donc rien. Nous n’incluons aucune donnée que nous n’avons pas pu vérifier. Vous dirigez une école et il manque quelque chose ? <a href="/bewerbung.html?lang=en">Inscrivez-la gratuitement</a> ou écrivez-nous.',
               'In November 2026 we read the websites of SalsaNueva, Salsa con Elegua, Encas-Danses Studio and Amanda Bachata, and we use the figures from our October 2026 list. A Lyon school\'s website could not be read automatically, so we cite nothing from it. We include nothing we could not check. Run a school and something is missing? <a href="/bewerbung.html?lang=en">Enter it for free</a> or write to us.'), alt=False)
    faq = [
        ('Combien coûte un cours de bachata en France ?', 'How much does a Bachata class in France cost?',
         'Cela dépend de l’école, et beaucoup ne publient pas leurs tarifs sur la page principale. SalsaNueva (Paris) met en avant une offre découverte à 99 €. Demandez toujours le prix du groupe avant de payer.',
         'It depends on the school, and many do not publish rates on the main page. SalsaNueva (Paris) highlights a discovery offer at €99. Always ask for the group price before paying.'),
        ('Peut-on essayer un cours de bachata gratuitement ?', 'Can I try a Bachata class for free?',
         'Parfois. Salsa con Elegua indique « 1er cours gratuit et sans engagement » sur son site. D’autres écoles proposent un cours ou un pack d’essai ; vérifiez les conditions.',
         'Sometimes. Salsa con Elegua states "1st class free and without commitment" on its website. Other schools offer a trial class or pack; check the conditions.'),
        ('Faut-il un partenaire pour un cours de bachata ?', 'Do I need a partner for a Bachata class?',
         'En général non : on change de partenaire pendant le cours. Demandez à l’école avant le premier cours.',
         'Usually not: partners change during class. Ask the school before the first class.'),
        ('Quel niveau choisir si je n’ai jamais dansé ?', 'Which level should I pick if I have never danced?',
         'Le niveau débutant. Salsa con Elegua propose des cours de bachata débutant, intermédiaire et avancé ; SalsaNueva organise chaque dimanche des séances d’initiation pour débutants.',
         'The beginner level. Salsa con Elegua offers beginner, intermediate and advanced Bachata classes; SalsaNueva runs beginner introduction sessions every Sunday.'),
        ('Dans quelles villes y a-t-il le plus d’écoles de bachata ?', 'Which cities have the most Bachata schools?',
         f'Dans notre liste : Paris ({len(BF.by_city("paris"))}), Toulouse ({len(BF.by_city("toulouse"))}), Marseille, Strasbourg et Nantes ({len(BF.by_city("marseille"))} chacune) et Bordeaux ({len(BF.by_city("bordeaux"))}). Certaines écoles ont plusieurs adresses.',
         f'On our list: Paris ({len(BF.by_city("paris"))}), Toulouse ({len(BF.by_city("toulouse"))}), Marseille, Strasbourg and Nantes ({len(BF.by_city("marseille"))} each) and Bordeaux ({len(BF.by_city("bordeaux"))}). Some schools have several addresses.'),
        ('Quand le classement des écoles de France sera-t-il publié ?', 'When is the France ranking published?',
         'Au printemps 2027. D’ici là, nous affichons un classement provisoire fondé sur des données publiques d’octobre 2026.',
         'In spring 2027. Until then we show an interim standing based on public data from October 2026.'),
    ]
    body += BF.faq_html(t, faq)
    BF.fr_page('fr/cours-de-bachata.html', 'fr/cours-de-bachata.html',
        'Cours de bachata en France : écoles, niveaux et tarifs',
        'Cours de bachata en France : comment fonctionnent niveaux, cours d’essai et tarifs chez SalsaNueva, Salsa con Elegua et d’autres écoles, et quoi demander avant de vous inscrire.',
        'Bachata classes in France: schools, levels and prices',
        'Bachata classes in France: how levels, trial classes and prices work at SalsaNueva, Salsa con Elegua and other schools, and what to ask before you sign up.',
        h + body, t.en, [crumbs('Bachata France', 'fr/index.html'), crumbs('Cours de bachata', 'fr/cours-de-bachata.html'), faq_schema(faq)])

espana(); france()
