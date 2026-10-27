# Builds the Netherlands section (/nl/) in Dutch + English. Same structure and the same 100-point scoring as build_pl.py.
# Run after build.py/build_guides.py:  python3 tools/build_nl.py
import os, sys, re, io, json, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import netherlands_data as P
import rank_variant as RV
BASE = '/nl/scholen/'
FULL = {e['name']: RV.total(e) for es in RV.polish_entries(P, BASE).values() for e in es}
from build import T, page, crumbs, faq_schema, ICON, ROOT
os.makedirs(os.path.join(ROOT, 'nl'), exist_ok=True)

def f1(x): return f'{x:.1f}'.replace('.', ',')
def f1en(x): return f'{x:.1f}'
ranked = sorted(P.SCHOOLS, key=lambda s: (-FULL[s[0]], s[0]))
_TOP = [FULL[ranked[0][0]]]
def by_city(k): return [s for s in ranked if s[1] == k]

# ---------- Portuguese header / footer ----------
_NLH = B.HEADER
_NLH = _NLH.replace('<a class="brand" href="index.html"', '<a class="brand" href="/"', 1)
_NLH = re.sub(r'<ul id="mnav">.*?</ul>', '''<ul id="mnav">
        <li><a href="nl/#ranking" data-i18n="sn1">Ranglijst</a></li>
        <li><a href="nl/#steden" data-i18n="sn2">Steden</a></li>
        <li><a href="nl/#metodo" data-i18n="sn3">Methode</a></li>
        <li><a href="index.html" data-i18n="sn4">Europa</a></li>
        <li><a href="deutschland.html" data-i18n="sn5">Duitsland</a></li>
        <li><a href="pl/" data-i18n="sn7">Polen</a></li>
        <li><a href="es/" data-i18n="sn8">Spanje</a></li>
        <li><a href="it/" data-i18n="sn9">Italië</a></li>
        <li><a href="pt/" data-i18n="sn10">Portugal</a></li>
        <li><a href="fr/" data-i18n="sn11">Frankrijk</a></li>
        <li><a href="uk/">UK</a></li>
        <li><a href="be/">Belgium</a></li>
        <li><a href="ie/">Ireland</a></li>
        <li><a href="at/">Austria</a></li>
        <li><a href="ch/">Switzerland</a></li>
        <li><a href="ee/">Eastern Europe</a></li>
        <li><a href="nd/">Nordics</a></li>
        <li><a href="em/">Eastern Mediterranean</a></li>
      </ul>''', _NLH, count=1, flags=re.S)
_NLH = _NLH.replace('data-lang="de" aria-pressed="true">DE<', 'data-lang="de" aria-pressed="true">NL<')
_NLH = re.sub(r'<a class="btn btn-gold" href="bewerbung.html" data-i18n="t5">.*?</a>', '<a class="btn btn-gold" href="bewerbung.html?lang=en" data-i18n="sn6">School aanmelden</a>', _NLH, count=1)
_brand = re.search(r'<a class="brand" href="index.html">.*?</a>', B.FOOTER, re.S).group(0).replace('href="index.html"', 'href="/"', 1)
_NLF = f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        {_brand}
        <p class="indep" data-i18n="sf1">Onafhankelijk project dat Europese Latin-dansscholen in beeld brengt. De ranglijsten zijn gebaseerd op openbare gegevens en zijn niet te koop.</p>
      </div>
      <div>
        <p class="fh" data-i18n="sf2">Rankings</p>
        <ul><li><a href="nl/#ranking" data-i18n="sf3">Nederland 2027</a></li><li><a href="nl/#metodo" data-i18n="sf4">Hoe we beoordelen</a></li>{''.join(f'<li><a href="nl/bachata-{k}.html">Bachata {v[0]}</a></li>' for k, v in list(P.CITIES.items())[:4])}<li><a href="index.html" data-i18n="sn4">Europa</a></li></ul>
      </div>
      <div>
        <p class="fh" data-i18n="sf5">Contact</p>
        <ul><li><a href="bewerbung.html?lang=en" data-i18n="sn6">School aanmelden</a></li><li><a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a></li><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li></ul>
      </div>
    </div>
    <div class="legal"><span>© 2026 Latin Dance Awards</span><span data-i18n="sf6">Bachata-editie · Nederland</span></div>
  </div>
