# Support pages for the biggest city pages (class guides built only from the schools' own websites, read 10 Nov 2026):
#   es/clases-de-bachata-madrid, es/clases-de-bachata-barcelona, uk/bachata-classes-london, fr/cours-de-bachata-paris
# (Vienna: bachata-kurs-wien is built inside build_guides.py.)  Nothing here is invented: every price, address and
# time comes from a school's own site or from our ranking data.
# Run after build_es/_schools, build_uk/_schools, build_fr/_schools:  python3 tools/build_support_cities.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_es as BE
import build_uk as BU
import build_fr as BF
from build import T, crumbs, faq_schema

def lk(u, n): return f'<a href="{u}" rel="noopener" target="_blank">{n}</a>'

def tops(ss, fmt, n=4):
    out, seen = [], set()
    for s in ss:
        if s[2] is None: continue
        b = s[0].split()[0].lower()
        if b in seen: continue
        seen.add(b); out.append(s)
        if len(out) == n: break
    return out

# ===================================================================== MADRID
def madrid():
    ss = BE.by_city('madrid'); n = len(ss); t = T('sc1')
    tp = tops(ss, BE.f1)
    top_es = '; '.join(f'{s[0]} ({BE.f1(s[2])} ★, {s[3]} reseñas)' for s in tp)
    top_en = '; '.join(f'{s[0]} ({BE.f1en(s[2])} ★, {s[3]} reviews)' for s in tp)
    def ul(items): return '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in items) + '</ul>'
    h = BE.hero(t, ('Guía · Clases de bachata Madrid', 'Guide · Bachata classes in Madrid'),
        ('Clases de bachata en Madrid: escuelas, clases de prueba y cómo elegir', 'Bachata classes in Madrid: schools, trial classes and how to choose'),
        ('Qué escuelas de Madrid dan clases de bachata, qué publican sobre niveles, clases de prueba y matrícula, y cómo elegir según barrio y metro. Con datos de las webs de las escuelas.',
         'Which Madrid schools teach Bachata, what they publish about levels, trial classes and enrolment, and how to choose by district and metro. Based on the schools\' own websites.'),
        [('cal', f'<b>{n} escuelas</b> en nuestra lista', f'<b>{n} schools</b> in our list'), ('check', 'Webs revisadas en <b>noviembre de 2026</b>', 'Websites checked in <b>November 2026</b>')],
        f'<a class="btn btn-gold" href="/es/bachata-madrid">{t("span", "Ver el ranking de Madrid", "See the Madrid ranking")}</a>')
    body = ''
    body += BE.sec(t, 1, ('Clases de bachata en Madrid de un vistazo', 'Bachata classes in Madrid at a glance'),
        t('p', f'En Madrid hemos encontrado {n} escuelas y sedes con bachata en su oferta (algunas tienen varias salas). Entre las de nota más alta en Google figuran: {top_es} (octubre de 2026). Es una clasificación provisional, no el ranking final de primavera de 2027.',
               f'In Madrid we found {n} schools and locations offering Bachata (some have several rooms). Among the highest Google ratings are: {top_en} (October 2026). This is an interim standing, not the final spring 2027 ranking.')
        + t('p', 'La lista completa, con puntos y enlace a cada escuela, está en <a href="/es/bachata-madrid">Bachata Madrid: las mejores escuelas de baile 2027</a>. Aquí explicamos cómo organizan las clases, qué se publica sobre clases de prueba y qué preguntar. Para una visión de toda España, mira <a href="/es/clases-de-bachata">clases de bachata en España</a>.',
                 'The full list with points and links to each school is on <a href="/es/bachata-madrid">Bachata Madrid: the best dance schools 2027</a>. Here we explain how classes are organised, what is published about trial classes and what to ask. For all of Spain, see <a href="/es/clases-de-bachata">Bachata classes in Spain</a>.'), alt=False)
    body += BE.sec(t, 2, ('Cuatro escuelas madrileñas, según sus webs', 'Four Madrid schools, according to their websites'),
        t('p', 'Hemos leído en noviembre de 2026 las webs de varias escuelas. Esto es lo que dicen, tal cual; horarios y precios cambian cada temporada, así que confírmalos con la escuela.',
               'In November 2026 we read the websites of several schools. This is what they say, as stated; timetables and prices change every season, so confirm them with the school.')
        + '<h3>' + t('span', lk('http://www.clasesdesalsaybachata.com/', 'Premiumdance') + ' (Calle Ambros 34)', lk('http://www.clasesdesalsaybachata.com/', 'Premiumdance') + ' (Calle Ambros 34)') + '</h3>'
        + ul([('Según su web, está cerca de las estaciones de metro O’Donnell, Manuel Becerra, Goya y Ventas.', 'According to its website it is near the metro stations O’Donnell, Manuel Becerra, Goya and Ventas.'),
              ('Enseña bachata moderna sensual y bachata fusión de pasos libres, junto a salsa cubana, timba, lady style y otros estilos. Habla de grupos para todos los niveles y de «4 niveles diferenciados» para salsa cubana y bachata, sin nombrarlos.', 'It teaches modern sensual Bachata and free-step fusion Bachata alongside Cuban salsa, timba, lady style and other styles. It mentions groups for all levels and “4 distinct levels” for Cuban salsa and Bachata, without naming them.'),
              ('No hace falta ir en pareja: dice que equilibra el número de chicos y chicas en cada clase. Ofrece una clase de prueba a precio promocional y sin compromiso; el horario de septiembre de 2026 a junio de 2027 está en una imagen.', 'You do not need to come with a partner: it says it balances the number of men and women in each class. It offers a trial class at a promotional price with no commitment; the September 2026 to June 2027 timetable is an image.')])
        + '<h3>' + t('span', lk('https://www.yobailoacademiadebaile.com', 'Yo Bailo Academia de Baile') + ' (Calle Cafeto 5)', lk('https://www.yobailoacademiadebaile.com', 'Yo Bailo Academia de Baile') + ' (Calle Cafeto 5)') + '</h3>'
        + ul([('Metro Pacífico (líneas 1 y 6). Da clases de lunes a domingo; enseña salsa, bachata, kizomba, reparto, afrobeats y bachazouk, entre otros.', 'Metro Pacífico (lines 1 and 6). Classes run Monday to Sunday; it teaches salsa, Bachata, kizomba, reparto, afrobeats and bachazouk, among others.'),
              ('La primera clase es gratis y se reserva en su app. Durante las jornadas de puertas abiertas de septiembre, la matrícula era gratis y había un 15 % de descuento en el bono de 20 clases. Los precios van en una página aparte.', 'The first class is free and booked through its app. During the September open days enrolment was free and there was a 15% discount on the 20-class pass. Prices are on a separate page.')])
        + '<h3>' + t('span', lk('https://www.dancingboulevard.com', 'Dancing Boulevard') + ' (Calle de Andorra 65)', lk('https://www.dancingboulevard.com', 'Dancing Boulevard') + ' (Calle de Andorra 65)') + '</h3>'
        + ul([('Salsa y bachata entre más de una docena de estilos. Su web promete «primera clase gratis», «sin matrícula» y «sin compromiso de permanencia».', 'Salsa and Bachata among more than a dozen styles. Its website promises a “free first class”, “no enrolment fee” and “no minimum commitment”.'),
              ('Horarios y precios están en secciones aparte, con lo que aquí no podemos citarlos.', 'Timetables and prices are in separate sections, so we cannot quote them here.')])
        + '<h3>' + t('span', lk('https://evolutiondance.es', 'Evolution Dance School') + ' (Chamberí, Marqués de Lema 13)', lk('https://evolutiondance.es', 'Evolution Dance School') + ' (Chamberí, Marqués de Lema 13)') + '</h3>'
        + ul([('A unos dos minutos a pie del metro Cuatro Caminos, según su web.', 'About two minutes on foot from Cuatro Caminos metro, according to its website.'),
              ('La bachata aparece como sensual, tradicional, lady style y men style, con clases para principiantes, intermedios y avanzados.', 'Bachata appears as sensual, traditional, lady style and men style, with classes for beginners, intermediate and advanced students.'),
              ('La primera clase es gratis de lunes a jueves; viernes y sábados, si compras un bono de clases ese mismo día. Se reserva por WhatsApp.', 'The first class is free Monday to Thursday; on Fridays and Saturdays only if you buy a class pass the same day. You book by WhatsApp.')]))
    body += BE.sec(t, 3, ('Clase de prueba, matrícula y precios: lo que se publica', 'Trial class, enrolment and prices: what is published'),
        t('p', 'En las cuatro webs hay clase de prueba o primera clase gratis, y ninguna muestra importes en la página que leímos: todas remiten a páginas de precios y horarios aparte. Resumen de lo publicado:',
               'All four websites offer a trial or free first class, and none shows amounts on the page we read: they all point to separate price and timetable pages. Summary of what is published:')
        + ul([('<strong>Premiumdance:</strong> clase de prueba a precio promocional, sin compromiso.', '<strong>Premiumdance:</strong> trial class at a promotional price, no commitment.'),
              ('<strong>Yo Bailo:</strong> primera clase gratis por la app; matrícula gratis en las jornadas de puertas abiertas.', '<strong>Yo Bailo:</strong> first class free through the app; free enrolment during the open days.'),
              ('<strong>Dancing Boulevard:</strong> primera clase gratis, sin matrícula y sin compromiso de permanencia.', '<strong>Dancing Boulevard:</strong> free first class, no enrolment fee and no minimum commitment.'),
              ('<strong>Evolution Dance School:</strong> primera clase gratis de lunes a jueves.', '<strong>Evolution Dance School:</strong> first class free Monday to Thursday.')])
        + t('p', 'Antes de pagar un bono, pide el precio mensual del grupo, cuántas horas incluye y si la clase de prueba se descuenta.', 'Before paying for a pass, ask for the monthly group price, how many hours it includes and whether the trial class is deducted.'))
    body += BE.sec(t, 4, ('Madrid es grande: elige por barrio y metro', 'Madrid is big: choose by district and metro'),
        t('p', 'Madrid tiene escuelas repartidas por todo el mapa, y una clase a la que tardas una hora en llegar se abandona antes. Las webs que leímos indican estas referencias: Premiumdance cerca de O’Donnell, Goya y Ventas; Yo Bailo en Pacífico; Evolution en Cuatro Caminos. Salsabachata, de la lista, tiene varias sedes (Ventas, Avenida de América, Quevedo y Sol) y cada una tiene su ficha en nuestra página de Madrid.',
               'Madrid has schools all over the map, and a class that takes an hour to reach gets dropped sooner. The websites we read give these references: Premiumdance near O’Donnell, Goya and Ventas; Yo Bailo at Pacífico; Evolution at Cuatro Caminos. Salsabachata, from our list, has several locations (Ventas, Avenida de América, Quevedo and Sol), each with its own profile on our Madrid page.')
        + t('p', 'Si es tu primera vez, empieza por el nivel de iniciación aunque hayas bailado otros estilos. Nuestra guía de principiantes (en alemán) está en <a href="/bachata-fuer-anfaenger">Bachata für Anfänger</a>, y el paso básico en <a href="/bachata-grundschritt">Bachata Grundschritt</a>.',
                 'If it is your first time, start at the beginner level even if you have danced other styles. Our beginner guide (in German) is at <a href="/bachata-fuer-anfaenger">Bachata for beginners</a>, and the basic step at <a href="/bachata-grundschritt">Bachata basic step</a>.'))
    body += BE.sec(t, 5, ('Qué preguntar antes de apuntarte', 'What to ask before you sign up'),
        ul([('<strong>¿Qué estilo?</strong> Moderna, sensual, tradicional y lady style son clases distintas; Evolution, por ejemplo, las separa.', '<strong>Which style?</strong> Modern, sensual, traditional and lady style are different classes; Evolution, for example, lists them separately.'),
            ('<strong>¿Qué niveles hay en bachata?</strong> Premiumdance habla de cuatro niveles pero no los nombra; pregunta qué incluye cada uno.', '<strong>Which Bachata levels exist?</strong> Premiumdance mentions four levels but does not name them; ask what each includes.'),
            ('<strong>¿Cuándo empieza el próximo grupo?</strong> Los horarios cambian por temporada; algunas escuelas lo publican como imagen.', '<strong>When does the next group start?</strong> Timetables change by season; some schools publish them as an image.'),
            ('<strong>¿Hay matrícula y permanencia?</strong> Dancing Boulevard indica que no; en otras escuelas hay que preguntarlo.', '<strong>Is there an enrolment fee and a minimum stay?</strong> Dancing Boulevard says no; at other schools you have to ask.')]))
    body += BE.sec(t, 6, ('Cómo hemos preparado esta guía', 'How we prepared this guide'),
        t('p', f'Hemos leído en noviembre de 2026 las webs de Premiumdance, Yo Bailo, Dancing Boulevard y Evolution Dance School, y usamos las valoraciones de Google de octubre de 2026 de nuestra lista. Las demás {n - 4} escuelas y sedes de Madrid están enlazadas en la <a href="/es/bachata-madrid">página de la ciudad</a>; no hemos analizado aquí su oferta. La clasificación es independiente: los puestos no se pueden comprar.',
               f'In November 2026 we read the websites of Premiumdance, Yo Bailo, Dancing Boulevard and Evolution Dance School, and we use the October 2026 Google ratings from our list. The other {n - 4} schools and locations in Madrid are linked on the <a href="/es/bachata-madrid">city page</a>; we did not analyse their offers here. The ranking is independent: places cannot be bought.'))
    faq = [
        ('¿Dónde puedo aprender bachata en Madrid?', 'Where can I learn Bachata in Madrid?',
         f'En Madrid hemos encontrado {n} escuelas y sedes con bachata, entre ellas Premiumdance, Yo Bailo Academia de Baile, Dancing Boulevard, Evolution Dance School y Salsabachata. La lista completa está en nuestra página de Bachata Madrid.',
         f'In Madrid we found {n} schools and locations with Bachata, including Premiumdance, Yo Bailo Academia de Baile, Dancing Boulevard, Evolution Dance School and Salsabachata. The full list is on our Bachata Madrid page.'),
        ('¿Hay clases de prueba gratis en Madrid?', 'Are there free trial classes in Madrid?',
         'Sí, en varias. Yo Bailo, Dancing Boulevard y Evolution Dance School anuncian la primera clase gratis (Evolution, de lunes a jueves), y Premiumdance ofrece una clase de prueba a precio promocional. Confirma las condiciones al reservar.',
         'Yes, at several. Yo Bailo, Dancing Boulevard and Evolution Dance School advertise a free first class (Evolution, Monday to Thursday), and Premiumdance offers a trial class at a promotional price. Confirm the conditions when you book.'),
        ('¿Cuánto cuesta una clase de bachata en Madrid?', 'How much does a Bachata class in Madrid cost?',
         'Las cuatro escuelas que leímos no muestran importes en la página principal y remiten a páginas de precios aparte. Pide siempre el precio del grupo, las horas incluidas y la permanencia antes de pagar.',
         'The four schools we read do not show amounts on the main page and point to separate price pages. Always ask for the group price, the hours included and the minimum stay before paying.'),
        ('¿Necesito pareja para una clase de bachata?', 'Do I need a partner for a Bachata class?',
         'Normalmente no. Premiumdance dice expresamente que no hace falta ir en pareja y que equilibra el número de chicos y chicas. En otras escuelas se rotan las parejas; pregúntalo antes.',
         'Usually not. Premiumdance says explicitly that you do not need to come with a partner and that it balances the number of men and women. At other schools partners rotate; ask beforehand.'),
        ('¿Cuál es la mejor escuela de bachata de Madrid?', 'What is the best Bachata school in Madrid?',
         f'Según nuestros datos provisionales de octubre de 2026, entre las de mejor valoración en Google están {top_es}. No es el ranking final, que se publicará en primavera de 2027.',
         f'By our interim data from October 2026, the best Google ratings include {top_en}. This is not the final ranking, which follows in spring 2027.'),
    ]
    body += BE.faq_html(t, faq)
    BE.es_page('es/clases-de-bachata-madrid.html', 'es/clases-de-bachata-madrid.html',
        'Clases de bachata Madrid: escuelas, niveles y precios',
        'Clases de bachata en Madrid: qué publican Premiumdance, Yo Bailo, Dancing Boulevard y Evolution sobre niveles y clases de prueba gratis, y cómo elegir por barrio y metro.',
        'Bachata classes Madrid: schools, levels and prices',
        'Bachata classes in Madrid: what Premiumdance, Yo Bailo, Dancing Boulevard and Evolution publish about levels and free trial classes, and how to choose by district and metro.',
        h + body, t.en, [crumbs('Bachata Madrid', 'es/bachata-madrid.html'), crumbs('Clases de bachata Madrid', 'es/clases-de-bachata-madrid.html'), faq_schema(faq)])

