# Builds the Netherlands section (/nl/) in Dutch + English. Same structure and the same 100-point scoring as build_pl.py.
# Run after build.py/build_guides.py:  python3 tools/build_uk.py
import os, sys, re, io, json, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import uk_data as P
import rank_variant as RV
BASE = '/uk/schools/'
FULL = {e['name']: RV.total(e) for es in RV.polish_entries(P, BASE).values() for e in es}
from build import T, page, crumbs, faq_schema, ICON, ROOT
os.makedirs(os.path.join(ROOT, 'uk'), exist_ok=True)

def f1(x): return f'{x:.1f}'.replace('.', ',')
def f1en(x): return f'{x:.1f}'
ranked = sorted(P.SCHOOLS, key=lambda s: (-FULL[s[0]], s[0]))
_TOP = [FULL[ranked[0][0]]]
def by_city(k): return [s for s in ranked if s[1] == k]

# ---------- Portuguese header / footer ----------
_UKH = B.HEADER
_UKH = _UKH.replace('<a class="brand" href="index.html"', '<a class="brand" href="/"', 1)
_UKH = re.sub(r'<ul id="mnav">.*?</ul>', '''<ul id="mnav">
        <li><a href="uk/#ranking" data-i18n="sn1">Ranking</a></li>
        <li><a href="uk/#cities" data-i18n="sn2">Cities</a></li>
        <li><a href="uk/#metodo" data-i18n="sn3">Method</a></li>
        <li><a href="index.html" data-i18n="sn4">Europe</a></li>
        <li><a href="deutschland.html" data-i18n="sn5">Germany</a></li>
      </ul>''', _UKH, count=1, flags=re.S)
_UKH = _UKH.replace('data-lang="de" aria-pressed="true">DE<', 'data-lang="de" aria-pressed="true">UK<')
_UKH = re.sub(r'<a class="btn btn-gold" href="bewerbung.html" data-i18n="t5">.*?</a>', '<a class="btn btn-gold" href="bewerbung.html?lang=en" data-i18n="sn6">Enter a school</a>', _UKH, count=1)
_brand = re.search(r'<a class="brand" href="index.html">.*?</a>', B.FOOTER, re.S).group(0).replace('href="index.html"', 'href="/"', 1)
_UKF = f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        {_brand}
        <p class="indep" data-i18n="sf1">An independent project celebrating Europe’s Latin dance schools. Rankings are based on public data and are not for sale.</p>
      </div>
      <div>
        <p class="fh" data-i18n="sf2">Rankings</p>
        <ul><li><a href="uk/#ranking" data-i18n="sf3">UK 2027</a></li><li><a href="uk/#metodo" data-i18n="sf4">How we rank</a></li>{''.join(f'<li><a href="uk/bachata-{k}.html">Bachata {v[0]}</a></li>' for k, v in list(P.CITIES.items())[:4])}<li><a href="index.html" data-i18n="sn4">Europa</a></li></ul>
      </div>
      <div>
        <p class="fh" data-i18n="sf5">Contact</p>
        <ul><li><a href="bewerbung.html?lang=en" data-i18n="sn6">Enter a school</a></li><li><a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a></li><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li></ul>
      </div>
    </div>
    <div class="legal"><span>© 2026 Latin Dance Awards</span><span data-i18n="sf6">Bachata Edition · United Kingdom</span></div>
  </div>