</footer>'''

SHARED_ES_EN = {'sn1': 'Ranking', 'sn2': 'Cities', 'sn3': 'Method', 'sn4': 'Europe', 'sn5': 'Germany', 'sn6': 'Enter a school', 'sn7': 'Poland', 'sn8': 'Spain', 'sn9': 'Italy', 'sn10': 'Portugal', 'sn11': 'France',
  'sf1': "An independent project celebrating Europe's Latin dance schools. Rankings are based on public data and can't be bought.",
  'sf2': 'Rankings', 'sf3': 'Netherlands 2027', 'sf4': 'How we score', 'sf5': 'Contact', 'sf6': 'Bachata Edition · Netherlands'}

def nl_page(fname, canon, title, desc, title_en, desc_en, main, en, schema, js=''):
    oh, of = B.HEADER, B.FOOTER
    B.HEADER, B.FOOTER = _NLH, _NLF
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            B.SHARED_EN = dict(B.SHARED_EN); B.SHARED_EN.update(SHARED_ES_EN)
            page(fname, title, desc, title_en, desc_en, canon, main, en, js, schema=schema)
    finally:
        B.HEADER, B.FOOTER = oh, of
    fp = os.path.join(ROOT, fname); h = open(fp, encoding='utf-8').read()
    h = h.replace('<html lang="de">', '<html lang="nl">', 1).replace('hreflang="de"', 'hreflang="nl"').replace('document.documentElement.lang=l;', 'document.documentElement.lang=(l==="en"?"en":"nl");')
    h = h.replace('og:locale" content="de_DE"', 'og:locale" content="nl_NL"')
    open(fp, 'w', encoding='utf-8').write(h)
    print('wrote', fname)

def school_list(ss, t, start=1):
    lis = []
    for i, s in enumerate(ss, start):
        lis.append(f'<li><b>{i}</b><a href="{s[4]}" rel="nofollow noopener" target="_blank">{s[0]}</a><span>{f1(FULL[s[0]])} pt · {f1(s[2])} ★ ({s[3]})</span></li>')
    return '<ol class="top">' + ''.join(lis) + '</ol>'

def hero(t, edition, h1, lede, facts, ctas, seal='badge-bachata-netherlands-2027.svg', alt='Bachata Awards Nederland 2027 zegel'):
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
    return '<section class="block alt" id="faq"><div class="wrap"><div class="sec-head">' + t("h2", 'Veelgestelde vragen', 'Frequently asked questions') + '</div><div class="faq">' + ''.join(f'<details>{t("summary", q, qe)}{t("p", a, ae)}</details>' for q, qe, a, ae in faq) + '</div></div></section>'

N = len(P.SCHOOLS); NC = len(P.CITIES)
METHOD_ES = ('We beoordelen scholen zoals in Duitsland, op negen criteria en 100 punten: jaren actief, aanbod voor beginners, evenementen, Google-score, aantal reviews en social media (samen 75 punten), plus festivals, recente reviews en wedstrijden (25 punten, voorlopig "nog te bevestigen"). De gegevens komen van de websites van de scholen, Google Maps en Instagram. Wat niet bevestigd kan worden, telt met de laagste waarde, en de school kan het bij de aanmelding aanvullen.',
             'We score schools exactly as in Germany, on nine factors and 100 points: years active, beginner offer, events, Google rating, number of reviews and social media (75 points together), plus festivals, recent reviews and competitions (25 points, still “to be confirmed”). The data comes from the schools’ websites, Google Maps and Instagram. Anything we cannot confirm counts at the lowest level, and a school can complete it in its application.')

# ---------- /nl/ index ----------
t = T('nl')
city_cards = ''.join(
    f'<article><h3>{t("span", "Bachata " + v[0], "Bachata " + v[1])}</h3>{t("p", f"{len(by_city(k))} scholen, bovenaan: {by_city(k)[0][0]}.", f"{len(by_city(k))} schools, led by {by_city(k)[0][0]}.")}<a href="/nl/bachata-{k}.html">{t("span", "Scholen in de stad →", "Schools in this city →")}</a></article>'
    for k, v in P.CITIES.items())
main = hero(t, ('Bachata-editie · Nederland 2027', 'Bachata Edition · Netherlands 2027'),
  ('De beste bachata-dansscholen van Nederland: ranglijst 2027', 'The best Bachata schools in the Netherlands: ranking 2027'),
  (f'Onafhankelijke ranglijst van bachata-dansscholen in {NC} Nederlandse steden, gebaseerd op openbare gegevens. De resultaten publiceren we in het voorjaar van 2027.', f'An independent ranking of Bachata schools in {NC} Dutch cities, based on public data. Results will be published in spring 2027.'),
  [('cal', f'<b>{N} scholen</b> in {NC} steden', f'<b>{N} schools</b> in {NC} cities'), ('check', 'Onafhankelijk, <b>niet te koop</b>', 'Independent, <b>not for sale</b>'), ('clock', 'Resultaten in het <b>voorjaar van 2027</b>', 'Results <b>spring 2027</b>')],
  f'<a class="btn btn-gold" href="#ranking">{t("span", "Bekijk de huidige stand", "See the current standings")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Meld je school aan", "Enter your school")}</a>')
NL_C = RV.polish_entries(P, BASE)
TX = {k: list(v) if isinstance(v, list) else v for k, v in B.R_TEXT.items()}
TX['cities'] = {'netherlands': ['Heel Nederland', 'All Netherlands']}
TX['cities'].update({k: [v[0], v[1]] for k, v in P.CITIES.items()})
def _tx(k, es, en): TX[k] = [es, en]
_tx('title_city', 'De beste bachata-scholen: {c}', 'Best Bachata schools in {c}')
_tx('title_de', 'De beste bachata-scholen van Nederland', 'Best Bachata schools in the Netherlands')
_tx('sub_interim', 'Tussenstand: de plaatsen kunnen nog veranderen tot de resultaten in het voorjaar van 2027 worden gepubliceerd.', 'Interim standing: places can still change until the results are published in spring 2027.')
_tx('help_h', 'Hoe werkt de ranglijst?', 'How does the ranking work?')
_tx('help_p', 'Elke school wordt beoordeeld op dezelfde openbare criteria, in alle landen hetzelfde. Plaatsen zijn niet te koop.', 'Every school is scored on the same public criteria, identical in every country. Places cannot be bought.')
_tx('help_how', 'Hoe we beoordelen', 'How scoring works')
_tx('help_add', 'Mijn school toevoegen', 'Add my school')
_tx('help_tips_h', 'Zo verbeter je de plaats van je school', "How to improve your school's place")
TX['help_tips'] = [[
  'Verzorg je Google-profiel en vraag leerlingen om een review (Google-score 25 pt, aantal reviews 10 pt, recente reviews 5 pt)',
  'Zet het oprichtingsjaar, het team van docenten en de niveaus op je website (jaren actief 10 pt)',
  'Bied een proefles en vaste beginnersgroepen aan (aanbod voor beginners 10 pt)',
  'Organiseer feesten en workshops, nodig gastdocenten uit en laat het online zien (evenementen 10 pt)',
  'Houd je Instagram actief (social media 10 pt)',
  'Bevestig je festivals en wedstrijden met een link (festivals 15 pt, wedstrijden 5 pt)'], B.R_TEXT['help_tips'][1]]
_tx('pts', 'punten', 'points'); _tx('site', 'Website', 'Website'); _tx('insta', 'Instagram', 'Instagram')
_tx('note_h', 'Ontbreekt je school?', 'Is your school missing?')
_tx('note_p', 'Meld je school gratis aan voor de ranglijst van 2027.', 'Enter your school for the 2027 ranking for free.')
_tx('note_btn', 'Gratis aanmelden', 'Apply for free')
_tx('page_link', 'Schoolpagina, reviews en stemmen', 'School page, reviews and voting')
_tx('vote_h', 'Publieksprijs', 'Audience Award')
_tx('vote_banner', 'Publieksprijs: open een school en stem. Eén stem per persoon, bevestigd per e-mail. Los van de punten; de uitslag komt samen met de ranglijst.', 'Audience Award: open a school and vote. One vote per person, confirmed by email. It is separate from the points, and the result comes with the ranking.')
_tx('vote_btn', 'Stem op deze school', 'Vote for this school')
_tx('vote_mail', 'Je e-mailadres', 'Your email address')
_tx('vote_send', 'Stem versturen', 'Send my vote')
_tx('news_opt', 'Ja, ik ontvang af en toe graag nieuws, evenementen en aanbiedingen over bachata per e-mail. Je kunt je altijd afmelden.', B.R_TEXT['news_opt'][1])
_tx('vote_note', 'Eén stem per persoon. We sturen je een bevestigingslink. Je e-mailadres gebruiken we alleen hiervoor en om dubbele stemmen te verwijderen.', B.R_TEXT['vote_note'][1])
_tx('vote_ok', 'Bijna klaar: we hebben je een e-mail gestuurd. Klik op de link zodat je stem meetelt. Kijk ook in je spam.', B.R_TEXT['vote_ok'][1])
_tx('vote_err', 'Dat is niet gelukt. Controleer je e-mailadres en probeer het opnieuw.', B.R_TEXT['vote_err'][1])
_tx('vote_done', 'Vanaf dit apparaat is al een stem uitgebracht. Bedankt!', B.R_TEXT['vote_done'][1])
_tx('prelim_badge', 'Tussenstand · niet de einduitslag, de scholen strijden nog', 'Interim standing · not final, schools are still competing')
_tx('prelim_h', 'Hoe de tussenstand wordt berekend', 'How the interim standing is calculated')
_tx('prelim_p', 'We rekenen de punten zoals in Duitsland: tot 75 punten voor zes criteria (jaren actief, aanbod voor beginners, evenementen, Google-score, aantal reviews, social media) en tot 25 punten voor festivals, recente reviews en wedstrijden, die nog "te bevestigen" zijn. Gegevens: websites van de scholen, Google Maps en Instagram, stand oktober 2026. Wat niet bevestigd is, telt met de laagste waarde. De plaatsen kunnen nog veranderen.', 'Points are calculated exactly as in Germany: up to 75 points for six factors (years active, beginner offer, events, Google rating, number of reviews, social media) and up to 25 points for festivals, recent reviews and competitions, which are still “to be confirmed”. Data: school websites, Google Maps and Instagram, status October 2026. Anything unconfirmed counts at the lowest level. Positions can still change.')
_tx('empty', 'Er zijn nog geen resultaten voor deze stad.', 'There are no results for this city yet.')
_ES_TBC = ['Festivals', 'Recente reviews', 'Deelname aan wedstrijden', 'Gewonnen wedstrijden']
_EN_TBC = ['Festivals', 'Recent reviews', 'Competitions entered', 'Competitions won']
_MX = ['15', '5', '5', '5']
_QUICK = ['netherlands', 'amsterdam', 'rotterdam', 'utrecht', 'denhaag', 'eindhoven']
es_js = RV.make_js('netherlands', {}, TX, NL_C, _QUICK, 100, pl=True, code='NL', extra={
  'tbc': ([[n, m] for n, m in zip(_ES_TBC, _MX)], [[n, m] for n, m in zip(_EN_TBC, _MX)]),
  'literals': {
    '"Follower · Posts: "': '"Volgers · posts: "',
    '"Zu bestätigen"': '"Te bevestigen"',
    '"Noch ohne Punkte. Schulen bestätigen diese Angaben mit Links bei der Bewerbung."': '"Nog geen punten. Scholen bevestigen deze gegevens met links bij de aanmelding."',
    '"Jetzt bestätigen"': '"Nu bevestigen"',
    '"Keine Stadt gefunden"': '"Geen stad gevonden"',
    '["Jahre im Unterricht","Einsteigerangebot","Events und Gastlehrer","Google-Bewertung","Anzahl Bewertungen","Social Media"]': '["Jaren lesgeven","Aanbod voor beginners","Evenementen en gasten","Google-score","Aantal reviews","Social media"]',
    '"Alle "+pl.length+" Schulen anzeigen"': '"Bekijk alle "+pl.length+" scholen"',
  }})
_tabs = RV.tabs_html(t, [(k, TX['cities'][k][0], TX['cities'][k][1]) for k in _QUICK])
RANK_SECTION = RV.ranking_section(_tabs, 'Zoek een stad …', 'Search city …', 'Steden / Cities')
main += RANK_SECTION
main += f'''
{sec(t, 1, ("Bachata in Nederlandse steden", "Bachata in Dutch cities"), '<div class="cards two" id="steden">' + city_cards + '</div>', alt=False).replace('<section class="block"', '<section class="block" id="steden-sec"')}
{sec(t, 2, ("Hoe we bachata-scholen beoordelen", "How we score Bachata schools"), t("p", *METHOD_ES) + t("p", 'De ranglijst is uitsluitend gebaseerd op openbare gegevens. Plaatsen zijn niet te koop; eventuele betaalde vermeldingen worden als advertentie gemarkeerd en hebben geen invloed op de punten. We verzamelen de schoolgegevens zelf via Google Maps en de websites, dus er kunnen fouten in zitten: <a href="/bewerbung.html?lang=en">meld een school aan of stuur ons een correctie</a>.', 'The ranking is based only on public data. Places cannot be bought, and paid mentions, if any, will be labelled as ads and do not affect points. We collect the school data ourselves from Google Maps and the schools\' websites, so it may contain errors: <a href="/bewerbung.html?lang=en">enter a school or send a correction</a>.'), alt=True).replace('<section class="block alt"', '<section class="block alt" id="metodo"')}
{sec(t, 3, ("Europese ranglijst en ranglijsten per land", "Europe ranking and country rankings"), t("p", 'Latin Dance Awards maakt een ranglijst van scholen in heel Europa en een aparte ranglijst per land. Nederland komt erbij naast Duitsland, Polen, Spanje, Italië, Portugal en Frankrijk. Zie het <a href="/">overzicht van Europa</a>, de <a href="/deutschland.html">ranglijst van Duitsland</a>, die van <a href="/es/">Spanje</a> of die van <a href="/it/">Italië</a>.', 'Latin Dance Awards builds one ranking of schools across Europe plus a separate ranking for each country. The Netherlands joins Germany, Poland, Spain, Italy, Portugal and France. See the <a href="/">Europe overview</a>, the <a href="/deutschland.html">Germany ranking</a>, the <a href="/es/">Spain ranking</a> or the <a href="/it/">Italy ranking</a>.'), alt=False)}
'''
faq = [
 ('Wat is de beste bachata-school van Nederland?', 'What is the best Bachata school in the Netherlands?',
  f'Op dit moment staat volgens onze gegevens {ranked[0][0]} ({P.CITIES[ranked[0][1]][0]}) bovenaan met {f1(_TOP[0])} van de 100 punten. Het is een tussenstand; de definitieve resultaten volgen in het voorjaar van 2027.',
  f'As of today, by our data, {ranked[0][0]} ({P.CITIES[ranked[0][1]][1]}) leads with {f1en(_TOP[0])} of 100 points. This is an interim standing; final results come in spring 2027.'),
 ('Waar komen de gegevens vandaan?', 'Where does the ranking data come from?',
  'Uit openbare bronnen: de score en het aantal reviews op Google Maps en de websites van de scholen zelf, waar we controleren of bachata wordt gegeven.', 'From public sources: ratings and review counts on Google Maps and the schools\' own websites, where we check that the school teaches Bachata.'),
 ('Kan ik een plaats in de ranglijst kopen?', 'Can I buy a place in the ranking?', 'Nee. Plaatsen zijn niet te koop en betaalde vermeldingen hebben geen invloed op de punten.', 'No. Places cannot be bought, and paid mentions do not affect points.'),
 ('Hoe meld ik mijn school aan?', 'How do I enter my school?', 'Gebruik het <a href="/bewerbung.html?lang=en">gratis aanmeldformulier</a> (in het Engels). Met een aanmelding kun je je gegevens bevestigen en de volledige score krijgen.', 'Use the <a href="/bewerbung.html?lang=en">free application form</a> (in English). Applying lets you confirm your details and receive the full score.'),
 ('Welke steden staan in de ranglijst?', 'Which cities does the ranking cover?', f'Om te beginnen: {", ".join(v[0] for v in P.CITIES.values())}. Er komen steden bij zodra scholen zich aanmelden.', f'To start with: {", ".join(v[1] for v in P.CITIES.values())}. We will add more cities as schools apply.'),
]
main += faq_html(t, faq)
nl_page('nl/index.html', 'nl/', 'De beste bachata-dansscholen van Nederland: ranglijst 2027',
  f'Ranglijst van bachata-dansscholen in Nederland: {N} scholen in {NC} steden, met scores, punten en methode. Resultaten in het voorjaar van 2027. Onafhankelijk en niet te koop.',
  'The best Bachata schools in the Netherlands: 2027 ranking', f'Ranking of Bachata schools in the Netherlands: {N} schools in {NC} cities with ratings, points and method. Results in spring 2027. Independent and not for sale.',
  main, t.en, [crumbs('Nederland', 'nl/'), faq_schema(faq)], js=es_js)

# ---------- city pages ----------
for k, (cpl, cen, loc) in P.CITIES.items():
    ss = by_city(k); n = len(ss); t = T('nc' + k[:2])
    ranks = {s[0]: ranked.index(s) + 1 for s in ss}
    cards = ''.join(f'<article><h3>{s[0]}</h3>{t("p", f"Google-score: {f1(s[2])} ★ ({s[3]} reviews). Plaats {ranks[s[0]]} in Nederland.", f"Google rating: {f1en(s[2])} ★ ({s[3]} reviews). Rank {ranks[s[0]]} in the Netherlands.")}<a href="{s[4]}" rel="nofollow noopener" target="_blank">{t("span", "Website van de school", "School website")} →</a></article>' for s in ss)
    main = hero(t, (f'Bachata {cpl} · 2027', f'Bachata {cen} · 2027'),
      (f'Bachata {cpl}: de beste dansscholen 2027', f'Bachata {cen}: the best dance schools 2027'),
      (f'Bachata-scholen {loc}: {n} locaties met bevestigde lessen, met Google-scores en punten uit de tussenstand. Resultaten in het voorjaar van 2027.', f'Bachata schools in {cen}: {n} places with confirmed classes, with Google ratings and interim ranking points. Results in spring 2027.'),
      [('cal', f'<b>{n} scholen</b> {loc}', f'<b>{n} schools</b> in {cen}'), ('check', 'Gegevens van <b>oktober 2026</b>', 'Data from <b>October 2026</b>')],
      f'<a class="btn btn-gold" href="#ranking">{t("span", "Bekijk de ranglijst", "See the ranking")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Meld je school aan", "Enter your school")}</a>')
    main += f'''
