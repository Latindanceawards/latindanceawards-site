# Builds the Europe hub = homepage (index.html): one overall ranking plus a block per country.
# Run after build.py, build_guides.py and build_pl.py:  python3 tools/build_hub.py
import os, sys, re, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import poland_data as P
from build import T, page, crumbs, faq_schema, ICON, ROOT

def f1(x): return f'{x:.1f}'.replace('.', ',')
def _num(x): return float(x.replace(',', '.'))

def de_rows():
    out = []
    for e in B.SCH:
        m = re.match(r'([\d,]+) ★ · ([\d.]+)', (e['fx'][0] if e.get('fx') else '').replace('\xa0', ' '))
        cn = B.CITY_NAMES.get(e['city'], (e['city'].title(), e['city'].title()))
        if m:
            r, v = _num(m.group(1)), int(m.group(2).replace('.', ''))
            out.append(dict(name=e['name'], cc='de', city=cn[0], r=r, v=v, pts=P.pts(r, v), href=f'/schools/{e["slug"]}.html'))
        else:
            out.append(dict(name=e['name'], cc='de', city=cn[0], r=None, v=0, pts=0.0, href=f'/schools/{e["slug"]}.html'))
    return out

def pl_rows():
    return [dict(name=s[0], cc='pl', city=P.CITIES[s[1]][0], r=s[2], v=s[3], pts=P.pts(s[2], s[3]), href=f'/pl/bachata-{s[1]}.html') for s in P.SCHOOLS]

ALL = sorted(de_rows() + pl_rows(), key=lambda x: (-x['pts'], x['name']))
ND = sum(1 for x in ALL if x['cc'] == 'de'); NP = len(ALL) - ND
NCD = 79; NC = len(P.CITIES)
TOPN = 25
t = T('eu')

def hero(edition, h1, lede, facts, ctas):
    return f'''<section class="page-hero"><div class="wrap">
  <div>
    <span class="edition rise d1"><i></i>{t("span", *edition)}</span>
    <h1 class="rise d2">{t("span", *h1)}</h1>
    <p class="lede rise d3">{t("span", *lede)}</p>
    <div class="facts rise d4">{''.join(f'<span>{ICON[ic]}{t("span", d, e)}</span>' for ic, d, e in facts)}</div>
    <div class="ctas rise d5">{ctas}</div>
  </div>
  <div class="seal-box rise d3"><img class="seal" src="badge-bachata-europe.svg" alt="Siegel der Bachata Awards Europa" width="360" height="360" fetchpriority="low"></div>
</div></section>'''

def sec(h2, body, alt=True, sid=''):
    idattr = f' id="{sid}"' if sid else ''
    return f'<section{idattr} class="block{" alt" if alt else ""}"><div class="wrap prose">{t("h2", *h2)}{body}</div></section>'

def row(i, x):
    flag = x['cc'].upper()
    hid = ' class="more" hidden' if i > TOPN else ''
    return (f'<li data-c="{x["cc"]}"{hid}><b>{i}</b><a href="{x["href"]}">{x["name"]}</a>'
            f'<em>{x["city"]} · {flag}</em><span>' + (f'{f1(x["pts"])} / 35 · {f1(x["r"])} ★ ({x["v"]})' if x['r'] else 'keine Google-Bewertung') + '</span></li>')

def top3(cc):
    xs = [x for x in ALL if x['cc'] == cc][:3]
    return '<ol class="top">' + ''.join(f'<li><b>{i}</b><a href="{x["href"]}">{x["name"]}</a><span>{f1(x["pts"])} / 35</span></li>' for i, x in enumerate(xs, 1)) + '</ol>'

rows = ''.join(row(i, x) for i, x in enumerate(ALL, 1))

