# Builds the keyword landing pages (city guides, topic guides). Run: python3 tools/build_guides.py
# Reuses tools/build.py (head, CSS, header, footer, helpers). Running this also rebuilds the base pages.
import os, sys, urllib.parse
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
              ('bachata-gelsenkirchen', 'Gelsenkirchen', 'Gelsenkirchen'), ('bachata-oldenburg', 'Oldenburg', 'Oldenburg'), ('bachata-kempten', 'Kempten', 'Kempten'), ('bachata-leipzig', 'Leipzig', 'Leipzig')]
TOPIC_PAGES = [('bachata-tanzen', 'Bachata tanzen lernen', 'Learn to dance Bachata'),
               ('bachata-festivals-deutschland', 'Bachata-Festivals 2026/2027', 'Bachata festivals 2026/2027'),
               ('bachata-grundschritt', 'Bachata-Grundschritt', 'Bachata basic step'),
               ('bachata-sensual', 'Bachata Sensual', 'Bachata Sensual'),
               ('bachata-dominicana', 'Bachata Dominicana', 'Bachata Dominicana'),
               ('bachata-tanzkurs', 'Bachata Tanzkurs', 'Bachata dance course'),
               ('bachata-fuer-anfaenger', 'Bachata für Anfänger', 'Bachata for beginners'),
               ('bachata-ladies-styling', 'Bachata Ladies Styling', 'Bachata ladies styling'),
               ('bachata-moderna', 'Bachata Moderna', 'Bachata Moderna'),
               ('bachata-party', 'Bachata Party', 'Bachata party')]

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
                + (f'<a href="{c["url"]}" rel="noopener" target="_blank">{c["name"]} →</a>' if c.get('url') else '') + '</article>'
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
    nl_de = ', '.join(names[:-1]) + ' und ' + names[-1]
    nl_en = ', '.join(names[:-1]) + ' and ' + names[-1]
    intro_de = f'In {cde} haben wir {n} Anbieter mit Bachata-Kursen erfasst: {nl_de}.'
    intro_en = f'In {cen} we have listed {n} providers with Bachata classes: {nl_en}.'
    if top:
        intro_de += f' Die beste Google-Bewertung unter ihnen hat {top[0]["name"]} mit {top[1][0]} Sternen bei {top[1][1]} Bewertungen (Stand Oktober 2026).'
        intro_en += f' The best Google rating among them belongs to {top[0]["name"]} with {top[1][0].replace(",", ".")} stars from {top[1][1]} reviews (as of October 2026).'
    if most and most[0] is not (top[0] if top else None):
        intro_de += f' Die meisten Bewertungen sammelt {most[0]["name"]} mit {most[1][1]}.'
        intro_en += f' {most[0]["name"]} has the most reviews with {most[1][1]}.'
    note = (f'Die Liste umfasst {n} Schulen in {cde}. Weitere Anbieter nehmen wir nach der Bewerbung auf.',
            f'The list covers {n} schools in {cde}. We add further providers after they apply.')
    party = (f'Socials und Übungsabende laufen in {cde} meist über die Schulen selbst, zum Beispiel bei {nl_de}. Die aktuellen Termine stehen auf deren Websites und in den Social-Media-Kanälen. Größere Veranstaltungen findest du zusätzlich in den <a href="{SV}" rel="noopener" target="_blank">Veranstaltungslisten von Salsa Vida</a>.',
             f'Socials and practice nights in {cen} mostly run through the schools themselves, for example at {nl_en}. Current dates are on their websites and social media channels. You can also find larger events in the <a href="{SV}" rel="noopener" target="_blank">Salsa Vida event listings</a>.')
    faq_extra = [
      (f'In {cde} listen wir {n} Anbieter mit Bachata-Kursen: {nl_de}. Die Auswahl bildet den Stand vom Oktober 2026 ab. Das Ranking mit Punkten erscheint am 20. Dezember 2026.',
       f'In {cen} we list {n} providers with Bachata classes: {nl_en}. The selection reflects the state in October 2026. The ranking with scores is published on December 20, 2026.'),
      ('Das entscheidet jede Schule selbst. Frag vor der Anmeldung nach einer Probestunde oder einem Einsteigertermin, die Kontaktdaten stehen auf der jeweiligen Website.',
       'Each school decides this itself. Ask for a trial class or a beginner date before you sign up; the contact details are on each school\'s website.'),
      (f'Frag bei den Schulen in {cde} nach Socials und Übungsabenden und schau in die Veranstaltungslisten von Salsa Vida. Dort stehen auch Festivals in der Region.',
       f'Ask the schools in {cen} about socials and practice nights, and check the Salsa Vida event listings, which also include festivals in the region.'),
    ]
    slug = 'bachata-' + key
    city_guide(slug, f'cg{idx}', cde, cen, key, (intro_de, intro_en), cards, note, party, faq_extra)
    return slug, cde, cen

AUTO_CITIES = [k for k, c in sorted(((k, sum(1 for e in B.SCH if e['city'] == k)) for k in {e['city'] for e in B.SCH}), key=lambda x: -x[1]) if c >= 3 and k not in ('berlin', 'hamburg', 'muenchen')]
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
