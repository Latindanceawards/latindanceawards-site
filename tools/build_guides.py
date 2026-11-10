# Builds the keyword landing pages (city guides, topic guides). Run: python3 tools/build_guides.py
# Reuses tools/build.py (head, CSS, header, footer, helpers). Running this also rebuilds the base pages.
import os, sys, re, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
from build import T, page, crumbs, faq_schema, ICON, ROOT

B.PAGE_CSS += r'''
.cards.two{grid-template-columns:repeat(2,1fr)}
.cards article a{color:var(--gold-light);font-weight:600}
.cards article .meta{display:block;margin-top:12px;font-size:13.5px;color:var(--gold)}
.prose .btnrow{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px;max-width:none}
@media (max-width:960px){.cards.two{grid-template-columns:1fr}}
'''

# Planned guide pages: slug -> (anchor text DE, anchor text EN, group). Only pages that exist get linked.
CITY_PAGES = [('bachata-berlin', 'Berlin', 'Berlin'), ('bachata-hamburg', 'Hamburg', 'Hamburg'),
              ('bachata-muenchen', 'München', 'Munich'), ('bachata-koeln', 'Köln', 'Cologne'),
              ('bachata-frankfurt', 'Frankfurt', 'Frankfurt'), ('bachata-duesseldorf', 'Düsseldorf', 'Düsseldorf'),
              ('bachata-stuttgart', 'Stuttgart', 'Stuttgart'), ('bachata-freiburg', 'Freiburg', 'Freiburg'), ('bachata-bremen', 'Bremen', 'Bremen'),
              ('bachata-dresden', 'Dresden', 'Dresden'), ('bachata-nuernberg', 'Nürnberg', 'Nuremberg'), ('bachata-saarbruecken', 'Saarbrücken', 'Saarbrücken'),
              ('bachata-essen', 'Essen', 'Essen'), ('bachata-bonn', 'Bonn', 'Bonn'), ('bachata-karlsruhe', 'Karlsruhe', 'Karlsruhe'),
              ('bachata-kassel', 'Kassel', 'Kassel'), ('bachata-hannover', 'Hannover', 'Hannover'), ('bachata-braunschweig', 'Braunschweig', 'Braunschweig'), ('bachata-heidelberg', 'Heidelberg', 'Heidelberg'), ('bachata-dortmund', 'Dortmund', 'Dortmund'), ('bachata-kiel', 'Kiel', 'Kiel'), ('bachata-bochum', 'Bochum', 'Bochum'), ('bachata-regensburg', 'Regensburg', 'Regensburg'), ('bachata-mannheim', 'Mannheim', 'Mannheim'), ('bachata-wuerzburg', 'Würzburg', 'Würzburg'), ('bachata-muenster', 'Münster', 'Münster'), ('bachata-augsburg', 'Augsburg', 'Augsburg'),
              ('bachata-gelsenkirchen', 'Gelsenkirchen', 'Gelsenkirchen'), ('bachata-oldenburg', 'Oldenburg', 'Oldenburg'), ('bachata-kempten', 'Kempten', 'Kempten'), ('bachata-leipzig', 'Leipzig', 'Leipzig')]
TOPIC_PAGES = [('bachata-tanzen', 'Bachata tanzen lernen', 'Learn to dance Bachata'),
               ('bachata-festivals-deutschland', 'Bachata-Festivals 2026/2027', 'Bachata festivals 2026/2027'),
               ('bachata-grundschritt', 'Bachata-Grundschritt', 'Bachata basic step'),
               ('bachata-sensual', 'Bachata Sensual', 'Bachata Sensual'),
               ('bachata-dominicana', 'Bachata Dominicana', 'Bachata Dominicana'),
               ('bachata-musik', 'Bachata Musik', 'Bachata music'),
               ('bachata-tanzschule', 'Bachata Tanzschule', 'Bachata dance school'),
               ('bachata-tanzkurs', 'Bachata Tanzkurs', 'Bachata dance course'),
               ('bachata-salsa-unterschied', 'Salsa und Bachata', 'Salsa and Bachata'),
               ('bachata-schritte', 'Bachata Schritte', 'Bachata steps'),
               ('bachata-lernen', 'Bachata lernen', 'Learn Bachata'),
               ('bachata-workshop', 'Bachata Workshop', 'Bachata workshop'),
               ('bachata-fuer-anfaenger', 'Bachata für Anfänger', 'Bachata for beginners'),
               ('bachata-ladies-styling', 'Bachata Ladies Styling', 'Bachata ladies styling'),
               ('bachata-moderna', 'Bachata Moderna', 'Bachata Moderna'),
               ('bachata-party', 'Bachata Party', 'Bachata party'),
               ('bachata-kurs-in-der-naehe', 'Bachata Kurs in der Nähe', 'Bachata class near you'),
               ('bachata-solo', 'Bachata Solo', 'Bachata solo'),
               ('bachata-was-ist-das', 'Was ist Bachata', 'What is Bachata'),
               ('salsa-tanzen', 'Salsa tanzen', 'Dancing Salsa'),
               ('bachata-hochzeitstanz', 'Bachata Hochzeitstanz', 'Bachata wedding dance'),
               ('bachata-kurs-berlin', 'Bachata Kurs Berlin', 'Bachata class Berlin'),
               ('bachata-tanzschule-berlin', 'Bachata Tanzschule Berlin', 'Bachata dance school Berlin'),
               ('bachata-staedte-deutschland', 'Alle Städte und Schulen', 'All cities and schools')]

SHOW_FESTIVALS = False  # set True to publish the festival listing again

def exists(slug): return os.path.exists(os.path.join(ROOT, slug + '.html'))

def render_blocks(t, blocks):
    out = []
    for b in blocks:
        if b[0] == 'p': out.append('    ' + t('p', b[1], b[2]))
        elif b[0] == 'h3': out.append('    ' + t('h3', b[1], b[2]))
        elif b[0] == 'ul':
            out.append('    <ul>' + ''.join(f'<li>{t("span", d, e)}</li>' for d, e in b[1]) + '</ul>')
        elif b[0] == 'cards':
            out.append('    <div class="cards two">' + ''.join(
                f'<article>{t("h3", c["name"], c["name"])}{t("p", c["de"], c["en"])}'
                 + '</article>'
                for c in b[1]) + '</div>')
        elif b[0] == 'raw': out.append(b[1])
        elif b[0] == 'ev': out.append(ev_block(t, b[1]))
        elif b[0] == 'evall': out.append(ev_cards(t, EV_BY_CITY[b[1]]))
    return '\n'.join(out)

from events_data import EVENTS, CITY_LABEL, META, WD
EV_BY_CITY = {}
for _e in EVENTS: EV_BY_CITY.setdefault(_e['city'], []).append(_e)

def ev_cards(t, evs, h='h3'):
    out = []
    for e in evs:
        links = ''
        if e['site']: links += f'<a href="{e["site"]}" rel="noopener nofollow" target="_blank">{t("span", "Veranstalter", "Organiser")}</a> '
        links += f'<a href="{e["src"]}" rel="noopener nofollow" target="_blank">{t("span", "Quelle", "Source")}</a> '
        links += f'<a href="https://www.google.com/maps/search/?api=1&amp;query={urllib.parse.quote(e["venue"] + ", " + e["addr"])}" rel="noopener nofollow" target="_blank">{t("span", "Karte", "Map")}</a>'
        price = f' ({e["price"]})' if e['price'] else ''
        out.append(f'<article data-city="{e["city"]}">{t(h, e["name"], e["name"])}'
                   f'<p>{e["venue"]}, {e["addr"]}</p>'
                   f'{t("p", e["rec"][0] + ". " + e["time"][0] + ".", e["rec"][1] + ". " + e["time"][1] + ".")}'
                   f'<span class="meta">{e["price"] or "&nbsp;"}</span><div class="evl">{links}</div></article>')
    return '<div class="cards two evc">' + ''.join(out) + '</div>'

def ev_block(t, key):
    evs = EV_BY_CITY.get(key, [])
    if not evs: return ''
    note = t('p', 'Regelmäßige Socials mit Bachata, nach Stand Oktober 2026 aus öffentlichen Listen und den Seiten der Veranstalter. Zeiten und Preise ändern sich, bitte prüfe sie vor dem Besuch. Alle Details: <a href="bachata-party-' + key + '.html">Bachata-Party in der Stadt</a>. Dein Social fehlt? <a href="bachata-socials.html#eintragen">Trag es kostenlos ein</a>.',
               'Regular socials with Bachata, as of October 2026, from public listings and the organisers\' pages. Times and prices change, so please check before you go. Full details: <a href="bachata-party-' + key + '.html">Bachata party page</a>. Is your social missing? <a href="bachata-socials.html#eintragen">List it for free</a>.')
    return ev_cards(t, evs) + '\n    ' + note


def guide_page(slug, pref, title_de, desc_de, title_en, desc_en, crumb, edition, h1, lede, facts, sections, faq,
               ranking_anchor=None, sibling_group=None):
    t = T(pref)
    if ranking_anchor in EV_BY_CITY and not slug.startswith('bachata-party-'):
        sections = [(a, b, (list(c) + [('ev', ranking_anchor)]) if a.startswith('Bachata-Party in') else c) for a, b, c in sections]
    faq_html = '\n'.join(f'      <details>{t("summary", q, qe)}{t("p", a, ae)}</details>' for q, qe, a, ae in faq)
    secs = []
    for i, (h2, h2e, blocks) in enumerate(sections):
        alt = ' alt' if i % 2 == 0 else ''
        secs.append(f'''<section class="block{alt}" aria-labelledby="{pref}h{i}">
  <div class="wrap prose">
    {t("h2", h2, h2e, f'id="{pref}h{i}"')}
{render_blocks(t, blocks)}
  </div>
</section>''')
    # internal-link block: other cities + topic guides + ranking + application
    links = []
    if sibling_group == 'city':
        for s, de, en in CITY_PAGES:
            if s != slug and exists(s):
                links.append(f'<a href="{s}.html">{t("span", "Bachata " + de, "Bachata " + en)}</a>')
    for s, de, en in TOPIC_PAGES:
        if s != slug and exists(s):
            links.append(f'<a href="{s}.html">{t("span", de, en)}</a>')
    links.append(f'<a href="rankings.html{("#" + ranking_anchor) if ranking_anchor else ""}">{t("span", "Rankings 2026", "Rankings 2026")}</a>')
    secs.append(f'''<section class="block{" alt" if len(sections) % 2 == 0 else ""}" aria-labelledby="{pref}more">
  <div class="wrap prose">
    {t("h2", "Weiterlesen auf Latin Dance Awards", "More on Latin Dance Awards", f'id="{pref}more"')}
    {t("p", 'Alle Städte, Stile und Festivals im Überblick. Die vollständige Methode steht auf der <a href="deutschland.html#method">Startseite</a>, die Bewerbung für Schulen auf der <a href="bewerbung.html">Bewerbungsseite</a>.', 'All cities, styles and festivals at a glance. The full method is on the <a href="deutschland.html#method">homepage</a>, and schools can enter on the <a href="bewerbung.html">application page</a>.')}
    <div class="citylinks">{"".join(links)}</div>
  </div>
</section>''')
    seal = '<img class="seal" src="badge-bachata-2026.svg" alt="Siegel der Bachata Awards 2026" width="360" height="360" fetchpriority="low">'
    fact_html = ''.join(f'<span>{ICON[ic]}{t("span", d, e)}</span>' for ic, d, e in facts)
    main = f'''
<section class="page-hero" aria-labelledby="{pref}title">
  <div class="wrap">
    <div>
      <span class="edition rise d1"><i></i>{t("span", edition[0], edition[1])}</span>
      <h1 id="{pref}title" class="rise d2">{t("span", h1[0], h1[1])}</h1>
      <p class="lede rise d3">{t("span", lede[0], lede[1])}</p>
      <div class="facts rise d4">{fact_html}</div>
      <div class="ctas rise d5">
        <a class="btn btn-gold" href="rankings.html{("#" + ranking_anchor) if ranking_anchor else ""}">{t("span", "Zum Ranking 2026", "See the 2026 ranking")}</a>
        <a class="btn btn-ghost" href="bewerbung.html">{t("span", "Schule kostenlos bewerben", "Enter a school for free")}</a>
      </div>
    </div>
    <div class="seal-box rise d3">{seal}</div>
  </div>
</section>

{chr(10).join(secs)}

<section class="block{" alt" if len(sections) % 2 == 1 else ""}" id="faq" aria-labelledby="{pref}faq">
  <div class="wrap">
    <div class="sec-head">{t("h2", "Häufige Fragen", "Frequently asked questions", f'id="{pref}faq"')}</div>
    <div class="faq">
{faq_html}
    </div>
  </div>
</section>
'''
    page(slug + '.html', title_de, desc_de, title_en, desc_en, slug + '.html', main, t.en, '',
         schema=[crumbs(crumb, slug + '.html'), faq_schema(faq)])

# ======================================================================
# BACHATA BERLIN
# ======================================================================
WIKI = '<a href="https://de.wikipedia.org/wiki/Bachata" rel="noopener">Wikipedia</a>'
WIKI_EN = '<a href="https://en.wikipedia.org/wiki/Bachata_(music)" rel="noopener">Wikipedia</a>'

berlin_sections = [
 ('Bachata in Berlin: So ist die Szene', 'Bachata in Berlin: what the scene is like', [
   ('p', f'Berlin gehört zu den größten Städten für Bachata in Deutschland. Hier gibt es Schulen für jedes Level, regelmäßige Partys und Workshops mit internationalen Gästen. Bachata stammt aus der Dominikanischen Republik ({WIKI}), und in Berlin treffen sich heute alle Stile: ursprüngliches Dominicana, modernes Bachata und das in Europa entstandene Bachata Sensual.',
          f'Berlin is one of the biggest cities for Bachata in Germany. It has schools for every level, regular parties and workshops with international guests. Bachata comes from the Dominican Republic ({WIKI_EN}), and in Berlin all styles meet today: original Dominicana, modern Bachata and Bachata Sensual, which developed in Europe.'),
   ('p', 'Wer in Berlin Bachata lernen will, hat die Qual der Wahl. Die Stadt ist groß, die Anfahrtswege sind lang, und jede Schule hat einen anderen Schwerpunkt. Deshalb lohnt es sich, den Kurs nach Stadtteil, Stil und Probestunde auszuwählen.',
          'If you want to learn Bachata in Berlin, you are spoilt for choice. The city is big, journeys are long, and every school has its own focus. So it pays to choose a class by district, style and trial class.'),
 ]),
 ('Bachata-Schulen in Berlin im Überblick', 'Bachata schools in Berlin at a glance', [
   ('p', 'Diese Berliner Schulen erscheinen bei Google besonders sichtbar für die Suche nach einem Bachata-Kurs. Die Reihenfolge ist alphabetisch und keine Wertung: Das offizielle Ranking erscheint am 20. Dezember 2026. Angaben beruhen auf den Websites der Schulen (Stand Oktober 2026), bitte prüfe Termine und Preise direkt dort.',
          'These Berlin schools show up most prominently on Google when you search for a Bachata class. The order is alphabetical and not a rating: the official ranking is published on December 20, 2026. Details come from the schools\' own websites (as of October 2026), so please check dates and prices there.'),
   ('cards', [
     {'name': 'BachatAcademy', 'url': 'https://www.bachatacademy.de',
      'de': 'Im Studio in der Samariterstraße 34 in Friedrichshain. Es gibt eine kostenlose, unverbindliche Probestunde, du brauchst weder Erfahrung noch Partner. Die Partner wechseln im Kurs regelmäßig. Auf der Website sind zwölf Lehrer genannt, dazu Bachata Sensual und Conscious Bachata.',
      'en': 'Studio at Samariterstraße 34 in Friedrichshain. It offers a free, no-obligation trial class, and you need neither experience nor a partner. Partners rotate in class. The website lists twelve teachers, plus Bachata Sensual and Conscious Bachata.'},
     {'name': 'La Mambita', 'url': 'https://www.mambita.de/bachata',
      'de': 'In Schöneberg, gut mit S-Bahn und U-Bahn erreichbar. Der Schwerpunkt liegt auf Bachata Sensual und Moderna mit kurzen Ausflügen in Dominicana. Dienstags laufen vier Levels nacheinander, vom Einstieg bis zur Fortgeschrittenen-Stufe. Drop-in ist möglich, Urban Sports Club wird akzeptiert.',
      'en': 'In Schöneberg, easy to reach by S-Bahn and U-Bahn. The focus is Bachata Sensual and Moderna with short excursions into Dominicana. On Tuesdays four levels run back to back, from beginner to advanced. Drop-in is possible and Urban Sports Club is accepted.'},
     {'name': 'HAVANNA Berlin', 'url': 'https://www.havanna-berlin.de/dance-lesson',
      'de': 'Tanzschule mit Latin-Programm, auf der Website gibt es eine eigene Seite zu den Tanzkursen.',
      'en': 'Dance school with a Latin programme, with a dedicated page for dance classes on its website.'},
     {'name': 'Cumbancha', 'url': 'https://www.cumbancha.de',
      'de': 'Berliner Tanzschule mit Bachata-Kursen im Programm.',
      'en': 'Berlin dance school with Bachata classes in its programme.'},
     {'name': 'Zapatissimo', 'url': 'https://www.zapatissimo.de/bachata-kurse-berlin',
      'de': 'Tanzschule mit eigener Seite für Bachata-Kurse in Berlin, unter anderem mit Bootcamp-Angeboten.',
      'en': 'Dance school with its own page for Bachata classes in Berlin, including bootcamp formats.'},
     {'name': 'Traumtänzer', 'url': 'https://www.traumtaenzer.de',
      'de': 'Tanzschule, die bei der Suche nach einem Bachata-Kurs in Berlin auftaucht.',
      'en': 'Dance school that appears when searching for a Bachata class in Berlin.'},
   ]),
   ('p', 'Deine Schule fehlt oder die Angaben stimmen nicht mehr? Dann schreib uns über die <a href="bewerbung.html">kostenlose Bewerbung</a>, wir ergänzen und korrigieren.',
          'Is your school missing, or are the details out of date? Send us the <a href="bewerbung.html">free application</a> and we will add or correct it.'),
 ]),
 ('Bachata-Kurs in Berlin finden: Level, Probestunde, Kosten', 'Finding a Bachata class in Berlin: levels, trial class, cost', [
   ('p', 'Ein guter Bachata-Kurs in Berlin passt zu deinem Level, deinem Zeitplan und deinem Weg zur Arbeit. Diese Punkte helfen bei der Auswahl:',
          'A good Bachata class in Berlin fits your level, your schedule and your commute. These points help you choose:'),
   ('ul', [
     ('<strong>Probestunde:</strong> Einige Schulen bieten sie kostenlos an. Nutze sie, bevor du dich für einen Monat oder ein Paket entscheidest.', '<strong>Trial class:</strong> some schools offer it for free. Use it before you commit to a month or a bundle.'),
     ('<strong>Level:</strong> Starte bei den Einsteigern, auch mit Tanzerfahrung. Der Bachata-Grundschritt mit seinem Tap auf Zählzeit vier gibt die Basis für alles Weitere.', '<strong>Level:</strong> start with beginners, even if you have danced before. The basic step with its tap on count four is the base for everything else.'),
     ('<strong>Partner:</strong> Du brauchst in der Regel niemanden mitzubringen. Frag nach, ob die Partner im Kurs wechseln.', '<strong>Partner:</strong> you usually do not need to bring anyone. Ask whether partners rotate in class.'),
     ('<strong>Lage:</strong> Berlin ist groß. Ein Kurs in deinem Kiez oder auf dem Arbeitsweg bleibt eher ein fester Termin.', '<strong>Location:</strong> Berlin is big. A class in your neighbourhood or on your commute is more likely to stay a fixed date.'),
     ('<strong>Flexible Modelle:</strong> Manche Studios akzeptieren Urban Sports Club oder bieten Drop-in. Das ist praktisch, wenn deine Woche wechselt.', '<strong>Flexible options:</strong> some studios accept Urban Sports Club or offer drop-in. That is handy if your week changes.'),
   ]),
   ('p', 'Die Preise unterscheiden sich je nach Schule und Modell (Einzelstunde, Monatsbeitrag, Workshop). Wir nennen hier bewusst keine festen Zahlen, weil sie sich ändern. Vergleiche am besten zwei oder drei Preislisten.',
          'Prices differ by school and model (single class, monthly fee, workshop). We deliberately do not quote fixed numbers here because they change. It is best to compare two or three price lists.'),
   ('p', 'Mehr Details zu Formaten und Anbietern findest du auf <a href="bachata-kurs-berlin.html">Bachata Kurs Berlin</a>, einen Vergleich der Schulen auf <a href="bachata-tanzschule-berlin.html">Bachata Tanzschule Berlin</a>.',
          'You will find more on formats and providers at <a href="bachata-kurs-berlin.html">Bachata class Berlin</a>, and a comparison of schools at <a href="bachata-tanzschule-berlin.html">Bachata dance school Berlin</a>.'),
 ]),
 ('Bachata lernen in Berlin: Welcher Stil passt zu dir?', 'Learning Bachata in Berlin: which style suits you?', [
   ('h3', 'Bachata Dominicana', 'Bachata Dominicana'),
   ('p', 'Der Stil der Karibik: schnelle Fußarbeit, offene Haltung und viel Spiel mit der Musik. Ideal für alle, die Rhythmus lieben.',
          'The Caribbean style: fast footwork, an open hold and lots of play with the music. Ideal if you love rhythm.'),
   ('h3', 'Bachata Sensual', 'Bachata Sensual'),
   ('p', 'In Europa entstanden und in Berlin sehr verbreitet: enge Verbindung, Wellen und fließende Drehungen. Auf vielen Partys und Festivals der Hauptstil.',
          'Developed in Europe and very common in Berlin: close connection, body waves and flowing turns. The main style at many parties and festivals.'),
   ('h3', 'Bachata Moderna', 'Bachata Moderna'),
   ('p', 'Grundschritt plus Drehungen und Elemente anderer Tänze. Viele Einsteigerkurse beginnen hier, weil der Zugang leicht ist.',
          'Basic step plus turns and elements from other dances. Many beginner classes start here because it is easy to get into.'),
 ]),
 ('Bachata-Party in Berlin: Socials und Übungsabende', 'Bachata parties in Berlin: socials and practice nights', [
   ('p', 'Tanzen lernst du im Kurs, besser wirst du auf der Tanzfläche. Viele Berliner Schulen veranstalten eigene Socials oder Übungsabende, und es gibt Partys, die nur Bachata spielen. BachatAcademy nennt auf der Website zum Beispiel Bachata-Day-Socials und Workshops, La Mambita bietet Social-Dance-Events an.',
          'You learn to dance in class, but you improve on the dance floor. Many Berlin schools run their own socials or practice nights, and there are parties that play only Bachata. BachatAcademy, for example, lists Bachata Day socials and workshops on its website, and La Mambita offers social dance events.'),
   ('p', 'Tipp für den ersten Besuch: Komm früh, tanze mit Leuten aus deinem Kurs und frag nach einem Tanz. Die Szene ist offen, und Anfänger sind überall willkommen. Wer plant, mehr Szene zu erleben, findet in unserem Überblick der <a href="rankings.html">Rankings</a> bald auch die Schulen mit den meisten Events und Gastlehrern.',
          'Tip for your first visit: come early, dance with people from your class and ask for a dance. The scene is open and beginners are welcome everywhere. If you want to see more of the scene, our <a href="rankings.html">rankings</a> will soon show which schools run the most events and guest teachers.'),
 ]),
 ('So bewerten wir die Bachata-Schulen in Berlin', 'How we score Bachata schools in Berlin', [
   ('p', 'Das Berliner Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html#berlin">Ranking-Seite</a>. Jede Schule wird nach denselben neun öffentlichen Kriterien mit zusammen 100 Punkten bewertet, unter anderem Google-Bewertung, Festivals, Jahre aktiv, Kursangebot für Einsteiger, Events und Social Media. Plätze sind nicht käuflich.',
          'The Berlin ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html#berlin">ranking page</a>. Every school is scored on the same nine public factors, 100 points in total, including Google rating, festivals, years active, beginner offer, events and social media. Places cannot be bought.'),
   ('p', 'Du leitest eine Schule in Berlin? <a href="bewerbung.html">Bewirb dich bis zum 30. November</a> kostenlos, damit wir deine Angaben bestätigen können.',
          'Do you run a school in Berlin? <a href="bewerbung.html">Apply for free by November 30</a> so we can confirm your details.'),
 ]),
]

berlin_faq = [
 ('Wo kann ich in Berlin Bachata lernen?', 'Where can I learn Bachata in Berlin?',
  'In vielen Berliner Tanzschulen und Studios, zum Beispiel BachatAcademy in Friedrichshain und La Mambita in Schöneberg. Oben findest du eine Übersicht mit Links zu den Websites.',
  'In many Berlin dance schools and studios, for example BachatAcademy in Friedrichshain and La Mambita in Schöneberg. Above you will find an overview with links to their websites.'),
 ('Brauche ich einen Partner für einen Bachata-Kurs in Berlin?', 'Do I need a partner for a Bachata class in Berlin?',
  'Nein, in der Regel nicht. Viele Schulen wechseln die Partner im Kurs. Frag am besten vor der Probestunde nach.',
  'No, usually not. Many schools rotate partners in class. It is best to ask before the trial class.'),
 ('Gibt es eine kostenlose Probestunde?', 'Is there a free trial class?',
  'Manche Schulen bieten sie an, BachatAcademy nennt auf der Website zum Beispiel eine kostenlose, unverbindliche Probestunde. Termine ändern sich, prüfe sie direkt bei der Schule.',
  'Some schools do. BachatAcademy, for example, lists a free, no-obligation trial class on its website. Dates change, so check them with the school.'),
 ('Welcher Bachata-Stil ist für Anfänger am besten?', 'Which Bachata style is best for beginners?',
  'Die meisten Einsteiger starten mit Bachata Moderna oder Sensual. Wichtig ist der Grundschritt und ein klarer Rhythmus. Der Stil lässt sich später wechseln.',
  'Most beginners start with Bachata Moderna or Sensual. What matters is the basic step and a clear rhythm. You can switch styles later.'),
 ('Wann erscheint das Ranking der besten Bachata-Schulen in Berlin?', 'When is the ranking of the best Bachata schools in Berlin published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html#berlin">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html#berlin">ranking page</a>.'),
 ('Wo finde ich Bachata-Partys in Berlin?', 'Where can I find Bachata parties in Berlin?',
  'Viele Schulen veranstalten eigene Socials, die du auf ihren Websites und auf Instagram findest. Frag in deinem Kurs nach den nächsten Terminen.',
  'Many schools run their own socials, which you can find on their websites and on Instagram. Ask in your class about the next dates.'),
]

guide_page('bachata-berlin', 'bb',
  'Bachata Berlin: Die besten Bachata-Schulen 2026',
  'Bachata Berlin: Schulen, Kurse und Partys im Überblick. So findest du den passenden Bachata-Kurs, mit Probestunde, Stilen und dem Ranking 2026.',
  'Bachata Berlin: The best Bachata schools 2026',
  'Bachata Berlin: schools, classes and parties at a glance. How to find the right Bachata class, with trial classes, styles and the 2026 ranking.',
  'Bachata Berlin', ('Bachata Berlin · Awards 2026', 'Bachata Berlin · Awards 2026'),
  ('Bachata Berlin: Die <em class="foil">besten Schulen</em> 2026', 'Bachata Berlin: the <em class="foil">best schools</em> 2026'),
  ('Bachata Berlin im Überblick: Schulen, Kurse und Partys. So findest du den richtigen Bachata-Kurs in Berlin, vom ersten Probetraining bis zur Tanzparty. Das Ranking erscheint am 20. Dezember 2026.',
   'Bachata Berlin at a glance: schools, classes and parties. Find the right Bachata class in Berlin, from your first trial class to your first dance party. The ranking is published on December 20, 2026.'),
  [('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>'), ('check', 'Unabhängig, <b>nicht käuflich</b>', 'Independent, <b>not for sale</b>')],
  berlin_sections, berlin_faq, ranking_anchor='berlin', sibling_group='city')


# ======================================================================
# Reusable city guide (Hamburg, München, ...)
# ======================================================================
t_wa_de = 'WhatsApp-Gruppe beitreten'

def city_guide(slug, pref, city_de, city_en, rank_anchor, intro, cards, cards_note, party, faq_extra, lede_extra=('', '')):
    secs = [
     (f'Bachata in {city_de}: So ist die Szene', f'Bachata in {city_en}: what the scene is like', [
       ('p', intro[0] + f' Bachata stammt aus der Dominikanischen Republik ({WIKI}), und heute gibt es drei Stile: ursprüngliches Dominicana, modernes Bachata und das in Europa entstandene Bachata Sensual.',
             intro[1] + f' Bachata comes from the Dominican Republic ({WIKI_EN}), and today there are three styles: original Dominicana, modern Bachata and Bachata Sensual, which developed in Europe.'),
       ('p', f'Wer in {city_de} Bachata lernen will, sollte Stil, Level, Wochentag und Anfahrt vergleichen. Eine Schule direkt auf dem Arbeitsweg oder im eigenen Viertel bleibt eher ein fester Termin als ein Kurs am anderen Ende der Stadt.',
             f'If you want to learn Bachata in {city_en}, compare style, level, weekday and journey. A school on your commute or in your own neighbourhood is more likely to stay a fixed date than a class across town.'),
     ]),
     (f'Bachata-Schulen in {city_de} im Überblick', f'Bachata schools in {city_en} at a glance', [
       ('p', f'Diese Anbieter in {city_de} haben Bachata im Programm. Die Reihenfolge ist alphabetisch und keine Wertung: Das offizielle Ranking erscheint am 20. Dezember 2026. Die Angaben stammen von den Websites der Schulen und von Veranstaltungslisten (Stand Oktober 2026). Termine und Preise ändern sich, bitte prüfe sie direkt bei der Schule.',
             f'These providers in {city_en} offer Bachata. The order is alphabetical and not a rating: the official ranking is published on December 20, 2026. Details come from the schools\' websites and event listings (as of October 2026). Dates and prices change, so please check them with the school.'),
       ('cards', cards),
       ('p', cards_note[0] + ' Deine Schule fehlt oder die Angaben stimmen nicht mehr? Schick uns die <a href="bewerbung.html">kostenlose Bewerbung</a>, wir ergänzen und korrigieren.',
             cards_note[1] + ' Is your school missing, or are the details out of date? Send us the <a href="bewerbung.html">free application</a> and we will add or correct it.'),
     ]),
     (f'Bachata-Kurs in {city_de} finden: Level, Probestunde, Kosten', f'Finding a Bachata class in {city_en}: levels, trial class, cost', [
       ('p', f'Ein guter Bachata-Kurs in {city_de} passt zu deinem Level, deinem Zeitplan und deinem Weg. Diese Punkte helfen bei der Auswahl:',
             f'A good Bachata class in {city_en} fits your level, your schedule and your journey. These points help you choose:'),
       ('ul', [
         ('<strong>Level:</strong> Starte bei den Einsteigern, auch mit Tanzerfahrung. Der Grundschritt mit seinem Tap auf Zählzeit vier ist die Basis für alles Weitere.', '<strong>Level:</strong> start with beginners, even if you have danced before. The basic step with its tap on count four is the base for everything else.'),
         ('<strong>Probestunde:</strong> Frag nach einer Schnupperstunde oder einem Einsteigertermin, bevor du dich für einen Monat oder ein Paket entscheidest.', '<strong>Trial class:</strong> ask for a taster class or a beginner start date before you commit to a month or a bundle.'),
         ('<strong>Partner:</strong> Du brauchst in der Regel niemanden mitzubringen. Frag nach, ob die Partner im Kurs wechseln.', '<strong>Partner:</strong> you usually do not need to bring anyone. Ask whether partners rotate in class.'),
         ('<strong>Rhythmus:</strong> Viele Kurse laufen als Block über mehrere Wochen. Ein fester Wochentag hilft beim Dranbleiben.', '<strong>Routine:</strong> many courses run as a block over several weeks. A fixed weekday helps you stick with it.'),
       ]),
       ('p', 'Preise unterscheiden sich je nach Schule und Modell (Einzelstunde, Monatsbeitrag, Workshop). Wir nennen hier bewusst keine festen Zahlen, weil sie sich ändern. Vergleiche am besten zwei oder drei Preislisten.',
             'Prices differ by school and model (single class, monthly fee, workshop). We deliberately do not quote fixed numbers here because they change. It is best to compare two or three price lists.'),
     ]),
     (f'Bachata lernen in {city_de}: Welcher Stil passt zu dir?', f'Learning Bachata in {city_en}: which style suits you?', [
       ('h3', 'Bachata Dominicana', 'Bachata Dominicana'),
       ('p', 'Der Stil der Karibik: schnelle Fußarbeit, offene Haltung und viel Spiel mit der Musik. Ideal für alle, die Rhythmus lieben.', 'The Caribbean style: fast footwork, an open hold and lots of play with the music. Ideal if you love rhythm.'),
       ('h3', 'Bachata Sensual', 'Bachata Sensual'),
       ('p', 'In Europa entstanden: enge Verbindung, Wellen und fließende Drehungen. Auf vielen Partys und Festivals der Hauptstil.', 'Developed in Europe: close connection, body waves and flowing turns. The main style at many parties and festivals.'),
       ('h3', 'Bachata Moderna', 'Bachata Moderna'),
       ('p', 'Grundschritt plus Drehungen und Elemente anderer Tänze. Viele Einsteigerkurse beginnen hier, weil der Zugang leicht ist.', 'Basic step plus turns and elements from other dances. Many beginner classes start here because it is easy to get into.'),
     ]),
     (f'Bachata-Party in {city_de}: Socials und Übungsabende', f'Bachata parties in {city_en}: socials and practice nights', [
       ('p', party[0], party[1]),
       ('p', 'Tipp für den ersten Besuch: Komm früh, tanze mit Leuten aus deinem Kurs und frag nach einem Tanz. Die Szene ist offen, und Anfänger sind willkommen. Welche Schulen die meisten Events und Gastlehrer haben, zeigt bald das <a href="rankings.html#' + rank_anchor + '">Ranking</a>.',
             'Tip for your first visit: come early, dance with people from your class and ask for a dance. The scene is open and beginners are welcome. The <a href="rankings.html#' + rank_anchor + '">ranking</a> will soon show which schools run the most events and guest teachers.'),
     ]),
     (f'Bachata-Community in {city_de}: WhatsApp und Tanzreise', f'Bachata community in {city_en}: WhatsApp and dance trip', [
       ('p', f'Tänzer aus {city_de} tauschen sich über Socials, Mitfahrgelegenheiten und Festivals aus. Besuchst du die Stadt nur kurz, zeigt dir die <a href="reisen.html?c={rank_anchor}">Tanzreise-Seite</a> die Schulen mit Zwischenstand, die Community und Lehrer und DJs vor Ort.',
             f'Dancers from {city_en} swap news about socials, rides and festivals. If you are only visiting, the <a href="reisen.html?c={rank_anchor}">dance trip page</a> shows the schools with interim scores, the community and teachers and DJs there.'),
       (('raw', f'<div class="btnrow"><a class="btn btn-gold" href="{B.WHATSAPP[rank_anchor]}" target="_blank" rel="noopener">' + t_wa_de + '</a></div>') if rank_anchor in B.WHATSAPP else
        ('p', f'Für {city_de} gibt es noch keine WhatsApp-Gruppe. Du kennst die Szene und willst eine starten? <a href="mailto:hello@latindanceawards.com?subject=WhatsApp%20{city_de}">Schreib uns</a>, wir helfen dir beim Aufsetzen und verlinken sie hier.',
              f'There is no WhatsApp group for {city_en} yet. Do you know the scene and want to start one? <a href="mailto:hello@latindanceawards.com?subject=WhatsApp%20{city_en}">Email us</a> and we will help you set it up and link it here.')),
     ]),
     (f'So bewerten wir die Bachata-Schulen in {city_de}', f'How we score Bachata schools in {city_en}', [
       ('p', f'Das Ranking für {city_de} erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html#{rank_anchor}">Ranking-Seite</a>. Jede Schule wird nach denselben neun öffentlichen Kriterien mit zusammen 100 Punkten bewertet, unter anderem Google-Bewertung, Festivals, Jahre aktiv, Kursangebot für Einsteiger, Events und Social Media. Plätze sind nicht käuflich.',
             f'The {city_en} ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html#{rank_anchor}">ranking page</a>. Every school is scored on the same nine public factors, 100 points in total, including Google rating, festivals, years active, beginner offer, events and social media. Places cannot be bought.'),
       ('p', f'Du leitest eine Schule in {city_de}? <a href="bewerbung.html">Bewirb dich bis zum 30. November</a> kostenlos, damit wir deine Angaben bestätigen können.',
             f'Do you run a school in {city_en}? <a href="bewerbung.html">Apply for free by November 30</a> so we can confirm your details.'),
     ]),
    ]
    faq = [
     (f'Wo kann ich in {city_de} Bachata lernen?', f'Where can I learn Bachata in {city_en}?', faq_extra[0][0], faq_extra[0][1]),
     (f'Brauche ich einen Partner für einen Bachata-Kurs in {city_de}?', f'Do I need a partner for a Bachata class in {city_en}?',
      'Nein, in der Regel nicht. Viele Schulen wechseln die Partner im Kurs. Frag am besten vor der ersten Stunde nach.', 'No, usually not. Many schools rotate partners in class. It is best to ask before your first class.'),
     ('Welcher Bachata-Stil ist für Anfänger am besten?', 'Which Bachata style is best for beginners?',
      'Die meisten Einsteiger starten mit Bachata Moderna oder Sensual. Wichtig sind der Grundschritt und ein klarer Rhythmus. Der Stil lässt sich später wechseln.', 'Most beginners start with Bachata Moderna or Sensual. What matters is the basic step and a clear rhythm. You can switch styles later.'),
     (f'Gibt es eine Probestunde in {city_de}?', f'Is there a trial class in {city_en}?', faq_extra[1][0], faq_extra[1][1]),
     (f'Wann erscheint das Ranking der besten Bachata-Schulen in {city_de}?', f'When is the ranking of the best Bachata schools in {city_en} published?',
      f'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html#{rank_anchor}">Ranking-Seite</a>.', f'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html#{rank_anchor}">ranking page</a>.'),
     (f'Wo finde ich Bachata-Partys in {city_de}?', f'Where can I find Bachata parties in {city_en}?', faq_extra[2][0], faq_extra[2][1]),
    ]
    guide_page(slug, pref,
      f'Bachata {city_de}: Die besten Bachata-Schulen 2026',
      f'Bachata {city_de}: Schulen, Kurse und Partys im Überblick. So findest du den passenden Bachata-Kurs, mit Stilen, Probestunde und dem Ranking 2026.',
      f'Bachata {city_en}: The best Bachata schools 2026',
      f'Bachata {city_en}: schools, classes and parties at a glance. How to find the right Bachata class, with styles, trial classes and the 2026 ranking.',
      f'Bachata {city_de}', (f'Bachata {city_de} · Awards 2026', f'Bachata {city_en} · Awards 2026'),
      (f'Bachata {city_de}: Die <em class="foil">besten Schulen</em> 2026', f'Bachata {city_en}: the <em class="foil">best schools</em> 2026'),
      (f'Bachata {city_de} im Überblick: Schulen, Kurse und Partys. So findest du den richtigen Bachata-Kurs in {city_de}, vom ersten Probetraining bis zur Tanzparty. Das Ranking erscheint am 20. Dezember 2026.',
       f'Bachata {city_en} at a glance: schools, classes and parties. Find the right Bachata class in {city_en}, from your first trial class to your first dance party. The ranking is published on December 20, 2026.'),
      [('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>'), ('check', 'Unabhängig, <b>nicht käuflich</b>', 'Independent, <b>not for sale</b>')],
      secs, faq, ranking_anchor=rank_anchor, sibling_group='city')

SV = 'https://www.salsavida.com/de/event/germany/'
city_guide('bachata-hamburg', 'bh', 'Hamburg', 'Hamburg', 'hamburg',
  ('Hamburg hat eine lebendige Latin-Szene mit Tanzschulen, Stadtteilzentren und Studios, die Bachata unterrichten. Das Angebot reicht vom klassischen Abendkurs bis zur Kombination aus Kurs und Social.',
   'Hamburg has a lively Latin scene, with dance schools, community centres and studios that teach Bachata. The offer ranges from classic evening classes to a mix of class and social.'),
  [
   {'name': 'A Bailar Hamburg', 'url': 'https://www.abailar-hamburg.de/',
    'de': 'Tanzschule in der Eiffestraße 664b. Auf der Website stehen Bachata Dominicana, Salsa Cubana und Kizomba, Kurse von Anfänger bis Fortgeschrittene, ohne Vorkenntnisse oder Partner. Es gibt zwei Probestunden in verschiedenen Kursen, freie Practica-Abende am Freitag und Partys. Ein neuer Anfängerkurs Bachata Dominicana I startet am 02.11.2026 (montags, 18:00).',
    'en': 'Dance school at Eiffestraße 664b. Its website lists Bachata Dominicana, Salsa Cubana and Kizomba, courses from beginner to advanced, with no experience or partner needed. It offers two trial lessons in different courses, free Friday practice nights and parties. A new beginner course, Bachata Dominicana I, starts on November 2, 2026 (Mondays, 18:00).'},
   {'name': 'ICB Studios HafenCity', 'url': SV + 'hamburg/icb-sunday-at-icb-studios-hafencity/',
    'de': 'Laut Veranstaltungsliste ein Bachata-Kurs mit anschließendem Social, sonntags von 19:00 bis 23:00 Uhr in der HafenCity.',
    'en': 'According to the event listing, a Bachata class followed by a social, on Sundays from 7 pm to 11 pm in HafenCity.'},
   {'name': 'Kulturladen Hamm', 'url': SV + 'hamburg/bachata-classes-at-kulturladen-hamm/',
    'de': 'Stadtteilzentrum mit Bachata-Kursen, laut Liste montags von 18:00 bis 21:30 Uhr.',
    'en': 'Community centre with Bachata courses, listed on Mondays from 6 pm to 9:30 pm.'},
   {'name': 'Kulturklinker Barmbek', 'url': SV + 'hamburg/bachata-classes-at-kulturklinker-barmbek/',
    'de': 'Bachata-Kurse in Barmbek, laut Liste mittwochs zwischen 17:15 und 21:30 Uhr.',
    'en': 'Bachata courses in Barmbek, listed on Wednesdays between 5:15 pm and 9:30 pm.'},
   {'name': 'Mi Pasion Tanzschule', 'url': SV + 'hamburg/salsa-courses-at-mi-pasion-dance-school-hamburg/',
    'de': 'Tanzschule mit Salsa und Bachata, laut Liste montags bis freitags am Abend.',
    'en': 'Dance school with Salsa and Bachata, listed Monday to Friday in the evening.'},
   {'name': 'SalsaHH', 'url': SV + 'hamburg/salsa-latin-courses-at-salsahh-hamburg/',
    'de': 'Salsa- und Latin-Kurse mit Bachata, laut Liste montags bis freitags am Abend.',
    'en': 'Salsa and Latin courses including Bachata, listed Monday to Friday in the evening.'},
   {'name': 'Tango Chocolate', 'url': SV + 'hamburg/bachata-chocolate-at-tango-chocolate/',
    'de': 'Bachata-Kurs mit Social, laut Liste donnerstags ab 19:30 Uhr.',
    'en': 'Bachata class with a social, listed on Thursdays from 7:30 pm.'},
  ],
  ('Mehrere Angebote stammen aus Veranstaltungslisten und nennen weder Level noch Preise, frag dort direkt nach.', 'Several entries come from event listings and give neither levels nor prices, so ask the provider directly.'),
  ('Tanzen lernst du im Kurs, besser wirst du auf der Tanzfläche. In Hamburg verbinden mehrere Anbieter Kurs und Social an einem Abend, etwa sonntags in der HafenCity oder donnerstags bei Tango Chocolate. A Bailar Hamburg nennt auf seiner Website außerdem freie Practica-Abende am Freitag und eigene Partys.',
   'You learn to dance in class, but you improve on the dance floor. In Hamburg several providers combine a class and a social in one evening, for example on Sundays in HafenCity or on Thursdays at Tango Chocolate. A Bailar Hamburg also lists free Friday practice nights and its own parties on its website.'),
  [('In vielen Hamburger Tanzschulen und Stadtteilzentren, zum Beispiel bei A Bailar Hamburg, im Kulturladen Hamm oder im Kulturklinker Barmbek. Oben findest du eine Übersicht mit Links.',
    'In many Hamburg dance schools and community centres, for example A Bailar Hamburg, Kulturladen Hamm or Kulturklinker Barmbek. Above you will find an overview with links.'),
   ('Manche Schulen bieten sie an: A Bailar Hamburg nennt auf der Website zwei Probestunden in verschiedenen Kursen. Prüfe Termine direkt bei der Schule.',
    'Some schools do: A Bailar Hamburg lists two trial lessons in different courses on its website. Check dates directly with the school.'),
   ('Viele Anbieter verbinden Kurs und Social an einem Abend. Schau auf die Websites der Schulen und frag im Kurs nach den nächsten Terminen.',
    'Many providers combine a class and a social in one evening. Check the schools\' websites and ask in class about the next dates.')])

city_guide('bachata-muenchen', 'bm', 'München', 'Munich', 'muenchen',
  ('München hat mehrere Tanzakademien mit eigenen Bachata-Levels, vom Starter-Kurs bis zur Fortgeschrittenen-Stufe. Dazu kommen Salsa-Studios, die Bachata im Wochenplan haben.',
   'Munich has several dance academies with their own Bachata levels, from starter classes up to advanced. There are also Salsa studios with Bachata in their weekly schedule.'),
  [
   {'name': 'Dance MUNICH', 'url': 'https://urbansportsclub.com/de/venues/dance-munich-academy-pinakothek-der-moderne',
    'de': 'Akademie mit zwei Standorten, Glasbrunnen und Pinakothek der Moderne. Die Bachata-Levels heißen Starter, Basic, Level-Up, Improver, Pre-Intermediate, Intermediate und Advanced, mit Kursen donnerstags und freitags. Neue Teilnehmer machen zuerst einen Level Check. Es gibt Social Trainings und eine eigene Anmeldung bei DanceMunich (Angaben über die Urban-Sports-Club-Seite).',
    'en': 'Academy with two locations, Glasbrunnen and Pinakothek der Moderne. The Bachata levels are Starter, Basic, Level-Up, Improver, Pre-Intermediate, Intermediate and Advanced, with classes on Thursdays and Fridays. New participants first take a level check. There are social trainings and a separate registration with DanceMunich (details via the Urban Sports Club page).'},
   {'name': 'Salsa Club Munich', 'url': SV + 'munich/bachata-classes-at-salsa-club-munich/',
    'de': 'Taucht in der Veranstaltungsliste mit einem Bachata-Kurs am Freitagabend auf. Genaue Termine stehen im Eintrag.',
    'en': 'Appears in the event listing with a Friday evening Bachata class. Exact dates are in the listing.'},
   {'name': 'Salsamas Pasing', 'url': SV + 'munich/bachata-classes-at-salsamas-pasing/',
    'de': 'Studio in Pasing mit Bachata-Kursen an mehreren Wochentagen, laut Liste am Abend.',
    'en': 'Studio in Pasing with Bachata classes on several weekdays, listed in the evening.'},
   {'name': 'Salsea Dance Academy', 'url': 'https://salsea.de/academy/',
    'de': 'Akademie in der Hessstraße 48b (Innenhof), etwa drei Minuten zu Fuß von der U2 Theresienstraße. Bachata läuft in Vier-Wochen-Blöcken mit den Levels Starter, Basic, Style, Improver, Intermediate, Advanced und Club. Laut Liste gibt es freitags auch eine Bachata-Party.',
    'en': 'Academy at Hessstraße 48b (courtyard), about a three-minute walk from U2 Theresienstraße. Bachata runs in four-week blocks with the levels Starter, Basic, Style, Improver, Intermediate, Advanced and Club. A Friday Bachata party is also listed.'},
  ],
  ('Einige Angebote stammen aus Veranstaltungslisten. Dort fehlen oft Levels und Preise, frag direkt nach.', 'Some entries come from event listings, which often lack levels and prices, so ask directly.'),
  ('Tanzen lernst du im Kurs, besser wirst du auf der Tanzfläche. In München bieten Akademien eigene Social Trainings an. Dance MUNICH nennt dafür feste Abende unter der Woche am Standort Pinakothek der Moderne, und Salsea führt laut Veranstaltungsliste freitags eine Bachata-Party.',
   'You learn to dance in class, but you improve on the dance floor. In Munich academies offer their own social trainings. Dance MUNICH lists fixed weekday evenings for them at its Pinakothek der Moderne location, and Salsea runs a Friday Bachata party according to the event listing.'),
  [('In Münchner Tanzakademien und Studios, zum Beispiel bei Dance MUNICH, Salsea oder Salsamas in Pasing. Oben findest du eine Übersicht mit Links.',
    'In Munich dance academies and studios, for example Dance MUNICH, Salsea or Salsamas in Pasing. Above you will find an overview with links.'),
   ('Bei Dance MUNICH machen neue Teilnehmer zuerst einen Level Check, der dir den passenden Kurs zuweist. Ob es Probestunden gibt, prüfst du direkt bei der Akademie.',
    'At Dance MUNICH new participants first take a level check, which places you in the right class. Check directly with the academy whether trial classes are offered.'),
   ('Akademien wie Dance MUNICH und Salsea nennen Social Trainings und Partys auf ihren Seiten. Frag im Kurs nach den nächsten Terminen.',
    'Academies like Dance MUNICH and Salsea list social trainings and parties on their pages. Ask in class about the next dates.')])

# ======================================================================
# AUTO CITY GUIDES (cities with 3+ schools; content built from the real candidate data)
# ======================================================================
def _num(x):
    try: return float(str(x).replace('.', '').replace(',', '.').split()[0])
    except Exception: return None

def _auto_city(key, idx):
    sch = sorted([e for e in B.SCH if e['city'] == key], key=lambda e: e['name'].lower())
    cde, cen = B.CITY_NAMES[key]
    n = len(sch)
    def g(e):  # (rating, reviews) or None
        f = e['fx'][0]
        if '★' not in f: return None
        r, v = f.split('★')[0].strip(), f.split('·')[1].strip()
        return r, int(v.replace('.', ''))
    cards = []
    for e in sch:
        gg = g(e)
        ig = e['fx'][1] if len(e['fx']) > 1 and e['fx'][1] != '–' else None
        parts_de, parts_en = [], []
        if gg:
            parts_de.append(f'Google: {gg[0]} Sterne bei {gg[1]} Bewertungen')
            parts_en.append(f'Google: {gg[0].replace(",", ".")} stars from {gg[1]} reviews')
        if ig:
            fol = ig.split('·')[0].strip()
            parts_de.append(f'Instagram: {fol} Follower'); parts_en.append(f'Instagram: {fol} followers')
        d = (', '.join(parts_de) + '. ') if parts_de else 'Zu dieser Schule liegen uns noch keine öffentlichen Bewertungszahlen vor. '
        en_ = (', '.join(parts_en) + '. ') if parts_en else 'We do not have public rating figures for this school yet. '
        cards.append({'name': e['name'], 'url': e['url'],
                      'de': d + f'Bachata steht im Kursangebot. <a href="schools/{e["slug"]}.html">Punkte, Bewertungen und Abstimmung</a>.',
                      'en': en_ + f'Bachata is part of the course offer. <a href="schools/{e["slug"]}.html">Score, reviews and voting</a>.'})
    rated = [(e, g(e)) for e in sch if g(e)]
    top = max(rated, key=lambda x: (_num(x[1][0]), x[1][1])) if rated else None
    most = max(rated, key=lambda x: x[1][1]) if rated else None
    names = [e['name'] for e in sch]
    nl_de = (', '.join(names[:-1]) + ' und ' + names[-1]) if len(names) > 1 else names[0]
    nl_en = (', '.join(names[:-1]) + ' and ' + names[-1]) if len(names) > 1 else names[0]
    intro_de = f'In {cde} haben wir {n} Anbieter mit Bachata-Kursen erfasst: {nl_de}.'
    intro_en = f'In {cen} we have listed {n} {'provider' if n == 1 else 'providers'} with Bachata classes: {nl_en}.'
    if top:
        intro_de += f' Die beste Google-Bewertung unter ihnen hat {top[0]["name"]} mit {top[1][0]} Sternen bei {top[1][1]} Bewertungen (Stand Oktober 2026).'
        intro_en += f' The best Google rating among them belongs to {top[0]["name"]} with {top[1][0].replace(",", ".")} stars from {top[1][1]} reviews (as of October 2026).'
    if most and most[0] is not (top[0] if top else None):
        intro_de += f' Die meisten Bewertungen sammelt {most[0]["name"]} mit {most[1][1]}.'
        intro_en += f' {most[0]["name"]} has the most reviews with {most[1][1]}.'
    note = (f'Die Liste umfasst {n} Schulen in {cde}. Weitere Anbieter nehmen wir nach der Bewerbung auf.' if n > 1 else f'Die Liste umfasst bisher eine Schule in {cde}. Weitere Anbieter nehmen wir nach der Bewerbung auf.',
            f'The list covers {n} schools in {cde}. We add further providers after they apply.' if n > 1 else f'The list covers one school in {cde} so far. We add further providers after they apply.')
    party = (f'Socials und Übungsabende laufen in {cde} meist über die Schulen selbst, zum Beispiel bei {nl_de}. Die aktuellen Termine stehen auf deren Websites und in den Social-Media-Kanälen. Größere Veranstaltungen findest du zusätzlich in den <a href="{SV}" rel="noopener" target="_blank">Veranstaltungslisten von Salsa Vida</a>.',
             f'Socials and practice nights in {cen} mostly run through the schools themselves, for example at {nl_en}. Current dates are on their websites and social media channels. You can also find larger events in the <a href="{SV}" rel="noopener" target="_blank">Salsa Vida event listings</a>.')
    faq_extra = [
      (f'In {cde} listen wir {n} Anbieter mit Bachata-Kursen: {nl_de}. Die Auswahl bildet den Stand vom Oktober 2026 ab. Das Ranking mit Punkten erscheint am 20. Dezember 2026.',
       f'In {cen} we list {n} {'provider' if n == 1 else 'providers'} with Bachata classes: {nl_en}. The selection reflects the state in October 2026. The ranking with scores is published on December 20, 2026.'),
      ('Das entscheidet jede Schule selbst. Frag vor der Anmeldung nach einer Probestunde oder einem Einsteigertermin, die Kontaktdaten stehen auf der jeweiligen Website.',
       'Each school decides this itself. Ask for a trial class or a beginner date before you sign up; the contact details are on each school\'s website.'),
      (f'Frag bei den Schulen in {cde} nach Socials und Übungsabenden und schau in die Veranstaltungslisten von Salsa Vida. Dort stehen auch Festivals in der Region.',
       f'Ask the schools in {cen} about socials and practice nights, and check the Salsa Vida event listings, which also include festivals in the region.'),
    ]
    slug = 'bachata-' + key
    city_guide(slug, f'cg{idx}', cde, cen, key, (intro_de, intro_en), cards, note, party, faq_extra)
    return slug, cde, cen

AUTO_CITIES = [k for k, c in sorted(((k, sum(1 for e in B.SCH if e['city'] == k)) for k in {e['city'] for e in B.SCH}), key=lambda x: (-x[1], x[0])) if (c >= 3 or k in ('kassel', 'hannover', 'braunschweig', 'heidelberg', 'dortmund', 'kiel', 'bochum', 'wuerzburg', 'muenster', 'augsburg', 'regensburg', 'mannheim')) and k not in ('berlin', 'hamburg', 'muenchen')]
if 'leipzig' not in AUTO_CITIES and any(e['city'] == 'leipzig' for e in B.SCH): AUTO_CITIES.append('leipzig')  # 2 schools, still a keyword page (bachata leipzig, 110/mo)
for _i, _k in enumerate(AUTO_CITIES):
    _auto_city(_k, _i)

# ======================================================================
# BACHATA FESTIVALS DEUTSCHLAND (keyword page + festival listing)
# ======================================================================
FV = 'https://www.salsavida.com/event/germany/'
fest_cards = [
 {'name': 'The Bachata Flow Generation, Frankfurt', 'url': FV + 'frankfurt/the-bachata-flow-generation-frankfurt/',
  'de': '<strong>30. Oktober bis 1. November 2026.</strong> Bachata-Festival in Frankfurt laut Veranstaltungsliste von Salsa Vida.',
  'en': '<strong>October 30 to November 1, 2026.</strong> Bachata festival in Frankfurt according to the Salsa Vida event listing.'},
 {'name': 'Conexión Gran Bachata Latin Festival, Frankfurt', 'url': FV + 'frankfurt/conexion-gran-bachata-latin-festival/',
  'de': '<strong>6. bis 8. November 2026.</strong> Bachata- und Latin-Festival in Frankfurt, gelistet bei Salsa Vida.',
  'en': '<strong>November 6 to 8, 2026.</strong> Bachata and Latin festival in Frankfurt, listed on Salsa Vida.'},
 {'name': 'Frankfurt Bachata Festival', 'url': FV + 'frankfurt/frankfurt-bachata-festival/',
  'de': '<strong>26. bis 29. November 2026.</strong> Viertägiges Bachata-Festival in Frankfurt laut Veranstaltungsliste.',
  'en': '<strong>November 26 to 29, 2026.</strong> Four-day Bachata festival in Frankfurt according to the event listing.'},
 {'name': 'Bachata Zouk Royals Congress (5. Ausgabe), Freiburg', 'url': FV + 'freiburg/bachata-zouk-royals-congress-fifth-edition/',
  'de': '<strong>11. bis 13. Dezember 2026.</strong> Kongress in Freiburg, der neben Bachata auch Zouk umfasst. Fünfte Ausgabe.',
  'en': '<strong>December 11 to 13, 2026.</strong> Congress in Freiburg that covers Zouk as well as Bachata. Fifth edition.'},
 {'name': 'Bachatation Festival, Karlsruhe', 'url': 'https://www.bachatation.de/',
  'de': '<strong>25. bis 28. Februar 2027</strong> bei Son Latino Studios. Laut Veranstalter über 40 Stunden Workshops mit internationalen Trainern, vier Partys (Neon, Pink, Gala in Schwarz-Weiß, Casual), Tages-Socials und ein Jack-&-Jill-Wettbewerb.',
  'en': '<strong>February 25 to 28, 2027</strong> at Son Latino Studios. According to the organiser, more than 40 hours of workshops with international trainers, four parties (Neon, Pink, black-and-white Gala, Casual), day socials and a Jack &amp; Jill competition.'},
 {'name': 'Bachata Festival Germany, Stuttgart', 'url': FV + 'stuttgart/bachata-festival-stuttgart/',
  'de': '<strong>7. bis 11. April 2027.</strong> Mehrtägiges Bachata-Festival in Stuttgart, gelistet bei Salsa Vida.',
  'en': '<strong>April 7 to 11, 2027.</strong> Multi-day Bachata festival in Stuttgart, listed on Salsa Vida.'},
 {'name': 'Pure Bachata Summer Festival, Köln', 'url': FV + 'cologne/pure-bachata-festival/',
  'de': '<strong>30. April bis 2. Mai 2027.</strong> Bachata-Festival in Köln laut Veranstaltungsliste.',
  'en': '<strong>April 30 to May 2, 2027.</strong> Bachata festival in Cologne according to the event listing.'},
 {'name': 'Salsa-Bachata-Kizomba Festival, Augsburg', 'url': FV + 'augsburg/salsafestival-augsburg/',
  'de': '<strong>30. April bis 2. Mai 2027.</strong> Festival in Augsburg mit Salsa, Bachata und Kizomba.',
  'en': '<strong>April 30 to May 2, 2027.</strong> Festival in Augsburg with Salsa, Bachata and Kizomba.'},
 {'name': 'DJ Got Us Fallin in Love Bachata, Stuttgart', 'url': FV + 'stuttgart/dj-got-us-fallin-in-love-bachata/',
  'de': '<strong>21. bis 23. Mai 2027.</strong> Bachata-Event in Stuttgart, gelistet bei Salsa Vida.',
  'en': '<strong>May 21 to 23, 2027.</strong> Bachata event in Stuttgart, listed on Salsa Vida.'},
]

fest_extra = {
 'dortmund': {'name': 'La Klave Festival, Dortmund', 'url': 'https://www.salsavida.com/event/germany/dortmund/la-klave-festival/', 'de': '<strong>13. bis 15. November 2026.</strong> Latin-Festival in Dortmund. Der Stil-Schwerpunkt steht in der Veranstaltungsliste nicht, prüfe das Programm auf Bachata-Workshops.', 'en': '<strong>November 13 to 15, 2026.</strong> Latin festival in Dortmund. The listing does not state the style focus, so check the programme for Bachata workshops.'},
 'hannover': {'name': 'Creme de la Creme Deluxe Edition, Hannover', 'url': 'https://www.salsavida.com/event/germany/lower-saxony/hannover/creme-de-la-creme-deluxe-edition/', 'de': '<strong>20. bis 22. November 2026.</strong> Latin-Tanzevent in Hannover. Prüfe im Programm, welche Bachata-Angebote dabei sind.', 'en': '<strong>November 20 to 22, 2026.</strong> Latin dance event in Hannover. Check the programme for the Bachata offering.'},
 'stuttgart_dec': {'name': 'Latin Festival Stuttgart', 'url': 'https://www.salsavida.com/event/germany/stuttgart/latin-festival-stuttgart/', 'de': '<strong>3. bis 7. Dezember 2026.</strong> Fünftägiges Latin-Festival in Stuttgart.', 'en': '<strong>December 3 to 7, 2026.</strong> Five-day Latin festival in Stuttgart.'},
 'dus': {'name': 'Confuego Xmas Gala, Düsseldorf', 'url': 'https://www.salsavida.com/event/germany/dusseldorf/confuego-xmas-gala-2025/', 'de': '<strong>11. bis 13. Dezember 2026.</strong> Latin-Weihnachtsgala in Düsseldorf. Der Stil-Schwerpunkt ist in der Liste nicht angegeben.', 'en': '<strong>December 11 to 13, 2026.</strong> Latin Christmas gala in Düsseldorf. The listing does not state the style focus.'},
 'wue': {'name': 'Latin Festival Würzburg', 'url': 'https://www.salsavida.com/event/germany/wurzburg/latin-festival-wurzburg/', 'de': '<strong>22. bis 24. Januar 2027.</strong> Latin-Festival in Würzburg.', 'en': '<strong>January 22 to 24, 2027.</strong> Latin festival in Würzburg.'},
 'rust': {'name': 'Euro Dance Festival, Rust (Europa-Park)', 'url': 'https://www.salsavida.com/event/germany/rust/euro-dance-festival-rust-edition/', 'de': '<strong>9. bis 14. Februar 2027.</strong> Mehrtägiges Tanzfestival in Rust bei Freiburg.', 'en': '<strong>February 9 to 14, 2027.</strong> Multi-day dance festival in Rust near Freiburg.'},
 'boe': {'name': 'BachaKizz Sensation, Böblingen', 'url': 'https://www.bachamap.com/festivals/germany/bachakizz-sensation-2027-all-in-one-bachata-kizomba-festival-d24751b3', 'de': '<strong>17. bis 21. Februar 2027.</strong> All-in-one-Festival für Bachata und Kizomba in Böblingen bei Stuttgart.', 'en': '<strong>February 17 to 21, 2027.</strong> All-in-one festival for Bachata and Kizomba in Böblingen near Stuttgart.'},
 'ham': {'name': 'BIG3 Festival, Hamburg', 'url': 'https://www.salsavida.com/event/germany/hamburg/big3-festival-hamburg/', 'de': '<strong>19. bis 21. Februar 2027.</strong> Latin-Festival in Hamburg.', 'en': '<strong>February 19 to 21, 2027.</strong> Latin festival in Hamburg.'},
 'bsf': {'name': 'Berlin Salsa Festival „Fiesta Elegante“', 'url': 'https://www.salsavida.com/event/germany/berlin/berlin-salsa-festival/', 'de': '<strong>2. bis 5. April 2027.</strong> Salsa-Festival in Berlin. Bachata gehört bei vielen Berliner Festivals zum Rahmenprogramm, prüfe das Programm.', 'en': '<strong>April 2 to 5, 2027.</strong> Salsa festival in Berlin. Bachata is part of the programme at many Berlin festivals, so check the programme.'},
 'xpl': {'name': 'Xplosion Ritmo Berlin Festival', 'url': 'https://www.salsavida.com/event/germany/berlin/xplosion-ritmo-berlin-festival/', 'de': '<strong>13. bis 16. Mai 2027</strong> laut Salsa Vida (andere Listen nennen den 14. bis 16. Mai). Festival in Berlin, 5. Jubiläum.', 'en': '<strong>May 13 to 16, 2027</strong> according to Salsa Vida (other listings give May 14 to 16). Festival in Berlin, 5th anniversary.'},
 'trier': {'name': 'Trier Old Town Festival', 'url': 'https://www.salsavida.com/event/germany/trier/trier-old-town-festival/', 'de': '<strong>25. bis 27. Juni 2027.</strong> Tanzfestival in der Trierer Altstadt.', 'en': "<strong>June 25 to 27, 2027.</strong> Dance festival in Trier's old town."},
 'frb': {'name': 'Euro Dance Festival, Freiburg', 'url': 'https://www.salsavida.com/event/germany/freiburg/euro-dance-festival-freiburg-edition/', 'de': '<strong>29. Juli bis 1. August 2027.</strong> Sommer-Ausgabe des Euro Dance Festivals in Freiburg.', 'en': '<strong>July 29 to August 1, 2027.</strong> Summer edition of the Euro Dance Festival in Freiburg.'},
 'dusfest': {'name': 'Düsseldorf Bachata Fest', 'url': 'https://dusseldorf.bachata-fest.com/', 'de': '<strong>8. bis 11. Januar 2027.</strong> Bachata-Festival in Düsseldorf laut Website des Veranstalters.', 'en': "<strong>January 8 to 11, 2027.</strong> Bachata festival in Düsseldorf according to the organiser's website."},
 'lvl': {'name': 'Bachata Level Up 4', 'url': 'https://www.goandance.com/en/event/9879/bachata-level-up-4', 'de': '<strong>19. bis 21. Februar 2027.</strong> Bachata-Wochenende in Sachsen laut Goandance. Die Stadt nennt die Liste nicht.', 'en': '<strong>February 19 to 21, 2027.</strong> Bachata weekend in Saxony according to Goandance. The listing does not name the city.'},
 'bzf': {'name': 'Bachazouk Festival Germany', 'url': 'https://www.goandance.com/en/event/9603/bachazouk-festival-germany', 'de': '<strong>5. bis 7. März 2027.</strong> Festival für Bachata und Zouk in Baden-Württemberg laut Goandance.', 'en': '<strong>March 5 to 7, 2027.</strong> Bachata and Zouk festival in Baden-Württemberg according to Goandance.'},
 'bof': {'name': 'Bachata on Fire Festival am Bodensee, Konstanz (2. Ausgabe)', 'url': 'https://www.goandance.com/en/event/9581/bachata-on-fire-festival-am-bodensee-2-edition', 'de': '<strong>19. bis 21. März 2027.</strong> Bachata-Festival am Bodensee in Konstanz, zweite Ausgabe.', 'en': '<strong>March 19 to 21, 2027.</strong> Bachata festival at Lake Constance in Konstanz, second edition.'},
 'bzw': {'name': 'Bachazouk Wave', 'url': 'https://www.goandance.com/en/event/9468/bachazouk-wave', 'de': '<strong>2. bis 4. April 2027.</strong> Bachata-und-Zouk-Event in Baden-Württemberg laut Goandance.', 'en': '<strong>April 2 to 4, 2027.</strong> Bachata and Zouk event in Baden-Württemberg according to Goandance.'},
 'fbu': {'name': 'Frankfurt Bachata United', 'url': 'https://www.goandance.com/en/event/9636/frankfurt-bachata-united', 'de': '<strong>9. bis 11. April 2027.</strong> Bachata-Festival in Frankfurt laut Goandance.', 'en': '<strong>April 9 to 11, 2027.</strong> Bachata festival in Frankfurt according to Goandance.'},
 'bss': {'name': 'Bachatasummerfestival Stuttgart', 'url': 'https://www.goandance.com/en/event/10073/bachatasummerfestival-stuttgart-2027', 'de': '<strong>25. bis 28. Juni 2027.</strong> Bachata-Sommerfestival in Stuttgart.', 'en': '<strong>June 25 to 28, 2027.</strong> Bachata summer festival in Stuttgart.'},
 'vib': {'name': 'Vibras Bachata Summer Festival', 'url': 'https://www.goandance.com/en/event/9925/vibras-bachata-summer-festival-2027', 'de': '<strong>27. bis 29. August 2027.</strong> Bachata-Sommerfestival in Hessen laut Goandance.', 'en': '<strong>August 27 to 29, 2027.</strong> Bachata summer festival in Hesse according to Goandance.'},
 'ext': {'name': 'Extravadanza Bachata Congress', 'url': 'https://www.goandance.com/en/event/10050/extravadanza-bachata-congress-2027', 'de': '<strong>17. bis 21. September 2027.</strong> Bachata-Kongress in Hessen laut Goandance.', 'en': '<strong>September 17 to 21, 2027.</strong> Bachata congress in Hesse according to Goandance.'},
 'bbf': {'name': 'Berlin Bachata Festival (Bachata Explosion)', 'url': 'https://bachataexplosion.com/', 'de': '<strong>22. bis 24. Oktober 2027</strong> im MOA Berlin. Tickets im Early-Bird-Verkauf.', 'en': '<strong>October 22 to 24, 2027</strong> at MOA Berlin. Early-bird tickets on sale.'},
 'mun': {'name': 'Munich Bachata Fest', 'url': 'https://bachata-fest.com/', 'de': '<strong>16. bis 19. Dezember 2027.</strong> Bachata-Festival in München laut Website des Veranstalters.', 'en': "<strong>December 16 to 19, 2027.</strong> Bachata festival in Munich according to the organiser's website."},
}
_order = ['The Bachata Flow', 'Conexión', 'dortmund', 'hannover', 'Frankfurt Bachata Festival', 'stuttgart_dec', 'Bachata Zouk', 'dus', 'dusfest', 'wue', 'rust', 'boe', 'ham', 'lvl', 'Bachatation', 'bzf', 'bof', 'bsf', 'bzw', 'Bachata Festival Germany', 'fbu', 'Pure', 'Salsa-Bachata', 'xpl', 'DJ Got', 'trier', 'bss', 'frb', 'vib', 'ext', 'bbf', 'mun']
_base = list(fest_cards)
fest_cards = []
for _k in _order:
    if _k in fest_extra: fest_cards.append(fest_extra[_k])
    else: fest_cards.append(next(c for c in _base if c["name"].startswith(_k)))
assert len(fest_cards) == 32

fest_sections = [
 ('Bachata-Festivals in Deutschland: Was dich erwartet', 'Bachata festivals in Germany: what to expect', [
   ('p', 'Ein Bachata-Festival ist ein Wochenende, an dem sich die Szene trifft: Workshops tagsüber, Partys am Abend und internationale Tänzer und DJs. Für Einsteiger ist es die beste Gelegenheit, in kurzer Zeit viele Stile zu sehen und neue Leute kennenzulernen. Fortgeschrittene nutzen die Workshops, um bei Trainern zu lernen, die sonst nicht in der eigenen Stadt unterrichten.',
         'A Bachata festival is a weekend where the scene comes together: workshops during the day, parties in the evening, and international dancers and DJs. For beginners it is the best chance to see many styles in a short time and meet new people. Advanced dancers use the workshops to learn from trainers who do not usually teach in their own city.'),
   ('p', 'Die meisten Festivals mischen mehrere Elemente. Das Bachatation Festival in Karlsruhe nennt auf seiner Website zum Beispiel mehr als 40 Stunden Workshops auf verschiedenen Levels, vier Partys, Tages-Socials und einen Jack-&-Jill-Wettbewerb. Ein Jack & Jill ist ein Wettbewerb, bei dem die Paare ausgelost werden.',
         'Most festivals mix several elements. The Bachatation Festival in Karlsruhe, for example, lists on its website more than 40 hours of workshops at different levels, four parties, day socials and a Jack &amp; Jill competition. A Jack &amp; Jill is a competition in which the partners are drawn at random.'),
   ('p', 'Auf dieser Seite sammeln wir die kommenden Bachata- und Latin-Festivals in Deutschland nach Datum. Reine Salsa-Kongresse lassen wir weg, bei gemischten Latin-Festivals steht dabei, wenn der Bachata-Anteil nicht bekannt ist. Die Angaben stammen von den Websites der Veranstalter und aus der Veranstaltungsliste von Salsa Vida. Termine und Programm können sich ändern, prüfe sie deshalb immer beim Veranstalter, bevor du buchst.',
         'On this page we collect the upcoming Bachata and Latin festivals in Germany by date. Pure salsa congresses are left out, and for mixed Latin festivals we note when the Bachata share is not known. The details come from the organisers\' websites and from the Salsa Vida event listing. Dates and programmes can change, so always check with the organiser before you book.'),
 ]),
 ('Kommende Bachata-Festivals 2026 und 2027 nach Datum', 'Upcoming Bachata festivals in 2026 and 2027 by date', [
   ('p', 'Die Reihenfolge ist chronologisch und keine Wertung. Die Links führen zur Eventseite oder zur Website des Veranstalters.',
         'The order is chronological and not a rating. The links lead to the event page or the organiser\'s website.'),
   ('cards', fest_cards),
   ('p', 'Dein Festival fehlt? Schreib uns an <a href="mailto:hello@latindanceawards.com?subject=Festival%20eintragen">hello@latindanceawards.com</a> mit Name, Ort, Datum und Link. Der Standardeintrag ist kostenlos.',
         'Is your festival missing? Email us at <a href="mailto:hello@latindanceawards.com?subject=List%20my%20festival">hello@latindanceawards.com</a> with the name, place, date and link. The standard listing is free.'),
 ]),
 ('Welches Bachata-Festival passt zu dir?', 'Which Bachata festival suits you?', [
   ('p', 'Die Festivals unterscheiden sich in Größe, Stil und Niveau. Diese Fragen helfen bei der Auswahl:', 'Festivals differ in size, style and level. These questions help you choose:'),
   ('ul', [
     ('<strong>Level:</strong> Schau, ob es Workshops für dein Niveau gibt. Viele Festivals trennen Einsteiger, Mittelstufe und Fortgeschrittene.', '<strong>Level:</strong> check whether there are workshops for your level. Many festivals separate beginners, intermediate and advanced.'),
     ('<strong>Stil:</strong> Manche setzen auf Sensual, andere auf Dominicana oder mischen Bachata mit Salsa, Kizomba oder Zouk. Das Programm zeigt den Schwerpunkt.', '<strong>Style:</strong> some focus on Sensual, others on Dominicana or mix Bachata with Salsa, Kizomba or Zouk. The programme shows the focus.'),
     ('<strong>Dauer und Preis:</strong> Ein Fullpass gilt für alle Workshops und Partys, ein Partypass nur für die Abende. Vergleiche die Pakete auf der Website des Veranstalters.', '<strong>Length and price:</strong> a full pass covers all workshops and parties, a party pass only the evenings. Compare the packages on the organiser\'s website.'),
     ('<strong>Anreise:</strong> Frankfurt, Stuttgart und Köln liegen gut im Netz. Plane Hotel und Zug früh, weil die Preise am Festivalwochenende steigen.', '<strong>Travel:</strong> Frankfurt, Stuttgart and Cologne are well connected. Plan the hotel and train early, as prices rise on festival weekends.'),
   ]),
   ('p', 'Tipp für das erste Festival: Komm mit etwas Grundlagenwissen, besuche zuerst die Einsteiger-Workshops und geh abends auf die Partys. Dort lernst du am meisten.',
         'Tip for your first festival: arrive with some basics, start with the beginner workshops and go to the parties in the evening. That is where you learn the most.'),
 ]),
 ('Für Veranstalter: Festival eintragen und hervorheben', 'For organisers: list and promote your festival', [
   ('p', 'Du organisierst ein Bachata-Festival, einen Kongress oder ein Wochenende mit Workshops in Deutschland? Dann trag es hier ein, damit Tänzer es finden.',
         'Do you organise a Bachata festival, a congress or a workshop weekend in Germany? List it here so dancers can find it.'),
   ('ul', [
     ('<strong>Standardeintrag, kostenlos:</strong> Name, Ort, Datum und Link in der Liste oben.', '<strong>Standard listing, free:</strong> name, place, date and link in the list above.'),
     ('<strong>Hervorgehobener Eintrag, 29 € pro Festival:</strong> Platz am Anfang der Liste, farbige Hervorhebung mit Hinweis „Anzeige“, Logo, Kurztext und Ticketlink. Gilt bis zum Festivaltermin.', '<strong>Featured listing, €29 per festival:</strong> a place at the top of the list, colour highlight marked "Anzeige" (advertisement), logo, short text and ticket link. Runs until the festival date.'),
   ]),
   ('p', 'Bezahlte Einträge sind als Anzeige gekennzeichnet und haben keinen Einfluss auf das Ranking der Schulen. Anfragen an <a href="mailto:hello@latindanceawards.com?subject=Hervorgehobener%20Festival-Eintrag">hello@latindanceawards.com</a>.',
         'Paid listings are marked as advertisements and have no influence on the school ranking. Enquiries to <a href="mailto:hello@latindanceawards.com?subject=Featured%20festival%20listing">hello@latindanceawards.com</a>.'),
 ]),
 ('Festivals und das Ranking der Bachata-Schulen', 'Festivals and the Bachata school ranking', [
   ('p', 'Auftritte der Lehrer auf Festivals und Kongressen zählen beim Ranking der Bachata-Schulen mit: Für dieses Kriterium vergeben wir bis zu 15 von 100 Punkten. Schulen, deren Lehrer 2025 oder 2026 auf Festivals unterrichtet haben, können das bei der <a href="bewerbung.html">kostenlosen Bewerbung</a> angeben. Das Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>.',
         'Teachers\' appearances at festivals and congresses count towards the Bachata school ranking: for this factor we award up to 15 of 100 points. Schools whose teachers taught at festivals in 2025 or 2026 can state this in the <a href="bewerbung.html">free application</a>. The ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>.'),
 ]),
]
fest_faq = [
 ('Welche Bachata-Festivals gibt es in Deutschland 2026 und 2027?', 'Which Bachata festivals are there in Germany in 2026 and 2027?',
  'Auf dieser Seite findest du 32 Festivals, unter anderem in Frankfurt, Stuttgart, Berlin, Hamburg, Köln, Freiburg und Karlsruhe, sortiert nach Datum. Das nächste ist The Bachata Flow Generation in Frankfurt vom 30. Oktober bis 1. November 2026.',
  'This page lists 32 festivals, including Frankfurt, Stuttgart, Berlin, Hamburg, Cologne, Freiburg and Karlsruhe, sorted by date. The next one is The Bachata Flow Generation in Frankfurt from October 30 to November 1, 2026.'),
 ('Wann ist das Bachatation Festival?', 'When is the Bachatation Festival?',
  'Die Website nennt für die Ausgabe 2027 den Zeitraum 25. bis 28. Februar in Karlsruhe bei Son Latino Studios. Das Workshop-Programm war zuletzt noch nicht veröffentlicht.',
  'For the 2027 edition the website gives February 25 to 28 in Karlsruhe at Son Latino Studios. The workshop programme had not been published at the last check.'),
 ('Brauche ich Erfahrung für ein Bachata-Festival?', 'Do I need experience for a Bachata festival?',
  'Nein. Viele Festivals bieten Workshops für Einsteiger an, und die Partys stehen allen offen. Prüfe im Programm, ob dein Level dabei ist.',
  'No. Many festivals offer beginner workshops, and the parties are open to everyone. Check the programme to see whether your level is included.'),
 ('Wie kann ich mein Festival eintragen?', 'How can I list my festival?',
  'Schreib an hello@latindanceawards.com mit Name, Ort, Datum und Link. Der Standardeintrag ist kostenlos, ein hervorgehobener Eintrag kostet 29 Euro und ist als Anzeige gekennzeichnet.',
  'Email hello@latindanceawards.com with the name, place, date and link. The standard listing is free, a featured listing costs €29 and is marked as an advertisement.'),
 ('Können Festivals das Ranking der Schulen beeinflussen?', 'Can festivals influence the school ranking?',
  'Nein, Plätze sind nicht käuflich. Festival-Auftritte der Lehrer zählen als ein Kriterium von neun, bezahlte Festival-Einträge haben keinen Einfluss.',
  'No, places cannot be bought. Teachers\' festival appearances are one factor of nine, and paid festival listings have no influence.'),
]
(guide_page if SHOW_FESTIVALS else (lambda *a, **k: None))('bachata-festivals-deutschland', 'bf',
  'Bachata Festival Deutschland 2026/2027: Termine im Überblick',
  'Bachata Festival Deutschland: kommende Festivals 2026 und 2027 nach Datum, mit Orten, Programm und Links. Dazu Tipps für dein erstes Festival.',
  'Bachata festival Germany 2026/2027: dates at a glance',
  'Bachata festivals in Germany: upcoming festivals in 2026 and 2027 by date, with places, programme and links, plus tips for your first festival.',
  'Bachata-Festivals Deutschland', ('Bachata-Festivals · 2026/2027', 'Bachata festivals · 2026/2027'),
  ('Bachata Festival Deutschland: <em class="foil">Termine</em> 2026/2027', 'Bachata festivals in Germany: <em class="foil">dates</em> 2026/2027'),
  ('Alle kommenden Bachata-Festivals in Deutschland nach Datum, mit Ort, Programm und Link. Dazu Tipps, welches Festival zu dir passt, und die Möglichkeit für Veranstalter, ihr Festival einzutragen.',
   'All upcoming Bachata festivals in Germany by date, with place, programme and link. Plus tips on which festival suits you, and a way for organisers to list their festival.'),
  [('cal', '<b>32 Festivals</b> bis Dezember 2027', '<b>32 festivals</b> until December 2027'), ('free', 'Eintrag <b>kostenlos</b>', 'Listing <b>free</b>'), ('check', 'Termine <b>vom Veranstalter prüfen</b>', 'Check dates <b>with the organiser</b>')],
  fest_sections, fest_faq, sibling_group='topic')


# ======================================================================
# BACHATA TANZEN (guide) and BACHATA GRUNDSCHRITT (guide)
# ======================================================================
CITY_LINKS_DE = ('<a href="bachata-berlin.html">Berlin</a>, <a href="bachata-hamburg.html">Hamburg</a>, <a href="bachata-muenchen.html">München</a>, '
                 '<a href="bachata-koeln.html">Köln</a>, <a href="bachata-frankfurt.html">Frankfurt</a> und <a href="bachata-duesseldorf.html">Düsseldorf</a>')
CITY_LINKS_EN = ('<a href="bachata-berlin.html">Berlin</a>, <a href="bachata-hamburg.html">Hamburg</a>, <a href="bachata-muenchen.html">Munich</a>, '
                 '<a href="bachata-koeln.html">Cologne</a>, <a href="bachata-frankfurt.html">Frankfurt</a> and <a href="bachata-duesseldorf.html">Düsseldorf</a>')
UNESCO = '<a href="https://en.wikipedia.org/wiki/Bachata_(music)" rel="noopener">Wikipedia</a>'

tanzen_sections = [
 ('Bachata tanzen: Was ist das eigentlich?', 'Dancing Bachata: what is it, exactly?', [
   ('p', f'Bachata tanzen heißt, zu Gitarrenmusik aus der Dominikanischen Republik einen Paartanz mit klarem Vier-Schritt-Rhythmus zu tanzen. Bachata entstand dort im 20. Jahrhundert, Musik und Tanz gehören zusammen, und die Tradition steht auf der UNESCO-Liste des immateriellen Kulturerbes ({WIKI}). Typisch für die Musik sind Gitarren, Bass, Bongos und Güira, also ein weicher, melodischer Klang, der sich gut zum Einstieg eignet.',
         f'Dancing Bachata means dancing a couple dance with a clear four-beat rhythm to guitar music from the Dominican Republic. Bachata developed there in the 20th century, music and dance belong together, and the tradition is on the UNESCO list of intangible cultural heritage ({WIKI_EN}). The music is typically built on guitars, bass, bongos and güira, a soft, melodic sound that suits beginners well.'),
   ('p', 'Heute wird Bachata weltweit getanzt, und in Europa hat sich daraus eine eigene Szene mit Schulen, Socials und Festivals entwickelt. Wer Bachata tanzen lernen will, findet in Deutschland in fast jeder größeren Stadt Kurse. Auf dieser Seite bekommst du den Überblick: Stile, erste Schritte, Kurssuche, Übungstipps und Fragen, die Einsteiger oft stellen.',
         'Today Bachata is danced all over the world, and in Europe it has grown into its own scene with schools, socials and festivals. If you want to learn to dance Bachata, you will find classes in almost every larger city in Germany. This page gives you the overview: styles, first steps, finding a class, practice tips and questions beginners often ask.'),
 ]),
 ('Bachata tanzen lernen: Die drei Stile im Vergleich', 'Learning to dance Bachata: the three styles compared', [
   ('p', 'Bevor du einen Kurs buchst, lohnt sich ein Blick auf die Stile. Die Schulen nennen sie unterschiedlich, aber meist begegnen dir diese drei:',
         'Before you book a class it helps to know the styles. Schools name them differently, but you will usually meet these three:'),
   ('h3', 'Bachata Dominicana', 'Bachata Dominicana'),
   ('p', 'Der ursprüngliche Stil: kleine, schnelle Schritte, offene Haltung, viel Spiel mit dem Rhythmus. Wer die Musik liebt und gern mit den Füßen spielt, ist hier richtig.',
         'The original style: small, quick steps, an open hold and lots of play with the rhythm. If you love the music and like playing with your feet, this is for you.'),
   ('h3', 'Bachata Moderna', 'Bachata Moderna'),
   ('p', 'Der Grundschritt wird mit Drehungen und Elementen anderer Tänze erweitert. Viele Einsteigerkurse beginnen hier, weil der Zugang leicht ist und du schnell auf Partys tanzen kannst.',
         'The basic step is extended with turns and elements from other dances. Many beginner classes start here because it is easy to get into and you can soon dance at parties.'),
   ('h3', 'Bachata Sensual', 'Bachata Sensual'),
   ('p', 'In Europa entstanden: enge Verbindung, Körperwellen und fließende Drehungen. Auf vielen Socials und Festivals der Hauptstil. Er verlangt Führung und Körperspannung, die du Schritt für Schritt aufbaust.',
         'Developed in Europe: close connection, body waves and flowing turns. The main style at many socials and festivals. It asks for lead, follow and body tension, which you build up step by step.'),
 ]),
 ('Bachata Anfänger: Die ersten Schritte', 'Bachata for beginners: your first steps', [
   ('p', 'Als Anfänger brauchst du weder Vorkenntnisse noch einen Partner. Diese Grundlagen kommen in jedem Einsteigerkurs vor:',
         'As a beginner you need neither experience nor a partner. These basics come up in every beginner class:'),
   ('ul', [
     ('<strong>Grundschritt:</strong> Drei Schritte zur Seite und ein Tap auf Zählzeit vier, dann zurück. Die ausführliche Anleitung steht im Ratgeber zum <a href="bachata-grundschritt.html">Bachata-Grundschritt</a>.', '<strong>Basic step:</strong> three steps to the side and a tap on count four, then back. The full walkthrough is in the guide to the <a href="bachata-grundschritt.html">Bachata basic step</a>.'),
     ('<strong>Musik hören:</strong> Zähle beim Hören mit, 1-2-3-4, und achte auf die Betonung der Zählzeit vier. Das schult dein Timing, bevor du dich bewegst.', '<strong>Listening:</strong> count along, 1-2-3-4, and notice the accent on count four. It trains your timing before you move.'),
     ('<strong>Haltung:</strong> Locker in den Knien, Oberkörper ruhig, Gewicht über den Fußballen. Das gilt für alle Stile.', '<strong>Posture:</strong> relaxed knees, a calm upper body, weight over the balls of your feet. This applies to all styles.'),
     ('<strong>Verbindung:</strong> Führen und Folgen läuft über Hände und Arme, nicht über Kraft. Im Kurs wechselst du meist die Partner und lernst so schnell.', '<strong>Connection:</strong> lead and follow work through hands and arms, not force. In class you usually rotate partners and learn quickly that way.'),
     ('<strong>Erste Drehung:</strong> Wenn der Grundschritt sitzt, kommen einfache Drehungen und der Wechsel der Seiten dazu.', '<strong>First turn:</strong> once the basic step feels natural, simple turns and side changes follow.'),
   ]),
 ]),
 ('Bachata-Kurs finden: So wählst du die richtige Schule', 'Finding a Bachata class: how to choose the right school', [
   ('p', f'Kurse gibt es in fast jeder größeren Stadt. Wir haben Übersichten für {CITY_LINKS_DE}. Darauf findest du Schulen mit Links zu ihren Websites, alphabetisch und ohne Wertung.',
         f'Classes exist in almost every larger city. We have overviews for {CITY_LINKS_EN}. They list schools with links to their websites, alphabetical and without a rating.'),
   ('ul', [
     ('<strong>Probestunde:</strong> Frag nach einer Schnupperstunde, bevor du ein Paket buchst. Manche Schulen bieten sie an, andere nicht.', '<strong>Trial class:</strong> ask for a taster class before you buy a bundle. Some schools offer one, others do not.'),
     ('<strong>Level:</strong> Starte bei den Einsteigern, auch wenn du schon andere Tänze kennst. Die Schulen nennen die Stufen unterschiedlich, frag nach.', '<strong>Level:</strong> start with beginners, even if you know other dances. Schools name their levels differently, so ask.'),
     ('<strong>Stil:</strong> Schau, ob der Kurs Dominicana, Moderna oder Sensual unterrichtet. Der Stil lässt sich später wechseln.', '<strong>Style:</strong> check whether the class teaches Dominicana, Moderna or Sensual. You can switch styles later.'),
     ('<strong>Lage und Termin:</strong> Ein fester Wochentag in deiner Nähe hält dich im Training. Prüfe Anfahrt und Uhrzeit ehrlich.', '<strong>Place and time:</strong> a fixed weekday close to you keeps you training. Be honest about the journey and the hour.'),
     ('<strong>Preis:</strong> Einzelstunde, Monatsbeitrag und Block unterscheiden sich. Vergleiche zwei oder drei Preislisten, wir nennen bewusst keine Zahlen, weil sie sich ändern.', '<strong>Price:</strong> single class, monthly fee and block courses differ. Compare two or three price lists; we deliberately quote no numbers because they change.'),
   ]),
   ('p', 'Das offizielle Ranking der Bachata-Schulen erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>. Die Methode mit allen Kriterien steht auf der <a href="deutschland.html#method">Startseite</a>. Du leitest eine Schule? <a href="bewerbung.html">Bewirb dich kostenlos bis zum 30. November</a>.',
         'The official ranking of Bachata schools is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>. The method with all factors is on the <a href="deutschland.html#method">homepage</a>. Do you run a school? <a href="bewerbung.html">Apply for free by November 30</a>.'),
 ]),
 ('Bachata zu Hause üben: Tipps zum Dranbleiben', 'Practising Bachata at home: tips to keep going', [
   ('p', 'Kurs und Üben gehören zusammen. Schon wenige Minuten am Tag helfen, damit sich der Grundschritt in der nächsten Stunde vertraut anfühlt.',
         'Class and practice go together. Even a few minutes a day help the basic step feel familiar in your next class.'),
   ('ul', [
     ('Übe den Grundschritt vor einem Spiegel oder beim Zähneputzen, ohne Musik, dann mit Musik.', 'Practise the basic step in front of a mirror, or while brushing your teeth, first without music and then with music.'),
     ('Höre Bachata auf dem Weg zur Arbeit und zähle die Zählzeiten mit.', 'Listen to Bachata on your way to work and count the beats.'),
     ('Wiederhole nach dem Kurs die ein oder zwei Elemente, die dir schwerfielen, statt alles zu üben.', 'After class, repeat the one or two moves you found hard instead of practising everything.'),
     ('Geh früh auf ein Social, auch nur für eine halbe Stunde. Tanzen mit fremden Partnern lehrt mehr als jedes Video.', 'Go to a social early, even for half an hour. Dancing with new partners teaches more than any video.'),
   ]),
 ]),
 ('Bachata-Socials und Festivals: Wo du tanzen kannst', 'Bachata socials and festivals: where to dance', [
   ('p', 'Auf einem Social tanzt du frei, ohne Unterricht, meist mit gemischter Musik. Eine Liste regelmäßiger Termine findest du auf der Seite <a href="bachata-socials.html">Bachata-Socials in Deutschland</a>. Viele Schulen laden außerdem zu eigenen Übungsabenden ein.',
         'At a social you dance freely, without a lesson, usually to mixed music. You will find a list of regular dates on the page <a href="bachata-socials.html">Bachata socials in Germany</a>. Many schools also invite you to their own practice nights.'),
   ('p', 'Tipp für den ersten Besuch: Komm früh, sag, dass du Anfänger bist, und frag nach einem Tanz. Die Szene ist offen, und die meisten freuen sich über neue Gesichter.',
         'Tip for your first visit: come early, say you are a beginner and ask for a dance. The scene is open, and most people enjoy new faces.'),
 ]),
]

tanzen_faq = [
 ('Wie lange dauert es, Bachata tanzen zu lernen?', 'How long does it take to learn to dance Bachata?',
  'Das hängt von dir ab. Den Grundschritt lernen die meisten in der ersten Stunde, für sicheres Führen oder Folgen auf einem Social brauchst du in der Regel mehrere Wochen regelmäßiges Training. Eine feste Zahl nennen wir bewusst nicht.',
  'That depends on you. Most people pick up the basic step in the first class; for confident leading or following at a social you usually need several weeks of regular training. We deliberately give no fixed number.'),
 ('Brauche ich einen Partner, um Bachata tanzen zu lernen?', 'Do I need a partner to learn Bachata?',
  'Nein, in der Regel nicht. Viele Schulen wechseln die Partner im Kurs. Frag am besten vor der ersten Stunde nach.',
  'No, usually not. Many schools rotate partners in class. It is best to ask before your first class.'),
 ('Welcher Bachata-Stil ist für Anfänger am besten?', 'Which Bachata style is best for beginners?',
  'Die meisten Einsteiger starten mit Bachata Moderna oder Sensual. Wichtig sind der Grundschritt und ein klarer Rhythmus. Der Stil lässt sich später wechseln.',
  'Most beginners start with Bachata Moderna or Sensual. What matters is the basic step and a clear rhythm. You can switch styles later.'),
 ('Kann ich Bachata tanzen lernen, ohne vorher zu tanzen?', 'Can I learn Bachata without any dance experience?',
  'Ja. Einsteigerkurse setzen keine Vorkenntnisse voraus. Wichtig sind Freude an der Musik und die Bereitschaft, regelmäßig zu üben.',
  'Yes. Beginner classes assume no experience. What matters is enjoying the music and being willing to practise regularly.'),
 ('Wo kann ich Bachata tanzen lernen?', 'Where can I learn to dance Bachata?',
  f'In Tanzschulen und Studios in fast jeder größeren Stadt. Übersichten findest du für {CITY_LINKS_DE}.',
  f'In dance schools and studios in almost every larger city. You will find overviews for {CITY_LINKS_EN}.'),
 ('Wann erscheint das Ranking der besten Bachata-Schulen?', 'When is the ranking of the best Bachata schools published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html">ranking page</a>.'),
]

guide_page('bachata-tanzen', 'bt',
  'Bachata tanzen lernen: Stile, Schritte, Kurse',
  'Bachata tanzen lernen: die drei Stile, erste Schritte für Anfänger, Tipps zur Kurswahl und zum Üben. Mit Links zu Schulen in deiner Stadt.',
  'Learn to dance Bachata: styles, steps, classes',
  'Learn to dance Bachata: the three styles, first steps for beginners, tips for choosing a class and for practising, with links to schools in your city.',
  'Bachata tanzen', ('Bachata tanzen · Ratgeber', 'Dancing Bachata · Guide'),
  ('Bachata tanzen lernen: <em class="foil">Stile, Schritte, Kurse</em>', 'Learn to dance Bachata: <em class="foil">styles, steps, classes</em>'),
  ('Bachata tanzen macht Spaß und ist leichter, als es aussieht. Hier erfährst du, welche Stile es gibt, wie die ersten Schritte gehen, woran du einen guten Kurs erkennst und wie du am besten übst.',
   'Dancing Bachata is fun and easier than it looks. Here you learn which styles exist, how the first steps go, how to recognise a good class and how to practise best.'),
  [('check', 'Für <b>Anfänger</b> ohne Partner', 'For <b>beginners</b> without a partner'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  tanzen_sections, tanzen_faq, sibling_group='topic')

grund_sections = [
 ('Bachata-Grundschritt: Das Wichtigste in Kürze', 'The Bachata basic step: the essentials', [
   ('p', f'Der Bachata-Grundschritt ist die Basis für alles, was du später tanzt. Er besteht aus vier Zählzeiten: Du machst drei Schritte in eine Richtung, auf Zählzeit vier folgt ein Tap, dann geht es mit drei Schritten zurück. Bachata stammt aus der Dominikanischen Republik ({WIKI}), und dieser Rhythmus trägt Musik und Tanz bis heute.',
         f'The Bachata basic step is the base for everything you dance later. It has four counts: you take three steps in one direction, a tap follows on count four, then three steps take you back. Bachata comes from the Dominican Republic ({WIKI_EN}), and this rhythm carries the music and the dance to this day.'),
   ('p', 'Auf dieser Seite findest du den Grundschritt Schritt für Schritt, typische Fehler, Übungstipps und den Weg zu den ersten Figuren. Wenn du lieber im Kurs lernst, hilft dir der Ratgeber <a href="bachata-tanzen.html">Bachata tanzen lernen</a> bei der Wahl.',
         'On this page you find the basic step one move at a time, common mistakes, practice tips and the path to your first figures. If you would rather learn in class, the guide <a href="bachata-tanzen.html">Learn to dance Bachata</a> helps you choose.'),
 ]),
 ('Bachata-Grundschritt Schritt für Schritt', 'The Bachata basic step, one move at a time', [
   ('ul', [
     ('<strong>Zählzeit 1:</strong> Tritt mit dem linken Fuß einen kleinen Schritt zur Seite.', '<strong>Count 1:</strong> take a small step to the side with your left foot.'),
     ('<strong>Zählzeit 2:</strong> Setze den rechten Fuß neben den linken.', '<strong>Count 2:</strong> bring your right foot next to your left.'),
     ('<strong>Zählzeit 3:</strong> Tritt wieder mit links zur Seite.', '<strong>Count 3:</strong> step to the side with your left again.'),
     ('<strong>Zählzeit 4:</strong> Tippe mit dem rechten Fuß neben den linken und bewege dabei die Hüfte. Das Gewicht bleibt links.', '<strong>Count 4:</strong> tap your right foot next to your left and move your hip. Your weight stays on the left.'),
     ('<strong>Zählzeit 5 bis 8:</strong> Spiegelverkehrt in die andere Richtung: rechts, links, rechts, Tap mit links.', '<strong>Counts 5 to 8:</strong> the same in mirror image to the other side: right, left, right, tap with left.'),
   ]),
   ('p', 'Führende und Folgende tanzen den Grundschritt gespiegelt, sodass beide gleichzeitig zur selben Seite gehen. Die Schritte bleiben klein, die Knie locker, das Gewicht liegt über den Fußballen. Je kleiner du anfängst, desto leichter wird später das Führen und Folgen.',
         'Leaders and followers dance the basic step mirrored, so both move to the same side at the same time. Keep the steps small, the knees relaxed and your weight over the balls of your feet. The smaller you start, the easier leading and following become later.'),
 ]),
 ('Häufige Fehler beim Bachata-Grundschritt', 'Common mistakes in the Bachata basic step', [
   ('ul', [
     ('<strong>Zu große Schritte:</strong> Sie bringen dich aus dem Rhythmus. Halte sie klein.', '<strong>Steps that are too big:</strong> they throw you off the rhythm. Keep them small.'),
     ('<strong>Steife Knie:</strong> Ohne leichte Beugung wirkt der Tap hart. Bleib locker.', '<strong>Stiff knees:</strong> without a slight bend the tap feels hard. Stay relaxed.'),
     ('<strong>Falsche Zählzeit:</strong> Der Tap gehört auf die vier, nicht auf die eins. Zähle laut mit, bis es sitzt.', '<strong>Wrong count:</strong> the tap belongs on four, not on one. Count out loud until it sits.'),
     ('<strong>Blick auf die Füße:</strong> Schau lieber nach vorn. Die Füße finden den Weg von allein.', '<strong>Looking at your feet:</strong> look ahead instead. Your feet find the way on their own.'),
     ('<strong>Hektik:</strong> Langsame Musik zum Üben hilft. Erst das Tempo steigern, wenn der Ablauf sicher ist.', '<strong>Rushing:</strong> practise with slow music. Increase the tempo only when the pattern is secure.'),
   ]),
 ]),
 ('Bachata Schritte üben: Vom Grundschritt zu den ersten Figuren', 'Practising Bachata steps: from the basic step to your first figures', [
   ('p', 'Sobald der Grundschritt sicher sitzt, kommen die nächsten Bausteine dazu. Die Reihenfolge unterscheidet sich je nach Schule, aber meist siehst du diese Schritte:',
         'Once the basic step is secure, the next building blocks follow. The order differs by school, but you will usually see these:'),
   ('ul', [
     ('<strong>Vorwärts und rückwärts:</strong> Derselbe Rhythmus, nur in einer anderen Richtung.', '<strong>Forward and back:</strong> the same rhythm, just in a different direction.'),
     ('<strong>Seitenwechsel:</strong> Das Paar tauscht die Seiten, ohne den Takt zu verlieren.', '<strong>Side change:</strong> the couple swap sides without losing the beat.'),
     ('<strong>Einfache Drehung:</strong> Die Folgende dreht sich unter dem erhobenen Arm.', '<strong>Simple turn:</strong> the follower turns under a raised arm.'),
     ('<strong>Stilbausteine:</strong> Je nach Stil kommen Fußspiel (Dominicana), Drehfiguren (Moderna) oder Körperwellen (Sensual) dazu.', '<strong>Style building blocks:</strong> depending on the style, footwork (Dominicana), turn patterns (Moderna) or body waves (Sensual) come in.'),
   ]),
   ('p', 'Welcher Stil zu dir passt, erklärt der Ratgeber <a href="bachata-tanzen.html">Bachata tanzen</a>. Geübt wird am besten regelmäßig und in kurzen Einheiten, mit Musik und gern vor einem Spiegel.',
         'Which style suits you is explained in the guide <a href="bachata-tanzen.html">Dancing Bachata</a>. Practice works best in regular, short sessions, with music and ideally in front of a mirror.'),
 ]),
 ('Bachata-Rhythmus und Musik: So hörst du die Zählzeiten', 'Bachata rhythm and music: how to hear the counts', [
   ('p', 'Die Musik hilft dir mehr als jede Erklärung. Typische Bachata-Stücke werden von Gitarren, Bass, Bongos und Güira getragen, und die Güira und die Bongos geben dir einen klaren Puls zum Mitzählen. Höre ein Stück dreimal: beim ersten Mal nur zu, beim zweiten Mal klatschst du die vier Zählzeiten, beim dritten Mal trittst du den Grundschritt.',
         'The music helps you more than any explanation. Typical Bachata tracks are carried by guitars, bass, bongos and güira, and the güira and bongos give you a clear pulse to count along with. Listen to a track three times: the first time just listen, the second time clap the four counts, the third time step the basic step.'),
   ('p', 'Achte außerdem auf Unterschiede im Tempo. Langsamere Stücke sind ideal zum Lernen, weil du mehr Zeit für jeden Schritt hast. Schnellere Stücke kommen später, wenn der Ablauf automatisch läuft. Wer die Musik kennt, tanzt entspannter und merkt schneller, wann ein Stück zum eigenen Stil passt.',
         'Also notice differences in tempo. Slower tracks are ideal for learning because you have more time for each step. Faster tracks come later, when the pattern runs automatically. If you know the music you dance more relaxed and notice sooner when a track suits your own style.'),
 ]),
 ('Bachata-Grundschritt im Kurs lernen', 'Learning the Bachata basic step in class', [
   ('p', f'Im Einsteigerkurs lernst du den Grundschritt mit Musik, mit Korrektur und mit wechselnden Partnern. Übersichten über Schulen und Kurse findest du für {CITY_LINKS_DE}. Alle Listen sind alphabetisch und keine Wertung.',
         f'In a beginner class you learn the basic step with music, with corrections and with rotating partners. You will find overviews of schools and classes for {CITY_LINKS_EN}. All lists are alphabetical and not a rating.'),
   ('p', 'Das offizielle Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>, die Methode steht auf der <a href="deutschland.html#method">Startseite</a>. Schulen können sich bis zum 30. November <a href="bewerbung.html">kostenlos bewerben</a>.',
         'The official ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>, and the method is on the <a href="deutschland.html#method">homepage</a>. Schools can <a href="bewerbung.html">apply for free</a> until November 30.'),
 ]),
]

grund_faq = [
 ('Wie geht der Bachata-Grundschritt?', 'How does the Bachata basic step go?',
  'Drei Schritte zur Seite, auf Zählzeit vier ein Tap, dann drei Schritte zurück und wieder ein Tap. Die Schritte sind klein, die Knie locker.',
  'Three steps to the side, a tap on count four, then three steps back and another tap. Keep the steps small and the knees relaxed.'),
 ('Wie schnell kann ich den Grundschritt lernen?', 'How quickly can I learn the basic step?',
  'Die meisten lernen den Ablauf in der ersten Stunde. Bis er sich sicher und entspannt anfühlt, hilft regelmäßiges Üben mit Musik.',
  'Most people learn the pattern in the first class. Regular practice with music helps until it feels secure and relaxed.'),
 ('Auf welcher Zählzeit kommt der Tap?', 'On which count does the tap come?',
  'Auf die vier und die acht. Der Tap betont den Takt und gibt dem Tanz seinen Charakter.',
  'On four and eight. The tap accents the beat and gives the dance its character.'),
 ('Brauche ich einen Partner, um den Grundschritt zu üben?', 'Do I need a partner to practise the basic step?',
  'Nein. Den Grundschritt kannst du allein üben, am besten mit Musik und vor einem Spiegel.',
  'No. You can practise the basic step alone, ideally with music and in front of a mirror.'),
 ('Ist der Grundschritt in allen Bachata-Stilen gleich?', 'Is the basic step the same in all Bachata styles?',
  'Die Grundidee ist ähnlich, die Ausführung unterscheidet sich. Dominicana setzt auf Fußspiel, Moderna auf Drehungen, Sensual auf Körperwellen. Ein Kurs zeigt dir den Unterschied.',
  'The basic idea is similar, but the execution differs. Dominicana focuses on footwork, Moderna on turns, Sensual on body waves. A class shows you the difference.'),
 ('Wo kann ich Bachata im Kurs lernen?', 'Where can I learn Bachata in class?',
  f'In Tanzschulen in fast jeder größeren Stadt. Übersichten gibt es für {CITY_LINKS_DE}.',
  f'In dance schools in almost every larger city. Overviews exist for {CITY_LINKS_EN}.'),
]

guide_page('bachata-grundschritt', 'bg',
  'Bachata Grundschritt: Anleitung für Anfänger',
  'Bachata Grundschritt Schritt für Schritt: Zählzeiten, typische Fehler, Übungstipps und der Weg zu den ersten Figuren. Mit Links zu Kursen.',
  'Bachata basic step: a guide for beginners',
  'The Bachata basic step one move at a time: counts, common mistakes, practice tips and the path to your first figures, with links to classes.',
  'Bachata Grundschritt', ('Bachata Grundschritt · Anleitung', 'Bachata basic step · Guide'),
  ('Bachata Grundschritt: <em class="foil">Anleitung</em> für Anfänger', 'Bachata basic step: a <em class="foil">guide</em> for beginners'),
  ('Der Bachata-Grundschritt in vier Zählzeiten: Schritt für Schritt erklärt, mit typischen Fehlern und Tipps zum Üben. So gelingt dir der Einstieg, allein zu Hause oder im Kurs.',
   'The Bachata basic step in four counts: explained move by move, with common mistakes and practice tips. This is how you get started, alone at home or in class.'),
  [('check', 'Für <b>Anfänger</b> ohne Partner', 'For <b>beginners</b> without a partner'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  grund_sections, grund_faq, sibling_group='topic')


# ======================================================================
# BACHATA FESTIVALS DEUTSCHLAND and BACHATA SENSUAL (added 2026-10-28)
# Festival facts: only from the organisers' own websites, checked 2026-10-28.
# ======================================================================
FRA_FEST = '<a href="https://frankfurt-bachata-festival.de/" rel="noopener nofollow" target="_blank">Frankfurt Bachata Festival</a>'
DUS_FEST = '<a href="https://dusseldorf.bachata-fest.com/" rel="noopener nofollow" target="_blank">Düsseldorf Bachata Fest</a>'

festd_sections = [
 ('Bachata Festival in Deutschland: Das erwartet dich', 'Bachata festival in Germany: what to expect', [
   ('p', f'Ein Bachata Festival ist ein Wochenende nur für Bachata: Workshops am Tag, Socials und Partys am Abend, dazu Live-Auftritte und Gast-Trainer. Bachata stammt aus der Dominikanischen Republik ({WIKI}), und in Deutschland sind daraus eigene Festivals gewachsen, die Tänzer aus ganz Europa anziehen. Diese Seite zeigt dir, welche Festivals 2026 und 2027 bei den Veranstaltern angekündigt sind, und hilft dir bei der Wahl.',
         f'A Bachata festival is a weekend devoted to Bachata alone: workshops by day, socials and parties at night, plus live acts and guest teachers. Bachata comes from the Dominican Republic ({WIKI_EN}), and in Germany it has grown its own festivals that draw dancers from all over Europe. This page shows which festivals are announced by their organisers for 2026 and 2027 and helps you choose.'),
   ('p', 'Wichtig zur Methode: Wir nennen Daten nur, wenn wir sie auf der Website des Veranstalters gefunden haben (Stand 28. Oktober 2026). Wo die Website keinen Termin zeigt, steht er nicht hier. Termine, Orte und Preise ändern sich, bitte prüfe sie direkt beim Veranstalter.',
         'A note on method: we only state dates that we found on the organiser\'s own website (as of October 28, 2026). Where a website shows no date, we do not list one. Dates, venues and prices change, so please check them with the organiser.'),
 ]),
 ('Bachata-Festivals 2026 und 2027: Termine der Veranstalter', 'Bachata festivals 2026 and 2027: organiser dates', [
   ('p', 'Die Reihenfolge ist chronologisch und keine Wertung. Alle Angaben stammen von den Websites der Veranstalter.',
         'The order is chronological and not a rating. All details come from the organisers\' own websites.'),
   ('cards', [
     {'name': 'Düsseldorf Bachata Fest 2027', 'url': 'https://dusseldorf.bachata-fest.com/',
      'de': '<strong>8. bis 11. Januar 2027</strong> in Düsseldorf. Der Veranstalter nennt es „Germany\'s biggest bachata festival" mit Workshops, Künstlern und Socials. Künstler, Preise und genauer Veranstaltungsort standen beim letzten Check nicht auf der Seite.',
      'en': '<strong>January 8 to 11, 2027</strong> in Düsseldorf. The organiser calls it "Germany\'s biggest bachata festival" with workshops, artists and socials. Artists, prices and the exact venue were not shown on the page at the last check.'},
     {'name': 'Frankfurt Bachata Festival 2027', 'url': 'https://frankfurt-bachata-festival.de/',
      'de': '<strong>22. bis 25. April 2027</strong> in Frankfurt am Main. Der Veranstalter nennt Mario Baro als Live-Act und Early-Bird-Pässe in begrenzter Zahl: Partypass, Social Pass und Fullpass, dazu einen Paar-Fullpass. Die Seite widerspricht sich bei der Dauer (drei oder vier Tage), frag also vor dem Buchen nach.',
      'en': '<strong>April 22 to 25, 2027</strong> in Frankfurt am Main. The organiser names Mario Baro as a live act and offers limited early-bird passes: party pass, social pass and full pass, plus a couple full pass. The page is inconsistent on length (three or four days), so ask before you book.'},
     {'name': 'Munich Bachata Fest', 'url': 'https://bachata-fest.com/',
      'de': 'Der Veranstalter von Düsseldorf führt auf bachata-fest.com auch ein Festival in München. Einen Termin zeigte die Übersichtsseite beim letzten Check nicht, schau dort nach.',
      'en': 'The Düsseldorf organiser also lists a festival in Munich on bachata-fest.com. The overview page showed no date at the last check, so look there.'},
     {'name': 'Bachata Festival Stuttgart', 'url': 'https://bachatafestival-stuttgart.de/',
      'de': 'Festival in Stuttgart mit eigener Website des Veranstalters. Wir konnten die Termine dort nicht abschließend prüfen und nennen deshalb keinen.',
      'en': 'Festival in Stuttgart with its own organiser website. We could not fully confirm the dates there and therefore state none.'},
   ]),
   ('p', 'Dein Festival fehlt oder eine Angabe stimmt nicht mehr? Schreib an <a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a> mit Name, Ort, Datum und Link zur Veranstalter-Seite. Der Eintrag ist kostenlos und nicht käuflich.',
          'Is your festival missing or a detail out of date? Email <a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a> with name, place, date and a link to the organiser\'s page. Listing is free and cannot be bought.'),
 ]),
 ('Bachata Festival Deutschland: Welches passt zu dir?', 'Bachata festival Germany: which one suits you?', [
   ('ul', [
     ('<strong>Dein Level:</strong> Viele Festivals bieten Workshops für Einsteiger bis Fortgeschrittene. Prüfe im Programm, ob dein Level dabei ist, bevor du buchst.', '<strong>Your level:</strong> many festivals offer workshops from beginner to advanced. Check the programme for your level before you book.'),
     ('<strong>Dein Stil:</strong> Manche Festivals setzen auf Sensual, andere auf Dominicana oder Moderna. Der Stil-Ratgeber hilft: <a href="bachata-sensual.html">Bachata Sensual</a>, <a href="bachata-tanzen.html">Bachata tanzen</a>.', '<strong>Your style:</strong> some festivals lean towards Sensual, others towards Dominicana or Moderna. The style guides help: <a href="bachata-sensual.html">Bachata Sensual</a>, <a href="bachata-tanzen.html">Dancing Bachata</a>.'),
     ('<strong>Dein Pass:</strong> Ein Fullpass enthält Workshops und Partys, ein Party- oder Social Pass nur die Abende. Wer vor allem tanzen will, braucht nicht immer alle Workshops.', '<strong>Your pass:</strong> a full pass covers workshops and parties, a party or social pass only the evenings. If you mainly want to dance, you do not always need every workshop.'),
     ('<strong>Anreise:</strong> Die Festivals liegen in Großstädten mit guter Bahnanbindung. Buch das Hotel früh, besonders bei Festivals im Partyhotel.', '<strong>Travel:</strong> the festivals take place in big cities with good rail links. Book your hotel early, especially for festivals held at a party hotel.'),
     ('<strong>Dein Budget:</strong> Preise nennen wir bewusst nur, wo der Veranstalter sie zeigt, denn Early-Bird-Preise steigen meist mit der Zeit.', '<strong>Your budget:</strong> we quote prices only where the organiser shows them, because early-bird prices usually rise over time.'),
   ]),
 ]),
 ('Dein erstes Bachata-Festival: Tipps für Anfänger', 'Your first Bachata festival: tips for beginners', [
   ('p', 'Du musst kein Profi sein. Auf Festivals tanzen Anfänger und Fortgeschrittene zusammen, und die meisten freuen sich über neue Gesichter. Mit diesen Tipps startest du entspannt:',
         'You do not have to be a pro. At festivals beginners and advanced dancers dance together, and most people enjoy new faces. These tips help you start relaxed:'),
   ('ul', [
     ('Lerne vorher den <a href="bachata-grundschritt.html">Grundschritt</a> sicher, damit du auf dem Social nicht zählen musst.', 'Learn the <a href="bachata-grundschritt.html">basic step</a> well beforehand, so you do not have to count on the social floor.'),
     ('Wähle zwei oder drei Workshops statt eines vollen Tages. Pausen sind wichtig, die Partys gehen lange.', 'Pick two or three workshops instead of a full day. Rest matters, the parties run late.'),
     ('Sag offen, dass du Anfänger bist, und frag nach einem Tanz. Die Szene ist freundlich und höflich.', 'Say openly that you are a beginner and ask for a dance. The scene is friendly and polite.'),
     ('Pack Wechselkleidung und bequeme Tanzschuhe ein, ein Festival bedeutet viele Stunden auf der Fläche.', 'Pack a change of clothes and comfortable dance shoes; a festival means many hours on the floor.'),
     ('Trink genug Wasser und plane Schlaf ein. Wer am Sonntag noch tanzt, hat am Freitag nicht alles gegeben.', 'Drink enough water and plan for sleep. Whoever still dances on Sunday did not give everything on Friday.'),
   ]),
 ]),
 ('Bachata lernen vor dem Festival: Kurse in deiner Stadt', 'Learning Bachata before the festival: classes in your city', [
   ('p', f'Wer sich auf ein Festival vorbereitet, startet am besten in einem Kurs. Übersichten über Schulen mit Links zu den Websites findest du für {CITY_LINKS_DE}. Alle Listen sind alphabetisch und keine Wertung.',
         f'The best way to prepare for a festival is a regular class. You will find overviews of schools with links to their websites for {CITY_LINKS_EN}. All lists are alphabetical and not a rating.'),
   ('p', 'Auch auf Socials kannst du üben. Regelmäßige Termine findest du auf der Seite <a href="bachata-socials.html">Bachata-Socials in Deutschland</a>.',
         'You can also practise at socials. Regular dates are on the page <a href="bachata-socials.html">Bachata socials in Germany</a>.'),
 ]),
 ('Festivals und das Ranking der Bachata-Schulen', 'Festivals and the ranking of Bachata schools', [
   ('p', 'Auftritte der Lehrer auf Festivals und Kongressen zählen als eines von neun Kriterien im Ranking (bis zu 15 von 100 Punkten). Bezahlte Festival-Einträge haben keinen Einfluss, Plätze sind nicht käuflich. Das offizielle Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>, die Methode steht auf der <a href="deutschland.html#method">Startseite</a>.',
         'Teachers\' appearances at festivals and congresses count as one of nine factors in the ranking (up to 15 of 100 points). Paid festival listings have no influence, and places cannot be bought. The official ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>, and the method is on the <a href="deutschland.html#method">homepage</a>.'),
   ('p', 'Du leitest eine Schule, deren Lehrer auf Festivals unterrichten? <a href="bewerbung.html">Bewirb dich kostenlos bis zum 30. November</a> und schick uns die Links zu den Line-ups.',
         'Do you run a school whose teachers teach at festivals? <a href="bewerbung.html">Apply for free by November 30</a> and send us the links to the line-ups.'),
 ]),
]

festd_faq = [
 ('Welche Bachata-Festivals gibt es in Deutschland 2027?', 'Which Bachata festivals are there in Germany in 2027?',
  'Auf den Websites der Veranstalter sind das Düsseldorf Bachata Fest vom 8. bis 11. Januar 2027 und das Frankfurt Bachata Festival vom 22. bis 25. April 2027 angekündigt. Weitere Festivals in München und Stuttgart führen wir oben ohne Termin, bis der Veranstalter sie bestätigt.',
  'The organisers\' websites announce the Düsseldorf Bachata Fest for January 8 to 11, 2027 and the Frankfurt Bachata Festival for April 22 to 25, 2027. We list further festivals in Munich and Stuttgart above without a date until the organiser confirms it.'),
 ('Brauche ich Erfahrung für ein Bachata Festival?', 'Do I need experience for a Bachata festival?',
  'Nein. Viele Festivals bieten Workshops für Einsteiger, und die Partys stehen allen offen. Prüfe im Programm, ob dein Level dabei ist.',
  'No. Many festivals offer beginner workshops, and the parties are open to everyone. Check the programme to see whether your level is included.'),
 ('Brauche ich einen Partner für ein Bachata Festival?', 'Do I need a partner for a Bachata festival?',
  'In der Regel nicht. In Workshops wechseln die Partner, und auf den Socials fragst du einfach um einen Tanz. Manche Veranstalter bieten zusätzlich Paar-Pässe an.',
  'Usually not. Partners rotate in workshops, and at socials you simply ask for a dance. Some organisers also offer couple passes.'),
 ('Was kostet ein Bachata Festival?', 'How much does a Bachata festival cost?',
  'Das hängt vom Pass ab. Der Veranstalter des Frankfurt Bachata Festivals zeigt Early-Bird-Pässe in begrenzter Zahl für Partys, Socials oder das volle Programm. Aktuelle Preise stehen nur auf der Website des Veranstalters, wir nennen hier keine festen Zahlen.',
  'That depends on the pass. The Frankfurt Bachata Festival organiser shows limited early-bird passes for parties, socials or the full programme. Current prices are only on the organiser\'s website, so we quote no fixed numbers here.'),
 ('Wie finde ich den richtigen Bachata-Stil für ein Festival?', 'How do I find the right Bachata style for a festival?',
  'Schau ins Programm und hör dir die Gast-Trainer an. Die Stile erklären wir im Ratgeber zu <a href="bachata-sensual.html">Bachata Sensual</a> und auf der Seite <a href="bachata-tanzen.html">Bachata tanzen</a>.',
  'Look at the programme and check the guest teachers. We explain the styles in the guide to <a href="bachata-sensual.html">Bachata Sensual</a> and on the page <a href="bachata-tanzen.html">Dancing Bachata</a>.'),
 ('Wie kann ich mein Festival eintragen?', 'How can I list my festival?',
  'Schreib an hello@latindanceawards.com mit Name, Ort, Datum und Link zur Veranstalter-Seite. Der Eintrag ist kostenlos.',
  'Email hello@latindanceawards.com with name, place, date and a link to the organiser\'s page. Listing is free.'),
 ('Können Festivals das Ranking der Schulen beeinflussen?', 'Can festivals influence the school ranking?',
  'Nein, Plätze sind nicht käuflich. Festival-Auftritte der Lehrer zählen als ein Kriterium von neun, bezahlte Einträge haben keinen Einfluss. Das Ranking erscheint am 20. Dezember 2026.',
  'No, places cannot be bought. Teachers\' festival appearances are one factor of nine, and paid listings have no influence. The ranking is published on December 20, 2026.'),
]

guide_page('bachata-festivals-deutschland', 'bf',
  'Bachata Festival Deutschland 2026/2027: Termine',
  'Bachata Festival Deutschland: Termine 2026 und 2027 laut Veranstaltern, mit Tipps zur Wahl, zum Pass und zum ersten Festival. Alle Angaben geprüft.',
  'Bachata festival Germany 2026/2027: dates',
  'Bachata festival Germany: 2026 and 2027 dates as announced by organisers, with tips on choosing a festival, a pass and your first festival.',
  'Bachata-Festivals Deutschland', ('Bachata-Festivals · 2026/2027', 'Bachata festivals · 2026/2027'),
  ('Bachata Festival Deutschland: <em class="foil">Termine</em> 2026/2027', 'Bachata festival Germany: <em class="foil">dates</em> 2026/2027'),
  ('Bachata Festival in Deutschland: Termine 2026 und 2027 laut Veranstaltern, dazu Tipps für dein erstes Festival. Wir nennen nur Daten, die wir auf der Website des Veranstalters gefunden haben.',
   'Bachata festival in Germany: 2026 and 2027 dates as announced by organisers, plus tips for your first festival. We only state dates we found on the organiser\'s own website.'),
  [('cal', 'Stand <b>28. Oktober 2026</b>', 'As of <b>October 28, 2026</b>'), ('check', 'Termine <b>vom Veranstalter geprüft</b>', 'Dates <b>checked with organisers</b>')],
  festd_sections, festd_faq, sibling_group='topic')

sens_sections = [
 ('Bachata Sensual: Was ist das?', 'Bachata Sensual: what is it?', [
   ('p', f'Bachata Sensual ist ein Stil des Bachata-Tanzes, der in Europa bekannt wurde und heute auf vielen Socials und Festivals zu sehen ist. Bachata selbst stammt aus der Dominikanischen Republik ({WIKI}). Beim Sensual-Stil stehen Körperbewegung, kreisende Bewegungen und Wellen im Vordergrund, dazu eine enge, elastische Verbindung zwischen den Partnern.',
         f'Bachata Sensual is a style of Bachata dancing that became known in Europe and is seen at many socials and festivals today. Bachata itself comes from the Dominican Republic ({WIKI_EN}). In Sensual the focus is on body movement, circular motion and waves, with a close, elastic connection between partners.'),
   ('p', 'Laut dem Tanzportal <a href="https://www.salsavida.com/de/articles/the-different-styles-of-bachata-dancing/" rel="noopener nofollow" target="_blank">SalsaVida</a> wird der Stil mit Spanien und den Lehrmethoden aus Cádiz verbunden. Korke Escalona und Judith Cordero haben die unter dem Namen Bachata Sensual bekannte Methode entwickelt und so zur Verbreitung beigetragen.',
         'According to the dance portal <a href="https://www.salsavida.com/de/articles/the-different-styles-of-bachata-dancing/" rel="noopener nofollow" target="_blank">SalsaVida</a>, the style is linked to Spain and to teaching approaches from Cádiz. Korke Escalona and Judith Cordero developed the method known as Bachata Sensual and helped spread it.'),
   ('p', 'Auf dieser Seite erfährst du, wie sich Bachata Sensual von Dominicana und Moderna unterscheidet, was typisch ist, worauf Anfänger achten sollten und wo du den Stil lernen kannst.',
         'On this page you learn how Bachata Sensual differs from Dominicana and Moderna, what is typical, what beginners should watch for and where you can learn the style.'),
 ]),
 ('Bachata Sensual, Dominicana und Moderna im Vergleich', 'Bachata Sensual, Dominicana and Moderna compared', [
   ('h3', 'Bachata Sensual', 'Bachata Sensual'),
   ('p', 'Weicher und fließender als der traditionelle Stil. Torso-Bewegungen, Isolationen und eine nahe Haltung prägen den Tanz. SalsaVida betont, dass erzwungene Wellen oder Dips kein gutes Sensual sind: Die Bewegung soll aus der Verbindung kommen.',
         'Softer and more fluid than the traditional style. Torso movement, isolations and a close hold shape the dance. SalsaVida stresses that forced waves or dips are not good Sensual: the movement should come from the connection.'),
   ('h3', 'Bachata Dominicana', 'Bachata Dominicana'),
   ('p', 'Der Stil aus der Dominikanischen Republik: Fußarbeit, Spielfreude, Synkopen und schnelle Richtungswechsel, mit Reaktionen auf die Instrumente. Figurenketten spielen eine kleinere Rolle. Mehr dazu bald auf unserer Seite <a href="bachata-dominicana.html">Bachata Dominicana</a>.',
         'The style from the Dominican Republic: footwork, playfulness, syncopation and quick direction changes, reacting to the instruments. Long figure chains play a smaller role. More soon on our page <a href="bachata-dominicana.html">Bachata Dominicana</a>.'),
   ('h3', 'Bachata Moderna', 'Bachata Moderna'),
   ('p', 'Drehmuster, Wraps und strukturierte Partnerarbeit, geprägt von Salsa und Gesellschaftstanz. Der musterorientierteste der drei Hauptstile und oft der am häufigsten unterrichtete.',
         'Turn patterns, wraps and structured partnerwork, shaped by salsa and ballroom. The most pattern-driven of the three main styles and often the most widely taught.'),
 ]),
 ('Bachata Sensual lernen: So fängst du an', 'Learning Bachata Sensual: how to start', [
   ('p', 'Sensual baut auf dem gleichen Grundschritt auf wie alle Bachata-Stile. Lerne zuerst den <a href="bachata-grundschritt.html">Bachata-Grundschritt</a> sicher, dann kommen Körperarbeit und Verbindung dazu.',
         'Sensual builds on the same basic step as all Bachata styles. Learn the <a href="bachata-grundschritt.html">Bachata basic step</a> first, then add body work and connection.'),
   ('ul', [
     ('<strong>Grundschritt zuerst:</strong> Drei Schritte, Tap auf vier. Ohne sicheres Timing wirken Wellen und Drehungen unruhig.', '<strong>Basic step first:</strong> three steps, tap on four. Without secure timing, waves and turns look restless.'),
     ('<strong>Verbindung statt Kraft:</strong> Führen und Folgen läuft über Hände, Arme und Körpermitte. Frag im Kurs nach Übungen zur Verbindung.', '<strong>Connection instead of force:</strong> lead and follow work through hands, arms and your centre. Ask in class for connection exercises.'),
     ('<strong>Langsam üben:</strong> Körperwellen lernst du am besten in langsamer Musik, vor dem Spiegel oder allein, bevor du sie mit Partner tanzt.', '<strong>Practise slowly:</strong> you learn body waves best to slow music, in front of a mirror or alone, before you dance them with a partner.'),
     ('<strong>Nähe nur im Einvernehmen:</strong> Nahe Haltung ist Teil des Stils, aber jeder darf Nein sagen. Sprich es an und achte auf dein Gegenüber.', '<strong>Closeness only by consent:</strong> a close hold is part of the style, but anyone may say no. Speak up and respect your partner.'),
     ('<strong>Offen bleiben:</strong> Probiere alle Stile aus. Viele Tänzer mischen Sensual, Moderna und Dominicana.', '<strong>Stay open:</strong> try all the styles. Many dancers mix Sensual, Moderna and Dominicana.'),
   ]),
 ]),
 ('Bachata-Sensual-Kurs finden: Beispiele von Schulen', 'Finding a Bachata Sensual class: school examples', [
   ('p', 'Viele Bachata-Schulen unterrichten Sensual. Die folgenden Angaben stammen von den Websites der Schulen (Stand Oktober 2026), alphabetisch und keine Wertung. Prüfe Termine und Preise direkt dort.',
         'Many Bachata schools teach Sensual. The following details come from the schools\' websites (as of October 2026), alphabetical and not a rating. Check dates and prices there.'),
   ('cards', [
     {'name': 'BachatAcademy, Berlin', 'url': 'https://www.bachatacademy.de',
      'de': 'Studio in Friedrichshain. Die Website nennt Bachata Sensual und Conscious Bachata sowie eine kostenlose, unverbindliche Probestunde.',
      'en': 'Studio in Friedrichshain. The website lists Bachata Sensual and Conscious Bachata and a free, no-obligation trial class.'},
     {'name': 'La Calidad', 'url': 'https://www.lacalidad.de/dances/bachata',
      'de': 'Die Schule beschreibt Bachata Sensual, auch Fusion oder Moderna genannt, als weicher, fließender und ausdrucksstärker als den traditionellen Stil. Kurse gibt es in den Levels 1 bis 3, laut Website sind Probestunde und ein 4-Wochen-Paket buchbar.',
      'en': 'The school describes Bachata Sensual, also called Fusion or Moderna, as softer, more fluid and more expressive than the traditional style. Classes run in levels 1 to 3, and according to the website a trial class and a 4-week package can be booked.'},
     {'name': 'La Mambita, Berlin', 'url': 'https://www.mambita.de/bachata',
      'de': 'Schwerpunkt auf Bachata Sensual und Moderna, dienstags laufen vier Levels nacheinander. Drop-in ist laut Website möglich.',
      'en': 'Focus on Bachata Sensual and Moderna, with four levels back to back on Tuesdays. According to the website drop-in is possible.'},
   ]),
   ('p', f'Schulen in deiner Stadt findest du hier: {CITY_LINKS_DE}. Deine Schule fehlt? Nutze die <a href="bewerbung.html">kostenlose Bewerbung</a>.',
         f'Schools in your city: {CITY_LINKS_EN}. Is your school missing? Use the <a href="bewerbung.html">free application</a>.'),
 ]),
 ('Bachata Sensual auf Socials und Festivals', 'Bachata Sensual at socials and festivals', [
   ('p', 'Sensual gehört zu den sichtbarsten Stilen auf Socials und Festivals. Auf einer Party tanzt du oft mit Menschen, die verschiedene Stile mischen, also pass deine Nähe und dein Tempo an dein Gegenüber an. Regelmäßige Termine findest du auf der Seite <a href="bachata-socials.html">Bachata-Socials in Deutschland</a>.',
         'Sensual is among the most visible styles at socials and festivals. At a party you often dance with people who mix styles, so adapt your closeness and tempo to your partner. Regular dates are on the page <a href="bachata-socials.html">Bachata socials in Germany</a>.'),
   ('p', 'Mehr zu den Terminen im Überblick: <a href="bachata-festivals-deutschland.html">Bachata Festival Deutschland 2026/2027</a>.',
         'The dates at a glance: <a href="bachata-festivals-deutschland.html">Bachata festival Germany 2026/2027</a>.'),
 ]),
 ('Bachata Sensual und das Ranking der Schulen', 'Bachata Sensual and the school ranking', [
   ('p', 'Im Ranking zählt kein Stil mehr als der andere. Jede Schule wird nach denselben neun öffentlichen Kriterien mit zusammen 100 Punkten bewertet, unter anderem Google-Bewertung, Einsteigerangebot, Events und Festivals. Das offizielle Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>, die Methode steht auf der <a href="deutschland.html#method">Startseite</a>.',
         'No style counts more than another in the ranking. Every school is scored on the same nine public factors, 100 points in total, including Google rating, beginner offer, events and festivals. The official ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>, and the method is on the <a href="deutschland.html#method">homepage</a>.'),
   ('p', 'Du leitest eine Schule? <a href="bewerbung.html">Bewirb dich kostenlos bis zum 30. November</a>.',
         'Do you run a school? <a href="bewerbung.html">Apply for free by November 30</a>.'),
 ]),
]

sens_faq = [
 ('Was ist Bachata Sensual?', 'What is Bachata Sensual?',
  'Ein Bachata-Stil mit Fokus auf Körperbewegung, Wellen und einer engen, elastischen Verbindung. Er wurde in Europa bekannt und wird mit Spanien verbunden.',
  'A Bachata style focusing on body movement, waves and a close, elastic connection. It became known in Europe and is linked to Spain.'),
 ('Was ist der Unterschied zwischen Bachata Sensual und Dominicana?', 'What is the difference between Bachata Sensual and Dominicana?',
  'Dominicana setzt auf Fußarbeit, Synkopen und Spiel mit der Musik, Sensual auf Körperwellen, Isolationen und Nähe. Der Grundschritt ist in beiden die Basis.',
  'Dominicana focuses on footwork, syncopation and playing with the music, Sensual on body waves, isolations and closeness. The basic step is the base for both.'),
 ('Ist Bachata Sensual für Anfänger geeignet?', 'Is Bachata Sensual suitable for beginners?',
  'Ja, wenn du den Grundschritt sicher kannst. Viele Schulen bieten Sensual schon in Einsteigerkursen an. Frag nach einer Probestunde.',
  'Yes, once you have the basic step. Many schools offer Sensual in beginner classes. Ask for a trial class.'),
 ('Brauche ich einen Partner für Bachata Sensual?', 'Do I need a partner for Bachata Sensual?',
  'Nein, in der Regel nicht. In Kursen wechseln die Partner meist. Körperwellen kannst du allein üben.',
  'No, usually not. Partners usually rotate in class. You can practise body waves alone.'),
 ('Ist Bachata Sensual dasselbe wie Moderna?', 'Is Bachata Sensual the same as Moderna?',
  'Nein, aber die Begriffe werden nicht überall gleich verwendet. Eine Schule nennt Sensual auch Fusion oder Moderna. Frag in der Probestunde, was im Kurs gelehrt wird.',
  'No, but the terms are not used the same way everywhere. One school calls Sensual also Fusion or Moderna. Ask in the trial class what the course teaches.'),
 ('Wo kann ich Bachata Sensual lernen?', 'Where can I learn Bachata Sensual?',
  f'In vielen Tanzschulen, zum Beispiel in Berlin. Übersichten gibt es für {CITY_LINKS_DE}.',
  f'In many dance schools, for example in Berlin. Overviews exist for {CITY_LINKS_EN}.'),
 ('Wann erscheint das Ranking der Bachata-Schulen?', 'When is the ranking of Bachata schools published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html">ranking page</a>.'),
]

guide_page('bachata-sensual', 'bs',
  'Bachata Sensual: Stil, Schritte, Kurse lernen',
  'Bachata Sensual erklärt: Unterschied zu Dominicana und Moderna, typische Merkmale, Tipps für Anfänger und Kurse bei Schulen mit Links.',
  'Bachata Sensual: style, steps, how to learn',
  'Bachata Sensual explained: how it differs from Dominicana and Moderna, typical features, tips for beginners and classes at schools, with links.',
  'Bachata Sensual', ('Bachata Sensual · Ratgeber', 'Bachata Sensual · Guide'),
  ('Bachata Sensual: <em class="foil">Stil, Schritte</em> und Kurse', 'Bachata Sensual: <em class="foil">style, steps</em> and classes'),
  ('Bachata Sensual verbindet Körperbewegung, Wellen und eine enge Verbindung. Hier erfährst du, was den Stil ausmacht, wie er sich von Dominicana und Moderna unterscheidet und wie du ihn lernst.',
   'Bachata Sensual combines body movement, waves and a close connection. Here you learn what defines the style, how it differs from Dominicana and Moderna and how to learn it.'),
  [('check', 'Für <b>Anfänger</b> ohne Partner', 'For <b>beginners</b> without a partner'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  sens_sections, sens_faq, sibling_group='topic')



# ======================================================================
# BACHATA DOMINICANA (added 2026-10-28)
# ======================================================================
SV_STYLES = '<a href="https://www.salsavida.com/de/articles/the-different-styles-of-bachata-dancing/" rel="noopener nofollow" target="_blank">SalsaVida</a>'
SV_STYLES_EN = SV_STYLES
dom_sections = [
 ('Bachata Dominicana: Was ist das?', 'Bachata Dominicana: what is it?', [
   ('p', f'Bachata Dominicana ist der ursprüngliche Stil des Bachata-Tanzes. Er stammt aus der Dominikanischen Republik ({WIKI}), wo Bachata als Gesellschaftstanz entstand. Im Mittelpunkt stehen Fußarbeit, Spielfreude und die Reaktion auf die Musik. Wer Bachata Dominicana tanzt, hört auf Gitarre, Bongos und Güira und antwortet mit den Füßen.',
         f'Bachata Dominicana is the original style of Bachata dancing. It comes from the Dominican Republic ({WIKI_EN}), where Bachata developed as a social dance. The focus is on footwork, playfulness and reacting to the music. Dancers of Bachata Dominicana listen to guitar, bongos and güira and answer with their feet.'),
   ('p', f'Laut dem Tanzportal {SV_STYLES} geht es im traditionellen Stil um Fußarbeit, Synkopen, schnelle Richtungswechsel und das Reagieren auf die Instrumente. Lange Figurenketten spielen eine kleinere Rolle, Drehungen und Partnerarbeit gibt es, sie stehen aber weniger im Zentrum.',
         f'According to the dance portal {SV_STYLES_EN}, the traditional style is about footwork, syncopation, quick direction changes and reacting to the instruments. Long figure chains play a smaller role; turns and partnerwork exist but are less central.'),
   ('p', 'Auf dieser Seite erfährst du, was Dominicana von Sensual und Moderna unterscheidet, wie du anfängst und wo du den Stil im Kurs lernst.',
         'On this page you learn what sets Dominicana apart from Sensual and Moderna, how to start and where to learn the style in class.'),
 ]),
 ('Bachata Dominicana, Sensual und Moderna im Vergleich', 'Bachata Dominicana, Sensual and Moderna compared', [
   ('h3', 'Bachata Dominicana', 'Bachata Dominicana'),
   ('p', 'Rhythmische Fußarbeit, offene Haltung, Improvisation und Nähe zur Musik. Der Körper bleibt eher ruhig, die Füße erzählen.',
         'Rhythmic footwork, an open hold, improvisation and closeness to the music. The body stays calmer while the feet do the talking.'),
   ('h3', 'Bachata Sensual', 'Bachata Sensual'),
   ('p', 'Weicher und körperbetonter, mit Wellen, Isolationen und enger Verbindung. Mehr dazu im Ratgeber <a href="bachata-sensual.html">Bachata Sensual</a>.',
         'Softer and more body-focused, with waves, isolations and a close connection. More in the guide <a href="bachata-sensual.html">Bachata Sensual</a>.'),
   ('h3', 'Bachata Moderna', 'Bachata Moderna'),
   ('p', 'Drehmuster, Wraps und strukturierte Partnerarbeit, geprägt von Salsa und Gesellschaftstanz. Oft der Stil, mit dem Einsteigerkurse beginnen.',
         'Turn patterns, wraps and structured partnerwork, shaped by salsa and ballroom. Often the style that beginner classes start with.'),
   ('p', 'Alle drei Stile bauen auf demselben Rhythmus auf. Wer den <a href="bachata-grundschritt.html">Bachata-Grundschritt</a> sicher tanzt, kann jeden von ihnen lernen.',
         'All three styles build on the same rhythm. If you dance the <a href="bachata-grundschritt.html">Bachata basic step</a> securely, you can learn any of them.'),
 ]),
 ('Bachata Dominicana lernen: So fängst du an', 'Learning Bachata Dominicana: how to start', [
   ('ul', [
     ('<strong>Grundschritt zuerst:</strong> Drei Schritte, Tap auf Zählzeit vier. In Dominicana wird er schneller und kleiner getanzt, deshalb zählt sauberes Timing.', '<strong>Basic step first:</strong> three steps, tap on count four. In Dominicana it is danced faster and smaller, so clean timing matters.'),
     ('<strong>Musik hören:</strong> Achte auf Güira und Bongos und versuche, Betonungen mit den Füßen zu beantworten.', '<strong>Listen to the music:</strong> notice the güira and bongos and try to answer accents with your feet.'),
     ('<strong>Klein anfangen:</strong> Kleine Schritte, lockere Knie, Gewicht über den Fußballen. Fußarbeit wird durch Wiederholung leicht.', '<strong>Start small:</strong> small steps, relaxed knees, weight over the balls of your feet. Footwork becomes easy through repetition.'),
     ('<strong>Spielen statt perfekt sein:</strong> Dominicana lebt von Improvisation. Probiere kleine Variationen aus, wenn der Grundschritt sitzt.', '<strong>Play instead of being perfect:</strong> Dominicana lives on improvisation. Try small variations once the basic step sits.'),
     ('<strong>Probestunde nutzen:</strong> Frag die Schule, ob der Kurs wirklich Dominicana lehrt. Die Begriffe werden nicht überall gleich verwendet.', '<strong>Use a trial class:</strong> ask the school whether the class really teaches Dominicana. The terms are not used the same way everywhere.'),
   ]),
   ('p', 'Plane für Dominicana etwas mehr Geduld ein als für Moderna. Die Füße lernen schnell, aber das Gefühl für die Musik wächst mit jeder Stunde, die du tanzt. Höre dazwischen traditionelle und moderne Stücke und achte darauf, wie sich die Betonungen verändern. So entwickelst du ein Gespür dafür, wann du ruhig bleibst und wann du spielst.',
         'Plan for a little more patience with Dominicana than with Moderna. Your feet learn quickly, but the feel for the music grows with every hour you dance. In between, listen to traditional and modern tracks and notice how the accents change. That builds a sense of when to stay calm and when to play.'),
 ]),
 ('Bachata-Dominicana-Kurs finden: Beispiele', 'Finding a Bachata Dominicana class: examples', [
   ('p', 'Dominicana wird seltener angeboten als Moderna oder Sensual, aber es gibt Kurse. Die Beispiele stammen aus öffentlichen Kurslisten (Stand Oktober 2026), alphabetisch und keine Wertung. Prüfe Termine und Preise direkt beim Anbieter.',
         'Dominicana is offered less often than Moderna or Sensual, but classes exist. The examples come from public course listings (as of October 2026), alphabetical and not a rating. Check dates and prices with the provider.'),
   ('cards', [
     {'name': 'Hochschulsport Leuphana, Lüneburg', 'url': 'https://buchung.hochschulsport.leuphana.de/angebote/aktueller_zeitraum/_Bachata_Dominican.html',
      'de': 'Der Kurs „Bachata Dominican" vermittelt laut Anbieter die authentischen Grundlagen des ursprünglichen Stils mit rhythmischer Fußarbeit, spielerischer Improvisation und Nähe zur Musik. Zielgruppe sind Anfänger und Mittelstufe, ein Partner ist nicht nötig.',
      'en': 'According to the provider, the "Bachata Dominican" course teaches the authentic basics of the original style with rhythmic footwork, playful improvisation and closeness to the music. It is aimed at beginners and intermediate dancers, and no partner is needed.'},
     {'name': 'Tanzstudio GLOW, Berlin-Mitte', 'url': 'https://urbansportsclub.com/de/venues/the-essence-of-bachata',
      'de': 'Laut Eintrag bei Urban Sports Club läuft sonntags ein Kurs „Bachata Dominicana" mit einer Stunde Footwork und Bodymovement und einer Stunde Partnerwork. Er richtet sich an Tänzer mit Grundkenntnissen.',
      'en': 'According to the Urban Sports Club listing, a "Bachata Dominicana" course runs on Sundays with one hour of footwork and body movement and one hour of partnerwork. It is aimed at dancers who know the basics.'},
   ]),
   ('p', f'Schulen in deiner Stadt findest du hier: {CITY_LINKS_DE}. Du bietest Dominicana an und fehlst in der Liste? Nutze die <a href="bewerbung.html">kostenlose Bewerbung</a>.',
         f'Schools in your city: {CITY_LINKS_EN}. Do you teach Dominicana and are missing from the list? Use the <a href="bewerbung.html">free application</a>.'),
 ]),
 ('Bachata Dominicana auf Socials und Festivals', 'Bachata Dominicana at socials and festivals', [
   ('p', 'Auf Socials triffst du alle Stile gemischt. Dominicana-Fans erkennen sich an kleinen, schnellen Schritten und viel Musikalität. Regelmäßige Termine findest du auf der Seite <a href="bachata-socials.html">Bachata-Socials in Deutschland</a>, die Festival-Termine laut Veranstaltern auf <a href="bachata-festivals-deutschland.html">Bachata Festival Deutschland</a>.',
         'At socials you meet all styles mixed. Dominicana fans are recognisable by small, quick steps and a lot of musicality. Regular dates are on the page <a href="bachata-socials.html">Bachata socials in Germany</a>, and festival dates as announced by organisers are on <a href="bachata-festivals-deutschland.html">Bachata festival Germany</a>.'),
   ('p', 'Mehr Grundlagen zum Tanzen allgemein: <a href="bachata-tanzen.html">Bachata tanzen lernen</a>.',
         'More basics on dancing in general: <a href="bachata-tanzen.html">Learn to dance Bachata</a>.'),
 ]),
 ('Bachata Dominicana und das Ranking der Schulen', 'Bachata Dominicana and the school ranking', [
   ('p', 'Im Ranking zählt kein Stil mehr als der andere. Jede Schule wird nach denselben neun öffentlichen Kriterien mit zusammen 100 Punkten bewertet, unter anderem Google-Bewertung, Einsteigerangebot, Events und Festivals. Das offizielle Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>, die Methode steht auf der <a href="deutschland.html#method">Startseite</a>.',
         'No style counts more than another in the ranking. Every school is scored on the same nine public factors, 100 points in total, including Google rating, beginner offer, events and festivals. The official ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>, and the method is on the <a href="deutschland.html#method">homepage</a>.'),
   ('p', 'Du leitest eine Schule? <a href="bewerbung.html">Bewirb dich kostenlos bis zum 30. November</a>.',
         'Do you run a school? <a href="bewerbung.html">Apply for free by November 30</a>.'),
 ]),
]

dom_faq = [
 ('Was ist Bachata Dominicana?', 'What is Bachata Dominicana?',
  'Der ursprüngliche Bachata-Stil aus der Dominikanischen Republik mit Fokus auf Fußarbeit, Synkopen, Improvisation und dem Reagieren auf die Musik.',
  'The original Bachata style from the Dominican Republic, focusing on footwork, syncopation, improvisation and reacting to the music.'),
 ('Was ist der Unterschied zwischen Dominicana und Sensual?', 'What is the difference between Dominicana and Sensual?',
  'Dominicana setzt auf Fußarbeit und Spiel mit dem Rhythmus, Sensual auf Körperwellen, Isolationen und eine engere Verbindung. Der Grundschritt ist in beiden die Basis.',
  'Dominicana focuses on footwork and playing with the rhythm, Sensual on body waves, isolations and a closer connection. The basic step is the base for both.'),
 ('Ist Bachata Dominicana für Anfänger geeignet?', 'Is Bachata Dominicana suitable for beginners?',
  'Ja, wenn du den Grundschritt lernst. Ein Hochschulsport-Kurs in Lüneburg richtet sich laut Anbieter an Anfänger und Mittelstufe. Andere Kurse setzen Grundkenntnisse voraus, lies die Beschreibung.',
  'Yes, as you learn the basic step. A university sport course in Lüneburg is aimed at beginners and intermediate dancers according to the provider. Other courses assume basic knowledge, so read the description.'),
 ('Brauche ich einen Partner für Bachata Dominicana?', 'Do I need a partner for Bachata Dominicana?',
  'In der Regel nicht. Die Fußarbeit kannst du allein üben, und in Kursen wechseln die Partner meist. Der Lüneburger Kurs nennt ausdrücklich, dass kein Partner nötig ist.',
  'Usually not. You can practise footwork alone, and partners usually rotate in class. The Lüneburg course explicitly states that no partner is needed.'),
 ('Wo kann ich Bachata Dominicana lernen?', 'Where can I learn Bachata Dominicana?',
  f'In einzelnen Kursen von Tanzschulen und Hochschulsport. Übersichten über Schulen gibt es für {CITY_LINKS_DE}.',
  f'In individual courses at dance schools and university sport. Overviews of schools exist for {CITY_LINKS_EN}.'),
 ('Wann erscheint das Ranking der Bachata-Schulen?', 'When is the ranking of Bachata schools published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html">ranking page</a>.'),
]

guide_page('bachata-dominicana', 'bd',
  'Bachata Dominicana: Stil, Merkmale, Kurse lernen',
  'Bachata Dominicana erklärt: der ursprüngliche Stil aus der Dominikanischen Republik, Unterschied zu Sensual und Moderna, Tipps und Kurse.',
  'Bachata Dominicana: style, features, how to learn',
  'Bachata Dominicana explained: the original style from the Dominican Republic, how it differs from Sensual and Moderna, tips and classes.',
  'Bachata Dominicana', ('Bachata Dominicana · Ratgeber', 'Bachata Dominicana · Guide'),
  ('Bachata Dominicana: <em class="foil">Stil, Merkmale</em> und Kurse', 'Bachata Dominicana: <em class="foil">style, features</em> and classes'),
  ('Bachata Dominicana ist der ursprüngliche Stil aus der Dominikanischen Republik mit Fußarbeit, Spielfreude und Nähe zur Musik. Hier erfährst du, was ihn ausmacht und wie du ihn lernst.',
   'Bachata Dominicana is the original style from the Dominican Republic, with footwork, playfulness and closeness to the music. Here you learn what defines it and how to learn it.'),
  [('check', 'Für <b>Anfänger</b> ohne Partner', 'For <b>beginners</b> without a partner'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  dom_sections, dom_faq, sibling_group='topic')


# ======================================================================
# Events page: recurring Bachata socials by city + submit form
# ======================================================================
B.PAGE_CSS += r'''
.evc article p{margin:6px 0;color:var(--muted);font-size:15px;line-height:1.5}
.evc article .evl{display:flex;gap:14px;margin-top:10px;font-size:14px}
.evc article .evl a{color:var(--gold-light);font-weight:600}
.evh{margin:44px 0 16px;font-family:var(--serif);font-weight:500;font-size:28px}
.evw{max-width:1000px}
'''
_te = T('ev')
_ev_secs = ''
for _k, (_de, _en) in CITY_LABEL.items():
    if _k in EV_BY_CITY:
        _g = f'<a href="bachata-{_k}.html">{_te("span", "Bachata-Schulen in " + _de, "Bachata schools in " + _en)}</a>' if exists('bachata-' + _k) else ''
        _ev_secs += f'<section class="evcity" data-city="{_k}" id="{_k}">{_te("h2", "Bachata-Socials in " + _de, "Bachata socials in " + _en, "class=\"evh\"")}{ev_cards(_te, EV_BY_CITY[_k])}<p class="muted" style="margin-top:12px"><a href="bachata-party-{_k}.html">{_te("span", "Alle Details: Bachata-Party in " + _de, "Full details: Bachata party in " + _en)}</a> · {_g}</p></section>'
_ev_cityopts = ''.join(f'<option value="{k}">{CITY_LABEL[k][0]}</option>' for k in CITY_LABEL if k in EV_BY_CITY)
_ev_n = len(EVENTS)
_emain = f"""<section class="page-hero"><div class="wrap" style="grid-template-columns:1fr"><div>
  {_te("h1", "Bachata-Socials in Deutschland", "Bachata socials in Germany")}
  {_te("p", "Regelmäßige Bachata-Partys und Übungsabende nach Stadt, mit Ort, Zeit und Preis. Du veranstaltest einen Social? Trag ihn kostenlos ein.", "Regular Bachata parties and practice nights by city, with place, time and price. Do you run a social? List it for free.", 'class="lede"')}
  <div class="ctas"><a class="btn btn-gold" href="#eintragen">{_te("span", "Social eintragen", "List a social")}</a></div>
</div></div></section>
<section class="block"><div class="wrap tp evw">
  <label style="max-width:320px">{_te("span", "Stadt", "City")}<select id="evsel"><option value="">{_te("span", "Alle Städte", "All cities")}</option>{_ev_cityopts}</select></label>
  <p class="muted" style="margin-top:12px">{_te("span", f"{_ev_n} Socials in fünf Städten, Stand Oktober 2026. Die Angaben stammen aus öffentlichen Veranstaltungslisten und von den Seiten der Veranstalter. Zeiten und Preise ändern sich, bitte prüfe sie vor dem Besuch. Weitere Städte folgen, sobald Veranstalter ihre Socials eintragen. Zum ersten Mal auf einem Social? <a href='bachata-party.html'>So läuft eine Bachata Party ab</a>.", f"{_ev_n} socials in five cities, as of October 2026. Details come from public event listings and the organisers' own pages. Times and prices change, so please check before you go. More cities follow as organisers list their socials. First time at a social? <a href='bachata-party.html'>How a Bachata party runs</a>.")}</p>
  {_ev_secs}
  <section id="evnew" hidden><h2 class="evh">{_te("span", "Neu eingetragen", "Newly listed")}</h2><div class="cards two evc" id="evnewl"></div></section>

  <div class="prose" id="lesen" style="margin:34px 0">
    {_te("h2", "So liest du diese Liste", "How to read this list")}
    {_te("p", "<b>Kurs vor der Party.</b> Steht bei einem Eintrag eine Kurszeit vor der Party, lohnt sich der frühe Start: Im kurzen Workshop lernst du die Figuren des Abends und tanzt dich ein, bevor die Fläche voll wird. Als Einsteiger kommst du am besten zu diesen Terminen.", "<b>Class before the party.</b> If an entry lists a class time before the party, arrive for it. The short workshop teaches the moves of the night and lets you warm up before the floor fills. Beginners are best off at these dates.")}
    {_te("p", "<b>Monatlich oder wöchentlich.</b> „Jeden Freitag“ heißt jede Woche, „jeden 2. Samstag im Monat“ nur einmal im Monat. Feiertage, Ferien und Sonderveranstaltungen können einen Termin verschieben. Bestätige deshalb jeden Abend kurz beim Veranstalter, den du über den Link „Veranstalter“ erreichst.", "<b>Monthly or weekly.</b> “Every Friday” means every week, “every 2nd Saturday of the month” only once a month. Public holidays, school breaks and special events can move a date, so confirm each night with the organiser through the “Veranstalter” link.")}
    {_te("p", "<b>Preis und Getränke.</b> Manche Socials nennen einen Eintritt inklusive Workshop, andere einen Getränkegutschein. Das steht dann bei der Angabe. Fehlt ein Preis, hat der Veranstalter keinen veröffentlicht, und wir schreiben keinen dazu.", "<b>Price and drinks.</b> Some socials list an entry that includes the workshop, others a drink voucher. It says so in the entry. If no price is shown, the organiser has not published one, and we do not add one.")}
    {_te("p", "<b>Stand der Angaben.</b> Die Liste wurde im Oktober 2026 aus öffentlichen Quellen zusammengestellt und nicht bei jedem Veranstalter einzeln bestätigt. Sie ist eine Orientierung, kein Fahrplan. Siehst du einen Fehler oder fehlt ein Social? Mit dem Formular unten oder per E-Mail korrigieren wir ihn.", "<b>Status of the data.</b> The list was compiled from public sources in October 2026 and not confirmed with every organiser individually. It is a guide, not a timetable. If you see a mistake or a social is missing, tell us with the form below or by email and we will correct it.")}
  </div>

  <div class="box" id="eintragen"><h3>{_te("span", "Social kostenlos eintragen", "List your social for free")}</h3>
    <form id="evform" novalidate style="display:grid;gap:14px">
      <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
      <div class="row2"><label>{_te("span", "Name des Socials", "Name of the social")}<input type="text" name="name" maxlength="80" required></label>
      <label>{_te("span", "Stadt", "City")}<select name="city">{B._copts_n}</select></label></div>
      <div class="row2"><label>{_te("span", "Ort (Club oder Schule)", "Venue (club or school)")}<input type="text" name="venue" maxlength="80" required></label>
      <label>{_te("span", "Adresse", "Address")}<input type="text" name="addr" maxlength="120"></label></div>
      <div class="row2"><label>{_te("span", "Wann (zum Beispiel jeden 2. Freitag)", "When (for example every 2nd Friday)")}<input type="text" name="when" maxlength="80"></label>
      <label>{_te("span", "Uhrzeit", "Time")}<input type="text" name="time" maxlength="60"></label></div>
      <div class="row2"><label>{_te("span", "Eintritt", "Entry price")}<input type="text" name="price" maxlength="40"></label>
      <label>{_te("span", "Link zur Veranstaltung", "Link to the event")}<input type="url" name="link" placeholder="https://" maxlength="200"></label></div>
      <label>{_te("span", "Deine E-Mail (wird nicht veröffentlicht)", "Your email (not published)")}<input type="email" name="email" maxlength="120" required></label>
      <label class="consent"><input type="checkbox" name="consent"><span>{_te("span", "Ich bestätige, dass ich den Social veranstalte oder dazu befugt bin, und stimme zu, dass die Angaben öffentlich angezeigt werden. Ich kann Änderung oder Löschung jederzeit per E-Mail verlangen.", "I confirm that I run this social or am authorised to list it, and I agree that the details are shown publicly. I can ask for changes or removal at any time by email.")}</span></label>
      <div class="btnrow"><button type="submit" class="btn btn-gold">{_te("span", "Social einreichen", "Submit social")}</button></div>
      <p class="muted" id="evmsg" role="status" hidden></p>
    </form></div>
  <p class="muted" style="margin-top:18px">{_te("span", "Du veranstaltest einen Social, der hier steht, und möchtest etwas ändern oder entfernen lassen? Schreib an hello@latindanceawards.com, wir antworten schnell.", "Do you run a social listed here and want something changed or removed? Email hello@latindanceawards.com and we will reply quickly.")}</p>
</div></section>"""
_ejs = r"""
  var EP="__EP__";
  var S={err:["Bitte Name, Ort und E-Mail ausfüllen und der Veröffentlichung zustimmen.","Please fill in name, venue and email and agree to publication."],ok:["Danke! Wir prüfen den Eintrag und schalten ihn danach frei.","Thank you! We will review the listing and then publish it."],fail:["Das hat nicht geklappt. Bitte versuche es noch einmal.","That did not work. Please try again."],org:["Veranstalter","Organiser"]};
  function L(k){return S[k][window.LANG==="en"?1:0];}
  function esc(x){return String(x==null?"":x).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
  var sel=document.getElementById("evsel");
  function filt(){ var v=sel.value; [].forEach.call(document.querySelectorAll(".evcity"),function(s){ s.hidden=!!v&&s.getAttribute("data-city")!==v; }); }
  sel.addEventListener("change",function(){ try{history.replaceState(null,"",v_()+(sel.value?"#"+sel.value:""));}catch(e){} filt(); });
  function v_(){ return location.pathname+location.search; }
  var h=(location.hash||"").slice(1); if(h&&sel.querySelector('option[value="'+h+'"]')){ sel.value=h; filt(); }
  fetch(EP+"?action=events").then(function(r){return r.json();}).then(function(j){
    var a=j.items||[]; if(!a.length) return; var box=document.getElementById("evnewl"); box.innerHTML="";
    a.forEach(function(p){ var u=/^https:\/\//i.test(p.link||"")?p.link:"";
      box.innerHTML+='<article><h3>'+esc(p.name)+'</h3><p>'+esc(p.venue)+(p.addr?', '+esc(p.addr):'')+', '+esc(p.city)+'</p><p>'+esc(p.when)+(p.time?'. '+esc(p.time):'')+'</p><span class="meta">'+esc(p.price||"")+'</span>'+(u?'<div class="evl"><a href="'+esc(u)+'" rel="noopener nofollow ugc" target="_blank">'+esc(L("org"))+'</a></div>':'')+'</article>'; });
    document.getElementById("evnew").hidden=false;
  }).catch(function(){});
  var f=document.getElementById("evform"),m=document.getElementById("evmsg"),mailRe=/^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  f.addEventListener("submit",function(ev){ ev.preventDefault(); var e=f.elements;
    if(!e.name.value.trim()||!e.venue.value.trim()||!mailRe.test(e.email.value.trim())||!e.consent.checked){ m.textContent=L("err"); m.hidden=false; return; }
    var b=new URLSearchParams({action:"event",name:e.name.value.trim(),city:e.city.value,venue:e.venue.value.trim(),addr:e.addr.value.trim(),when:e.when.value.trim(),time:e.time.value.trim(),price:e.price.value.trim(),link:e.link.value.trim(),email:e.email.value.trim(),hp:e.hp.value,language:window.LANG==="en"?"EN":"DE"});
    var btn=f.querySelector("button[type=submit]"); btn.disabled=true;
    fetch(EP,{method:"POST",mode:"no-cors",body:b}).then(function(){ f.reset(); btn.disabled=false; m.textContent=L("ok"); m.hidden=false; }).catch(function(){ btn.disabled=false; m.textContent=L("fail"); m.hidden=false; });
  });
""".replace('__EP__', B.EP_URL)
page('bachata-socials.html', 'Bachata-Socials in Deutschland: Partys nach Stadt · Latin Dance Awards',
     'Regelmäßige Bachata-Socials und Partys in Berlin, Hamburg, München, Köln und Frankfurt mit Ort, Zeit und Preis. Veranstalter tragen kostenlos ein.',
     'Bachata socials in Germany: parties by city · Latin Dance Awards',
     'Regular Bachata socials and parties in Berlin, Hamburg, Munich, Cologne and Frankfurt with place, time and price. Organisers can list for free.',
     'bachata-socials.html', _emain, _te.en, _ejs, schema=[crumbs('Bachata-Socials', 'bachata-socials.html')])


# ======================================================================
# One full page per city: "Bachata Party {city}"
# ======================================================================
def party_page(key):
    de, en = CITY_LABEL[key]; evs = EV_BY_CITY[key]; slug = f'bachata-party-{key}'
    n = len(evs)
    by_day = {}
    for e in evs:
        for d in META[e['name']][0]: by_day.setdefault(d, []).append(e)
    days = sorted(by_day)
    day_de = ', '.join(WD[d][0] for d in days); day_en = ', '.join(WD[d][1] for d in days)
    cls = [e for e in evs if META[e['name']][1]]
    monthly = [e for e in evs if META[e['name']][2]]
    weekly = n - len(monthly)
    sch = [x for x in B.SCH if x['city'] == key][:3]
    cal = [(f'<strong>{WD[d][0]}:</strong> ' + ', '.join(f'{e["name"]} ({e["venue"]})' for e in by_day[d]),
            f'<strong>{WD[d][1]}:</strong> ' + ', '.join(f'{e["name"]} ({e["venue"]})' for e in by_day[d])) for d in days]
    secs = [
     (f'Bachata-Party in {de}: Das Wichtigste auf einen Blick', f'Bachata party in {en}: the essentials', [
       ('p', f'In {de} findest du aktuell {n} regelmäßige Socials mit Bachata, davon {weekly} wöchentlich oder an festen Tagen und {len(monthly)} monatlich. Sie verteilen sich auf {day_de}. Die Angaben stammen aus öffentlichen Veranstaltungslisten und von den Seiten der Veranstalter (Stand Oktober 2026).',
             f'{en} currently has {n} regular socials with Bachata, {weekly} weekly or on fixed days and {len(monthly)} monthly. They fall on {day_en}. Details come from public event listings and the organisers\' pages (as of October 2026).'),
       ('p', 'Zeiten, Preise und Programm ändern sich. Prüfe vor dem Besuch die Seite des Veranstalters, die du bei jedem Eintrag verlinkt findest.',
             'Times, prices and programme change. Before you go, check the organiser\'s page, which is linked on every listing.'),
     ]),
     (f'Bachata-Socials in {de} nach Wochentag', f'Bachata socials in {en} by weekday', [
       ('ul', cal),
       ('p', 'Monatliche Socials findest du unten mit ihrem festen Wochentag im Monat, zum Beispiel jeden 2. oder 3. Samstag.',
             'Monthly socials are listed below with their fixed day of the month, for example every 2nd or 3rd Saturday.'),
     ]),
     (f'Alle Bachata-Partys in {de} im Detail', f'All Bachata parties in {en} in detail', [
       ('evall', key),
     ]),
     (f'Bachata-Party für Anfänger in {de}', f'Bachata parties for beginners in {en}', [
       ('p', 'Auf einen Social zu gehen ist der schnellste Weg, das Gelernte anzuwenden. Für den Einstieg sind Abende ideal, an denen vor der Party ein Kurs oder Workshop läuft: Du lernst die Grundlagen und tanzt danach mit Leuten, die auf demselben Stand sind.',
             'Going to a social is the fastest way to use what you learned. Evenings with a class or workshop before the party are ideal for starting out: you learn the basics and then dance with people at the same level.'),
       ('ul', [(f'<strong>{e["name"]}</strong> ({e["venue"]}): ' + e['time'][0], f'<strong>{e["name"]}</strong> ({e["venue"]}): ' + e['time'][1]) for e in cls]) if cls else ('p', 'Bei den meisten Einträgen ist kein Kurs vor der Party angegeben. Frag beim Veranstalter nach.', 'Most listings do not mention a class before the party. Ask the organiser.'),
       ('p', 'Du brauchst keinen Partner. Auf Socials wechselt man die Tanzpartner mit jedem Lied. Du kannst jeden fragen, und ein Nein ist völlig in Ordnung.',
             'You do not need a partner. At socials people change dance partners with every song. You can ask anyone, and a no is perfectly fine.'),
     ]),
     (f'Bachata-Social in {de}: Das erwartet dich', f'A Bachata social in {en}: what to expect', [
       ('ul', [
         ('<strong>Musik:</strong> Je nach Abend läuft Bachata Sensual, Moderna oder Dominicana, oft gemischt mit Salsa. Bei reinen Bachata-Abenden steht das im Titel.', '<strong>Music:</strong> depending on the night you will hear Bachata Sensual, Moderna or Dominicana, often mixed with Salsa. Pure Bachata nights say so in the title.'),
         ('<strong>Etikette:</strong> Frag höflich zum Tanz, bedanke dich danach und achte auf dein Gegenüber. Ein gepflegtes Äußeres und ein Ersatzshirt sind auf Socials normal.', '<strong>Etiquette:</strong> ask politely for a dance, say thank you afterwards and pay attention to your partner. Fresh clothes and a spare shirt are normal at socials.'),
         ('<strong>Schuhe:</strong> Nimm Schuhe mit glatter Sohle mit, mit denen du dich drehen kannst, und vermeide Sneaker mit starkem Profil.', '<strong>Shoes:</strong> bring shoes with a smooth sole you can turn in, and avoid sneakers with a heavy tread.'),
         ('<strong>Ankunft:</strong> Komm zum Kurs oder früh am Abend. Dann ist es leerer, und du lernst die Szene leichter kennen.', '<strong>Arrival:</strong> come for the class or early in the evening. It is quieter and easier to get to know people.'),
       ]),
     ]),
     (f'Bachata lernen in {de}: Schulen und Kurse', f'Learning Bachata in {en}: schools and classes', [
       ('p', f'Wenn du in {de} Bachata richtig lernen willst, findest du auf der Seite <a href="bachata-{key}.html">Bachata {de}</a> die Schulen im Überblick. Das Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html#{key}">Ranking-Seite</a>.',
             f'If you want to properly learn Bachata in {en}, the page <a href="bachata-{key}.html">Bachata {en}</a> gives an overview of the schools. The ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html#{key}">ranking page</a>.'),
       ('ul', [(f'<a href="schools/{x["slug"]}.html">{x["name"]}</a>: Zwischenstand {str(x["pts"]).replace(".", ",")} von 100 Punkten', f'<a href="schools/{x["slug"]}.html">{x["name"]}</a>: interim score {x["pts"]} of 100 points') for x in sch]) if sch else ('p', '', ''),
       ('p', 'Reisende finden auf der <a href="reisen.html?c=' + key + '">Tanzreise-Seite</a> die Schulen, die Community und Lehrer und DJs vor Ort. <a href="bachata-socials.html#eintragen">Trag deinen Social kostenlos ein</a>, wenn er hier fehlt.',
             'Visitors will find the schools, the community and teachers and DJs on the <a href="reisen.html?c=' + key + '">dance trip page</a>. <a href="bachata-socials.html#eintragen">List your social for free</a> if it is missing here.'),
     ]),
    ]
    first = evs[0]; fri = [e for e in evs if 4 in META[e['name']][0]]; sun = [e for e in evs if 6 in META[e['name']][0]]
    def names(l): return ', '.join(f'{e["name"]} ({e["venue"]})' for e in l)
    faq = [
     (f'Wo gibt es Bachata-Partys in {de}?', f'Where are the Bachata parties in {en}?',
      f'Regelmäßige Bachata-Socials gibt es zum Beispiel bei {names(evs[:3])}. Alle {n} Einträge mit Zeit und Preis stehen oben auf dieser Seite.',
      f'Regular Bachata socials include {names(evs[:3])}. All {n} listings with time and price are above on this page.'),
     (f'Gibt es freitags eine Bachata-Party in {de}?', f'Is there a Bachata party in {en} on Fridays?',
      (f'Ja: {names(fri)}.' if fri else f'In unserer Liste steht für {de} aktuell kein fester Freitags-Social. Die Wochentage findest du oben.'),
      (f'Yes: {names(fri)}.' if fri else f'Our list currently has no fixed Friday social for {en}. The weekdays are listed above.')),
     (f'Gibt es sonntags eine Bachata-Party in {de}?', f'Is there a Bachata party in {en} on Sundays?',
      (f'Ja: {names(sun)}.' if sun else f'In unserer Liste steht für {de} aktuell kein fester Sonntags-Social. Die Wochentage findest du oben.'),
      (f'Yes: {names(sun)}.' if sun else f'Our list currently has no fixed Sunday social for {en}. The weekdays are listed above.')),
     ('Brauche ich einen Partner für einen Bachata-Social?', 'Do I need a partner for a Bachata social?',
      'Nein. Auf Socials werden die Tanzpartner gewechselt. Du kannst jeden zum Tanz auffordern, und ein Nein ist in Ordnung.', 'No. Partners change at socials. You can ask anyone to dance, and a no is fine.'),
     ('Was kostet ein Bachata-Social?', 'How much does a Bachata social cost?',
      'Bei den gelisteten Socials liegt der Eintritt meist im einstelligen bis niedrigen zweistelligen Euro-Bereich, oft mit Kurs. Den genauen Preis zeigt jeder Eintrag, aber prüfe ihn beim Veranstalter.', 'For the listed socials entry is usually a single-digit to low double-digit euro amount, often including a class. Each listing shows the price, but check it with the organiser.'),
     (f'Wie trage ich meinen Social in {de} ein?', f'How do I list my social in {en}?',
      'Über das <a href="bachata-socials.html#eintragen">kostenlose Formular</a>. Wir prüfen den Eintrag und schalten ihn frei.', 'Use the <a href="bachata-socials.html#eintragen">free form</a>. We review the listing and publish it.'),
    ]
    guide_page(slug, 'bp' + key[:2],
      f'Bachata Party {de}: Socials und Termine 2026',
      f'Bachata Party {de}: {n} regelmäßige Socials nach Wochentag, mit Ort, Uhrzeit, Preis und Tipps für Anfänger. Stand Oktober 2026.',
      f'Bachata party {en}: socials and dates 2026',
      f'Bachata party {en}: {n} regular socials by weekday with place, time, price and tips for beginners. As of October 2026.',
      f'Bachata Party {de}', (f'Bachata Party {de} · 2026', f'Bachata party {en} · 2026'),
      (f'Bachata Party {de}: <em class="foil">Socials</em> nach Wochentag', f'Bachata party {en}: <em class="foil">socials</em> by weekday'),
      (f'Alle regelmäßigen Bachata-Partys und Socials in {de} auf einen Blick: Wochentag, Ort, Uhrzeit, Preis und Karte, dazu Tipps für deinen ersten Social.',
       f'All regular Bachata parties and socials in {en} at a glance: weekday, place, time, price and map, plus tips for your first social.'),
      [('cal', f'<b>{n} Socials</b> in {de}', f'<b>{n} socials</b> in {en}'), ('clock', f'<b>{day_de}</b>', f'<b>{day_en}</b>'), ('check', 'Stand <b>Oktober 2026</b>', 'As of <b>October 2026</b>')],
      secs, faq, ranking_anchor=key, sibling_group='city')

for _k in CITY_LABEL:
    if _k in EV_BY_CITY: party_page(_k)


# ======================================================================
# THREE GUIDES (added 2026-10-29): Bachata Tanzkurs, Bachata für Anfänger, Bachata Ladies Styling
# SERP check 2026-10-29: results for these terms are mostly course listings, university sport pages and Meetup, few editorial guides.
# No prices or durations are stated: they differ by school and were not verified.
# ======================================================================
LINK_TANZEN = '<a href="bachata-tanzen.html">Bachata tanzen lernen</a>'
LINK_TANZEN_EN = '<a href="bachata-tanzen.html">Learn to dance Bachata</a>'
LINK_GRUND = '<a href="bachata-grundschritt.html">Bachata-Grundschritt</a>'
LINK_GRUND_EN = '<a href="bachata-grundschritt.html">Bachata basic step</a>'
LINK_KURS = '<a href="bachata-tanzkurs.html">Bachata Tanzkurs</a>'
LINK_KURS_EN = '<a href="bachata-tanzkurs.html">Bachata dance course</a>'
LINK_ANF = '<a href="bachata-fuer-anfaenger.html">Bachata für Anfänger</a>'
LINK_ANF_EN = '<a href="bachata-fuer-anfaenger.html">Bachata for beginners</a>'
LINK_SENS = '<a href="bachata-sensual.html">Bachata Sensual</a>'
LINK_DOM = '<a href="bachata-dominicana.html">Bachata Dominicana</a>'
RANK_P = ('Das offizielle Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>, die Methode steht auf der <a href="deutschland.html#method">Startseite</a>. Schulen können sich bis zum 30. November <a href="bewerbung.html">kostenlos bewerben</a>.',
          'The official ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>, and the method is on the <a href="deutschland.html#method">homepage</a>. Schools can <a href="bewerbung.html">apply for free</a> until November 30.')

# ---------------------------------------------------------------- Bachata Tanzkurs
kurs_sections = [
 ('Bachata Tanzkurs: Das Wichtigste in Kürze', 'Bachata dance course: the essentials', [
   ('p', f'Ein Bachata-Tanzkurs bringt dir Grundschritt, Führen und Folgen mit Musik bei. Die Lehrer korrigieren deine Haltung, und du tanzt mit wechselnden Partnern. Das geht schneller, als allein vor dem Video zu üben. Du brauchst keine Vorkenntnisse und in den meisten Einsteigerkursen auch keinen Partner.',
         f'A Bachata dance course teaches you the basic step, leading and following with music. The teachers correct your posture, and you dance with rotating partners. That is faster than practising alone in front of a video. You need no previous experience and, in most beginner classes, no partner.'),
   ('p', f'Bachata stammt aus der Dominikanischen Republik ({WIKI}). Die Schulen unterscheiden sich in Stil, Gruppengröße und Preis. Hier siehst du die Kursformen, den Ablauf einer Stunde und die Fragen, die du vor der Anmeldung stellen solltest.',
         f'Bachata comes from the Dominican Republic ({WIKI_EN}). Schools differ in style, group size and price. Here you see the course formats, how a class runs and the questions to ask before you sign up.'),
 ]),
 ('Kursformen im Überblick', 'Course formats at a glance', [
   ('ul', [
     ('<strong>Gruppenkurs:</strong> Eine feste Gruppe trifft sich regelmäßig, die Stufen reichen vom Anfänger bis zur Mittelstufe.', '<strong>Group course:</strong> a fixed group meets regularly, with levels from beginner to intermediate.'),
     ('<strong>Einsteigerkurs ohne Partner:</strong> Du kommst allein, die Partner wechseln während der Stunde.', '<strong>Beginner course without a partner:</strong> you come alone and partners rotate during the class.'),
     ('<strong>Wochenend- oder Intensivkurs:</strong> Mehrere Stunden an einem oder zwei Tagen, gut für einen schnellen Einstieg oder zum Auffrischen.', '<strong>Weekend or intensive course:</strong> several hours over one or two days, good for a fast start or a refresher.'),
     ('<strong>Workshop:</strong> Einzelne Termine zu einem Thema, etwa Drehungen, Musikalität oder Styling.', '<strong>Workshop:</strong> single sessions on one topic, such as turns, musicality or styling.'),
     ('<strong>Privatstunde:</strong> Der Lehrer arbeitet nur mit dir oder deinem Partner. Das passt, wenn du ein festes Ziel hast, zum Beispiel einen Hochzeitstanz.', '<strong>Private lesson:</strong> the teacher works only with you or your partner. It fits when you have a fixed goal, for example a wedding dance.'),
     ('<strong>Hochschulsport:</strong> Mehrere Hochschulen haben Bachata im Programm. Frag bei deiner Hochschule nach dem aktuellen Angebot.', '<strong>University sport:</strong> several universities have Bachata in their programme. Ask your university about the current offer.'),
     ('<strong>Online-Kurs:</strong> Videokurse helfen beim Üben zwischen den Stunden. Führen und Folgen lernst du am besten mit echten Partnern.', '<strong>Online course:</strong> video courses help with practice between classes. You learn leading and following best with real partners.'),
   ]),
 ]),
 ('So läuft eine Bachata-Stunde ab', 'How a Bachata class runs', [
   ('p', 'Die Reihenfolge unterscheidet sich je nach Schule. Eine typische Stunde sieht so aus:', 'The order differs by school. A typical class looks like this:'),
   ('ul', [
     ('<strong>Aufwärmen:</strong> Hüfte, Knie und Schultern lockern, oft schon zur Musik.', '<strong>Warm-up:</strong> loosen hips, knees and shoulders, often already to music.'),
     ('<strong>Grundschritt:</strong> Der Lehrer wiederholt den Ablauf aus der letzten Stunde, mehr dazu im Ratgeber zum ' + LINK_GRUND + '.', '<strong>Basic step:</strong> the teacher repeats the pattern from the last class, more in the guide to the ' + LINK_GRUND_EN + '.'),
     ('<strong>Neuer Baustein:</strong> Eine Figur oder Technik, erst allein und in Etappen, dann mit Partner.', '<strong>New building block:</strong> a figure or technique, first alone and in stages, then with a partner.'),
     ('<strong>Partnerwechsel:</strong> Du übst mit mehreren Partnern und lernst, dich auf unterschiedliche Menschen einzustellen.', '<strong>Partner rotation:</strong> you practise with several partners and learn to adapt to different people.'),
     ('<strong>Freies Tanzen:</strong> Zum Schluss laufen oft Lieder, zu denen du das Gelernte ausprobierst.', '<strong>Free dancing:</strong> at the end, songs often play so you can try out what you learned.'),
   ]),
 ]),
 ('Welches Level passt zu dir?', 'Which level suits you?', [
   ('ul', [
     ('<strong>Einsteiger:</strong> Du hast noch nie Bachata getanzt. Dran sind Rhythmus, Grundschritt und einfache Drehungen. Der Ratgeber ' + LINK_ANF + ' zeigt den Einstieg.', '<strong>Beginner:</strong> you have never danced Bachata. The focus is rhythm, basic step and simple turns. The guide ' + LINK_ANF_EN + ' shows the start.'),
     ('<strong>Grundkurs:</strong> Du kennst den Grundschritt und einfache Figuren und willst sicherer führen oder folgen.', '<strong>Improver:</strong> you know the basic step and simple figures and want to lead or follow with more confidence.'),
     ('<strong>Mittelstufe:</strong> Figurenfolgen, Musikalität und der eigene Stil stehen im Mittelpunkt.', '<strong>Intermediate:</strong> figure sequences, musicality and your own style are the focus.'),
   ]),
   ('p', 'Die Namen der Stufen wählt jede Schule selbst. Lies die Beschreibung oder frage in der Probestunde nach.', 'Each school chooses its own level names. Read the description or ask in a trial class.'),
 ]),
 ('Worauf du bei der Kurswahl achtest', 'What to look for when choosing a course', [
   ('ul', [
     ('<strong>Probestunde:</strong> Frag, ob du zuschauen oder mittanzen kannst. So merkst du, ob Lehrstil und Gruppe zu dir passen.', '<strong>Trial class:</strong> ask whether you can watch or join in. This shows whether the teaching style and the group suit you.'),
     ('<strong>Partnerwechsel:</strong> Ein guter Einsteigerkurs wechselt die Partner, damit alle Führen und Folgen lernen.', '<strong>Partner rotation:</strong> a good beginner course rotates partners so everyone learns leading and following.'),
     ('<strong>Gruppengröße:</strong> In kleineren Gruppen bekommst du mehr Korrektur. Frage, wie viele Personen ein Lehrer betreut.', '<strong>Group size:</strong> in smaller groups you get more correction. Ask how many people one teacher looks after.'),
     ('<strong>Stil:</strong> Manche Schulen lehren ' + LINK_SENS + ', andere ' + LINK_DOM + ' oder Moderna. Frage, welcher Stil im Einsteigerkurs dran ist.', '<strong>Style:</strong> some schools teach ' + LINK_SENS + ', others ' + LINK_DOM + ' or Moderna. Ask which style the beginner course covers.'),
     ('<strong>Vertrag und Kündigung:</strong> Lies, wie lange du dich bindest und wann du kündigen kannst. Manche Schulen bieten Kurse ohne Vertragsbindung an.', '<strong>Contract and cancellation:</strong> read how long you commit and when you can cancel. Some schools offer courses without a contract.'),
     ('<strong>Socials:</strong> Eine Schule mit eigener Party gibt dir Gelegenheit, das Gelernte zu tanzen. Eine Übersicht findest du bei den <a href="bachata-socials.html">Bachata-Socials</a>.', '<strong>Socials:</strong> a school with its own party gives you a chance to dance what you learned. See the <a href="bachata-socials.html">Bachata socials</a> overview.'),
     ('<strong>Ort und Zeit:</strong> Einen Kurs, den du gut erreichst, besuchst du eher regelmäßig.', '<strong>Place and time:</strong> you attend a course you can reach easily more regularly.'),
   ]),
   ('p', 'Preise nennen wir hier nicht. Sie unterscheiden sich von Schule zu Schule und stehen auf deren Websites.', 'We do not list prices here. They differ from school to school and are on the school websites.'),
 ]),
 ('Das brauchst du für deinen ersten Kurs', 'What you need for your first course', [
   ('ul', [
     ('<strong>Kleidung:</strong> Bequem und so, dass du dich frei bewegen kannst.', '<strong>Clothing:</strong> comfortable, so you can move freely.'),
     ('<strong>Schuhe:</strong> Eine glatte Sohle erleichtert das Drehen, und die Schuhe sollten festen Halt geben.', '<strong>Shoes:</strong> a smooth sole makes turning easier, and the shoes should hold your foot firmly.'),
     ('<strong>Wasser:</strong> Eine Flasche für die Pausen.', '<strong>Water:</strong> a bottle for the breaks.'),
     ('<strong>Partner:</strong> Nicht nötig. Frage bei der Anmeldung, ob der Kurs für Einzelpersonen offen ist.', '<strong>Partner:</strong> not required. Ask when you sign up whether the course is open to individuals.'),
   ]),
   ('p', 'Rhythmusgefühl wächst beim Üben mit Musik. Du musst es nicht mitbringen.', 'A sense of rhythm grows through practice with music. You do not need to bring it.'),
 ]),
 ('Bachata Tanzkurs in deiner Stadt', 'Bachata dance course in your city', [
   ('p', f'Übersichten über Schulen und Kurse findest du für {CITY_LINKS_DE}. Alle Listen sind alphabetisch und keine Wertung. Allgemeine Grundlagen stehen im Ratgeber {LINK_TANZEN}.',
         f'You will find overviews of schools and classes for {CITY_LINKS_EN}. All lists are alphabetical and not a rating. General basics are in the guide {LINK_TANZEN_EN}.'),
   ('p', RANK_P[0], RANK_P[1]),
 ]),
]

kurs_faq = [
 ('Wie lange dauert ein Bachata-Tanzkurs?', 'How long does a Bachata dance course last?',
  'Das legt die Schule fest. Viele Kurse laufen als Staffel über mehrere Wochen, andere als Wochenendkurs. Die Dauer steht in der Kursbeschreibung.',
  'The school decides. Many courses run as a series over several weeks, others as a weekend course. The length is in the course description.'),
 ('Brauche ich einen Partner für den Bachata-Kurs?', 'Do I need a partner for the Bachata course?',
  'In den meisten Einsteigerkursen nicht. Die Partner wechseln während der Stunde. Frage vor der Anmeldung nach, ob der Kurs für Einzelpersonen offen ist.',
  'Not in most beginner courses. Partners rotate during the class. Ask before signing up whether the course is open to individuals.'),
 ('Kann ich eine Probestunde machen?', 'Can I take a trial class?',
  'Viele Schulen bieten eine an. Frage vor der Anmeldung danach.',
  'Many schools offer one. Ask before you sign up.'),
 ('Was ziehe ich zum Bachata-Kurs an?', 'What do I wear to a Bachata course?',
  'Bequeme Kleidung und Schuhe mit glatter Sohle, die festen Halt geben. Eine Flasche Wasser gehört dazu.',
  'Comfortable clothes and shoes with a smooth sole that hold your foot firmly. Bring a bottle of water.'),
 ('Welchen Stil lerne ich im Einsteigerkurs?', 'Which style do I learn in the beginner course?',
  'Das hängt von der Schule ab. Der Grundschritt ist in allen Stilen ähnlich. Die Ratgeber zu <a href="bachata-sensual.html">Sensual</a> und <a href="bachata-dominicana.html">Dominicana</a> erklären die Unterschiede.',
  'That depends on the school. The basic step is similar in all styles. The guides to <a href="bachata-sensual.html">Sensual</a> and <a href="bachata-dominicana.html">Dominicana</a> explain the differences.'),
 ('Wo finde ich einen Bachata-Kurs in meiner Stadt?', 'Where do I find a Bachata course in my city?',
  f'Übersichten gibt es für {CITY_LINKS_DE}. Das offizielle Ranking folgt am 20. Dezember 2026.',
  f'Overviews exist for {CITY_LINKS_EN}. The official ranking follows on December 20, 2026.'),
]

guide_page('bachata-tanzkurs', 'bk',
  'Bachata Tanzkurs: Formen, Ablauf, Auswahl',
  'Bachata Tanzkurs finden: Kursformen, Ablauf einer Stunde, Level und Fragen vor der Anmeldung. Auch ohne Partner. Mit Links zu Schulen in deiner Stadt.',
  'Bachata dance course: formats, class, choosing',
  'Find a Bachata dance course: formats, how a class runs, levels and questions to ask before signing up. No partner needed, with links to schools in your city.',
  'Bachata Tanzkurs', ('Bachata Tanzkurs · Ratgeber', 'Bachata dance course · Guide'),
  ('Bachata Tanzkurs: <em class="foil">Formen, Ablauf, Auswahl</em>', 'Bachata dance course: <em class="foil">formats, class, choosing</em>'),
  ('So findest du den passenden Bachata-Tanzkurs: Welche Kursformen es gibt, wie eine Stunde abläuft, welches Level zu dir passt und welche Fragen du vor der Anmeldung stellst.',
   'How to find the right Bachata dance course: which formats exist, how a class runs, which level suits you and which questions to ask before you sign up.'),
  [('check', 'Auch <b>ohne Partner</b>', 'Also <b>without a partner</b>'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  kurs_sections, kurs_faq, sibling_group='topic')

# ---------------------------------------------------------------- Bachata für Anfänger
anf_sections = [
 ('Bachata für Anfänger: So startest du ohne Vorkenntnisse', 'Bachata for beginners: how to start with no experience', [
   ('p', 'Wenn du noch nie Bachata getanzt hast, bist du hier richtig. Du brauchst weder Tanzerfahrung noch einen Partner. Mit dem Grundschritt, etwas Musik und regelmäßigem Üben kommst du Schritt für Schritt zu den ersten Liedern.',
         'If you have never danced Bachata, you are in the right place. You need neither dance experience nor a partner. With the basic step, some music and regular practice you get to your first songs step by step.'),
   ('p', f'Dieser Ratgeber zeigt, was du am Anfang brauchst, wie die ersten Wochen aussehen können und was gegen typische Sorgen hilft. Bachata kommt aus der Dominikanischen Republik ({WIKI}).',
         f'This guide shows what you need at the start, what the first weeks can look like and what helps against typical worries. Bachata comes from the Dominican Republic ({WIKI_EN}).'),
 ]),
 ('Was du am Anfang brauchst', 'What you need at the start', [
   ('ul', [
     ('<strong>Kleidung und Schuhe:</strong> Bequeme Kleidung und Schuhe mit glatter Sohle, die festen Halt geben.', '<strong>Clothes and shoes:</strong> comfortable clothes and shoes with a smooth sole that hold your foot firmly.'),
     ('<strong>Zeit:</strong> Eine Stunde im Kurs pro Woche und dazwischen kurze Übungen zu Hause.', '<strong>Time:</strong> one class a week and short practice sessions at home in between.'),
     ('<strong>Musik:</strong> Lieder mit klarem Beat. Langsamere Stücke helfen beim Lernen.', '<strong>Music:</strong> songs with a clear beat. Slower tracks help while learning.'),
     ('<strong>Geduld:</strong> Die ersten Stunden fühlen sich ungewohnt an. Das legt sich mit der Wiederholung.', '<strong>Patience:</strong> the first classes feel unfamiliar. That fades with repetition.'),
   ]),
   ('p', 'Einen Partner brauchst du nicht. In Einsteigerkursen wechseln die Partner. Mehr zur Wahl des Kurses steht im Ratgeber ' + LINK_KURS + '.',
         'You do not need a partner. Partners rotate in beginner courses. More on choosing a course is in the guide ' + LINK_KURS_EN + '.'),
 ]),
 ('Die ersten Wochen: ein möglicher Fahrplan', 'The first weeks: a possible plan', [
   ('p', 'Jede Schule geht anders vor. Diese Reihenfolge dient als Orientierung:', 'Every school works differently. This order is a guide:'),
   ('ul', [
     ('<strong>Woche 1:</strong> Den Takt hören und den Grundschritt auf der Stelle tanzen.', '<strong>Week 1:</strong> hear the beat and dance the basic step on the spot.'),
     ('<strong>Woche 2:</strong> Seitenschritt, dazu vorwärts und rückwärts mit demselben Rhythmus.', '<strong>Week 2:</strong> side step, plus forward and back in the same rhythm.'),
     ('<strong>Woche 3:</strong> Grundhaltung und Verbindung mit dem Partner, erste Übungen zu Führen und Folgen.', '<strong>Week 3:</strong> basic hold and connection with the partner, first exercises in leading and following.'),
     ('<strong>Woche 4:</strong> Eine einfache Drehung der Folgenden und der erste Übungsabend oder Social.', '<strong>Week 4:</strong> a simple turn for the follower and the first practice evening or social.'),
   ]),
   ('p', f'Den Ablauf des Grundschritts erklärt der Ratgeber {LINK_GRUND}.', f'The pattern of the basic step is explained in the guide {LINK_GRUND_EN}.'),
 ]),
 ('Häufige Sorgen von Anfängern', 'Common worries of beginners', [
   ('ul', [
     ('<strong>Ich habe kein Rhythmusgefühl.</strong> Rhythmus lässt sich lernen. Zähle laut mit und höre Bachata mit klarem Beat. Der Grundschritt hat vier Zählzeiten und wiederholt sich.', '<strong>I have no sense of rhythm.</strong> Rhythm can be learned. Count out loud and listen to Bachata with a clear beat. The basic step has four counts and repeats.'),
     ('<strong>Ich habe keinen Partner.</strong> Das ist im Einsteigerkurs normal. Die Partner wechseln, und viele andere kommen auch allein.', '<strong>I have no partner.</strong> That is normal in a beginner course. Partners rotate, and many others come alone too.'),
     ('<strong>Ich mache Fehler.</strong> Das tun alle Anfänger. Die Lehrer korrigieren, und die anderen im Kurs lernen genauso.', '<strong>I make mistakes.</strong> All beginners do. The teachers correct you, and the others in the class are learning the same way.'),
     ('<strong>Ich bin zu alt oder zu unsportlich.</strong> Bachata ist ein Paartanz ohne feste Altersgrenze, und die Bewegungen lassen sich locker und klein tanzen.', '<strong>I am too old or not sporty enough.</strong> Bachata is a partner dance with no fixed age limit, and the movements can be danced relaxed and small.'),
   ]),
 ]),
 ('Bachata-Begriffe für den Einstieg', 'Bachata terms for the start', [
   ('p', 'Im Kurs fallen ein paar Wörter immer wieder. Diese Liste hilft dir beim Einstieg:', 'A few words come up again and again in class. This list helps you get started:'),
   ('ul', [
     ('<strong>Zählzeit:</strong> Einer der Schläge im Takt. Bachata wird in Vierergruppen gezählt, also eins bis vier.', '<strong>Count:</strong> one of the beats in the bar. Bachata is counted in groups of four, one to four.'),
     ('<strong>Führen und Folgen:</strong> Eine Person gibt Impulse, die andere reagiert darauf. Die Rollen kannst du in vielen Kursen wechseln.', '<strong>Leading and following:</strong> one person gives signals and the other responds. In many courses you can switch the roles.'),
     ('<strong>Tap:</strong> Ein kurzes Antippen mit dem Fuß auf der vierten Zählzeit, bei dem das Gewicht auf dem anderen Fuß bleibt.', '<strong>Tap:</strong> a short touch of the foot on count four while the weight stays on the other foot.'),
     ('<strong>Figur:</strong> Eine feste Abfolge von Schritten zu zweit, zum Beispiel eine Drehung.', '<strong>Figure:</strong> a fixed sequence of steps for two, for example a turn.'),
     ('<strong>Social:</strong> Eine Tanzparty, auf der du mit wechselnden Partnern tanzt. Mehr dazu bei den <a href="bachata-socials.html">Bachata-Socials</a>.', '<strong>Social:</strong> a dance party where you dance with changing partners. More at the <a href="bachata-socials.html">Bachata socials</a>.'),
   ]),
 ]),
 ('Zwischen den Stunden üben', 'Practising between classes', [
   ('ul', [
     ('Zehn Minuten Grundschritt zu einem Lied, lieber oft als lang.', 'Ten minutes of basic step to a song, short and often rather than long.'),
     ('Laut mitzählen, bis der Ablauf sitzt.', 'Count out loud until the pattern sits.'),
     ('Langsame Stücke wählen und das Tempo erst später steigern.', 'Choose slow tracks and raise the tempo only later.'),
     ('Vor einem Spiegel üben, ohne ständig auf die Füße zu schauen.', 'Practise in front of a mirror without constantly looking at your feet.'),
   ]),
   ('p', f'Typische Fehler und Übungstipps stehen im Ratgeber {LINK_GRUND}, den Überblick über die Stile gibt {LINK_TANZEN}.',
         f'Typical mistakes and practice tips are in the guide {LINK_GRUND_EN}, and {LINK_TANZEN_EN} gives an overview of the styles.'),
 ]),
 ('Welcher Stil passt für den Einstieg?', 'Which style suits a beginner?', [
   ('p', 'Der Grundschritt ist in allen Stilen ähnlich. Starte mit dem Stil, den deine Schule im Einsteigerkurs lehrt. Später kannst du wechseln oder mehrere lernen.',
         'The basic step is similar in all styles. Start with the style your school teaches in the beginner course. Later you can switch or learn several.'),
   ('ul', [
     ('<strong>Sensual:</strong> Weich und körperbetont, mit enger Verbindung. Mehr im Ratgeber ' + LINK_SENS + '.', '<strong>Sensual:</strong> soft and body-focused with a close connection. More in the guide ' + LINK_SENS + '.'),
     ('<strong>Dominicana:</strong> Fußspiel und schnelle Richtungswechsel. Mehr im Ratgeber ' + LINK_DOM + '.', '<strong>Dominicana:</strong> footwork and quick direction changes. More in the guide ' + LINK_DOM + '.'),
     ('<strong>Moderna:</strong> Drehfiguren und fließende Übergänge.', '<strong>Moderna:</strong> turn patterns and flowing transitions.'),
   ]),
 ]),
 ('Deinen ersten Kurs finden', 'Finding your first course', [
   ('p', f'Kursformen, Level und Fragen für die Anmeldung findest du im Ratgeber {LINK_KURS}. Übersichten über Schulen gibt es für {CITY_LINKS_DE}. Alle Listen sind alphabetisch und keine Wertung.',
         f'Course formats, levels and questions for signing up are in the guide {LINK_KURS_EN}. Overviews of schools exist for {CITY_LINKS_EN}. All lists are alphabetical and not a rating.'),
   ('p', RANK_P[0], RANK_P[1]),
 ]),
]

anf_faq = [
 ('Wie lange dauert es, bis ich Bachata tanzen kann?', 'How long until I can dance Bachata?',
  'Das hängt von Übung und Kurs ab. Den Grundschritt lernen die meisten in der ersten Stunde. Für den ersten Social reichen oft einige Wochen regelmäßiger Teilnahme.',
  'That depends on practice and the course. Most people learn the basic step in the first class. A few weeks of regular classes are often enough for a first social.'),
 ('Brauche ich als Anfänger einen Tanzpartner?', 'Do I need a dance partner as a beginner?',
  'Nein. In Einsteigerkursen wechseln die Partner, und viele kommen allein.',
  'No. Partners rotate in beginner courses, and many people come alone.'),
 ('Muss ich Spanisch können?', 'Do I need to speak Spanish?',
  'Nein. Der Unterricht läuft in der Sprache der Schule, die Zählzeiten lernst du schnell.',
  'No. Classes run in the school language, and you pick up the counts quickly.'),
 ('Welche Schuhe brauche ich?', 'Which shoes do I need?',
  'Schuhe mit glatter Sohle, die festen Halt geben. Spezielle Tanzschuhe sind am Anfang nicht nötig.',
  'Shoes with a smooth sole that hold your foot firmly. Special dance shoes are not needed at the start.'),
 ('Kann ich Bachata auch allein zu Hause lernen?', 'Can I also learn Bachata alone at home?',
  'Den Grundschritt kannst du allein üben. Führen und Folgen lernst du besser im Kurs mit wechselnden Partnern.',
  'You can practise the basic step alone. Leading and following are better learned in class with rotating partners.'),
 ('Wie oft sollte ich üben?', 'How often should I practise?',
  'Kurze Einheiten sind besser als lange. Zehn Minuten Grundschritt mehrmals pro Woche helfen, bis der Ablauf von allein läuft.',
  'Short sessions beat long ones. Ten minutes of basic step several times a week help until the pattern runs on its own.'),
 ('Wo finde ich einen Anfängerkurs?', 'Where do I find a beginner course?',
  f'Übersichten gibt es für {CITY_LINKS_DE}. Das offizielle Ranking folgt am 20. Dezember 2026.',
  f'Overviews exist for {CITY_LINKS_EN}. The official ranking follows on December 20, 2026.'),
]

guide_page('bachata-fuer-anfaenger', 'ba',
  'Bachata für Anfänger: So startest du richtig',
  'Bachata für Anfänger: Was du brauchst, ein Fahrplan für die ersten Wochen und Antworten auf typische Sorgen. Ohne Vorkenntnisse und ohne Partner.',
  'Bachata for beginners: how to start right',
  'Bachata for beginners: what you need, a plan for the first weeks and answers to typical worries. No experience and no partner needed.',
  'Bachata für Anfänger', ('Bachata für Anfänger · Ratgeber', 'Bachata for beginners · Guide'),
  ('Bachata für Anfänger: <em class="foil">So startest du richtig</em>', 'Bachata for beginners: <em class="foil">how to start right</em>'),
  ('Du hast noch nie Bachata getanzt? Hier findest du, was du am Anfang brauchst, einen Fahrplan für die ersten Wochen und Antworten auf die häufigsten Sorgen.',
   'Never danced Bachata? Here is what you need at the start, a plan for the first weeks and answers to the most common worries.'),
  [('check', '<b>Ohne Vorkenntnisse</b> und Partner', '<b>No experience</b> or partner needed'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  anf_sections, anf_faq, sibling_group='topic')

# ---------------------------------------------------------------- Bachata Ladies Styling
lady_sections = [
 ('Bachata Ladies Styling: Das Wichtigste in Kürze', 'Bachata ladies styling: the essentials', [
   ('p', 'Ladies Styling sind die Bewegungen, die die Folgende zusätzlich zum Paartanz ausführt: Körperwellen, Hüftbewegung, Armführung und Fußvariationen. Das Styling macht den eigenen Tanz ausdrucksvoller, ohne den Grundschritt zu verändern.',
         'Ladies styling is the set of movements the follower adds on top of the partner dance: body waves, hip movement, arm styling and footwork variations. Styling makes your own dance more expressive without changing the basic step.'),
   ('p', f'Viele Schulen bieten Ladies Styling als eigenen Kurs oder als Workshop an. Bachata kommt aus der Dominikanischen Republik ({WIKI}), und die einzelnen Stile setzen beim Styling unterschiedliche Schwerpunkte.',
         f'Many schools offer ladies styling as a separate course or as a workshop. Bachata comes from the Dominican Republic ({WIKI_EN}), and the individual styles put different emphasis on styling.'),
 ]),
 ('Was zum Ladies Styling gehört', 'What ladies styling includes', [
   ('ul', [
     ('<strong>Körperwellen und Isolationen:</strong> Einzelne Körperteile bewegen, etwa Brust, Rippen oder Hüfte.', '<strong>Body waves and isolations:</strong> moving single body parts, such as chest, ribs or hips.'),
     ('<strong>Hüftbewegung:</strong> Kleine Kreise und Akzente, die zum Rhythmus passen.', '<strong>Hip movement:</strong> small circles and accents that match the rhythm.'),
     ('<strong>Armführung:</strong> Wohin die Arme gehen und wie sie die Bewegung des Körpers fortsetzen.', '<strong>Arm styling:</strong> where the arms go and how they continue the movement of the body.'),
     ('<strong>Fußvariationen:</strong> Zusätzliche Schritte und Muster im Grundrhythmus.', '<strong>Footwork variations:</strong> extra steps and patterns within the basic rhythm.'),
     ('<strong>Haltung und Blick:</strong> Eine aufrechte Haltung gibt jeder Bewegung mehr Wirkung.', '<strong>Posture and gaze:</strong> an upright posture gives every movement more impact.'),
     ('<strong>Musikalität:</strong> Bewegungen auf die Akzente und Pausen der Musik setzen.', '<strong>Musicality:</strong> placing movements on the accents and pauses of the music.'),
   ]),
 ]),
 ('Für wen ist Ladies Styling?', 'Who is ladies styling for?', [
   ('p', 'Du solltest den Grundschritt kennen, bevor du mit Styling beginnst. Einige Anbieter haben Styling-Kurse für Einsteiger. Das Wort „Ladies“ beschreibt in der Regel die Rolle der Folgenden. Ob ein Kurs für alle offen ist, entscheidet die Schule, frage danach.',
         'You should know the basic step before you start styling. Some providers have styling courses for beginners. The word "ladies" usually describes the follower role. Whether a course is open to everyone is up to the school, so ask.'),
   ('p', f'Den Grundschritt erklärt der Ratgeber {LINK_GRUND}, den Einstieg der Ratgeber {LINK_ANF}.', f'The basic step is explained in the guide {LINK_GRUND_EN}, and the start in the guide {LINK_ANF_EN}.'),
 ]),
 ('Ladies Styling lernen: Kurs, Workshop oder online', 'Learning ladies styling: course, workshop or online', [
   ('ul', [
     ('<strong>Workshop:</strong> Ein einzelner Termin zu einem Thema. Workshops gibt es bei Schulen und bei Festivals, mehr unter <a href="bachata-festivals-deutschland.html">Bachata-Festivals</a>.', '<strong>Workshop:</strong> a single session on one topic. Workshops run at schools and at festivals, more under <a href="bachata-festivals-deutschland.html">Bachata festivals</a>.'),
     ('<strong>Regelmäßiger Kurs:</strong> Du arbeitest über mehrere Termine an Technik und Ausdruck.', '<strong>Regular course:</strong> you work on technique and expression over several sessions.'),
     ('<strong>Privatstunde:</strong> Der Lehrer korrigiert dich einzeln und passt die Übungen an dich an.', '<strong>Private lesson:</strong> the teacher corrects you individually and adapts the exercises to you.'),
     ('<strong>Online-Kurs:</strong> Es gibt Videokurse zum Styling. Dir fehlt dabei die Korrektur, also nutze einen Spiegel oder nimm dich auf Video auf.', '<strong>Online course:</strong> styling video courses exist. You miss the correction, so use a mirror or record yourself on video.'),
   ]),
   ('p', f'Allgemeine Hinweise zur Kurswahl stehen im Ratgeber {LINK_KURS}.', f'General tips on choosing a course are in the guide {LINK_KURS_EN}.'),
 ]),
 ('Drei erste Übungen für Ladies Styling', 'Three first exercises for ladies styling', [
   ('p', 'Diese Übungen kannst du ohne Partner machen. Beginne langsam und achte auf lockere Knie.', 'You can do these exercises without a partner. Start slowly and keep your knees relaxed.'),
   ('ul', [
     ('<strong>Hüftkreis:</strong> Stehe mit leicht gebeugten Knien und zeichne mit der Hüfte einen kleinen Kreis. Ein Kreis pro Zählzeitgruppe reicht zum Anfang.', '<strong>Hip circle:</strong> stand with slightly bent knees and draw a small circle with your hips. One circle per group of counts is enough at the start.'),
     ('<strong>Rippenbewegung:</strong> Schiebe die Rippen abwechselnd nach rechts und links, ohne die Hüfte mitzunehmen. Das trainiert die Isolation.', '<strong>Rib movement:</strong> slide the ribs alternately to the right and left without taking the hips along. This trains isolation.'),
     ('<strong>Arm auf die Zählzeit:</strong> Tanze den Grundschritt und hebe auf jeder vierten Zählzeit einen Arm langsam an. Danach wechselst du den Arm.', '<strong>Arm on the count:</strong> dance the basic step and raise one arm slowly on every fourth count. Then switch arms.'),
   ]),
 ]),
 ('Ladies Styling zu Hause üben', 'Practising ladies styling at home', [
   ('ul', [
     ('Mit einem langsamen Lied beginnen und eine Bewegung nach der anderen üben.', 'Start with a slow song and practise one movement after the other.'),
     ('Vor dem Spiegel arbeiten und Haltung und Armführung kontrollieren.', 'Work in front of a mirror and check posture and arm styling.'),
     ('Dich aufnehmen und das Video mit dem Vorbild aus dem Kurs vergleichen.', 'Record yourself and compare the video with the example from class.'),
     ('Erst die Einzelbewegung sicher machen, dann mit dem Grundschritt verbinden.', 'Make the single movement secure first, then combine it with the basic step.'),
     ('Aufwärmen und bei Schmerzen eine Pause machen.', 'Warm up and take a break if something hurts.'),
   ]),
 ]),
 ('Ladies Styling in den Stilen: Sensual, Dominicana, Moderna', 'Ladies styling across the styles: Sensual, Dominicana, Moderna', [
   ('ul', [
     ('<strong>Sensual:</strong> Weiche Wellen und Isolationen, eine enge Verbindung. Mehr im Ratgeber ' + LINK_SENS + '.', '<strong>Sensual:</strong> soft waves and isolations with a close connection. More in the guide ' + LINK_SENS + '.'),
     ('<strong>Dominicana:</strong> Fußspiel und Spielfreude, das Styling kommt aus den Schritten. Mehr im Ratgeber ' + LINK_DOM + '.', '<strong>Dominicana:</strong> footwork and playfulness, with the styling coming out of the steps. More in the guide ' + LINK_DOM + '.'),
     ('<strong>Moderna:</strong> Drehungen und fließende Übergänge, bei denen die Arme viel Ausdruck tragen.', '<strong>Moderna:</strong> turns and flowing transitions where the arms carry much of the expression.'),
   ]),
   ('p', f'Einen Überblick über die Stile gibt der Ratgeber {LINK_TANZEN}.', f'The guide {LINK_TANZEN_EN} gives an overview of the styles.'),
 ]),
 ('Schuhe, Kleidung und Sicherheit', 'Shoes, clothing and safety', [
   ('ul', [
     ('<strong>Schuhe:</strong> Wähle eine Sohle, mit der du gut drehen kannst. Absätze sind optional. Trage sie erst, wenn du sicher stehst.', '<strong>Shoes:</strong> choose a sole you can turn well on. Heels are optional. Wear them only when you stand securely.'),
     ('<strong>Kleidung:</strong> Bequem und so, dass Hüfte und Arme frei bleiben.', '<strong>Clothing:</strong> comfortable, so hips and arms stay free.'),
     ('<strong>Aufwärmen:</strong> Hüfte, Rücken und Knie lockern, bevor du Isolationen übst.', '<strong>Warm-up:</strong> loosen hips, back and knees before you practise isolations.'),
   ]),
 ]),
 ('Kurse und Workshops finden', 'Finding courses and workshops', [
   ('p', f'Frage bei Schulen in deiner Stadt nach Styling-Kursen und Workshops. Übersichten über Schulen gibt es für {CITY_LINKS_DE}. Alle Listen sind alphabetisch und keine Wertung.',
         f'Ask schools in your city about styling courses and workshops. Overviews of schools exist for {CITY_LINKS_EN}. All lists are alphabetical and not a rating.'),
   ('p', RANK_P[0], RANK_P[1]),
 ]),
]

lady_faq = [
 ('Was ist Bachata Ladies Styling?', 'What is bachata ladies styling?',
  'Es sind die Bewegungen der Folgenden zusätzlich zum Paartanz, etwa Körperwellen, Hüftbewegung, Armführung und Fußvariationen.',
  'It is the set of movements the follower adds on top of the partner dance, such as body waves, hip movement, arm styling and footwork variations.'),
 ('Brauche ich Vorkenntnisse für Ladies Styling?', 'Do I need experience for ladies styling?',
  'Du solltest den Grundschritt kennen. Einige Anbieter haben Styling-Kurse für Einsteiger. Frage bei der Schule nach.',
  'You should know the basic step. Some providers have styling courses for beginners. Ask the school.'),
 ('Brauche ich Absatzschuhe?', 'Do I need heels?',
  'Nein. Wähle eine Sohle, mit der du gut drehen kannst. Absätze trägst du, wenn du sicher stehst.',
  'No. Choose a sole you can turn well on. Wear heels once you stand securely.'),
 ('Kann ich Ladies Styling online lernen?', 'Can I learn ladies styling online?',
  'Ja, es gibt Videokurse. Dir fehlt die Korrektur, also übe vor dem Spiegel oder nimm dich auf Video auf.',
  'Yes, video courses exist. You miss the correction, so practise in front of a mirror or record yourself.'),
 ('Gehört Styling zu jedem Bachata-Stil?', 'Is styling part of every Bachata style?',
  'Ja, aber mit anderen Schwerpunkten. Sensual setzt auf Wellen, Dominicana auf Fußspiel, Moderna auf Drehungen und Arme.',
  'Yes, but with different emphasis. Sensual focuses on waves, Dominicana on footwork, Moderna on turns and arms.'),
 ('Wie lange dauert es, Ladies Styling zu lernen?', 'How long does it take to learn ladies styling?',
  'Das hängt von deiner Erfahrung und der Übung ab. Einzelne Bewegungen lernst du schnell, den Ausdruck zur Musik entwickelst du über Monate des regelmäßigen Übens.',
  'That depends on your experience and practice. You learn single movements quickly, while expression to the music develops over months of regular practice.'),
 ('Wo finde ich Ladies-Styling-Kurse in meiner Stadt?', 'Where do I find ladies styling courses in my city?',
  f'Frage bei den Schulen nach. Übersichten gibt es für {CITY_LINKS_DE}.',
  f'Ask the schools. Overviews exist for {CITY_LINKS_EN}.'),
]

guide_page('bachata-ladies-styling', 'bl',
  'Bachata Ladies Styling: Was es ist, wie du es lernst',
  'Bachata Ladies Styling: Körperwellen, Hüfte, Arme und Fußvariationen. Was dazugehört, wie du es lernst und übst, und worauf du bei Schuhen achtest.',
  'Bachata ladies styling: what it is, how to learn it',
  'Bachata ladies styling: body waves, hips, arms and footwork variations. What it includes, how to learn and practise it, and what to look for in shoes.',
  'Bachata Ladies Styling', ('Bachata Ladies Styling · Ratgeber', 'Bachata ladies styling · Guide'),
  ('Bachata Ladies Styling: <em class="foil">Was es ist, wie du es lernst</em>', 'Bachata ladies styling: <em class="foil">what it is, how to learn it</em>'),
  ('Körperwellen, Hüfte, Arme und Fußvariationen: Hier erfährst du, was Ladies Styling in der Bachata ist, wie du es im Kurs oder zu Hause lernst und worauf du bei Schuhen achtest.',
   'Body waves, hips, arms and footwork variations: here you learn what ladies styling in Bachata is, how to learn it in class or at home and what to look for in shoes.'),
  [('check', 'Für <b>Folgende</b> mit Grundschritt', 'For <b>followers</b> who know the basic step'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  lady_sections, lady_faq, sibling_group='topic')

# ======================================================================
# TWO GUIDES (added 2026-10-29): Bachata Moderna, Bachata Party (Ablauf & Etikette)
# SERP check 2026-10-29: "bachata moderna" -> style overviews and wiki pages, no German course guide.
# "bachata party" -> event listings; we already have bachata-socials.html, so this page targets
# the how-it-works / etiquette / first-time angle and links to the socials listing (no cannibalisation).
# Facts about Moderna come only from SalsaVida (via existing site text): turn patterns, wraps, structured partnerwork.
# No prices, no invented history.
# ======================================================================
LINK_SOCIALS = '<a href="bachata-socials.html">Bachata-Socials in Deutschland</a>'
LINK_SOCIALS_EN = '<a href="bachata-socials.html">Bachata socials in Germany</a>'
LINK_FEST = '<a href="bachata-festivals-deutschland.html">Bachata-Festivals</a>'
LINK_FEST_EN = '<a href="bachata-festivals-deutschland.html">Bachata festivals</a>'
LINK_LADY = '<a href="bachata-ladies-styling.html">Bachata Ladies Styling</a>'
LINK_LADY_EN = '<a href="bachata-ladies-styling.html">Bachata ladies styling</a>'
LINK_MOD = '<a href="bachata-moderna.html">Bachata Moderna</a>'
LINK_MOD_EN = '<a href="bachata-moderna.html">Bachata Moderna</a>'

LINK_PARTY = '<a href="bachata-party.html">Bachata Party</a>'
LINK_PARTY_EN = '<a href="bachata-party.html">Bachata party</a>'
# ---------------------------------------------------------------- Bachata Moderna
mod_sections = [
 ('Bachata Moderna: Das Wichtigste in Kürze', 'Bachata Moderna: the essentials', [
   ('p', f'Bachata Moderna ist ein Partnertanz-Stil mit Drehmustern, Wraps und klar strukturierter Partnerarbeit. Er ist von Salsa und Gesellschaftstanz geprägt und gilt als der musterorientierteste der drei Hauptstile. Die Basis bleibt der Bachata-Grundschritt aus der Dominikanischen Republik ({WIKI}).',
         f'Bachata Moderna is a partner-dance style with turn patterns, wraps and clearly structured partnerwork. It is shaped by salsa and ballroom and is considered the most pattern-driven of the three main styles. The base remains the Bachata basic step from the Dominican Republic ({WIKI_EN}).'),
   ('p', 'Viele Einsteigerkurse beginnen mit Moderna, weil sich Figuren Schritt für Schritt erklären lassen. Hier siehst du, was den Stil ausmacht, wie er sich von Sensual und Dominicana unterscheidet und wie du den Einstieg findest.',
         'Many beginner classes start with Moderna because figures can be explained step by step. Here you see what defines the style, how it differs from Sensual and Dominicana and how to get started.'),
 ]),
 ('Was Bachata Moderna ausmacht', 'What defines Bachata Moderna', [
   ('ul', [
     ('<strong>Drehmuster:</strong> Die Folgende dreht sich unter dem Arm der Führenden, einfach oder mehrfach, oft in Ketten.', '<strong>Turn patterns:</strong> the follower turns under the leader\'s arm, single or multiple, often in chains.'),
     ('<strong>Wraps:</strong> Die Arme werden um den Körper gewickelt und wieder gelöst, ein typisches Merkmal des Stils.', '<strong>Wraps:</strong> the arms are wrapped around the body and released again, a typical feature of the style.'),
     ('<strong>Strukturierte Partnerarbeit:</strong> Figuren haben einen klaren Ablauf, den man lernen und wiederholen kann.', '<strong>Structured partnerwork:</strong> figures have a clear sequence that you can learn and repeat.'),
     ('<strong>Offene und geschlossene Haltung:</strong> Der Tanz wechselt zwischen Abstand und Nähe, je nach Figur.', '<strong>Open and closed hold:</strong> the dance moves between distance and closeness, depending on the figure.'),
     ('<strong>Klare Führung:</strong> Das Führen läuft über Hand und Arm, deshalb ist Verbindung wichtig.', '<strong>Clear leading:</strong> leading works through hand and arm, so connection matters.'),
   ]),
   ('p', 'Dass Salsa und Gesellschaftstanz den Stil geprägt haben, beschreibt SalsaVida in seinem Überblick über die Bachata-Stile. Salsa-Tänzer finden sich in Moderna deshalb oft schnell zurecht.',
         'SalsaVida describes in its overview of Bachata styles that salsa and ballroom shaped the style. Salsa dancers therefore often find their way into Moderna quickly.'),
 ]),
 ('Moderna, Sensual und Dominicana im Vergleich', 'Moderna, Sensual and Dominicana compared', [
   ('ul', [
     ('<strong>Moderna:</strong> Drehungen, Wraps und feste Abläufe. Mehr Struktur, weniger Improvisation.', '<strong>Moderna:</strong> turns, wraps and fixed sequences. More structure, less improvisation.'),
     ('<strong>Sensual:</strong> Weicher und fließender, mit Körperbewegung, Isolationen und enger Haltung. Mehr im Ratgeber ' + LINK_SENS + '.', '<strong>Sensual:</strong> softer and more fluid, with body movement, isolations and a close hold. More in the guide ' + LINK_SENS + '.'),
     ('<strong>Dominicana:</strong> Fußarbeit, Spielfreude und schnelle Richtungswechsel, Figurenketten spielen eine kleinere Rolle. Mehr im Ratgeber ' + LINK_DOM + '.', '<strong>Dominicana:</strong> footwork, playfulness and quick direction changes, with figure chains playing a smaller role. More in the guide ' + LINK_DOM + '.'),
   ]),
   ('p', 'Die Begriffe werden nicht überall gleich verwendet. Eine Berliner Schule nennt Bachata Sensual auch Fusion oder Moderna. Frag deshalb in der Probestunde, was im Kurs gelehrt wird, statt dich nur nach dem Namen zu richten.',
         'The terms are not used the same way everywhere. One Berlin school also calls Bachata Sensual Fusion or Moderna. So ask in the trial class what the course teaches instead of going by the name alone.'),
 ]),
 ('Bachata Moderna lernen: So fängst du an', 'Learning Bachata Moderna: how to start', [
   ('ul', [
     ('<strong>Grundschritt zuerst:</strong> Drei Schritte, Tap auf vier. Ohne sicheres Timing geraten Drehungen aus dem Takt. Der Ratgeber ' + LINK_GRUND + ' erklärt ihn.', '<strong>Basic step first:</strong> three steps, tap on four. Without secure timing, turns fall off the beat. The guide ' + LINK_GRUND_EN + ' explains it.'),
     ('<strong>Einfache Drehung:</strong> Übe eine einzelne Drehung unter dem Arm, bevor du Ketten tanzt.', '<strong>Simple turn:</strong> practise a single turn under the arm before you dance chains.'),
     ('<strong>Spotting:</strong> Fixiere beim Drehen einen Punkt, damit dir nicht schwindelig wird.', '<strong>Spotting:</strong> fix one point while turning so you do not get dizzy.'),
     ('<strong>Weiche Arme:</strong> Die Führende zieht nicht, die Folgende hält nicht dagegen. Beide halten Spannung, ohne zu verkrampfen.', '<strong>Soft arms:</strong> the leader does not pull and the follower does not resist. Both keep tension without tightening up.'),
     ('<strong>Partner wechseln:</strong> In Kursen mit Partnerwechsel übst du Führung und Verbindung mit vielen Menschen.', '<strong>Rotate partners:</strong> in classes with partner rotation you practise leading and connection with many people.'),
   ]),
   ('p', f'Der Einstieg ohne Vorkenntnisse ist im Ratgeber {LINK_ANF} beschrieben, die Kursformen stehen im Ratgeber {LINK_KURS}.',
         f'Starting without experience is described in the guide {LINK_ANF_EN}, and the course formats are in the guide {LINK_KURS_EN}.'),
 ]),
 ('Wie eine Moderna-Stunde abläuft', 'How a Moderna class runs', [
   ('p', 'Die Abläufe unterscheiden sich je nach Schule. Häufig beginnt die Stunde mit Aufwärmen und Grundschritt. Danach lernst du eine neue Figur in kleinen Teilen und wiederholst sie mit wechselnden Partnern. Am Ende steht oft eine kurze Kombination zur Musik. Frag in der Probestunde, wie dein Kurs aufgebaut ist.',
         'The format differs by school. Often the class starts with a warm-up and the basic step. Then you learn a new figure in small parts and repeat it with rotating partners. At the end there is often a short combination to the music. Ask in the trial class how your course is structured.'),
 ]),
 ('Typische Fehler in Moderna', 'Common mistakes in Moderna', [
   ('ul', [
     ('<strong>Zu viel Kraft:</strong> Wer die Folgende durch die Figur zieht, verliert die Musik. Führe mit kleinen, klaren Impulsen.', '<strong>Too much force:</strong> pulling the follower through a figure loses the music. Lead with small, clear signals.'),
     ('<strong>Figuren statt Musik:</strong> Eine lange Kette passt nicht zu jedem Lied. Höre auf Pausen und Akzente.', '<strong>Figures instead of music:</strong> a long chain does not fit every song. Listen for breaks and accents.'),
     ('<strong>Grundschritt vergessen:</strong> Zwischen den Figuren läuft der Grundschritt weiter.', '<strong>Forgetting the basic step:</strong> the basic step keeps going between figures.'),
     ('<strong>Keine Rückmeldung:</strong> Sage deinem Partner freundlich, wenn dir ein Wrap oder eine Drehung unangenehm ist.', '<strong>No feedback:</strong> tell your partner kindly if a wrap or a turn feels uncomfortable.'),
   ]),
 ]),
 ('Moderna auf Partys und Festivals', 'Moderna at parties and festivals', [
   ('p', f'Auf Socials tanzt du Moderna mit wechselnden Partnern. Das klappt am besten mit Figuren, die du sicher kennst. Wie ein Abend abläuft, steht im Ratgeber {LINK_PARTY}. Eine Übersicht regelmäßiger Partys gibt die Seite {LINK_SOCIALS}, Workshops findest du bei den {LINK_FEST}.',
         f'At socials you dance Moderna with rotating partners. That works best with figures you know well. How an evening runs is in the guide {LINK_PARTY_EN}. An overview of regular parties is on the page {LINK_SOCIALS_EN}, and you find workshops at the {LINK_FEST_EN}.'),
 ]),
 ('Moderna-Kurse in deiner Stadt finden', 'Finding Moderna classes in your city', [
   ('p', f'Schau auf den Seiten der Schulen nach dem Stil, und frage nach einer Probestunde. Übersichten über Schulen gibt es für {CITY_LINKS_DE}. Alle Listen sind alphabetisch und keine Wertung.',
         f'Check the schools\' pages for the style and ask for a trial class. Overviews of schools exist for {CITY_LINKS_EN}. All lists are alphabetical and not a rating.'),
   ('p', RANK_P[0], RANK_P[1]),
 ]),
]
mod_faq = [
 ('Was ist Bachata Moderna?', 'What is Bachata Moderna?',
  'Ein Partnertanz-Stil mit Drehmustern, Wraps und strukturierter Partnerarbeit, geprägt von Salsa und Gesellschaftstanz.',
  'A partner-dance style with turn patterns, wraps and structured partnerwork, shaped by salsa and ballroom.'),
 ('Was ist der Unterschied zwischen Moderna und Sensual?', 'What is the difference between Moderna and Sensual?',
  'Moderna setzt auf Drehungen und feste Abläufe, Sensual auf weiche Körperbewegung und enge Haltung. Manche Schulen verwenden die Namen aber gleichbedeutend.',
  'Moderna focuses on turns and fixed sequences, Sensual on soft body movement and a close hold. Some schools, however, use the names interchangeably.'),
 ('Ist Moderna für Anfänger geeignet?', 'Is Moderna suitable for beginners?',
  'Ja. Viele Einsteigerkurse beginnen mit Moderna, weil sich Figuren schrittweise lernen lassen. Du brauchst zuerst den Grundschritt.',
  'Yes. Many beginner classes start with Moderna because figures can be learned step by step. You need the basic step first.'),
 ('Brauche ich Salsa-Kenntnisse für Moderna?', 'Do I need salsa experience for Moderna?',
  'Nein. Salsa-Tänzer finden sich aber oft schnell zurecht, weil der Stil von Salsa geprägt ist.',
  'No. Salsa dancers often find their way quickly, though, because the style is shaped by salsa.'),
 ('Kann ich Moderna mit Sensual und Dominicana mischen?', 'Can I mix Moderna with Sensual and Dominicana?',
  'Ja. Viele Tänzer mischen die Stile. Der Grundschritt ist derselbe.',
  'Yes. Many dancers mix the styles. The basic step is the same.'),
 ('Wie vermeide ich Schwindel bei Drehungen?', 'How do I avoid dizziness when turning?',
  'Fixiere beim Drehen einen Punkt (Spotting) und beginne mit einzelnen Drehungen.',
  'Fix one point while turning (spotting) and start with single turns.'),
 ('Wo finde ich Moderna-Kurse in meiner Stadt?', 'Where do I find Moderna classes in my city?',
  f'Frage bei den Schulen nach dem Stil und einer Probestunde. Übersichten gibt es für {CITY_LINKS_DE}.',
  f'Ask the schools about the style and a trial class. Overviews exist for {CITY_LINKS_EN}.'),
]

# ---------------------------------------------------------------- Bachata Party
party_sections = [
 ('Bachata Party: Das Wichtigste in Kürze', 'Bachata party: the essentials', [
   ('p', 'Eine Bachata Party, auch Social genannt, ist ein Abend, an dem alle frei tanzen. Viele Veranstalter beginnen mit einem Kurs, danach läuft die Party. Du tanzt mit wechselnden Partnern, niemand erwartet perfekte Technik, und du musst keinen Partner mitbringen.',
         'A Bachata party, also called a social, is an evening where everyone dances freely. Many organisers start with a class and the party follows. You dance with rotating partners, nobody expects perfect technique and you do not need to bring a partner.'),
   ('p', f'Wo regelmäßig getanzt wird, zeigt die Seite {LINK_SOCIALS} mit Ort, Zeit und Preis nach Stadt. Hier erfährst du, wie ein Abend abläuft, was die Etikette ist und wie du dich beim ersten Mal vorbereitest.',
         f'The page {LINK_SOCIALS_EN} shows where regular dancing happens, with place, time and price by city. Here you learn how an evening runs, what the etiquette is and how to prepare for your first time.'),
 ]),
 ('So läuft ein Social ab', 'How a social runs', [
   ('p', 'Die Abläufe unterscheiden sich je nach Veranstalter. Die Berliner und Hamburger Socials auf unserer Seite zeigen typische Muster:',
         'Formats differ by organiser. The Berlin and Hamburg socials on our page show typical patterns:'),
   ('ul', [
     ('<strong>Kurs vor der Party:</strong> Eine Stunde Unterricht, danach beginnt die Party. Das ist ein guter Einstieg, weil du dich warm tanzt.', '<strong>Class before the party:</strong> an hour of teaching, then the party starts. This is a good way in because you warm up.'),
     ('<strong>Workshop mit Party:</strong> Manche Abende kombinieren einen Workshop mit dem Social.', '<strong>Workshop with party:</strong> some evenings combine a workshop with the social.'),
     ('<strong>Offene Tanzfläche:</strong> Die Musik läuft, und jeder fordert andere auf.', '<strong>Open dance floor:</strong> the music plays and everyone asks others to dance.'),
     ('<strong>Mehrere Stile:</strong> Viele Socials mischen Salsa, Bachata und Kizomba, andere spielen nur Bachata.', '<strong>Several styles:</strong> many socials mix salsa, bachata and kizomba, others play only bachata.'),
   ]),
   ('p', 'Zeiten und Preise ändern sich, prüfe sie vor dem Besuch beim Veranstalter.', 'Times and prices change, so check with the organiser before you go.'),
 ]),
 ('Etikette auf der Tanzfläche', 'Dance floor etiquette', [
   ('ul', [
     ('<strong>Auffordern ist normal:</strong> Du darfst jede Person ansprechen, Frauen und Männer. Ein freundliches Lächeln und die Frage reichen.', '<strong>Asking is normal:</strong> you may approach anyone, women and men. A friendly smile and the question are enough.'),
     ('<strong>Nein ist ein vollständiger Satz:</strong> Wer ablehnt, muss das nicht erklären. Bedanke dich und frage jemand anderen.', '<strong>No is a complete sentence:</strong> whoever declines does not have to explain. Say thanks and ask someone else.'),
     ('<strong>Ein Song reicht:</strong> Tanze ein Lied und bedanke dich. Mehrere Tänze mit derselben Person sind ok, wenn beide es wollen.', '<strong>One song is enough:</strong> dance one song and say thanks. Several dances with the same person are fine if both want it.'),
     ('<strong>Nähe nur im Einvernehmen:</strong> Nahe Haltung gehört zu Sensual, aber jeder bestimmt seine Grenze. Achte auf dein Gegenüber.', '<strong>Closeness only by consent:</strong> a close hold belongs to Sensual, but everyone sets their own limit. Pay attention to your partner.'),
     ('<strong>Raum respektieren:</strong> Tanze so, dass du andere Paare nicht anstößt, und entschuldige dich bei Kollisionen.', '<strong>Respect space:</strong> dance so that you do not bump into other couples and apologise after collisions.'),
     ('<strong>Kein Unterricht auf der Fläche:</strong> Gib keine ungefragten Korrekturen. Frag lieber im Kurs nach.', '<strong>No teaching on the floor:</strong> do not give unasked corrections. Ask in class instead.'),
   ]),
 ]),
 ('Dein erstes Mal: Vorbereitung', 'Your first time: preparation', [
   ('ul', [
     ('<strong>Grundschritt lernen:</strong> Ein sicherer Grundschritt reicht. Der Ratgeber ' + LINK_GRUND + ' erklärt ihn, der Ratgeber ' + LINK_ANF + ' den Einstieg.', '<strong>Learn the basic step:</strong> a secure basic step is enough. The guide ' + LINK_GRUND_EN + ' explains it, and the guide ' + LINK_ANF_EN + ' the start.'),
     ('<strong>Früh kommen:</strong> Wenn ein Kurs vor der Party läuft, nutze ihn. Du lernst Leute kennen und tanzt dich ein.', '<strong>Come early:</strong> if a class runs before the party, use it. You meet people and warm up.'),
     ('<strong>Allein kommen:</strong> Ein Partner ist nicht nötig. Viele Besucher kommen allein.', '<strong>Come alone:</strong> a partner is not needed. Many visitors come alone.'),
     ('<strong>Bequem anziehen:</strong> Kleidung, in der du dich bewegen kannst, und Schuhe mit Sohlen, die gut drehen.', '<strong>Dress comfortably:</strong> clothes you can move in and shoes with soles that turn well.'),
     ('<strong>Wasser und Pausen:</strong> Trinke genug und mache Pausen. Zuschauen ist erlaubt.', '<strong>Water and breaks:</strong> drink enough and take breaks. Watching is allowed.'),
   ]),
 ]),
 ('Welchen Stil tanzt du auf der Party?', 'Which style do you dance at the party?', [
   ('p', f'Auf den Partys treffen verschiedene Stile aufeinander. Sensual lebt von Körperbewegung und enger Haltung ({LINK_SENS}), {LINK_MOD} von Drehungen und Wraps, Dominicana von Fußspiel ({LINK_DOM}). Der Grundschritt ist derselbe, deshalb kannst du mit allen tanzen. Ein Überblick steht im Ratgeber {LINK_TANZEN}.',
         f'Different styles meet at parties. Sensual lives on body movement and a close hold ({LINK_SENS}), {LINK_MOD_EN} on turns and wraps, Dominicana on footwork ({LINK_DOM}). The basic step is the same, so you can dance with everyone. An overview is in the guide {LINK_TANZEN_EN}.'),
 ]),
 ('Sicherheit und Wohlbefinden', 'Safety and wellbeing', [
   ('ul', [
     ('<strong>Gute Veranstalter</strong> sagen klar, dass Nein akzeptiert wird. Wenn dir etwas unangenehm ist, sprich die Veranstalter an.', '<strong>Good organisers</strong> state clearly that no is accepted. If something feels uncomfortable, speak to the organisers.'),
     ('<strong>Heimweg planen:</strong> Kläre vorher, wie du nach Hause kommst, besonders bei Partys bis in die Nacht.', '<strong>Plan the way home:</strong> sort out in advance how you get home, especially for parties that run late into the night.'),
     ('<strong>Getränke im Blick behalten:</strong> Lass dein Glas nicht unbeaufsichtigt.', '<strong>Keep an eye on drinks:</strong> do not leave your glass unattended.'),
   ]),
 ]),
 ('Weiter tanzen: Festivals und Workshops', 'Dancing further: festivals and workshops', [
   ('p', f'Wer mehr will, findet auf {LINK_FEST} Workshops, Partys und Tänzer aus vielen Städten. Wie du ein Festival wählst, steht auf der Seite. Wenn du lieber im Kurs übst, hilft der Ratgeber {LINK_KURS}. Für Tanzende in der Rolle der Folgenden gibt es {LINK_LADY}.',
         f'If you want more, {LINK_FEST_EN} offer workshops, parties and dancers from many cities. The page explains how to choose a festival. If you prefer to practise in class, the guide {LINK_KURS_EN} helps. For dancers in the follower role there is {LINK_LADY_EN}.'),
 ]),
 ('Partys und Schulen in deiner Stadt', 'Parties and schools in your city', [
   ('p', f'Städteseiten mit Schulen und Terminen gibt es für {CITY_LINKS_DE}. Alle Listen sind alphabetisch und keine Wertung. Veranstalter können ihren Social kostenlos eintragen.',
         f'City pages with schools and dates exist for {CITY_LINKS_EN}. All lists are alphabetical and not a rating. Organisers can list their social for free.'),
   ('p', RANK_P[0], RANK_P[1]),
 ]),
]
party_faq = [
 ('Was ist eine Bachata Party?', 'What is a bachata party?',
  'Ein Abend zum freien Tanzen mit wechselnden Partnern, oft mit einem Kurs vor der Party. Man nennt ihn auch Social.',
  'An evening of free dancing with rotating partners, often with a class before the party. It is also called a social.'),
 ('Brauche ich einen Partner für eine Bachata Party?', 'Do I need a partner for a bachata party?',
  'Nein. Viele Besucher kommen allein und tanzen mit wechselnden Partnern.',
  'No. Many visitors come alone and dance with rotating partners.'),
 ('Wie gut muss ich tanzen können?', 'How well do I need to dance?',
  'Ein sicherer Grundschritt reicht für den Anfang. Viele Socials beginnen mit einem Kurs, der dir den Einstieg erleichtert.',
  'A secure basic step is enough to start. Many socials begin with a class that makes it easier to get in.'),
 ('Darf ich jemanden zum Tanzen auffordern?', 'May I ask someone to dance?',
  'Ja, das ist normal, bei allen Geschlechtern. Wer ablehnt, muss das nicht erklären.',
  'Yes, that is normal, across all genders. Whoever declines does not have to explain.'),
 ('Was ziehe ich an?', 'What do I wear?',
  'Bequeme Kleidung, in der du dich bewegen kannst, und Schuhe mit Sohlen, die gut drehen. Der Dresscode hängt vom Veranstalter ab.',
  'Comfortable clothes you can move in and shoes with soles that turn well. The dress code depends on the organiser.'),
 ('Was kostet ein Social?', 'What does a social cost?',
  f'Das hängt vom Veranstalter ab. Preise für Beispiele stehen auf der Seite {LINK_SOCIALS}. Prüfe sie vor dem Besuch.',
  f'That depends on the organiser. Example prices are on the page {LINK_SOCIALS_EN}. Check them before you go.'),
 ('Wo finde ich Bachata Partys in meiner Stadt?', 'Where do I find bachata parties in my city?',
  f'Die Seite {LINK_SOCIALS} listet Socials für Berlin, Hamburg, München, Köln und Frankfurt. Städteseiten gibt es für {CITY_LINKS_DE}.',
  f'The page {LINK_SOCIALS_EN} lists socials for Berlin, Hamburg, Munich, Cologne and Frankfurt. City pages exist for {CITY_LINKS_EN}.'),
]

guide_page('bachata-moderna', 'bm',
  'Bachata Moderna: Drehungen, Wraps, Einstieg und Kurse',
  'Bachata Moderna erklärt: Drehmuster, Wraps und strukturierte Partnerarbeit, Unterschied zu Sensual und Dominicana, typische Fehler und wie du den Einstieg findest.',
  'Bachata Moderna: turns, wraps, how to start',
  'Bachata Moderna explained: turn patterns, wraps and structured partnerwork, the difference from Sensual and Dominicana, common mistakes and how to get started.',
  'Bachata Moderna', ('Bachata Moderna · Ratgeber', 'Bachata Moderna · Guide'),
  ('Bachata Moderna: <em class="foil">Drehungen, Wraps, Einstieg</em>', 'Bachata Moderna: <em class="foil">turns, wraps, how to start</em>'),
  ('Drehmuster, Wraps und klare Partnerarbeit: Hier erfährst du, was Bachata Moderna ausmacht, wie sich der Stil von Sensual und Dominicana unterscheidet und wie du ihn lernst.',
   'Turn patterns, wraps and clear partnerwork: here you learn what defines Bachata Moderna, how the style differs from Sensual and Dominicana and how to learn it.'),
  [('check', 'Für <b>Einsteiger</b> mit Grundschritt', 'For <b>beginners</b> with the basic step'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  mod_sections, mod_faq, sibling_group='topic')

guide_page('bachata-party', 'bp',
  'Bachata Party: Ablauf, Etikette, erstes Mal',
  'Bachata Party und Social: So läuft ein Abend ab, welche Etikette gilt und wie du dich beim ersten Mal vorbereitest. Mit Links zu Partys in deiner Stadt.',
  'Bachata party: how it runs, etiquette, first time',
  'Bachata party and social: how an evening runs, which etiquette applies and how to prepare for your first time. With links to parties in your city.',
  'Bachata Party', ('Bachata Party · Ratgeber', 'Bachata party · Guide'),
  ('Bachata Party: <em class="foil">Ablauf, Etikette, erstes Mal</em>', 'Bachata party: <em class="foil">how it runs, etiquette, first time</em>'),
  ('Wie läuft ein Bachata-Social ab, was ist auf der Tanzfläche üblich und wie bereitest du dich vor? Alles für deinen ersten Abend, ohne Partner und ohne Vorkenntnisse.',
   'How does a Bachata social run, what is usual on the dance floor and how do you prepare? Everything for your first evening, without a partner and without experience.'),
  [('check', 'Auch <b>allein</b> möglich', 'Possible <b>alone</b> too'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  party_sections, party_faq, sibling_group='topic')


# ---------------------------------------------------------------- Index of all German cities and schools (crawl path to every page)
_cities = sorted({e['city'] for e in B.SCH}, key=lambda k: B.CITY_NAMES[k][0].lower())
idx_sections = [
 ('Bachata-Städte in Deutschland: Überblick', 'Bachata cities in Germany: overview', [
   ('p', f'Diese Übersicht führt zu allen Städteseiten und Schulprofilen in Deutschland: {len(_cities)} Städte und {len(B.SCH)} Schulen mit Bachata-Kursen. Die Reihenfolge ist alphabetisch und keine Wertung. Das offizielle Ranking erscheint am 20. Dezember 2026, die Methode steht auf der <a href="deutschland.html#method">Startseite</a>.',
         f'This overview leads to all city pages and school profiles in Germany: {len(_cities)} cities and {len(B.SCH)} schools with Bachata classes. The order is alphabetical and not a rating. The official ranking is published on December 20, 2026, and the method is on the <a href="deutschland.html#method">homepage</a>.'),
 ])]
for _k in _cities:
    _de, _en = B.CITY_NAMES[_k]
    _ss = sorted([e for e in B.SCH if e['city'] == _k], key=lambda e: e['name'].lower())
    _blocks = []
    if exists('bachata-' + _k):
        _blocks.append(('p', f'<a href="bachata-{_k}.html">Bachata {_de}: Schulen, Kurse und Partys</a>', f'<a href="bachata-{_k}.html">Bachata {_en}: schools, classes and parties</a>'))
    _blocks.append(('ul', [(f'<a href="schools/{e["slug"]}.html">{e["name"]}</a>', f'<a href="schools/{e["slug"]}.html">{e["name"]}</a>') for e in _ss]))
    idx_sections.append((f'Bachata {_de}', f'Bachata {_en}', _blocks))
idx_faq = [
 ('Was zeigt diese Seite?', 'What does this page show?',
  'Sie listet alle Städte und Schulen in Deutschland, die wir erfasst haben, mit Links zu den Städteseiten und Schulprofilen.',
  'It lists all cities and schools in Germany that we have recorded, with links to the city pages and school profiles.'),
 ('Ist die Reihenfolge eine Wertung?', 'Is the order a rating?',
  'Nein, die Listen sind alphabetisch. Das offizielle Ranking erscheint am 20. Dezember 2026.',
  'No, the lists are alphabetical. The official ranking is published on December 20, 2026.'),
 ('Meine Schule fehlt. Was tun?', 'My school is missing. What can I do?',
  'Schulen können sich kostenlos auf der <a href="bewerbung.html">Bewerbungsseite</a> eintragen.',
  'Schools can enter for free on the <a href="bewerbung.html">application page</a>.'),
]
guide_page('bachata-staedte-deutschland', 'bsd',
  'Bachata Schulen Deutschland: Alle Städte und Schulen',
  'Alle Städte und Bachata-Schulen in Deutschland auf einen Blick: Links zu den Städteseiten und Schulprofilen, alphabetisch und ohne Wertung.',
  'Bachata schools Germany: all cities and schools',
  'All cities and Bachata schools in Germany at a glance: links to the city pages and school profiles, alphabetical and without rating.',
  'Alle Städte und Schulen', ('Bachata Schulen Deutschland · Übersicht', 'Bachata schools Germany · Overview'),
  ('Bachata Schulen in Deutschland: <em class="foil">alle Städte</em>', 'Bachata schools in Germany: <em class="foil">all cities</em>'),
  ('Alle Städte und Schulen mit Bachata-Kursen in Deutschland, mit Links zu den Städteseiten und Schulprofilen.',
   'All cities and schools with Bachata classes in Germany, with links to the city pages and school profiles.'),
  [('check', '<b>Alphabetisch</b>, keine Wertung', '<b>Alphabetical</b>, not a rating'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  idx_sections, idx_faq, sibling_group='topic')

# ---- Bachata Musik (added 2026-11-03) ----
UNESCO = '<a href="https://ich.unesco.org/en/RL/music-and-dance-of-the-dominican-bachata-01514" rel="noopener nofollow" target="_blank">UNESCO</a>'
mus_sections = [
 ('Bachata Musik: Was ist das?', 'Bachata music: what is it?', [
   ('p', f'Bachata Musik stammt aus der Dominikanischen Republik. Laut {UNESCO} entwickelte sie sich aus einer Verbindung des rhythmischen Boleros mit anderen afro-antillanischen Genres wie Son, Cha-Cha-Cha und Merengue. Die Texte handeln von Liebe, Leidenschaft und Nostalgie, und die Musik ist bis heute eng mit dem Tanz verbunden.',
         f'Bachata music comes from the Dominican Republic. According to {UNESCO}, it developed from a fusion of rhythmic bolero with other Afro-Antillean genres such as son, cha-cha-cha and merengue. The lyrics deal with love, passion and nostalgia, and the music is still closely tied to the dance.'),
   ('p', 'Auf dieser Seite findest du die Geschichte der Bachata Musik, die typischen Instrumente, bekannte Künstler und Hinweise, worauf du beim Tanzen zur Musik achtest.',
         'On this page you find the history of Bachata music, the typical instruments, well-known artists and tips on what to listen for when you dance to it.'),
 ]),
 ('Geschichte der Bachata Musik', 'History of Bachata music', [
   ('p', f'Nach {WIKI} entstand Bachata Anfang der 1960er-Jahre. Zuerst war sie vor allem romantische Gitarrenmusik und weniger Tanzmusik. Später übernahmen Musiker Elemente des Merengue, erhöhten das Tempo und spielten Bachata zunehmend zum Tanzen.',
         f'According to {WIKI_EN}, Bachata emerged in the early 1960s. At first it was mainly romantic guitar music rather than dance music. Later, musicians borrowed elements of merengue, raised the tempo and increasingly played Bachata for dancing.'),
   ('p', 'In den 1970er- und 1980er-Jahren galt die Musik als Musik der unteren Schichten und lief kaum im Radio. Um 1990 änderte sich ihr Ansehen, vor allem durch Juan Luis Guerra. Ab 2003 folgte ein Produktionsboom in der hispanischen Karibik.',
         'In the 1970s and 1980s the music was seen as music of the lower classes and was rarely played on the radio. Around 1990 its image changed, largely thanks to Juan Luis Guerra. From 2003 a production boom followed across the Hispanic Caribbean.'),
   ('p', 'Seit 2019 steht die „Music and dance of Dominican Bachata" auf der Repräsentativen Liste des immateriellen Kulturerbes der Menschheit der UNESCO.',
         'Since 2019, "Music and dance of Dominican Bachata" has been on UNESCO\'s Representative List of the Intangible Cultural Heritage of Humanity.'),
 ]),
 ('Instrumente und Rhythmus', 'Instruments and rhythm', [
   ('ul', [
     ('<strong>Gitarre:</strong> Ein oder zwei Gitarren führen die Musik, heute werden häufig auch E-Gitarren eingesetzt.', '<strong>Guitar:</strong> one or two guitars lead the music, and electric guitars are now widely used.'),
     ('<strong>Bongos, Maracas und Güira:</strong> Die Perkussion hält den Rhythmus und gibt dem Tanz seine Betonungen.', '<strong>Bongos, maracas and güira:</strong> the percussion holds the rhythm and gives the dance its accents.'),
     ('<strong>Bass:</strong> Er begleitet die Gitarren und trägt die Zählzeiten.', '<strong>Bass:</strong> it accompanies the guitars and carries the counts.'),
     ('<strong>Gesang:</strong> Meist singt ein Musiker die Hauptstimme.', '<strong>Vocals:</strong> usually one musician sings the lead.'),
   ]),
   ('p', 'Bachata steht im 4/4-Takt. Laut Wikipedia liegt das Tempo zwischen 100 und 160 Schlägen pro Minute. Dazu passt der <a href="bachata-grundschritt.html">Bachata-Grundschritt</a>: drei Schritte und ein Tap auf Zählzeit vier, danach das Ganze in die Gegenrichtung.',
         'Bachata is in 4/4 time. According to Wikipedia, the tempo lies between 100 and 160 beats per minute. The <a href="bachata-grundschritt.html">Bachata basic step</a> fits it: three steps and a tap on count four, then the same in the other direction.'),
 ]),
 ('Bekannte Künstler der Bachata Musik', 'Well-known Bachata artists', [
   ('p', 'Die folgende Auswahl stützt sich auf Wikipedia und ist keine Wertung.',
         'The following selection is based on Wikipedia and is not a rating.'),
   ('ul', [
     ('<strong>Juan Luis Guerra:</strong> Der dominikanische Sänger und Komponist gewann 1992 mit dem Album „Bachata Rosa" einen Grammy.', '<strong>Juan Luis Guerra:</strong> the Dominican singer and composer won a Grammy in 1992 with the album "Bachata Rosa".'),
     ('<strong>Aventura:</strong> Ihr Lied „Obsesión" war das erfolgreichste Bachata-Stück in Deutschland und erreichte im September 2004 Platz 1 der Media-Control-Singlecharts.', '<strong>Aventura:</strong> their song "Obsesión" was the most successful Bachata track in Germany and reached No. 1 on the Media Control singles chart in September 2004.'),
     ('<strong>Romeo Santos:</strong> Der US-Sänger (geboren 1981) zählt zu den führenden Künstlern des Genres.', '<strong>Romeo Santos:</strong> the US singer (born 1981) is listed among the genre\'s leading artists.'),
   ]),
 ]),
 ('Stile der Bachata Musik und des Tanzes', 'Styles of Bachata music and dance', [
   ('p', 'Neben der traditionellen Form gibt es moderne Spielarten. Bachata Urban mischt R&B, Hip-Hop und Reggaeton. Bachata Sensual entstand in den 2010er-Jahren und bringt Körperwellen aus dem Zouk in den Tanz. Mehr dazu findest du in den Ratgebern <a href="bachata-sensual.html">Bachata Sensual</a>, <a href="bachata-dominicana.html">Bachata Dominicana</a> und <a href="bachata-moderna.html">Bachata Moderna</a>.',
         'Besides the traditional form there are modern variants. Bachata Urban mixes in R&B, hip-hop and reggaeton. Bachata Sensual emerged in the 2010s and brings body waves from zouk into the dance. More in the guides <a href="bachata-sensual.html">Bachata Sensual</a>, <a href="bachata-dominicana.html">Bachata Dominicana</a> and <a href="bachata-moderna.html">Bachata Moderna</a>.'),
 ]),
 ('Bachata Musik im Wettbewerb und als Gesellschaftstanz', 'Bachata music in competition and as a social dance', [
   ('p', 'Bachata Musik ist nicht nur Hintergrund für Socials. Laut Wikipedia fand die erste Bachata-Weltmeisterschaft 2005 im italienischen Bassano del Grappa statt, organisiert von der International Dance Organization (IDO). Heute veranstaltet die IDO regelmäßig Welt- und Europameisterschaften. Im Wettbewerb gibt es außerdem eine showorientierte Bachata, die Techniken aus dem lateinamerikanischen Turniertanz nutzt.',
         'Bachata music is not only background for socials. According to Wikipedia, the first Bachata World Championship took place in 2005 in Bassano del Grappa, Italy, organised by the International Dance Organization (IDO). Today the IDO holds world and European championships regularly. Competition also includes a show-oriented Bachata that uses techniques from Latin ballroom dancing.'),
   ('p', 'Für den normalen Tanzabend zählt etwas anderes: Du musst die Lieder nicht kennen, um gut zu tanzen. Wer den Rhythmus hört und den Grundschritt hält, kann zu fast jedem Stück tanzen. Mit der Zeit erkennst du Strophe, Refrain und Gitarrensolo und kannst deine Bewegungen darauf abstimmen.',
         'For a normal dance evening something else counts: you do not need to know the songs to dance well. If you hear the rhythm and hold the basic step, you can dance to almost any track. With time you recognise verse, chorus and guitar solo and can match your movements to them.'),
 ]),
 ('Zur Bachata Musik tanzen: Worauf du achtest', 'Dancing to Bachata music: what to listen for', [
   ('ul', [
     ('<strong>Gitarre und Güira heraushören:</strong> Die Gitarre gibt die Melodie, die Güira die Betonung. Beides hilft dir beim Timing.', '<strong>Pick out guitar and güira:</strong> the guitar carries the melody, the güira the accent. Both help your timing.'),
     ('<strong>Auf Zählzeit vier achten:</strong> Dort sitzt der Tap, im Lied oft eine kleine Betonung.', '<strong>Listen for count four:</strong> that is where the tap sits, often a small accent in the song.'),
     ('<strong>Langsam beginnen:</strong> Zum Üben passen Stücke im unteren Tempobereich, bis der Grundschritt sicher sitzt.', '<strong>Start slowly:</strong> for practice, tracks at the lower end of the tempo range suit you until the basic step is secure.'),
     ('<strong>Stile unterscheiden:</strong> Traditionelle Stücke laden zu Fußarbeit ein, Sensual-Stücke zu weichen Bewegungen.', '<strong>Tell the styles apart:</strong> traditional tracks invite footwork, Sensual tracks invite soft movement.'),
   ]),
   ('p', 'Wie du den Tanz von Grund auf lernst, steht im Ratgeber <a href="bachata-tanzen.html">Bachata tanzen lernen</a>. Wo du ihn übst, zeigt die Seite <a href="bachata-socials.html">Bachata-Socials in Deutschland</a>.',
         'How to learn the dance from scratch is in the guide <a href="bachata-tanzen.html">Learn to dance Bachata</a>. Where to practise it is shown on the page <a href="bachata-socials.html">Bachata socials in Germany</a>.'),
 ]),
 ('Bachata Musik und das Ranking der Schulen', 'Bachata music and the school ranking', [
   ('p', f'Gute Schulen lehren Tanz und Musik zusammen. Schulen in deiner Stadt findest du hier: {CITY_LINKS_DE}. Das offizielle Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>, die Methode steht auf der <a href="deutschland.html#method">Startseite</a>.',
         f'Good schools teach dance and music together. Schools in your city: {CITY_LINKS_EN}. The official ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>, and the method is on the <a href="deutschland.html#method">homepage</a>.'),
   ('p', 'Du leitest eine Schule? <a href="bewerbung.html">Bewirb dich kostenlos bis zum 30. November</a>.',
         'Do you run a school? <a href="bewerbung.html">Apply for free by November 30</a>.'),
 ]),
]
mus_faq = [
 ('Woher kommt Bachata Musik?', 'Where does Bachata music come from?',
  'Aus der Dominikanischen Republik. Sie entstand Anfang der 1960er-Jahre und entwickelte sich laut UNESCO aus dem Bolero und anderen afro-antillanischen Genres.',
  'From the Dominican Republic. It emerged in the early 1960s and, according to UNESCO, developed from bolero and other Afro-Antillean genres.'),
 ('Welche Instrumente gehören zur Bachata Musik?', 'Which instruments belong to Bachata music?',
  'Gitarren (heute oft elektrisch), Bongos, Maracas, Güira und Bass, dazu Gesang.',
  'Guitars (now often electric), bongos, maracas, güira and bass, plus vocals.'),
 ('Wie schnell ist Bachata Musik?', 'How fast is Bachata music?',
  'Laut Wikipedia liegt das Tempo zwischen 100 und 160 Schlägen pro Minute im 4/4-Takt.',
  'According to Wikipedia, the tempo lies between 100 and 160 beats per minute in 4/4 time.'),
 ('Welche Künstler sind bekannt?', 'Which artists are well known?',
  'Zu den bekannten Namen zählen Juan Luis Guerra, Aventura und Romeo Santos.',
  'Well-known names include Juan Luis Guerra, Aventura and Romeo Santos.'),
 ('Ist Bachata Kulturerbe?', 'Is Bachata cultural heritage?',
  'Ja. Seit 2019 steht die Musik und der Tanz der dominikanischen Bachata auf der UNESCO-Liste des immateriellen Kulturerbes.',
  'Yes. Since 2019 the music and dance of Dominican Bachata has been on the UNESCO list of intangible cultural heritage.'),
 ('Wann erscheint das Ranking der Bachata-Schulen?', 'When is the ranking of Bachata schools published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html">ranking page</a>.'),
]
guide_page('bachata-musik', 'bmu',
  'Bachata Musik: Geschichte, Instrumente, Künstler',
  'Bachata Musik erklärt: Herkunft aus der Dominikanischen Republik, Geschichte, Instrumente, Tempo, bekannte Künstler und Tipps zum Tanzen.',
  'Bachata music: history, instruments, artists',
  'Bachata music explained: origin in the Dominican Republic, history, instruments, tempo, well-known artists and tips for dancing to it.',
  'Bachata Musik', ('Bachata Musik · Ratgeber', 'Bachata music · Guide'),
  ('Bachata Musik: <em class="foil">Geschichte, Instrumente</em> und Künstler', 'Bachata music: <em class="foil">history, instruments</em> and artists'),
  ('Bachata Musik kommt aus der Dominikanischen Republik und ist heute UNESCO-Kulturerbe. Hier erfährst du, woher sie stammt, wie sie klingt und worauf du beim Tanzen achtest.',
   'Bachata music comes from the Dominican Republic and is now UNESCO heritage. Here you learn where it comes from, how it sounds and what to listen for when you dance.'),
  [('check', 'Quellen: <b>UNESCO, Wikipedia</b>', 'Sources: <b>UNESCO, Wikipedia</b>'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  mus_sections, mus_faq, sibling_group='topic')

# ---- Bachata Tanzschule (added 2026-11-03) ----
ts_sections = [
 ('Bachata Tanzschule: Was du suchst', 'Bachata dance school: what you are looking for', [
   ('p', f'Eine gute Bachata Tanzschule bringt dir den Tanz Schritt für Schritt bei, ohne dass du Vorkenntnisse oder einen Partner brauchst. Bachata kommt aus der Dominikanischen Republik ({WIKI}) und wird heute in Deutschland in Tanzschulen, Tanzstudios und Vereinen unterrichtet. Das Angebot ist groß, deshalb lohnt sich ein klarer Blick auf ein paar Punkte.',
         f'A good Bachata dance school teaches you the dance step by step, without prior knowledge or a partner. Bachata comes from the Dominican Republic ({WIKI_EN}) and is taught in Germany today in dance schools, studios and clubs. The offer is large, so it is worth looking at a few points.'),
   ('p', 'Diese Seite zeigt dir, woran du eine passende Schule erkennst, welche Fragen du vor dem ersten Kurs stellst und wo du Schulen in deiner Stadt findest.',
         'This page shows you how to recognise a suitable school, which questions to ask before your first class and where to find schools in your city.'),
 ]),
 ('Woran du eine gute Bachata Tanzschule erkennst', 'How to recognise a good Bachata dance school', [
   ('ul', [
     ('<strong>Anfängerkurs mit klarem Plan:</strong> Es sollte beschrieben sein, was du in welchem Kurs lernst, zum Beispiel den <a href="bachata-grundschritt.html">Grundschritt</a>.', '<strong>Beginner class with a clear plan:</strong> it should be described what you learn in which class, for example the <a href="bachata-grundschritt.html">basic step</a>.'),
     ('<strong>Probestunde:</strong> Viele Schulen bieten eine Schnupperstunde an. Frag danach, bevor du dich bindest.', '<strong>Trial class:</strong> many schools offer a taster lesson. Ask for it before you commit.'),
     ('<strong>Stilangabe:</strong> Prüfe, ob der Kurs <a href="bachata-moderna.html">Moderna</a>, <a href="bachata-sensual.html">Sensual</a> oder <a href="bachata-dominicana.html">Dominicana</a> lehrt. Die Begriffe werden nicht überall gleich verwendet.', '<strong>Style information:</strong> check whether the class teaches <a href="bachata-moderna.html">Moderna</a>, <a href="bachata-sensual.html">Sensual</a> or <a href="bachata-dominicana.html">Dominicana</a>. The terms are not used the same way everywhere.'),
     ('<strong>Gruppengröße und Partnerwechsel:</strong> In kleinen Gruppen mit Wechsel lernst du schneller und tanzt später sicherer auf Socials.', '<strong>Group size and rotation:</strong> in small groups with rotation you learn faster and later dance more confidently at socials.'),
     ('<strong>Praxis außerhalb des Kurses:</strong> Übungsabende, Partys und Events zeigen, ob die Schule eine Community aufbaut.', '<strong>Practice outside class:</strong> practice nights, parties and events show whether the school builds a community.'),
   ]),
 ]),
 ('Fragen vor dem ersten Kurs', 'Questions before your first class', [
   ('p', 'Stelle der Schule vor der Anmeldung ein paar einfache Fragen. Wie lang ist der Kurs und wie viele Termine hat er? Ist er für völlige Anfänger gedacht? Brauche ich einen Partner? Was kostet er, und gibt es eine Probestunde? Laufen die Kurse in Blöcken oder fortlaufend? Seriöse Schulen beantworten das offen. Preise und Termine ändern sich, deshalb gelten immer die Angaben auf der Website der Schule.',
         'Ask the school a few simple questions before you sign up. How long is the class and how many sessions does it have? Is it meant for complete beginners? Do I need a partner? What does it cost, and is there a trial class? Do classes run in blocks or continuously? Reputable schools answer openly. Prices and dates change, so the details on the school\'s own website always apply.'),
   ('p', 'Wenn du noch ganz am Anfang stehst, hilft dir der Ratgeber <a href="bachata-fuer-anfaenger.html">Bachata für Anfänger</a>. Eine Übersicht über Kursformen steht auf der Seite <a href="bachata-tanzkurs.html">Bachata Tanzkurs</a>.',
         'If you are just starting out, the guide <a href="bachata-fuer-anfaenger.html">Bachata for beginners</a> helps. An overview of class formats is on the page <a href="bachata-tanzkurs.html">Bachata dance course</a>.'),
 ]),
 ('Der erste Kurs: So bereitest du dich vor', 'Your first class: how to prepare', [
   ('p', 'Zieh bequeme Kleidung an und wähle Schuhe, mit denen du dich auf dem Boden drehen kannst. Komm ein paar Minuten früher, damit du die Lehrkräfte und die Gruppe kennenlernst. Du musst vorher nichts können: Im ersten Kurs geht es um Takt, Grundschritt und das Gefühl für die Musik. Hör vorher ein paar Stücke, damit du den Rhythmus kennst. Hintergründe dazu findest du auf der Seite <a href="bachata-musik.html">Bachata Musik</a>.',
         'Wear comfortable clothes and choose shoes you can turn in on the floor. Arrive a few minutes early so you can meet the teachers and the group. You do not need to know anything beforehand: the first class is about timing, the basic step and a feel for the music. Listen to a few tracks beforehand so you know the rhythm. Background is on the page <a href="bachata-musik.html">Bachata music</a>.'),
   ('p', 'Gib dir mindestens vier bis sechs Wochen, bevor du entscheidest, ob eine Schule zu dir passt. Am Anfang fühlt sich fast jeder unsicher, das ist normal. Wichtig ist, dass du dich in der Gruppe wohlfühlst und dass die Lehrkräfte Fehler freundlich korrigieren. Wenn das stimmt, kommt die Sicherheit mit jeder Stunde von selbst.',
         'Give yourself at least four to six weeks before you decide whether a school suits you. Almost everyone feels unsure at the start, which is normal. What matters is that you feel comfortable in the group and that the teachers correct mistakes kindly. If that is right, confidence comes by itself with every lesson.'),
 ]),
 ('Bachata Tanzschule in deiner Stadt finden', 'Finding a Bachata dance school in your city', [
   ('p', f'Auf Latin Dance Awards findest du Städteseiten mit Schulen, alphabetisch sortiert und ohne Wertung: {CITY_LINKS_DE}. Alle weiteren Städte stehen auf der Seite <a href="bachata-staedte-deutschland.html">Alle Städte und Schulen</a>.',
         f'On Latin Dance Awards you find city pages with schools, sorted alphabetically and without rating: {CITY_LINKS_EN}. All other cities are on the page <a href="bachata-staedte-deutschland.html">All cities and schools</a>.'),
   ('p', 'Die Angaben stammen von den Websites der Schulen. Prüfe Termine und Preise immer direkt dort, bevor du dich anmeldest.',
         'The information comes from the schools\' own websites. Always check dates and prices there before you sign up.'),
 ]),
 ('Tanzschule, Tanzstudio oder Verein: Was passt?', 'Dance school, studio or club: what fits?', [
   ('p', 'Klassische Tanzschulen bieten oft mehrere Tanzarten an und haben feste Kursstufen. Spezialisierte Latin-Studios konzentrieren sich auf Bachata, Salsa und verwandte Tänze und veranstalten häufig eigene Partys. Hochschulsport und Vereine sind meist günstiger und lockerer, haben aber kürzere Semester und weniger Auswahl bei den Stilen. Keine Form ist grundsätzlich besser, es kommt auf dein Ziel an: Willst du auf Socials tanzen, auf der Bühne stehen oder einfach Bewegung mit Musik?',
         'Classic dance schools often offer several dances and have fixed course levels. Specialised Latin studios concentrate on Bachata, salsa and related dances and often run their own parties. University sport and clubs are usually cheaper and more relaxed, but have shorter terms and less choice of styles. No format is better by default; it depends on your goal: do you want to dance at socials, perform on stage or simply move to music?'),
   ('p', 'Auf der Seite <a href="bachata-socials.html">Bachata-Socials in Deutschland</a> siehst du, wo du das Gelernte anwenden kannst.',
         'On the page <a href="bachata-socials.html">Bachata socials in Germany</a> you see where to use what you have learned.'),
 ]),
 ('Bachata Tanzschule und das Ranking', 'Bachata dance school and the ranking', [
   ('p', 'Das Ranking bewertet jede Schule nach denselben neun öffentlichen Kriterien mit zusammen 100 Punkten, unter anderem Google-Bewertung, Einsteigerangebot, Events und Festivals. Das offizielle Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>, die Methode steht auf der <a href="deutschland.html#method">Startseite</a>. Bis dahin sind alle Listen alphabetisch und keine Wertung.',
         'The ranking scores every school on the same nine public factors, 100 points in total, including Google rating, beginner offer, events and festivals. The official ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>, and the method is on the <a href="deutschland.html#method">homepage</a>. Until then all lists are alphabetical and not a rating.'),
   ('p', 'Du leitest eine Schule? <a href="bewerbung.html">Bewirb dich kostenlos bis zum 30. November</a>.',
         'Do you run a school? <a href="bewerbung.html">Apply for free by November 30</a>.'),
 ]),
]
ts_faq = [
 ('Was macht eine gute Bachata Tanzschule aus?', 'What makes a good Bachata dance school?',
  'Ein klarer Anfängerkurs, eine Probestunde, eine genaue Stilangabe, kleine Gruppen mit Partnerwechsel und Übungsabende oder Partys.',
  'A clear beginner class, a trial lesson, a precise style description, small groups with partner rotation and practice nights or parties.'),
 ('Brauche ich Vorkenntnisse für eine Bachata Tanzschule?', 'Do I need prior experience for a Bachata dance school?',
  'Nein. Anfängerkurse sind für Menschen ohne Vorkenntnisse gedacht. Lies die Kursbeschreibung, ob die Stufe zu dir passt.',
  'No. Beginner classes are meant for people without prior experience. Read the class description to see whether the level suits you.'),
 ('Brauche ich einen Partner?', 'Do I need a partner?',
  'In den meisten Kursen nicht, da die Partner wechseln. Frag im Zweifel bei der Schule nach.',
  'In most classes you do not, as partners rotate. If in doubt, ask the school.'),
 ('Wie finde ich eine Schule in meiner Stadt?', 'How do I find a school in my city?',
  f'Über die Städteseiten: {CITY_LINKS_DE}. Weitere Städte stehen auf <a href="bachata-staedte-deutschland.html">Alle Städte und Schulen</a>.',
  f'Via the city pages: {CITY_LINKS_EN}. More cities are on <a href="bachata-staedte-deutschland.html">All cities and schools</a>.'),
 ('Sind die Listen eine Bewertung?', 'Are the lists a rating?',
  'Nein. Bis zum Ranking sind alle Listen alphabetisch und keine Wertung.',
  'No. Until the ranking, all lists are alphabetical and not a rating.'),
 ('Wann erscheint das Ranking der Bachata-Schulen?', 'When is the ranking of Bachata schools published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html">ranking page</a>.'),
]
guide_page('bachata-tanzschule', 'bts',
  'Bachata Tanzschule finden: Tipps und Fragen',
  'Bachata Tanzschule finden: Woran du gute Schulen erkennst, welche Fragen du vor dem ersten Kurs stellst und wo du Schulen in deiner Stadt findest.',
  'Finding a Bachata dance school: tips and questions',
  'Finding a Bachata dance school: how to recognise good schools, which questions to ask before your first class and where to find schools in your city.',
  'Bachata Tanzschule', ('Bachata Tanzschule · Ratgeber', 'Bachata dance school · Guide'),
  ('Bachata Tanzschule finden: <em class="foil">Tipps</em> und Fragen', 'Finding a Bachata dance school: <em class="foil">tips</em> and questions'),
  ('Eine Bachata Tanzschule passt zu dir, wenn Stil, Niveau und Atmosphäre stimmen. Hier erfährst du, worauf du achtest und wo du Schulen in deiner Stadt findest.',
   'A Bachata dance school suits you when style, level and atmosphere fit. Here you learn what to look for and where to find schools in your city.'),
  [('check', 'Für <b>Anfänger</b> ohne Partner', 'For <b>beginners</b> without a partner'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  ts_sections, ts_faq, sibling_group='topic')


# ======================================================================
# SALSA UND BACHATA and BACHATA SCHRITTE (added 2026-11-04)
# Facts: de.wikipedia.org (Bachata, Salsa (Tanz)), checked 2026-11-04. No school claims.
# ======================================================================
SALSA_WIKI = '<a href="https://de.wikipedia.org/wiki/Salsa_(Tanz)" rel="noopener">Wikipedia</a>'

vs_sections = [
 ('Salsa und Bachata: Das sind die wichtigsten Unterschiede', 'Salsa and Bachata: the main differences', [
   ('p', f'Salsa und Bachata sind beide Paartänze aus der Karibik, und viele Tanzschulen bieten sie nebeneinander an. Trotzdem sind sie verschieden: Salsa tanzt du in einem Achter-Muster mit Pausen, Bachata in einem Vierer-Muster mit Tap. Bachata stammt aus der Dominikanischen Republik ({WIKI}), Salsa ist ein lateinamerikanischer Gesellschaftstanz mit afrokaribischen und europäischen Wurzeln ({SALSA_WIKI}). Auf dieser Seite vergleichen wir beide Tänze für Einsteiger und zeigen, womit du am besten startest.',
          f'Salsa and Bachata are both couple dances from the Caribbean, and many dance schools offer them side by side. Still, they differ: Salsa runs in an eight-count pattern with pauses, Bachata in a four-count pattern with a tap. Bachata comes from the Dominican Republic ({WIKI_EN}), while Salsa is a Latin American social dance with Afro-Caribbean and European roots ({SALSA_WIKI}). On this page we compare both dances for beginners and show you which one to start with.'),
   ('p', 'Kurz gesagt: Wer einen ruhigen, durchgehenden Schritt mit klarem Tap mag, fühlt sich bei Bachata schnell zu Hause. Wer lieber ein Muster mit Pausen und Drehungen lernt, findet bei Salsa einen guten Einstieg. Beides lässt sich später kombinieren.',
         'In short: if you like a steady, continuous step with a clear tap, you will feel at home in Bachata quickly. If you prefer a pattern with pauses and turns, Salsa is a good way in. You can combine both later.'),
 ]),
 ('Herkunft und Geschichte im Vergleich', 'Origin and history compared', [
   ('p', 'Bachata entstand Anfang der 1960er-Jahre in der Dominikanischen Republik. Zuerst war sie romantische Gitarrenmusik in der Tradition des Bolero und wurde weniger getanzt. Mit der Zeit nahm die Musik Einflüsse des Merengue auf, die Tempi stiegen, und Bachata wurde Tanzmusik. 2019 nahm die UNESCO Bachata in die Liste des immateriellen Kulturerbes auf.',
         'Bachata emerged in the early 1960s in the Dominican Republic. At first it was romantic guitar music in the tradition of the bolero and was danced less often. Over time the music took on influences from merengue, tempos rose, and Bachata became dance music. In 2019 UNESCO added Bachata to its list of intangible cultural heritage.'),
   ('p', 'Salsa hat ihre Wurzeln in Rumba, Danzón, Mambo, Son und Latin Jazz. Nach dem Zweiten Weltkrieg brachten Auswanderer aus Kuba, Puerto Rico, Kolumbien und Venezuela diese Traditionen nach New York. Nach Deutschland kam Salsa Anfang der 1980er-Jahre. Salsa ist also die ältere Tanzfamilie, Bachata als eigener Tanz die jüngere, und in Europa hat sie sich in den letzten Jahren stark verbreitet.',
         'Salsa has its roots in rumba, danzón, mambo, son and Latin jazz. After the Second World War, emigrants from Cuba, Puerto Rico, Colombia and Venezuela brought these traditions to New York. Salsa reached Germany in the early 1980s. So Salsa is the older dance family and Bachata the younger dance in its own right, and in Europe it has spread strongly in recent years.'),
 ]),
 ('Musik und Rhythmus: Salsa gegen Bachata', 'Music and rhythm: Salsa versus Bachata', [
   ('p', 'Beide Musikrichtungen stehen im 4/4-Takt, klingen aber unterschiedlich. Bachata nutzt traditionell zwei akustische Gitarren, dazu Bongos, Bass und Güira. Das Tempo liegt etwa zwischen 100 und 160 Schlägen pro Minute. Salsa lebt von den Schlaginstrumenten, der Clave und der betonten vierten Zählzeit, auf der beim Tanzen die Pause liegt.',
         'Both kinds of music are in 4/4 time but sound different. Bachata traditionally uses two acoustic guitars plus bongos, bass and güira. The tempo is roughly between 100 and 160 beats per minute. Salsa lives on its percussion, the clave and the accented fourth beat, where the pause falls when you dance.'),
   ('p', 'Zum Reinhören hilft unser Ratgeber <a href="bachata-musik.html">Bachata Musik</a>. Wenn du Bachata und Salsa auf einer Party hörst, achte auf die Gitarre: Sie führt Bachata, während bei Salsa Bläser und Percussion den Ton angeben.',
         'To listen in, our guide <a href="bachata-musik.html">Bachata music</a> helps. When you hear Bachata and Salsa at the same party, listen for the guitar: it leads Bachata, while in Salsa brass and percussion set the tone.'),
 ]),
 ('Grundschritt: Acht Zählzeiten gegen vier', 'Basic step: eight counts versus four', [
   ('p', 'Der Salsa-Grundschritt dauert zwei Takte, also zählst du bis acht: 1, 2, 3, Pause, 5, 6, 7, Pause. Es wird also nur auf drei von vier Schlägen gestiegen, auf der vierten Zählzeit ruht der Fuß. Je nach Stil wechselt die Richtung auf der 1 („on 1“) oder auf der 2 („on 2“).',
         'The Salsa basic step lasts two bars, so you count to eight: 1, 2, 3, pause, 5, 6, 7, pause. You step on only three of four beats, and your foot rests on the fourth count. Depending on the style the direction changes on 1 ("on 1") or on 2 ("on 2").'),
   ('p', 'Beim Bachata-Grundschritt machst du auf 1, 2 und 3 je einen Schritt, auf der 4 folgt ein Tap mit Hüftbewegung. Die Bewegung kommt aus den Knien und der Hüfte. Eine genaue Anleitung steht im Ratgeber <a href="bachata-grundschritt.html">Bachata Grundschritt</a>. Weil Bachata nicht standardisiert ist, tanzen Schulen und Stile den Schritt leicht unterschiedlich.',
         'In the Bachata basic step you take one step each on 1, 2 and 3, and on 4 comes a tap with a hip movement. The movement comes from the knees and hips. A full walkthrough is in the guide <a href="bachata-grundschritt.html">Bachata basic step</a>. Because Bachata is not standardised, schools and styles dance the step slightly differently.'),
 ]),
 ('Haltung, Nähe und Stil: Wie fühlen sich die Tänze an?', 'Hold, closeness and style: how do the dances feel?', [
   ('p', 'Bachata wird meist eng und hüftbetont getanzt. Die europäische Variante hält etwas mehr Abstand und enthält Figuren. Neuere Stile wie <a href="bachata-sensual.html">Bachata Sensual</a> ergänzen Körperwellen und Oberkörperbewegungen, und <a href="bachata-dominicana.html">Bachata Dominicana</a> bleibt näher am ursprünglichen Stil. Eine Übersicht der Stile findest du im Ratgeber <a href="bachata-tanzen.html">Bachata tanzen</a>.',
         'Bachata is usually danced close and hip-focused. The European version keeps a little more distance and includes figures. Newer styles such as <a href="bachata-sensual.html">Bachata Sensual</a> add body waves and upper-body movement, and <a href="bachata-dominicana.html">Bachata Dominicana</a> stays closer to the original style. An overview of the styles is in the guide <a href="bachata-tanzen.html">Dancing Bachata</a>.'),
   ('p', 'Salsa wird je nach Stil mit mehr Drehungen und Wechseln der Position getanzt. Welche Tanzweise dir besser gefällt, merkst du am schnellsten in einer Probestunde.',
         'Depending on the style, Salsa is danced with more turns and changes of position. The quickest way to find out which you prefer is a trial class.'),
 ]),
 ('Salsa oder Bachata zuerst lernen?', 'Learn Salsa or Bachata first?', [
   ('ul', [
     ('<strong>Du magst klare, gleichmäßige Schritte:</strong> Starte mit Bachata. Der Vierer-Rhythmus mit dem Tap ist leicht zu zählen.', '<strong>You like clear, even steps:</strong> start with Bachata. The four-count rhythm with the tap is easy to count.'),
     ('<strong>Du magst Muster mit Pausen und Drehungen:</strong> Salsa kann besser passen. Der Achter-Rhythmus braucht etwas mehr Konzentration.', '<strong>You like patterns with pauses and turns:</strong> Salsa may suit you better. The eight-count rhythm needs a bit more concentration.'),
     ('<strong>Du weißt es noch nicht:</strong> Besuche je eine Probestunde. Viele Schulen bieten beides an, siehe unsere <a href="bachata-staedte-deutschland.html">Übersicht der Städte und Schulen</a>.', '<strong>You do not know yet:</strong> take one trial class of each. Many schools offer both, see our <a href="bachata-staedte-deutschland.html">overview of cities and schools</a>.'),
     ('<strong>Du hast keinen Partner:</strong> Das ist bei beiden Tänzen normal, in den meisten Kursen wechseln die Partner.', '<strong>You have no partner:</strong> that is normal for both dances, in most classes partners rotate.'),
   ]),
   ('p', 'Die Schritte unterscheiden sich, aber das Grundprinzip bleibt gleich: Du hörst auf die Musik, hältst Kontakt zum Partner und tanzt auf dem Rhythmus. Wer eines der beiden Tänze kann, lernt den anderen meist schneller. Im Ratgeber <a href="bachata-tanzkurs.html">Bachata Tanzkurs</a> steht, worauf du bei der Kurswahl achtest.',
         'The steps differ, but the basic principle stays the same: you listen to the music, keep contact with your partner and dance on the rhythm. Whoever knows one of the two dances usually learns the other faster. The guide <a href="bachata-tanzkurs.html">Bachata dance course</a> explains what to look for when choosing a class.'),
 ]),
 ('Salsa und Bachata Kurse in deiner Stadt', 'Salsa and Bachata classes in your city', [
   ('p', f'Für Bachata gibt es Übersichten mit Links zu den Websites der Schulen für {CITY_LINKS_DE}. Die Listen sind alphabetisch und keine Wertung. Ob eine Schule auch Salsa anbietet, steht auf ihrer eigenen Website, bitte prüfe es dort.',
         f'For Bachata we have overviews with links to schools\' websites for {CITY_LINKS_EN}. The lists are alphabetical and not a rating. Whether a school also offers Salsa is stated on its own website, so please check there.'),
   ('p', 'Das offizielle Ranking der Bachata-Schulen erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>. Die Methode steht auf der <a href="index.html#method">Startseite</a>. Du leitest eine Schule? <a href="bewerbung.html">Bewirb dich kostenlos bis zum 30. November</a>.',
         'The official ranking of Bachata schools is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>. The method is explained on the <a href="index.html#method">home page</a>. Do you run a school? <a href="bewerbung.html">Apply for free by November 30</a>.'),
 ]),
]

vs_faq = [
 ('Was ist der Unterschied zwischen Salsa und Bachata?', 'What is the difference between Salsa and Bachata?',
  'Salsa wird in einem Achter-Muster mit Pausen auf der 4 und der 8 getanzt, Bachata in einem Vierer-Muster mit einem Tap auf der 4. Auch Herkunft und Musik unterscheiden sich: Bachata kommt aus der Dominikanischen Republik und lebt von der Gitarre.',
  'Salsa is danced in an eight-count pattern with pauses on 4 and 8, Bachata in a four-count pattern with a tap on 4. Origin and music differ too: Bachata comes from the Dominican Republic and is driven by the guitar.'),
 ('Ist Bachata leichter als Salsa?', 'Is Bachata easier than Salsa?',
  'Viele Einsteiger finden den Bachata-Grundschritt leichter zu zählen, weil er nur vier Zählzeiten hat. Ob dir einer der beiden Tänze leichter fällt, hängt aber von dir ab. Eine Probestunde zeigt es am schnellsten.',
  'Many beginners find the Bachata basic step easier to count because it has only four counts. Which of the two dances comes easier depends on you, though. A trial class shows it fastest.'),
 ('Kann ich Salsa und Bachata gleichzeitig lernen?', 'Can I learn Salsa and Bachata at the same time?',
  'Ja. Viele Schulen bieten beide Tänze an, und die Grundprinzipien sind ähnlich. Plane am Anfang aber genug Übungszeit ein, damit sich die Schritte nicht vermischen.',
  'Yes. Many schools offer both dances and the basic principles are similar. At the start, plan enough practice time so the steps do not blur together.'),
 ('Brauche ich einen Partner für Salsa oder Bachata?', 'Do I need a partner for Salsa or Bachata?',
  'In der Regel nicht. In den meisten Kursen wechseln die Partner. Frag vor der Probestunde nach.',
  'Usually not. In most classes partners rotate. Ask before the trial class.'),
 ('Woher kommt Bachata?', 'Where does Bachata come from?',
  'Aus der Dominikanischen Republik. Sie entstand Anfang der 1960er-Jahre und steht seit 2019 auf der UNESCO-Liste des immateriellen Kulturerbes.',
  'From the Dominican Republic. It emerged in the early 1960s and has been on UNESCO\'s list of intangible cultural heritage since 2019.'),
 ('Wann erscheint das Ranking der Bachata-Schulen?', 'When is the ranking of Bachata schools published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html">ranking page</a>.'),
]

guide_page('bachata-salsa-unterschied', 'bsu',
  'Salsa und Bachata: Unterschiede, Musik und Schritte',
  'Salsa und Bachata im Vergleich: Herkunft, Musik, Grundschritt mit Zählzeiten und die Frage, womit Anfänger starten. Mit Links zu Kursen in deiner Stadt.',
  'Salsa and Bachata: differences, music and steps',
  'Salsa and Bachata compared: origin, music, the basic step with counts and which to start with as a beginner. With links to classes in your city.',
  'Salsa und Bachata', ('Salsa und Bachata · Vergleich', 'Salsa and Bachata · Comparison'),
  ('Salsa und Bachata: <em class="foil">Unterschiede</em> im Überblick', 'Salsa and Bachata: the <em class="foil">differences</em> at a glance'),
  ('Salsa und Bachata im Vergleich: Herkunft, Musik, Grundschritt und die Frage, womit du als Anfänger startest. Verständlich erklärt, mit Links zu Kursen.',
   'Salsa and Bachata compared: origin, music, basic step and which to start with as a beginner. Clearly explained, with links to classes.'),
  [('check', 'Für <b>Anfänger</b> ohne Partner', 'For <b>beginners</b> without a partner'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  vs_sections, vs_faq, sibling_group='topic')

schr_sections = [
 ('Bachata Schritte: Das lernst du als Erstes', 'Bachata steps: what you learn first', [
   ('p', f'Bachata Schritte sind die Bausteine, aus denen du später ganze Tänze zusammensetzt. Bachata stammt aus der Dominikanischen Republik ({WIKI}), ist nicht standardisiert und kennt deshalb viele Varianten. In Einsteigerkursen lernst du trotzdem fast überall dieselben Grundbausteine: den Seitwärtsschritt mit Tap, den Wechsel von Vor und Zurück, die Hüftbewegung und erste Drehungen. Diese Seite erklärt sie in der Reihenfolge, in der du sie üben solltest.',
          f'Bachata steps are the building blocks you later put together into whole dances. Bachata comes from the Dominican Republic ({WIKI_EN}), is not standardised and therefore has many variations. Still, in beginner classes you learn almost everywhere the same basic building blocks: the side step with a tap, the switch between forward and back, the hip movement and first turns. This page explains them in the order you should practise them.'),
   ('p', 'Die genaue Anleitung zum ersten Schritt steht im Ratgeber <a href="bachata-grundschritt.html">Bachata Grundschritt</a>. Hier geht es um den Weg danach.',
         'The exact walkthrough of the first step is in the guide <a href="bachata-grundschritt.html">Bachata basic step</a>. Here we cover the path after it.'),
 ]),
 ('Rhythmus und Zählzeiten: Die Grundlage aller Schritte', 'Rhythm and counts: the basis of every step', [
   ('p', 'Bachata steht im 4/4-Takt, das Tempo liegt etwa zwischen 100 und 160 Schlägen pro Minute. Du zählst 1, 2, 3, 4 und machst auf den ersten drei Zählzeiten je einen Schritt. Auf der 4 folgt ein Tap, bei dem die Hüfte mitgeht. Wer diesen Takt im Ohr hat, kann jeden weiteren Schritt darauf aufbauen.',
         'Bachata is in 4/4 time and the tempo is roughly between 100 and 160 beats per minute. You count 1, 2, 3, 4 and take one step on each of the first three counts. On 4 comes a tap with the hip moving along. Once you have this beat in your ears, you can build every further step on it.'),
   ('p', 'Zum Üben hilft Musik mit klarem Gitarrenmotiv. Mehr dazu im Ratgeber <a href="bachata-musik.html">Bachata Musik</a>. Beginne mit einem langsamen Lied und steigere das Tempo erst, wenn der Tap sicher sitzt.',
         'Music with a clear guitar motif helps for practice. More in the guide <a href="bachata-musik.html">Bachata music</a>. Start with a slow song and raise the tempo only when the tap sits securely.'),
 ]),
 ('Die wichtigsten Bachata Schritte für Anfänger', 'The most important Bachata steps for beginners', [
   ('ul', [
     ('<strong>Seitwärts-Grundschritt:</strong> Drei kleine Schritte zur Seite und ein Tap. Das ist die Basis, alle anderen Schritte bauen darauf auf.', '<strong>Side basic step:</strong> three small steps to the side and a tap. This is the base, all other steps build on it.'),
     ('<strong>Vor und zurück:</strong> Derselbe Rhythmus, aber nach vorn und hinten statt zur Seite. Er trainiert die Führung der Partner.', '<strong>Forward and back:</strong> the same rhythm, but forward and backward instead of sideways. It trains the lead and follow between partners.'),
     ('<strong>Hüftbewegung auf der 4:</strong> Beim Tap zieht eine Hüfte leicht nach oben. Die Bewegung kommt aus den Knien, nicht aus dem Oberkörper.', '<strong>Hip movement on 4:</strong> at the tap one hip lifts slightly. The movement comes from the knees, not the upper body.'),
     ('<strong>Gewichtswechsel:</strong> Du verlagerst das Gewicht bewusst von einem Fuß auf den anderen. Er macht den Schritt weich und gibt dem Partner ein klares Signal.', '<strong>Weight change:</strong> you shift your weight deliberately from one foot to the other. It makes the step smooth and gives your partner a clear signal.'),
     ('<strong>Erste Drehungen:</strong> Die Folgende dreht sich unter dem Arm, während die Führende den Grundschritt weitertanzt. Das ist der erste Schritt zur Figur.', '<strong>First turns:</strong> the follower turns under the arm while the leader keeps dancing the basic step. This is the first step towards a figure.'),
   ]),
   ('p', 'Welche Bausteine genau in welchem Kurs dran sind, unterscheidet sich je nach Schule und Stil. Frag in der Probestunde nach dem Lehrplan.',
         'Which building blocks exactly come up in which class differs by school and style. Ask about the curriculum in the trial class.'),
 ]),
 ('Bachata Schritte je nach Stil', 'Bachata steps by style', [
   ('h3', 'Bachata Dominicana', 'Bachata Dominicana'),
   ('p', 'Der ursprüngliche Stil mit ausgeprägter Fußarbeit und enger Haltung. Die Schritte sind schnell und spielerisch. Mehr im Ratgeber <a href="bachata-dominicana.html">Bachata Dominicana</a>.',
         'The original style with pronounced footwork and a close hold. The steps are quick and playful. More in the guide <a href="bachata-dominicana.html">Bachata Dominicana</a>.'),
   ('h3', 'Bachata Moderna', 'Bachata Moderna'),
   ('p', 'Grundschritt plus Drehungen und Elemente anderer Tänze. Viele Einsteigerkurse beginnen hier. Siehe <a href="bachata-moderna.html">Bachata Moderna</a>.',
         'Basic step plus turns and elements from other dances. Many beginner classes start here. See <a href="bachata-moderna.html">Bachata Moderna</a>.'),
   ('h3', 'Bachata Sensual', 'Bachata Sensual'),
   ('p', 'Ein neuerer Stil aus den 2010er-Jahren mit Körperwellen und Oberkörperbewegungen, zum Teil aus dem Zouk übernommen. Siehe <a href="bachata-sensual.html">Bachata Sensual</a>.',
         'A newer style from the 2010s with body waves and upper-body movements, partly borrowed from zouk. See <a href="bachata-sensual.html">Bachata Sensual</a>.'),
 ]),
 ('Vom Schritt zur Figur: So übst du', 'From step to figure: how to practise', [
   ('ul', [
     ('<strong>Täglich fünf Minuten:</strong> Kurze, regelmäßige Einheiten bringen mehr als eine lange Stunde pro Woche.', '<strong>Five minutes a day:</strong> short, regular sessions beat one long hour a week.'),
     ('<strong>Laut mitzählen:</strong> Zähle 1, 2, 3, 4, bis der Tap automatisch kommt.', '<strong>Count out loud:</strong> count 1, 2, 3, 4 until the tap comes automatically.'),
     ('<strong>Klein anfangen:</strong> Kleine Schritte und lockere Knie lassen sich später leichter in Figuren einbauen.', '<strong>Start small:</strong> small steps and relaxed knees are easier to build into figures later.'),
     ('<strong>Im Spiegel prüfen:</strong> Achte darauf, dass Gewicht und Hüfte zum Takt passen.', '<strong>Check in the mirror:</strong> make sure your weight and hip match the beat.'),
     ('<strong>Mit Partner üben:</strong> Erst im Kurs oder auf einem Social merkst du, wie Führen und Folgen die Schritte verändern. Termine siehst du bei den <a href="bachata-socials.html">Bachata-Socials</a>.', '<strong>Practise with a partner:</strong> only in class or at a social do you notice how leading and following change the steps. Dates are on the <a href="bachata-socials.html">Bachata socials</a> page.'),
   ]),
 ]),
 ('Bachata Schritte im Kurs lernen', 'Learning Bachata steps in class', [
   ('p', 'Videos helfen beim Einstieg, aber im Kurs bekommst du Korrektur und lernst das Führen und Folgen. Wie du einen Kurs wählst, steht im Ratgeber <a href="bachata-fuer-anfaenger.html">Bachata für Anfänger</a> und bei <a href="bachata-tanzkurs.html">Bachata Tanzkurs</a>.',
         'Videos help you get started, but in class you receive corrections and learn leading and following. How to choose a class is covered in the guide <a href="bachata-fuer-anfaenger.html">Bachata for beginners</a> and at <a href="bachata-tanzkurs.html">Bachata dance course</a>.'),
   ('p', f'Schulen mit Links zu ihren Websites findest du für {CITY_LINKS_DE}. Die Listen sind alphabetisch und keine Wertung. Das offizielle Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>, die Methode steht auf der <a href="index.html#method">Startseite</a>.',
         f'Schools with links to their websites are listed for {CITY_LINKS_EN}. The lists are alphabetical and not a rating. The official ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>, and the method is on the <a href="index.html#method">home page</a>.'),
   ('p', 'Du leitest eine Schule? <a href="bewerbung.html">Bewirb dich kostenlos bis zum 30. November</a>.',
         'Do you run a school? <a href="bewerbung.html">Apply for free by November 30</a>.'),
 ]),
]

schr_faq = [
 ('Welche Bachata Schritte lernt man als Erstes?', 'Which Bachata steps do you learn first?',
  'Zuerst den Grundschritt mit drei Schritten und einem Tap auf der 4, dann Vor und Zurück, die Hüftbewegung und erste Drehungen.',
  'First the basic step with three steps and a tap on 4, then forward and back, the hip movement and first turns.'),
 ('Wie viele Bachata Schritte gibt es?', 'How many Bachata steps are there?',
  'Eine feste Zahl gibt es nicht, denn Bachata ist nicht standardisiert. Es gibt viele Varianten und Bewegungsfolgen, je nach Stil und Schule.',
  'There is no fixed number, because Bachata is not standardised. There are many variations and sequences, depending on style and school.'),
 ('Kann ich Bachata Schritte zu Hause lernen?', 'Can I learn Bachata steps at home?',
  'Den Grundschritt ja, mit Musik und einem Spiegel. Führen und Folgen lernst du aber erst mit Partner, am besten im Kurs.',
  'The basic step yes, with music and a mirror. You only learn leading and following with a partner, ideally in class.'),
 ('Wie schnell ist Bachata?', 'How fast is Bachata?',
  'Das Tempo liegt etwa zwischen 100 und 160 Schlägen pro Minute im 4/4-Takt. Anfänger üben am besten zu langsameren Liedern.',
  'The tempo is roughly between 100 and 160 beats per minute in 4/4 time. Beginners practise best to slower songs.'),
 ('Unterscheiden sich die Schritte je nach Stil?', 'Do the steps differ by style?',
  'Ja. Dominicana betont die Fußarbeit, Moderna ergänzt Drehungen, Sensual Körperwellen. Der Grundrhythmus bleibt gleich.',
  'Yes. Dominicana stresses footwork, Moderna adds turns, Sensual adds body waves. The basic rhythm stays the same.'),
 ('Wann erscheint das Ranking der Bachata-Schulen?', 'When is the ranking of Bachata schools published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html">ranking page</a>.'),
]

guide_page('bachata-schritte', 'bsc',
  'Bachata Schritte: Die wichtigsten Grundschritte lernen',
  'Bachata Schritte für Anfänger: Rhythmus, Zählzeiten, Seitwärtsschritt, Hüfte und erste Drehungen, dazu Übungstipps und Links zu Kursen in deiner Stadt.',
  'Bachata steps: learn the most important basics',
  'Bachata steps for beginners: rhythm, counts, side step, hip movement and first turns, plus practice tips and links to classes in your city.',
  'Bachata Schritte', ('Bachata Schritte · Ratgeber', 'Bachata steps · Guide'),
  ('Bachata Schritte: <em class="foil">Grundbausteine</em> für Anfänger', 'Bachata steps: <em class="foil">building blocks</em> for beginners'),
  ('Bachata Schritte für Anfänger: Rhythmus, Zählzeiten, Seitwärtsschritt, Hüftbewegung und erste Drehungen, in der Reihenfolge, in der du sie übst.',
   'Bachata steps for beginners: rhythm, counts, side step, hip movement and first turns, in the order you should practise them.'),
  [('check', 'Für <b>Anfänger</b> ohne Partner', 'For <b>beginners</b> without a partner'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  schr_sections, schr_faq, sibling_group='topic')

# ---------- Bachata lernen ----------
lern_sections = [
 ('Bachata lernen: Die vier Wege im Überblick', 'Learning Bachata: the four routes at a glance', [
   ('p', f'Bachata lernen kannst du auf mehreren Wegen, und die meisten Tänzer kombinieren sie. Der Tanz stammt aus der Dominikanischen Republik ({WIKI}) und wird heute in vielen Stilen getanzt. Für den Einstieg brauchst du keine Vorkenntnisse und keinen festen Partner. Die vier häufigsten Wege sind der Kurs in einer Tanzschule, Workshops, Videos zum Selbststudium und das Ausprobieren auf einer Party. Jeder Weg hat andere Stärken, und diese Seite hilft dir bei der Wahl.',
          f'You can learn Bachata in several ways, and most dancers combine them. The dance comes from the Dominican Republic ({WIKI_EN}) and is danced in many styles today. To start you need no prior experience and no fixed partner. The four most common routes are a class at a dance school, workshops, videos for self-study and trying it out at a party. Each route has different strengths, and this page helps you choose.'),
 ]),
 ('Bachata lernen im Kurs', 'Learning Bachata in a class', [
   ('p', 'Ein Kurs ist für die meisten Anfänger der sicherste Start. Du bekommst Korrektur von einer Lehrkraft, lernst Führen und Folgen mit wechselnden Partnern und hast einen festen Termin, der dich bei der Stange hält. Worauf du bei der Wahl achtest, steht im Ratgeber <a href="bachata-tanzkurs.html">Bachata Tanzkurs</a> und bei <a href="bachata-tanzschule.html">Bachata Tanzschule</a>. Viele Schulen bieten eine Probestunde an, frag vorher nach.',
         'For most beginners a class is the safest start. You get corrections from a teacher, learn leading and following with changing partners and have a fixed date that keeps you going. What to look for when choosing is in the guide <a href="bachata-tanzkurs.html">Bachata dance course</a> and at <a href="bachata-tanzschule.html">Bachata dance school</a>. Many schools offer a trial class, so ask beforehand.'),
 ]),
 ('Bachata lernen mit Workshops und Videos', 'Learning Bachata with workshops and videos', [
   ('p', 'Workshops dauern meist einen Abend oder ein Wochenende und vertiefen ein Thema, zum Beispiel Drehungen oder Musikalität. Sie ersetzen den Kurs nicht, ergänzen ihn aber gut. Mehr dazu auf der Seite <a href="bachata-workshop.html">Bachata Workshop</a>. Videos eignen sich zum Wiederholen und für den Grundschritt, ersetzen aber nicht die Rückmeldung einer Lehrkraft und das Gefühl für den Partner.',
         'Workshops usually last an evening or a weekend and deepen one topic, for example turns or musicality. They do not replace a class but complement it well. More on the page <a href="bachata-workshop.html">Bachata workshop</a>. Videos suit repetition and the basic step, but do not replace a teacher’s feedback and the feel for your partner.'),
 ]),
 ('Bachata lernen: Das übst du zuerst', 'Learning Bachata: what to practise first', [
   ('ul', [
     ('<strong>Rhythmus hören:</strong> Bachata steht im 4/4-Takt. Zähle 1, 2, 3, 4 und lerne, den Tap auf der 4 zu erkennen. Hilfreich ist der Ratgeber <a href="bachata-musik.html">Bachata Musik</a>.', '<strong>Hear the rhythm:</strong> Bachata is in 4/4 time. Count 1, 2, 3, 4 and learn to recognise the tap on 4. The guide <a href="bachata-musik.html">Bachata music</a> helps.'),
     ('<strong>Grundschritt:</strong> Drei Schritte und ein Tap. Die Anleitung steht im Ratgeber <a href="bachata-grundschritt.html">Bachata Grundschritt</a>.', '<strong>Basic step:</strong> three steps and a tap. The walkthrough is in the guide <a href="bachata-grundschritt.html">Bachata basic step</a>.'),
     ('<strong>Weitere Bausteine:</strong> Vor und zurück, Hüftbewegung und erste Drehungen findest du unter <a href="bachata-schritte.html">Bachata Schritte</a>.', '<strong>More building blocks:</strong> forward and back, hip movement and first turns are covered under <a href="bachata-schritte.html">Bachata steps</a>.'),
     ('<strong>Stil wählen:</strong> Dominicana, Moderna und Sensual fühlen sich verschieden an. Probiere sie aus, bevor du dich festlegst.', '<strong>Choose a style:</strong> Dominicana, Moderna and Sensual feel different. Try them before you commit.'),
   ]),
 ]),
 ('Bachata lernen ohne Partner', 'Learning Bachata without a partner', [
   ('p', 'Du musst nicht mit einem Partner kommen. In den meisten Kursen wechseln die Paare durch, und alleine zu starten ist üblich. Wer mehr Sicherheit sucht, liest vorher den Ratgeber <a href="bachata-fuer-anfaenger.html">Bachata für Anfänger</a>. Für den Einstieg in die Tanzkultur lohnt sich auch ein Blick auf die <a href="bachata-party.html">Bachata Party</a> und die Termine der <a href="bachata-socials.html">Bachata-Socials</a>.',
         'You do not need to bring a partner. In most classes the couples rotate, and starting alone is common. If you want more confidence, read the guide <a href="bachata-fuer-anfaenger.html">Bachata for beginners</a> first. To get into the dance culture, take a look at the <a href="bachata-party.html">Bachata party</a> and the dates on the <a href="bachata-socials.html">Bachata socials</a> page.'),
 ]),
 ('Häufige Fehler beim Bachata lernen', 'Common mistakes when learning Bachata', [
   ('p', 'Viele Anfänger machen zu große Schritte, halten die Knie durchgedrückt oder zählen nicht mit. Das macht den Tanz hektisch und anstrengend. Kleine Schritte, weiche Knie und ein ruhiger Blick zum Partner helfen. Ein weiterer Klassiker ist, zu früh Figuren lernen zu wollen. Wer den Grundschritt sicher beherrscht, lernt Figuren später deutlich schneller.',
         'Many beginners take steps that are too big, keep their knees locked or do not count along. This makes the dance hectic and tiring. Small steps, soft knees and a calm look at your partner help. Another classic is wanting to learn figures too early. If you master the basic step securely, you learn figures much faster later.'),
   ('p', 'Auch die Musik wird oft unterschätzt. Wer Bachata regelmäßig hört, findet den Takt schneller und tanzt entspannter. Der Ratgeber <a href="bachata-tanzen.html">Bachata tanzen</a> fasst den Einstieg noch einmal zusammen, und die Unterschiede zur Salsa erklärt die Seite <a href="bachata-salsa-unterschied.html">Salsa und Bachata</a>.',
         'Music is also often underestimated. If you listen to Bachata regularly, you find the beat faster and dance more relaxed. The guide <a href="bachata-tanzen.html">Bachata dancing</a> sums up the start once more, and the page <a href="bachata-salsa-unterschied.html">Salsa and Bachata</a> explains the differences from salsa.'),
 ]),
 ('Was du zum Bachata lernen mitbringst', 'What to bring when learning Bachata', [
   ('p', 'Für den ersten Kurs reichen bequeme Kleidung und Schuhe, in denen du dich auf dem Boden drehen kannst. Straßenschuhe mit rutschiger oder sehr rauer Sohle sind ungeeignet. Manche Schulen empfehlen Tanzschuhe, aber für die ersten Stunden ist das keine Pflicht. Bring etwas zu trinken mit und plane Zeit ein, um in Ruhe anzukommen.',
         'For the first class, comfortable clothes and shoes you can turn in on the floor are enough. Street shoes with a slippery or very rough sole are unsuitable. Some schools recommend dance shoes, but for the first lessons this is not mandatory. Bring something to drink and allow time to arrive calmly.'),
 ]),
 ('So bleibst du dran', 'How to keep going', [
   ('ul', [
     ('<strong>Regelmäßig statt lang:</strong> Kurze Übungseinheiten mehrmals pro Woche bringen mehr als eine lange.', '<strong>Regular rather than long:</strong> short practice sessions several times a week beat one long one.'),
     ('<strong>Ein Ziel setzen:</strong> Zum Beispiel der erste Besuch einer Party oder eines Festivals, siehe <a href="bachata-festivals-deutschland.html">Bachata-Festivals</a>.', '<strong>Set a goal:</strong> for example your first party or festival, see <a href="bachata-festivals-deutschland.html">Bachata festivals</a>.'),
     ('<strong>Geduld haben:</strong> Wie schnell du vorankommst, hängt von Übung, Kurs und Vorerfahrung ab. Vergleiche dich nicht mit anderen.', '<strong>Be patient:</strong> how fast you progress depends on practice, class and prior experience. Do not compare yourself with others.'),
   ]),
 ]),
 ('Schulen zum Bachata lernen finden', 'Finding schools to learn Bachata', [
   ('p', f'Schulen mit Links zu ihren Websites findest du für {CITY_LINKS_DE}. Die Listen sind alphabetisch und keine Wertung. Das offizielle Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>, die Methode steht auf der <a href="index.html#method">Startseite</a>.',
         f'Schools with links to their websites are listed for {CITY_LINKS_EN}. The lists are alphabetical and not a rating. The official ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>, and the method is on the <a href="index.html#method">home page</a>.'),
   ('p', 'Du leitest eine Schule? <a href="bewerbung.html">Bewirb dich kostenlos bis zum 30. November</a>.',
         'Do you run a school? <a href="bewerbung.html">Apply for free by November 30</a>.'),
 ]),
]
lern_faq = [
 ('Wie kann ich Bachata lernen?', 'How can I learn Bachata?',
  'Am besten im Kurs einer Tanzschule, ergänzt durch Workshops, Videos zum Wiederholen und Besuche auf Partys. Ein fester Partner ist nicht nötig.',
  'Best in a class at a dance school, complemented by workshops, videos for repetition and visits to parties. A fixed partner is not needed.'),
 ('Kann man Bachata alleine lernen?', 'Can you learn Bachata alone?',
  'Den Grundschritt ja, mit Musik und einem Spiegel. Führen und Folgen lernst du aber nur mit Partner, am besten im Kurs.',
  'The basic step yes, with music and a mirror. You only learn leading and following with a partner, ideally in class.'),
 ('Wie lange dauert es, Bachata zu lernen?', 'How long does it take to learn Bachata?',
  'Das hängt von Übung, Kurs und Vorerfahrung ab. Eine feste Dauer gibt es nicht. Frag in der Probestunde nach dem Lehrplan.',
  'It depends on practice, class and prior experience. There is no fixed duration. Ask about the curriculum in the trial class.'),
 ('Ist Bachata leicht zu lernen?', 'Is Bachata easy to learn?',
  'Der Grundschritt gilt als einfach, weil er nur drei Schritte und einen Tap hat. Schwieriger werden Führen, Folgen und Musikalität.',
  'The basic step is considered easy because it has only three steps and a tap. Leading, following and musicality are harder.'),
 ('Brauche ich Vorkenntnisse zum Bachata lernen?', 'Do I need prior experience to learn Bachata?',
  'Nein. Anfängerkurse setzen keine Vorkenntnisse voraus. Siehe <a href="bachata-fuer-anfaenger.html">Bachata für Anfänger</a>.',
  'No. Beginner classes assume no prior experience. See <a href="bachata-fuer-anfaenger.html">Bachata for beginners</a>.'),
 ('Wann erscheint das Ranking der Bachata-Schulen?', 'When is the ranking of Bachata schools published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html">ranking page</a>.'),
]
guide_page('bachata-lernen', 'bln',
  'Bachata lernen: So startest du als Anfänger',
  'Bachata lernen als Anfänger: Kurs, Workshop oder Video? Die vier Wege im Vergleich, was du zuerst übst und wie du ohne Partner startest. Mit Links zu Schulen.',
  'Learn Bachata: how to start as a beginner',
  'Learn Bachata as a beginner: class, workshop or video? The four routes compared, what to practise first and how to start without a partner. With links to schools.',
  'Bachata lernen', ('Bachata lernen · Ratgeber', 'Learn Bachata · Guide'),
  ('Bachata lernen: Der <em class="foil">Einstieg</em> für Anfänger', 'Learn Bachata: the <em class="foil">start</em> for beginners'),
  ('Bachata lernen als Anfänger: Kurs, Workshop oder Video? Die vier Wege im Vergleich, mit Übungstipps und Hinweisen, wie du ohne Partner startest.',
   'Learn Bachata as a beginner: class, workshop or video? The four routes compared, with practice tips and advice on starting without a partner.'),
  [('check', 'Für <b>Anfänger</b> ohne Partner', 'For <b>beginners</b> without a partner'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  lern_sections, lern_faq, sibling_group='topic')

# ---------- Bachata Workshop ----------
ws_sections = [
 ('Bachata Workshop: Was ist das?', 'Bachata workshop: what is it?', [
   ('p', f'Ein Bachata Workshop ist eine kurze, konzentrierte Unterrichtseinheit zu einem bestimmten Thema. Anders als ein laufender Kurs dauert er meist einen Abend, einen Tag oder ein Wochenende. Bachata stammt aus der Dominikanischen Republik ({WIKI}) und hat viele Stile, deshalb gibt es Workshops zu Dominicana, Moderna, Sensual und zu Querschnittsthemen wie Musikalität oder Partnerarbeit.',
          f'A Bachata workshop is a short, focused teaching session on one topic. Unlike an ongoing class it usually lasts an evening, a day or a weekend. Bachata comes from the Dominican Republic ({WIKI_EN}) and has many styles, so there are workshops on Dominicana, Moderna, Sensual and on cross-cutting topics such as musicality or partner work.'),
 ]),
 ('Bachata Workshop oder Kurs?', 'Bachata workshop or class?', [
   ('ul', [
     ('<strong>Kurs:</strong> Regelmäßiger Termin über mehrere Wochen, baut Schritt für Schritt auf. Gut für den Einstieg, siehe <a href="bachata-tanzkurs.html">Bachata Tanzkurs</a>.', '<strong>Class:</strong> regular date over several weeks, builds up step by step. Good for starting, see <a href="bachata-tanzkurs.html">Bachata dance course</a>.'),
     ('<strong>Workshop:</strong> Ein Thema in kurzer Zeit. Gut zum Vertiefen oder Ausprobieren eines Stils.', '<strong>Workshop:</strong> one topic in a short time. Good for deepening or trying out a style.'),
   ]),
   ('p', 'Wer noch nie getanzt hat, startet meist besser mit einem Kurs. Ein Workshop für Einsteiger ist aber möglich, wenn er so ausgeschrieben ist. Mehr im Ratgeber <a href="bachata-lernen.html">Bachata lernen</a>.',
         'If you have never danced, you usually do better starting with a class. A beginner workshop is possible, though, if it is advertised as such. More in the guide <a href="bachata-lernen.html">Learn Bachata</a>.'),
 ]),
 ('Formate: Wo finden Bachata Workshops statt?', 'Formats: where do Bachata workshops take place?', [
   ('ul', [
     ('<strong>In der Tanzschule:</strong> Viele Schulen bieten Workshops mit eigenen oder Gastlehrern an. Die Termine stehen auf den Websites der Schulen.', '<strong>At the dance school:</strong> many schools offer workshops with their own or guest teachers. The dates are on the schools’ websites.'),
     ('<strong>Auf Festivals:</strong> Festivals bestehen aus Workshops am Tag und Partys am Abend. Siehe <a href="bachata-festivals-deutschland.html">Bachata-Festivals in Deutschland</a>.', '<strong>At festivals:</strong> festivals consist of workshops by day and parties in the evening. See <a href="bachata-festivals-deutschland.html">Bachata festivals in Germany</a>.'),
     ('<strong>Intensiv-Wochenenden:</strong> Mehrere Einheiten an einem Wochenende, oft mit einem Schwerpunkt wie Drehungen oder Sensual.', '<strong>Intensive weekends:</strong> several sessions on one weekend, often with a focus such as turns or Sensual.'),
     ('<strong>Universitäts- und Vereinsangebote:</strong> Manche Hochschulsportprogramme führen gelegentlich Bachata-Workshops.', '<strong>University and club offers:</strong> some university sports programmes occasionally run Bachata workshops.'),
   ]),
 ]),
 ('Themen und Stile bei Bachata Workshops', 'Topics and styles at Bachata workshops', [
   ('p', 'Typische Themen sind Grundschritt und Drehungen, Musikalität, Körperbewegung und Partnerarbeit. Stilworkshops behandeln <a href="bachata-dominicana.html">Bachata Dominicana</a>, <a href="bachata-moderna.html">Bachata Moderna</a> oder <a href="bachata-sensual.html">Bachata Sensual</a>. Für Tänzerinnen gibt es zusätzlich Angebote zu <a href="bachata-ladies-styling.html">Ladies Styling</a>.',
         'Typical topics are the basic step and turns, musicality, body movement and partner work. Style workshops cover <a href="bachata-dominicana.html">Bachata Dominicana</a>, <a href="bachata-moderna.html">Bachata Moderna</a> or <a href="bachata-sensual.html">Bachata Sensual</a>. For women dancers there are also offers on <a href="bachata-ladies-styling.html">ladies styling</a>.'),
 ]),
 ('Bachata Workshop auf Festivals und Kongressen', 'Bachata workshops at festivals and congresses', [
   ('p', 'Auf Festivals laufen mehrere Workshops parallel, meist nach Level getrennt. Du wählst vorab aus, welche Einheiten du besuchst, und tanzt abends auf den Partys. Das ist eine gute Gelegenheit, mehrere Lehrkräfte und Stile kennenzulernen. Eine Übersicht über Festivals steht auf der Seite <a href="bachata-festivals-deutschland.html">Bachata-Festivals 2026/2027</a>. Prüfe Termine, Programm und Preise immer auf der Website des Veranstalters.',
         'At festivals several workshops run in parallel, usually separated by level. You choose in advance which sessions to attend and dance at the parties in the evening. This is a good opportunity to get to know several teachers and styles. An overview of festivals is on the page <a href="bachata-festivals-deutschland.html">Bachata festivals 2026/2027</a>. Always check dates, programme and prices on the organiser’s website.'),
 ]),
 ('Bachata Workshop für Einsteiger', 'Bachata workshops for beginners', [
   ('p', 'Einsteiger-Workshops erklären den Grundschritt, das Zählen und erste Drehungen und eignen sich zum Reinschnuppern. Wenn du danach dranbleiben willst, ist ein regelmäßiger Kurs der nächste Schritt. Die Ratgeber <a href="bachata-fuer-anfaenger.html">Bachata für Anfänger</a> und <a href="bachata-schritte.html">Bachata Schritte</a> bereiten dich gut vor.',
         'Beginner workshops explain the basic step, counting and first turns and are good for a first taste. If you want to keep going afterwards, a regular class is the next step. The guides <a href="bachata-fuer-anfaenger.html">Bachata for beginners</a> and <a href="bachata-schritte.html">Bachata steps</a> prepare you well.'),
   ('p', 'Auch wer schon tanzt, profitiert: Ein Workshop zeigt dir neue Perspektiven und hilft, Gewohnheiten zu hinterfragen. Gerade bei Stilen wie Sensual lohnt sich der Blick von außen, weil die Körpertechnik schwer allein zu überprüfen ist.',
         'Those who already dance also benefit: a workshop shows you new perspectives and helps you question habits. Especially for styles like Sensual an outside view is worthwhile, because body technique is hard to check alone.'),
 ]),
 ('Fragen vor der Anmeldung', 'Questions before signing up', [
   ('ul', [
     ('<strong>Für welches Level?</strong> Anfänger, Fortgeschrittene oder offen für alle.', '<strong>Which level?</strong> Beginner, intermediate or open to all.'),
     ('<strong>Mit oder ohne Partner?</strong> Bei manchen Workshops wird gewechselt, bei anderen ist ein Partner nötig.', '<strong>With or without a partner?</strong> Some workshops rotate partners, others require one.'),
     ('<strong>Wer unterrichtet?</strong> Informiere dich über Lehrkräfte und deren Stil auf den Websites der Veranstalter.', '<strong>Who teaches?</strong> Find out about the teachers and their style on the organisers’ websites.'),
     ('<strong>Was kostet es?</strong> Preise und Dauer stehen beim Veranstalter. Wir nennen hier bewusst keine Zahlen, weil sie sich ändern.', '<strong>What does it cost?</strong> Prices and duration are with the organiser. We deliberately give no figures here because they change.'),
   ]),
 ]),
 ('So holst du das Meiste aus einem Workshop', 'How to get the most from a workshop', [
   ('ul', [
     ('<strong>Vorher den Grundschritt üben:</strong> Dann bleibt Zeit fürs Neue. Siehe <a href="bachata-grundschritt.html">Bachata Grundschritt</a>.', '<strong>Practise the basic step beforehand:</strong> then there is time for the new material. See <a href="bachata-grundschritt.html">Bachata basic step</a>.'),
     ('<strong>Nachher wiederholen:</strong> Übe das Gelernte in den Tagen danach, solange es frisch ist.', '<strong>Repeat afterwards:</strong> practise what you learned in the days after, while it is fresh.'),
     ('<strong>Auf einer Party anwenden:</strong> Termine siehst du bei den <a href="bachata-socials.html">Bachata-Socials</a>.', '<strong>Use it at a party:</strong> dates are on the <a href="bachata-socials.html">Bachata socials</a> page.'),
   ]),
 ]),
 ('Schulen mit Workshops finden', 'Finding schools with workshops', [
   ('p', f'Schulen mit Links zu ihren Websites findest du für {CITY_LINKS_DE}. Die Listen sind alphabetisch und keine Wertung. Aktuelle Workshop-Termine findest du dort bei den Schulen selbst. Das offizielle Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>, die Methode steht auf der <a href="index.html#method">Startseite</a>.',
         f'Schools with links to their websites are listed for {CITY_LINKS_EN}. The lists are alphabetical and not a rating. Current workshop dates are on the schools’ own sites. The official ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>, and the method is on the <a href="index.html#method">home page</a>.'),
   ('p', 'Du leitest eine Schule? <a href="bewerbung.html">Bewirb dich kostenlos bis zum 30. November</a>.',
         'Do you run a school? <a href="bewerbung.html">Apply for free by November 30</a>.'),
 ]),
]
ws_faq = [
 ('Was ist ein Bachata Workshop?', 'What is a Bachata workshop?',
  'Eine kurze Unterrichtseinheit zu einem Thema, meist an einem Abend oder Wochenende, im Gegensatz zu einem laufenden Kurs.',
  'A short teaching session on one topic, usually on an evening or weekend, as opposed to an ongoing class.'),
 ('Wo finde ich Bachata Workshops?', 'Where do I find Bachata workshops?',
  'Bei Tanzschulen, auf Festivals und bei Intensiv-Wochenenden. Aktuelle Termine stehen auf den Websites der Veranstalter.',
  'At dance schools, at festivals and at intensive weekends. Current dates are on the organisers’ websites.'),
 ('Ist ein Workshop für Anfänger geeignet?', 'Is a workshop suitable for beginners?',
  'Ja, wenn er als Anfänger- oder offener Workshop ausgeschrieben ist. Für den ersten Einstieg ist meist ein Kurs besser.',
  'Yes, if it is advertised as a beginner or open workshop. For the very first start a class is usually better.'),
 ('Brauche ich einen Partner für einen Bachata Workshop?', 'Do I need a partner for a Bachata workshop?',
  'Das hängt vom Workshop ab. Oft wird gewechselt. Die Ausschreibung nennt es meist, sonst frag beim Veranstalter nach.',
  'It depends on the workshop. Partners are often rotated. The listing usually says, otherwise ask the organiser.'),
 ('Was kostet ein Bachata Workshop?', 'How much does a Bachata workshop cost?',
  'Das legt der Veranstalter fest und es ändert sich. Aktuelle Preise stehen auf den Websites der Schulen und Festivals.',
  'The organiser sets it and it changes. Current prices are on the schools’ and festivals’ websites.'),
 ('Wann erscheint das Ranking der Bachata-Schulen?', 'When is the ranking of Bachata schools published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html">ranking page</a>.'),
]
guide_page('bachata-workshop', 'bws',
  'Bachata Workshop: Formate, Themen und Tipps',
  'Bachata Workshop finden und wählen: Unterschied zum Kurs, Formate von Tanzschule bis Festival, Themen und Fragen vor der Anmeldung. Mit Links zu Schulen.',
  'Bachata workshop: formats, topics and tips',
  'Find and choose a Bachata workshop: difference from a class, formats from dance school to festival, topics and questions before signing up. With links to schools.',
  'Bachata Workshop', ('Bachata Workshop · Ratgeber', 'Bachata workshop · Guide'),
  ('Bachata Workshop: <em class="foil">Formate</em> und Themen', 'Bachata workshop: <em class="foil">formats</em> and topics'),
  ('Bachata Workshop finden und wählen: Unterschied zum Kurs, Formate von Tanzschule bis Festival, Themen und die richtigen Fragen vor der Anmeldung.',
   'Find and choose a Bachata workshop: difference from a class, formats from dance school to festival, topics and the right questions before signing up.'),
  [('check', 'Für <b>Einsteiger</b> und Fortgeschrittene', 'For <b>beginners</b> and advanced dancers'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  ws_sections, ws_faq, sibling_group='topic')

# ---- Support pages (Nov 2026): Kurs in der Nähe, Solo, Hochzeitstanz ----
def _closing(what_de, what_en):
    return ('Schulen in deiner Stadt finden', 'Finding schools in your city', [
        ('p', f'Schulen mit Links zu ihren Websites findest du für {CITY_LINKS_DE}. Die Listen sind alphabetisch und keine Wertung. {what_de} Das offizielle Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html">Ranking-Seite</a>, die Methode steht auf der <a href="deutschland.html#method">Startseite</a>. Eine Übersicht aller Städte gibt es unter <a href="bachata-staedte-deutschland.html">Alle Städte und Schulen</a>.',
              f'Schools with links to their websites are listed for {CITY_LINKS_EN}. The lists are alphabetical and not a rating. {what_en} The official ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html">ranking page</a>, and the method is on the <a href="deutschland.html#method">homepage</a>. An overview of all cities is on <a href="bachata-staedte-deutschland.html">All cities and schools</a>.'),
        ('p', 'Du leitest eine Schule? <a href="bewerbung.html">Bewirb dich kostenlos bis zum 30. November</a>.',
              'Do you run a school? <a href="bewerbung.html">Apply for free by November 30</a>.'),
    ])
_rank_faq = ('Wann erscheint das Ranking der Bachata-Schulen?', 'When is the ranking of Bachata schools published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html">ranking page</a>.')

kin_sections = [
 ('Bachata Kurs in der Nähe finden: So gehst du vor', 'Finding a Bachata class near you: how to proceed', [
   ('p', 'Wer „Bachata Kurs in der Nähe“ sucht, will meist drei Dinge wissen: Gibt es einen Kurs in meiner Stadt, passt der Termin und ist er für mich geeignet? Eine Karte mit Treffern beantwortet nur die erste Frage. Die anderen beiden klärst du am besten auf den Websites der Schulen, und dafür brauchst du eine kurze Liste statt hundert Treffer.',
         'Anyone searching for “Bachata class near me” usually wants three things: is there a class in my city, does the time fit and is it suitable for me? A map of results only answers the first question. You settle the other two best on the schools’ websites, and for that you need a short list instead of a hundred results.'),
   ('p', 'Auf Latin Dance Awards sind die Schulen nach Städten geordnet, mit Link zur jeweiligen Website. Starte bei deiner Stadt, öffne zwei oder drei Schulen und vergleiche dort Kursplan, Level und Probestunde. Eine Übersicht aller Städte findest du unter <a href="bachata-staedte-deutschland.html">Alle Städte und Schulen</a>.',
         'On Latin Dance Awards the schools are sorted by city, with a link to each website. Start with your city, open two or three schools and compare timetable, level and trial lesson there. An overview of all cities is on <a href="bachata-staedte-deutschland.html">All cities and schools</a>.'),
 ]),
 ('Schritt für Schritt zum passenden Kurs', 'Step by step to the right class', [
   ('ul', [
     ('<strong>1. Stadt und Anfahrt festlegen:</strong> Ein Kurs, den du in 20 Minuten erreichst, besuchst du eher regelmäßig als einen, der eine Stunde entfernt ist.', '<strong>1. Fix city and travel:</strong> you are more likely to attend a class regularly if you can reach it in 20 minutes than one an hour away.'),
     ('<strong>2. Level prüfen:</strong> Suche nach „Anfänger“, „Level 1“ oder „Grundkurs“. Wenn du schon tanzt, achte auf „Mittelstufe“ oder „Level 2“. Mehr dazu unter <a href="bachata-fuer-anfaenger.html">Bachata für Anfänger</a>.', '<strong>2. Check the level:</strong> look for “beginner”, “level 1” or “basic class”. If you already dance, look for “intermediate” or “level 2”. More on <a href="bachata-fuer-anfaenger.html">Bachata for beginners</a>.'),
     ('<strong>3. Stil klären:</strong> Bachata hat mehrere Stile, die Kurse unterscheiden sich spürbar. Siehe <a href="bachata-sensual.html">Bachata Sensual</a>, <a href="bachata-moderna.html">Bachata Moderna</a> und <a href="bachata-dominicana.html">Bachata Dominicana</a>.', '<strong>3. Clarify the style:</strong> Bachata has several styles and classes differ noticeably. See <a href="bachata-sensual.html">Bachata Sensual</a>, <a href="bachata-moderna.html">Bachata Moderna</a> and <a href="bachata-dominicana.html">Bachata Dominicana</a>.'),
     ('<strong>4. Termin und Format:</strong> Läuft der Kurs fortlaufend, oder startet ein neuer Block? Für Einsteiger ist ein Blockstart oft angenehmer, weil alle gleichzeitig beginnen.', '<strong>4. Date and format:</strong> does the class run continuously, or does a new block start? For beginners a block start is often more comfortable because everyone begins at the same time.'),
     ('<strong>5. Probestunde fragen:</strong> Viele Schulen bieten eine Schnupperstunde an. Ob und zu welchen Bedingungen, steht auf der Website der Schule.', '<strong>5. Ask about a trial lesson:</strong> many schools offer a taster lesson. Whether and on what terms is on the school’s website.'),
   ]),
 ]),
 ('Woran du einen guten Kurs erkennst', 'How to recognise a good class', [
   ('p', 'Ein guter Einsteigerkurs erklärt den Grundschritt langsam, zählt laut mit und lässt dich schon in der ersten Stunde zur Musik tanzen. Du solltest den Wechsel zwischen Führen und Folgen ausprobieren dürfen, und die Gruppe sollte so groß sein, dass die Lehrkraft Fehler noch sieht. Was ein Kurs vermitteln sollte, steht auch im Ratgeber <a href="bachata-tanzkurs.html">Bachata Tanzkurs</a>.',
         'A good beginner class explains the basic step slowly, counts out loud and lets you dance to the music in the very first lesson. You should be allowed to try both leading and following, and the group should be small enough for the teacher to still see mistakes. What a class should teach is also covered in the guide <a href="bachata-tanzkurs.html">Bachata dance class</a>.'),
   ('p', 'Ein Kurs ist nicht automatisch besser, weil er mehr Bewertungen hat. Eine Liste aller Kurse einer Stadt sagt noch nichts über die Qualität. Genau deshalb bewerten wir Schulen mit einer offenen Methode, deren Ergebnis am 20. Dezember 2026 erscheint.',
         'A class is not automatically better because it has more reviews. A list of all classes in a city says nothing about quality. That is exactly why we assess schools with an open method, and the result is published on December 20, 2026.'),
 ]),
 ('Kurs ohne Partner: Geht das?', 'Class without a partner: does it work?', [
   ('p', 'Ja. In den meisten Bachata-Kursen für Einsteiger wird gewechselt, du brauchst also keinen festen Partner. Schreibe der Schule vorher kurz, wenn du allein kommst, dann kann sie auf das Verhältnis in der Gruppe achten. Wer lieber erst allein übt, findet Ideen auf der Seite <a href="bachata-solo.html">Bachata Solo</a>.',
         'Yes. In most Bachata classes for beginners partners are rotated, so you do not need a fixed partner. Send the school a short note beforehand if you come alone, so it can keep an eye on the balance in the group. If you prefer to practise alone first, you will find ideas on the page <a href="bachata-solo.html">Bachata solo</a>.'),
 ]),
 ('Alternativen zum klassischen Kurs', 'Alternatives to a regular class', [
   ('ul', [
     ('<strong>Workshop:</strong> Ein Thema an einem Abend oder Wochenende, siehe <a href="bachata-workshop.html">Bachata Workshop</a>.', '<strong>Workshop:</strong> one topic on an evening or weekend, see <a href="bachata-workshop.html">Bachata workshop</a>.'),
     ('<strong>Hochschulsport:</strong> Viele Universitäten und Hochschulen führen Bachata im Sportprogramm. Das gilt meist nur für Studierende, die Anmeldung läuft über das Hochschulsport-Portal.', '<strong>University sport:</strong> many universities and colleges include Bachata in their sports programme. This usually applies to students only, and registration goes through the university sport portal.'),
     ('<strong>Social mit Einführung:</strong> Manche Partys beginnen mit einer kurzen Einführungsstunde. Termine siehe <a href="bachata-socials.html">Bachata-Socials</a> und <a href="bachata-party.html">Bachata Party</a>.', '<strong>Social with an introduction:</strong> some parties start with a short introductory lesson. Dates are on <a href="bachata-socials.html">Bachata socials</a> and <a href="bachata-party.html">Bachata party</a>.'),
   ]),
 ]),
 ('Was du zum ersten Kurs mitbringst', 'What to bring to your first class', [
   ('ul', [
     ('Bequeme Kleidung und Schuhe, mit denen du dich auf dem Boden drehen kannst.', 'Comfortable clothes and shoes in which you can turn on the floor.'),
     ('Etwas zu trinken und ein Handtuch.', 'Something to drink and a towel.'),
     ('Etwas Zeit vorher, um die Schule zu finden und anzukommen.', 'A little time beforehand to find the school and arrive.'),
     ('Den Grundschritt kannst du vorher anschauen, siehe <a href="bachata-grundschritt.html">Bachata Grundschritt</a>. Nötig ist das nicht.', 'You can look at the basic step beforehand, see <a href="bachata-grundschritt.html">Bachata basic step</a>. It is not required.'),
   ]),
 ]),
 _closing('Aktuelle Kurszeiten stehen bei den Schulen selbst.', 'Current class times are on the schools’ own sites.'),
]
kin_faq = [
 ('Wie finde ich einen Bachata Kurs in meiner Nähe?', 'How do I find a Bachata class near me?',
  'Wähle deine Stadt auf Latin Dance Awards, öffne zwei bis drei Schulen und vergleiche Kursplan, Level und Probestunde auf deren Websites.',
  'Pick your city on Latin Dance Awards, open two to three schools and compare timetable, level and trial lesson on their websites.'),
 ('Gibt es Bachata Kurse für Anfänger ohne Vorkenntnisse?', 'Are there Bachata classes for beginners without experience?',
  'Ja, die meisten Schulen bieten einen Anfänger- oder Grundkurs an. Suche nach „Level 1“, „Anfänger“ oder „Grundkurs“.',
  'Yes, most schools offer a beginner or basic class. Look for “level 1”, “beginner” or “basic class”.'),
 ('Brauche ich einen Partner für einen Bachata Kurs?', 'Do I need a partner for a Bachata class?',
  'In den meisten Einsteigerkursen nicht, es wird gewechselt. Im Zweifel frag die Schule.',
  'In most beginner classes you do not, partners are rotated. If in doubt, ask the school.'),
 ('Kann ich vorher eine Probestunde machen?', 'Can I try a lesson first?',
  'Viele Schulen bieten das an. Ob und zu welchen Bedingungen, steht auf der Website der Schule.',
  'Many schools offer this. Whether and on what terms is on the school’s website.'),
 ('Was kostet ein Bachata Kurs?', 'How much does a Bachata class cost?',
  'Das legt jede Schule selbst fest und es ändert sich. Aktuelle Preise stehen auf der Website der Schule. Wir nennen hier bewusst keine Zahlen.',
  'Each school sets this itself and it changes. Current prices are on the school’s website. We deliberately give no figures here.'),
 _rank_faq,
]
guide_page('bachata-kurs-in-der-naehe', 'bkn',
  'Bachata Kurs in der Nähe: So findest du den richtigen',
  'Bachata Kurs in der Nähe finden: Schritt für Schritt zum passenden Kurs, woran du einen guten Kurs erkennst, Kurs ohne Partner und Alternativen. Mit Links zu Schulen.',
  'Bachata class near you: how to find the right one',
  'Find a Bachata class near you: step by step to the right class, how to recognise a good one, classes without a partner and alternatives. With links to schools.',
  'Bachata Kurs in der Nähe', ('Bachata Kurs in der Nähe · Ratgeber', 'Bachata class near you · Guide'),
  ('Bachata Kurs <em class="foil">in der Nähe</em> finden', 'Find a Bachata class <em class="foil">near you</em>'),
  ('So findest du einen Bachata Kurs in deiner Stadt: Level, Stil, Termin und Probestunde in fünf Schritten, plus Links zu Schulen nach Städten.',
   'How to find a Bachata class in your city: level, style, date and trial lesson in five steps, plus links to schools by city.'),
  [('check', 'Für <b>Einsteiger</b> ohne Partner', 'For <b>beginners</b> without a partner'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  kin_sections, kin_faq, sibling_group='topic')

solo_sections = [
 ('Bachata Solo: Was ist das?', 'Bachata solo: what is it?', [
   ('p', 'Bachata ist ein Paartanz, aber du kannst vieles davon allein üben und manche Kurse sind ausdrücklich ohne Partner. „Bachata Solo“ meint deshalb zwei Dinge: Üben für dich zu Hause und Kurse, in denen jede Person für sich tanzt, zum Beispiel mit Fokus auf Grundschritt, Körperbewegung und Musikalität. In solchen Kursen wird meist kein Partner gebraucht und nicht gewechselt.',
         'Bachata is a partner dance, but you can practise much of it alone, and some classes are explicitly without a partner. “Bachata solo” therefore means two things: practising for yourself at home and classes in which each person dances alone, for example with a focus on basic step, body movement and musicality. In such classes you usually do not need a partner and do not rotate.'),
   ('p', 'Solo ersetzt den Paartanz nicht, bereitet ihn aber gut vor. Wer sicher im Grundschritt und im Rhythmus ist, kommt im Paarkurs schneller mit. Mehr zum Einstieg im Ratgeber <a href="bachata-tanzen.html">Bachata tanzen lernen</a>.',
         'Solo does not replace partner dancing, but it prepares for it well. If you are secure in the basic step and rhythm, you keep up faster in a partner class. More on getting started in the guide <a href="bachata-tanzen.html">Learn to dance Bachata</a>.'),
 ]),
 ('Was du allein üben kannst', 'What you can practise alone', [
   ('ul', [
     ('<strong>Grundschritt:</strong> Drei Schritte, ein Tap, und zurück. Zähle laut mit, siehe <a href="bachata-grundschritt.html">Bachata Grundschritt</a>.', '<strong>Basic step:</strong> three steps, a tap, and back. Count out loud, see <a href="bachata-grundschritt.html">Bachata basic step</a>.'),
     ('<strong>Rhythmus und Zählzeiten:</strong> Höre Bachata-Songs und finde die Betonung auf der vierten Zählzeit. Lieder zum Üben nennt <a href="bachata-musik.html">Bachata Musik</a>.', '<strong>Rhythm and counts:</strong> listen to Bachata songs and find the emphasis on count four. Songs to practise with are on <a href="bachata-musik.html">Bachata music</a>.'),
     ('<strong>Hüftbewegung:</strong> Die seitliche Hüftbewegung im Schritt kannst du vor dem Spiegel prüfen.', '<strong>Hip movement:</strong> you can check the sideways hip movement in the step in front of a mirror.'),
     ('<strong>Drehungen:</strong> Einfache Eigendrehungen übst du ohne Partner und merkst, ob du ruhig auf dem Standbein bleibst.', '<strong>Turns:</strong> simple solo turns can be practised without a partner and you notice whether you stay steady on the standing leg.'),
     ('<strong>Arm- und Körperarbeit:</strong> Besonders im Sensual-Stil, siehe <a href="bachata-sensual.html">Bachata Sensual</a>, und im Ladies Styling, siehe <a href="bachata-ladies-styling.html">Bachata Ladies Styling</a>.', '<strong>Arm and body work:</strong> especially in the Sensual style, see <a href="bachata-sensual.html">Bachata Sensual</a>, and in ladies styling, see <a href="bachata-ladies-styling.html">Bachata ladies styling</a>.'),
   ]),
 ]),
 ('Ein einfacher Übungsplan für zu Hause', 'A simple practice plan for home', [
   ('p', 'Kurze Einheiten sind besser als eine lange. Fünfzehn bis zwanzig Minuten reichen, wenn du konzentriert übst:',
         'Short sessions are better than one long one. Fifteen to twenty minutes are enough if you practise with focus:'),
   ('ul', [
     ('Erst aufwärmen: Fußgelenke, Knie und Hüfte lockern.', 'Warm up first: loosen ankles, knees and hips.'),
     ('Grundschritt ohne Musik zählen, dann mit Musik.', 'Count the basic step without music, then with music.'),
     ('Ein Element pro Einheit: Hüfte, Eigendrehung oder Gewichtsverlagerung.', 'One element per session: hips, solo turn or weight transfer.'),
     ('Zum Schluss frei zur Musik tanzen, ohne zu bewerten.', 'Finish by dancing freely to the music without judging.'),
   ]),
 ]),
 ('Kurse ohne Partner finden', 'Finding classes without a partner', [
   ('p', 'Wenn eine Schule einen Solo-, Styling- oder Einzelkurs anbietet, steht das auf ihrer Website. Frage sonst nach, ob du in einem normalen Anfängerkurs ohne Partner mitmachen kannst, denn dort wird meist gewechselt. Wie du Kurse in deiner Stadt findest, steht auf der Seite <a href="bachata-kurs-in-der-naehe.html">Bachata Kurs in der Nähe</a>.',
         'If a school offers a solo, styling or individual class, it says so on its website. Otherwise ask whether you can join a regular beginner class without a partner, because partners are usually rotated there. How to find classes in your city is on the page <a href="bachata-kurs-in-der-naehe.html">Bachata class near you</a>.'),
   ('p', 'Auch Hochschulsport-Programme und Vereine haben gelegentlich Solo-Angebote. Ob es sie gibt, entscheidet der jeweilige Anbieter.',
         'University sport programmes and clubs occasionally have solo offers, too. Whether they exist is up to the respective provider.'),
 ]),
 ('Solo üben und dann zur Party', 'Practise solo, then go to a party', [
   ('p', 'Wer allein geübt hat, wirkt auf der Tanzfläche meist entspannter. Auf Partys wird oft getanzt, ohne dass du einen Partner mitbringen musst. Termine stehen unter <a href="bachata-socials.html">Bachata-Socials</a>, Tipps zum Verhalten unter <a href="bachata-party.html">Bachata Party</a>.',
         'If you have practised alone, you usually look more relaxed on the dance floor. At parties you often dance without having to bring a partner. Dates are on <a href="bachata-socials.html">Bachata socials</a>, tips on behaviour on <a href="bachata-party.html">Bachata party</a>.'),
 ]),
 _closing('Ob eine Schule Solo-Angebote hat, steht auf ihrer eigenen Website.', 'Whether a school has solo offers is on its own website.'),
]
solo_faq = [
 ('Kann man Bachata alleine tanzen?', 'Can you dance Bachata alone?',
  'Ja, Grundschritt, Rhythmus, Hüftbewegung und Eigendrehungen lassen sich allein üben. Der Paartanz selbst braucht natürlich einen Partner.',
  'Yes, the basic step, rhythm, hip movement and solo turns can be practised alone. The partner dance itself of course needs a partner.'),
 ('Gibt es Bachata Solo Kurse?', 'Are there Bachata solo classes?',
  'Manche Schulen bieten sie an, meist mit Fokus auf Grundschritt, Körperbewegung oder Styling. Ob es sie gibt, steht auf der Website der Schule.',
  'Some schools offer them, usually with a focus on basic step, body movement or styling. Whether they exist is on the school’s website.'),
 ('Wie lerne ich Bachata zu Hause?', 'How do I learn Bachata at home?',
  'Mit kurzen Übungseinheiten: Grundschritt zählen, zur Musik tanzen und pro Einheit ein Element üben. Siehe auch <a href="bachata-grundschritt.html">Bachata Grundschritt</a>.',
  'With short practice sessions: count the basic step, dance to the music and practise one element per session. See also <a href="bachata-grundschritt.html">Bachata basic step</a>.'),
 ('Brauche ich einen Partner, um Bachata zu lernen?', 'Do I need a partner to learn Bachata?',
  'Nein. In den meisten Einsteigerkursen wird gewechselt. Im Zweifel frag die Schule.',
  'No. In most beginner classes partners are rotated. If in doubt, ask the school.'),
 _rank_faq,
]
guide_page('bachata-solo', 'bso',
  'Bachata Solo: Allein üben und Kurse ohne Partner',
  'Bachata solo tanzen: was du allein üben kannst, ein Übungsplan für zu Hause, Kurse ohne Partner und der Weg zur Party. Mit Links zu Schulen.',
  'Bachata solo: practise alone and classes without a partner',
  'Bachata solo: what you can practise alone, a practice plan for home, classes without a partner and the way to the party. With links to schools.',
  'Bachata Solo', ('Bachata Solo · Ratgeber', 'Bachata solo · Guide'),
  ('Bachata Solo: <em class="foil">allein üben</em>, ohne Partner lernen', 'Bachata solo: <em class="foil">practise alone</em>, learn without a partner'),
  ('Bachata ist ein Paartanz, doch vieles lässt sich allein üben. Hier steht, was, wie und wo, plus ein einfacher Plan für zu Hause.',
   'Bachata is a partner dance, but much of it can be practised alone. Here is what, how and where, plus a simple plan for home.'),
  [('check', 'Auch <b>ohne Partner</b>', 'Also <b>without a partner</b>'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  solo_sections, solo_faq, sibling_group='topic')

hz_sections = [
 ('Bachata als Hochzeitstanz: Passt das?', 'Bachata as a wedding dance: does it fit?', [
   ('p', 'Ein Hochzeitstanz muss nicht der klassische Walzer sein. Viele Paare wählen einen Tanz, der zu ihnen passt, und Bachata ist dafür beliebt: Der Takt ist ruhig, der Schritt ist schnell gelernt und die Bewegung ist nah und persönlich. Gerade weil der Grundschritt so einfach ist, können auch Paare ohne Tanzerfahrung in wenigen Wochen eine kleine Choreografie lernen.',
         'A wedding dance does not have to be the classic waltz. Many couples choose a dance that suits them, and Bachata is popular for this: the beat is calm, the step is learned quickly and the movement is close and personal. Precisely because the basic step is so simple, even couples without dance experience can learn a small choreography in a few weeks.'),
   ('p', 'Wie schnell das geht, hängt von euch ab, von der Übungszeit und vom Lehrer. Wir versprechen hier keine feste Zahl an Stunden. Fragt die Schule, wie sie einen Hochzeitstanz plant.',
         'How fast it goes depends on you, on practice time and on the teacher. We do not promise a fixed number of lessons here. Ask the school how it plans a wedding dance.'),
 ]),
 ('Welcher Bachata-Stil für die Hochzeit?', 'Which Bachata style for the wedding?', [
   ('ul', [
     ('<strong>Bachata Dominicana:</strong> Der ursprüngliche Stil mit schnellem Fußwerk und lebendiger Stimmung. Siehe <a href="bachata-dominicana.html">Bachata Dominicana</a>.', '<strong>Bachata Dominicana:</strong> the original style with quick footwork and a lively mood. See <a href="bachata-dominicana.html">Bachata Dominicana</a>.'),
     ('<strong>Bachata Moderna:</strong> Mehr Drehungen und Figuren, oft auf Pop-Bachata. Siehe <a href="bachata-moderna.html">Bachata Moderna</a>.', '<strong>Bachata Moderna:</strong> more turns and figures, often to pop Bachata. See <a href="bachata-moderna.html">Bachata Moderna</a>.'),
     ('<strong>Bachata Sensual:</strong> Enge Verbindung und weiche Körperbewegung, eher romantisch. Siehe <a href="bachata-sensual.html">Bachata Sensual</a>.', '<strong>Bachata Sensual:</strong> close connection and soft body movement, rather romantic. See <a href="bachata-sensual.html">Bachata Sensual</a>.'),
   ]),
   ('p', 'Für einen Hochzeitstanz ist weniger oft mehr. Eine ruhige Moderna- oder Sensual-Variante mit wenigen sauberen Elementen wirkt meist besser als viele schnelle Figuren. Das ist eine Empfehlung, keine Regel.',
         'For a wedding dance less is often more. A calm Moderna or Sensual variant with a few clean elements usually looks better than many fast figures. This is a suggestion, not a rule.'),
 ]),
 ('Das Lied wählen', 'Choosing the song', [
   ('p', 'Wählt ein Lied, das ihr beide mögt und das sich gut zählen lässt. Bachata-Lieder haben einen klaren Takt, aber nicht jedes Lied passt für eine Choreografie. Lehrkräfte können beim Zuschneiden der Länge helfen: Viele Paare tanzen nicht das ganze Lied, sondern etwa zwei Minuten. Mehr zur Musik findet ihr auf der Seite <a href="bachata-musik.html">Bachata Musik</a>.',
         'Choose a song you both like and that is easy to count. Bachata songs have a clear beat, but not every song suits a choreography. Teachers can help trim the length: many couples do not dance the whole song but about two minutes. You will find more on the music on the page <a href="bachata-musik.html">Bachata music</a>.'),
 ]),
 ('So bereitet ihr euch vor', 'How to prepare', [
   ('ul', [
     ('<strong>Früh anfangen:</strong> Plant genug Zeit ein, damit ihr ohne Druck üben könnt. Fragt bei der Schule, wann ihr starten solltet.', '<strong>Start early:</strong> allow enough time so you can practise without pressure. Ask the school when you should start.'),
     ('<strong>Grundschritt sichern:</strong> Beginnt mit dem Grundschritt, siehe <a href="bachata-grundschritt.html">Bachata Grundschritt</a>, und baut erst dann Drehungen auf.', '<strong>Secure the basic step:</strong> begin with the basic step, see <a href="bachata-grundschritt.html">Bachata basic step</a>, and add turns only then.'),
     ('<strong>Im Outfit üben:</strong> Probiert Schuhe und Kleidung vor dem Tag aus, besonders Absätze und lange Röcke.', '<strong>Practise in the outfit:</strong> try shoes and clothing before the day, especially heels and long skirts.'),
     ('<strong>Auf dem Boden proben:</strong> Fragt, ob ihr auf einem ähnlichen Boden wie am Hochzeitstag üben könnt.', '<strong>Rehearse on the floor:</strong> ask whether you can practise on a floor similar to the wedding venue.'),
     ('<strong>Einen Plan B haben:</strong> Wenn ihr nervös seid, einigt euch auf eine kurze Version, die ihr sicher beherrscht.', '<strong>Have a plan B:</strong> if you are nervous, agree on a short version you master securely.'),
   ]),
 ]),
 ('Privatstunden, Gruppenkurs oder Paarkurs?', 'Private lessons, group class or couples class?', [
   ('p', 'Für einen Hochzeitstanz entscheiden sich viele Paare für Privatstunden, weil die Choreografie dann genau auf Lied und Können zugeschnitten wird. Ein Gruppenkurs ist dagegen eine gute Basis, wenn ihr erst einmal ein Gefühl für den Tanz bekommen wollt. Ob eine Schule Hochzeitstanz-Kurse anbietet und wie sie ablaufen, steht auf der Website der Schule. Eine Einführung in Kurse findet ihr unter <a href="bachata-tanzkurs.html">Bachata Tanzkurs</a> und <a href="bachata-kurs-in-der-naehe.html">Bachata Kurs in der Nähe</a>.',
         'Many couples choose private lessons for a wedding dance because the choreography is then tailored exactly to the song and ability. A group class, on the other hand, is a good base if you first want to get a feel for the dance. Whether a school offers wedding dance classes and how they work is on the school’s website. You will find an introduction to classes at <a href="bachata-tanzkurs.html">Bachata dance class</a> and <a href="bachata-kurs-in-der-naehe.html">Bachata class near you</a>.'),
 ]),
 ('Fragen an die Tanzschule', 'Questions for the dance school', [
   ('ul', [
     ('Bietet die Schule Hochzeitstanz an, und in welchem Format?', 'Does the school offer wedding dance, and in what format?'),
     ('Wie läuft die Planung: Liedwahl, Aufbau, Proben?', 'How does planning work: song choice, structure, rehearsals?'),
     ('Kann die Choreografie an unser Niveau angepasst werden?', 'Can the choreography be adapted to our level?'),
     ('Was kostet es und was ist enthalten? Preise nennen wir hier bewusst nicht, weil sie sich ändern.', 'What does it cost and what is included? We deliberately give no prices here because they change.'),
   ]),
 ]),
 _closing('Ob eine Schule Hochzeitstanz anbietet, steht auf ihrer eigenen Website.', 'Whether a school offers wedding dance is on its own website.'),
]
hz_faq = [
 ('Kann man Bachata als Hochzeitstanz tanzen?', 'Can you dance Bachata as a wedding dance?',
  'Ja. Der Grundschritt ist einfach, der Takt ruhig. Viele Paare wählen eine kurze Choreografie mit wenigen Elementen.',
  'Yes. The basic step is simple and the beat calm. Many couples choose a short choreography with a few elements.'),
 ('Wie früh sollten wir mit dem Hochzeitstanz anfangen?', 'How early should we start the wedding dance?',
  'Das hängt von euch und der Schule ab. Plant genug Zeit ein und fragt die Schule nach ihrer Empfehlung.',
  'That depends on you and the school. Allow enough time and ask the school for its recommendation.'),
 ('Welcher Stil eignet sich am besten?', 'Which style suits best?',
  'Das ist Geschmackssache. Ruhige Moderna- oder Sensual-Varianten mit wenigen sauberen Elementen wirken oft gut, Dominicana ist lebendiger.',
  'That is a matter of taste. Calm Moderna or Sensual variants with a few clean elements often look good, Dominicana is livelier.'),
 ('Brauchen wir Tanzerfahrung?', 'Do we need dance experience?',
  'Nein. Der Bachata-Grundschritt ist leicht zu lernen. Eine Lehrkraft passt die Choreografie an euer Niveau an.',
  'No. The Bachata basic step is easy to learn. A teacher adapts the choreography to your level.'),
 ('Was kostet ein Hochzeitstanz-Kurs?', 'How much does a wedding dance course cost?',
  'Das legt jede Schule selbst fest und es ändert sich. Fragt direkt bei der Schule nach.',
  'Each school sets this itself and it changes. Ask the school directly.'),
 _rank_faq,
]
guide_page('bachata-hochzeitstanz', 'bhz',
  'Bachata Hochzeitstanz: Stil, Lied und Vorbereitung',
  'Bachata als Hochzeitstanz: Passt das, welcher Stil, Liedwahl, Vorbereitung, Privatstunden oder Kurs und Fragen an die Tanzschule. Mit Links zu Schulen.',
  'Bachata wedding dance: style, song and preparation',
  'Bachata as a wedding dance: does it fit, which style, choosing the song, preparation, private lessons or class and questions for the dance school. With links to schools.',
  'Bachata Hochzeitstanz', ('Bachata Hochzeitstanz · Ratgeber', 'Bachata wedding dance · Guide'),
  ('Bachata <em class="foil">Hochzeitstanz</em>: Stil, Lied, Vorbereitung', 'Bachata <em class="foil">wedding dance</em>: style, song, preparation'),
  ('Ihr wollt zu eurer Hochzeit Bachata tanzen? Hier steht, welcher Stil passt, wie ihr das Lied wählt und wie ihr euch vorbereitet.',
   'Want to dance Bachata at your wedding? Here is which style fits, how to choose the song and how to prepare.'),
  [('check', 'Auch ohne <b>Tanzerfahrung</b>', 'Also without <b>dance experience</b>'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  hz_sections, hz_faq, sibling_group='topic')

# ---- Berlin support pages (Nov 2026): strengthen the biggest city cluster ----
def _berlin_cards(extra_de=None):
    return ('cards', [
     {'name': 'BachatAcademy', 'url': 'https://www.bachatacademy.de',
      'de': 'Studio in der Samariterstraße 34 in Friedrichshain. Auf der Website steht eine kostenlose, unverbindliche Probestunde, du brauchst weder Erfahrung noch Partner. Die Partner wechseln im Kurs regelmäßig. Genannt sind zwölf Lehrer sowie Bachata Sensual und Conscious Bachata.',
      'en': 'Studio at Samariterstraße 34 in Friedrichshain. The website lists a free, no-obligation trial class, and you need neither experience nor a partner. Partners rotate in class. It names twelve teachers plus Bachata Sensual and Conscious Bachata.'},
     {'name': 'Cumbancha', 'url': 'https://www.cumbancha.de',
      'de': 'Berliner Tanzschule mit Bachata-Kursen im Programm.',
      'en': 'Berlin dance school with Bachata classes in its programme.'},
     {'name': 'HAVANNA Berlin', 'url': 'https://www.havanna-berlin.de/dance-lesson',
      'de': 'Tanzschule mit Latin-Programm, auf der Website gibt es eine eigene Seite zu den Tanzkursen.',
      'en': 'Dance school with a Latin programme, with a dedicated page for dance classes on its website.'},
     {'name': 'La Mambita', 'url': 'https://www.mambita.de/bachata',
      'de': 'Studio in Schöneberg, mit S-Bahn und U-Bahn gut erreichbar. Schwerpunkt Bachata Sensual und Moderna mit kurzen Ausflügen in Dominicana. Dienstags laufen vier Levels nacheinander, Drop-in ist möglich und Urban Sports Club wird akzeptiert.',
      'en': 'Studio in Schöneberg, easy to reach by S-Bahn and U-Bahn. Focus on Bachata Sensual and Moderna with short excursions into Dominicana. On Tuesdays four levels run back to back, drop-in is possible and Urban Sports Club is accepted.'},
     {'name': 'Traumtänzer', 'url': 'https://www.traumtaenzer.de',
      'de': 'Tanzschule, die bei der Suche nach einem Bachata-Kurs in Berlin auftaucht.',
      'en': 'Dance school that appears when searching for a Bachata class in Berlin.'},
     {'name': 'Zapatissimo', 'url': 'https://www.zapatissimo.de/bachata-kurse-berlin',
      'de': 'Tanzschule mit eigener Seite für Bachata-Kurse in Berlin, unter anderem mit Bootcamp-Angeboten.',
      'en': 'Dance school with its own page for Bachata classes in Berlin, including bootcamp formats.'},
    ])

_BERLIN_APPLY = ('p', 'Deine Schule fehlt oder die Angaben stimmen nicht mehr? Schreib uns über die <a href="bewerbung.html">kostenlose Bewerbung</a>, wir ergänzen und korrigieren.',
                      'Is your school missing, or are the details out of date? Send us the <a href="bewerbung.html">free application</a> and we will add or correct it.')
_BERLIN_SCORE = ('So bewerten wir die Berliner Schulen', 'How we score the Berlin schools', [
   ('p', 'Das Berliner Ranking erscheint am <strong>20. Dezember 2026</strong> auf der <a href="rankings.html#berlin">Ranking-Seite</a>. Jede Schule wird nach denselben neun öffentlichen Kriterien mit zusammen 100 Punkten bewertet, unter anderem Google-Bewertung, Festivals, Jahre aktiv, Kursangebot für Einsteiger, Events und Social Media. Plätze sind nicht käuflich, die Methode steht auf der <a href="index.html#method">Startseite</a>. Die Gesamtübersicht für die Stadt findest du auf <a href="bachata-berlin.html">Bachata Berlin</a>.',
         'The Berlin ranking is published on <strong>December 20, 2026</strong> on the <a href="rankings.html#berlin">ranking page</a>. Every school is scored on the same nine public factors, 100 points in total, including Google rating, festivals, years active, beginner offer, events and social media. Places cannot be bought, and the method is on the <a href="index.html#method">homepage</a>. The full overview for the city is on <a href="bachata-berlin.html">Bachata Berlin</a>.'),
   ('p', 'Du leitest eine Schule in Berlin? <a href="bewerbung.html">Bewirb dich bis zum 30. November</a> kostenlos.',
         'Do you run a school in Berlin? <a href="bewerbung.html">Apply for free by November 30</a>.'),
])

bkb_sections = [
 ('Bachata-Kurs in Berlin: Das Angebot im Überblick', 'Bachata class in Berlin: the offer at a glance', [
   ('p', 'Wer in Berlin einen Bachata-Kurs sucht, findet Angebote in fast allen Teilen der Stadt: Studios mit eigenem Schwerpunkt auf Bachata, klassische Tanzschulen mit Latin-Programm und Anbieter mit Workshops oder Bootcamps. Die Stadt ist groß, deshalb entscheidet am Ende oft nicht der beste Lehrer, sondern der Kurs, den du wirklich regelmäßig erreichst.',
         'If you are looking for a Bachata class in Berlin, you will find offers in almost every part of the city: studios that focus on Bachata, classic dance schools with a Latin programme and providers with workshops or bootcamps. The city is big, so in the end it is often not the best teacher that decides but the class you can actually reach regularly.'),
   ('p', 'Diese Seite hilft dir, einen Kurs auszuwählen. Eine Übersicht über die Berliner Szene mit Stilen und Partys steht auf <a href="bachata-berlin.html">Bachata Berlin</a>, allgemeine Tipps zur Kurswahl unter <a href="bachata-tanzkurs.html">Bachata Tanzkurs</a>.',
         'This page helps you choose a class. An overview of the Berlin scene with styles and parties is on <a href="bachata-berlin.html">Bachata Berlin</a>, and general tips on choosing a class are on <a href="bachata-tanzkurs.html">Bachata dance course</a>.'),
 ]),
 ('Bachata-Kurse in Berlin: Anbieter von A bis Z', 'Bachata classes in Berlin: providers from A to Z', [
   ('p', 'Die Liste ist alphabetisch und keine Wertung, das offizielle Ranking erscheint am 20. Dezember 2026. Die Angaben beruhen auf den Websites der Anbieter (Stand Oktober 2026). Kurszeiten, Preise und Gruppen ändern sich, bitte prüfe sie direkt dort.',
         'The list is alphabetical and not a rating, the official ranking is published on December 20, 2026. The details are based on the providers’ own websites (as of October 2026). Class times, prices and groups change, so please check them there.'),
   _berlin_cards(), _BERLIN_APPLY,
 ]),
 ('Kursformate: Wochenkurs, Drop-in, Workshop und Bootcamp', 'Class formats: weekly class, drop-in, workshop and bootcamp', [
   ('ul', [
     ('<strong>Wochenkurs:</strong> Jede Woche derselbe Termin mit derselben Gruppe. Das ist der beste Weg, wenn du den Grundschritt sicher lernen willst, siehe <a href="bachata-grundschritt.html">Bachata Grundschritt</a>.', '<strong>Weekly class:</strong> the same slot every week with the same group. This is the best way if you want to learn the basic step securely, see <a href="bachata-grundschritt.html">Bachata basic step</a>.'),
     ('<strong>Drop-in:</strong> Du buchst einzelne Stunden. Das passt, wenn dein Kalender wechselt. La Mambita nennt auf der Website Drop-in und akzeptiert Urban Sports Club.', '<strong>Drop-in:</strong> you book single classes. This suits a changing calendar. La Mambita lists drop-in on its website and accepts Urban Sports Club.'),
     ('<strong>Workshop:</strong> Ein Thema an einem Termin, etwa Drehungen oder Styling. Mehr dazu unter <a href="bachata-workshop.html">Bachata Workshop</a>.', '<strong>Workshop:</strong> one topic on one date, such as turns or styling. More on <a href="bachata-workshop.html">Bachata workshop</a>.'),
     ('<strong>Bootcamp:</strong> Intensive Einheiten über mehrere Stunden. Zapatissimo nennt Bootcamp-Angebote auf der Seite zu den Bachata-Kursen in Berlin.', '<strong>Bootcamp:</strong> intensive sessions over several hours. Zapatissimo lists bootcamp formats on its page for Bachata classes in Berlin.'),
   ]),
 ]),
 ('Welches Level und welcher Stil passt zu dir?', 'Which level and which style suit you?', [
   ('p', 'Starte als Einsteiger im ersten Level, auch wenn du schon anderes getanzt hast. Der Bachata-Grundschritt mit dem Tap auf Zählzeit vier ist die Basis für alles Weitere, und Einsteigerkurse sind der leichteste Weg, die Musik zu verstehen. Mehr dazu auf <a href="bachata-fuer-anfaenger.html">Bachata für Anfänger</a>.',
         'Start in the first level as a beginner, even if you have danced other things. The Bachata basic step with the tap on count four is the base for everything else, and beginner classes are the easiest way to understand the music. More on <a href="bachata-fuer-anfaenger.html">Bachata for beginners</a>.'),
   ('p', 'Beim Stil gilt: Moderna ist leicht zugänglich, Sensual bringt Körperarbeit und enge Verbindung, Dominicana mehr Fußarbeit und Spiel mit dem Rhythmus. Die Unterschiede erklären <a href="bachata-moderna.html">Bachata Moderna</a>, <a href="bachata-sensual.html">Bachata Sensual</a> und <a href="bachata-dominicana.html">Bachata Dominicana</a>.',
         'On style: Moderna is easy to get into, Sensual brings body work and a close connection, Dominicana more footwork and play with the rhythm. The differences are explained on <a href="bachata-moderna.html">Bachata Moderna</a>, <a href="bachata-sensual.html">Bachata Sensual</a> and <a href="bachata-dominicana.html">Bachata Dominicana</a>.'),
 ]),
 ('Lage und Anfahrt: Kurs in deinem Kiez wählen', 'Location and commute: choose a class in your neighbourhood', [
   ('p', 'In Berlin sind Wege lang, und ein Kurs, den du nur nach einer Stunde Fahrt erreichst, fällt schnell aus. Prüfe deshalb vor der Anmeldung die Anbindung. La Mambita liegt zum Beispiel in Schöneberg und ist laut eigener Website gut mit S-Bahn und U-Bahn erreichbar, BachatAcademy hat sein Studio in Friedrichshain.',
         'In Berlin distances are long, and a class that takes an hour to reach is quickly skipped. So check the connections before you sign up. La Mambita, for example, is in Schöneberg and, according to its own website, easy to reach by S-Bahn and U-Bahn, while BachatAcademy has its studio in Friedrichshain.'),
 ]),
 ('Fragen, die du vor der Anmeldung stellen solltest', 'Questions to ask before you sign up', [
   ('ul', [
     ('Gibt es eine Probestunde und was kostet sie?', 'Is there a trial class and what does it cost?'),
     ('Wechseln die Partner im Kurs, und muss ich jemanden mitbringen?', 'Do partners rotate in class, and do I have to bring someone?'),
     ('Wie groß sind die Gruppen und wie viele Levels gibt es?', 'How big are the groups and how many levels are there?'),
     ('Wie lange läuft ein Block und wie kann ich kündigen oder pausieren?', 'How long does a block run and how can I cancel or pause?'),
     ('Gibt es Socials oder Übungsabende, auf denen ich das Gelernte anwende?', 'Are there socials or practice nights where I can use what I have learnt?'),
   ]),
   ('p', 'Preise nennen wir bewusst nicht, weil sie sich ändern. Vergleiche am besten zwei oder drei Preislisten. Zu den Partys in der Stadt siehe <a href="bachata-party-berlin.html">Bachata Party Berlin</a>.',
         'We deliberately do not quote prices because they change. It is best to compare two or three price lists. For parties in the city see <a href="bachata-party-berlin.html">Bachata party Berlin</a>.'),
 ]),
 _BERLIN_SCORE,
]
bkb_faq = [
 ('Wo finde ich einen Bachata-Kurs in Berlin?', 'Where do I find a Bachata class in Berlin?',
  'Bei Studios und Tanzschulen in der ganzen Stadt, zum Beispiel BachatAcademy in Friedrichshain und La Mambita in Schöneberg. Oben steht eine alphabetische Liste mit Links.',
  'At studios and dance schools across the city, for example BachatAcademy in Friedrichshain and La Mambita in Schöneberg. An alphabetical list with links is above.'),
 ('Gibt es Bachata-Kurse für Anfänger in Berlin?', 'Are there Bachata classes for beginners in Berlin?',
  'Ja, die meisten Anbieter haben Einsteigerlevels. La Mambita nennt auf der Website vier Levels nacheinander am Dienstag, vom Einstieg bis zur Fortgeschrittenen-Stufe.',
  'Yes, most providers have beginner levels. La Mambita lists four levels back to back on Tuesdays on its website, from beginner to advanced.'),
 ('Gibt es eine kostenlose Probestunde in Berlin?', 'Is there a free trial class in Berlin?',
  'BachatAcademy nennt auf der Website eine kostenlose, unverbindliche Probestunde. Bei anderen Anbietern prüfe die Website, Angebote ändern sich.',
  'BachatAcademy lists a free, no-obligation trial class on its website. For other providers check the website, as offers change.'),
 ('Brauche ich einen Partner für einen Bachata-Kurs?', 'Do I need a partner for a Bachata class?',
  'In der Regel nicht. Bei BachatAcademy wechseln die Partner laut Website regelmäßig. Frag bei anderen Schulen vorher nach.',
  'Usually not. At BachatAcademy partners rotate regularly according to the website. Ask other schools beforehand.'),
 ('Kann ich mit Urban Sports Club Bachata tanzen?', 'Can I dance Bachata with Urban Sports Club?',
  'La Mambita nennt auf der Website, dass Urban Sports Club akzeptiert wird. Ob andere Anbieter teilnehmen, steht auf deren Websites.',
  'La Mambita states on its website that Urban Sports Club is accepted. Whether other providers take part is on their websites.'),
 ('Wann erscheint das Ranking der Bachata-Schulen in Berlin?', 'When is the ranking of Bachata schools in Berlin published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html#berlin">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html#berlin">ranking page</a>.'),
]
guide_page('bachata-kurs-berlin', 'bkb',
  'Bachata Kurs Berlin: Anbieter, Formate und Tipps',
  'Bachata Kurs Berlin finden: Anbieter von A bis Z, Kursformate wie Drop-in und Bootcamp, Level, Stil, Anfahrt und Fragen vor der Anmeldung. Mit Links zu Schulen.',
  'Bachata class Berlin: providers, formats and tips',
  'Find a Bachata class in Berlin: providers from A to Z, class formats such as drop-in and bootcamp, level, style, commute and questions before signing up. With links to schools.',
  'Bachata Kurs Berlin', ('Bachata Kurs Berlin · Ratgeber', 'Bachata class Berlin · Guide'),
  ('Bachata Kurs Berlin: <em class="foil">Anbieter</em> und Tipps', 'Bachata class Berlin: <em class="foil">providers</em> and tips'),
  ('Bachata Kurs Berlin finden: Anbieter von A bis Z, Kursformate, Level und Stil, Anfahrt und die Fragen, die du vor der Anmeldung stellen solltest.',
   'Find a Bachata class in Berlin: providers from A to Z, class formats, level and style, commute and the questions to ask before you sign up.'),
  [('check', 'Für <b>Einsteiger</b> ohne Partner', 'For <b>beginners</b> without a partner'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  bkb_sections, bkb_faq, ranking_anchor='berlin', sibling_group='city')

btb_sections = [
 ('Bachata Tanzschule Berlin: Was dich erwartet', 'Bachata dance school Berlin: what to expect', [
   ('p', 'Eine Bachata Tanzschule in Berlin kann ein spezialisiertes Bachata-Studio sein oder eine klassische Tanzschule, die Bachata neben Salsa und anderen Tänzen anbietet. Beides hat Vorteile: Spezialisierte Studios bieten oft mehr Levels und Stile, Tanzschulen mit breitem Programm haben meist feste Strukturen und mehrere Tanzarten unter einem Dach.',
         'A Bachata dance school in Berlin can be a specialised Bachata studio or a classic dance school that offers Bachata alongside Salsa and other dances. Both have advantages: specialised studios often offer more levels and styles, while schools with a broad programme usually have fixed structures and several dances under one roof.'),
   ('p', 'Diese Seite hilft dir bei der Auswahl. Allgemeine Kriterien stehen auf <a href="bachata-tanzschule.html">Bachata Tanzschule</a>, die Übersicht der Stadt auf <a href="bachata-berlin.html">Bachata Berlin</a>.',
         'This page helps you choose. General criteria are on <a href="bachata-tanzschule.html">Bachata dance school</a>, and the overview of the city is on <a href="bachata-berlin.html">Bachata Berlin</a>.'),
 ]),
 ('Tanzschulen in Berlin mit Bachata im Programm', 'Dance schools in Berlin with Bachata in their programme', [
   ('p', 'Die Liste ist alphabetisch und keine Wertung, das offizielle Ranking erscheint am 20. Dezember 2026. Die Angaben beruhen auf den Websites der Schulen (Stand Oktober 2026), bitte prüfe Angebote und Preise direkt dort.',
         'The list is alphabetical and not a rating, the official ranking is published on December 20, 2026. The details are based on the schools’ own websites (as of October 2026), so please check offers and prices there.'),
   _berlin_cards(), _BERLIN_APPLY,
 ]),
 ('Woran du eine gute Tanzschule erkennst', 'How to recognise a good dance school', [
   ('ul', [
     ('<strong>Transparente Infos:</strong> Kurszeiten, Level und Probestunde stehen klar auf der Website.', '<strong>Transparent information:</strong> class times, levels and trial class are clearly on the website.'),
     ('<strong>Lehrer:</strong> Die Website nennt, wer unterrichtet. BachatAcademy führt zum Beispiel zwölf Lehrer namentlich auf.', '<strong>Teachers:</strong> the website says who teaches. BachatAcademy, for example, lists twelve teachers.'),
     ('<strong>Einsteigerangebot:</strong> Ein eigener Anfängerkurs mit wechselnden Partnern macht den Einstieg leicht.', '<strong>Beginner offer:</strong> a dedicated beginner class with rotating partners makes starting easy.'),
     ('<strong>Events:</strong> Socials und Übungsabende helfen, das Gelernte anzuwenden.', '<strong>Events:</strong> socials and practice nights help you use what you have learnt.'),
     ('<strong>Flexibilität:</strong> Drop-in oder Urban Sports Club können sinnvoll sein, wenn dein Alltag wechselt.', '<strong>Flexibility:</strong> drop-in or Urban Sports Club can make sense if your daily routine changes.'),
   ]),
 ]),
 ('Tanzschule oder Studio: Der Unterschied im Alltag', 'Dance school or studio: the difference in practice', [
   ('p', 'Eine große Tanzschule bietet meist mehrere Tanzarten, feste Kursblöcke und Räume für Feiern. Ein Studio mit Bachata-Schwerpunkt, wie La Mambita mit Sensual und Moderna, geht tiefer in die Stile und lässt oft mehr Raum für Einzelstunden. Welche Form besser ist, hängt von dir ab: Willst du nur Bachata lernen oder auch Salsa und andere Tänze? Den Unterschied der beiden Tänze erklärt <a href="bachata-salsa-unterschied.html">Salsa und Bachata</a>.',
         'A large dance school usually offers several dances, fixed class blocks and rooms for celebrations. A studio with a Bachata focus, such as La Mambita with Sensual and Moderna, goes deeper into the styles and often leaves more room for single classes. Which form is better depends on you: do you only want to learn Bachata or also Salsa and other dances? The difference between the two dances is explained on <a href="bachata-salsa-unterschied.html">Salsa and Bachata</a>.'),
 ]),
 ('Probestunde und Einstieg', 'Trial class and getting started', [
   ('p', 'Nutze eine Probestunde, bevor du dich bindest. Achte darauf, ob dir die Gruppe, der Lehrer und der Raum zusagen. BachatAcademy nennt auf der Website eine kostenlose, unverbindliche Probestunde, ohne dass du Erfahrung oder Partner brauchst. Wie du Kurse in deiner Nähe findest, steht unter <a href="bachata-kurs-in-der-naehe.html">Bachata Kurs in der Nähe</a>, konkrete Berliner Kurse unter <a href="bachata-kurs-berlin.html">Bachata Kurs Berlin</a>.',
         'Use a trial class before you commit. Check whether you like the group, the teacher and the room. BachatAcademy lists a free, no-obligation trial class on its website, with no experience or partner needed. How to find classes near you is on <a href="bachata-kurs-in-der-naehe.html">Bachata class near you</a>, and specific Berlin classes on <a href="bachata-kurs-berlin.html">Bachata class Berlin</a>.'),
 ]),
 _BERLIN_SCORE,
]
btb_faq = [
 ('Welche Tanzschulen in Berlin bieten Bachata an?', 'Which dance schools in Berlin offer Bachata?',
  'Zum Beispiel BachatAcademy, Cumbancha, HAVANNA Berlin, La Mambita, Traumtänzer und Zapatissimo. Die Liste oben ist alphabetisch und keine Wertung.',
  'For example BachatAcademy, Cumbancha, HAVANNA Berlin, La Mambita, Traumtänzer and Zapatissimo. The list above is alphabetical and not a rating.'),
 ('Was ist die beste Bachata Tanzschule in Berlin?', 'What is the best Bachata dance school in Berlin?',
  'Das hängt von Level, Stil und Lage ab. Ein Ranking nach neun öffentlichen Kriterien erscheint am 20. Dezember 2026 auf der <a href="rankings.html#berlin">Ranking-Seite</a>.',
  'That depends on level, style and location. A ranking based on nine public factors is published on December 20, 2026 on the <a href="rankings.html#berlin">ranking page</a>.'),
 ('Gibt es eine kostenlose Probestunde?', 'Is there a free trial class?',
  'BachatAcademy nennt auf der Website eine kostenlose, unverbindliche Probestunde. Bei anderen Schulen prüfe die Website.',
  'BachatAcademy lists a free, no-obligation trial class on its website. For other schools check the website.'),
 ('Brauche ich Vorkenntnisse?', 'Do I need previous experience?',
  'Nein, die meisten Schulen bieten Einsteigerkurse. Bei BachatAcademy brauchst du laut Website weder Erfahrung noch Partner.',
  'No, most schools offer beginner classes. At BachatAcademy you need neither experience nor a partner according to the website.'),
 ('Was kostet eine Tanzschule in Berlin?', 'What does a dance school in Berlin cost?',
  'Das legt jede Schule selbst fest und es ändert sich. Wir nennen bewusst keine Zahlen, die aktuellen Preise stehen auf den Websites.',
  'Each school sets this itself and it changes. We deliberately give no figures, current prices are on the websites.'),
 ('Wann erscheint das Ranking der Bachata-Schulen in Berlin?', 'When is the ranking of Bachata schools in Berlin published?',
  'Am 20. Dezember 2026 um 19 Uhr auf der <a href="rankings.html#berlin">Ranking-Seite</a>.',
  'On December 20, 2026 at 7 pm (CET) on the <a href="rankings.html#berlin">ranking page</a>.'),
]
guide_page('bachata-tanzschule-berlin', 'btb',
  'Bachata Tanzschule Berlin: Auswahl und Vergleich',
  'Bachata Tanzschule Berlin: Schulen von A bis Z, woran du eine gute Tanzschule erkennst, Studio oder Tanzschule und die Probestunde. Mit Links zu den Websites.',
  'Bachata dance school Berlin: choosing and comparing',
  'Bachata dance school in Berlin: schools from A to Z, how to recognise a good school, studio or dance school and the trial class. With links to the websites.',
  'Bachata Tanzschule Berlin', ('Bachata Tanzschule Berlin · Ratgeber', 'Bachata dance school Berlin · Guide'),
  ('Bachata Tanzschule Berlin: <em class="foil">Auswahl</em> und Vergleich', 'Bachata dance school Berlin: <em class="foil">choosing</em> and comparing'),
  ('Bachata Tanzschule Berlin finden: Schulen von A bis Z, Kriterien für eine gute Schule, Studio oder Tanzschule und der Einstieg mit Probestunde.',
   'Find a Bachata dance school in Berlin: schools from A to Z, criteria for a good school, studio or dance school and getting started with a trial class.'),
  [('check', 'Für <b>Einsteiger</b> ohne Partner', 'For <b>beginners</b> without a partner'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  btb_sections, btb_faq, ranking_anchor='berlin', sibling_group='city')

# ---- Basics pages (Nov 2026): Was ist Bachata, Salsa tanzen ----
_WP_B = '<a href="https://en.wikipedia.org/wiki/Bachata_(dance)" rel="noopener nofollow" target="_blank">Wikipedia</a>'
_WP_S = '<a href="https://en.wikipedia.org/wiki/Salsa_dance" rel="noopener nofollow" target="_blank">Wikipedia</a>'
_SVH = '<a href="https://www.salsavida.com/de/articles/history-of-bachata-dance-music/" rel="noopener nofollow" target="_blank">Salsa Vida</a>'
_CONV = '<a href="https://theconversation.com/how-bachata-rose-from-dominican-republics-brothels-and-shantytowns-to-become-a-global-sensation-260886" rel="noopener nofollow" target="_blank">The Conversation</a>'
_SVS = '<a href="https://www.salsavida.com/de/salsa-dance/" rel="noopener nofollow" target="_blank">Salsa Vida</a>'

was_sections = [
 ('Was ist Bachata?', 'What is Bachata?', [
   ('p', 'Bachata ist zugleich eine Musikrichtung und ein Paartanz aus der Dominikanischen Republik. Die Musik wird von Gitarren getragen, der Tanz wird zu zweit getanzt und besteht im Kern aus einem einfachen Grundschritt mit vier Zählzeiten. Heute wird Bachata in vielen Ländern getanzt, auch in Deutschland, wo es Kurse, Partys und Festivals gibt.',
         'Bachata is both a style of music and a partner dance from the Dominican Republic. The music is carried by guitars, the dance is done in pairs and at its core is a simple basic step with four counts. Today Bachata is danced in many countries, including Germany, where there are classes, parties and festivals.'),
   ('p', 'Auf dieser Seite findest du einen Überblick: Wo Bachata herkommt, wie sich Musik und Tanz entwickelt haben, welche Stile es gibt und wie du als Einsteiger anfängst. Zu jedem Punkt führen wir dich zu den ausführlichen Ratgebern.',
         'This page gives an overview: where Bachata comes from, how the music and the dance developed, which styles exist and how you get started as a beginner. For each point we link you to the detailed guides.'),
 ]),
 ('Woher kommt Bachata?', 'Where does Bachata come from?', [
   ('p', f'Nach {_WP_B} entstand der Tanz in der Dominikanischen Republik in den 1960er-Jahren. Die Musik begann als romantische Gitarrenmusik in der Tradition des Bolero und war zunächst weniger Tanzmusik. Später nahm sie Elemente des Merengue auf, das Tempo stieg und Bachata wurde zunehmend zum Tanzen gespielt.',
         f'According to {_WP_B}, the dance was created in the Dominican Republic in the 1960s. The music began as romantic guitar music in the tradition of the bolero and was at first less dance music. Later it took on elements of merengue, the tempo rose and Bachata was increasingly played for dancing.'),
   ('p', 'In den 1970er- und 1980er-Jahren galt Bachata als Musik der unteren Schichten und lief kaum im Radio. Um 1990 änderte sich das, vor allem durch Juan Luis Guerra, der 1992 mit „Bachata Rosa“ einen Grammy gewann. 2019 nahm die UNESCO „Music and dance of Dominican Bachata“ in die Liste des immateriellen Kulturerbes der Menschheit auf. Mehr zur Musik steht im Ratgeber <a href="bachata-musik.html">Bachata Musik</a>.',
         'In the 1970s and 1980s Bachata was regarded as music of the lower classes and hardly played on the radio. Around 1990 that changed, above all through Juan Luis Guerra, who won a Grammy in 1992 with “Bachata Rosa”. In 2019 UNESCO added “Music and dance of Dominican Bachata” to the Representative List of the Intangible Cultural Heritage of Humanity. More on the music is in the guide <a href="bachata-musik.html">Bachata music</a>.'),
 ]),
 ('Die Anfänge: Ein Wort für „Fest“ und die erste Aufnahme', 'The beginnings: a word for “party” and the first recording', [
   ('p', f'Bevor „Bachata“ eine Musikrichtung bezeichnete, stand das Wort nach {_SVH} meist für ein Fest oder eine zwanglose Zusammenkunft. Als erste Bachata-Aufnahmen gelten Lieder von José Manuel Calderón aus dem Jahr 1962. Die Musik entstand auf dem Land und in den Armenvierteln von Santo Domingo und wurde stark von Bolero und Son geprägt, später auch vom Merengue.',
         f'Before “bachata” named a style of music, the word usually stood for a party or an informal gathering, according to {_SVH}. Songs by José Manuel Calderón from 1962 are regarded as the first Bachata recordings. The music grew up in the countryside and in the shantytowns of Santo Domingo and was strongly shaped by bolero and son, later also by merengue.'),
   ('p', f'Der Radiosender Radio Guarachita, geleitet von Radhamés Aracena, spielte diese Musik fast ausschließlich und trug laut {_CONV} und {_SVH} entscheidend zu ihrer Verbreitung bei.',
         f'The radio station Radio Guarachita, run by Radhamés Aracena, played this music almost exclusively and, according to {_CONV} and {_SVH}, contributed decisively to its spread.'),
 ]),
 ('Stigma und „música de amargue“', 'Stigma and “música de amargue”', [
   ('p', f'Bachata war lange die Musik der armen, ländlichen Migranten. Die städtische Mittel- und Oberschicht sah auf sie herab, und laut {_CONV} wurde sie mit Bordellen und dem Leben der Unterschicht verbunden. Merengue hatte in der dominikanischen Kultur ein deutlich höheres Ansehen.',
         f'Bachata was long the music of poor, rural migrants. The urban middle and upper class looked down on it and, according to {_CONV}, it was associated with brothels and lower-class life. Merengue had a much higher standing in Dominican culture.'),
   ('p', 'Mitte der 1980er-Jahre prägten die Künstler Luis Segura und Leonardo Paniagua den Begriff „música de amargue“, die Musik der romantischen Bitterkeit. Er beschreibt die oft wehmütigen, von Liebeskummer geprägten Texte und wurde zu einem festen Gefühl der Bachata, ähnlich dem Blues.',
         'In the mid-1980s the artists Luis Segura and Leonardo Paniagua coined the term “música de amargue”, music of romantic bitterness. It describes the often wistful lyrics full of heartbreak and became a lasting feeling of Bachata, similar to the blues.'),
 ]),
 ('Eine kurze Zeitleiste der Bachata', 'A short timeline of Bachata', [
   ('ul', [
     ('<strong>1962:</strong> Erste Aufnahmen, die als Bachata gelten (José Manuel Calderón).', '<strong>1962:</strong> first recordings regarded as Bachata (José Manuel Calderón).'),
     ('<strong>1960er-Jahre:</strong> Radio Guarachita bringt die Gitarrenmusik zu einem breiteren Publikum.', '<strong>1960s:</strong> Radio Guarachita brings the guitar music to a wider audience.'),
     ('<strong>Mitte der 1980er:</strong> Der Begriff „música de amargue“ entsteht.', '<strong>Mid-1980s:</strong> the term “música de amargue” is coined.'),
     ('<strong>1990:</strong> Juan Luis Guerras Album „Bachata Rosa“ macht die Musik romantischer und bringt sie zu einem internationalen Publikum. 1992 folgt der Grammy.', '<strong>1990:</strong> Juan Luis Guerra’s album “Bachata Rosa” makes the music more romantic and brings it to an international audience. The Grammy follows in 1992.'),
     ('<strong>2002:</strong> Aventura aus der Bronx hat mit „Obsesión“ einen internationalen Hit, 2004 steht das Lied in Deutschland auf Platz 1 der Charts.', '<strong>2002:</strong> Aventura from the Bronx have an international hit with “Obsesión”, in 2004 the song is number 1 in the German charts.'),
     ('<strong>2000er:</strong> Lehrer außerhalb der Dominikanischen Republik entwickeln Bachata Moderna und Bachata Sensual.', '<strong>2000s:</strong> teachers outside the Dominican Republic develop Bachata Moderna and Bachata Sensual.'),
     ('<strong>2019:</strong> Die UNESCO nimmt Musik und Tanz der dominikanischen Bachata in die Liste des immateriellen Kulturerbes auf.', '<strong>2019:</strong> UNESCO adds the music and dance of Dominican Bachata to the list of intangible cultural heritage.'),
   ]),
 ]),
 ('So entwickelte sich der Tanz', 'How the dance developed', [
   ('p', f'Der Tanz entstand laut {_SVH} sozial auf Partys, in Bars und bei Familienfeiern, nicht im Tanzstudio. Er stützte sich vor allem auf den Paartanz des Bolero. Auf Salsa-Festivals und Kongressen wurde Bachata in den 1990er- und 2000er-Jahren oft wie Merengue oder Cumbia behandelt, als Gesellschaftstanz neben dem Hauptprogramm.',
         f'According to {_SVH}, the dance grew socially at parties, in bars and at family celebrations, not in the dance studio. It drew mostly on the couple dancing of the bolero. At Salsa festivals and congresses in the 1990s and 2000s Bachata was often treated like merengue or cumbia, as a social dance alongside the main programme.'),
   ('p', 'Als Lehrer außerhalb der Dominikanischen Republik begannen, Bachata systematisch zu unterrichten, kamen Drehungen und Partnerarbeit aus dem Salsa hinzu: Bachata Moderna. In Spanien entwickelten Korke und Judith in Cádiz Bachata Sensual, mit Körperwellen, Isolationen und einem weicheren Look, der laut Salsa Vida zum Teil vom Zouk beeinflusst ist. Seit den frühen 2010er-Jahren gibt es Bachata-Kategorien bei großen Tanzwettbewerben.',
         'When teachers outside the Dominican Republic began to teach Bachata systematically, turns and partner work from Salsa were added: Bachata Moderna. In Spain Korke and Judith developed Bachata Sensual in Cádiz, with body waves, isolations and a softer look which, according to Salsa Vida, is partly influenced by zouk. Since the early 2010s there have been Bachata categories at major dance competitions.'),
 ]),
 ('Wie sieht der Tanz aus?', 'What does the dance look like?', [
   ('p', f'Der ursprüngliche Tanz wurde laut {_WP_B} in geschlossener Haltung getanzt, ähnlich wie der Bolero, oft in enger Umarmung. Der Grundschritt bewegt sich in einem kleinen Quadrat. Heute wird oft zu schnellerer Musik getanzt, mit mehr Fußarbeit, einfachen Drehungen und einem Wechsel zwischen geschlossener und offener Haltung.',
         f'According to {_WP_B}, the original dance was done in closed position, similar to the bolero, often in a close embrace. The basic step moves within a small square. Today people often dance to faster music, with more footwork, simple turns and a change between closed and open position.'),
   ('p', 'Der Grundschritt besteht aus drei Schritten in eine Richtung und einem Tap auf Zählzeit vier, danach geht es in die Gegenrichtung. Wie das genau aussieht, steht auf der Seite <a href="bachata-grundschritt.html">Bachata Grundschritt</a>.',
         'The basic step consists of three steps in one direction and a tap on count four, then you go back in the other direction. Exactly how that looks is on the page <a href="bachata-grundschritt.html">Bachata basic step</a>.'),
 ]),
 ('Die Stile der Bachata', 'The styles of Bachata', [
   ('ul', [
     ('<strong>Bachata Dominicana:</strong> Der ursprüngliche Stil aus der Dominikanischen Republik mit lebendigem Fußwerk. Siehe <a href="bachata-dominicana.html">Bachata Dominicana</a>.', '<strong>Bachata Dominicana:</strong> the original style from the Dominican Republic with lively footwork. See <a href="bachata-dominicana.html">Bachata Dominicana</a>.'),
     (f'<strong>Bachata Moderna:</strong> Laut {_WP_B} vor allem in New York von der Diaspora und von Salsa-Tänzern entwickelt, mit mehr Drehungen und Figuren. Siehe <a href="bachata-moderna.html">Bachata Moderna</a>.', f'<strong>Bachata Moderna:</strong> according to {_WP_B} developed especially in New York by the diaspora and by salsa dancers, with more turns and figures. See <a href="bachata-moderna.html">Bachata Moderna</a>.'),
     ('<strong>Bachata Sensual:</strong> In Spanien entstanden, verbunden mit Korke Escalona und Judith Cordero, mit enger Verbindung und weicher Körperbewegung. Siehe <a href="bachata-sensual.html">Bachata Sensual</a>.', '<strong>Bachata Sensual:</strong> created in Spain, associated with Korke Escalona and Judith Cordero, with a close connection and soft body movement. See <a href="bachata-sensual.html">Bachata Sensual</a>.'),
   ]),
   ('p', 'Welcher Stil zu dir passt, hängt vom Geschmack ab. Einsteiger lernen meist erst den Grundschritt und entscheiden später, welchen Stil sie vertiefen.',
         'Which style suits you depends on taste. Beginners usually learn the basic step first and decide later which style to deepen.'),
 ]),
 ('Bachata in Deutschland', 'Bachata in Germany', [
   ('p', 'In Deutschland wurde Bachata durch Lieder wie „Obsesión“ von Aventura bekannt, das im September 2004 Platz 1 der Media-Control-Singlecharts erreichte. Inzwischen gibt es in vielen Städten Kurse, regelmäßige Partys und Festivals. Termine findest du unter <a href="bachata-socials.html">Bachata-Socials</a> und <a href="bachata-festivals-deutschland.html">Bachata-Festivals</a>.',
         'In Germany Bachata became known through songs such as “Obsesión” by Aventura, which reached number 1 in the Media Control singles chart in September 2004. Meanwhile there are classes, regular parties and festivals in many cities. You will find dates under <a href="bachata-socials.html">Bachata socials</a> and <a href="bachata-festivals-deutschland.html">Bachata festivals</a>.'),
 ]),
 ('Bachata und Salsa: Was ist der Unterschied?', 'Bachata and Salsa: what is the difference?', [
   ('p', 'Beide Tänze kommen aus der Karibik, haben aber verschiedene Wurzeln, Musik und Schritte. Bachata ist ein 4er-Rhythmus mit Gitarre, Salsa lebt von Percussion und Bläsern. Alle Unterschiede im Überblick stehen im Ratgeber <a href="bachata-salsa-unterschied.html">Salsa und Bachata</a>, die Grundlagen zu Salsa auf der Seite <a href="salsa-tanzen.html">Salsa tanzen</a>.',
         'Both dances come from the Caribbean, but have different roots, music and steps. Bachata is a four-count rhythm with guitar, Salsa lives on percussion and brass. All differences at a glance are in the guide <a href="bachata-salsa-unterschied.html">Salsa and Bachata</a>, the basics of Salsa on the page <a href="salsa-tanzen.html">Dancing Salsa</a>.'),
 ]),
 ('Bachata lernen: So fängst du an', 'Learning Bachata: how to start', [
   ('ul', [
     ('<strong>Grundschritt üben:</strong> Er ist leicht und die Basis für alles. Siehe <a href="bachata-grundschritt.html">Bachata Grundschritt</a>.', '<strong>Practise the basic step:</strong> it is easy and the base for everything. See <a href="bachata-grundschritt.html">Bachata basic step</a>.'),
     ('<strong>Einen Kurs finden:</strong> Siehe <a href="bachata-kurs-in-der-naehe.html">Bachata Kurs in der Nähe</a> und <a href="bachata-fuer-anfaenger.html">Bachata für Anfänger</a>.', '<strong>Find a class:</strong> see <a href="bachata-kurs-in-der-naehe.html">Bachata class near you</a> and <a href="bachata-fuer-anfaenger.html">Bachata for beginners</a>.'),
     ('<strong>Zur Party gehen:</strong> Tanzen lernt man beim Tanzen. Tipps unter <a href="bachata-party.html">Bachata Party</a>.', '<strong>Go to a party:</strong> you learn dancing by dancing. Tips on <a href="bachata-party.html">Bachata party</a>.'),
   ]),
   ('p', 'Einen vollständigen Einstieg gibt der Ratgeber <a href="bachata-tanzen.html">Bachata tanzen lernen</a>.',
         'A complete introduction is in the guide <a href="bachata-tanzen.html">Learn to dance Bachata</a>.'),
 ]),
 _closing('Wer Bachata in der eigenen Stadt lernen will, findet dort die Schulen.', 'If you want to learn Bachata in your own city, you will find the schools there.'),
]
was_faq = [
 ('Was ist Bachata?', 'What is Bachata?',
  'Bachata ist eine Musikrichtung und ein Paartanz aus der Dominikanischen Republik. Die Musik wird von Gitarren getragen, der Grundschritt hat vier Zählzeiten.',
  'Bachata is a style of music and a partner dance from the Dominican Republic. The music is carried by guitars and the basic step has four counts.'),
 ('Woher kommt Bachata?', 'Where does Bachata come from?',
  'Aus der Dominikanischen Republik. Nach Wikipedia entstand der Tanz in den 1960er-Jahren.',
  'From the Dominican Republic. According to Wikipedia the dance was created in the 1960s.'),
 ('Was bedeutet das Wort Bachata?', 'What does the word Bachata mean?',
  'Ursprünglich bezeichnete es meist ein Fest oder eine zwanglose Zusammenkunft. Später wurde es zum Namen der Musikrichtung.',
  'Originally it usually meant a party or an informal gathering. Later it became the name of the style of music.'),
 ('Wann entstand Bachata?', 'When did Bachata begin?',
  'Als erste Bachata-Aufnahmen gelten Lieder von 1962. Der Tanz entwickelte sich in den folgenden Jahrzehnten auf Partys und im Familienkreis.',
  'Songs from 1962 are regarded as the first Bachata recordings. The dance developed in the following decades at parties and in family circles.'),
 ('Wer machte Bachata international bekannt?', 'Who made Bachata known internationally?',
  'Juan Luis Guerra mit „Bachata Rosa“ (1990) und später Aventura mit „Obsesión“, dazu Romeo Santos als Solokünstler.',
  'Juan Luis Guerra with “Bachata Rosa” (1990) and later Aventura with “Obsesión”, plus Romeo Santos as a solo artist.'),
 ('Welche Bachata-Stile gibt es?', 'Which Bachata styles are there?',
  'Die drei bekanntesten sind Dominicana, Moderna und Sensual. Dazu kommen Mischformen.',
  'The three best known are Dominicana, Moderna and Sensual. There are also fusion forms.'),
 ('Ist Bachata schwer zu lernen?', 'Is Bachata hard to learn?',
  'Der Grundschritt ist leicht. Wie schnell du vorankommst, hängt von deiner Übung ab. Ein Anfängerkurs ist ein guter Start.',
  'The basic step is easy. How fast you progress depends on your practice. A beginner class is a good start.'),
 ('Was ist der Unterschied zwischen Bachata und Salsa?', 'What is the difference between Bachata and Salsa?',
  'Andere Wurzeln, andere Musik, anderer Grundschritt. Details im Ratgeber <a href="bachata-salsa-unterschied.html">Salsa und Bachata</a>.',
  'Different roots, different music, different basic step. Details in the guide <a href="bachata-salsa-unterschied.html">Salsa and Bachata</a>.'),
 _rank_faq,
]
guide_page('bachata-was-ist-das', 'bwi',
  'Was ist Bachata? Herkunft, Geschichte und Stile',
  'Was ist Bachata? Herkunft aus der Dominikanischen Republik, Geschichte von Musik und Tanz, die Stile Dominicana, Moderna und Sensual und wie du anfängst.',
  'What is Bachata? Origin, history and styles',
  'What is Bachata? Origin in the Dominican Republic, history of the music and the dance, the styles Dominicana, Moderna and Sensual and how to start.',
  'Was ist Bachata', ('Was ist Bachata · Ratgeber', 'What is Bachata · Guide'),
  ('Was ist Bachata? <em class="foil">Herkunft</em>, Geschichte, Stile', 'What is Bachata? <em class="foil">Origin</em>, history, styles'),
  ('Bachata ist Musik und Paartanz aus der Dominikanischen Republik. Hier erfährst du, woher sie kommt, wie sie sich entwickelt hat und welche Stile es gibt.',
   'Bachata is music and a partner dance from the Dominican Republic. Here you learn where it comes from, how it developed and which styles exist.'),
  [('check', 'Für <b>Einsteiger</b> und Neugierige', 'For <b>beginners</b> and the curious'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  was_sections, was_faq, sibling_group='topic')

sal_sections = [
 ('Was ist Salsa?', 'What is Salsa?', [
   ('p', 'Salsa ist ein Paartanz und eine Musikrichtung mit Wurzeln in der Karibik. Getanzt wird zu schneller, rhythmisch dichter Musik, meist mit Percussion und Bläsern. Der Tanz ist in vielen Ländern verbreitet, auch in Deutschland, wo viele Tanzschulen Salsa-Kurse anbieten. Auf Latin Dance Awards steht Salsa neben Bachata, weil viele Tänzer beide lernen.',
         'Salsa is a partner dance and a style of music with roots in the Caribbean. It is danced to fast, rhythmically dense music, usually with percussion and brass. The dance is widespread in many countries, including Germany, where many dance schools offer Salsa classes. On Latin Dance Awards Salsa sits next to Bachata because many dancers learn both.'),
 ]),
 ('Woher kommt Salsa?', 'Where does Salsa come from?', [
   ('p', f'Nach {_WP_S} hat sich Salsa aus afro-kubanischen und karibischen Gesellschaftstänzen entwickelt, darunter Son cubano, Danzón, Mambo, Cha-Cha-Chá und Rumba. Der Begriff „Salsa“ wurde in den 1960er- und 1970er-Jahren in New York als Bezeichnung für die dort entstandene afro-karibische Tanzmusik bekannt. Als Förderer nennt Wikipedia unter anderem Johnny Pacheco, Fania Records und die Fania All-Stars.',
         f'According to {_WP_S}, Salsa developed from Afro-Cuban and Caribbean social dances, including son cubano, danzón, mambo, cha-cha-chá and rumba. The term “salsa” became known in New York in the 1960s and 1970s as a label for the Afro-Caribbean dance music created there. Wikipedia names Johnny Pacheco, Fania Records and the Fania All-Stars among its promoters.'),
   ('p', 'Nach Deutschland kam Salsa Anfang der 1980er-Jahre. Salsa ist damit die ältere Tanzfamilie, Bachata als eigener Tanz die jüngere. Den Vergleich findest du im Ratgeber <a href="bachata-salsa-unterschied.html">Salsa und Bachata</a>.',
         'Salsa came to Germany in the early 1980s. Salsa is thus the older dance family, Bachata as its own dance the younger one. You will find the comparison in the guide <a href="bachata-salsa-unterschied.html">Salsa and Bachata</a>.'),
 ]),
 ('Eine kurze Zeitleiste der Salsa', 'A short timeline of Salsa', [
   ('ul', [
     ('<strong>Ab 1892:</strong> Der Son cubano entwickelt sich im Osten Kubas und erreicht Santiago de Cuba.', '<strong>From 1892:</strong> the son cubano develops in eastern Cuba and reaches Santiago de Cuba.'),
     ('<strong>1947:</strong> Der Mambo kommt nach New York, der Palladium Ballroom wird zum wichtigen Ort für Mambo-Tänzer.', '<strong>1947:</strong> the mambo arrives in New York and the Palladium Ballroom becomes an important venue for mambo dancers.'),
     ('<strong>1964:</strong> Fania Records wird in New York gegründet und macht „Salsa“ zum Oberbegriff für diese Musik.', '<strong>1964:</strong> Fania Records is founded in New York and makes “salsa” the umbrella term for this music.'),
     ('<strong>1973:</strong> Die Fania All Stars spielen im Yankee Stadium und bringen Salsa in den Mainstream.', '<strong>1973:</strong> the Fania All Stars play Yankee Stadium and bring Salsa into the mainstream.'),
     ('<strong>1980er:</strong> Der New-York-Stil wird systematisiert, Eddie Torres verbreitet das Tanzen „on 2“.', '<strong>1980s:</strong> the New York style is systematised, Eddie Torres spreads dancing “on 2”.'),
     ('<strong>1990er:</strong> Der Los-Angeles-Stil (On 1), geprägt von den Vazquez Brothers, verbreitet sich weltweit.', '<strong>1990s:</strong> the Los Angeles style (On 1), shaped by the Vazquez Brothers, spreads worldwide.'),
     ('<strong>1997:</strong> In Puerto Rico findet der erste Salsa-Kongress statt, mehrtägig mit Workshops und Partys.', '<strong>1997:</strong> the first Salsa congress takes place in Puerto Rico, lasting several days with workshops and parties.'),
   ]),
   ('p', f'Die Daten stützen sich auf {_SVS} und {_WP_S}. In der Fachliteratur gibt es teils abweichende Angaben, die Zeitleiste ist deshalb eine grobe Orientierung.',
         f'The dates are based on {_SVS} and {_WP_S}. The literature sometimes gives differing figures, so the timeline is a rough guide.'),
 ]),
 ('Die wichtigsten Salsa-Stile', 'The main Salsa styles', [
   ('ul', [
     (f'<strong>Kubanisch (Casino):</strong> Ein Kreistanz, bei dem die Tanzenden umeinander herum tanzen. Laut {_WP_S} geht der Name auf die „Casinos Deportivos“ zurück. Aus Havanna stammt auch Rueda de Casino aus den 1950er-Jahren.', f'<strong>Cuban (Casino):</strong> a circular dance in which the dancers move around each other. According to {_WP_S} the name goes back to the “Casinos Deportivos”. Rueda de Casino, from the 1950s, also comes from Havana.'),
     ('<strong>Los Angeles (On 1):</strong> Linear, auf einer „Linie“ getanzt, mit dem Break auf der ersten Zählzeit.', '<strong>Los Angeles (On 1):</strong> linear, danced on a “slot”, with the break on the first beat.'),
     ('<strong>New York (On 2):</strong> Ebenfalls linear, aber auf der zweiten Zählzeit getanzt, mit starkem Gewicht auf Solo-Passagen („Shines“).', '<strong>New York (On 2):</strong> also linear, but danced on the second beat, with strong emphasis on solo passages (“shines”).'),
     ('<strong>Kolumbianisch (Cali):</strong> Ein Kreisstil mit schneller Fußarbeit. Cali gilt als „Hauptstadt der Salsa“.', '<strong>Colombian (Cali):</strong> a circular style with fast footwork. Cali is known as the “capital of salsa”.'),
     ('<strong>Casino Rueda:</strong> Ein Gruppentanz, bei dem mehrere Paare im Kreis tanzen und Figuren angesagt werden. Er wurde in den 1950er-Jahren in Havanna entwickelt.', '<strong>Casino Rueda:</strong> a group dance in which several couples dance in a circle and figures are called. It was developed in Havana in the 1950s.'),
     ('<strong>Salsa Choke:</strong> Ein kolumbianischer Stil, der solo oder in der Gruppe getanzt wird.', '<strong>Salsa Choke:</strong> a Colombian style danced solo or in a group.'),
   ]),
   ('p', 'In vielen Tanzschulen wird ein Stil unterrichtet, den die Schule auf ihrer Website nennt. Frage vor der Anmeldung, welcher Stil im Kurs gelehrt wird.',
         'Many dance schools teach one style, which the school names on its website. Ask which style the class teaches before you sign up.'),
 ]),
 ('Der Grundschritt: Drei Schritte auf vier Zählzeiten', 'The basic step: three steps on four beats', [
   ('p', f'Das Grundmuster ist laut {_WP_S} drei Schritte auf vier Zählzeiten. Auf die vierte Zählzeit fällt beim Tanzen die Pause, das Muster läuft über acht Zählzeiten. Das Tempo liegt nach Wikipedia meist zwischen 160 und 220 Schlägen pro Minute. Bachata dagegen hat einen Grundschritt über vier Zählzeiten mit einem Tap auf der vierten, siehe <a href="bachata-grundschritt.html">Bachata Grundschritt</a>.',
         f'According to {_WP_S}, the basic pattern is three steps on four beats. The pause falls on the fourth beat when dancing and the pattern runs over eight counts. According to Wikipedia the tempo is mostly between 160 and 220 beats per minute. Bachata, on the other hand, has a basic step over four counts with a tap on the fourth, see <a href="bachata-grundschritt.html">Bachata basic step</a>.'),
 ]),
 ('Salsa oder Bachata zuerst lernen?', 'Learn Salsa or Bachata first?', [
   ('p', 'Beides geht. Salsa hat mehr Figuren und ein schnelleres Tempo. Bachata hat einen einfachen Grundschritt und ein ruhigeres Tempo. Wer zuerst Bachata lernt, hat meist einen leichteren Einstieg in den Paartanz, wer mit Salsa beginnt, lernt früh viel Drehtechnik. Es gibt hier kein Richtig und Falsch. Eine ausführliche Gegenüberstellung steht im Ratgeber <a href="bachata-salsa-unterschied.html">Salsa und Bachata</a>.',
         'Both work. Salsa has more figures and a faster tempo. Bachata has a simple basic step and a calmer tempo. If you learn Bachata first you usually have an easier start into partner dancing, if you start with Salsa you learn a lot of turn technique early. There is no right and wrong here. A detailed comparison is in the guide <a href="bachata-salsa-unterschied.html">Salsa and Bachata</a>.'),
 ]),
 ('Zählen: On 1 und On 2', 'Counting: On 1 and On 2', [
   ('p', f'Salsa wird im 4/4-Takt in Achterphrasen gezählt: 1–2–3, Pause, 5–6–7, Pause. Getreten wird auf 1, 2, 3, 5, 6 und 7, die Zählzeiten 4 und 8 bleiben leer. Nach {_SVS} liegt der Unterschied zwischen On 1 und On 2 darin, wo der Break fällt: bei On 1 auf den Zählzeiten 1 und 5, bei On 2 auf 2 und 6.',
         f'Salsa is counted in eight-beat phrases in 4/4 time: 1–2–3, pause, 5–6–7, pause. You step on 1, 2, 3, 5, 6 and 7, counts 4 and 8 stay empty. According to {_SVS} the difference between On 1 and On 2 is where the break falls: on counts 1 and 5 for On 1, on 2 and 6 for On 2.'),
   ('p', 'Als Zeitgeber helfen die Clave und der Tumbao der Conga. Wer sie erst einmal heraushört, findet den Takt auch in schnellen Stücken.',
         'The clave and the conga tumbao help as timing anchors. Once you can pick them out, you find the beat even in fast pieces.'),
 ]),
 ('Technik und Partnerarbeit für den Anfang', 'Technique and partner work for the start', [
   ('ul', [
     ('<strong>Haltung:</strong> Nach Salsa Vida helfen ein leicht nach vorn geneigter Oberkörper, lockere Knie und das Gewicht auf den Fußballen.', '<strong>Posture:</strong> according to Salsa Vida a slightly forward-leaning upper body, relaxed knees and weight on the balls of the feet help.'),
     ('<strong>Arme:</strong> Sie schwingen natürlich mit und müssen nicht gesetzt werden.', '<strong>Arms:</strong> they swing naturally and do not have to be posed.'),
     ('<strong>Partnerarbeit:</strong> Am Anfang stehen offene und geschlossene Haltung, der Cross-Body-Lead und einfache Drehungen.', '<strong>Partner work:</strong> at the start come open and closed position, the cross-body lead and simple turns.'),
     ('<strong>Tempo drosseln:</strong> Beim Üben hilft es, Lieder zu verlangsamen, bis die Schritte sitzen.', '<strong>Slow it down:</strong> when practising it helps to slow songs down until the steps are secure.'),
   ]),
   ('p', 'Die Grundlagen lernst du in wenigen Stunden, bis zur Sicherheit dauert es deutlich länger. Ein Anfängerkurs gibt dir dafür eine Struktur.',
         'You can learn the basics in a few hours, but it takes considerably longer to become secure. A beginner class gives you a structure for that.'),
 ]),
 ('Salsa lernen: So fängst du an', 'Learning Salsa: how to start', [
   ('ul', [
     ('<strong>Stil wählen:</strong> Kubanisch, On 1, On 2 oder Cali. Frage bei der Schule nach.', '<strong>Choose a style:</strong> Cuban, On 1, On 2 or Cali. Ask the school.'),
     ('<strong>Anfängerkurs besuchen:</strong> Ein Grundkurs lehrt Grundschritt, Zählen und erste Drehungen. Wie du einen Kurs findest, steht unter <a href="bachata-kurs-in-der-naehe.html">Bachata Kurs in der Nähe</a>, das Vorgehen gilt ähnlich für Salsa.', '<strong>Attend a beginner class:</strong> a basic class teaches the basic step, counting and first turns. How to find a class is described under <a href="bachata-kurs-in-der-naehe.html">Bachata class near you</a>, the procedure is similar for Salsa.'),
     ('<strong>Musik hören:</strong> Wer den Rhythmus kennt, tanzt entspannter. Zum Vergleich hilft <a href="bachata-musik.html">Bachata Musik</a>.', '<strong>Listen to the music:</strong> if you know the rhythm you dance more relaxed. For comparison, <a href="bachata-musik.html">Bachata music</a> helps.'),
   ]),
 ]),
 _closing('Viele Schulen unterrichten neben Bachata auch Salsa, das steht bei den Schulen selbst.', 'Many schools teach Salsa in addition to Bachata, which is stated on the schools’ own sites.'),
]
sal_faq = [
 ('Was ist Salsa?', 'What is Salsa?',
  'Ein Paartanz und eine Musikrichtung mit Wurzeln in der Karibik, getanzt zu schneller Musik mit Percussion und Bläsern.',
  'A partner dance and a style of music with roots in the Caribbean, danced to fast music with percussion and brass.'),
 ('Woher kommt Salsa?', 'Where does Salsa come from?',
  'Salsa entwickelte sich aus afro-kubanischen und karibischen Tänzen. Der Begriff wurde in den 1960er- und 1970er-Jahren in New York bekannt.',
  'Salsa developed from Afro-Cuban and Caribbean dances. The term became known in New York in the 1960s and 1970s.'),
 ('Was sind die wichtigsten Salsa-Stile?', 'What are the main Salsa styles?',
  'Kubanisch (Casino), Los Angeles (On 1), New York (On 2) und Kolumbianisch (Cali).',
  'Cuban (Casino), Los Angeles (On 1), New York (On 2) and Colombian (Cali).'),
 ('Was ist der Unterschied zwischen On 1 und On 2?', 'What is the difference between On 1 and On 2?',
  'Es geht darum, wo der Break fällt: bei On 1 auf den Zählzeiten 1 und 5, bei On 2 auf 2 und 6.',
  'It is about where the break falls: on counts 1 and 5 for On 1, on 2 and 6 for On 2.'),
 ('Wie zählt man Salsa?', 'How do you count Salsa?',
  'In Achterphrasen: 1–2–3, Pause, 5–6–7, Pause. Getreten wird auf 1, 2, 3, 5, 6 und 7.',
  'In eight-beat phrases: 1–2–3, pause, 5–6–7, pause. You step on 1, 2, 3, 5, 6 and 7.'),
 ('Ist Salsa schwerer als Bachata?', 'Is Salsa harder than Bachata?',
  'Das ist Ansichtssache. Salsa hat mehr Figuren und ein schnelleres Tempo, Bachata einen einfacheren Grundschritt.',
  'That is a matter of opinion. Salsa has more figures and a faster tempo, Bachata a simpler basic step.'),
 ('Kann ich Salsa und Bachata zusammen lernen?', 'Can I learn Salsa and Bachata together?',
  'Ja, viele Tänzer lernen beide. Frage deine Schule nach Kursen für beide Tänze.',
  'Yes, many dancers learn both. Ask your school about classes for both dances.'),
 _rank_faq,
]
guide_page('salsa-tanzen', 'sal',
  'Salsa tanzen: Herkunft, Stile und Einstieg',
  'Salsa tanzen: Was ist Salsa, woher kommt sie, die Stile Kubanisch, On 1, On 2 und Cali, der Grundschritt und wie du anfängst. Mit Vergleich zu Bachata.',
  'Dancing Salsa: origin, styles and how to start',
  'Dancing Salsa: what Salsa is, where it comes from, the Cuban, On 1, On 2 and Cali styles, the basic step and how to start. With a comparison to Bachata.',
  'Salsa tanzen', ('Salsa tanzen · Ratgeber', 'Dancing Salsa · Guide'),
  ('Salsa tanzen: <em class="foil">Herkunft</em>, Stile, Einstieg', 'Dancing Salsa: <em class="foil">origin</em>, styles, how to start'),
  ('Salsa kommt aus der Karibik und wurde in New York zum Begriff. Hier steht, woher sie kommt, welche Stile es gibt und wie du anfängst.',
   'Salsa comes from the Caribbean and became a household term in New York. Here is where it comes from, which styles exist and how to start.'),
  [('check', 'Für <b>Einsteiger</b>', 'For <b>beginners</b>'), ('cal', 'Ranking am <b>20. Dezember</b>', 'Ranking on <b>December 20</b>')],
  sal_sections, sal_faq, sibling_group='topic')

# ======================================================================
# BACHATA KURS WIEN  (support page for /at/bachata-vienna; keyword "bachata kurs wien", 210/mo, SD 8)
# Facts come from the schools' own websites (read 10 Nov 2026) and our Austria data. Nothing is invented.
# ======================================================================
import austria_data as _AT
_wv = [s for s in _AT.SCHOOLS if s[1] == 'vienna']
_wv_top = sorted(_wv, key=lambda s: (-(s[2] or 0), -s[3]))[:4]
_wv_top_de = ', '.join(f'{s[0]} ({f"{s[2]:.1f}".replace(".", ",")} ★, {s[3]} Bewertungen)' for s in _wv_top)
_wv_top_en = ', '.join(f'{s[0]} ({s[2]:.1f} ★, {s[3]} reviews)' for s in _wv_top)
def _wl(u, n): return f'<a href="{u}" rel="noopener" target="_blank">{n}</a>'
wien_sections = [
 ('Bachata Kurse in Wien im Überblick', 'Bachata classes in Vienna at a glance', [
   ('p', f'In unserer Liste stehen {len(_wv)} Schulen und Studios mit Bachata in Wien. Die höchsten Google-Bewertungen haben derzeit {_wv_top_de} (Stand Oktober 2026). Das ist kein Ranking: Die Zahlen sind ein Zwischenstand, das offizielle Ergebnis folgt im Frühjahr 2027.',
         f'Our list has {len(_wv)} schools and studios teaching Bachata in Vienna. The highest Google ratings right now belong to {_wv_top_en} (October 2026). This is not a ranking: the figures are an interim standing, and the official result follows in spring 2027.'),
   ('p', 'Die vollständige Liste mit Punkten und Links zu jeder Schule steht auf der Seite <a href="/at/bachata-vienna">Bachata Vienna: the best dance schools 2027</a> (auf Englisch). Hier geht es darum, wie die Kurse aufgebaut sind, was die Schulen öffentlich zu Level, Preis und Terminen schreiben und was du vor der Anmeldung fragen solltest.',
         'The full list with points and links to every school is on the page <a href="/at/bachata-vienna">Bachata Vienna: the best dance schools 2027</a> (in English). Here we look at how classes are built, what the schools publish about level, price and dates, and what to ask before you sign up.'),
 ]),
 ('Vier Wiener Schulen im Detail', 'Four Viennese schools in detail', [
   ('p', 'Wir haben im November 2026 die Websites mehrerer Schulen gelesen. Das steht dort, so wie es dort steht. Termine ändern sich jedes Semester, bitte bestätige sie bei der Schule.',
         'In November 2026 we read the websites of several schools. This is what they say, as stated. Dates change every term, so please confirm them with the school.'),
   ('h3', _wl('https://www.salsavienna.at/', 'Salsa Vienna') + ' (Wallgasse, 1060 Wien)', _wl('https://www.salsavienna.at/', 'Salsa Vienna') + ' (Wallgasse, 1060 Vienna)'),
   ('ul', [
     ('Die Kurse finden laut Website derzeit im „Günter“ (Restaurant, Bar &amp; more) in der Wallgasse im 6. Bezirk statt.', 'According to its website the courses currently take place at “Günter” (restaurant, bar &amp; more) in Wallgasse in the 6th district.'),
     ('Bachata gibt es in drei Leveln: Bachata 1 ohne Vorkenntnisse, Bachata 2 mit Vorkenntnissen und Bachata 3, das auf beiden aufbaut. Genannt werden Bachata 1 am Dienstag 19:30–20:30 und Bachata 2 am Dienstag 20:30–21:30 (Start 3.11.2026).', 'Bachata is offered at three levels: Bachata 1 without experience, Bachata 2 with experience and Bachata 3, which builds on both. Listed are Bachata 1 on Tuesday 19:30–20:30 and Bachata 2 on Tuesday 20:30–21:30 (start 3 November 2026).'),
     ('Ein Bachata-Kurs besteht aus vier Abenden zu je 60 Minuten, einmal pro Woche am selben Wochentag. Der Preis: 60 € pro Person, mit gültigem Studentenausweis 48 €. Privatstunden gibt es auf Anfrage.', 'A Bachata course is four evenings of 60 minutes, once a week on the same weekday. The price: €60 per person, €48 with a valid student ID. Private lessons are available on request.'),
     ('Ob man für die Bachata-Kurse einen Partner braucht, steht auf der Seite nicht. Beim Kurs „Salsa Cali Paartanz“ ist es ein Paarkurs, „Salsa Cali Footwork“ wird solo getanzt.', 'The page does not say whether a partner is needed for the Bachata courses. “Salsa Cali Paartanz” is a couples course, “Salsa Cali Footwork” is danced solo.'),
   ]),
   ('h3', _wl('https://www.lentodance.at/', 'Lento Dance Studio') + ' (Traungasse 14, 1030 Wien)', _wl('https://www.lentodance.at/', 'Lento Dance Studio') + ' (Traungasse 14, 1030 Vienna)'),
   ('ul', [
     ('Die Website nennt Salsa, Bachata (Sensual und Traditional), Heels und Kizomba und schreibt „all levels welcome (Beginner to Advanced)“ sowie „no dance partner required“.', 'The website lists salsa, Bachata (Sensual and Traditional), heels and kizomba and says “all levels welcome (Beginner to Advanced)” and “no dance partner required”.'),
     ('Anfängerkurse stehen täglich um 18:00 Uhr im Programm. Die Seite mischt allerdings ältere und neuere Beiträge, deshalb lohnt sich eine Nachfrage per E-Mail (info@lentodance.at).', 'Beginner classes are listed every day at 18:00. The page mixes older and newer posts, though, so it is worth asking by email (info@lentodance.at).'),
     ('Bezahlt wird pro Kurs oder mit einem 30-Tage-Pass. Preise für Bachata nennt die Seite nicht; für Kizomba steht 12 € pro Stunde, 8 € für Studierende und 49 € für 30 Tage.', 'You pay per class or with a 30-day pass. The page gives no Bachata prices; for kizomba it says €12 per hour, €8 for students and €49 for 30 days.'),
     ('Mittwochs findet ein Social von 21:00 bis 24:00 Uhr in der Lento Party Hall (Zaunergasse 4) statt. Der Eintritt kostet 7 € und ist im Monatspass enthalten.', 'On Wednesdays there is a social from 21:00 to 24:00 at the Lento Party Hall (Zaunergasse 4). Entry is €7 and included in the monthly pass.'),
   ]),
   ('h3', _wl('https://salsahouse.at/', 'SalsaHouse') + ' (Märzstraße 105, 1150 Wien)', _wl('https://salsahouse.at/', 'SalsaHouse') + ' (Märzstraße 105, 1150 Vienna)'),
   ('ul', [
     ('Neben Bachata unterrichtet SalsaHouse Salsa, Rueda de Casino, Kizomba und Son Moderno. Einsteiger beginnen laut Website in „Basic 1“-Kursen, die regelmäßig wiederholt werden.', 'Besides Bachata, SalsaHouse teaches salsa, Rueda de Casino, kizomba and Son Moderno. According to its website beginners start in “Basic 1” courses, which are repeated regularly.'),
     ('Die weiteren Level heißen Improver, Intermediate, Advanced und Perfecting. Das richtige Level klärt die Schule in einem persönlichen Gespräch. Eigene Bachata-Level nennt die Seite nicht.', 'The further levels are Improver, Intermediate, Advanced and Perfecting. The school settles the right level in a personal conversation. The page does not name separate Bachata levels.'),
     ('Der Wochenplan ist ein Bild, die Preise stehen auf einer eigenen Seite. Wir können hier deshalb keine Zeiten oder Beträge zitieren.', 'The weekly timetable is an image and the prices are on a separate page, so we cannot quote times or amounts here.'),
   ]),
   ('h3', _wl('https://www.tumbao.at/', 'Tumbao Dance Studio') + ' (Margaretenstraße 26, 1040 Wien)', _wl('https://www.tumbao.at/', 'Tumbao Dance Studio') + ' (Margaretenstraße 26, 1040 Vienna)'),
   ('ul', [
     ('Genannt werden Bachata Dominicana, Bachata Sensual und Bachata Lady Styling, dazu viele weitere Stile. Die Kurse sind laut Website für „Anfänger bis Profi“.', 'Listed are Bachata Dominicana, Bachata Sensual and Bachata Lady Styling, plus many other styles. The courses are for “beginners to pros”, according to the website.'),
     ('Kartenpakete (10er- und 50er-Block) lassen sich online kaufen; Preise nennt die Startseite nicht. Der Kursplan steht unter tumbao.at/Tanzkurse, das Studio gibt Montag bis Freitag 17:00–21:00 als Öffnungszeit an.', 'Class packs (10 and 50 classes) can be bought online; the home page gives no prices. The timetable is at tumbao.at/Tanzkurse, and the studio lists Monday to Friday 17:00–21:00 as opening hours.'),
   ]),
 ]),
 ('Preise und Probestunde: Was veröffentlicht ist', 'Prices and trial class: what is published', [
   ('p', 'Nach der Lektüre fällt vor allem auf, was fehlt. Das haben wir gefunden:', 'After reading the sites, what stands out most is what is missing. This is what we found:'),
   ('ul', [
     ('<strong>Salsa Vienna:</strong> 60 € für vier Bachata-Abende (48 € mit Studentenausweis), also 15 € pro Abend (12 € mit Studentenausweis).', '<strong>Salsa Vienna:</strong> €60 for four Bachata evenings (€48 with a student ID), which is €15 per evening (€12 with a student ID).'),
     ('<strong>Lento Dance Studio:</strong> Einzelkurs oder 30-Tage-Pass, Bachata-Preise nicht genannt; Social 7 €.', '<strong>Lento Dance Studio:</strong> single class or 30-day pass, Bachata prices not stated; social €7.'),
     ('<strong>Tumbao:</strong> 10er- und 50er-Block, keine Beträge auf der Startseite.', '<strong>Tumbao:</strong> 10 and 50-class packs, no amounts on the home page.'),
     ('<strong>SalsaHouse:</strong> Preise auf einer separaten Seite.', '<strong>SalsaHouse:</strong> prices on a separate page.'),
   ]),
   ('p', 'Eine Probestunde nennt keine der vier Seiten, die wir gelesen haben. Frag deshalb nach, bevor du einen Block kaufst: Gibt es eine Probestunde, und wird sie angerechnet?', 'None of the four pages we read mentions a trial class. So ask before you buy a pack: is there a trial class, and is it credited?'),
 ]),
 ('Welches Level passt, wenn du bei null beginnst?', 'Which level fits if you start from zero?', [
   ('p', 'Wähle den Einsteigerkurs, auch wenn du schon einen anderen Tanz kannst. Bei Salsa Vienna ist das Bachata 1, bei SalsaHouse „Basic 1“, bei Lento Dance die täglichen Anfängerklassen. Der Grundschritt der Bachata steht auf der Seite <a href="bachata-grundschritt.html">Bachata Grundschritt</a>, einen allgemeinen Einstieg bietet <a href="bachata-fuer-anfaenger.html">Bachata für Anfänger</a>.',
         'Pick the beginner class even if you already know another dance. At Salsa Vienna that is Bachata 1, at SalsaHouse “Basic 1”, at Lento Dance the daily beginner classes. The basic step is explained on <a href="bachata-grundschritt.html">Bachata basic step</a>, and <a href="bachata-fuer-anfaenger.html">Bachata for beginners</a> gives a general introduction.'),
   ('p', 'Einen Partner brauchst du in den meisten Gruppenkursen nicht, weil die Partner wechseln. Lento Dance schreibt das ausdrücklich. Welcher Stil zu dir passt, erklären die Seiten <a href="bachata-sensual.html">Bachata Sensual</a> und <a href="bachata-dominicana.html">Bachata Dominicana</a>; allgemeine Hinweise zur Kurswahl stehen unter <a href="bachata-tanzkurs.html">Bachata Tanzkurs</a>.',
         'You do not need a partner in most group classes because partners rotate. Lento Dance says so explicitly. Which style suits you is explained on <a href="bachata-sensual.html">Bachata Sensual</a> and <a href="bachata-dominicana.html">Bachata Dominicana</a>; general tips on choosing a class are at <a href="bachata-tanzkurs.html">Bachata dance course</a>.'),
 ]),
 ('Was du vor der Anmeldung fragen solltest', 'What to ask before you sign up', [
   ('ul', [
     ('<strong>Welches Level?</strong> Frag, ob es eigene Bachata-Level gibt oder ob Bachata in gemischten Gruppen läuft. Salsa Vienna trennt Bachata 1 bis 3, SalsaHouse nennt keine eigenen Bachata-Level.', '<strong>Which level?</strong> Ask whether there are separate Bachata levels or mixed groups. Salsa Vienna separates Bachata 1 to 3, SalsaHouse does not name separate Bachata levels.'),
     ('<strong>Wie viele Abende?</strong> Ein Kurs bei Salsa Vienna hat vier Abende; bei Kartenpaketen (Tumbao) zählt, wie lange die Karte gültig ist.', '<strong>How many evenings?</strong> A course at Salsa Vienna has four evenings; for class packs (Tumbao) what matters is how long the card is valid.'),
     ('<strong>Wo genau?</strong> Salsa Vienna wechselt den Kursort, andere Schulen haben mehrere Räume. Prüfe Adresse und Bezirk vor dem ersten Abend.', '<strong>Where exactly?</strong> Salsa Vienna changes its venue, other schools have several rooms. Check the address and district before the first evening.'),
     ('<strong>Social danach?</strong> Lento Dance veranstaltet mittwochs ein Social. Wie so ein Abend abläuft, steht bei <a href="bachata-party.html">Bachata Party</a> und <a href="bachata-socials.html">Bachata-Socials</a>.', '<strong>A social afterwards?</strong> Lento Dance holds a social on Wednesdays. What such an evening is like is explained at <a href="bachata-party.html">Bachata party</a> and <a href="bachata-socials.html">Bachata socials</a>.'),
   ]),
 ]),
 ('So haben wir diese Seite erstellt', 'How we prepared this page', [
   ('p', f'Wir haben im November 2026 die Websites von Salsa Vienna, Lento Dance Studio, SalsaHouse und Tumbao Dance Studio gelesen und nutzen die Google-Bewertungen unserer Liste von Oktober 2026. Die übrigen {len(_wv) - 4} Wiener Schulen sind auf der <a href="/at/bachata-vienna">Städteseite</a> verlinkt; ihre Angebote haben wir hier nicht ausgewertet. Preise und Termine ändern sich, bitte prüfe sie direkt bei der Schule. Die Seite ist unabhängig: Plätze lassen sich nicht kaufen.',
         f'In November 2026 we read the websites of Salsa Vienna, Lento Dance Studio, SalsaHouse and Tumbao Dance Studio, and we use the Google ratings from our October 2026 list. The other {len(_wv) - 4} Viennese schools are linked on the <a href="/at/bachata-vienna">city page</a>; we did not evaluate their offers here. Prices and dates change, so please check them with the school. The page is independent: places cannot be bought.'),
 ]),
]
wien_faq = [
 ('Wo kann ich in Wien Bachata lernen?', 'Where can I learn Bachata in Vienna?',
  f'In unserer Liste stehen {len(_wv)} Schulen mit Bachata in Wien, darunter Lento Dance Studio, Salsa Vienna, SalsaHouse und Tumbao Dance Studio. Die vollständige Liste steht auf unserer Seite Bachata Vienna.',
  f'Our list has {len(_wv)} schools with Bachata in Vienna, including Lento Dance Studio, Salsa Vienna, SalsaHouse and Tumbao Dance Studio. The full list is on our Bachata Vienna page.'),
 ('Was kostet ein Bachata Kurs in Wien?', 'How much does a Bachata class in Vienna cost?',
  'Das hängt von der Schule ab, und viele nennen ihre Preise nicht auf der Startseite. Salsa Vienna veröffentlicht 60 € für vier Bachata-Abende zu je 60 Minuten (48 € mit Studentenausweis). Frag bei jeder Schule nach dem Preis und danach, was er enthält.',
  'It depends on the school, and many do not state prices on the home page. Salsa Vienna publishes €60 for four Bachata evenings of 60 minutes (€48 with a student ID). Ask each school for the price and what it includes.'),
 ('Brauche ich einen Partner für einen Bachata Kurs?', 'Do I need a partner for a Bachata class?',
  'Meist nicht. Lento Dance Studio schreibt „no dance partner required“, und in den meisten Gruppen wechseln die Partner. Bei Salsa Vienna ist das für die Bachata-Kurse nicht angegeben; frag vorher nach.',
  'Usually not. Lento Dance Studio writes “no dance partner required”, and in most groups partners rotate. Salsa Vienna does not say for its Bachata courses, so ask beforehand.'),
 ('Gibt es eine kostenlose Probestunde?', 'Is there a free trial class?',
  'Auf den vier Seiten, die wir gelesen haben, steht keine. Das heißt nicht, dass es keine gibt: Schreib die Schule an und frag, ob ein Probetermin möglich ist und ob er angerechnet wird.',
  'None is mentioned on the four pages we read. That does not mean there is none: write to the school and ask whether a trial is possible and credited.'),
 ('Welche ist die beste Bachata Schule in Wien?', 'What is the best Bachata school in Vienna?',
  f'Nach unseren vorläufigen Daten vom Oktober 2026 führen die Google-Bewertungen Lento Dance Studio, Salsa &amp; Latin Studio Julion, Salsa Vienna und Vienna Salsa Studio an (jeweils 5,0 ★). Das ist nicht das Endergebnis, das im Frühjahr 2027 folgt.',
  'By our interim data from October 2026, the Google ratings are led by Lento Dance Studio, Salsa &amp; Latin Studio Julion, Salsa Vienna and Vienna Salsa Studio (5.0 ★ each). This is not the final result, which follows in spring 2027.'),
]
guide_page('bachata-kurs-wien', 'bkw',
  'Bachata Kurs Wien: Schulen, Level und Preise',
  'Bachata Kurs in Wien: Level, Preise und Termine laut Websites von Lento Dance, SalsaHouse, Tumbao und Salsa Vienna und was du vor der Anmeldung fragst.',
  'Bachata class Vienna: schools, levels and prices',
  'Bachata class in Vienna: levels, prices and dates according to the websites of Lento Dance, SalsaHouse, Tumbao and Salsa Vienna, and what to ask before you sign up.',
  'Bachata Kurs Wien', ('Bachata Kurs Wien · Ratgeber', 'Bachata class Vienna · Guide'),
  ('Bachata Kurs Wien: <em class="foil">Schulen</em>, Level und Preise', 'Bachata class Vienna: <em class="foil">schools</em>, levels and prices'),
  ('Was Wiener Schulen zu Level, Preisen und Terminen veröffentlichen und was du vor der Anmeldung fragen solltest. Mit Daten von den Websites der Schulen.',
   'What Viennese schools publish about level, prices and dates, and what to ask before you sign up. Based on the schools’ own websites.'),
  [('check', 'Websites gelesen im <b>November 2026</b>', 'Websites read in <b>November 2026</b>'), ('cal', f'<b>{len(_wv)} Schulen</b> in Wien', f'<b>{len(_wv)} schools</b> in Vienna')],
  wien_sections, wien_faq)

# --- Thin-content tiering: city pages with at most 2 listed schools are mostly template text.
# They stay online and linked from the cities index, but are set to noindex until the 20 Dec ranking gives real data.
_NOINDEX_MAX_SCHOOLS = 2
for _k in {e['city'] for e in B.SCH}:
    if sum(1 for e in B.SCH if e['city'] == _k) <= _NOINDEX_MAX_SCHOOLS:
        _p = os.path.join(ROOT, f'bachata-{_k}.html')
        if os.path.exists(_p):
            _h = open(_p, encoding='utf-8').read()
            _h2 = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex,follow">', _h, count=1)
            if _h2 != _h: open(_p, 'w', encoding='utf-8').write(_h2)
