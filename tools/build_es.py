# Builds the Spain section (/es/) in Spanish + English. Same structure and the same 100-point scoring as build_pl.py.
# Run after build.py/build_guides.py:  python3 tools/build_es.py
import os, sys, re, io, json, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import spain_data as P
import rank_variant as RV
BASE = '/es/escuelas/'
FULL = {e['name']: RV.total(e) for es in RV.polish_entries(P, BASE).values() for e in es}
from build import T, page, crumbs, faq_schema, ICON, ROOT
os.makedirs(os.path.join(ROOT, 'es'), exist_ok=True)

def f1(x): return f'{x:.1f}'.replace('.', ',')
def f1en(x): return f'{x:.1f}'
ranked = sorted(P.SCHOOLS, key=lambda s: (-FULL[s[0]], s[0]))
_TOP = [FULL[ranked[0][0]]]
def by_city(k): return [s for s in ranked if s[1] == k]

# ---------- Spanish header / footer ----------
_ESH = B.HEADER
_ESH = _ESH.replace('<a class="brand" href="index.html"', '<a class="brand" href="/"', 1)
_ESH = re.sub(r'<ul id="mnav">.*?</ul>', '''<ul id="mnav">
        <li><a href="es/#ranking" data-i18n="sn1">Ranking</a></li>
        <li><a href="es/#ciudades" data-i18n="sn2">Ciudades</a></li>
        <li><a href="es/#metodo" data-i18n="sn3">Método</a></li>
        <li><a href="index.html" data-i18n="sn4">Europa</a></li>
        <li><a href="deutschland.html" data-i18n="sn5">Alemania</a></li>
      </ul>''', _ESH, count=1, flags=re.S)
_ESH = _ESH.replace('data-lang="de" aria-pressed="true">DE<', 'data-lang="de" aria-pressed="true">ES<')
_ESH = re.sub(r'<a class="btn btn-gold" href="bewerbung.html" data-i18n="t5">.*?</a>', '<a class="btn btn-gold" href="bewerbung.html?lang=en" data-i18n="sn6">Inscribir escuela</a>', _ESH, count=1)
_brand = re.search(r'<a class="brand" href="index.html">.*?</a>', B.FOOTER, re.S).group(0).replace('href="index.html"', 'href="/"', 1)
_ESF = f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        {_brand}
        <p class="indep" data-i18n="sf1">Proyecto independiente que celebra las escuelas europeas de baile latino. Los rankings se basan en datos públicos y no se pueden comprar.</p>
      </div>
      <div>
        <p class="fh" data-i18n="sf2">Rankings</p>
        <ul><li><a href="es/#ranking" data-i18n="sf3">España 2027</a></li><li><a href="es/#metodo" data-i18n="sf4">Cómo puntuamos</a></li>{''.join(f'<li><a href="es/bachata-{k}.html">Bachata {v[0]}</a></li>' for k, v in list(P.CITIES.items())[:4])}<li><a href="index.html" data-i18n="sn4">Europa</a></li></ul>
      </div>
      <div>
        <p class="fh" data-i18n="sf5">Contacto</p>
        <ul><li><a href="bewerbung.html?lang=en" data-i18n="sn6">Inscribir escuela</a></li><li><a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a></li><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li></ul>
      </div>
    </div>
    <div class="legal"><span>© 2026 Latin Dance Awards</span><span data-i18n="sf6">Edición Bachata · España</span></div>
  </div>
