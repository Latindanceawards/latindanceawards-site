# usage: python3 tools/add_pl.py  (reads ADD list below via argv json) – adds cities/schools, sitemap, llms
import re, sys, json
sys.path.insert(0, 'tools')
cities, schools = json.loads(sys.argv[1]), json.loads(sys.argv[2])
p = 'tools/poland_data.py'; s = open(p).read()
for k, (a, b, c) in cities.items():
    if f"'{k}':" not in s:
        s = s.replace("'siedlce': ('Siedlce', 'Siedlce', 'Siedlcach'),", f"'siedlce': ('Siedlce', 'Siedlce', 'Siedlcach'), '{k}': ('{a}', '{b}', '{c}'),", 1)
a = s.index(" ('Baila Studio Tańca'"); e = s.index("\n", a) + 1
s = s[:e] + ''.join(f" ({n!r}, {c!r}, {r}, {v}, {u!r}),\n" for n, c, r, v, u in schools) + s[e:]
open(p, 'w').write(s)
sm = open('sitemap.xml').read()
blk = re.search(r'  <url>\s*<loc>https://latindanceawards.com/pl/bachata-bielsko-biala.html</loc>.*?</url>\n', sm, re.S).group(0)
l = open('llms.txt').read(); ln = [x for x in l.split('\n') if 'bachata-bielsko-biala' in x][0]
for k, (a, b, c) in cities.items():
    if f'bachata-{k}.html' not in sm: sm = sm.replace('</urlset>', blk.replace('bielsko-biala', k) + '</urlset>')
    if f'bachata-{k}.html' not in l: l = l.replace(ln, ln + '\n' + ln.replace('Bielsko-Biała', a).replace('bielsko-biala', k))
import rank_variant as RV, importlib, poland_data as P
importlib.reload(P)
have = set(re.findall(r'/pl/szkoly/([^<]+)\.html', sm))
sm = sm.replace('</urlset>', ''.join(f'  <url><loc>https://latindanceawards.com/pl/szkoly/{RV.pl_slug(x[0])}.html</loc></url>\n' for x in P.SCHOOLS if RV.pl_slug(x[0]) not in have) + '</urlset>')
open('sitemap.xml', 'w').write(sm); open('llms.txt', 'w').write(l)
