# Support pages for the Iberian/Eastern city pages that get school-name searches:
#   es/clases-de-bachata-valencia, es/clases-de-bachata-sevilla, ee/bachata-classes-sofia
# All facts come from the schools' own websites (checked 8 Nov 2026) or from our ranking data. Nothing is invented.
# Run after build_es.py / build_es_schools.py / build_ee.py:  python3 tools/build_support_ib.py
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_es as BE
import build_ee as EE
from build import T, crumbs, faq_schema

LAST = 'noviembre de 2026'

def ul(t, items):
    return '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in items) + '</ul>'

def top_list(mod, ss, t, n, rating_word, rev_word, rank_word):
    rows = []
    for s in ss:
        if s[2] is None: continue
        rows.append((s[0], mod.f1(s[2]), mod.f1en(s[2]), s[3]))
    return rows[:n]

# ===================================================================== VALENCIA
def valencia():
    k = 'valencia'; ss = BE.by_city(k); n = len(ss)
    t = T('sv1')
    pos = {s[0]: i for i, s in enumerate(ss, 1)}
    top5 = [s for s in ss if s[2] is not None][:5]
    top_es = '; '.join(f'{s[0]} ({BE.f1(s[2])} ★, {s[3]} reseñas)' for s in top5)
    top_en = '; '.join(f'{s[0]} ({BE.f1en(s[2])} ★, {s[3]} reviews)' for s in top5)
    bsv = next(s for s in ss if s[0] == 'Bachata Studio Valencia')
    h = BE.hero(t, ('Guía · Clases de bachata Valencia', 'Guide · Bachata classes in Valencia'),
        ('Clases de bachata en Valencia: escuelas, niveles y cómo elegir', 'Bachata classes in Valencia: schools, levels and how to choose'),
        (f'Qué escuelas dan clases de bachata en Valencia, cómo organizan los niveles y qué conviene preguntar antes de apuntarte. Con datos de las webs de las escuelas y de Google, sin inventar nada.',
         'Which schools teach Bachata in Valencia, how they organise levels and what to ask before you sign up. Based on the schools\' own websites and Google data, nothing invented.'),
        [('cal', f'<b>{n} escuelas</b> en nuestra lista', f'<b>{n} schools</b> in our list'), ('check', 'Webs revisadas en <b>noviembre de 2026</b>', 'Websites checked in <b>November 2026</b>')],
        f'<a class="btn btn-gold" href="/es/bachata-valencia">{t("span", "Ver el ranking de Valencia", "See the Valencia ranking")}</a>')
    body = ''
    body += BE.sec(t, 1, ('Clases de bachata en Valencia de un vistazo', 'Bachata classes in Valencia at a glance'),
        t('p', f'En Valencia hemos encontrado {n} escuelas y academias donde se enseña bachata. Las que más valoraciones de Google reúnen ahora mismo: {top_es}. Es una clasificación provisional basada en datos de octubre de 2026; los resultados finales se publicarán en primavera de 2027.',
                f'We found {n} schools and academies teaching Bachata in Valencia. The ones with the strongest Google ratings right now: {top_en}. This is an interim standing based on October 2026 data; final results follow in spring 2027.')
        + t('p', 'La lista completa, con puntos y enlaces a cada escuela, está en la página <a href="/es/bachata-valencia">Bachata Valencia: las mejores escuelas de baile 2027</a>. Aquí te explicamos cómo funcionan las clases en la práctica.',
                  'The full list with points and links to each school is on the <a href="/es/bachata-valencia">Bachata Valencia: best dance schools 2027</a> page. Here we explain how classes work in practice.'), alt=False)
    body += BE.sec(t, 2, ('Cómo organizan las clases algunas escuelas valencianas', 'How some Valencian schools organise their classes'),
        t('p', f'Hemos leído las webs de varias escuelas ({LAST}). Esto es lo que publican, tal cual; los horarios cambian cada temporada, así que confírmalos con la escuela.',
               'We read the websites of several schools (November 2026). This is what they publish, as stated; timetables change every season, so confirm with the school.')
        + '<h3>' + t('span', '<a href="https://iodance.es/" rel="noopener" target="_blank">IO Dance</a> (Camins al Grau)', '<a href="https://iodance.es/" rel="noopener" target="_blank">IO Dance</a> (Camins al Grau)') + '</h3>'
        + ul(t, [('Dirección según su web: Plaça de Sant Felip Neri 4, 46021, en el barrio de Camins al Grau.', 'Address on its website: Plaça de Sant Felip Neri 4, 46021, in the Camins al Grau neighbourhood.'),
                 ('Enseña bachata tradicional y sensual, con grupos de Bachata Lady Style y Bachata Men Style, además de salsa lineal.', 'Teaches traditional and sensual Bachata, with Bachata Lady Style and Men Style groups, plus linear salsa.'),
                 ('Los niveles van de Iniciación (nivel 0) a nivel 5. Según la web, las clases combinadas de bachata y salsa lineal se incluyen en todos los grupos hasta el nivel 3.', 'Levels run from Iniciación (level 0) to level 5. According to the site, combined Bachata and linear salsa classes are part of every group up to level 3.'),
                 ('Ofrece una clase de prueba gratuita y abre grupos nuevos cuando hay al menos 12 personas apuntadas.', 'It offers a free trial class and opens new groups once at least 12 people have signed up.'),
                 ('Precios publicados: clases privadas 35 € y paquete de baile nupcial 290 €. Los precios de los grupos no aparecen en la página que leímos.', 'Published prices: private classes €35 and a wedding-dance package €290. Group prices do not appear on the page we read.')])
        + '<h3>' + t('span', '<a href="https://bachataschool.com/" rel="noopener" target="_blank">Andrés y Marta Bachata School</a>', '<a href="https://bachataschool.com/" rel="noopener" target="_blank">Andrés y Marta Bachata School</a>') + '</h3>'
        + ul(t, [('Dirección según su web: Carrer Fornoles 4, 46015 Valencia.', 'Address on its website: Carrer Fornoles 4, 46015 Valencia.'),
                 ('La bachata es el centro de la oferta, con bachata sensual y estilos de fusión; la salsa se ofrece como categoría aparte.', 'Bachata is the focus, including sensual Bachata and fusion styles; salsa is a separate category.'),
                 ('Publica horarios regulares e intensivos de 2026 como imágenes y habla de "flexibilidad horaria en todas las clases". No muestra precios en la página principal.', 'It publishes regular and intensive 2026 timetables as images and mentions "flexible hours in all classes". No prices on the main page.')])
        + '<h3>' + t('span', '<a href="https://con-ben.com" rel="noopener" target="_blank">Baila con Ben</a>', '<a href="https://con-ben.com" rel="noopener" target="_blank">Baila con Ben</a>') + '</h3>'
        + ul(t, [('Ofrece clases de grupo y particulares de salsa y bachata, y organiza sesiones de baile social, algunas gratuitas.', 'Offers group and private salsa and Bachata classes and organises social dance sessions, some of them free.'),
                 ('Las clases se dan en distintos lugares de Valencia, así que la ubicación depende del grupo. Pregunta antes de apuntarte.', 'Classes are held at different places around Valencia, so the location depends on the group. Ask before you sign up.')])
        + '<h3>' + t('span', 'Otras escuelas de la lista', 'Other schools on the list')+ '</h3>'
        + ul(t, [('123 y a Bailar se presenta como escuela de baile y alquiler de salas de ensayo en Valencia, con clases de salsa, bachata y otros ritmos latinos.', '123 y a Bailar describes itself as a dance school and rehearsal-room rental in Valencia, with salsa, Bachata and other Latin rhythms.'),
                 ('Ecuahey se define como escuela especializada en bailes sociales y anuncia talleres y socials con fecha en su web.', 'Ecuahey describes itself as a school specialised in social dances and lists dated workshops and socials on its site.')]))
    body += BE.sec(t, 5, ('Socials y práctica: bailar fuera de clase', 'Socials and practice: dancing outside class'),
        t('p', 'La clase enseña el paso; el social lo consolida. Según su web, Ecuahey anuncia talleres y socials con fecha en Valencia (por ejemplo, un evento en Tulum Valencia, Avda. Cortes Valencianas 58, el 14 de noviembre de 2026), y Baila con Ben organiza sesiones de baile social, algunas gratuitas. Consulta fechas y precios en las webs de las escuelas, porque cambian.',
               'Class teaches the step; the social makes it stick. According to its website, Ecuahey lists dated workshops and socials in Valencia (for example an event at Tulum Valencia, Avda. Cortes Valencianas 58, on 14 November 2026), and Baila con Ben organises social dance sessions, some of them free. Check dates and prices on the schools\' websites, as they change.')
        + t('p', 'Para entender cómo es una noche de baile, lee <a href="/bachata-party">Bachata Party</a> (en alemán) y la guía de <a href="/bachata-socials">Bachata-Socials</a>.', 'To see what a dance night is like, read <a href="/bachata-party">Bachata Party</a> (in German) and the <a href="/bachata-socials">Bachata socials</a> guide.'))
    body += BE.sec(t, 3, ('Bachata Studio Valencia: qué sabemos', 'Bachata Studio Valencia: what we know'),
        t('p', f'Bachata Studio Valencia ocupa el puesto {pos["Bachata Studio Valencia"]} de {n} en nuestra clasificación provisional de la ciudad, con {BE.f1(bsv[2])} ★ en Google y {bsv[3]} reseñas (datos de octubre de 2026). Como tiene pocas reseñas, su puntuación aún es baja; cada reseña nueva cuenta mucho más que en escuelas con cientos. No hemos podido leer sus horarios ni precios, así que no los damos: consúltalos en su web.',
               f'Bachata Studio Valencia is number {pos["Bachata Studio Valencia"]} of {n} in our interim standing for the city, with {BE.f1en(bsv[2])} ★ on Google and {bsv[3]} reviews (October 2026 data). With few reviews, its score is still low; each new review counts far more than at schools with hundreds. We could not read its timetable or prices, so we do not state them: check its website.')
        + t('p', 'Su ficha, con puntos, enlace a la web y votación del Premio del público, está en <a href="/es/escuelas/bachata-studio-valencia">Bachata Studio Valencia · reseñas y valoración</a>.',
                 'Its profile, with points, a link to the website and Audience Award voting, is at <a href="/es/escuelas/bachata-studio-valencia">Bachata Studio Valencia · reviews and rating</a>.'))
    body += BE.sec(t, 4, ('Niveles, clase de prueba y precios: qué preguntar', 'Levels, trial class and prices: what to ask'),
        t('p', 'Después de leer las webs, lo que más se repite es lo que no se publica: precios de grupo y horarios actuales. Antes de pagar un bono, pregunta esto:',
               'After reading the websites, what stands out is what is not published: group prices and current timetables. Before you pay for a pass, ask:')
        + ul(t, [('<strong>¿Hay clase de prueba?</strong> IO Dance la ofrece gratis según su web; en otras escuelas hay que preguntarlo.', '<strong>Is there a trial class?</strong> IO Dance offers one free according to its site; at other schools you have to ask.'),
                 ('<strong>¿Cuándo empieza el próximo grupo de iniciación?</strong> Muchas escuelas abren grupos nuevos solo con un mínimo de alumnos.', '<strong>When does the next beginner group start?</strong> Many schools only open new groups with a minimum number of students.'),
                 ('<strong>¿Qué estilo se enseña?</strong> Bachata tradicional, sensual y moderna tienen carácter distinto; los grupos de Lady Style o Men Style se centran en el estilo individual.', '<strong>Which style is taught?</strong> Traditional, sensual and moderna Bachata differ in character; Lady Style or Men Style groups focus on individual styling.'),
                 ('<strong>¿Dónde se da la clase?</strong> Algunas escuelas usan varias salas; comprueba el barrio antes de apuntarte.', '<strong>Where is the class held?</strong> Some schools use several rooms; check the neighbourhood before you sign up.')])
        + t('p', 'Si es tu primera vez, lee también nuestra guía general <a href="/bachata-fuer-anfaenger">Bachata für Anfänger</a> (en alemán) o empieza por el paso básico en <a href="/bachata-grundschritt">Bachata Grundschritt</a>.', 'If it is your first time, our general guide <a href="/bachata-fuer-anfaenger">Bachata für Anfänger</a> (in German) and the basic step page <a href="/bachata-grundschritt">Bachata Grundschritt</a> help too.'))
    body += BE.sec(t, 6, ('Cómo hemos preparado esta guía', 'How we prepared this guide'),
        t('p', f'Hemos leído en {LAST} las webs de IO Dance, Andrés y Marta Bachata School, Baila con Ben, 123 y a Bailar y Ecuahey, y usamos las valoraciones de Google de octubre de 2026 de nuestra lista. De Bachata Studio Valencia no podemos citar horarios ni precios porque su web no se pudo leer de forma automática. No incluimos ningún dato que no hayamos podido comprobar. ¿Eres de una escuela y falta algo? <a href="/bewerbung.html?lang=en">Inscríbela gratis</a> o escríbenos.',
               f'In November 2026 we read the websites of IO Dance, Andrés y Marta Bachata School, Baila con Ben, 123 y a Bailar and Ecuahey, and we use the October 2026 Google ratings from our list. For Bachata Studio Valencia we cannot quote timetables or prices because its website could not be read automatically. We include nothing we could not check. Run a school and something is missing? <a href="/bewerbung.html?lang=en">Enter it for free</a> or write to us.'), alt=False)
    faq = [
        ('¿Dónde puedo aprender bachata en Valencia?', 'Where can I learn Bachata in Valencia?',
         f'En Valencia hemos encontrado {n} escuelas con clases de bachata, entre ellas IO Dance, Andrés y Marta Bachata School, Baila con Ben, 123 y a Bailar y Bachata Studio Valencia. La lista completa está en nuestra página de Bachata Valencia.',
         f'We found {n} schools with Bachata classes in Valencia, including IO Dance, Andrés y Marta Bachata School, Baila con Ben, 123 y a Bailar and Bachata Studio Valencia. The full list is on our Bachata Valencia page.'),
        ('¿Hay clases de prueba gratuitas en Valencia?', 'Are there free trial classes in Valencia?',
         'IO Dance anuncia una clase de prueba gratis en su web. En las demás escuelas que revisamos no consta, así que conviene preguntarlo por WhatsApp o correo.',
         'IO Dance advertises a free trial class on its site. For the other schools we checked it is not stated, so ask by WhatsApp or email.'),
        ('¿Cuánto cuesta una clase de bachata en Valencia?', 'How much does a Bachata class in Valencia cost?',
         'Las escuelas que revisamos casi no publican precios de grupo. IO Dance publica clases privadas a 35 €. Pide siempre el precio del grupo y el tipo de bono antes de pagar.',
         'The schools we checked hardly publish group prices. IO Dance publishes private classes at €35. Always ask for the group price and the pass type before paying.'),
        ('¿Qué niveles hay?', 'What levels are there?',
         'Depende de la escuela. IO Dance, por ejemplo, va de Iniciación (nivel 0) al nivel 5. Si empiezas de cero, elige un grupo de iniciación aunque ya hayas bailado otros estilos.',
         'It depends on the school. IO Dance, for example, runs from Iniciación (level 0) to level 5. If you start from zero, choose a beginner group even if you have danced other styles.'),
        ('¿Cuál es la mejor escuela de bachata de Valencia?', 'What is the best Bachata school in Valencia?',
         f'Según nuestros datos provisionales de octubre de 2026, lideran Andrés y Marta Bachata School y Baila con Ben (5,0 ★ en Google). No es el ranking final: se publicará en primavera de 2027.',
         'By our interim data from October 2026, Andrés y Marta Bachata School and Baila con Ben lead (5.0 ★ on Google). This is not the final ranking, which follows in spring 2027.'),
    ]
    body += BE.faq_html(t, faq)
    BE.es_page('es/clases-de-bachata-valencia.html', 'es/clases-de-bachata-valencia.html',
        'Clases de bachata Valencia: escuelas, niveles y precios',
        f'Clases de bachata en Valencia: cómo organizan niveles y clases de prueba IO Dance, Andrés y Marta y otras escuelas, qué preguntar antes de apuntarte y datos de Google.',
        'Bachata classes Valencia: schools, levels and prices',
        'Bachata classes in Valencia: how IO Dance, Andrés y Marta and other schools organise levels and trial classes, what to ask before you sign up, and Google data.',
        h + body, t.en, [crumbs('Bachata Valencia', 'es/bachata-valencia.html'), crumbs('Clases de bachata Valencia', 'es/clases-de-bachata-valencia.html'), faq_schema(faq)])