# ===================================================================== BARCELONA
def barcelona():
    ss = BE.by_city('barcelona'); n = len(ss); t = T('sc2')
    tp = tops(ss, BE.f1)
    top_es = '; '.join(f'{s[0]} ({BE.f1(s[2])} ★, {s[3]} reseñas)' for s in tp)
    top_en = '; '.join(f'{s[0]} ({BE.f1en(s[2])} ★, {s[3]} reviews)' for s in tp)
    def ul(items): return '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in items) + '</ul>'
    h = BE.hero(t, ('Guía · Clases de bachata Barcelona', 'Guide · Bachata classes in Barcelona'),
        ('Clases de bachata en Barcelona: escuelas, precios y cómo elegir', 'Bachata classes in Barcelona: schools, prices and how to choose'),
        ('Qué publican las escuelas de Barcelona sobre niveles, precios y clases de prueba, con direcciones y horarios tal como aparecen en sus webs, y qué preguntar antes de apuntarte.',
         'What Barcelona schools publish about levels, prices and trial classes, with addresses and timetables as they appear on their websites, and what to ask before you sign up.'),
        [('cal', f'<b>{n} escuelas</b> en nuestra lista', f'<b>{n} schools</b> in our list'), ('check', 'Webs revisadas en <b>noviembre de 2026</b>', 'Websites checked in <b>November 2026</b>')],
        f'<a class="btn btn-gold" href="/es/bachata-barcelona">{t("span", "Ver el ranking de Barcelona", "See the Barcelona ranking")}</a>')
    body = ''
    body += BE.sec(t, 1, ('Clases de bachata en Barcelona de un vistazo', 'Bachata classes in Barcelona at a glance'),
        t('p', f'En Barcelona hemos encontrado {n} escuelas con bachata. Entre las de nota más alta en Google: {top_es} (octubre de 2026). Es una clasificación provisional; el ranking final llega en primavera de 2027.',
               f'In Barcelona we found {n} schools with Bachata. Among the highest Google ratings: {top_en} (October 2026). This is an interim standing; the final ranking follows in spring 2027.')
        + t('p', 'La lista completa, con puntos y enlace a cada escuela, está en <a href="/es/bachata-barcelona">Bachata Barcelona: las mejores escuelas de baile 2027</a>. Para el panorama de toda España, mira <a href="/es/clases-de-bachata">clases de bachata en España</a>.',
                 'The full list with points and links to each school is on <a href="/es/bachata-barcelona">Bachata Barcelona: the best dance schools 2027</a>. For all of Spain, see <a href="/es/clases-de-bachata">Bachata classes in Spain</a>.'), alt=False)
    body += BE.sec(t, 2, ('Cuatro escuelas barcelonesas, según sus webs', 'Four Barcelona schools, according to their websites'),
        t('p', 'Hemos leído en noviembre de 2026 las webs de estas escuelas. Esto es lo que dicen, tal cual; los horarios cambian cada temporada, así que confírmalos con la escuela.',
               'In November 2026 we read the websites of these schools. This is what they say, as stated; timetables change every season, so confirm them with the school.')
        + '<h3>' + t('span', lk('https://dancelab.es/', 'DanceLab School') + ' (Carrer del Concili de Trento 46, Clot)', lk('https://dancelab.es/', 'DanceLab School') + ' (Carrer del Concili de Trento 46, Clot)') + '</h3>'
        + ul([('Es la que publica importes: 52 € al mes por 1 hora semanal o 72 € al mes por 2 horas semanales, más 60 € de matrícula en ambos casos. Los dos planes están abiertos a todos los niveles.', 'It is the one that publishes amounts: €52 a month for 1 hour a week or €72 a month for 2 hours a week, plus a €60 enrolment fee in both cases. Both plans are open to all levels.'),
              ('Ofrece bachata general, sensual, lady style y fusión, además de salsa, hip hop y otros estilos. La primera clase es gratis «según disponibilidad».', 'It offers general, sensual, lady style and fusion Bachata, plus salsa, hip hop and other styles. The first class is free “subject to availability”.'),
              ('El horario de la temporada 2026-27 está en una página aparte.', 'The 2026-27 timetable is on a separate page.')])
        + '<h3>' + t('span', lk('https://www.sevendance.com/', 'Seven Dance') + ' (C/ Perill 10)', lk('https://www.sevendance.com/', 'Seven Dance') + ' (C/ Perill 10)') + '</h3>'
        + ul([('Escuela con más de 700 m² en el centro y un club privado, Dio Club. Enseña bachata, salsa, salsa cubana, bailes de salón y baile nupcial.', 'A school of more than 700 m² in the centre with a private club, Dio Club. It teaches Bachata, salsa, Cuban salsa, ballroom and wedding dance.'),
              ('Anuncia clases de prueba gratuitas de salsa, bachata y bailes de salón del 8 al 11 de enero. Entre sus prácticas figuran los «Jueves de Bachata Nights» (22:00–02:00) y el «Domingo Tardeo de Bachateo» (18:00–22:00).', 'It announces free trial classes in salsa, Bachata and ballroom from 8 to 11 January. Its practice sessions include “Bachata Nights Thursdays” (22:00–02:00) and “Sunday Tardeo de Bachateo” (18:00–22:00).'),
              ('Los precios no aparecen en la página principal; solo un enlace a «Servicios y tarifas».', 'Prices do not appear on the main page; there is only a link to “Services and rates”.')])
        + '<h3>' + t('span', lk('https://www.barcelonabachata.com/', 'Barcelona Bachata School') + ' (Carrer de Galileu 11)', lk('https://www.barcelonabachata.com/', 'Barcelona Bachata School') + ' (Carrer de Galileu 11)') + '</h3>'
        + ul([('Cerca de la parada Plaça de Sants (L1/L5). Su web indica dos niveles: básico (menos de 6 meses) e intermedio (6 meses o más), con las clases los domingos a las 17:00 y a las 18:00.', 'Near the Plaça de Sants stop (L1/L5). Its website lists two levels: basic (under 6 months) and intermediate (6 months or more), with classes on Sundays at 17:00 and 18:00.'),
              ('Ofrece una clase de prueba gratuita y dice que no hace falta experiencia previa. No publica precios.', 'It offers a free trial lesson and says no previous experience is needed. It does not publish prices.'),
              ('Ojo con los listados de terceros: un anuncio externo que vimos mostraba estas mismas clases en miércoles. Confía en la web de la escuela.', 'Beware of third-party listings: an external listing we saw showed these same classes on Wednesdays. Trust the school’s own website.')])
        + '<h3>' + t('span', lk('https://bcnbaila.es/', 'BCN Baila') + ' (Carrer d’Aragó 178)', lk('https://bcnbaila.es/', 'BCN Baila') + ' (Carrer d’Aragó 178)') + '</h3>'
        + ul([('Salsa cubana, salsa en línea y bachata, desde principiantes absolutos hasta avanzados. Ofrece «prueba sin compromiso», talleres e intensivos de verano y organiza salidas sociales.', 'Cuban salsa, line salsa and Bachata, from complete beginners to advanced. It offers a “no-commitment trial”, summer workshops and intensives and organises social outings.'),
              ('Según su ficha en Urban Sports Club, no hace falta ir con pareja ni tener conocimientos. Los precios y horarios están en páginas aparte.', 'According to its Urban Sports Club listing, you need neither a partner nor prior knowledge. Prices and timetables are on separate pages.')]))
    body += BE.sec(t, 3, ('Precios y clase de prueba: lo que se publica', 'Prices and trial class: what is published'),
        t('p', 'Lo más llamativo es lo poco que se publica. Esto es todo lo que encontramos:', 'What stands out is how little is published. This is everything we found:')
        + ul([('<strong>DanceLab School:</strong> 52 €/mes (1 h semanal) o 72 €/mes (2 h semanales), más 60 € de matrícula; primera clase gratis según disponibilidad.', '<strong>DanceLab School:</strong> €52/month (1 h a week) or €72/month (2 h a week), plus €60 enrolment; first class free subject to availability.'),
              ('<strong>Seven Dance:</strong> clases de prueba gratis del 8 al 11 de enero; tarifas en otra página.', '<strong>Seven Dance:</strong> free trial classes from 8 to 11 January; rates on another page.'),
              ('<strong>Barcelona Bachata School:</strong> clase de prueba gratuita; sin precios publicados.', '<strong>Barcelona Bachata School:</strong> free trial lesson; no prices published.'),
              ('<strong>BCN Baila:</strong> prueba sin compromiso; precios en otra página.', '<strong>BCN Baila:</strong> no-commitment trial; prices on another page.')])
        + t('p', 'Con una matrícula de 60 € en DanceLab, el primer mes de 1 hora semanal cuesta 112 € (52 € + 60 €); calcula siempre el primer mes con matrícula incluida.', 'With a €60 enrolment at DanceLab, the first month at 1 hour a week costs €112 (€52 + €60); always work out the first month including enrolment.'))
    body += BE.sec(t, 4, ('Niveles y primeros pasos', 'Levels and first steps'),
        t('p', 'Barcelona Bachata School separa a quien lleva menos de seis meses de quien lleva más; es un criterio sencillo para elegir. Si empiezas de cero, elige el grupo básico aunque hayas bailado otros estilos: el paso básico de la bachata se explica en <a href="/bachata-grundschritt">Bachata Grundschritt</a> (en alemán) y una guía para principiantes está en <a href="/bachata-fuer-anfaenger">Bachata für Anfänger</a>.',
               'Barcelona Bachata School separates people with under six months from those with more; a simple rule for choosing. If you start from zero, pick the basic group even if you have danced other styles: the basic Bachata step is explained at <a href="/bachata-grundschritt">Bachata basic step</a> (in German) and a beginner guide is at <a href="/bachata-fuer-anfaenger">Bachata for beginners</a>.')
        + t('p', 'Después de la clase, lo que consolida es el social: Seven Dance anuncia noches de bachata en su club. Para saber cómo es una noche de baile, lee <a href="/bachata-party">Bachata Party</a> y <a href="/bachata-socials">Bachata-Socials</a> (en alemán).', 'After class, what consolidates is the social: Seven Dance announces Bachata nights at its club. To see what a dance night is like, read <a href="/bachata-party">Bachata party</a> and <a href="/bachata-socials">Bachata socials</a> (in German).'))
    body += BE.sec(t, 5, ('Qué preguntar antes de apuntarte', 'What to ask before you sign up'),
        ul([('<strong>¿Cuánto cuesta el primer mes?</strong> Incluye matrícula, como en DanceLab (60 €).', '<strong>What does the first month cost?</strong> Include enrolment, as at DanceLab (€60).'),
            ('<strong>¿Qué día y a qué hora?</strong> Comprueba en la web de la escuela, no en un listado externo.', '<strong>Which day and time?</strong> Check the school’s own website, not an external listing.'),
            ('<strong>¿Cuándo empieza el siguiente grupo?</strong> Algunas escuelas publican el horario en otra página.', '<strong>When does the next group start?</strong> Some schools publish the timetable on another page.'),
            ('<strong>¿Se descuenta la clase de prueba?</strong> Pregúntalo antes de pagar un bono.', '<strong>Is the trial class deducted?</strong> Ask before you pay for a pass.')]))
    body += BE.sec(t, 6, ('Cómo hemos preparado esta guía', 'How we prepared this guide'),
        t('p', f'Hemos leído en noviembre de 2026 las webs de DanceLab School, Seven Dance, Barcelona Bachata School y BCN Baila (esta última, junto con su ficha en Urban Sports Club), y usamos las valoraciones de Google de octubre de 2026 de nuestra lista. Las demás {n - 4} escuelas están enlazadas en la <a href="/es/bachata-barcelona">página de la ciudad</a>; no hemos analizado aquí su oferta. La clasificación es independiente: los puestos no se pueden comprar.',
               f'In November 2026 we read the websites of DanceLab School, Seven Dance, Barcelona Bachata School and BCN Baila (the latter together with its Urban Sports Club listing), and we use the October 2026 Google ratings from our list. The other {n - 4} schools are linked on the <a href="/es/bachata-barcelona">city page</a>; we did not analyse their offers here. The ranking is independent: places cannot be bought.'))
    faq = [
        ('¿Dónde puedo aprender bachata en Barcelona?', 'Where can I learn Bachata in Barcelona?',
         f'En Barcelona hemos encontrado {n} escuelas con bachata, entre ellas DanceLab School, Seven Dance, BCN Baila y Barcelona Bachata School. La lista completa está en nuestra página de Bachata Barcelona.',
         f'In Barcelona we found {n} schools with Bachata, including DanceLab School, Seven Dance, BCN Baila and Barcelona Bachata School. The full list is on our Bachata Barcelona page.'),
        ('¿Cuánto cuesta una clase de bachata en Barcelona?', 'How much does a Bachata class in Barcelona cost?',
         'De las escuelas que leímos, solo DanceLab School publica importes: 52 € al mes por 1 hora semanal y 72 € por 2 horas, más 60 € de matrícula. Las demás remiten a páginas de tarifas o no publican precios.',
         'Of the schools we read, only DanceLab School publishes amounts: €52 a month for 1 hour a week and €72 for 2 hours, plus a €60 enrolment fee. The others point to rate pages or do not publish prices.'),
        ('¿Hay clases de prueba gratuitas en Barcelona?', 'Are there free trial classes in Barcelona?',
         'Sí. DanceLab School ofrece la primera clase gratis según disponibilidad; Barcelona Bachata School, una clase de prueba gratuita; Seven Dance anuncia clases de prueba gratis del 8 al 11 de enero; y BCN Baila, una prueba sin compromiso.',
         'Yes. DanceLab School offers a first class free subject to availability; Barcelona Bachata School a free trial lesson; Seven Dance announces free trial classes from 8 to 11 January; and BCN Baila a no-commitment trial.'),
        ('¿Qué nivel elijo si nunca he bailado?', 'Which level should I pick if I have never danced?',
         'El básico. Barcelona Bachata School da el nivel básico a quien lleva menos de seis meses, y dice que no hace falta experiencia previa.',
         'The basic one. Barcelona Bachata School gives the basic level to people with under six months of experience, and says no previous experience is needed.'),
        ('¿Cuál es la mejor escuela de bachata de Barcelona?', 'What is the best Bachata school in Barcelona?',
         f'Según nuestros datos provisionales de octubre de 2026, entre las mejor valoradas en Google están {top_es}. No es el ranking final, que se publicará en primavera de 2027.',
         f'By our interim data from October 2026, the best Google ratings include {top_en}. This is not the final ranking, which follows in spring 2027.'),
    ]
    body += BE.faq_html(t, faq)
    BE.es_page('es/clases-de-bachata-barcelona.html', 'es/clases-de-bachata-barcelona.html',
        'Clases de bachata Barcelona: escuelas, niveles y precios',
        'Clases de bachata en Barcelona: precios de DanceLab, clases de prueba gratis en Seven Dance y otras escuelas, niveles y qué preguntar antes de apuntarte.',
        'Bachata classes Barcelona: schools, levels and prices',
        'Bachata classes in Barcelona: DanceLab prices, free trial classes at Seven Dance and other schools, levels and what to ask before you sign up.',
        h + body, t.en, [crumbs('Bachata Barcelona', 'es/bachata-barcelona.html'), crumbs('Clases de bachata Barcelona', 'es/clases-de-bachata-barcelona.html'), faq_schema(faq)])