</footer>'''

SHARED_ES_EN = {'sn1': 'Ranking', 'sn2': 'Cities', 'sn3': 'Method', 'sn4': 'Europe', 'sn5': 'Germany', 'sn6': 'Enter a school', 'sn7': 'Poland',
  'sf1': "An independent project celebrating Europe's Latin dance schools. Rankings are based on public data and can't be bought.",
  'sf2': 'Rankings', 'sf3': 'Spain 2027', 'sf4': 'How we score', 'sf5': 'Contact', 'sf6': 'Bachata Edition · Spain'}

def es_page(fname, canon, title, desc, title_en, desc_en, main, en, schema, js=''):
    oh, of = B.HEADER, B.FOOTER
    B.HEADER, B.FOOTER = _ESH, _ESF
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            B.SHARED_EN = dict(B.SHARED_EN); B.SHARED_EN.update(SHARED_ES_EN)
            page(fname, title, desc, title_en, desc_en, canon, main, en, js, schema=schema)
    finally:
        B.HEADER, B.FOOTER = oh, of
    fp = os.path.join(ROOT, fname); h = open(fp, encoding='utf-8').read()
    h = h.replace('<html lang="de">', '<html lang="es">', 1).replace('hreflang="de"', 'hreflang="es"').replace('document.documentElement.lang=l;', 'document.documentElement.lang=(l==="en"?"en":"es");')
    h = h.replace('og:locale" content="de_DE"', 'og:locale" content="es_ES"')
    open(fp, 'w', encoding='utf-8').write(h)
    print('wrote', fname)

def school_list(ss, t, start=1):
    lis = []
    for i, s in enumerate(ss, start):
        lis.append(f'<li><b>{i}</b><a href="{s[4]}" rel="nofollow noopener" target="_blank">{s[0]}</a><span>{f1(FULL[s[0]])} pts · {f1(s[2])} ★ ({s[3]})</span></li>')
    return '<ol class="top">' + ''.join(lis) + '</ol>'

def hero(t, edition, h1, lede, facts, ctas, seal='badge-bachata-spain-2027.svg', alt='Sello Bachata Awards España 2027'):
    return f'''<section class="page-hero"><div class="wrap">
  <div>
    <span class="edition rise d1"><i></i>{t("span", *edition)}</span>
    <h1 class="rise d2">{t("span", *h1)}</h1>
    <p class="lede rise d3">{t("span", *lede)}</p>
    <div class="facts rise d4">{''.join(f'<span>{ICON[ic]}{t("span", d, e)}</span>' for ic, d, e in facts)}</div>
    <div class="ctas rise d5">{ctas}</div>
  </div>
  <div class="seal-box rise d3"><img class="seal" src="/{seal}" alt="{alt}" width="360" height="360" fetchpriority="low"></div>
