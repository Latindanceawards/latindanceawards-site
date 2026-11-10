"""Post-build fixes; run after build_en.py and before prune_en.py. Idempotent.
 1. drop pseudo-hreflang="en" alternates that point to ?lang=en (same HTML toggled by JS)
 2. de-duplicate sitemap.xml (one <url> per loc, newest lastmod wins)
 3. absolute asset/link paths in 404.html"""
import re, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PSEUDO = re.compile(r'[ \t]*<link rel="alternate" hreflang="en" href="[^"]*\?lang=en">\n?')
n = 0
for f in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    if os.path.relpath(f, ROOT).startswith(('tools/', 'automation/')): continue   # never touch template sources
    s = open(f, encoding='utf-8').read()
    t = PSEUDO.sub('', s)
    if t != s: open(f, 'w', encoding='utf-8').write(t); n += 1
print('hreflang pseudo removed on', n, 'pages')

p = os.path.join(ROOT, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
head = s[:s.index('<url>')].rstrip(' \n') + '\n'
blocks = re.findall(r'  <url>.*?</url>\n', s, re.S)
best = {}; order = []
for b in blocks:
    b = re.sub(r'[ \t]*<xhtml:link rel="alternate" hreflang="en" href="[^"]*\?lang=en"/>\n', '', b)
    loc = re.search(r'<loc>(.*?)</loc>', b).group(1)
    lm = (re.search(r'<lastmod>(.*?)</lastmod>', b) or [None, ''])[1]
    if loc not in best: order.append(loc); best[loc] = (lm, b)
    else:
        old = best[loc]
        if (lm, b.count('xhtml:link')) > (old[0], old[1].count('xhtml:link')): best[loc] = (lm, b)
out = head + ''.join(best[l][1] for l in order) + '</urlset>\n'
open(p, 'w', encoding='utf-8').write(out)
print('sitemap', len(blocks), '->', len(order))

p = os.path.join(ROOT, '404.html'); s = open(p, encoding='utf-8').read()
t = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|tel:|data:|javascript:)', r'\1="/', s)
t = t.replace('url(fonts/', 'url(/fonts/')
if t != s: open(p, 'w', encoding='utf-8').write(t); print('404 fixed')

# 4. thin-page tiering for the national sections: city pages that list <= 2 schools are
#    near-duplicates of their school pages -> noindex,follow, out of sitemap.xml and llms.txt
DIRS = {'es':'escuelas','fr':'ecoles','it':'scuole','uk':'schools','pl':'szkoly','nl':'scholen','pt':'escolas',
        'at':'schools','ch':'schools','be':'schools','ie':'schools','ee':'schools','em':'schools','nd':'schools'}
KEEP = {'es/clases-de-bachata-valencia.html','es/clases-de-bachata-sevilla.html','ee/bachata-classes-sofia.html','es/clases-de-bachata-madrid.html','es/clases-de-bachata-barcelona.html','uk/bachata-classes-london.html','fr/cours-de-bachata-paris.html','es/bachata-valencia.html','es/bachata-sevilla.html','es/bachata-dos-hermanas.html','ee/bachata-sofia.html'}
thin = []
for c, d in DIRS.items():
    for f in sorted(glob.glob(os.path.join(ROOT, c, '*.html'))):
        rel = os.path.relpath(f, ROOT)
        s = open(f, encoding='utf-8').read()
        if rel in KEEP: continue
        if 'content="noindex' in s[:3000]: thin.append(rel); continue
        m = re.search(r'<main.*?</main>', s, re.S)
        links = set(re.findall(r'href="/%s/%s/([^"#?]+)' % (c, d), m.group(0) if m else s))
        if 1 <= len(links) <= 2:
            t = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex,follow">', s, count=1)
            if t != s: open(f, 'w', encoding='utf-8').write(t); thin.append(rel)
