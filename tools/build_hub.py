# Builds the Europe hub = homepage (index.html): one overall ranking plus a block per country.
# Run after build.py, build_guides.py and build_pl.py:  python3 tools/build_hub.py
import os, sys, re, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import poland_data as P
import spain_data as SP
import italy_data as IT
import portugal_data as PT
import france_data as FR
import netherlands_data as NL
import uk_data as UK
import belgium_data as BEX
import ireland_data as IEX
import austria_data as ATX
import switzerland_data as CHX
import easterneurope_data as EEX
import nordics_data as NDX
import easternmed_data as EMX
from build import T, page, crumbs, faq_schema, ICON, ROOT
import rank_variant as RV
DE_FULL = {e['name']: RV.total(e) for es in RV.german_entries().values() for e in es}
PL_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(P).values() for e in es}
ES_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(SP, '/es/escuelas/').values() for e in es}
IT_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(IT, '/it/scuole/').values() for e in es}
PT_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(PT, '/pt/escolas/').values() for e in es}
BE_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(BEX, '/be/schools/').values() for e in es}
IE_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(IEX, '/ie/schools/').values() for e in es}
AT_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(ATX, '/at/schools/').values() for e in es}
CH_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(CHX, '/ch/schools/').values() for e in es}
EE_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(EEX, '/ee/schools/').values() for e in es}
ND_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(NDX, '/nd/schools/').values() for e in es}
EM_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(EMX, '/em/schools/').values() for e in es}
UK_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(UK, '/uk/schools/').values() for e in es}
NL_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(NL, '/nl/scholen/').values() for e in es}
FR_FULL = {e['name']: RV.total(e) for es in RV.polish_entries(FR, '/fr/ecoles/').values() for e in es}

def f1(x): return f'{x:.1f}'.replace('.', ',')
def _num(x): return float(x.replace(',', '.'))

def de_rows():
    out = []
    for e in B.SCH:
        m = re.match(r'([\d,]+) ★ · ([\d.]+)', (e['fx'][0] if e.get('fx') else '').replace('\xa0', ' '))
        cn = B.CITY_NAMES.get(e['city'], (e['city'].title(), e['city'].title()))
        if m:
            r, v = _num(m.group(1)), int(m.group(2).replace('.', ''))
            out.append(dict(name=e['name'], cc='de', city=cn[0], r=r, v=v, pts=DE_FULL[e['name']], href=f'/schools/{e["slug"]}.html'))
        else:
            out.append(dict(name=e['name'], cc='de', city=cn[0], r=None, v=0, pts=0.0, href=f'/schools/{e["slug"]}.html'))
    return out

def pl_rows():
    return [dict(name=s[0], cc='pl', city=P.CITIES[s[1]][0], r=s[2], v=s[3], pts=PL_FULL[s[0]], href=f'/pl/bachata-{s[1]}.html') for s in P.SCHOOLS]

def es_rows():
    return [dict(name=s[0], cc='es', city=SP.CITIES[s[1]][0], r=s[2], v=s[3], pts=ES_FULL[s[0]], href=f'/es/bachata-{s[1]}.html') for s in SP.SCHOOLS]

def it_rows():
    return [dict(name=s[0], cc='it', city=IT.CITIES[s[1]][0], r=s[2], v=s[3], pts=IT_FULL[s[0]], href=f'/it/bachata-{s[1]}.html') for s in IT.SCHOOLS]

def pt_rows():
    return [dict(name=s[0], cc='pt', city=PT.CITIES[s[1]][0], r=s[2], v=s[3], pts=PT_FULL[s[0]], href=f'/pt/bachata-{s[1]}.html') for s in PT.SCHOOLS]

def fr_rows():
    return [dict(name=s[0], cc='fr', city=FR.CITIES[s[1]][0], r=s[2], v=s[3], pts=FR_FULL[s[0]], href=f'/fr/bachata-{s[1]}.html') for s in FR.SCHOOLS]

def nl_rows():
    return [dict(name=s[0], cc='nl', city=NL.CITIES[s[1]][0], r=s[2], v=s[3], pts=NL_FULL[s[0]], href=f'/nl/bachata-{s[1]}.html') for s in NL.SCHOOLS]

