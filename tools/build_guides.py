# Builds the keyword landing pages (city guides, topic guides). Run: python3 tools/build_guides.py
# Reuses tools/build.py (head, CSS, header, footer, helpers). Running this also rebuilds the base pages.
import os, sys
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
              ('bachata-gelsenkirchen', 'Gelsenkirchen', 'Gelsenkirchen'), ('bachata-oldenburg', 'Oldenburg', 'Oldenburg'), ('bachata-kempten', 'Kempten', 'Kempten')]
TOPIC_PAGES = [('bachata-tanzen', 'Bachata tanzen lernen', 'Learn to dance Bachata'),
               ('bachata-festivals-deutschland', 'Bachata-Festivals 2026/2027', 'Bachata festivals 2026/2027'),
               ('bachata-grundschritt', 'Bachata-Grundschritt', 'Bachata basic step'),
               ('bachata-sensual', 'Bachata Sensual', 'Bachata Sensual'),
               ('bachata-dominicana', 'Bachata Dominicana', 'Bachata Dominicana')]

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
    return '\n'.join(out)

from events_data import EVENTS, CITY_LABEL
EV_BY_CITY = {}
for _e in EVENTS: EV_BY_CITY.setdefault(_e['city'], []).append(_e)

def ev_cards(t, evs, h='h3'):
    out = []
    for e in evs:
        links = ''
        if e['site']: links += f'<a href="{e["site"]}" rel="noopener nofollow" target="_blank">{t("span", "Veranstalter", "Organiser")}</a> '
        links += f'<a href="{e["src"]}" rel="noopener nofollow" target="_blank">{t("span", "Quelle", "Source")}</a>'
        price = f' ({e["price"]})' if e['price'] else ''
        out.append(f'<article data-city="{e["city"]}">{t(h, e["name"], e["name"])}'
                   f'<p>{e["venue"]}, {e["addr"]}</p>'
                   f'{t("p", e["rec"][0] + ". " + e["time"][0] + ".", e["rec"][1] + ". " + e["time"][1] + ".")}'
                   f'<span class="meta">{e["price"] or "&nbsp;"}</span><div class="evl">{links}</div></article>')
    return '<div class="cards two evc">' + ''.join(out) + '</div>'

def ev_block(t, key):
    evs = EV_BY_CITY.get(key, [])
    if not evs: return ''
    note = t('p', 'Regelmäßige Socials mit Bachata, nach Stand Oktober 2026 aus öffentlichen Listen und den Seiten der Veranstalter. Zeiten und Preise ändern sich, bitte prüfe sie vor dem Besuch. Dein Social fehlt? <a href="bachata-socials.html#eintragen">Trag es kostenlos ein</a>.',
               'Regular socials with Bachata, as of October 2026, from public listings and the organisers\' pages. Times and prices change, so please check before you go. Is your social missing? <a href="bachata-socials.html#eintragen">List it for free</a>.')
    return ev_cards(t, evs) + '\n    ' + note


def guide_page(slug, pref, title_de, desc_de, title_en, desc_en, crumb, edition, h1, lede, facts, sections, faq,
               ranking_anchor=None, sibling_group=None):
    t = T(pref)
    if ranking_anchor in EV_BY_CITY:
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
    {t("p", 'Alle Städte, Stile und Festivals im Überblick. Die vollständige Methode steht auf der <a href="index.html#method">Startseite</a>, die Bewerbung für Schulen auf der <a href="bewerbung.html">Bewerbungsseite</a>.', 'All cities, styles and festivals at a glance. The full method is on the <a href="index.html#method">homepage</a>, and schools can enter on the <a href="bewerbung.html">application page</a>.')}
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
        _ev_secs += f'<section class="evcity" data-city="{_k}" id="{_k}">{_te("h2", "Bachata-Socials in " + _de, "Bachata socials in " + _en, "class=\"evh\"")}{ev_cards(_te, EV_BY_CITY[_k])}<p class="muted" style="margin-top:12px">{_g}</p></section>'
_ev_cityopts = ''.join(f'<option value="{k}">{CITY_LABEL[k][0]}</option>' for k in CITY_LABEL if k in EV_BY_CITY)
_ev_n = len(EVENTS)
_emain = f"""<section class="page-hero"><div class="wrap" style="grid-template-columns:1fr"><div>
  {_te("h1", "Bachata-Socials in Deutschland", "Bachata socials in Germany")}
  {_te("p", "Regelmäßige Bachata-Partys und Übungsabende nach Stadt, mit Ort, Zeit und Preis. Du veranstaltest einen Social? Trag ihn kostenlos ein.", "Regular Bachata parties and practice nights by city, with place, time and price. Do you run a social? List it for free.", 'class="lede"')}
  <div class="ctas"><a class="btn btn-gold" href="#eintragen">{_te("span", "Social eintragen", "List a social")}</a></div>
</div></div></section>
<section class="block"><div class="wrap tp evw">
  <label style="max-width:320px">{_te("span", "Stadt", "City")}<select id="evsel"><option value="">{_te("span", "Alle Städte", "All cities")}</option>{_ev_cityopts}</select></label>
  <p class="muted" style="margin-top:12px">{_te("span", f"{_ev_n} Socials in fünf Städten, Stand Oktober 2026. Die Angaben stammen aus öffentlichen Veranstaltungslisten und von den Seiten der Veranstalter. Zeiten und Preise ändern sich, bitte prüfe sie vor dem Besuch. Weitere Städte folgen, sobald Veranstalter ihre Socials eintragen.", f"{_ev_n} socials in five cities, as of October 2026. Details come from public event listings and the organisers' own pages. Times and prices change, so please check before you go. More cities follow as organisers list their socials.")}</p>
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
