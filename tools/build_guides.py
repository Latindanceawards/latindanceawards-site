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


# ======================================================================
# Reusable city guide (Hamburg, München, ...)
# ======================================================================
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