# ===================================================================== LONDON
def london():
    ss = BU.by_city('london'); n = len(ss); t = T('sc3')
    tp = tops(ss, BU.f1en)
    top_en = '; '.join(f'{s[0]} ({BU.f1en(s[2])} ★, {s[3]} reviews)' for s in tp)
    def p(a): return t('p', a, a)
    def ul(items): return '<ul>' + ''.join(f'<li>{t("span", a, a)}</li>' for a in items) + '</ul>'
    def sec(i, h2, blocks, alt=True): return BU.sec(t, i, (h2, h2), blocks, alt=alt)
    def h3(x): return '<h3>' + t('span', x, x) + '</h3>'
    h = BU.hero(t, ('Guide · Bachata classes in London', 'Guide · Bachata classes in London'),
        ('Bachata classes in London: schools, prices and venues', 'Bachata classes in London: schools, prices and venues'),
        ('What London schools publish about venues, levels, prices and trial classes, with details taken from their own websites, and what to ask before you book.',
         'What London schools publish about venues, levels, prices and trial classes, with details taken from their own websites, and what to ask before you book.'),
        [('cal', f'<b>{n} schools</b> in our list', f'<b>{n} schools</b> in our list'), ('check', 'Websites checked in <b>November 2026</b>', 'Websites checked in <b>November 2026</b>')],
        f'<a class="btn btn-gold" href="/uk/bachata-london">{t("span", "See the London ranking", "See the London ranking")}</a>')
    body = ''
    body += sec(1, 'Bachata classes in London at a glance',
        p(f'Our list has {n} schools and clubs teaching Bachata in London. The highest Google ratings right now: {top_en} (October 2026). This is an interim standing; the final ranking follows in spring 2027.')
        + p('The full list with points and a link to each school is on <a href="/uk/bachata-london">Bachata London: the best dance schools 2027</a>. For the whole country, see <a href="/uk/bachata-classes">Bachata classes in the UK</a>.'), alt=False)
    body += sec(2, 'Four London providers, according to their websites',
        p('In November 2026 we read the websites of several London providers. This is what they say, as stated; evenings and venues change by season, so confirm before you go.')
        + h3(lk('https://roguebachata.com/', 'Rogue Bachata') + ' (Clapham and King\'s Cross)')
        + ul(['Tuesdays at Cafe Sol, 56 Clapham High Street SW4 7UL: a class at 7:30pm (£10) and a free social from 8:30pm.',
              'Wednesdays at Keystone Crescent Members Club, King\'s Cross N1 9DX: two classes, Beginners or Experienced, 7:30–8:45pm (£10 per class), then a free social from 9pm. The Beginners class is for dancers with 0 to 1 year of Bachata experience.',
              'The site says "no partner, no experience, no pressure", and partners rotate in class. Both weekly nights are currently paused, and the site says they return in January 2027. Private lessons start at £70 an hour.'])
        + h3(lk('https://clubazucar.co.uk/', 'Club Azucar') + ' (Hammersmith)')
        + ul(['Classes are listed at Rivercourt Methodist Church, King Street, Hammersmith W6 9JT, near Ravenscourt Park. The footer shows a different address (233 King St W6 9LP), so confirm before visiting.',
              'Beginner Bachata for couples and singles runs on Wednesdays at 8pm, from £7.50 a class. Only the beginner Bachata class is listed.',
              'Class packs: 6 lessons £72, 10 lessons £120, 15 lessons £165 and 20 lessons £200, valid for Zumba, salsa, reggaeton and Bachata. A free trial is not stated.'])
        + h3(lk('https://dancebuzz.co.uk/', 'Dancebuzz') + ' (over 20 central locations)')
        + ul(['An adult dance school that lists Bachata among ballroom, Latin, street dance, salsa, swing and more, with evening and weekend courses in "over 20 central locations".',
              'Levels, prices and venues for Bachata are not stated on the page we read; the school gives a phone number (0203 086 8133) for enquiries.'])
        + h3(lk('https://ritmolatinolondon.com/', 'Ritmo Latino Dance Studio') + ' (Vauxhall)')
        + ul(['Describes "weekly Latin dance nights and weekenders in Vauxhall", covering Bachata, salsa, zouk and heels socials, plus London Sensual Days weekenders.',
              'The page gives no class schedule, levels, prices or trial class, so treat it as a social venue and ask for class details.']))
    body += sec(3, 'Prices and trial classes: what is published',
        p('Prices are the thing London schools publish least, so here is everything we found:')
        + ul(['<strong>Rogue Bachata:</strong> £10 per class; private lessons from £70 an hour; no free trial stated.',
              '<strong>Club Azucar:</strong> beginner Bachata from £7.50 a class; packs of 6 to 20 lessons at £72 to £200; private salsa or Latin lessons from £75.',
              '<strong>Dancebuzz and Ritmo Latino:</strong> no Bachata prices on the pages we read.'])
        + p('Per class, the 6-lesson pack at Club Azucar works out at £12 and the 20-lesson pack at £10 (£72 ÷ 6 and £200 ÷ 20), against £7.50 for a single beginner class. Do the sum for how often you will really come.'))
    body += sec(4, 'Choosing in a city this size',
        p('London is wide, so pick by evening and travel time first, then by level. The two weekly Rogue Bachata nights are in different parts of the city (Clapham and King\'s Cross); Club Azucar is in Hammersmith; Ritmo Latino in Vauxhall. A class near your commute is the one you will keep going to.')
        + p('If you are brand new, choose a beginners class and do not skip the basic level even if you have danced another style. Our beginner guide (in German) is at <a href="/bachata-fuer-anfaenger">Bachata für Anfänger</a>, and the basic step at <a href="/bachata-grundschritt">Bachata Grundschritt</a>.'), alt=False)
    body += sec(5, 'What to ask before you book',
        ul(['<strong>Is the class running?</strong> Rogue Bachata\'s weekly nights are paused until January 2027; breaks like this are common.',
            '<strong>Which address?</strong> Club Azucar lists two addresses on its site; check which one the class uses.',
            '<strong>Is there a free trial, and is it credited?</strong> Most of the pages we read do not say.',
            '<strong>Do I need a partner?</strong> Rogue Bachata says no; Club Azucar lists beginner Bachata for couples and singles.']))
    body += sec(6, 'How we prepared this guide',
        p(f'In November 2026 we read the websites of Rogue Bachata, Club Azucar, Dancebuzz and Ritmo Latino Dance Studio, and we use the October 2026 Google ratings from our list. The other {n - 4} London schools are linked on the <a href="/uk/bachata-london">city page</a>; we did not analyse their offers here. The ranking is independent: places cannot be bought.'))
    faq = [
        ('Where can I learn Bachata in London?', 'Where can I learn Bachata in London?',
         f'Our list has {n} schools and clubs teaching Bachata in London, including Rogue Bachata, Club Azucar, Dancebuzz and Ritmo Latino Dance Studio. The full list is on our Bachata London page.',
         f'Our list has {n} schools and clubs teaching Bachata in London, including Rogue Bachata, Club Azucar, Dancebuzz and Ritmo Latino Dance Studio. The full list is on our Bachata London page.'),
        ('How much does a Bachata class in London cost?', 'How much does a Bachata class in London cost?',
         'Of the providers we read, Rogue Bachata charges £10 per class and Club Azucar lists beginner Bachata from £7.50, with packs of 6 to 20 lessons at £72 to £200. Others do not publish Bachata prices.',
         'Of the providers we read, Rogue Bachata charges £10 per class and Club Azucar lists beginner Bachata from £7.50, with packs of 6 to 20 lessons at £72 to £200. Others do not publish Bachata prices.'),
        ('Do I need a partner for a Bachata class?', 'Do I need a partner for a Bachata class?',
         'Usually not. Rogue Bachata says "no partner, no experience, no pressure" and rotates partners in class; Club Azucar lists beginner Bachata for couples and singles. Ask the school before your first class.',
         'Usually not. Rogue Bachata says "no partner, no experience, no pressure" and rotates partners in class; Club Azucar lists beginner Bachata for couples and singles. Ask the school before your first class.'),
        ('Are there Bachata classes in London in winter?', 'Are there Bachata classes in London in winter?',
         'Yes, but check first. Rogue Bachata\'s Tuesday and Wednesday nights are paused and return in January 2027, while Club Azucar lists a weekly Wednesday beginner Bachata class.',
         'Yes, but check first. Rogue Bachata\'s Tuesday and Wednesday nights are paused and return in January 2027, while Club Azucar lists a weekly Wednesday beginner Bachata class.'),
        ('What is the best Bachata school in London?', 'What is the best Bachata school in London?',
         f'By our interim data from October 2026, the best Google ratings include {top_en}. This is not the final ranking, which follows in spring 2027.',
         f'By our interim data from October 2026, the best Google ratings include {top_en}. This is not the final ranking, which follows in spring 2027.'),
    ]
    body += BU.faq_html(t, faq)
    BU.uk_page('uk/bachata-classes-london.html', 'uk/bachata-classes-london.html',
        'Bachata classes London: schools, prices and venues',
        'Bachata classes in London: venues, prices and levels at Rogue Bachata, Club Azucar, Dancebuzz and Ritmo Latino, according to their websites, and what to ask before you book.',
        'Bachata classes London: schools, prices and venues',
        'Bachata classes in London: venues, prices and levels at Rogue Bachata, Club Azucar, Dancebuzz and Ritmo Latino, according to their websites, and what to ask before you book.',
        h + body, t.en, [crumbs('Bachata London', 'uk/bachata-london.html'), crumbs('Bachata classes London', 'uk/bachata-classes-london.html'), faq_schema(faq)])