</div></section>'''

def sec(t, i, h2, blocks, alt=True):
    return f'<section class="block{" alt" if alt else ""}"><div class="wrap prose">{t("h2", *h2)}{blocks}</div></section>'

def faq_html(t, faq):
    return '<section class="block alt" id="faq"><div class="wrap"><div class="sec-head">' + t("h2", 'Preguntas frecuentes', 'Frequently asked questions') + '</div><div class="faq">' + ''.join(f'<details>{t("summary", q, qe)}{t("p", a, ae)}</details>' for q, qe, a, ae in faq) + '</div></div></section>'

N = len(P.SCHOOLS); NC = len(P.CITIES)
METHOD_ES = ('Puntuamos las escuelas igual que en Alemania, con nueve criterios y 100 puntos: años de actividad, oferta para principiantes, eventos, valoración en Google, número de reseñas y redes sociales (75 puntos en total), más festivales, reseñas recientes y concursos (25 puntos, de momento «por confirmar»). Los datos proceden de las webs de las escuelas, de Google Maps y de Instagram. Lo que no se puede confirmar cuenta con el valor más bajo, y la escuela puede completarlo al inscribirse.',
             'We score schools exactly as in Germany, on nine factors and 100 points: years active, beginner offer, events, Google rating, number of reviews and social media (75 points together), plus festivals, recent reviews and competitions (25 points, still “to be confirmed”). The data comes from the schools’ websites, Google Maps and Instagram. Anything we cannot confirm counts at the lowest level, and a school can complete it in its application.')

# ---------- /es/ index ----------
t = T('es')
city_cards = ''.join(
    f'<article><h3>{t("span", "Bachata " + v[0], "Bachata " + v[1])}</h3>{t("p", f"{len(by_city(k))} escuelas, a la cabeza: {by_city(k)[0][0]}.", f"{len(by_city(k))} schools, led by {by_city(k)[0][0]}.")}<a href="/es/bachata-{k}.html">{t("span", "Escuelas de la ciudad →", "Schools in this city →")}</a></article>'
    for k, v in P.CITIES.items())
main = hero(t, ('Edición Bachata · España 2027', 'Bachata Edition · Spain 2027'),
  ('Las mejores escuelas de bachata de España: ranking 2027', 'The best Bachata schools in Spain: ranking 2027'),
  (f'Ranking independiente de escuelas de bachata en {NC} ciudades de España, basado en datos públicos. Publicaremos los resultados en primavera de 2027.', f'An independent ranking of Bachata schools in {NC} Spanish cities, based on public data. Results will be published in spring 2027.'),
  [('cal', f'<b>{N} escuelas</b> en {NC} ciudades', f'<b>{N} schools</b> in {NC} cities'), ('check', 'Independiente, <b>no se compra</b>', 'Independent, <b>not for sale</b>'), ('clock', 'Resultados en <b>primavera de 2027</b>', 'Results <b>spring 2027</b>')],
  f'<a class="btn btn-gold" href="#ranking">{t("span", "Ver la clasificación actual", "See the current standings")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Inscribe tu escuela", "Enter your school")}</a>')
ES_C = RV.polish_entries(P, BASE)
TX = {k: list(v) if isinstance(v, list) else v for k, v in B.R_TEXT.items()}
TX['cities'] = {'espana': ['Toda España', 'All Spain']}
TX['cities'].update({k: [v[0], v[1]] for k, v in P.CITIES.items()})
def _tx(k, es, en): TX[k] = [es, en]
_tx('title_city', 'Las mejores escuelas de bachata: {c}', 'Best Bachata schools in {c}')
_tx('title_de', 'Las mejores escuelas de bachata de España', 'Best Bachata schools in Spain')
_tx('sub_interim', 'Clasificación provisional: los puestos pueden cambiar hasta que publiquemos los resultados en primavera de 2027.', 'Interim standing: places can still change until the results are published in spring 2027.')
_tx('help_h', '¿Cómo funciona el ranking?', 'How does the ranking work?')
_tx('help_p', 'Cada escuela se puntúa con los mismos criterios públicos, igual en todos los países. Los puestos no se pueden comprar.', 'Every school is scored on the same public criteria, identical in every country. Places cannot be bought.')
_tx('help_how', 'Cómo puntuamos', 'How scoring works')
_tx('help_add', 'Añadir mi escuela', 'Add my school')
_tx('help_tips_h', 'Cómo mejorar el puesto de tu escuela', "How to improve your school's place")
TX['help_tips'] = [[
  'Cuida tu ficha de Google y pide a tus alumnos que dejen una reseña (valoración en Google 25 pts, número de reseñas 10 pts, reseñas recientes 5 pts)',
  'Indica en tu web el año de fundación, el equipo de profesores y los niveles de los cursos (años de actividad 10 pts)',
  'Ofrece una clase de prueba y grupos fijos para principiantes (oferta para principiantes 10 pts)',
  'Organiza fiestas y talleres, invita a profesores y muéstralo en internet (eventos 10 pts)',
  'Mantén tu Instagram al día (redes sociales 10 pts)',
  'Confirma con un enlace tus festivales y concursos (festivales 15 pts, concursos 5 pts)'], B.R_TEXT['help_tips'][1]]
_tx('pts', 'puntos', 'points'); _tx('site', 'Web', 'Website'); _tx('insta', 'Instagram', 'Instagram')
_tx('note_h', '¿Falta tu escuela?', 'Is your school missing?')
_tx('note_p', 'Inscribe tu escuela gratis en el ranking 2027.', 'Enter your school for the 2027 ranking for free.')
_tx('note_btn', 'Inscribir gratis', 'Apply for free')
_tx('page_link', 'Página de la escuela, reseñas y votación', 'School page, reviews and voting')
_tx('vote_h', 'Premio del público', 'Audience Award')
_tx('vote_banner', 'Premio del público: abre una escuela y vota. Un voto por persona, confirmado por correo. Es independiente de los puntos y el resultado se publicará junto con el ranking.', 'Audience Award: open a school and vote. One vote per person, confirmed by email. It is separate from the points, and the result comes with the ranking.')
_tx('vote_btn', 'Votar por esta escuela', 'Vote for this school')
_tx('vote_mail', 'Tu correo electrónico', 'Your email address')
_tx('vote_send', 'Enviar mi voto', 'Send my vote')
_tx('news_opt', 'Sí, quiero recibir de vez en cuando noticias, eventos y ofertas sobre bachata por correo. Puedes darte de baja cuando quieras.', B.R_TEXT['news_opt'][1])
_tx('vote_note', 'Un voto por persona. Te enviaremos un enlace de confirmación. Usamos tu correo solo para eso y para eliminar votos duplicados.', B.R_TEXT['vote_note'][1])
_tx('vote_ok', 'Casi listo: te hemos enviado un correo. Haz clic en el enlace para que tu voto cuente. Mira también en la carpeta de spam.', B.R_TEXT['vote_ok'][1])
_tx('vote_err', 'No ha funcionado. Revisa tu correo electrónico e inténtalo de nuevo.', B.R_TEXT['vote_err'][1])
_tx('vote_done', 'Ya se ha votado desde este dispositivo. ¡Gracias!', B.R_TEXT['vote_done'][1])
_tx('prelim_badge', 'Clasificación provisional · no es el resultado final, las escuelas siguen compitiendo', 'Interim standing · not final, schools are still competing')
_tx('prelim_h', 'Cómo se calcula la clasificación provisional', 'How the interim standing is calculated')
_tx('prelim_p', 'Calculamos los puntos igual que en Alemania: hasta 75 puntos por seis criterios (años de actividad, oferta para principiantes, eventos, valoración en Google, número de reseñas, redes sociales) y hasta 25 puntos por festivales, reseñas recientes y concursos, que aún están «por confirmar». Datos: webs de las escuelas, Google Maps e Instagram, a octubre de 2026. Lo que no se ha confirmado cuenta con el valor más bajo. Los puestos todavía pueden cambiar.', 'Points are calculated exactly as in Germany: up to 75 points for six factors (years active, beginner offer, events, Google rating, number of reviews, social media) and up to 25 points for festivals, recent reviews and competitions, which are still “to be confirmed”. Data: school websites, Google Maps and Instagram, status October 2026. Anything unconfirmed counts at the lowest level. Positions can still change.')
_tx('empty', 'Todavía no hay resultados para esta ciudad.', 'There are no results for this city yet.')
_ES_TBC = ['Festivales', 'Reseñas recientes', 'Participación en concursos', 'Concursos ganados']
_EN_TBC = ['Festivals', 'Recent reviews', 'Competitions entered', 'Competitions won']
_MX = ['15', '5', '5', '5']
_QUICK = ['espana', 'madrid', 'barcelona', 'valencia', 'sevilla', 'malaga', 'zaragoza']
es_js = RV.make_js('espana', {}, TX, ES_C, _QUICK, 100, pl=True, code='ES', extra={
  'tbc': ([[n, m] for n, m in zip(_ES_TBC, _MX)], [[n, m] for n, m in zip(_EN_TBC, _MX)]),
  'literals': {
    '"Follower · Posts: "': '"Seguidores · publicaciones: "',
    '"Zu bestätigen"': '"Por confirmar"',
    '"Noch ohne Punkte. Schulen bestätigen diese Angaben mit Links bei der Bewerbung."': '"Aún sin puntos. Las escuelas confirman estos datos con enlaces al inscribirse."',
    '"Jetzt bestätigen"': '"Confirmar ahora"',
    '"Keine Stadt gefunden"': '"No se ha encontrado ninguna ciudad"',
    '["Jahre im Unterricht","Einsteigerangebot","Events und Gastlehrer","Google-Bewertung","Anzahl Bewertungen","Social Media"]': '["Años de enseñanza","Oferta para principiantes","Eventos e invitados","Valoración en Google","Número de reseñas","Redes sociales"]',
    '"Alle "+pl.length+" Schulen anzeigen"': '"Ver las "+pl.length+" escuelas"',
  }})
_tabs = RV.tabs_html(t, [(k, TX['cities'][k][0], TX['cities'][k][1]) for k in _QUICK])
RANK_SECTION = RV.ranking_section(_tabs, 'Buscar ciudad …', 'Search city …', 'Ciudades / Cities')
main += RANK_SECTION
main += f'''
{sec(t, 1, ("Bachata en las ciudades españolas", "Bachata in Spanish cities"), '<div class="cards two" id="ciudades">' + city_cards + '</div>', alt=False).replace('<section class="block"', '<section class="block" id="ciudades-sec"')}
{sec(t, 2, ("Cómo puntuamos las escuelas de bachata", "How we score Bachata schools"), t("p", *METHOD_ES) + t("p", 'El ranking se basa solo en datos públicos. Los puestos no se pueden comprar, y las menciones de pago, si las hubiera, se marcarán como publicidad y no influyen en los puntos. Recogemos los datos de las escuelas nosotros mismos a partir de Google Maps y de sus webs, por lo que pueden contener errores: <a href="/bewerbung.html?lang=en">inscribe una escuela o envíanos una corrección</a>.', 'The ranking is based only on public data. Places cannot be bought, and paid mentions, if any, will be labelled as ads and do not affect points. We collect the school data ourselves from Google Maps and the schools\' websites, so it may contain errors: <a href="/bewerbung.html?lang=en">enter a school or send a correction</a>.'), alt=True).replace('<section class="block alt"', '<section class="block alt" id="metodo"')}
{sec(t, 3, ("Ranking de Europa y rankings por país", "Europe ranking and country rankings"), t("p", 'Latin Dance Awards crea un ranking de escuelas de toda Europa y un ranking aparte para cada país. España se suma a Alemania y Polonia. Mira el <a href="/">resumen de Europa</a>, el <a href="/deutschland.html">ranking de Alemania</a> o el <a href="/pl/">ranking de Polonia</a>.', 'Latin Dance Awards builds one ranking of schools across Europe plus a separate ranking for each country. Spain joins Germany and Poland. See the <a href="/">Europe overview</a>, the <a href="/deutschland.html">Germany ranking</a> or the <a href="/pl/">Poland ranking</a>.'), alt=False)}
'''
faq = [
 ('¿Cuál es la mejor escuela de bachata de España?', 'What is the best Bachata school in Spain?',
  f'A día de hoy, según nuestros datos, lidera {ranked[0][0]} ({P.CITIES[ranked[0][1]][0]}) con {f1(_TOP[0])} de 100 puntos. Es una clasificación provisional; los resultados finales se publicarán en primavera de 2027.',
  f'As of today, by our data, {ranked[0][0]} ({P.CITIES[ranked[0][1]][1]}) leads with {f1en(_TOP[0])} of 100 points. This is an interim standing; final results come in spring 2027.'),
 ('¿De dónde salen los datos del ranking?', 'Where does the ranking data come from?',
  'De fuentes públicas: la valoración y el número de reseñas en Google Maps y las webs de las propias escuelas, donde comprobamos que se enseña bachata.', 'From public sources: ratings and review counts on Google Maps and the schools\' own websites, where we check that the school teaches Bachata.'),
 ('¿Puedo comprar un puesto en el ranking?', 'Can I buy a place in the ranking?', 'No. Los puestos no se pueden comprar y las menciones de pago no influyen en los puntos.', 'No. Places cannot be bought, and paid mentions do not affect points.'),
 ('¿Cómo inscribo mi escuela?', 'How do I enter my school?', 'Usa el <a href="/bewerbung.html?lang=en">formulario de inscripción gratuito</a> (en inglés). Al inscribirte puedes confirmar tus datos y obtener la puntuación completa.', 'Use the <a href="/bewerbung.html?lang=en">free application form</a> (in English). Applying lets you confirm your details and receive the full score.'),
 ('¿Qué ciudades cubre el ranking?', 'Which cities does the ranking cover?', f'Para empezar: {", ".join(v[0] for v in P.CITIES.values())}. Añadiremos más ciudades a medida que se inscriban escuelas.', f'To start with: {", ".join(v[1] for v in P.CITIES.values())}. We will add more cities as schools apply.'),
]
main += faq_html(t, faq)
es_page('es/index.html', 'es/', 'Las mejores escuelas de bachata de España: ranking 2027',
  f'Ranking de escuelas de bachata en España: {N} escuelas en {NC} ciudades, con valoraciones, puntos y método. Resultados en primavera de 2027. Independiente y no se compra.',
  'The best Bachata schools in Spain: 2027 ranking', f'Ranking of Bachata schools in Spain: {N} schools in {NC} cities with ratings, points and method. Results in spring 2027. Independent and not for sale.',
  main, t.en, [crumbs('España', 'es/'), faq_schema(faq)], js=es_js)

# ---------- city pages ----------
for k, (cpl, cen, loc) in P.CITIES.items():
    ss = by_city(k); n = len(ss); t = T('ec' + k[:2])
    ranks = {s[0]: ranked.index(s) + 1 for s in ss}
    cards = ''.join(f'<article><h3>{s[0]}</h3>{t("p", f"Valoración en Google: {f1(s[2])} ★ ({s[3]} reseñas). Puesto {ranks[s[0]]} en España.", f"Google rating: {f1en(s[2])} ★ ({s[3]} reviews). Rank {ranks[s[0]]} in Spain.")}<a href="{s[4]}" rel="nofollow noopener" target="_blank">{t("span", "Web de la escuela", "School website")} →</a></article>' for s in ss)
    main = hero(t, (f'Bachata {cpl} · 2027', f'Bachata {cen} · 2027'),
      (f'Bachata {cpl}: las mejores escuelas de baile 2027', f'Bachata {cen}: the best dance schools 2027'),
      (f'Escuelas de bachata en {loc}: {n} lugares con clases confirmadas, con valoraciones de Google y puntos de la clasificación provisional. Resultados en primavera de 2027.', f'Bachata schools in {cen}: {n} places with confirmed classes, with Google ratings and interim ranking points. Results in spring 2027.'),
      [('cal', f'<b>{n} escuelas</b> en {loc}', f'<b>{n} schools</b> in {cen}'), ('check', 'Datos de <b>octubre de 2026</b>', 'Data from <b>October 2026</b>')],
      f'<a class="btn btn-gold" href="#ranking">{t("span", "Ver el ranking", "See the ranking")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Inscribe tu escuela", "Enter your school")}</a>')
    main += f'''
