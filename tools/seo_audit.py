# On-page SEO audit, score out of 100 per page. Usage: python3 tools/seo_audit.py
import re, os, json, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {  # page: (main keyword, target word count from competitor research or 0)
    'index.html': ('Bachata Schulen Europa', 0),
    'deutschland.html': ('Bachata Awards', 0),
    'rankings.html': ('beste Bachata-Schulen Deutschland', 960),
    'bewerbung.html': ('Bachata-Schule anmelden', 0),
    'bachata-berlin.html': ('Bachata Berlin', 900),
    'bachata-hamburg.html': ('Bachata Hamburg', 900),
    'bachata-muenchen.html': ('Bachata München', 850),
    'bachata-koeln.html': ('Bachata Köln', 800),
    'bachata-frankfurt.html': ('Bachata Frankfurt', 800),
    'bachata-party-frankfurt.html': ('Bachata Party Frankfurt', 0),
    'bachata-party-koeln.html': ('Bachata Party Köln', 0),
    'bachata-party-muenchen.html': ('Bachata Party München', 0),
    'bachata-party-hamburg.html': ('Bachata Party Hamburg', 0),
    'bachata-party-berlin.html': ('Bachata Party Berlin', 0),
    'bachata-stuttgart.html': ('Bachata Stuttgart', 800),
    'bachata-duesseldorf.html': ('Bachata Düsseldorf', 800),
    'bachata-freiburg.html': ('Bachata Freiburg', 800),
    'bachata-dresden.html': ('Bachata Dresden', 800),
    'bachata-nuernberg.html': ('Bachata Nürnberg', 800),
    'bachata-bremen.html': ('Bachata Bremen', 800),
    'bachata-saarbruecken.html': ('Bachata Saarbrücken', 800),
    'bachata-gelsenkirchen.html': ('Bachata Gelsenkirchen', 800),
    'bachata-bonn.html': ('Bachata Bonn', 800),
    'bachata-kempten.html': ('Bachata Kempten', 800),
    'bachata-kassel.html': ('Bachata Kassel', 800),
    'bachata-hannover.html': ('Bachata Hannover', 800),
    'bachata-braunschweig.html': ('Bachata Braunschweig', 800),
    'bachata-heidelberg.html': ('Bachata Heidelberg', 800),
    'bachata-dortmund.html': ('Bachata Dortmund', 800),
    'bachata-kiel.html': ('Bachata Kiel', 800),
    'bachata-bochum.html': ('Bachata Bochum', 800),
    'bachata-regensburg.html': ('Bachata Regensburg', 800),
    'bachata-mannheim.html': ('Bachata Mannheim', 800),
    'bachata-wuerzburg.html': ('Bachata Würzburg', 800),
    'bachata-muenster.html': ('Bachata Münster', 800),
    'bachata-augsburg.html': ('Bachata Augsburg', 800),
    'bachata-kurs-berlin.html': ('Bachata Kurs Berlin', 800),
    'bachata-tanzschule-berlin.html': ('Bachata Tanzschule Berlin', 800),
    'bachata-oldenburg.html': ('Bachata Oldenburg', 800),
    'bachata-essen.html': ('Bachata Essen', 800),
    'bachata-karlsruhe.html': ('Bachata Karlsruhe', 800),
    'bachata-leipzig.html': ('Bachata Leipzig', 800),
    'bachata-tanzen.html': ('Bachata tanzen', 900),
    'bachata-grundschritt.html': ('Bachata Grundschritt', 800),
    'bachata-festivals-deutschland.html': ('Bachata Festival Deutschland', 850),
    'bachata-sensual.html': ('Bachata Sensual', 850),
    'bachata-dominicana.html': ('Bachata Dominicana', 850),
    'bachata-musik.html': ('Bachata Musik', 850),
    'bachata-tanzschule.html': ('Bachata Tanzschule', 850),
    'bachata-tanzkurs.html': ('Bachata Tanzkurs', 850),
    'bachata-salsa-unterschied.html': ('Salsa und Bachata', 900),
    'bachata-schritte.html': ('Bachata Schritte', 900),
    'bachata-lernen.html': ('Bachata lernen', 900),
    'bachata-workshop.html': ('Bachata Workshop', 850),
    'bachata-kurs-in-der-naehe.html': ('Bachata Kurs in der Nähe', 800),
    'bachata-solo.html': ('Bachata Solo', 800),
    'bachata-hochzeitstanz.html': ('Bachata Hochzeitstanz', 800),
    'bachata-fuer-anfaenger.html': ('Bachata für Anfänger', 850),
    'bachata-ladies-styling.html': ('Bachata Ladies Styling', 850),
    'bachata-moderna.html': ('Bachata Moderna', 850),
    'bachata-staedte-deutschland.html': ('Bachata Schulen Deutschland', 0),
    'bachata-party.html': ('Bachata Party', 850),
}
sitemap = open(os.path.join(ROOT, 'sitemap.xml')).read()
llms = open(os.path.join(ROOT, 'llms.txt')).read()

