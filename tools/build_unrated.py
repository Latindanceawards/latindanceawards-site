#!/usr/bin/env python3
"""Builds bachata-schools-not-yet-rated.html: schools found by research that have no Google rating yet.
They are listed alphabetically by country and city, NOT scored and NOT ranked. When ratings are collected,
move a school into its country data file (tools/add_<cc>.py) and delete it from the JSON below.
Run after build.py, before clean_urls.py:  python3 tools/build_unrated.py"""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
from build import T, page, crumbs, ROOT

SRC = os.path.join(ROOT, 'tools', 'pending_schools', 'candidates-2026-11-03.json')
DONE = os.path.join(ROOT, 'tools', 'pending_schools', 'imported.json')  # names already moved into the ranking
COUNTRIES = [('fr', 'Frankreich', 'France'), ('es', 'Spanien', 'Spain'), ('it', 'Italien', 'Italy'),
             ('pt', 'Portugal', 'Portugal'), ('bg', 'Bulgarien', 'Bulgaria'), ('ua', 'Ukraine', 'Ukraine')]
LISTING = ('salsavida.com', 'goandance', 'top20.ua', 'helloasso', 'urbansportsclub')

data = json.load(open(SRC, encoding='utf-8'))
done = set(json.load(open(DONE, encoding='utf-8'))) if os.path.exists(DONE) else set()
t = T('nr')
esc = html.escape
secs, total = [], 0
for cc, de, en in COUNTRIES:
    rows = sorted((x for x in data.get(cc, []) if x['name'] not in done), key=lambda x: (x['city_name'].lower(), x['name'].lower()))
    if not rows: continue
    total += len(rows)
    by = {}
    for x in rows: by.setdefault(x['city_name'], []).append(x)
    body = ''
    for city, xs in sorted(by.items(), key=lambda kv: kv[0].lower()):
        lis = ''
        for x in xs:
            lst = any(k in x['url'] for k in LISTING)
            lis += (f'<li><a href="{esc(x["url"])}" rel="nofollow noopener" target="_blank">{esc(x["name"])}</a> '
                    + t('span', '(Quelle: Kursportal)' if lst else '(Website der Schule)', '(source: course listing)' if lst else "(school's website)") + '</li>')
        body += f'<h3>{esc(city)}</h3><ul>{lis}</ul>'
    secs.append((de, en, body))

blocks = ''.join(f'<h2>{t("span", f"{de}", f"{en}")}</h2>{body}' for de, en, body in secs)
intro = (t('p', 'Diese Schulen bieten laut öffentlichen Quellen Bachata-Kurse an. Für sie haben wir noch keine Google-Bewertung erfasst. Deshalb bekommen sie keine Punkte und keinen Platz im Ranking. Die Liste ist alphabetisch nach Land und Stadt und keine Wertung.',
          'According to public sources these schools offer Bachata classes. We have not yet collected a Google rating for them, so they get no points and no place in the ranking. The list is alphabetical by country and city and is not a rating.')
         + t('p', 'Du leitest eine dieser Schulen oder fehlst in der Liste? <a href="bewerbung.html">Bewirb dich kostenlos</a>, dann können wir deine Daten bestätigen und die Schule ins Ranking aufnehmen. Die Methode steht auf der <a href="deutschland.html#method">Startseite</a>.',
              'Do you run one of these schools or are you missing from the list? <a href="bewerbung.html">Apply for free</a> so we can confirm your data and add the school to the ranking. The method is on the <a href="deutschland.html#method">homepage</a>.')
         + t('p', 'Angaben und Links stammen von Kursseiten und Websites der Schulen. Prüfe Termine, Orte und Preise immer direkt beim Anbieter.',
              'Details and links come from course listings and schools\' own websites. Always check dates, locations and prices with the provider.'))
main = f'''
<section class="page-hero" aria-labelledby="nr-title"><div class="wrap"><div>
  <h1 id="nr-title">{t("span", "Bachata-Schulen ohne Bewertung (noch nicht im Ranking)", "Bachata schools not yet rated (not yet in the ranking)")}</h1>
  <p class="lede">{t("span", f"{total} Schulen in Frankreich, Spanien, Italien, Portugal, Bulgarien und der Ukraine. Keine Wertung.", f"{total} schools in France, Spain, Italy, Portugal, Bulgaria and Ukraine. Not a rating.")}</p>
</div></div></section>
<section class="section"><div class="wrap" style="max-width:760px;line-height:1.7">{intro}{blocks}</div></section>
'''
page('bachata-schools-not-yet-rated.html',
     'Bachata-Schulen ohne Bewertung: noch nicht im Ranking',
     f'{total} Bachata-Schulen in Frankreich, Spanien, Italien, Portugal, Bulgarien und der Ukraine, ohne Google-Bewertung und ohne Ranking-Platz. Alphabetisch, keine Wertung.',
     'Bachata schools not yet rated: not yet in the ranking',
     f'{total} Bachata schools in France, Spain, Italy, Portugal, Bulgaria and Ukraine without a Google rating or ranking place. Alphabetical, not a rating.',
     'bachata-schools-not-yet-rated.html', main, t.en, '',
     schema=[crumbs('Bachata schools not yet rated', 'bachata-schools-not-yet-rated.html')])
print('unrated page:', total, 'schools')