def uk_rows():
    return [dict(name=s[0], cc='uk', city=UK.CITIES[s[1]][0], r=s[2], v=s[3], pts=UK_FULL[s[0]], href=f'/uk/bachata-{s[1]}.html') for s in UK.SCHOOLS]

def be_rows():
    return [dict(name=s[0], cc='be', city=BEX.CITIES[s[1]][0], r=s[2], v=s[3], pts=BE_FULL[s[0]], href=f'/be/bachata-{s[1]}.html') for s in BEX.SCHOOLS]

def ie_rows():
    return [dict(name=s[0], cc='ie', city=IEX.CITIES[s[1]][0], r=s[2], v=s[3], pts=IE_FULL[s[0]], href=f'/ie/bachata-{s[1]}.html') for s in IEX.SCHOOLS]

def at_rows():
    return [dict(name=s[0], cc='at', city=ATX.CITIES[s[1]][0], r=s[2], v=s[3], pts=AT_FULL[s[0]], href=f'/at/bachata-{s[1]}.html') for s in ATX.SCHOOLS]

def ch_rows():
    return [dict(name=s[0], cc='ch', city=CHX.CITIES[s[1]][0], r=s[2], v=s[3], pts=CH_FULL[s[0]], href=f'/ch/bachata-{s[1]}.html') for s in CHX.SCHOOLS]

def ee_rows():
    return [dict(name=s[0], cc='ee', city=EEX.CITIES[s[1]][0], r=s[2], v=s[3], pts=EE_FULL[s[0]], href=f'/ee/bachata-{s[1]}.html') for s in EEX.SCHOOLS]

def nd_rows():
    return [dict(name=s[0], cc='nd', city=NDX.CITIES[s[1]][0], r=s[2], v=s[3], pts=ND_FULL[s[0]], href=f'/nd/bachata-{s[1]}.html') for s in NDX.SCHOOLS]

def em_rows():
    return [dict(name=s[0], cc='em', city=EMX.CITIES[s[1]][0], r=s[2], v=s[3], pts=EM_FULL[s[0]], href=f'/em/bachata-{s[1]}.html') for s in EMX.SCHOOLS]

NCTRY = 12 + len(set(EEX.COUNTRY.values())) + len(set(NDX.COUNTRY.values())) + len(set(EMX.COUNTRY.values()))
ALL = sorted(de_rows() + pl_rows() + es_rows() + it_rows() + pt_rows() + fr_rows() + nl_rows() + uk_rows() + be_rows() + ie_rows() + at_rows() + ch_rows() + ee_rows() + nd_rows() + em_rows(), key=lambda x: (-x['pts'], x['name']))
ND = sum(1 for x in ALL if x['cc'] == 'de'); NP = sum(1 for x in ALL if x['cc'] == 'pl'); NS = sum(1 for x in ALL if x['cc'] == 'es'); NI = sum(1 for x in ALL if x['cc'] == 'it'); NPT = sum(1 for x in ALL if x['cc'] == 'pt'); NF = sum(1 for x in ALL if x['cc'] == 'fr'); NN = sum(1 for x in ALL if x['cc'] == 'nl'); NU = sum(1 for x in ALL if x['cc'] == 'uk'); NBE = sum(1 for x in ALL if x['cc'] == 'be'); NIE = sum(1 for x in ALL if x['cc'] == 'ie'); NAT = sum(1 for x in ALL if x['cc'] == 'at'); NCH = sum(1 for x in ALL if x['cc'] == 'ch'); NEE = sum(1 for x in ALL if x['cc'] == 'ee'); NND = sum(1 for x in ALL if x['cc'] == 'nd'); NEM = sum(1 for x in ALL if x['cc'] == 'em')
NCD = 121; NC = len(P.CITIES); NCS = len(SP.CITIES); NCI = len(IT.CITIES); NCPT = len(PT.CITIES); NCF = len(FR.CITIES); NCN = len(NL.CITIES); NCU = len(UK.CITIES); NCBE = len(BEX.CITIES); NCIE = len(IEX.CITIES); NCAT = len(ATX.CITIES); NCCH = len(CHX.CITIES); NCEE = len(EEX.CITIES); NCND = len(NDX.CITIES); NCEM = len(EMX.CITIES)
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
            f'<em>{x["city"]} · {flag}</em><span>' + (f'{f1(x["pts"])} / 100 · {f1(x["r"])} ★ ({x["v"]})' if x['r'] else 'keine Google-Bewertung') + '</span></li>')

