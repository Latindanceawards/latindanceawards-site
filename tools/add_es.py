# usage: python3 tools/add_es.py '<cities json {key:name}>' '<schools json [[name,city,rating,reviews,url|"MAPS"],...]>'
# Adds cities/schools to spain_data.py, sitemap.xml and llms.txt. "MAPS" as url = Google Maps search link (school without own site).
import re, sys, json
sys.path.insert(0, 'tools')
cities, schools = json.loads(sys.argv[1]), json.loads(sys.argv[2])
p = 'tools/spain_data.py'; s = open(p).read()
cl = ''.join(f" {k!r}: ({v!r}, {v!r}, {v!r}),\n" for k, v in cities.items() if f"'{k}':" not in s)
s = s.replace("\n}\ndef _m(", "\n" + cl + "}\ndef _m(", 1)
city_name = lambda k: cities.get(k) or re.search(rf"'{k}': \('([^']+)'", s).group(1)
rows = ''
for n, c, r, v, u in schools:
    if f"({n!r}," in s: continue
    uu = f"_m({n!r}, {city_name(c)!r})" if u == 'MAPS' else repr(u)
    rows += f" ({n!r}, {c!r}, {r}, {v}, {uu}),\n"
i = s.index("\n]\n# Scoring data"); s = s[:i + 1] + rows + s[i + 1:]
open(p, 'w').write(s)
import spain_data as S, rank_variant as RV, collections
sl = collections.Counter(RV.pl_slug(x[0]) for x in S.SCHOOLS); dup = [k for k, v in sl.items() if v > 1]
assert not dup, dup
sm = open('sitemap.xml').read(); l = open('llms.txt').read()
def blk(path):
    u = 'https://latindanceawards.com/' + path
    return f'  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-10-27</lastmod>\n    <priority>0.8</priority>\n    <xhtml:link rel="alternate" hreflang="es" href="{u}"/>\n    <xhtml:link rel="alternate" hreflang="en" href="{u}?lang=en"/>\n    <xhtml:link rel="alternate" hreflang="x-default" href="{u}"/>\n  </url>\n'
add = ''
for k in S.CITIES:
    path = f'es/bachata-{k}.html'
    if '/' + path + '</loc>' not in sm: add += blk(path)
for x in S.SCHOOLS:
    loc = f'https://latindanceawards.com/es/escuelas/{RV.pl_slug(x[0])}.html'
    if loc not in sm: add += f'  <url><loc>{loc}</loc></url>\n'
open('sitemap.xml', 'w').write(sm.replace('</urlset>', add + '</urlset>'))
n, c = len(S.SCHOOLS), len(S.CITIES)
l = re.sub(r'Ranking de escuelas de bachata en España: \d+ escuelas en \d+ ciudades', f'Ranking de escuelas de bachata en España: {n} escuelas en {c} ciudades', l)
last = [x for x in l.split('\n') if 'es/bachata-' in x][-1]
new = ''.join(f'\n- [Bachata {v[0]}: las mejores escuelas de baile 2027](https://latindanceawards.com/es/bachata-{k}.html)' for k, v in S.CITIES.items() if f'es/bachata-{k}.html' not in l)
l = l.replace(last, last + new, 1); open('llms.txt', 'w').write(l)
print('schools', n, 'cities', c)