</footer>'''

SHARED_ES_EN = {'sn1': 'Ranking', 'sn2': 'Cities', 'sn3': 'Method', 'sn4': 'Europe', 'sn5': 'Germany', 'sn6': 'Enter a school', 'sn7': 'Poland', 'sn8': 'Spain', 'sn9': 'Italy', 'sn10': 'Portugal', 'sn11': 'France', 'sn12': 'Netherlands',
  'sf1': "An independent project celebrating Europe's Latin dance schools. Rankings are based on public data and can't be bought.",
  'sf2': 'Rankings', 'sf3': 'UK 2027', 'sf4': 'How we score', 'sf5': 'Contact', 'sf6': 'Bachata Edition · United Kingdom'}

def uk_page(fname, canon, title, desc, title_en, desc_en, main, en, schema, js=''):
    oh, of = B.HEADER, B.FOOTER
    B.HEADER, B.FOOTER = _UKH, _UKF
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            B.SHARED_EN = dict(B.SHARED_EN); B.SHARED_EN.update(SHARED_ES_EN)
            page(fname, title, desc, title_en, desc_en, canon, main, en, js, schema=schema)
    finally:
        B.HEADER, B.FOOTER = oh, of
    fp = os.path.join(ROOT, fname); h = open(fp, encoding='utf-8').read()
    h = h.replace('<html lang="de">', '<html lang="en-GB">', 1).replace('hreflang="de"', 'hreflang="en-GB"').replace('document.documentElement.lang=l;', 'document.documentElement.lang=(l==="en"?"en":"en-GB");')
    h = h.replace('og:locale" content="de_DE"', 'og:locale" content="uk_UK"')
    open(fp, 'w', encoding='utf-8').write(h)
    print('wrote', fname)

def school_list(ss, t, start=1):
    lis = []
    for i, s in enumerate(ss, start):
        lis.append(f'<li><b>{i}</b><a href="{s[4]}" rel="nofollow noopener" target="_blank">{s[0]}</a><span>{f1(FULL[s[0]])} pts · {f1(s[2])} ★ ({s[3]})</span></li>')
    return '<ol class="top">' + ''.join(lis) + '</ol>'

def hero(t, edition, h1, lede, facts, ctas, seal='badge-bachata-uk-2027.svg', alt='Bachata Awards UK 2027 seal'):
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
    return '<section class="block alt" id="faq"><div class="wrap"><div class="sec-head">' + t("h2", 'Frequently asked questions', 'Frequently asked questions') + '</div><div class="faq">' + ''.join(f'<details>{t("summary", q, qe)}{t("p", a, ae)}</details>' for q, qe, a, ae in faq) + '</div></div></section>'

N = len(P.SCHOOLS); NC = len(P.CITIES)
METHOD_ES = ('We score schools the same way as in Germany, on nine criteria and 100 points: years teaching, beginner offer, events, Google rating, number of reviews and social media (75 points in total), plus festivals, recent reviews and competitions (25 points, currently "to be confirmed"). Data comes from school websites, Google Maps and Instagram. Anything we cannot confirm counts at the lowest value, and a school can fill it in by applying.',
             'We score schools exactly as in Germany, on nine factors and 100 points: years active, beginner offer, events, Google rating, number of reviews and social media (75 points together), plus festivals, recent reviews and competitions (25 points, still “to be confirmed”). The data comes from the schools’ websites, Google Maps and Instagram. Anything we cannot confirm counts at the lowest level, and a school can complete it in its application.')

# ---------- /uk/ index ----------
t = T('uk')
city_cards = ''.join(
    f'<article><h3>{t("span", "Bachata " + v[0], "Bachata " + v[1])}</h3>{t("p", f"{len(by_city(k))} schools, led by {by_city(k)[0][0]}.", f"{len(by_city(k))} schools, led by {by_city(k)[0][0]}.")}<a href="/uk/bachata-{k}.html">{t("span", "Schools in this city →", "Schools in this city →")}</a></article>'
    for k, v in P.CITIES.items())
main = hero(t, ('Bachata Edition · UK 2027', 'Bachata Edition · UK 2027'),
  ('The best Bachata schools in the UK: ranking 2027', 'The best Bachata schools in the UK: ranking 2027'),
  (f'An independent ranking of Bachata schools in {NC} UK cities, based on public data. We will publish the results in spring 2027.', f'An independent ranking of Bachata schools in {NC} UK cities, based on public data. Results will be published in spring 2027.'),
  [('cal', f'<b>{N} schools</b> in {NC} cities', f'<b>{N} schools</b> in {NC} cities'), ('check', 'Independent, <b>not for sale</b>', 'Independent, <b>not for sale</b>'), ('clock', 'Results <b>spring 2027</b>', 'Results <b>spring 2027</b>')],
  f'<a class="btn btn-gold" href="#ranking">{t("span", "See the current standings", "See the current standings")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Enter your school", "Enter your school")}</a>')
UK_C = RV.polish_entries(P, BASE)
TX = {k: list(v) if isinstance(v, list) else v for k, v in B.R_TEXT.items()}
TX['cities'] = {'uk': ['All UK', 'All UK']}
TX['cities'].update({k: [v[0], v[1]] for k, v in P.CITIES.items()})
def _tx(k, es, en): TX[k] = [es, en]
_tx('title_city', 'Best Bachata schools: {c}', 'Best Bachata schools in {c}')
_tx('title_de', 'Best Bachata schools in the UK', 'Best Bachata schools in the UK')
_tx('sub_interim', 'Interim standing: places can still change until the results are published in spring 2027.', 'Interim standing: places can still change until the results are published in spring 2027.')
_tx('help_h', 'How does the ranking work?', 'How does the ranking work?')
_tx('help_p', 'Every school is scored on the same public criteria, identical in every country. Places cannot be bought.', 'Every school is scored on the same public criteria, identical in every country. Places cannot be bought.')
_tx('help_how', 'How we rank', 'How scoring works')
_tx('help_add', 'Add my school', 'Add my school')
_tx('help_tips_h', 'How to improve your school’s place', "How to improve your school's place")
TX['help_tips'] = [[
  'Keep your Google profile up to date and ask students for a review (Google rating 25 pts, number of reviews 10 pts, recent reviews 5 pts)',
  'State your founding year, your teaching team and class levels on your website (years teaching 10 pts)',
  'Offer a trial class and fixed beginner groups (beginner offer 10 pts)',
  'Run socials and workshops, invite guest teachers and show it online (events 10 pts)',
  'Keep your Instagram active (social media 10 pts)',
  'Confirm your festivals and competitions with a link (festivals 15 pts, competitions 5 pts)'], B.R_TEXT['help_tips'][1]]
_tx('pts', 'points', 'points'); _tx('site', 'Website', 'Website'); _tx('insta', 'Instagram', 'Instagram')
_tx('note_h', 'Is your school missing?', 'Is your school missing?')
_tx('note_p', 'Enter your school for the 2027 ranking for free.', 'Enter your school for the 2027 ranking for free.')
_tx('note_btn', 'Enter for free', 'Apply for free')
_tx('page_link', 'School page, reviews and voting', 'School page, reviews and voting')
_tx('vote_h', 'Audience Award', 'Audience Award')
_tx('vote_banner', 'Audience Award: open a school and vote. One vote per person, confirmed by email. It is separate from the points and the result is published with the ranking.', 'Audience Award: open a school and vote. One vote per person, confirmed by email. It is separate from the points, and the result comes with the ranking.')
_tx('vote_btn', 'Vote for this school', 'Vote for this school')
_tx('vote_mail', 'Your email address', 'Your email address')
_tx('vote_send', 'Send my vote', 'Send my vote')
_tx('news_opt', 'Yes, I would like to receive news, events and offers about Bachata by email from time to time. You can unsubscribe at any time.', B.R_TEXT['news_opt'][1])
_tx('vote_note', 'One vote per person. We will send you a confirmation link. We only use your email for this and to remove duplicate votes.', B.R_TEXT['vote_note'][1])
_tx('vote_ok', 'Almost done: we have sent you an email. Click the link so your vote counts. Check your spam folder too.', B.R_TEXT['vote_ok'][1])
_tx('vote_err', 'That did not work. Check your email address and try again.', B.R_TEXT['vote_err'][1])
_tx('vote_done', 'A vote has already been cast from this device. Thank you!', B.R_TEXT['vote_done'][1])
_tx('prelim_badge', 'Interim standing · not the final result, schools are still competing', 'Interim standing · not final, schools are still competing')
_tx('prelim_h', 'How the interim standing is calculated', 'How the interim standing is calculated')
_tx('prelim_p', 'We calculate points the same way as in Germany: up to 75 points for six criteria (years teaching, beginner offer, events, Google rating, number of reviews, social media) and up to 25 points for festivals, recent reviews and competitions, still "to be confirmed". Data: school websites, Google Maps and Instagram, as of October 2026. Anything unconfirmed counts at the lowest value. Places can still change.', 'Points are calculated exactly as in Germany: up to 75 points for six factors (years active, beginner offer, events, Google rating, number of reviews, social media) and up to 25 points for festivals, recent reviews and competitions, which are still “to be confirmed”. Data: school websites, Google Maps and Instagram, status October 2026. Anything unconfirmed counts at the lowest level. Positions can still change.')
_tx('empty', 'There are no results for this city yet.', 'There are no results for this city yet.')
_ES_TBC = ['Festivals', 'Recent reviews', 'Competitions entered', 'Competitions won']
_EN_TBC = ['Festivals', 'Recent reviews', 'Competitions entered', 'Competitions won']
_MX = ['15', '5', '5', '5']
_QUICK = ['uk', 'london', 'manchester', 'bristol', 'edinburgh', 'glasgow', 'cardiff']
es_js = RV.make_js('uk', {}, TX, UK_C, _QUICK, 100, pl=True, code='UK', extra={
  'tbc': ([[n, m] for n, m in zip(_ES_TBC, _MX)], [[n, m] for n, m in zip(_EN_TBC, _MX)]),
  'literals': {
    '"Follower · Posts: "': '"Followers · posts: "',
    '"Zu bestätigen"': '"To be confirmed"',
    '"Noch ohne Punkte. Schulen bestätigen diese Angaben mit Links bei der Bewerbung."': '"No points yet. Schools confirm this data with links when they apply."',
    '"Jetzt bestätigen"': '"Confirm now"',
    '"Keine Stadt gefunden"': '"No city found"',
    '["Jahre im Unterricht","Einsteigerangebot","Events und Gastlehrer","Google-Bewertung","Anzahl Bewertungen","Social Media"]': '["Years teaching","Beginner offer","Events and guests","Google rating","Number of reviews","Social media"]',
    '"Alle "+pl.length+" Schulen anzeigen"': '"See all "+pl.length+" schools"',
  }})
_tabs = RV.tabs_html(t, [(k, TX['cities'][k][0], TX['cities'][k][1]) for k in _QUICK])
RANK_SECTION = RV.ranking_section(_tabs, 'Search city …', 'Search city …', 'Cities / Cities')
main += RANK_SECTION
main += f'''
{sec(t, 1, ("Bachata in UK cities", "Bachata in UK cities"), '<div class="cards two" id="cities">' + city_cards + '</div>', alt=False).replace('<section class="block"', '<section class="block" id="cities-sec"')}
{sec(t, 2, ("How we score Bachata schools", "How we score Bachata schools"), t("p", *METHOD_ES) + t("p", 'The ranking is based only on public data. Places cannot be bought, and any paid listings are marked as ads and do not affect the points. We collect school data ourselves from Google Maps and school websites, so it may contain mistakes: <a href="/bewerbung.html?lang=en">enter a school or send us a correction</a>.', 'The ranking is based only on public data. Places cannot be bought, and paid mentions, if any, will be labelled as ads and do not affect points. We collect the school data ourselves from Google Maps and the schools\' websites, so it may contain errors: <a href="/bewerbung.html?lang=en">enter a school or send a correction</a>.'), alt=True).replace('<section class="block alt"', '<section class="block alt" id="metodo"')}
{sec(t, 3, ("Europe ranking and country rankings", "Europe ranking and country rankings"), t("p", 'Latin Dance Awards ranks schools across Europe and publishes a separate ranking for each country. The UK joins Germany, Poland, Spain, Italy, Portugal, France and the Netherlands. See the <a href="/">Europe overview</a>, the <a href="/deutschland.html">Germany ranking</a>, the <a href="/es/">Spain ranking</a> or the <a href="/it/">Italy ranking</a>.', 'Latin Dance Awards builds one ranking of schools across Europe plus a separate ranking for each country. The UK joins Germany, Poland, Spain, Italy, Portugal, France and the Netherlands. See the <a href="/">Europe overview</a>, the <a href="/deutschland.html">Germany ranking</a>, the <a href="/es/">Spain ranking</a> or the <a href="/it/">Italy ranking</a>.'), alt=False)}
'''
faq = [
 ('What is the best Bachata school in the UK?', 'What is the best Bachata school in the UK?',
  f'Right now, according to our data, {ranked[0][0]} ({P.CITIES[ranked[0][1]][0]}) is in front with {f1(_TOP[0])} of 100 points. This is an interim standing; final results follow in spring 2027.',
  f'As of today, by our data, {ranked[0][0]} ({P.CITIES[ranked[0][1]][1]}) leads with {f1en(_TOP[0])} of 100 points. This is an interim standing; final results come in spring 2027.'),
 ('Where does the data come from?', 'Where does the ranking data come from?',
  'From public sources: the rating and review count on Google Maps and the schools’ own websites, where we check that Bachata is taught.', 'From public sources: ratings and review counts on Google Maps and the schools\' own websites, where we check that the school teaches Bachata.'),
 ('Can I buy a place in the ranking?', 'Can I buy a place in the ranking?', 'No. Places cannot be bought and paid listings do not affect the points.', 'No. Places cannot be bought, and paid mentions do not affect points.'),
 ('How do I enter my school?', 'How do I enter my school?', 'Use the <a href="/bewerbung.html?lang=en">free application form</a>. By applying you can confirm your data and get the full score.', 'Use the <a href="/bewerbung.html?lang=en">free application form</a> (in English). Applying lets you confirm your details and receive the full score.'),
 ('Which cities does the ranking cover?', 'Which cities does the ranking cover?', f'To start with: {", ".join(v[0] for v in P.CITIES.values())}. We add more cities as schools apply.', f'To start with: {", ".join(v[1] for v in P.CITIES.values())}. We will add more cities as schools apply.'),
]
main += faq_html(t, faq)
uk_page('uk/index.html', 'uk/', 'The best Bachata schools in the UK: ranking 2027',
  f'Ranking of Bachata schools in the UK: {N} schools in {NC} cities, with ratings, points and method. Results in spring 2027. Independent and not for sale.',
  'The best Bachata schools in the UK: 2027 ranking', f'Ranking of Bachata schools in the UK: {N} schools in {NC} cities with ratings, points and method. Results in spring 2027. Independent and not for sale.',
  main, t.en, [crumbs('UK', 'uk/'), faq_schema(faq)], js=es_js)

# ---------- city pages ----------
for k, (cpl, cen, loc) in P.CITIES.items():
    ss = by_city(k); n = len(ss); t = T('uc' + k[:2])
    ranks = {s[0]: ranked.index(s) + 1 for s in ss}
    cards = ''.join(f'<article><h3>{s[0]}</h3>{t("p", f"Google rating: {f1(s[2])} ★ ({s[3]} reviews). Rank {ranks[s[0]]} in the UK.", f"Google rating: {f1en(s[2])} ★ ({s[3]} reviews). Rank {ranks[s[0]]} in the UK.")}<a href="{s[4]}" rel="nofollow noopener" target="_blank">{t("span", "School website", "School website")} →</a></article>' for s in ss)
    main = hero(t, (f'Bachata {cpl} · 2027', f'Bachata {cen} · 2027'),
      (f'Bachata {cpl}: the best dance schools 2027', f'Bachata {cen}: the best dance schools 2027'),
      (f'Bachata schools {loc}: {n} venues with confirmed classes, with Google ratings and interim ranking points. Results in spring 2027.', f'Bachata schools in {cen}: {n} places with confirmed classes, with Google ratings and interim ranking points. Results in spring 2027.'),
      [('cal', f'<b>{n} schools</b> {loc}', f'<b>{n} schools</b> in {cen}'), ('check', 'Data from <b>October 2026</b>', 'Data from <b>October 2026</b>')],
      f'<a class="btn btn-gold" href="#ranking">{t("span", "See the ranking", "See the ranking")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Enter your school", "Enter your school")}</a>')
    main += f'''