faq = [
 ('Wie entsteht das Europa-Ranking?', 'How is the Europe ranking built?',
  'Jedes Land bekommt ein eigenes Ranking, und das Europa-Ranking führt alle Schulen zusammen. Zurzeit gilt für alle Schulen derselbe Zwischenstand: die gewichtete Google-Bewertung und die Zahl der Bewertungen, zusammen höchstens 35 Punkte. Die vollständige Wertung nach neun Kriterien und 100 Punkten kommt, sobald ein Land seine Daten komplett hat.',
  'Each country gets its own ranking, and the Europe ranking brings all schools together. Right now every school has the same interim score: the weighted Google rating and the number of reviews, 35 points at most. The full scoring on nine factors and 100 points follows as soon as a country has its data complete.'),
 ('Kann eine Schule für einen besseren Platz bezahlen?', 'Can a school pay for a better place?',
  'Nein. Die Rankings basieren auf öffentlichen Daten und sind nicht käuflich. Anmelden ist kostenlos.', 'No. The rankings are based on public data and cannot be bought. Applying is free.'),
 ('Wann erscheinen die Ergebnisse?', 'When are the results published?',
  'Deutschland am 20. Dezember 2026 um 19 Uhr, Polen im Frühjahr 2027. Weitere Länder folgen.', 'Germany on December 20, 2026 at 7 pm, Poland in spring 2027. More countries follow.'),
 ('Wie kommt meine Schule ins Ranking?', 'How does my school get into the ranking?',
  'Melde sie kostenlos an. Wir nehmen jede Schule auf, die nachweislich Bachata unterrichtet, auch ohne Anmeldung.', 'Enter it for free. We include every school that demonstrably teaches Bachata, even without an application.'),
]
faq_html = ('<section class="block alt" id="faq"><div class="wrap"><div class="sec-head">' + t("h2", 'Häufige Fragen', 'Frequently asked questions') + '</div><div class="faq">'
            + ''.join(f'<details>{t("summary", q, qe)}{t("p", a, ae)}</details>' for q, qe, a, ae in faq) + '</div></div></section>')

hero_html = hero(('Europa · Bachata Awards', 'Europe · Bachata Awards'),
  ('Beste Bachata-Schulen in Europa: das Ranking', 'The best Bachata schools in Europe: the ranking'),
  (f'Ein Ranking für ganz Europa und ein eigenes Ranking für jedes Land: {len(ALL)} Schulen in zwei Ländern, unabhängig bewertet nach öffentlichen Daten.',
   f'One ranking for all of Europe and a separate ranking for each country: {len(ALL)} schools in two countries, scored independently from public data.'),
  [('cal', f'<b>{len(ALL)} Schulen</b> in {NCD + NC} Städten', f'<b>{len(ALL)} schools</b> in {NCD + NC} cities'),
   ('check', 'Unabhängig, <b>nicht käuflich</b>', 'Independent, <b>not for sale</b>'),
   ('clock', 'Deutschland <b>20. Dez</b> · Polen <b>Frühjahr 2027</b>', 'Germany <b>Dec 20</b> · Poland <b>spring 2027</b>')],
  f'<a class="btn btn-gold" href="#ranking">{t("span", "Europa-Ranking ansehen", "See the Europe ranking")}</a><a class="btn btn-ghost" href="bewerbung.html">{t("span", "Schule kostenlos anmelden", "Enter a school for free")}</a>')

CSS = ('<style>.eu-list{list-style:none;margin:0;padding:0;display:grid;gap:8px}'
 '.eu-list li{display:grid;grid-template-columns:34px 1fr auto;gap:4px 14px;align-items:center;padding:13px 16px;border-radius:14px;background:rgba(255,255,255,.04)}'
 '.eu-list li[hidden]{display:none}.eu-list b{font-family:var(--serif);color:var(--gold);font-size:20px}'
 '.eu-list a{color:inherit;font-weight:600;text-decoration:none}.eu-list a:hover{color:var(--gold-light)}'
 '.eu-list em{grid-column:2;font-style:normal;color:var(--muted);font-size:13px}'
 '.eu-list span{grid-column:3;grid-row:1/3;text-align:right;color:var(--muted);font-size:13px}'
 '.eu-filter{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0}'
 '.eu-filter button{font:inherit;font-size:14px;cursor:pointer;padding:9px 16px;border-radius:999px;border:1px solid rgba(228,185,91,.35);background:transparent;color:var(--muted)}'
 '.eu-filter button[aria-pressed=true]{background:linear-gradient(135deg,#FCEBB6,#E2B457 45%,#B07A27);color:#2A1A08;border-color:transparent}'
 '.eu-more{margin-top:18px;text-align:center}'
 '@media(max-width:560px){.eu-list li{grid-template-columns:28px 1fr}.eu-list span{grid-column:2;grid-row:auto;text-align:left}}</style>')

