# On-page SEO audit, score out of 100 per page. Usage: python3 tools/seo_audit.py
import re, os, json, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {  # page: (main keyword, target word count from competitor research or 0)
    'index.html': ('Bachata Awards', 0),
    'rankings.html': ('beste Bachata-Schulen Deutschland', 960),
    'bewerbung.html': ('Bachata-Schule anmelden', 0),
    'bachata-berlin.html': ('Bachata Berlin', 900),
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
    internal = set(re.findall(r'href="((?:/|)(?:index|rankings|bewerbung|bachata-[a-z]+)\.html[^"]*)"', s))
    outbound = re.findall(r'<a [^>]*href="https://(?!latindanceawards\.com)[^"]+"[^>]*rel="noopener"', s)
    url = 'https://latindanceawards.com/' + ('' if page == 'index.html' else page)
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
        ('2+ internal links to other pages', 4, len({re.sub(r'[#?].*', '', x).lstrip('/') for x in internal} - {page}) >= 2, f'{len(internal)}'),
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