# ===================================================================== PARIS
def paris():
    ss = BF.by_city('paris'); n = len(ss); t = T('sc4')
    tp = tops(ss, BF.f1)
    top_fr = '; '.join(f'{s[0]} ({BF.f1(s[2])} ★, {s[3]} avis)' for s in tp)
    top_en = '; '.join(f'{s[0]} ({BF.f1en(s[2])} ★, {s[3]} reviews)' for s in tp)
    def ul(items): return '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in items) + '</ul>'
    h = BF.hero(t, ('Guide · Cours de bachata Paris', 'Guide · Bachata classes in Paris'),
        ('Cours de bachata à Paris : écoles, niveaux et tarifs', 'Bachata classes in Paris: schools, levels and prices'),
        ('Ce que publient les écoles parisiennes sur les niveaux, les tarifs et les cours d’essai, avec adresses et horaires tels qu’ils figurent sur leurs sites, et quoi demander avant de vous inscrire.',
         'What Paris schools publish about levels, prices and trial classes, with addresses and timetables as they appear on their websites, and what to ask before you sign up.'),
        [('cal', f'<b>{n} écoles</b> dans notre liste', f'<b>{n} schools</b> in our list'), ('check', 'Sites consultés en <b>novembre 2026</b>', 'Websites checked in <b>November 2026</b>')],
        f'<a class="btn btn-gold" href="/fr/bachata-paris">{t("span", "Voir le classement de Paris", "See the Paris ranking")}</a>')
    body = ''
    body += BF.sec(t, 1, ('Cours de bachata à Paris en un coup d’œil', 'Bachata classes in Paris at a glance'),
        t('p', f'À Paris, notre liste compte {n} écoles et lieux avec de la bachata. Parmi les meilleures notes Google : {top_fr} (octobre 2026). C’est un classement provisoire ; le classement final suit au printemps 2027.',
               f'Our list has {n} schools and venues with Bachata in Paris. Among the highest Google ratings: {top_en} (October 2026). This is an interim standing; the final ranking follows in spring 2027.')
        + t('p', 'La liste complète, avec points et lien vers chaque école, se trouve sur <a href="/fr/bachata-paris">Bachata Paris : les meilleures écoles de danse 2027</a>. Pour la France entière, voyez <a href="/fr/cours-de-bachata">cours de bachata en France</a>.',
                 'The full list with points and links to each school is on <a href="/fr/bachata-paris">Bachata Paris: the best dance schools 2027</a>. For all of France, see <a href="/fr/cours-de-bachata">Bachata classes in France</a>.'), alt=False)
    body += BF.sec(t, 2, ('Trois écoles parisiennes, d’après leurs sites', 'Three Paris schools, according to their websites'),
        t('p', 'En novembre 2026, nous avons lu les sites de plusieurs écoles. Voici ce qu’elles publient, tel quel ; les plannings et les tarifs changent chaque saison, confirmez-les auprès de l’école.',
               'In November 2026 we read the websites of several schools. This is what they publish, as stated; timetables and rates change every season, so confirm them with the school.')
        + '<h3>' + t('span', lk('https://bachataunighted.com/', 'Bachata Paris Unighted Académie') + ' (74 bis rue Lauriston, 16e)', lk('https://bachataunighted.com/', 'Bachata Paris Unighted Académie') + ' (74 bis rue Lauriston, 16th)') + '</h3>'
        + ul([('C’est la plus transparente sur les tarifs 2026-2027 : 395 € à l’année (33 cours, payables en trois fois), carte de 12 cours à 168 € (valable 5 mois), carte de 5 cours à 80 € (valable 3 mois) et cours à l’unité à 18 €.', 'It is the most transparent on 2026-2027 rates: €395 for the year (33 classes, payable in three instalments), a 12-class card at €168 (valid 5 months), a 5-class card at €80 (valid 3 months) and a single class at €18.'),
              ('Un cours débutant (Vuelta Sol) a lieu le jeudi de 19h00 à 20h30, puis le cours « intermédiaire évolutif » de 20h30 à 22h00. La saison commence le jeudi 17 septembre 2026, avec 33 séances hors vacances scolaires (zone C) et jours fériés. Groupes limités à 20 places.', 'A beginner class (Vuelta Sol) runs on Thursdays 19:00–20:30, followed by the “evolving intermediate” class 20:30–22:00. The season starts on Thursday 17 September 2026, with 33 sessions excluding school (zone C) and public holidays. Groups are limited to 20 places.'),
              ('Pas besoin de partenaire : on tourne pendant le cours, et les couples sont les bienvenus. Pour l’essai, le site se contredit : la FAQ parle d’un premier cours à −50 % déduit d’un forfait, le calendrier d’un « essai gratuit » aux portes ouvertes. Confirmez avant de réserver.', 'No partner needed: partners rotate in class, and couples are welcome. On the trial the site contradicts itself: the FAQ mentions a first class at −50% credited against a package, the calendar a “free trial” at the open house. Confirm before booking.')])
        + '<h3>' + t('span', lk('https://bachatamore.fr/', 'Bachatamore') + ' (31 rue Blomet, 15e)', lk('https://bachatamore.fr/', 'Bachatamore') + ' (31 rue Blomet, 15th)') + '</h3>'
        + ul([('École uniquement de bachata, avec un accent sur la bachata sensuelle. Elle accueille débutants et danseurs expérimentés et dit adapter les cours au niveau de chacun ; petits groupes.', 'A Bachata-only school with a focus on sensual Bachata. It welcomes beginners and experienced dancers and says it adapts to each student’s level; small groups.'),
              ('On peut venir « seul ou accompagné ». L’essai se réserve en ligne via Billetweb, en choisissant le cours ; si une place est libre, vous pouvez rejoindre le groupe dans l’année (premier arrivé, premier servi). Le calendrier est sur une page séparée et les tarifs ne figurent pas sur la page principale.', 'You can come “alone or accompanied”. The trial is booked online through Billetweb by choosing the class; if there is room you can join the group during the year (first come, first served). The calendar is on a separate page and rates are not on the main page.')])
        + '<h3>' + t('span', lk('https://parisbachatero.com/', 'Paris Bachatero') + ' (Paris 16e, cours collectifs et particuliers)', lk('https://parisbachatero.com/', 'Paris Bachatero') + ' (Paris 16th, group and private classes)') + '</h3>'
        + ul([('Six styles sont listés : dominicaine, moderne, sensuelle, bachatango, influence et bachazouk. Les débutants complets sont bienvenus, avec une progression décrite en 10 leçons ; un lieu de cours collectifs dans le 16e est annoncé pour la rentrée de septembre 2026.', 'Six styles are listed: Dominican, modern, sensual, bachatango, influence and bachazouk. Complete beginners are welcome, with a described 10-lesson progression; a group-class location in the 16th is announced for the September 2026 start.'),
              ('Tarifs des cours particuliers : 55 €/h à Paris, 65 €/h à domicile en Île-de-France, 65 €/h en studio (location de salle en plus), 75 €/h en couple et 80 €/h pour une ouverture de bal. Un « 1er cours découverte » sans engagement est proposé, sans prix indiqué. On peut venir seul.', 'Private lesson rates: €55/h in Paris, €65/h at your home in Île-de-France, €65/h in a studio (room rental extra), €75/h as a couple and €80/h for a wedding first dance. A “1st discovery class” with no commitment is offered, with no price stated. You can come alone.')]))
    body += BF.sec(t, 3, ('Tarifs et cours d’essai : ce qui est publié', 'Rates and trial classes: what is published'),
        t('p', 'À Paris, les tarifs publiés sont rares et très variables selon la formule. Voici tout ce que nous avons trouvé :', 'In Paris, published rates are rare and vary widely by format. This is everything we found:')
        + ul([('<strong>Bachata Paris Unighted :</strong> 18 € le cours, 80 € les 5, 168 € les 12, 395 € l’année (33 cours).', '<strong>Bachata Paris Unighted:</strong> €18 a class, €80 for 5, €168 for 12, €395 for the year (33 classes).'),
              ('<strong>Paris Bachatero :</strong> cours particuliers de 55 à 80 € l’heure ; cours découverte sans prix.', '<strong>Paris Bachatero:</strong> private lessons from €55 to €80 an hour; discovery class with no price.'),
              ('<strong>Bachatamore :</strong> essai réservable en ligne ; pas de tarif sur la page principale.', '<strong>Bachatamore:</strong> trial bookable online; no rate on the main page.')])
        + t('p', 'Pour comparer, ramenez tout au prix par cours : chez Bachata Paris Unighted, la carte de 12 cours revient à 14 € le cours (168 ÷ 12) et l’année à environ 12 € (395 ÷ 33), contre 18 € le cours à l’unité.',
                 'To compare, bring everything down to the price per class: at Bachata Paris Unighted the 12-class card works out at €14 a class (168 ÷ 12) and the year at about €12 (395 ÷ 33), against €18 for a single class.'))
    body += BF.sec(t, 4, ('Quel niveau choisir ?', 'Which level should you pick?'),
        t('p', 'Si vous n’avez jamais dansé, choisissez un cours débutant, même si vous avez déjà pratiqué un autre style : chez Bachata Paris Unighted, c’est le cours débutant du jeudi à 19h00 ; Bachatamore et Paris Bachatero accueillent aussi les débutants complets. Le pas de base de la bachata est expliqué sur <a href="/bachata-grundschritt">Bachata Grundschritt</a> (en allemand) et un guide pour débutants se trouve sur <a href="/bachata-fuer-anfaenger">Bachata für Anfänger</a>.',
               'If you have never danced, pick a beginner class even if you have practised another style: at Bachata Paris Unighted that is the Thursday 19:00 beginner class; Bachatamore and Paris Bachatero also welcome complete beginners. The basic Bachata step is explained at <a href="/bachata-grundschritt">Bachata basic step</a> (in German) and a beginner guide is at <a href="/bachata-fuer-anfaenger">Bachata for beginners</a>.'), alt=False)
    body += BF.sec(t, 5, ('Quoi demander avant de vous inscrire', 'What to ask before you sign up'),
        ul([('<strong>Quel prix par cours ?</strong> Comparez l’unité, la carte et l’année ; vérifiez la durée de validité de la carte.', '<strong>What price per class?</strong> Compare single, card and year; check the card’s validity.'),
            ('<strong>L’essai est-il gratuit ou déduit ?</strong> Un site peut dire les deux ; demandez la condition exacte.', '<strong>Is the trial free or credited?</strong> A site can say both; ask for the exact condition.'),
            ('<strong>Quel style ?</strong> Bachatamore met l’accent sur la sensuelle ; Paris Bachatero liste six styles.', '<strong>Which style?</strong> Bachatamore focuses on sensual; Paris Bachatero lists six styles.'),
            ('<strong>Où et quand ?</strong> Paris est grand : vérifiez l’arrondissement et le jour avant de payer.', '<strong>Where and when?</strong> Paris is big: check the arrondissement and the day before paying.')]))
    body += BF.sec(t, 6, ('Comment nous avons préparé ce guide', 'How we prepared this guide'),
        t('p', f'En novembre 2026, nous avons lu les sites de Bachata Paris Unighted Académie, Bachatamore et Paris Bachatero, et nous utilisons les notes Google d’octobre 2026 de notre liste. Le site de Paris Bachata School n’a pas pu être lu automatiquement ; Salsa con Elegua et SalsaNueva (Paris) sont décrites dans notre <a href="/fr/cours-de-bachata">guide national</a>. Les autres écoles de Paris sont liées sur la <a href="/fr/bachata-paris">page de la ville</a>. Le classement est indépendant : les places ne s’achètent pas.',
               f'In November 2026 we read the websites of Bachata Paris Unighted Académie, Bachatamore and Paris Bachatero, and we use the October 2026 Google ratings from our list. The Paris Bachata School website could not be read automatically; Salsa con Elegua and SalsaNueva (Paris) are described in our <a href="/fr/cours-de-bachata">national guide</a>. The other Paris schools are linked on the <a href="/fr/bachata-paris">city page</a>. The ranking is independent: places cannot be bought.'))
    faq = [
        ('Où apprendre la bachata à Paris ?', 'Where can I learn Bachata in Paris?',
         f'Notre liste compte {n} écoles et lieux avec de la bachata à Paris, dont Bachata Paris Unighted Académie, Bachatamore, Paris Bachatero, SalsaNueva et Salsa con Elegua. La liste complète est sur notre page Bachata Paris.',
         f'Our list has {n} schools and venues with Bachata in Paris, including Bachata Paris Unighted Académie, Bachatamore, Paris Bachatero, SalsaNueva and Salsa con Elegua. The full list is on our Bachata Paris page.'),
        ('Combien coûte un cours de bachata à Paris ?', 'How much does a Bachata class in Paris cost?',
         'Chez Bachata Paris Unighted : 18 € le cours, 80 € la carte de 5, 168 € la carte de 12 et 395 € l’année (33 cours). Paris Bachatero publie des cours particuliers de 55 à 80 € l’heure. D’autres écoles ne publient pas de tarif sur la page principale.',
         'At Bachata Paris Unighted: €18 a class, €80 for a 5-class card, €168 for a 12-class card and €395 for the year (33 classes). Paris Bachatero publishes private lessons from €55 to €80 an hour. Other schools do not publish a rate on the main page.'),
        ('Y a-t-il un cours d’essai gratuit ?', 'Is there a free trial class?',
         'Cela dépend. Bachatamore permet de réserver un essai en ligne ; Paris Bachatero propose un « 1er cours découverte » sans engagement ; Bachata Paris Unighted indique un essai à −50 % déduit d’un forfait et, dans son calendrier, un essai gratuit aux portes ouvertes. Confirmez avant de réserver.',
         'It depends. Bachatamore lets you book a trial online; Paris Bachatero offers a “1st discovery class” with no commitment; Bachata Paris Unighted mentions a trial at −50% credited against a package and, in its calendar, a free trial at the open house. Confirm before booking.'),
        ('Faut-il un partenaire ?', 'Do I need a partner?',
         'Non, en général. Bachata Paris Unighted dit qu’on peut venir seul, Bachatamore « seul ou accompagné » et Paris Bachatero accepte aussi les personnes seules.',
         'Usually not. Bachata Paris Unighted says you can come alone, Bachatamore “alone or accompanied” and Paris Bachatero also accepts people on their own.'),
        ('Quelle est la meilleure école de bachata de Paris ?', 'What is the best Bachata school in Paris?',
         f'Selon nos données provisoires d’octobre 2026, parmi les meilleures notes Google figurent {top_fr}. Ce n’est pas le classement final, publié au printemps 2027.',
         f'By our interim data from October 2026, the best Google ratings include {top_en}. This is not the final ranking, which follows in spring 2027.'),
    ]
    body += BF.faq_html(t, faq)
    BF.fr_page('fr/cours-de-bachata-paris.html', 'fr/cours-de-bachata-paris.html',
        'Cours de bachata Paris : écoles, niveaux et tarifs',
        'Cours de bachata à Paris : tarifs de Bachata Paris Unighted, essai chez Bachatamore, cours particuliers de Paris Bachatero, niveaux et quoi demander avant de vous inscrire.',
        'Bachata classes Paris: schools, levels and prices',
        'Bachata classes in Paris: Bachata Paris Unighted rates, trials at Bachatamore, private lessons from Paris Bachatero, levels and what to ask before you sign up.',
        h + body, t.en, [crumbs('Bachata Paris', 'fr/bachata-paris.html'), crumbs('Cours de bachata Paris', 'fr/cours-de-bachata-paris.html'), faq_schema(faq)])

madrid(); barcelona(); london(); paris()