<section class="block alt" id="ranking"><div class="wrap tp" style="max-width:860px">
  {t("h2", f"Ranking de escuelas de bachata en {loc}", f"Ranking of Bachata schools in {cen}")}
  {t("p", f"Clasificación provisional según las valoraciones de Google de octubre de 2026 (máx. 100 puntos). Los resultados finales se publicarán en primavera de 2027.", "Interim standing by Google ratings as of October 2026 (max 100 points). The final results are published in spring 2027.", 'class="muted"')}
  <div class="box">{school_list(ss, t)}</div>
</div></section>
{sec(t, 1, (f"Escuelas de bachata en {loc} de un vistazo", f"Bachata schools in {cen} at a glance"), t("p", f"En {loc} hemos encontrado {n} escuelas donde se enseña bachata. El orden se basa en puntos provisionales, no en una evaluación completa. Los horarios, precios y grupos cambian, así que consúltalos en la web de la escuela.", f"In {cen} we found {n} schools that teach Bachata. The order is based on interim points, not a full assessment. Times, prices and groups change, so check them on the school's website.") + '<div class="cards two">' + cards + '</div>', alt=False)}
{sec(t, 2, (f"Cómo elegir un curso de bachata en {loc}", f"How to choose a Bachata class in {cen}"), t("p", "Un buen curso de bachata se adapta a tu nivel, a tu horario y a tu trayecto. Estos consejos te ayudarán:", "A good Bachata class fits your level, schedule and journey. These tips help:") + '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in [
   ('<strong>Nivel:</strong> empieza en un grupo de principiantes, aunque ya hayas bailado. El paso básico es la base de todo.', '<strong>Level:</strong> start with a beginner group, even if you have danced before. The basic step is the base for everything.'),
   ('<strong>Clase de prueba:</strong> pregunta por una clase de prueba o por el inicio de un grupo nuevo antes de comprar un bono.', '<strong>Trial class:</strong> ask for a trial class or a new group start before buying a pass.'),
   ('<strong>Pareja:</strong> normalmente no hace falta ir con pareja. Pregunta si se rotan los compañeros.', '<strong>Partner:</strong> you usually do not need to bring a partner. Ask whether partners rotate.'),
   ('<strong>Estilo:</strong> la bachata dominicana, la moderna y la sensual tienen un carácter distinto. Mira qué estilo enseña la escuela.', '<strong>Style:</strong> Dominicana, moderna and sensual bachata differ in character. Check which style the school teaches.')]) + '</ul>', alt=True)}
{sec(t, 3, ("Rankings de España, Europa y Alemania", "Spain, Europe and Germany rankings"), t("p", 'Mira el <a href="/es/">ranking de toda España</a>, el <a href="/">resumen de Europa</a> o el <a href="/deutschland.html">ranking de Alemania</a>. ¿Diriges una escuela en ' + loc + '? <a href="/bewerbung.html?lang=en">Inscríbela gratis</a>.', f'See the <a href="/es/">Spain ranking</a>, the <a href="/">Europe overview</a> or the <a href="/rankings.html">Germany ranking</a>. Do you run a school in {cen}? <a href="/bewerbung.html?lang=en">Enter it for free</a>.'), alt=False)}
'''
    top = ss[0]
    faq = [
     (f'¿Dónde puedo aprender bachata en {loc}?', f'Where can I learn Bachata in {cen}?', f'En {loc} se enseña bachata en {", ".join(s[0] for s in ss[:3])} y otras escuelas. Tienes la lista completa más arriba.', f'In {cen} Bachata is taught by {", ".join(s[0] for s in ss[:3])} and others. The full list is above.'),
     (f'¿Cuál es la mejor escuela de bachata en {loc}?', f'What is the best Bachata school in {cen}?', f'A día de hoy, según nuestros datos, lidera {top[0]} ({f1(top[2])} ★, {top[3]} reseñas). Es una clasificación provisional, no el ranking final.', f'As of today, by Google ratings, {top[0]} leads ({f1en(top[2])} ★, {top[3]} reviews). This is an interim standing, not the final ranking.'),
     ('¿Necesito pareja para un curso de bachata?', 'Do I need a partner for a Bachata class?', 'Normalmente no. En muchas escuelas se rotan las parejas. Pregúntalo antes de la primera clase.', 'Usually not. Many schools rotate partners. Ask before your first class.'),
     ('¿Con qué estilo de bachata debo empezar?', 'Which Bachata style should I start with?', 'La mayoría de los principiantes empieza con bachata moderna o sensual. Lo importante es el paso básico y el ritmo; el estilo se puede cambiar más adelante.', 'Most beginners start with moderna or sensual. What matters is the basic step and the rhythm, and you can change style later.'),
     ('¿Cuándo se publica el ranking completo?', 'When is the full ranking published?', 'En primavera de 2027. Hasta entonces mostramos una clasificación provisional basada en las valoraciones de Google.', 'In spring 2027. Until then we show an interim standing based on Google ratings.'),
    ]
    main += faq_html(t, faq)
    es_page(f'es/bachata-{k}.html', f'es/bachata-{k}.html', f'Bachata {cpl}: las mejores escuelas de baile 2027',
      f'Bachata {cpl}: {n} escuelas con valoraciones de Google y puntos del ranking 2027. Elige un curso de bachata en {loc} y consulta la clasificación provisional.',
      f'Bachata {cen}: the best dance schools 2027', f'Bachata {cen}: {n} schools with Google ratings and 2027 ranking points. Choose a Bachata class in {cen} and see the interim ranking.',
      main, t.en, [crumbs(f'Bachata {cpl}', f'es/bachata-{k}.html'), faq_schema(faq)])
