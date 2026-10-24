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
              ('bachata-frankfurt', 'Frankfurt', 'Frankfurt'), ('bachata-duesseldorf', 'Düsseldorf', 'Düsseldorf')]
TOPIC_PAGES = [('bachata-tanzen', 'Bachata tanzen lernen', 'Learn to dance Bachata'),
               ('bachata-festivals-deutschland', 'Bachata-Festivals 2026/2027', 'Bachata festivals 2026/2027'),
               ('bachata-grundschritt', 'Bachata-Grundschritt', 'Bachata basic step'),
               ('bachata-sensual', 'Bachata Sensual', 'Bachata Sensual'),
               ('bachata-dominicana', 'Bachata Dominicana', 'Bachata Dominicana')]

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
    return '\n'.join(out)

def guide_page(slug, pref, title_de, desc_de, title_en, desc_en, crumb, edition, h1, lede, facts, sections, faq,
               ranking_anchor=None, sibling_group=None):
    t = T(pref)
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