def top3(cc):
    xs = [x for x in ALL if x['cc'] == cc][:3]
    return '<ol class="top">' + ''.join(f'<li><b>{i}</b><a href="{x["href"]}">{x["name"]}</a><span>{f1(x["pts"])} / 100</span></li>' for i, x in enumerate(xs, 1)) + '</ol>'

rows = ''.join(row(i, x) for i, x in enumerate(ALL, 1))

faq = [
 ('Wie entsteht das Europa-Ranking?', 'How is the Europe ranking built?',
  'Jedes Land bekommt ein eigenes Ranking, und das Europa-Ranking führt alle Schulen zusammen. Überall gilt dieselbe Wertung: neun Kriterien, 100 Punkte, Daten aus Google Maps, von den Schulwebseiten und von Instagram. Was sich nicht bestätigen lässt, zählt mit dem niedrigsten Wert.',
  'Each country gets its own ranking, and the Europe ranking brings all schools together. The same scoring applies everywhere: nine factors, 100 points, with data from Google Maps, the schools’ websites and Instagram. Anything that cannot be confirmed counts at the lowest value.'),
 ('Kann eine Schule für einen besseren Platz bezahlen?', 'Can a school pay for a better place?',
  'Nein. Die Rankings basieren auf öffentlichen Daten und sind nicht käuflich. Anmelden ist kostenlos.', 'No. The rankings are based on public data and cannot be bought. Applying is free.'),
 ('Wann erscheinen die Ergebnisse?', 'When are the results published?',
  'Deutschland am 20. Dezember 2026 um 19 Uhr, Polen, Spanien, Italien, Portugal, Frankreich, die Niederlande, das Vereinigte Königreich, Belgien, Irland, Österreich, die Schweiz, Osteuropa, Skandinavien und Mittelmeer im Frühjahr 2027. Weitere Länder folgen.', 'Germany on December 20, 2026 at 7 pm, Poland, Spain, Italy, Portugal, France, the Netherlands, the UK, Belgium, Ireland, Austria, Switzerland, Eastern Europe, Nordics and Eastern Mediterranean in spring 2027. More countries follow.'),
 ('Wie kommt meine Schule ins Ranking?', 'How does my school get into the ranking?',
  'Melde sie kostenlos an. Wir nehmen jede Schule auf, die nachweislich Bachata unterrichtet, auch ohne Anmeldung.', 'Enter it for free. We include every school that demonstrably teaches Bachata, even without an application.'),
]
faq_html = ('<section class="block alt" id="faq"><div class="wrap"><div class="sec-head">' + t("h2", 'Häufige Fragen', 'Frequently asked questions') + '</div><div class="faq">'
            + ''.join(f'<details>{t("summary", q, qe)}{t("p", a, ae)}</details>' for q, qe, a, ae in faq) + '</div></div></section>')