# ===================================================================== SEVILLA / DOS HERMANAS
def sevilla():
    ss = BE.by_city('sevilla'); n = len(ss)
    dh = BE.by_city('dos-hermanas'); tum = dh[0]
    t = T('sv2')
    h = BE.hero(t, ('Guía · Clases de bachata Sevilla y Dos Hermanas', 'Guide · Bachata classes in Seville and Dos Hermanas'),
        ('Clases de bachata en Sevilla y Dos Hermanas: escuelas y cómo elegir', 'Bachata classes in Seville and Dos Hermanas: schools and how to choose'),
        ('Dónde se aprende bachata en Sevilla y en Dos Hermanas, con direcciones, grupos y precios tal como los publican las escuelas, y los datos de Google de nuestra lista.',
         'Where to learn Bachata in Seville and Dos Hermanas, with addresses, groups and prices as the schools publish them, plus the Google data from our list.'),
        [('cal', f'<b>{n} escuelas</b> en Sevilla, {len(dh)} en Dos Hermanas', f'<b>{n} schools</b> in Seville, {len(dh)} in Dos Hermanas'), ('check', 'Webs revisadas en <b>noviembre de 2026</b>', 'Websites checked in <b>November 2026</b>')],
        f'<a class="btn btn-gold" href="/es/bachata-sevilla">{t("span", "Ver el ranking de Sevilla", "See the Seville ranking")}</a>')
    body = ''
    body += BE.sec(t, 1, ('Clases de bachata en Sevilla de un vistazo', 'Bachata classes in Seville at a glance'),
        t('p', f'En Sevilla hemos encontrado {n} escuelas con clases de bachata y en Dos Hermanas, que forma parte del área metropolitana, otra más con ficha propia: Tumbao Latino Dance Center. La clasificación provisional, con valoraciones de Google de octubre de 2026, está en <a href="/es/bachata-sevilla">Bachata Sevilla</a> y <a href="/es/bachata-dos-hermanas">Bachata Dos Hermanas</a>.',
               f'We found {n} schools with Bachata classes in Seville and, in Dos Hermanas (part of the metropolitan area), one more with its own profile: Tumbao Latino Dance Center. The interim standing, with Google ratings from October 2026, is on <a href="/es/bachata-sevilla">Bachata Seville</a> and <a href="/es/bachata-dos-hermanas">Bachata Dos Hermanas</a>.'), alt=False)
    body += BE.sec(t, 2, ('Dos Hermanas: Tumbao Latino y Academia Bailamos', 'Dos Hermanas: Tumbao Latino and Academia Bailamos'),
        t('p', f'Tumbao Latino Dance Center es la escuela de Dos Hermanas de nuestra lista: {BE.f1(tum[2])} ★ en Google con {tum[3]} reseñas (octubre de 2026), puesto 1 en la ciudad y {BE.f1(BE.FULL[tum[0]])} puntos provisionales. No tiene web propia en nuestros datos, así que no podemos citar horarios ni precios; su ficha está en <a href="/es/escuelas/tumbao-latino-dance-center">Tumbao Latino Dance Center · reseñas y valoración</a>.',
               f'Tumbao Latino Dance Center is the Dos Hermanas school on our list: {BE.f1en(tum[2])} ★ on Google with {tum[3]} reviews (October 2026), number 1 in the city and {BE.f1en(BE.FULL[tum[0]])} interim points. We have no own website for it in our data, so we cannot quote timetables or prices; its profile is at <a href="/es/escuelas/tumbao-latino-dance-center">Tumbao Latino Dance Center · reviews and rating</a>.')
        + t('p', 'También en el municipio de Dos Hermanas, en Montequinto, está <a href="https://academiabailamos.es/" rel="noopener" target="_blank">Academia Bailamos</a>. Según su web (Avd. de Montequinto s/n, 41089) da clases de salsa, bachata y kizomba, con grupos de "Bachata inicio" los lunes a las 21:30 y los viernes a las 20:00, y la temporada 2026/2027 empezó el 1 de septiembre.',
                 'Also in the municipality of Dos Hermanas, in Montequinto, is Academia Bailamos. According to its website (Avd. de Montequinto s/n, 41089) it teaches salsa, Bachata and kizomba, with "Bachata inicio" groups on Mondays at 21:30 and Fridays at 20:00, and the 2026/2027 season started on 1 September.')
        + t('p', 'Precios que publica Academia Bailamos: Bachata inicio 15 €/mes (1 hora semanal) o 25 €/mes (2 horas); 2 clases a la semana, 25 €/mes; 3 clases, 35 €/mes; 4 clases, 43 €/mes. No menciona clase de prueba: pregunta por teléfono o correo.',
                 'Prices published by Academia Bailamos: Bachata inicio €15/month (1 hour a week) or €25/month (2 hours); 2 classes a week, €25/month; 3 classes, €35/month; 4 classes, €43/month. It does not mention a trial class: ask by phone or email.'))
    body += BE.sec(t, 5, ('Academia Bailamos: horarios, estilos y temporada', 'Academia Bailamos: hours, styles and season'),
        t('p', 'Según su web, Academia Bailamos abre de lunes a viernes: lunes y miércoles de 19:30 a 22:30, martes y jueves de 20:00 a 23:00 y viernes de 19:00 a 22:00. Además de bachata, enseña salsa y kizomba, y menciona zumba y SalsaJunior. Entre los grupos nuevos figura "Salsa inicio" los viernes a las 19:00, y en una publicación de eventos se cita un grupo de "Bachata Avanzado". La temporada 2026/2027 empezó el 1 de septiembre.',
               'According to its website, Academia Bailamos is open Monday to Friday: Monday and Wednesday 19:30 to 22:30, Tuesday and Thursday 20:00 to 23:00, Friday 19:00 to 22:00. Besides Bachata it teaches salsa and kizomba, and mentions zumba and SalsaJunior. New groups include "Salsa inicio" on Fridays at 19:00, and an event post mentions a "Bachata Avanzado" group. The 2026/2027 season began on 1 September.')
        + t('p', 'Es un buen ejemplo de cómo comparar escuelas: publica horas semanales y precio mensual, algo que muchas otras no hacen. Aun así, confirma el grupo actual por teléfono o correo antes de ir.', 'It is a good example of how to compare schools: it publishes weekly hours and a monthly price, which many others do not. Still, confirm the current group by phone or email before going.'))
    body += BE.sec(t, 3, ('Sevilla capital: Bailarte y Feeling Dance Studio', 'Seville city: Bailarte and Feeling Dance Studio'),
        t('p', 'Algunas escuelas de la lista, tal como se presentan en su web:', 'Some schools on the list, as they present themselves on their websites:')
        + ul(t, [('<a href="https://www.bailarte.net/" rel="noopener" target="_blank">Bailarte</a>: C/ Fernando Tirado 9, 41018, en la zona de Nervión (Buhaira). Presenta la bachata como baile de pareja de origen dominicano; no publica precios en la página principal.', 'Bailarte: C/ Fernando Tirado 9, 41018, in the Nervión (Buhaira) area. It presents Bachata as a couple dance of Dominican origin; no prices on the main page.'),
                 ('<a href="https://feelingdancestudio.com" rel="noopener" target="_blank">Feeling Dance Studio</a>: Calle Telegrafistas 14, 41015, barrio de Pino Montano. La bachata figura entre los estilos latinos; los horarios y tarifas están en una sección aparte.', 'Feeling Dance Studio: Calle Telegrafistas 14, 41015, Pino Montano neighbourhood. Bachata is listed among the Latin styles; timetables and rates are in a separate section.'),
                 ('Los Reyes del Mambo, Doble Giro y Academia de Baile Bachata SVQ completan la lista; todas con enlace en la página de Sevilla.', 'Los Reyes del Mambo, Doble Giro and Academia de Baile Bachata SVQ complete the list, all linked on the Seville page.')]))
    body += BE.sec(t, 4, ('Qué preguntar antes de apuntarte', 'What to ask before you sign up'),
        ul(t, [('<strong>Grupo de iniciación:</strong> pregunta cuándo empieza el siguiente; Academia Bailamos, por ejemplo, abre grupos nuevos de "Bachata inicio" al comienzo de la temporada.', '<strong>Beginner group:</strong> ask when the next one starts; Academia Bailamos, for example, opens new "Bachata inicio" groups at the start of the season.'),
               ('<strong>Tipo de bono:</strong> los precios mensuales dependen de las horas a la semana, así que compara con las mismas horas.', '<strong>Pass type:</strong> monthly prices depend on weekly hours, so compare like for like.'),
               ('<strong>Trayecto:</strong> Dos Hermanas y Sevilla están conectadas por cercanías y carretera, pero la clase de las 21:30 cambia mucho según cómo llegues.', '<strong>Journey:</strong> Dos Hermanas and Seville are linked by train and road, but a 21:30 class changes a lot depending on how you get there.')]))
    body += BE.sec(t, 6, ('Cómo hemos preparado esta guía', 'How we prepared this guide'),
        t('p', f'Hemos leído en {LAST} las webs de Academia Bailamos, Bailarte y Feeling Dance Studio y usamos las valoraciones de Google de octubre de 2026 de nuestra lista. Tumbao Latino Dance Center no tiene web en nuestros datos, y de Los Reyes del Mambo, Doble Giro y Academia de Baile Bachata SVQ no hemos leído horarios, por lo que no los citamos. Nada de lo que aquí figura está inventado. ¿Falta tu escuela? <a href="/bewerbung.html?lang=en">Inscríbela gratis</a>.',
               f'In November 2026 we read the websites of Academia Bailamos, Bailarte and Feeling Dance Studio and use the October 2026 Google ratings from our list. Tumbao Latino Dance Center has no website in our data, and we have not read timetables for Los Reyes del Mambo, Doble Giro or Academia de Baile Bachata SVQ, so we do not quote them. Nothing here is invented. Is your school missing? <a href="/bewerbung.html?lang=en">Enter it for free</a>.'), alt=False)
    faq = [
        ('¿Dónde puedo aprender bachata en Dos Hermanas?', 'Where can I learn Bachata in Dos Hermanas?',
         'En Dos Hermanas hay al menos Tumbao Latino Dance Center, con 4,9 ★ en Google y 38 reseñas (octubre de 2026), y Academia Bailamos en Montequinto, que publica grupos de "Bachata inicio" los lunes y viernes.',
         'In Dos Hermanas there are at least Tumbao Latino Dance Center, with 4.9 ★ on Google and 38 reviews (October 2026), and Academia Bailamos in Montequinto, which publishes "Bachata inicio" groups on Mondays and Fridays.'),
        ('¿Cuánto cuesta una clase de bachata en Dos Hermanas?', 'How much is a Bachata class in Dos Hermanas?',
         'Academia Bailamos publica 15 €/mes para Bachata inicio (1 hora semanal) y 25 €/mes con 2 horas. Para otras escuelas, pregunta directamente.',
         'Academia Bailamos publishes €15/month for Bachata inicio (1 hour a week) and €25/month with 2 hours. For other schools, ask directly.'),
        ('¿Qué escuelas de bachata hay en Sevilla?', 'Which Bachata schools are there in Seville?',
         f'Tenemos {n} escuelas en la lista de Sevilla, entre ellas Bailarte, Los Reyes del Mambo, Doble Giro, Feeling Dance Studio y Academia Bailamos. Todas aparecen con valoraciones en nuestra página de Bachata Sevilla.',
         f'We have {n} schools on the Seville list, including Bailarte, Los Reyes del Mambo, Doble Giro, Feeling Dance Studio and Academia Bailamos. All appear with ratings on our Bachata Seville page.'),
        ('¿Hace falta ir con pareja?', 'Do I need a partner?', 'Normalmente no. En muchos grupos se rotan las parejas; pregúntalo antes de la primera clase.', 'Usually not. Many groups rotate partners; ask before the first class.'),
        ('¿Cuándo se publica el ranking de Sevilla?', 'When is the Seville ranking published?', 'En primavera de 2027. Hasta entonces mostramos una clasificación provisional basada en las valoraciones de Google.', 'In spring 2027. Until then we show an interim standing based on Google ratings.'),
    ]
    body += BE.faq_html(t, faq)
    BE.es_page('es/clases-de-bachata-sevilla.html', 'es/clases-de-bachata-sevilla.html',
        'Clases de bachata Sevilla y Dos Hermanas: escuelas y precios',
        'Clases de bachata en Sevilla y Dos Hermanas: direcciones, grupos de iniciación y precios publicados por Academia Bailamos, Bailarte y otras escuelas, más los datos de Google de Tumbao Latino.',
        'Bachata classes Seville and Dos Hermanas: schools and prices',
        'Bachata classes in Seville and Dos Hermanas: addresses, beginner groups and prices published by Academia Bailamos, Bailarte and other schools, plus Google data for Tumbao Latino.',
        h + body, t.en, [crumbs('Bachata Sevilla', 'es/bachata-sevilla.html'), crumbs('Clases de bachata Sevilla', 'es/clases-de-bachata-sevilla.html'), faq_schema(faq)])