<section class="block alt" id="ranking"><div class="wrap tp" style="max-width:860px">
  {t("h2", f"Ranking of Bachata schools {loc}", f"Ranking of Bachata schools in {cen}")}
  {t("p", f"Interim standing based on Google ratings as of October 2026 (max. 100 points). Final results follow in spring 2027.", "Interim standing by Google ratings as of October 2026 (max 100 points). The final results are published in spring 2027.", 'class="muted"')}
  <div class="box">{school_list(ss, t)}</div>
</div></section>
{sec(t, 1, (f"Bachata schools {loc} at a glance", f"Bachata schools in {cen} at a glance"), t("p", f"We found {n} schools {loc} that teach Bachata. The order is based on interim points, not a full assessment. Times, prices and groups change, so check the school’s website.", f"In {cen} we found {n} schools that teach Bachata. The order is based on interim points, not a full assessment. Times, prices and groups change, so check them on the school's website.") + '<div class="cards two">' + cards + '</div>', alt=False)}
{sec(t, 2, (f"How to choose a Bachata class {loc}", f"How to choose a Bachata class in {cen}"), t("p", "A good Bachata class fits your level, your schedule and your commute. These tips help:", "A good Bachata class fits your level, schedule and journey. These tips help:") + '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in [
   ('<strong>Level:</strong> start in a beginner group, even if you have danced before. The basic step is the foundation of everything.', '<strong>Level:</strong> start with a beginner group, even if you have danced before. The basic step is the base for everything.'),
   ('<strong>Trial class:</strong> ask for a trial class or the start of a new group before buying a course.', '<strong>Trial class:</strong> ask for a trial class or a new group start before buying a pass.'),
   ('<strong>Partner:</strong> you usually do not need one. Ask whether partners rotate.', '<strong>Partner:</strong> you usually do not need to bring a partner. Ask whether partners rotate.'),
   ('<strong>Style:</strong> Dominican, modern and sensual Bachata each have their own character. Check which style the school teaches.', '<strong>Style:</strong> Dominicana, moderna and sensual bachata differ in character. Check which style the school teaches.')]) + '</ul>', alt=True)}
{sec(t, 3, ("UK, Europe and Germany rankings", "UK, Europe and Germany rankings"), t("p", 'See the <a href="/uk/">ranking for the whole UK</a>, the <a href="/">Europe overview</a> or the <a href="/deutschland.html">Germany ranking</a>. Do you run a school ' + loc + '? <a href="/bewerbung.html?lang=en">Enter it for free</a>.', f'See the <a href="/uk/">UK ranking</a>, the <a href="/">Europe overview</a> or the <a href="/rankings.html">Germany ranking</a>. Do you run a school in {cen}? <a href="/bewerbung.html?lang=en">Enter it for free</a>.'), alt=False)}
'''
    top = ss[0]
    faq = [
     (f'Where can I learn Bachata {loc}?', f'Where can I learn Bachata in {cen}?', f'You can learn Bachata {loc} at {", ".join(s[0] for s in ss[:3])} and other schools. The full list is above.', f'In {cen} Bachata is taught by {", ".join(s[0] for s in ss[:3])} and others. The full list is above.'),
     (f'What is the best Bachata school {loc}?', f'What is the best Bachata school in {cen}?', f'Right now, according to our data, {top[0]} is in front ({f1(top[2])} ★, {top[3]} reviews). This is an interim standing, not the final ranking.', f'As of today, by Google ratings, {top[0]} leads ({f1en(top[2])} ★, {top[3]} reviews). This is an interim standing, not the final ranking.'),
     ('Do I need a partner for a Bachata class?', 'Do I need a partner for a Bachata class?', 'Usually not. At many schools partners rotate. Ask before your first class.', 'Usually not. Many schools rotate partners. Ask before your first class.'),
     ('Which Bachata style should I start with?', 'Which Bachata style should I start with?', 'Most beginners start with modern or sensual Bachata. The basic step and the rhythm matter most; you can switch styles later.', 'Most beginners start with moderna or sensual. What matters is the basic step and the rhythm, and you can change style later.'),
     ('When is the full ranking published?', 'When is the full ranking published?', 'In spring 2027. Until then we show an interim standing based on Google ratings.', 'In spring 2027. Until then we show an interim standing based on Google ratings.'),
    ]
    main += faq_html(t, faq)
    uk_page(f'uk/bachata-{k}.html', f'uk/bachata-{k}.html', f'Bachata {cpl}: the best dance schools 2027',
      f'Bachata {cpl}: {n} schools with Google ratings and points from the 2027 ranking. Choose a Bachata class {loc} and see the interim standing.',
      f'Bachata {cen}: the best dance schools 2027', f'Bachata {cen}: {n} schools with Google ratings and 2027 ranking points. Choose a Bachata class in {cen} and see the interim ranking.',
      main, t.en, [crumbs(f'Bachata {cpl}', f'uk/bachata-{k}.html'), faq_schema(faq)])