main = hero_html + CSS + f'''
<section class="block alt" id="ranking"><div class="wrap tp" style="max-width:900px">
  {t("h2", "Europa-Ranking: der Zwischenstand", "Europe ranking: the interim standing")}
  {t("p", f"Alle {len(ALL)} Schulen aus allen Ländern in einer Liste, nach demselben Zwischenstand sortiert: gewichtete Google-Bewertung und Zahl der Bewertungen, höchstens 35 Punkte. Stand: Oktober 2026. Das ist kein Endergebnis.", f"All {len(ALL)} schools from all countries in one list, sorted by the same interim score: weighted Google rating and number of reviews, 35 points at most. Status: October 2026. This is not a final result.")}
  <div class="eu-filter" role="group" aria-label="Filter">
    <button type="button" data-f="all" aria-pressed="true">{t("span", f"Alle Länder ({len(ALL)})", f"All countries ({len(ALL)})")}</button>
    <button type="button" data-f="de" aria-pressed="false">{t("span", f"Deutschland ({ND})", f"Germany ({ND})")}</button>
    <button type="button" data-f="pl" aria-pressed="false">{t("span", f"Polen ({NP})", f"Poland ({NP})")}</button>
  </div>
  <ol class="eu-list" id="eu-list">{rows}</ol>
  <p class="eu-more"><button type="button" class="btn btn-ghost" id="eu-more">{t("span", "Alle anzeigen", "Show all")}</button></p>
</div></section>
<section class="block" id="laender"><div class="wrap tp" style="max-width:900px">
  {t("h2", "Rankings nach Ländern", "Rankings by country")}
  <div class="people">
    <div class="box"><h3>{t("span", "Deutschland", "Germany")}</h3><p class="muted">{t("span", f"{ND} Schulen in {NCD} Städten. Ergebnisse am 20. Dezember 2026 um 19 Uhr.", f"{ND} schools in {NCD} cities. Results on December 20, 2026 at 7 pm.")}</p>{top3("de")}<div class="btnrow"><a class="btn btn-gold" href="deutschland.html">{t("span", "Land ansehen", "See the country")}</a><a class="btn btn-ghost" href="rankings.html">{t("span", "Zum Ranking", "To the ranking")}</a></div></div>
    <div class="box"><h3>{t("span", "Polen", "Poland")}</h3><p class="muted">{t("span", f"{NP} Schulen in {NC} Städten. Ergebnisse im Frühjahr 2027.", f"{NP} schools in {NC} cities. Results in spring 2027.")}</p>{top3("pl")}<div class="btnrow"><a class="btn btn-gold" href="pl/">{t("span", "Land ansehen", "See the country")}</a></div></div>
  </div>
</div></section>
''' + sec(("So bewerten wir", "How we score"),
  t("p", "Jede Schule wird nach denselben öffentlichen Kriterien bewertet, in jedem Land gleich: Google-Bewertung, Zahl der Bewertungen, Jahre am Markt, Angebot für Anfänger, Veranstaltungen, Auftritt in sozialen Medien und mehr, zusammen 100 Punkte. Zurzeit zeigen wir für alle Länder denselben Zwischenstand aus zwei Kriterien. So bleibt das Europa-Ranking vergleichbar, bis jedes Land seine vollständigen Daten hat.",
        "Every school is scored on the same public factors, identical in every country: Google rating, number of reviews, years in business, beginner offer, events, social media presence and more, 100 points in total. For now we show the same interim standing from two factors for all countries. That keeps the Europe ranking comparable until every country has its full data.")
  + t("p", 'Die ausführliche Methode für Deutschland steht <a href="deutschland.html#method">hier</a>, die für Polen <a href="pl/#metoda">hier</a>.',
        'The detailed method for Germany is <a href="deutschland.html#method">here</a>, the one for Poland <a href="pl/#metoda">here</a>.'), alt=False, sid='methode') + sec(("Warum ein Ranking für ganz Europa?", "Why one ranking for all of Europe?"),
  t("p", "Wer eine gute Bachata-Schule sucht, schaut selten nur in die eigene Stadt: Auf Reisen, beim Umzug oder für ein Wochenende im Nachbarland zählt, wo es gute Kurse gibt. Das Europa-Ranking macht Schulen über Ländergrenzen hinweg vergleichbar, und die Länderseiten zeigen jeweils die beste Schule der Stadt.",
        "Anyone looking for a good Bachata school rarely looks only at their own city: when travelling, moving or planning a weekend in a neighbouring country, what matters is where the good classes are. The Europe ranking makes schools comparable across borders, and the country pages show the best school in each city."), alt=True) + faq_html + sec(
  ("Dein Land fehlt?", "Is your country missing?"),
  t("p", 'Wir starten weitere Länder Schritt für Schritt. Schreib uns an <a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a>, wenn du eine Schule betreibst oder die Szene in deinem Land kennst.',
        'We are adding more countries step by step. Email <a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a> if you run a school or know the scene in your country.'))