def norm(t): return re.sub(r'[\s\-–·|:]+', ' ', H.unescape(t).lower()).strip()
def toks(k): return [w[:-1] if w.endswith('s') and len(w) > 5 else w for w in norm(k).split()]
def has_kw(text, kw):
    t = norm(text)
    return all(w in t for w in toks(kw))
def text_of(h): return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()

total_ok = True
for page, (kw, target) in PAGES.items():
    s = open(os.path.join(ROOT, page), encoding='utf-8').read()
    head = s[:s.index('</head>')]
    body = s[s.index('<main'):s.index('</main>')]
    body_noscript = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', body, flags=re.S)
    words = text_of(body_noscript).split()
    title = re.search(r'<title>(.*?)</title>', head).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)"', head).group(1)
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    h2s = re.findall(r'<h2[^>]*>', body)
    levels = [int(x) for x in re.findall(r'<h([1-6])', s[s.index('<body'):])]
    skips = [f'h{a}->h{b}' for a, b in zip(levels, levels[1:]) if b > a + 1]
    schema = ' '.join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S))
    imgs = re.findall(r'<img[^>]*>', body)
    bad_imgs = [i for i in imgs if not re.search(r'alt="[^"]+"', i)]
    internal = set(re.findall(r'href="((?:/|)(?:index|rankings|bewerbung|bachata-[a-z]+)(?:\.html)?[^"]*)"', s))
    outbound = re.findall(r'<a [^>]*href="https://(?!latindanceawards\.com)[^"]+"[^>]*rel="noopener"', s)
    url = 'https://latindanceawards.com/' + ('' if page == 'index.html' else page[:-5])  # clean URL: Cloudflare redirects .html -> extensionless
    checks = [
        ('Title 30-60 chars', 8, 30 <= len(H.unescape(title)) <= 60, f'{len(H.unescape(title))} chars'),
        ('Keyword at start of title', 8, norm(title).startswith(' '.join(toks(kw))[:12]) or toks(kw)[0] in norm(title).split()[:2], title),
        ('Meta description 120-160', 7, 120 <= len(H.unescape(desc)) <= 160, f'{len(H.unescape(desc))} chars'),
        ('Keyword in meta description', 4, has_kw(desc, kw), ''),
        ('Exactly one H1', 6, len(h1s) == 1, f'{len(h1s)}'),
        ('Keyword in H1', 8, bool(h1s) and has_kw(text_of(h1s[0]), kw), text_of(h1s[0]) if h1s else ''),
        ('Keyword in first 100 words', 7, has_kw(' '.join(words[:100]), kw), ''),
        ('6+ H2 headings', 6, len(h2s) >= 6, f'{len(h2s)}'),
        ('No skipped heading levels', 4, not skips, ','.join(skips)),
        ('FAQ + FAQPage schema', 7, '"FAQPage"' in schema and '<details' in body, ''),
        ('BreadcrumbList (subpages)', 4, page == 'index.html' or '"BreadcrumbList"' in schema, ''),
        ('Canonical', 4, f'<link rel="canonical" href="{url}">' in head, ''),
        ('hreflang de/en/x-default', 4, all(f'hreflang="{l}"' in head for l in ('de', 'en', 'x-default')), ''),
        ('Open Graph title/desc/image', 4, all(f'og:{k}' in head for k in ('title', 'description', 'image')), ''),
        ('2+ internal links to other pages', 4, len({re.sub(r'(\.html)?([#?].*)?$', '', x).lstrip('/') for x in internal} - {page[:-5], page}) >= 2, f'{len(internal)}'),
        ('Authority outbound link (noopener)', 3, len(outbound) >= 1, f'{len(outbound)}'),
        ('All images have alt text', 3, not bad_imgs, f'{len(bad_imgs)} missing'),
        ('Word count vs target', 5, target == 0 or len(words) >= target, f'{len(words)} words (target {target})'),
        ('In sitemap.xml and llms.txt', 4, f'<loc>{url}</loc>' in sitemap and url in llms, ''),
    ]
    score = sum(w for _, w, ok, _ in checks if ok); maxs = sum(w for _, w, _, _ in checks)
    pct = round(score / maxs * 100)
    total_ok &= pct >= 90
    print(f'\n{page}  [{kw}]  SCORE {pct}/100  ({len(words)} words)')
    for name, w, ok, info in checks:
        print(f'  {"OK  " if ok else "FAIL"} {name:<36} {info}')