<section class="block alt" id="ranking"><div class="wrap tp" style="max-width:860px">
  {t("h2", f"Ranglijst van bachata-scholen {loc}", f"Ranking of Bachata schools in {cen}")}
  {t("p", f"Tussenstand op basis van de Google-scores van oktober 2026 (max. 100 punten). De definitieve resultaten volgen in het voorjaar van 2027.", "Interim standing by Google ratings as of October 2026 (max 100 points). The final results are published in spring 2027.", 'class="muted"')}
  <div class="box">{school_list(ss, t)}</div>
</div></section>
{sec(t, 1, (f"Bachata-scholen {loc} in één oogopslag", f"Bachata schools in {cen} at a glance"), t("p", f"We vonden {n} scholen {loc} waar bachata wordt gegeven. De volgorde is gebaseerd op voorlopige punten, niet op een volledige beoordeling. Tijden, prijzen en groepen veranderen, dus bekijk de website van de school.", f"In {cen} we found {n} schools that teach Bachata. The order is based on interim points, not a full assessment. Times, prices and groups change, so check them on the school's website.") + '<div class="cards two">' + cards + '</div>', alt=False)}
{sec(t, 2, (f"Zo kies je een bachata-les {loc}", f"How to choose a Bachata class in {cen}"), t("p", "Een goede bachata-les past bij je niveau, je agenda en je reistijd. Met deze tips kies je beter:", "A good Bachata class fits your level, schedule and journey. These tips help:") + '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in [
   ('<strong>Niveau:</strong> begin in een beginnersgroep, ook als je al eerder hebt gedanst. De basispas is de basis van alles.', '<strong>Level:</strong> start with a beginner group, even if you have danced before. The basic step is the base for everything.'),
   ('<strong>Proefles:</strong> vraag om een proefles of de start van een nieuwe groep voordat je een cursus koopt.', '<strong>Trial class:</strong> ask for a trial class or a new group start before buying a pass.'),
   ('<strong>Partner:</strong> meestal heb je geen partner nodig. Vraag of er wordt gewisseld.', '<strong>Partner:</strong> you usually do not need to bring a partner. Ask whether partners rotate.'),
   ('<strong>Stijl:</strong> dominicaanse, moderne en sensual bachata hebben elk een eigen karakter. Kijk welke stijl de school geeft.', '<strong>Style:</strong> Dominicana, moderna and sensual bachata differ in character. Check which style the school teaches.')]) + '</ul>', alt=True)}
{sec(t, 3, ("Ranglijsten van Nederland, Europa en Duitsland", "Netherlands, Europe and Germany rankings"), t("p", 'Bekijk de <a href="/nl/">ranglijst van heel Nederland</a>, het <a href="/">overzicht van Europa</a> of de <a href="/deutschland.html">ranglijst van Duitsland</a>. Heb je een school ' + loc + '? <a href="/bewerbung.html?lang=en">Meld hem gratis aan</a>.', f'See the <a href="/nl/">Netherlands ranking</a>, the <a href="/">Europe overview</a> or the <a href="/rankings.html">Germany ranking</a>. Do you run a school in {cen}? <a href="/bewerbung.html?lang=en">Enter it for free</a>.'), alt=False)}
'''
    top = ss[0]
    faq = [
     (f'Waar kan ik bachata leren {loc}?', f'Where can I learn Bachata in {cen}?', f'Bachata {loc} leer je bij {", ".join(s[0] for s in ss[:3])} en andere scholen. De volledige lijst staat hierboven.', f'In {cen} Bachata is taught by {", ".join(s[0] for s in ss[:3])} and others. The full list is above.'),
     (f'Wat is de beste bachata-school {loc}?', f'What is the best Bachata school in {cen}?', f'Op dit moment staat volgens onze gegevens {top[0]} bovenaan ({f1(top[2])} ★, {top[3]} reviews). Het is een tussenstand, niet de definitieve ranglijst.', f'As of today, by Google ratings, {top[0]} leads ({f1en(top[2])} ★, {top[3]} reviews). This is an interim standing, not the final ranking.'),
     ('Heb ik een partner nodig voor een bachata-les?', 'Do I need a partner for a Bachata class?', 'Meestal niet. Op veel scholen wordt van partner gewisseld. Vraag het voor de eerste les.', 'Usually not. Many schools rotate partners. Ask before your first class.'),
     ('Met welke bachata-stijl begin ik?', 'Which Bachata style should I start with?', 'De meeste beginners starten met moderne of sensual bachata. De basispas en het ritme zijn het belangrijkst; later kun je van stijl wisselen.', 'Most beginners start with moderna or sensual. What matters is the basic step and the rhythm, and you can change style later.'),
     ('Wanneer wordt de volledige ranglijst gepubliceerd?', 'When is the full ranking published?', 'In het voorjaar van 2027. Tot die tijd tonen we een tussenstand op basis van Google-scores.', 'In spring 2027. Until then we show an interim standing based on Google ratings.'),
    ]
    main += faq_html(t, faq)
    nl_page(f'nl/bachata-{k}.html', f'nl/bachata-{k}.html', f'Bachata {cpl}: de beste dansscholen 2027',
      f'Bachata {cpl}: {n} scholen met Google-scores en punten uit de ranglijst 2027. Kies een bachata-les {loc} en bekijk de tussenstand.',
      f'Bachata {cen}: the best dance schools 2027', f'Bachata {cen}: {n} schools with Google ratings and 2027 ranking points. Choose a Bachata class in {cen} and see the interim ranking.',
      main, t.en, [crumbs(f'Bachata {cpl}', f'nl/bachata-{k}.html'), faq_schema(faq)])
