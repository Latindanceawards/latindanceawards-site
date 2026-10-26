# Builds the Poland section (/pl/) in Polish + English, and the Europe hub is built by build_hub.py.
# Run after build.py/build_guides.py:  python3 tools/build_pl.py
import os, sys, re, io, json, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import poland_data as P
import rank_variant as RV
FULL = {e['name']: RV.total(e) for es in RV.polish_entries(P).values() for e in es}
from build import T, page, crumbs, faq_schema, ICON, ROOT
os.makedirs(os.path.join(ROOT, 'pl'), exist_ok=True)

def f1(x): return f'{x:.1f}'.replace('.', ',')
def f1en(x): return f'{x:.1f}'
ranked = sorted(P.SCHOOLS, key=lambda s: (-FULL[s[0]], s[0]))
_TOP = [FULL[ranked[0][0]]]
def by_city(k): return [s for s in ranked if s[1] == k]

# ---------- Polish header / footer ----------
_PLH = B.HEADER
_PLH = _PLH.replace('<a class="brand" href="index.html"', '<a class="brand" href="/"', 1)
_PLH = re.sub(r'<ul id="mnav">.*?</ul>', '''<ul id="mnav">
        <li><a href="pl/#ranking" data-i18n="pn1">Ranking</a></li>
        <li><a href="pl/#miasta" data-i18n="pn2">Miasta</a></li>
        <li><a href="pl/#metoda" data-i18n="pn3">Metoda</a></li>
        <li><a href="index.html" data-i18n="pn4">Europa</a></li>
        <li><a href="deutschland.html" data-i18n="pn5">Niemcy</a></li>
      </ul>''', _PLH, count=1, flags=re.S)
_PLH = _PLH.replace('data-lang="de" aria-pressed="true">DE<', 'data-lang="de" aria-pressed="true">PL<')
_PLH = re.sub(r'<a class="btn btn-gold" href="bewerbung.html" data-i18n="t5">.*?</a>', '<a class="btn btn-gold" href="bewerbung.html?lang=en" data-i18n="pn6">Zgłoś szkołę</a>', _PLH, count=1)
_brand = re.search(r'<a class="brand" href="index.html">.*?</a>', B.FOOTER, re.S).group(0).replace('href="index.html"', 'href="/"', 1)
_PLF = f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        {_brand}
        <p class="indep" data-i18n="pf1">Niezależny projekt, który celebruje europejskie szkoły tańców latynoamerykańskich. Rankingi opierają się na danych publicznych i nie można ich kupić.</p>
      </div>
      <div>
        <p class="fh" data-i18n="pf2">Rankingi</p>
        <ul><li><a href="pl/#ranking" data-i18n="pf3">Polska 2027</a></li><li><a href="pl/#metoda" data-i18n="pf4">Metoda oceny</a></li>{''.join(f'<li><a href="pl/bachata-{k}.html">Bachata {v[0]}</a></li>' for k, v in list(P.CITIES.items())[:4])}<li><a href="index.html" data-i18n="pn4">Europa</a></li></ul>
      </div>
      <div>
        <p class="fh" data-i18n="pf5">Kontakt</p>
        <ul><li><a href="bewerbung.html?lang=en" data-i18n="pn6">Zgłoś szkołę</a></li><li><a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a></li><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li></ul>
      </div>
    </div>
    <div class="legal"><span>© 2026 Latin Dance Awards</span><span data-i18n="pf6">Edycja Bachata · Polska</span></div>
  </div>