print('\nALL PAGES >= 90' if total_ok else '\nSOME PAGES BELOW 90')

# ---------- Site-wide checks: duplicates, broken internal links, orphans, page weight ----------
import collections, urllib.parse
SKIP = ('tools', 'automation', '.git', 'node_modules')
files = []
for d, dirs, fs in os.walk(ROOT):
    if os.path.relpath(d, ROOT).split(os.sep)[0] in SKIP: continue
    for f in fs:
        if f.endswith('.html') and f != 'google4c8a12ba6ad82dd8.html':
            files.append(os.path.relpath(os.path.join(d, f), ROOT))

def url_to_file(href, src):
    """Resolve an internal href (as written) to a repo file, or None if external/ignored."""
    href = href.split('#')[0].split('?')[0]
    if not href or re.match(r'^(https?:|mailto:|tel:|javascript:|data:)', href):
        if href.startswith('https://latindanceawards.com/'): href = href[len('https://latindanceawards.com/'):]
        else: return None
    base = '' if href.startswith('/') else os.path.dirname(src)
    p = os.path.normpath(os.path.join(base, href.lstrip('/')))
    if p in ('.', ''): return 'index.html'
    for c in (p, p + '.html', os.path.join(p, 'index.html')):
        if os.path.isfile(os.path.join(ROOT, c)): return c
    return False  # internal but missing

titles = collections.defaultdict(list); descs = collections.defaultdict(list)
inbound = collections.defaultdict(set); broken = []; heavy = []
for f in files:
    s = open(os.path.join(ROOT, f), encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', s); t = H.unescape(m.group(1)).strip() if m else ''
    m = re.search(r'<meta name="description" content="([^"]*)"', s); dsc = H.unescape(m.group(1)).strip() if m else ''
    if f != '404.html':  # duplicates only count within the same language tree (DE vs /en/)
        grp = 'en' if f.startswith('en' + os.sep) else 'de'
        titles[(grp, t)].append(f); descs[(grp, dsc)].append(f)
    if len(s.encode('utf-8')) > 250_000: heavy.append((f, len(s.encode('utf-8')) // 1000))
    body = re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.S)
    for h in set(re.findall(r'<a\b[^>]*?\bhref="([^"]+)"', body)):
        r = url_to_file(h, f)
        if r is None: continue
        if r is False: broken.append((f, h))
        elif r != f: inbound[r].add(f)

dup_t = {k[1]: v for k, v in titles.items() if len(v) > 1 and k[1]}
dup_d = {k[1]: v for k, v in descs.items() if len(v) > 1 and k[1]}
orphans = [f for f in files if f not in ('404.html', 'index.html', 'en/impressum.html') and not inbound.get(f)]
print('\n=== SITE-WIDE CHECKS ===')
print(f'Pages scanned: {len(files)}')
def show(label, items, fmt):
    print(f'{"OK  " if not items else "FAIL"} {label}: {len(items)}')
    for i in list(items)[:15]: print('       ' + fmt(i))
    if len(items) > 15: print(f'       ... and {len(items) - 15} more')
show('Duplicate titles', dup_t, lambda k: f'"{k[:60]}" -> {", ".join(dup_t[k][:4])}')
show('Duplicate meta descriptions', dup_d, lambda k: f'"{k[:50]}..." -> {", ".join(dup_d[k][:4])}')
show('Broken internal links', broken, lambda b: f'{b[0]} -> {b[1]}')
show('Orphan pages (no inbound link)', orphans, lambda o: o)
show('Pages over 250 KB (warning only: heavy inline CSS/JS)', heavy, lambda h: f'{h[0]} ({h[1]} KB)')
sitemap_missing = [f for f in files if f not in ('404.html',) and 'latindanceawards.com/' + (re.sub(r'(^|/)index\.html$', r'\1', f)[:-5] if f.endswith('.html') and not f.endswith('index.html') else re.sub(r'index\.html$', '', f)) not in sitemap and not f.endswith('index.html') and f != 'index.html' and f not in ('datenschutz.html', 'impressum.html', 'teilen.html', 'en/datenschutz.html', 'en/impressum.html', 'en/teilen.html')]  # legal/utility pages are intentionally unlisted
show('Pages missing from sitemap.xml (non-index)', sitemap_missing, lambda o: o)
SITE_OK = not (dup_t or dup_d or broken)
print('\nSITE-WIDE: ' + ('PASS (no duplicates or broken links)' if SITE_OK else 'ISSUES FOUND'))