# ===================================================================== SOFIA
def sofia():
    ss = EE.by_city('sofia'); n = len(ss)
    t = T('sv3')
    ritmo = next(s for s in ss if s[0] == 'Ritmo Dance Studio')
    h = EE.hero(t, ('Guide · Bachata classes in Sofia', 'Guide · Bachata classes in Sofia'),
        ('Bachata classes in Sofia: schools, groups and prices', 'Bachata classes in Sofia: schools, groups and prices'),
        ('Which schools teach Bachata in Sofia, when beginner groups start and what Pambos Dancing Center, Ritmo, PaLante and Latin Force publish on their websites. Facts from the schools themselves, nothing invented.',
         'Which schools teach Bachata in Sofia, when beginner groups start and what Pambos Dancing Center, Ritmo, PaLante and Latin Force publish on their websites. Facts from the schools themselves, nothing invented.'),
        [('cal', f'<b>{n} schools</b> in our list', f'<b>{n} schools</b> in our list'), ('check', 'Websites checked in <b>November 2026</b>', 'Websites checked in <b>November 2026</b>')],
        f'<a class="btn btn-gold" href="/ee/bachata-sofia">{t("span", "See the Sofia ranking", "See the Sofia ranking")}</a>')
    def P_(a): return t('p', a, a)
    def U_(items): return ul(t, [(a, a) for a in items])
    def S_(i, h2, blocks, alt=True): return EE.sec(t, i, (h2, h2), blocks, alt=alt)
    body = ''
    body += S_(1, 'Bachata classes in Sofia at a glance',
        P_(f'We found {n} schools in Sofia that teach Bachata. Right now only Ritmo Dance Studio ({EE.f1en(ritmo[2])} ★, {ritmo[3]} Google reviews) has a rating in our data; for the other schools we have not collected a Google rating yet, so their score is marked "not yet available" rather than guessed. The full list is on <a href="/ee/bachata-sofia">Bachata Sofia: the best dance schools 2027</a>.')
        + P_('Below is what four schools say on their own websites. Group start dates are as published in November 2026 and will pass, so use them as a guide to how each school works and confirm the current group with the school.'), alt=False)
    body += S_(2, 'Pambos Dancing Center (Los Pambos)',
        P_('<a href="https://pambosalsa.com/" rel="noopener" target="_blank">Pambos Dancing Center</a> is one of the schools people look up by name. We have not collected a Google rating for it yet, so we cannot give a star rating or review count, and we do not publish invented reviews. What its website (in Bulgarian) says:')
        + U_(['Adult Latin dances: salsa, bachata and kizomba, plus adult Greek dances and programmes for children, teenagers and women.',
              'The season opened on 5 October 2026, and a new adult beginner Bachata group in Sofia starts on 9 November 2026.',
              'Published prices in euro: a single visit costs 10; 8 visits cost 50; 16 visits cost 90 (adults).',
              'Main instructors named on the site: Pambos Agapiou and Elisaveta Hristova, with Elina Doychinova as instructor.',
              'The weekly timetable is on a separate page of the site. The page does not mention a trial class; the single-visit price is the closest option.'])
        + P_('Its profile, with the data we hold, a link to the website and Audience Award voting, is at <a href="/ee/schools/pambos-dancing-center">Pambos Dancing Center · Bachata Sofia · reviews and rating</a>. To read reviews, open the Google Maps link on that page: ratings and comments there come from students, not from us.'))
    body += S_(3, 'Ritmo Dance Studio, PaLante and Latin Force',
        U_(['Ritmo Dance Studio: address on its site is ul. Yordan Yosifov 8B, Studentski grad, with a second beginner location at NDK. Salsa & Bachata group 1 (absolute beginners) starts on 19 October 2026 on Mondays and Wednesdays at 18:30; group 2 (beginners) starts on 10 November 2026 on Tuesdays and Thursdays at 21:30; the NDK beginner group started on 15 September 2026 on Tuesdays and Thursdays at 18:30. Prices are on a separate page of the site.',
            'PaLante: Rakovski 78, in the centre, 50 metres from the Opera according to its site. The beginners class runs every Tuesday and Thursday from 18:20, and the listed content covers solo steps and three combinations; a separate advanced Bachata class on Tuesdays is listed too. The site is available in English and Bulgarian.',
            'Latin Force Dance Studio: three locations (Tsar Samuil 50 in the centre, Tsarigradsko shose 101 in Pliska and Osogovo 2 at Mall Sofia). The site lists 15 Bachata groups among 30+ styles, a discount of up to 25 % for visits with cards, and a timetable that is updated on its own schedule page.']))
    body += S_(5, 'How we prepared this guide',
        P_('In November 2026 we read the websites of Pambos Dancing Center, <a href="https://ritmo.bg/" rel="noopener" target="_blank">Ritmo Dance Studio</a>, <a href="https://www.palante.eu/en/groups/salsa-bachata-beginners-tuesday" rel="noopener" target="_blank">PaLante</a> and <a href="https://grafik.latinforce.bg/" rel="noopener" target="_blank">Latin Force</a>, and used the October 2026 Google data from our list. We have no Google rating for Pambos, PaLante, Latin Force, Paletro, Dance Station or Salsa Diva yet, and we have not read the sites of the last three, so we say nothing about them beyond their listing. Nothing here is invented. Run one of these schools and something is wrong or missing? <a href="/bewerbung.html?lang=en">Enter your school for free</a> or write to us.'), alt=False)
    body += S_(4, 'How to choose a Bachata class in Sofia',
        P_('Three things matter most when you compare schools, and the websites we read differ on each:')
        + U_(['Start date: beginner groups open on fixed dates (for example 9 November at Pambos, 10 November at Ritmo). Join at the start, not in the middle of a course.',
              'Location: Sofia schools use several districts (Studentski grad, centre, Pliska, a mall). Check the neighbourhood and how you will get there in the evening.',
              'Price model: Pambos publishes visit packs (1, 8 or 16 visits); other schools put prices on a separate page or do not publish them. Compare the price per class, not the pack size.',
              'Language: the schools\' sites are in Bulgarian (PaLante also in English). If you do not speak Bulgarian, ask by message whether the class is held in English before you book.'])
        + P_('If it is your first time, our guides <a href="/bachata-fuer-anfaenger">Bachata für Anfänger</a> (German) and <a href="/bachata-grundschritt">Bachata Grundschritt</a> explain the basic step, and <a href="/ee/">the Eastern Europe ranking</a> shows all cities.'))
    faq = [
        ('Where can I learn Bachata in Sofia?', 'Where can I learn Bachata in Sofia?',
         f'We list {n} schools in Sofia, including Ritmo Dance Studio, Pambos Dancing Center, PaLante, Latin Force and Dance Station. The full list is on our Bachata Sofia page.',
         f'We list {n} schools in Sofia, including Ritmo Dance Studio, Pambos Dancing Center, PaLante, Latin Force and Dance Station. The full list is on our Bachata Sofia page.'),
        ('How much does Pambos Dancing Center cost?', 'How much does Pambos Dancing Center cost?',
         'According to its website, a single adult visit costs 10 euro, 8 visits cost 50 and 16 visits cost 90. Prices may change, so confirm with the school.',
         'According to its website, a single adult visit costs 10 euro, 8 visits cost 50 and 16 visits cost 90. Prices may change, so confirm with the school.'),
        ('Are there reviews of Pambos Dancing Center?', 'Are there reviews of Pambos Dancing Center?',
         'We have not collected its Google rating yet, so we show no rating. Open the Google Maps link on its profile page to read what students wrote.',
         'We have not collected its Google rating yet, so we show no rating. Open the Google Maps link on its profile page to read what students wrote.'),
        ('When do beginner Bachata groups start in Sofia?', 'When do beginner Bachata groups start in Sofia?',
         'In November 2026, Pambos announces a new adult beginner Bachata group on 9 November and Ritmo a beginners Salsa & Bachata group on 10 November. Dates change each season.',
         'In November 2026, Pambos announces a new adult beginner Bachata group on 9 November and Ritmo a beginners Salsa & Bachata group on 10 November. Dates change each season.'),
        ('Do I need a partner?', 'Do I need a partner?', 'Usually not. Many beginner groups rotate partners; ask before the first class.', 'Usually not. Many beginner groups rotate partners; ask before the first class.'),
    ]
    body += EE.faq_html(t, faq)
    EE.ee_page('ee/bachata-classes-sofia.html', 'ee/bachata-classes-sofia.html',
        'Bachata classes Sofia: schools, groups and prices',
        'Bachata classes in Sofia: what Pambos Dancing Center, Ritmo, PaLante and Latin Force publish about beginner groups, locations and prices, and how to choose.',
        'Bachata classes Sofia: schools, groups and prices',
        'Bachata classes in Sofia: what Pambos Dancing Center, Ritmo, PaLante and Latin Force publish about beginner groups, locations and prices, and how to choose.',
        h + body, t.en, [crumbs('Bachata Sofia', 'ee/bachata-sofia.html'), crumbs('Bachata classes Sofia', 'ee/bachata-classes-sofia.html'), faq_schema(faq)])

valencia(); sevilla(); sofia()