if thin:
    p = os.path.join(ROOT, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
    for rel in thin:
        loc = 'https://latindanceawards.com/' + rel[:-5]
        s = re.sub(r'  <url>\n    <loc>%s</loc>.*?</url>\n' % re.escape(loc), '', s, flags=re.S)
    open(p, 'w', encoding='utf-8').write(s)
    p = os.path.join(ROOT, 'llms.txt'); L = open(p, encoding='utf-8').read().split('\n')
    gone = {'https://latindanceawards.com/' + r[:-5] for r in thin}
    L = [l for l in L if not any(l.endswith('(%s)' % g) for g in gone)]
    open(p, 'w', encoding='utf-8').write('\n'.join(L))
print('thin pages newly noindexed:', len(thin))
for r in thin: 
    if not os.path.basename(r).startswith('bachata-'): print('  check', r)

# 5. titles: <= 60 characters, and EN pages must not repeat their DE twin's title
SUFFIX = {'reviews and rating': 'reviews', 'reseñas y valoración': 'reseñas', 'avis et note': 'avis',
          'recensioni e valutazione': 'recensioni', 'avaliações e pontuação': 'avaliações'}
def set_title(s, new):
    s = re.sub(r'<title>.*?</title>', lambda m: '<title>%s</title>' % new, s, count=1)
    for pat in (r'(<meta property="og:title" content=")[^"]*(")', r'(<meta name="twitter:title" content=")[^"]*(")'):
        s = re.sub(pat, lambda m: m.group(1) + new + m.group(2), s, count=1)
    return s
tn = 0
titles = {}
for f in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(('tools/', 'automation/')): continue
    s = open(f, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', s)
    if not m: continue
    t = m.group(1); new = t
    if len(t) > 60 and ' · ' in t:
        head, _, suf = t.rpartition(' · ')
        new = head + ' · ' + SUFFIX[suf] if suf in SUFFIX else head
    if rel.startswith('en/') and os.path.exists(os.path.join(ROOT, rel[3:])):
        de = re.search(r'<title>(.*?)</title>', open(os.path.join(ROOT, rel[3:]), encoding='utf-8').read())
        if de and de.group(1) == new:
            nm, _, city = new.partition(' · ')
            alt = '%s reviews · %s' % (nm, city) if city else new + ' (EN)'
            new = alt if len(alt) <= 60 else '%s · %s (EN)' % (nm, city)
    if new != t:
        open(f, 'w', encoding='utf-8').write(set_title(s, new)); tn += 1
print('titles changed:', tn)

# 6. heading levels: h1 -> h3 jumps on the community pages become h2 (same look)
for rel in ('reisen.html', 'lehrer-djs.html', 'en/reisen.html', 'en/lehrer-djs.html'):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read()
    m = re.search(r'<main.*?</main>', s, re.S)
    if not m or '<h3' not in m.group(0): continue
    body = re.sub(r'<h3(?=[ >])', '<h2', m.group(0)); body = body.replace('</h3>', '</h2>')
    s = s[:m.start()] + body + s[m.end():]
    if '.tp .box h2{' not in s:
        s = s.replace('</style>', '.tp .box h2{font-family:var(--serif);font-weight:500;font-size:22px;margin-bottom:10px}</style>', 1)
    open(p, 'w', encoding='utf-8').write(s); print('headings fixed', rel)

# 7. crawlable language links DE <-> EN (the switcher is JS only, so the en/ tree had no inbound links)
LANGLINK = '<p class="xlang" style="text-align:center;margin:0;padding:0 16px 24px;font-size:.9em;opacity:.8"><a href="%s" hreflang="%s" lang="%s">%s</a></p>\n'
ln = 0
for f in glob.glob(os.path.join(ROOT, 'en', '**', '*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT); de = os.path.join(ROOT, rel[3:]) if rel != 'en/index.html' else os.path.join(ROOT, 'index.html')
    if not os.path.exists(de): continue
    for path, href, hl, label in ((f, '/' + rel[:-5].replace('en/index', 'en/'), 'en', None), (de, None, 'de', None)):
        pass
    en_url = '/' + (rel[:-5] if not rel.endswith('index.html') else rel[:-10])
    de_rel = os.path.relpath(de, ROOT)
    de_url = '/' if de_rel == 'index.html' else '/' + de_rel[:-5]
    for path, href, hl, label in ((de, en_url, 'en', 'English version'), (f, de_url, 'de', 'Deutsche Version')):
        s = open(path, encoding='utf-8').read()
        if 'class="xlang"' in s or '</footer>' not in s: continue
        s = s.replace('</footer>', LANGLINK % (href, hl, hl, label) + '</footer>', 1)
        open(path, 'w', encoding='utf-8').write(s); ln += 1
print('language links added:', ln)

# 8. short school-page meta descriptions (< 120 chars): add one neutral, true clause (page shows rating + reviews)
TAIL = {'en': ' Google rating and review data included.', 'fr': ' Note Google et avis inclus.', 'nl': ' Inclusief Google-score en reviews.'}
dn = 0
for f in glob.glob(os.path.join(ROOT, '*', 'schools', '*.html')) + glob.glob(os.path.join(ROOT, '*', 'ecoles', '*.html')) + glob.glob(os.path.join(ROOT, '*', 'scholen', '*.html')):
    rel = os.path.relpath(f, ROOT)
    s = open(f, encoding='utf-8').read()
    if 'content="noindex' in s[:3000]: continue
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not m or len(m.group(1)) >= 120: continue
    lang = 'fr' if rel.startswith('fr/') else 'nl' if rel.startswith('nl/') else 'en'
    new = m.group(1) + TAIL[lang]
    if len(new) > 158: continue
    for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")', r'(<meta name="twitter:description" content=")[^"]*(")'):
        s = re.sub(pat, lambda mm: mm.group(1) + new + mm.group(2), s, count=1)
    open(f, 'w', encoding='utf-8').write(s); dn += 1
print('meta descriptions extended:', dn)
