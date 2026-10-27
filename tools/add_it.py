# usage: python3 tools/add_it.py '<cities json {key:name}>' '<schools json [[name,city,rating,reviews,url|"MAPS"],...]>'
# Adds cities/schools to italy_data.py, sitemap.xml and llms.txt. "MAPS" as url = Google Maps search link (school without own site).
import re, sys, json
sys.path.insert(0, 'tools')
cities, schools = json.loads(sys.argv[1]), json.loads(sys.argv[2])
p = 'tools/italy_data.py'; s = open(p).read()
cl = ''.join(f" {k!r}: ({v!r}, {v!r}, {('a ' + v)!r}),\n" for k, v in cities.items() if f"'{k}':" not in s)
s = s.replace("\n}\ndef _m(", "\n" + cl + "}\ndef _m(", 1)
city_name = lambda k: cities.get(k) or re.search(rf"'{k}': \('([^']+)'", s).group(1)
rows = ''
for n, c, r, v, u in schools:
    if f"({n!r}," in s: continue
    uu = f"_m({n!r}, {city_name(c)!r})" if u == 'MAPS' else repr(u)
    rows += f" ({n!r}, {c!r}, {r}, {v}, {uu}),\n"
i = s.index("\n]\n# Scoring data"); s = s[:i + 1] + rows + s[i + 1:]
open(p, 'w').write(s)
import italy_data as S, rank_variant as RV, collections
sl = collections.Counter(RV.pl_slug(x[0]) for x in S.SCHOOLS); dup = [k for k, v in sl.items() if v > 1]
assert not dup, dup
sm = open('sitemap.xml').read(); l = open('llms.txt').read()
def blk(path):
    u = 'https://latindanceawards.com/' + path
    return f'  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-10-27</lastmod>\n    <priority>0.8</priority>\n    <xhtml:link rel="alternate" hreflang="it" href="{u}"/>\n    <xhtml:link rel="alternate" hreflang="en" href="{u}?lang=en"/>\n    <xhtml:link rel="alternate" hreflang="x-default" href="{u}"/>\n  </url>\n'
add = ''
for k in S.CITIES:
    path = f'it/bachata-{k}.html'
    if '/' + path + '</loc>' not in sm: add += blk(path)
for x in S.SCHOOLS:
    loc = f'https://latindanceawards.com/it/scuole/{RV.pl_slug(x[0])}.html'
    if loc not in sm: add += f'  <url><loc>{loc}</loc></url>\n'
open('sitemap.xml', 'w').write(sm.replace('</urlset>', add + '</urlset>'))
n, c = len(S.SCHOOLS), len(S.CITIES)
l = re.sub(r'Classifica delle scuole di bachata in Italia: \d+ scuole in \d+ città', f'Classifica delle scuole di bachata in Italia: {n} scuole in {c} città', l)
idx = '- [Le migliori scuole di bachata d’Italia: classifica 2027](https://latindanceawards.com/it/): Classifica delle scuole di bachata in Italia: 0 scuole in 0 città, con valutazioni, punti e metodo. Risultati in primavera 2027. Indipendente e non si compra.'
if 'latindanceawards.com/it/)' not in l:
    lastes = [x for x in l.split('\n') if 'es/bachata-' in x][-1]
    l = l.replace(lastes, lastes + '\n' + idx, 1)
l = re.sub(r'Classifica delle scuole di bachata in Italia: \d+ scuole in \d+ città', f'Classifica delle scuole di bachata in Italia: {n} scuole in {c} città', l)
its = [x for x in l.split('\n') if 'it/bachata-' in x]
last = its[-1] if its else [x for x in l.split('\n') if 'latindanceawards.com/it/)' in x][-1]
new = ''.join(f'\n- [Bachata {v[0]}: le migliori scuole di ballo 2027](https://latindanceawards.com/it/bachata-{k}.html)' for k, v in S.CITIES.items() if f'it/bachata-{k}.html' not in l)
l = l.replace(last, last + new, 1); open('llms.txt', 'w').write(l)
print('schools', n, 'cities', c)