hub_js = '''
  (function(){
    var list=document.getElementById("eu-list"),more=document.getElementById("eu-more"),f="all",open=false,TOP=%d;
    function inF(li){return f==="all"||li.getAttribute("data-c")===f;}
    function render(){var i=0,n=0;[].forEach.call(list.children,function(li){if(!inF(li)){li.hidden=true;return;}n++;i++;li.hidden=!open&&i>TOP;});more.parentNode.hidden=n<=TOP;}
    [].forEach.call(document.querySelectorAll(".eu-filter button"),function(b){b.addEventListener("click",function(){f=b.getAttribute("data-f");[].forEach.call(document.querySelectorAll(".eu-filter button"),function(x){x.setAttribute("aria-pressed",x===b?"true":"false");});render();});});
    more.addEventListener("click",function(){open=!open;var en=document.documentElement.lang==="en";more.firstChild.textContent=open?(en?"Show less":"Weniger anzeigen"):(en?"Show all":"Alle anzeigen");more.removeAttribute("data-i18n");render();});
    render();
  })();
''' % TOPN

# Europe header: same shell, nav points at the hub sections
H0 = B.HEADER
_a = H0.index('<ul id="mnav">'); _b = H0.index('</ul>', _a) + 5
nav = '''<ul id="mnav">
        <li><a href="#ranking" data-i18n="en1">Europa-Ranking</a></li>
        <li><a href="#laender" data-i18n="en2">Länder</a></li>
        <li><a href="#methode" data-i18n="en3">Bewertung</a></li>
        <li><a href="reisen.html" data-i18n="nav_trip">Tanzreise</a></li>
        <li><a href="lehrer-djs.html" data-i18n="nav_tdj">Lehrer &amp; DJs</a></li>
        <li><a href="bewerbung.html" data-i18n="nav_apply">Bewerben</a></li>
      </ul>'''
B.HEADER = H0[:_a] + nav + H0[_b:]
B.HEADER = B.HEADER.replace('<a class="brand" href="index.html"', '<a class="brand" href="#top"', 1)
B.SHARED_EN = dict(B.SHARED_EN); B.SHARED_EN.update({'en1': 'Europe ranking', 'en2': 'Countries', 'en3': 'How we score'})
with contextlib.redirect_stdout(io.StringIO()):
    page('index.html', 'Beste Bachata-Schulen in Europa: Ranking 2026',
         f'Bachata-Ranking für Europa: alle {len(ALL)} Schulen in einer Liste plus ein Ranking pro Land, bisher Deutschland und Polen. Unabhängig und nicht käuflich.',
         'The best Bachata schools in Europe: ranking 2026 · Latin Dance Awards',
         f'Bachata ranking for Europe: all {len(ALL)} schools in one list plus a ranking for each country, so far Germany and Poland. Independent and not for sale.',
         '', main, t.en, hub_js, schema=[crumbs('Europa', ''), faq_schema(faq)])
print('wrote index.html (Europe hub):', len(ALL), 'schools')