hero_html = hero(('Europa · Bachata Awards', 'Europe · Bachata Awards'),
  ('Beste Bachata-Schulen in Europa: das Ranking', 'The best Bachata schools in Europe: the ranking'),
  (f'Ein Ranking für ganz Europa und ein eigenes Ranking für jedes Land: {len(ALL)} Schulen in {NCTRY} Ländern, unabhängig bewertet nach öffentlichen Daten.',
   f'One ranking for all of Europe and a separate ranking for each country: {len(ALL)} schools in {NCTRY} countries, scored independently from public data.'),
  [('cal', f'<b>{len(ALL)} Schulen</b> in {NCD + NC + NCS + NCI + NCPT + NCF + NCN + NCU + NCBE + NCIE + NCAT + NCCH + NCEE + NCND + NCEM} Städten', f'<b>{len(ALL)} schools</b> in {NCD + NC + NCS + NCI + NCPT + NCF + NCN + NCU + NCBE + NCIE + NCAT + NCCH + NCEE + NCND + NCEM} cities'),
   ('check', 'Unabhängig, <b>nicht käuflich</b>', 'Independent, <b>not for sale</b>'),
   ('clock', 'Deutschland <b>20. Dez</b> · Polen, Spanien, Italien, Portugal, Frankreich, Niederlande, UK, BE, IE, AT, CH, Osteuropa, Skandinavien, Mittelmeer <b>Frühjahr 2027</b>', 'Germany <b>Dec 20</b> · Poland, Spain, Italy, Portugal, France, Netherlands, UK, BE, IE, AT, CH, Eastern Europe, Nordics, Eastern Mediterranean <b>spring 2027</b>')],
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

DE_C = RV.german_entries(); PL_C = RV.polish_entries(P); ES_C = RV.polish_entries(SP, '/es/escuelas/'); IT_C = RV.polish_entries(IT, '/it/scuole/'); PT_C = RV.polish_entries(PT, '/pt/escolas/'); FR_C = RV.polish_entries(FR, '/fr/ecoles/'); NL_C = RV.polish_entries(NL, '/nl/scholen/'); UK_C = RV.polish_entries(UK, '/uk/schools/'); BE_C = RV.polish_entries(BEX, '/be/schools/'); IE_C = RV.polish_entries(IEX, '/ie/schools/'); AT_C = RV.polish_entries(ATX, '/at/schools/'); CH_C = RV.polish_entries(CHX, '/ch/schools/'); EE_C = RV.polish_entries(EEX, '/ee/schools/'); ND_C = RV.polish_entries(NDX, '/nd/schools/'); EM_C = RV.polish_entries(EMX, '/em/schools/')
CANDS = dict(DE_C); CANDS.update(PL_C); CANDS.update(ES_C); CANDS.update(IT_C); CANDS.update(PT_C); CANDS.update(FR_C); CANDS.update(NL_C); CANDS.update(UK_C); CANDS.update(BE_C); CANDS.update(IE_C); CANDS.update(AT_C); CANDS.update(CH_C); CANDS.update(EE_C); CANDS.update(ND_C); CANDS.update(EM_C)
TX = {k: list(v) if isinstance(v, list) else v for k, v in B.R_TEXT.items()}
TX['cities'] = {'europa': ['Ganz Europa', 'All Europe'], 'de': ['Deutschland', 'Germany'], 'pl': ['Polen', 'Poland'], 'es': ['Spanien', 'Spain'], 'it': ['Italien', 'Italy'], 'pt': ['Portugal', 'Portugal'], 'fr': ['Frankreich', 'France'], 'nl': ['Niederlande', 'Netherlands'], 'uk': ['Vereinigtes Königreich', 'United Kingdom'], 'be': ['Belgien', 'Belgium'], 'ie': ['Irland', 'Ireland'], 'at': ['Österreich', 'Austria'], 'ch': ['Schweiz', 'Switzerland'], 'ee': ['Osteuropa', 'Eastern Europe'], 'nd': ['Skandinavien', 'Nordics'], 'em': ['Mittelmeer', 'Eastern Mediterranean']}
TX['cities'].update({k: v for k, v in B.R_TEXT['cities'].items() if k != 'deutschland'})
TX['cities'].update({k: [v[0], v[1]] for k, v in P.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in SP.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in IT.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in PT.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in FR.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in NL.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in UK.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in BEX.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in IEX.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in ATX.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in CHX.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in EEX.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in NDX.CITIES.items()})
TX['cities'].update({k: [v[0], v[1]] for k, v in EMX.CITIES.items()})
TX['title_de'] = ['Beste Bachata-Schulen Europas', 'Best Bachata schools in Europe']
TX['sub_interim'] = ['Zwischenstand: Die Platzierungen können sich noch ändern, bis die Länder ihre Ergebnisse veröffentlichen.', 'Interim standing: places can still change until each country publishes its results.']
TX['help_p'] = ['Jede Schule wird nach denselben öffentlichen Kriterien bewertet, in jedem Land gleich. Platzierungen sind nicht käuflich.', 'Every school is scored on the same public criteria, identical in every country. Places cannot be bought.']
TX['note_p'] = ['Melde deine Schule kostenlos an, egal in welchem Land.', 'Enter your school for free, in any country.']
TX['vote_banner'] = ['Publikumspreis: Öffne eine Schule und stimme ab. Eine Stimme pro Person, bestätigt per E-Mail. Der Publikumspreis ist unabhängig von den Punkten, das Ergebnis kommt mit dem jeweiligen Land.', 'Audience Award: open a school and vote. One vote per person, confirmed by email. It is separate from the points, and the result comes with each country.']
TX['prelim_p'] = ['Überall gilt dieselbe Wertung: bis zu 75 Punkte für sechs Kriterien (Jahre im Unterricht, Einsteigerangebot, Events, Google-Bewertung, Anzahl der Bewertungen, Social Media) und bis zu 25 Punkte für Festivals, aktuelle Bewertungen und Wettbewerbe, die noch „zu bestätigen“ sind. Daten: Schulwebseiten, Google Maps und Instagram, Stand Oktober 2026. Was nicht bestätigt ist, zählt mit dem niedrigsten Wert. Deutschland wird am 20. Dezember 2026 final, Polen, Spanien, Italien und Portugal im Frühjahr 2027. Die Platzierungen können sich noch ändern.', 'The same scoring applies everywhere: up to 75 points for six factors (years teaching, beginner offer, events, Google rating, number of reviews, social media) and up to 25 points for festivals, recent reviews and competitions, which are still “to be confirmed”. Data: school websites, Google Maps and Instagram, status October 2026. Anything unconfirmed counts at the lowest value. Germany becomes final on December 20, 2026, Poland, Spain, Italy and Portugal in spring 2027. Positions can still change.']
TBC = ([ 'Festivals', 'Aktuelle Bewertungen', 'Teilnahme an Wettbewerben', 'Wettbewerbe gewonnen'],
       ['Festivals', 'Recent reviews', 'Competitions entered', 'Competitions won'])
MAXV = ['15', '5', '5', '5']
tbc_pairs = ([[n, m] for n, m in zip(TBC[0], MAXV)], [[n, m] for n, m in zip(TBC[1], MAXV)])
hub_js = RV.make_js('europa', {'de': list(DE_C), 'pl': list(PL_C), 'es': list(ES_C), 'it': list(IT_C), 'pt': list(PT_C), 'fr': list(FR_C), 'nl': list(NL_C), 'uk': list(UK_C), 'be': list(BE_C), 'ie': list(IE_C), 'at': list(AT_C), 'ch': list(CH_C), 'ee': list(EE_C), 'nd': list(ND_C), 'em': list(EM_C)}, TX, CANDS, ['europa', 'de', 'pl', 'es', 'it', 'pt', 'fr', 'nl', 'uk', 'be', 'ie', 'at', 'ch', 'ee', 'nd', 'em'], 100, extra={'tbc': tbc_pairs})
tabs = RV.tabs_html(t, [('europa', 'Ganz Europa', 'All Europe'), ('de', 'Deutschland', 'Germany'), ('pl', 'Polen', 'Poland'), ('es', 'Spanien', 'Spain'), ('it', 'Italien', 'Italy'), ('pt', 'Portugal', 'Portugal'), ('fr', 'Frankreich', 'France'), ('nl', 'Niederlande', 'Netherlands'), ('uk', 'Vereinigtes Königreich', 'United Kingdom'), ('be', 'Belgien', 'Belgium'), ('ie', 'Irland', 'Ireland'), ('at', 'Österreich', 'Austria'), ('ch', 'Schweiz', 'Switzerland'), ('ee', 'Osteuropa', 'Eastern Europe'), ('nd', 'Skandinavien', 'Nordics'), ('em', 'Mittelmeer', 'Eastern Mediterranean')])
rank_section = RV.ranking_section(tabs, 'Stadt suchen …', 'Search city …', 'Länder und Städte / Countries and cities')

main = hero_html + rank_section + f'''
<section class="block" id="laender"><div class="wrap tp" style="max-width:900px">
  {t("h2", "Rankings nach Ländern", "Rankings by country")}
  <div class="people">
    <div class="box"><h3>{t("span", "Deutschland", "Germany")}</h3><p class="muted">{t("span", f"{ND} Schulen in {NCD} Städten. Ergebnisse am 20. Dezember 2026 um 19 Uhr.", f"{ND} schools in {NCD} cities. Results on December 20, 2026 at 7 pm.")}</p>{top3("de")}<div class="btnrow"><a class="btn btn-gold" href="deutschland.html">{t("span", "Land ansehen", "See the country")}</a><a class="btn btn-ghost" href="rankings.html">{t("span", "Zum Ranking", "To the ranking")}</a></div></div>
    <div class="box"><h3>{t("span", "Polen", "Poland")}</h3><p class="muted">{t("span", f"{NP} Schulen in {NC} Städten. Ergebnisse im Frühjahr 2027.", f"{NP} schools in {NC} cities. Results in spring 2027.")}</p>{top3("pl")}<div class="btnrow"><a class="btn btn-gold" href="pl/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Spanien", "Spain")}</h3><p class="muted">{t("span", f"{NS} Schulen in {NCS} Städten. Ergebnisse im Frühjahr 2027.", f"{NS} schools in {NCS} cities. Results in spring 2027.")}</p>{top3("es")}<div class="btnrow"><a class="btn btn-gold" href="es/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Italien", "Italy")}</h3><p class="muted">{t("span", f"{NI} Schulen in {NCI} Städten. Ergebnisse im Frühjahr 2027.", f"{NI} schools in {NCI} cities. Results in spring 2027.")}</p>{top3("it")}<div class="btnrow"><a class="btn btn-gold" href="it/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Portugal", "Portugal")}</h3><p class="muted">{t("span", f"{NPT} Schulen in {NCPT} Städten. Ergebnisse im Frühjahr 2027.", f"{NPT} schools in {NCPT} cities. Results in spring 2027.")}</p>{top3("pt")}<div class="btnrow"><a class="btn btn-gold" href="pt/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Frankreich", "France")}</h3><p class="muted">{t("span", f"{NF} Schulen in {NCF} Städten. Ergebnisse im Frühjahr 2027.", f"{NF} schools in {NCF} cities. Results in spring 2027.")}</p>{top3("fr")}<div class="btnrow"><a class="btn btn-gold" href="fr/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Niederlande", "Netherlands")}</h3><p class="muted">{t("span", f"{NN} Schulen in {NCN} Städten. Ergebnisse im Frühjahr 2027.", f"{NN} schools in {NCN} cities. Results in spring 2027.")}</p>{top3("nl")}<div class="btnrow"><a class="btn btn-gold" href="nl/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Vereinigtes Königreich", "United Kingdom")}</h3><p class="muted">{t("span", f"{NU} Schulen in {NCU} Städten. Ergebnisse im Frühjahr 2027.", f"{NU} schools in {NCU} cities. Results in spring 2027.")}</p>{top3("uk")}<div class="btnrow"><a class="btn btn-gold" href="uk/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Belgien", "Belgium")}</h3><p class="muted">{t("span", f"{NBE} Schulen in {NCBE} Städten. Ergebnisse im Frühjahr 2027.", f"{NBE} schools in {NCBE} cities. Results in spring 2027.")}</p>{top3("be")}<div class="btnrow"><a class="btn btn-gold" href="be/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Irland", "Ireland")}</h3><p class="muted">{t("span", f"{NIE} Schulen in {NCIE} Städten. Ergebnisse im Frühjahr 2027.", f"{NIE} schools in {NCIE} cities. Results in spring 2027.")}</p>{top3("ie")}<div class="btnrow"><a class="btn btn-gold" href="ie/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Österreich", "Austria")}</h3><p class="muted">{t("span", f"{NAT} Schulen in {NCAT} Städten. Ergebnisse im Frühjahr 2027.", f"{NAT} schools in {NCAT} cities. Results in spring 2027.")}</p>{top3("at")}<div class="btnrow"><a class="btn btn-gold" href="at/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Schweiz", "Switzerland")}</h3><p class="muted">{t("span", f"{NCH} Schulen in {NCCH} Städten. Ergebnisse im Frühjahr 2027.", f"{NCH} schools in {NCCH} cities. Results in spring 2027.")}</p>{top3("ch")}<div class="btnrow"><a class="btn btn-gold" href="ch/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Osteuropa", "Eastern Europe")}</h3><p class="muted">{t("span", f"{NEE} Schulen in {NCEE} Städten. Ergebnisse im Frühjahr 2027.", f"{NEE} schools in {NCEE} cities. Results in spring 2027.")}</p>{top3("ee")}<div class="btnrow"><a class="btn btn-gold" href="ee/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Skandinavien", "Nordics")}</h3><p class="muted">{t("span", f"{NND} Schulen in {NCND} Städten. Ergebnisse im Frühjahr 2027.", f"{NND} schools in {NCND} cities. Results in spring 2027.")}</p>{top3("nd")}<div class="btnrow"><a class="btn btn-gold" href="nd/">{t("span", "Land ansehen", "See the country")}</a></div></div>
    <div class="box"><h3>{t("span", "Mittelmeer", "Eastern Mediterranean")}</h3><p class="muted">{t("span", f"{NEM} Schulen in {NCEM} Städten. Ergebnisse im Frühjahr 2027.", f"{NEM} schools in {NCEM} cities. Results in spring 2027.")}</p>{top3("em")}<div class="btnrow"><a class="btn btn-gold" href="em/">{t("span", "Land ansehen", "See the country")}</a></div></div>
  </div>
</div></section>
''' + sec(("So bewerten wir", "How we score"),
  t("p", "Jede Schule wird nach denselben öffentlichen Kriterien bewertet, in jedem Land gleich: Google-Bewertung, Zahl der Bewertungen, Jahre am Markt, Angebot für Anfänger, Veranstaltungen, Auftritt in sozialen Medien und mehr, zusammen 100 Punkte. Zurzeit zeigen wir für alle Länder denselben Zwischenstand aus zwei Kriterien. So bleibt das Europa-Ranking vergleichbar, bis jedes Land seine vollständigen Daten hat.",
        "Every school is scored on the same public factors, identical in every country: Google rating, number of reviews, years in business, beginner offer, events, social media presence and more, 100 points in total. For now we show the same interim standing from two factors for all countries. That keeps the Europe ranking comparable until every country has its full data.")
  + t("p", 'Die ausführliche Methode für Deutschland steht <a href="deutschland.html#method">hier</a>, die für Polen <a href="pl/#metoda">hier</a> die für Spanien <a href="es/#metodo">hier</a> die für Italien <a href="it/#metodo">hier</a> die für Portugal <a href="pt/#metodo">hier</a> die für Frankreich <a href="fr/#metodo">hier</a> die für die Niederlande <a href="nl/#metodo">hier</a> und die für das Vereinigte Königreich <a href="uk/#metodo">hier</a>.',
        'The detailed method for Germany is <a href="deutschland.html#method">here</a>, the one for Poland <a href="pl/#metoda">here</a>, the one for Spain <a href="es/#metodo">here</a> the one for Italy <a href="it/#metodo">here</a> the one for Portugal <a href="pt/#metodo">here</a> the one for France <a href="fr/#metodo">here</a> the one for the Netherlands <a href="nl/#metodo">here</a> and the one for the UK <a href="uk/#metodo">here</a>.'), alt=False, sid='methode') + sec(("Warum ein Ranking für ganz Europa?", "Why one ranking for all of Europe?"),
  t("p", "Wer eine gute Bachata-Schule sucht, schaut selten nur in die eigene Stadt: Auf Reisen, beim Umzug oder für ein Wochenende im Nachbarland zählt, wo es gute Kurse gibt. Das Europa-Ranking macht Schulen über Ländergrenzen hinweg vergleichbar, und die Länderseiten zeigen jeweils die beste Schule der Stadt.",
        "Anyone looking for a good Bachata school rarely looks only at their own city: when travelling, moving or planning a weekend in a neighbouring country, what matters is where the good classes are. The Europe ranking makes schools comparable across borders, and the country pages show the best school in each city."), alt=True) + faq_html + sec(
  ("Dein Land fehlt?", "Is your country missing?"),
  t("p", 'Wir starten weitere Länder Schritt für Schritt. Schreib uns an <a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a>, wenn du eine Schule betreibst oder die Szene in deinem Land kennst.',
        'We are adding more countries step by step. Email <a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a> if you run a school or know the scene in your country.'))

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
         f'Bachata-Ranking für Europa: alle {len(ALL)} Schulen in einer Liste plus Ranking pro Land ({NCTRY} Länder). Unabhängig und nicht käuflich.',
         'The best Bachata schools in Europe: ranking 2026 · Latin Dance Awards',
         f'Bachata ranking for Europe: all {len(ALL)} schools in one list plus a ranking for each country, so far Germany, Poland, Spain and Italy. Independent and not for sale.',
         '', main, t.en, hub_js, schema=[crumbs('Europa', ''), faq_schema(faq)])
print('wrote index.html (Europe hub):', len(ALL), 'schools')