</footer>'''

SHARED_PL_EN = {'pn1': 'Ranking', 'pn2': 'Cities', 'pn3': 'Method', 'pn4': 'Europe', 'pn5': 'Germany', 'pn6': 'Enter a school',
  'pf1': "An independent project celebrating Europe's Latin dance schools. Rankings are based on public data and can't be bought.",
  'pf2': 'Rankings', 'pf3': 'Poland 2027', 'pf4': 'How we score', 'pf5': 'Contact', 'pf6': 'Bachata Edition · Poland'}

def pl_page(fname, canon, title, desc, title_en, desc_en, main, en, schema, js=''):
    oh, of = B.HEADER, B.FOOTER
    B.HEADER, B.FOOTER = _PLH, _PLF
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            B.SHARED_EN = dict(B.SHARED_EN); B.SHARED_EN.update(SHARED_PL_EN)
            page(fname, title, desc, title_en, desc_en, canon, main, en, js, schema=schema)
    finally:
        B.HEADER, B.FOOTER = oh, of
    fp = os.path.join(ROOT, fname); h = open(fp, encoding='utf-8').read()
    h = h.replace('<html lang="de">', '<html lang="pl">', 1).replace('hreflang="de"', 'hreflang="pl"').replace('document.documentElement.lang=l;', 'document.documentElement.lang=(l==="en"?"en":"pl");')
    h = h.replace('og:locale" content="de_DE"', 'og:locale" content="pl_PL"')
    open(fp, 'w', encoding='utf-8').write(h)
    print('wrote', fname)

def school_list(ss, t, start=1):
    lis = []
    for i, s in enumerate(ss, start):
        lis.append(f'<li><b>{i}</b><a href="{s[4]}" rel="nofollow noopener" target="_blank">{s[0]}</a><span>{f1(FULL[s[0]])} pkt · {f1(s[2])} ★ ({s[3]})</span></li>')
    return '<ol class="top">' + ''.join(lis) + '</ol>'

def hero(t, edition, h1, lede, facts, ctas, seal='badge-bachata-poland-2027.svg', alt='Odznaka Bachata Awards Polska 2027'):
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
    return '<section class="block alt" id="faq"><div class="wrap"><div class="sec-head">' + t("h2", 'Najczęstsze pytania', 'Frequently asked questions') + '</div><div class="faq">' + ''.join(f'<details>{t("summary", q, qe)}{t("p", a, ae)}</details>' for q, qe, a, ae in faq) + '</div></div></section>'

N = len(P.SCHOOLS); NC = len(P.CITIES)
METHOD_PL = ('Oceniamy szkoły tak samo jak w Niemczech, według dziewięciu kryteriów i 100 punktów: lata działalności, oferta dla początkujących, wydarzenia, ocena w Google, liczba opinii i media społecznościowe (razem 75 punktów) oraz festiwale, aktualne opinie i konkursy (25 punktów, na razie „do potwierdzenia”). Dane pochodzą ze stron szkół, z Map Google i z Instagrama. Czego nie da się potwierdzić, liczy się na najniższym poziomie, a szkoła może to uzupełnić w zgłoszeniu.',
             'We score schools exactly as in Germany, on nine factors and 100 points: years active, beginner offer, events, Google rating, number of reviews and social media (75 points together), plus festivals, recent reviews and competitions (25 points, still “to be confirmed”). The data comes from the schools’ websites, Google Maps and Instagram. Anything we cannot confirm counts at the lowest level, and a school can complete it in its application.')

def city_label(k): return P.CITIES[k]

# ---------- /pl/ index ----------
t = T('pl')
top5 = ranked[:5]
city_cards = ''.join(
    f'<article><h3>{t("span", "Bachata " + v[0], "Bachata " + v[1])}</h3>{t("p", f"{len(by_city(k))} szkół, na czele: {by_city(k)[0][0]}.", f"{len(by_city(k))} schools, led by {by_city(k)[0][0]}.")}<a href="/pl/bachata-{k}.html">{t("span", "Szkoły w mieście →", "Schools in this city →")}</a></article>'
    for k, v in P.CITIES.items())
main = hero(t, ('Edycja Bachata · Polska 2027', 'Bachata Edition · Poland 2027'),
  ('Najlepsze szkoły bachaty w Polsce: ranking 2027', 'The best Bachata schools in Poland: ranking 2027'),
  (f'Niezależny ranking szkół bachaty w {NC} miastach Polski, oparty na publicznych danych. Wyniki ogłosimy wiosną 2027.', f'An independent ranking of Bachata schools in {NC} Polish cities, based on public data. Results will be published in spring 2027.'),
  [('cal', f'<b>{N} szkół</b> w {NC} miastach', f'<b>{N} schools</b> in {NC} cities'), ('check', 'Niezależny, <b>nie do kupienia</b>', 'Independent, <b>not for sale</b>'), ('clock', 'Wyniki <b>wiosną 2027</b>', 'Results <b>spring 2027</b>')],
  f'<a class="btn btn-gold" href="#ranking">{t("span", "Zobacz stan na dziś", "See the current standings")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Zgłoś swoją szkołę", "Enter your school")}</a>')
import rank_variant as RV
PL_C = RV.polish_entries(P)
TX = {k: list(v) if isinstance(v, list) else v for k, v in B.R_TEXT.items()}
TX['cities'] = {'polska': ['Cała Polska', 'All Poland']}
TX['cities'].update({k: [v[0], v[1]] for k, v in P.CITIES.items()})
def _tx(k, pl, en): TX[k] = [pl, en]
_tx('title_city', 'Najlepsze szkoły bachaty: {c}', 'Best Bachata schools in {c}')
_tx('title_de', 'Najlepsze szkoły bachaty w Polsce', 'Best Bachata schools in Poland')
_tx('sub_interim', 'Stan przejściowy: miejsca mogą się jeszcze zmienić do ogłoszenia wyników wiosną 2027.', 'Interim standing: places can still change until the results are published in spring 2027.')
_tx('help_h', 'Jak działa ranking?', 'How does the ranking work?')
_tx('help_p', 'Każda szkoła jest oceniana według tych samych publicznych kryteriów, tak samo w każdym kraju. Miejsc nie można kupić.', 'Every school is scored on the same public criteria, identical in every country. Places cannot be bought.')
_tx('help_how', 'Jak oceniamy', 'How scoring works')
_tx('help_add', 'Dodaj moją szkołę', 'Add my school')
_tx('help_tips_h', 'Jak poprawić miejsce swojej szkoły', "How to improve your school's place")
TX['help_tips'] = [[
  'Dbaj o wizytówkę w Google i poproś uczniów o opinię (ocena w Google 25 pkt, liczba opinii 10 pkt, aktualne opinie 5 pkt)',
  'Podaj na stronie rok założenia, zespół instruktorów i poziomy kursów (lata działalności 10 pkt)',
  'Oferuj lekcję próbną i stałe terminy dla początkujących (oferta dla początkujących 10 pkt)',
  'Organizuj imprezy i warsztaty, zapraszaj gościnnych instruktorów i pokazuj to w sieci (wydarzenia 10 pkt)',
  'Regularnie prowadź Instagram (media społecznościowe 10 pkt)',
  'Potwierdź występy na festiwalach i udział w konkursach linkiem (festiwale 15 pkt, konkursy 5 pkt)'], B.R_TEXT['help_tips'][1]]
_tx('pts', 'punkty', 'points'); _tx('site', 'Strona', 'Website'); _tx('insta', 'Instagram', 'Instagram')
_tx('note_h', 'Brakuje Twojej szkoły?', 'Is your school missing?')
_tx('note_p', 'Zgłoś szkołę bezpłatnie do rankingu 2027.', 'Enter your school for the 2027 ranking for free.')
_tx('note_btn', 'Zgłoś bezpłatnie', 'Apply for free')
_tx('page_link', 'Strona szkoły, opinie i głosowanie', 'School page, reviews and voting')
_tx('vote_h', 'Nagroda publiczności', 'Audience Award')
_tx('vote_banner', 'Nagroda publiczności: otwórz szkołę i zagłosuj. Jeden głos na osobę, potwierdzony e-mailem. Nagroda jest niezależna od punktów, a wynik ogłosimy razem z rankingiem.', 'Audience Award: open a school and vote. One vote per person, confirmed by email. It is separate from the points, and the result comes with the ranking.')
_tx('vote_btn', 'Zagłosuj na tę szkołę', 'Vote for this school')
_tx('vote_mail', 'Twój adres e-mail', 'Your email address')
_tx('vote_send', 'Wyślij głos', 'Send my vote')
_tx('news_opt', 'Tak, wysyłajcie mi czasem wiadomości, wydarzenia i oferty związane z bachatą e-mailem. Wypisać się można w każdej chwili.', B.R_TEXT['news_opt'][1])
_tx('vote_note', 'Jeden głos na osobę. Wyślemy Ci link potwierdzający. Twojego adresu e-mail używamy tylko do tego i do usuwania podwójnych głosów.', B.R_TEXT['vote_note'][1])
_tx('vote_ok', 'Prawie gotowe: wysłaliśmy Ci e-mail. Kliknij w link, aby Twój głos się liczył. Sprawdź też folder ze spamem.', B.R_TEXT['vote_ok'][1])
_tx('vote_err', 'To nie zadziałało. Sprawdź adres e-mail i spróbuj ponownie.', B.R_TEXT['vote_err'][1])
_tx('vote_done', 'Na tym urządzeniu już głosowano. Dziękujemy!', B.R_TEXT['vote_done'][1])
_tx('prelim_badge', 'Stan przejściowy · nie wynik końcowy, szkoły wciąż rywalizują', 'Interim standing · not final, schools are still competing')
_tx('prelim_h', 'Jak powstaje stan przejściowy', 'How the interim standing is calculated')
_tx('prelim_p', 'Punkty liczymy tak samo jak w Niemczech: do 75 punktów za sześć kryteriów (lata działalności, oferta dla początkujących, wydarzenia, ocena w Google, liczba opinii, media społecznościowe) i do 25 punktów za festiwale, aktualne opinie i konkursy, które są jeszcze „do potwierdzenia”. Dane: strony szkół, Mapy Google i Instagram, stan na październik 2026. Czego nie potwierdzono, liczy się na najniższym poziomie. Miejsca mogą się jeszcze zmienić.', 'Points are calculated exactly as in Germany: up to 75 points for six factors (years active, beginner offer, events, Google rating, number of reviews, social media) and up to 25 points for festivals, recent reviews and competitions, which are still “to be confirmed”. Data: school websites, Google Maps and Instagram, status October 2026. Anything unconfirmed counts at the lowest level. Positions can still change.')
_tx('page_link', 'Strona szkoły, opinie i głosowanie', B.R_TEXT['page_link'][1])
_tx('empty', 'Dla tego miasta nie ma jeszcze wyników.', 'There are no results for this city yet.')
_PL_TBC = ['Festiwale', 'Aktualne opinie', 'Udział w konkursach', 'Wygrane konkursy']
_EN_TBC = ['Festivals', 'Recent reviews', 'Competitions entered', 'Competitions won']
_MX = ['15', '5', '5', '5']
_QUICK = ['polska', 'warszawa', 'krakow', 'wroclaw', 'poznan', 'gdansk', 'lodz']
pl_js = RV.make_js('polska', {}, TX, PL_C, _QUICK, 100, pl=True, extra={
  'tbc': ([[n, m] for n, m in zip(_PL_TBC, _MX)], [[n, m] for n, m in zip(_EN_TBC, _MX)]),
  'literals': {
    '"Follower · Posts: "': '"Obserwujący · posty: "',
    '"Zu bestätigen"': '"Do potwierdzenia"',
    '"Noch ohne Punkte. Schulen bestätigen diese Angaben mit Links bei der Bewerbung."': '"Jeszcze bez punktów. Szkoły potwierdzają te dane linkami przy zgłoszeniu."',
    '"Jetzt bestätigen"': '"Potwierdź teraz"',
    '"Keine Stadt gefunden"': '"Nie znaleziono miasta"',
    '["Jahre im Unterricht","Einsteigerangebot","Events und Gastlehrer","Google-Bewertung","Anzahl Bewertungen","Social Media"]': '["Lata nauczania","Oferta dla początkujących","Wydarzenia i goście","Ocena w Google","Liczba opinii","Media społecznościowe"]',
    '"Alle "+pl.length+" Schulen anzeigen"': '"Pokaż wszystkie szkoły ("+pl.length+")"',
  }})
_tabs = RV.tabs_html(t, [(k, TX['cities'][k][0], TX['cities'][k][1]) for k in _QUICK])
RANK_SECTION = RV.ranking_section(_tabs, 'Szukaj miasta …', 'Search city …', 'Miasta / Cities')
main += RANK_SECTION
main += f'''
{sec(t, 1, ("Bachata w polskich miastach", "Bachata in Polish cities"), '<div class="cards two" id="miasta">' + city_cards + '</div>', alt=False).replace('<section class="block"', '<section class="block" id="miasta-sec"')}
{sec(t, 2, ("Jak oceniamy szkoły bachaty", "How we score Bachata schools"), t("p", *METHOD_PL) + t("p", 'Ranking opiera się wyłącznie na danych publicznych. Miejsca nie można kupić, a płatne wzmianki, jeśli się pojawią, będą oznaczone jako reklama i nie wpływają na punkty. Dane o szkołach zbieramy samodzielnie z Map Google i stron szkół, dlatego mogą zawierać błędy: <a href="/bewerbung.html?lang=en">zgłoś szkołę lub poprawkę</a>.', 'The ranking is based only on public data. Places cannot be bought, and paid mentions, if any, will be labelled as ads and do not affect points. We collect the school data ourselves from Google Maps and the schools\' websites, so it may contain errors: <a href="/bewerbung.html?lang=en">enter a school or send a correction</a>.'), alt=True).replace('<section class="block alt"', '<section class="block alt" id="metoda"')}
{sec(t, 3, ("Ranking Europy i rankingi krajów", "Europe ranking and country rankings"), t("p", 'Latin Dance Awards tworzy jeden ranking szkół w całej Europie oraz osobny ranking dla każdego kraju. Polska jest drugim krajem po Niemczech. Zobacz <a href="/">przegląd Europy</a> albo <a href="/deutschland.html">ranking Niemiec</a>.', 'Latin Dance Awards builds one ranking of schools across Europe plus a separate ranking for each country. Poland is the second country after Germany. See the <a href="/">Europe overview</a> or the <a href="/rankings.html">Germany ranking</a>.'), alt=False)}
'''
faq = [
 ('Jaka jest najlepsza szkoła bachaty w Polsce?', 'What is the best Bachata school in Poland?',
  f'Na dziś, według naszych danych, prowadzi {ranked[0][0]} ({P.CITIES[ranked[0][1]][0]}) z {f1(_TOP[0])} z 100 punktów. To stan przejściowy, wyniki końcowe ukażą się wiosną 2027.',
  f'As of today, by our data, {ranked[0][0]} ({P.CITIES[ranked[0][1]][1]}) leads with {f1en(_TOP[0])} of 100 points. This is an interim standing; final results come in spring 2027.'),
 ('Skąd bierzecie dane do rankingu?', 'Where does the ranking data come from?',
  'Z publicznych źródeł: ocen i liczby opinii w Mapach Google oraz ze stron internetowych szkół, na których sprawdzamy, czy szkoła uczy bachaty.', 'From public sources: ratings and review counts on Google Maps and the schools\' own websites, where we check that the school teaches Bachata.'),
 ('Czy mogę kupić miejsce w rankingu?', 'Can I buy a place in the ranking?', 'Nie. Miejsc nie można kupić, a płatne wzmianki nie wpływają na punkty.', 'No. Places cannot be bought, and paid mentions do not affect points.'),
 ('Jak zgłosić swoją szkołę?', 'How do I enter my school?', 'Użyj <a href="/bewerbung.html?lang=en">bezpłatnego formularza zgłoszeniowego</a> (po angielsku). Dzięki zgłoszeniu potwierdzisz swoje dane i otrzymasz pełną punktację.', 'Use the <a href="/bewerbung.html?lang=en">free application form</a> (in English). Applying lets you confirm your details and receive the full score.'),
 ('W jakich miastach jest ranking?', 'Which cities does the ranking cover?', f'Na start: {", ".join(v[0] for v in P.CITIES.values())}. Kolejne miasta dodamy po zgłoszeniach szkół.', f'To start with: {", ".join(v[1] for v in P.CITIES.values())}. We will add more cities as schools apply.'),
]
main += faq_html(t, faq)
pl_page('pl/index.html', 'pl/', 'Najlepsze szkoły bachaty w Polsce: ranking 2027',
  f'Ranking szkół bachaty w Polsce: {N} szkół w {NC} miastach, z ocenami, punktami i metodą. Wyniki wiosną 2027. Niezależny i nie do kupienia.',
  'The best Bachata schools in Poland: 2027 ranking', f'Ranking of Bachata schools in Poland: {N} schools in {NC} cities with ratings, points and method. Results in spring 2027. Independent and not for sale.',
  main, t.en, [crumbs('Polska', 'pl/'), faq_schema(faq)], js=pl_js)

# ---------- city pages ----------
for k, (cpl, cen, loc) in P.CITIES.items():
    ss = by_city(k); n = len(ss); t = T('pc' + k[:2])
    ranks_in_pl = {s[0]: ranked.index(s) + 1 for s in ss}
    cards = ''.join(f'<article><h3>{s[0]}</h3>{t("p", f"Ocena w Google: {f1(s[2])} ★ ({s[3]} opinii). Miejsce {ranks_in_pl[s[0]]} w Polsce.", f"Google rating: {f1en(s[2])} ★ ({s[3]} reviews). Rank {ranks_in_pl[s[0]]} in Poland.")}<a href="{s[4]}" rel="nofollow noopener" target="_blank">{t("span", "Strona szkoły", "School website")} →</a></article>' for s in ss)
    main = hero(t, (f'Bachata {cpl} · 2027', f'Bachata {cen} · 2027'),
      (f'Bachata {cpl}: najlepsze szkoły tańca 2027', f'Bachata {cen}: the best dance schools 2027'),
      (f'Szkoły bachaty w {loc}: {n} miejsc z potwierdzonymi zajęciami, z ocenami z Google i punktami przejściowego rankingu. Wyniki wiosną 2027.', f'Bachata schools in {cen}: {n} places with confirmed classes, with Google ratings and interim ranking points. Results in spring 2027.'),
      [('cal', f'<b>{n} szkół</b> w {loc}', f'<b>{n} schools</b> in {cen}'), ('check', 'Dane z <b>października 2026</b>', 'Data from <b>October 2026</b>')],
      f'<a class="btn btn-gold" href="#ranking">{t("span", "Zobacz ranking", "See the ranking")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Zgłoś swoją szkołę", "Enter your school")}</a>')
    main += f'''
