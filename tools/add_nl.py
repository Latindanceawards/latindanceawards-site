# usage: python3 tools/add_nl.py '<cities json {key:name}>' '<schools json [[name,city,rating,reviews,url|"MAPS"],...]>'
# Adds cities/schools to netherlands_data.py, sitemap.xml and llms.txt. "MAPS" as url = Google Maps search link (school without own site).
import re, sys, json
sys.path.insert(0, 'tools')
cities, schools = json.loads(sys.argv[1]), json.loads(sys.argv[2])
p = 'tools/netherlands_data.py'; s = open(p).read()
cl = ''.join(f" {k!r}: ({v!r}, {v!r}, {('in ' + v)!r}),\n" for k, v in cities.items() if f"'{k}':" not in s)
s = s.replace("\n}\ndef _m(", "\n" + cl + "}\ndef _m(", 1)
city_name = lambda k: cities.get(k) or re.search(rf"'{k}': \('([^']+)'", s).group(1)
rows = ''
for n, c, r, v, u in schools:
    if f"({n!r}," in s: continue
    uu = f"_m({n!r}, {city_name(c)!r})" if u == 'MAPS' else repr(u)
    rows += f" ({n!r}, {c!r}, {r}, {v}, {uu}),\n"
i = s.index("\n]\n# Scoring data"); s = s[:i + 1] + rows + s[i + 1:]
open(p, 'w').write(s)
import netherlands_data as S, rank_variant as RV, collections
sl = collections.Counter(RV.pl_slug(x[0]) for x in S.SCHOOLS); dup = [k for k, v in sl.items() if v > 1]
assert not dup, dup
sm = open('sitemap.xml').read(); l = open('llms.txt').read()
def blk(path):
    u = 'https://latindanceawards.com/' + path
    return f'  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-10-27</lastmod>\n    <priority>0.8</priority>\n    <xhtml:link rel="alternate" hreflang="nl" href="{u}"/>\n    <xhtml:link rel="alternate" hreflang="en" href="{u}?lang=en"/>\n    <xhtml:link rel="alternate" hreflang="x-default" href="{u}"/>\n  </url>\n'
add = ''
for k in S.CITIES:
    path = f'nl/bachata-{k}.html'
    if '/' + path + '</loc>' not in sm: add += blk(path)
for x in S.SCHOOLS:
    loc = f'https://latindanceawards.com/nl/scholen/{RV.pl_slug(x[0])}.html'
    if loc not in sm: add += f'  <url><loc>{loc}</loc></url>\n'
open('sitemap.xml', 'w').write(sm.replace('</urlset>', add + '</urlset>'))
n, c = len(S.SCHOOLS), len(S.CITIES)
l = re.sub(r'Ranglijst van bachata-dansscholen in Nederland: \d+ scholen in \d+ steden', f'Ranglijst van bachata-dansscholen in Nederland: {n} scholen in {c} steden', l)
idx = '- [De beste bachata-dansscholen van Nederland: ranglijst 2027](https://latindanceawards.com/nl/): Ranglijst van bachata-dansscholen in Nederland: 0 scholen in 0 steden, met scores, punten en methode. Resultaten in het voorjaar van 2027. Onafhankelijk en niet te koop.'
if 'latindanceawards.com/nl/)' not in l:
    lastes = [x for x in l.split('\n') if 'fr/bachata-' in x][-1]
    l = l.replace(lastes, lastes + '\n' + idx, 1)
l = re.sub(r'Ranglijst van bachata-dansscholen in Nederland: \d+ scholen in \d+ steden', f'Ranglijst van bachata-dansscholen in Nederland: {n} scholen in {c} steden', l)
its = [x for x in l.split('\n') if 'nl/bachata-' in x]
last = its[-1] if its else [x for x in l.split('\n') if 'latindanceawards.com/nl/)' in x][-1]
new = ''.join(f'\n- [Bachata {v[0]}: de beste dansscholen 2027](https://latindanceawards.com/nl/bachata-{k}.html)' for k, v in S.CITIES.items() if f'nl/bachata-{k}.html' not in l)
l = l.replace(last, last + new, 1); open('llms.txt', 'w').write(l)
print('schools', n, 'cities', c)