<section class="block alt" id="ranking"><div class="wrap tp" style="max-width:860px">
  {t("h2", f"Ranking szkół bachaty w {loc}", f"Ranking of Bachata schools in {cen}")}
  {t("p", f"Stan przejściowy według ocen w Google z października 2026 (maks. 100 punktów). Wyniki końcowe ukażą się wiosną 2027.", "Interim standing by Google ratings as of October 2026 (max 100 points). The final results are published in spring 2027.", 'class="muted"')}
  <div class="box">{school_list(ss, t)}</div>
</div></section>
{sec(t, 1, (f"Szkoły bachaty w {loc} w skrócie", f"Bachata schools in {cen} at a glance"), t("p", f"W {loc} znaleźliśmy {n} szkół, które uczą bachaty. Kolejność jest oparta na przejściowych punktach, a nie na pełnej ocenie. Godziny, ceny i grupy zmieniają się, więc sprawdź je na stronie szkoły.", f"In {cen} we found {n} schools that teach Bachata. The order is based on interim points, not a full assessment. Times, prices and groups change, so check them on the school's website.") + '<div class="cards two">' + cards + '</div>', alt=False)}
{sec(t, 2, (f"Jak wybrać kurs bachaty w {loc}", f"How to choose a Bachata class in {cen}"), t("p", "Dobry kurs bachaty pasuje do Twojego poziomu, terminu i dojazdu. Pomogą te wskazówki:", "A good Bachata class fits your level, schedule and journey. These tips help:") + '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in [
   ('<strong>Poziom:</strong> zacznij od grupy dla początkujących, nawet jeśli tańczyłeś wcześniej. Podstawowy krok to baza dla wszystkiego.', '<strong>Level:</strong> start with a beginner group, even if you have danced before. The basic step is the base for everything.'),
   ('<strong>Lekcja próbna:</strong> zapytaj o zajęcia próbne lub start nowej grupy, zanim kupisz karnet.', '<strong>Trial class:</strong> ask for a trial class or a new group start before buying a pass.'),
   ('<strong>Partner:</strong> zwykle nie musisz przychodzić z partnerem. Zapytaj, czy pary się zmieniają.', '<strong>Partner:</strong> you usually do not need to bring a partner. Ask whether partners rotate.'),
   ('<strong>Styl:</strong> bachata dominicana, moderna i sensual różnią się charakterem. Zobacz, który styl uczy szkoła.', '<strong>Style:</strong> Dominicana, moderna and sensual bachata differ in character. Check which style the school teaches.')]) + '</ul>', alt=True)}
{sec(t, 3, ("Ranking Polski, Europy i Niemiec", "Poland, Europe and Germany rankings"), t("p", 'Zobacz <a href="/pl/">ranking całej Polski</a>, <a href="/">przegląd Europy</a> albo <a href="/deutschland.html">ranking Niemiec</a>. Prowadzisz szkołę w ' + loc + '? <a href="/bewerbung.html?lang=en">Zgłoś ją bezpłatnie</a>.', f'See the <a href="/pl/">Poland ranking</a>, the <a href="/">Europe overview</a> or the <a href="/rankings.html">Germany ranking</a>. Do you run a school in {cen}? <a href="/bewerbung.html?lang=en">Enter it for free</a>.'), alt=False)}
'''
    top = ss[0]
    faq = [
     (f'Gdzie nauczyć się bachaty w {loc}?', f'Where can I learn Bachata in {cen}?', f'W {loc} bachaty uczą m.in. {", ".join(s[0] for s in ss[:3])}. Pełna lista jest powyżej.', f'In {cen} Bachata is taught by {", ".join(s[0] for s in ss[:3])} and others. The full list is above.'),
     (f'Jaka jest najlepsza szkoła bachaty w {loc}?', f'What is the best Bachata school in {cen}?', f'Na dziś, według naszych danych, prowadzi {top[0]} ({f1(top[2])} ★, {top[3]} opinii). To stan przejściowy, a nie ostateczny ranking.', f'As of today, by Google ratings, {top[0]} leads ({f1en(top[2])} ★, {top[3]} reviews). This is an interim standing, not the final ranking.'),
     ('Czy potrzebuję partnera na kurs bachaty?', 'Do I need a partner for a Bachata class?', 'Zazwyczaj nie. W wielu szkołach pary się zmieniają. Zapytaj o to przed pierwszymi zajęciami.', 'Usually not. Many schools rotate partners. Ask before your first class.'),
     ('Od jakiego stylu bachaty zacząć?', 'Which Bachata style should I start with?', 'Większość początkujących zaczyna od bachaty moderna lub sensual. Najważniejszy jest krok podstawowy i rytm, a styl można później zmienić.', 'Most beginners start with moderna or sensual. What matters is the basic step and the rhythm, and you can change style later.'),
     ('Kiedy ukaże się pełny ranking?', 'When is the full ranking published?', 'Wiosną 2027. Do tego czasu pokazujemy stan przejściowy, oparty na ocenach w Google.', 'In spring 2027. Until then we show an interim standing based on Google ratings.'),
    ]
    main += faq_html(t, faq)
    pl_page(f'pl/bachata-{k}.html', f'pl/bachata-{k}.html', f'Bachata {cpl}: najlepsze szkoły tańca 2027',
      f'Bachata {cpl}: {n} szkół z ocenami z Google i punktami rankingu 2027. Wybierz kurs bachaty w {loc} i zobacz przejściowy ranking.',
      f'Bachata {cen}: the best dance schools 2027', f'Bachata {cen}: {n} schools with Google ratings and 2027 ranking points. Choose a Bachata class in {cen} and see the interim ranking.',
      main, t.en, [crumbs(f'Bachata {cpl}', f'pl/bachata-{k}.html'), faq_schema(faq)])

