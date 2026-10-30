#!/usr/bin/env python3
"""Post-build step: give every school profile page a plain internal link from its city page.
City pages list schools with an external (nofollow) link to the school's own site. This links the
school NAME to our profile page (list item + card heading) and keeps the external 'school website'
link in the card. Idempotent. Run after build scripts and BEFORE clean_urls.py (or after; both work)."""
import os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'tools', '.git', 'automation', 'node_modules', 'fonts'}
def rd(p): return open(p, encoding='utf-8').read()

# 1. index school profile pages: name -> [(url path, {external hrefs})]
idx = {}
for d, dirs, files in os.walk(ROOT):
    rel = os.path.relpath(d, ROOT)
    if rel == '.' or rel.split(os.sep)[0] in SKIP: continue
    for f in files:
        if not f.endswith('.html'): continue
        s = rd(os.path.join(d, f))
        if 'id="sp-title"' not in s: continue
        m = re.search(r'<h1 id="sp-title">(.*?)</h1>', s, re.S)
        if not m: continue
        name = html.unescape(re.sub('<[^>]+>', '', m.group(1))).strip()
        ext = {html.unescape(x).rstrip('/') for x in re.findall(r'href="(https?://[^"]+)"', s)}
        url = '/' + os.path.join(rel, f)[:-5].replace(os.sep, '/')
        idx.setdefault(name, []).append((url, ext))

def pick(name, ext, city_dir):
    c = idx.get(html.unescape(name).strip())
    if not c: return None
    c = [x for x in c if x[0].startswith('/' + city_dir + '/')] if city_dir else c
    if len(c) == 1: return c[0][0]
    e = html.unescape(ext).rstrip('/')
    m = [x for x in c if e in x[1]]
    return m[0][0] if len(m) == 1 else None

LI = re.compile(r'(<li><b>\d+</b>)<a href="(https?://[^"]+)" rel="nofollow noopener" target="_blank">([^<]*)</a>')
ART = re.compile(r'<article><h3>([^<]+)</h3>(.*?)<a href="(https?://[^"]+)" rel="nofollow noopener"', re.S)
changed = linked = missed = 0
for d, dirs, files in os.walk(ROOT):
    rel = os.path.relpath(d, ROOT)
    top = rel.split(os.sep)[0]
    if top in SKIP: continue
    if os.sep in rel: continue  # only city pages directly in the country dir (or root)
    cdir = '' if rel == '.' else rel
    for f in files:
        if not (f.startswith('bachata-') and f.endswith('.html')): continue
        p = os.path.join(d, f); s = rd(p); o = s
        def li(m):
            global linked, missed
            u = pick(m.group(3), m.group(2), cdir)
            if not u: missed += 1; return m.group(0)
            linked += 1; return f'{m.group(1)}<a href="{u}">{m.group(3)}</a>'
        s = LI.sub(li, s)
        def art(m):
            global linked, missed
            u = pick(m.group(1), m.group(3), cdir)
            if not u: missed += 1; return m.group(0)
            linked += 1
            return f'<article><h3><a href="{u}" style="color:inherit;font-weight:inherit">{m.group(1)}</a></h3>{m.group(2)}<a href="{m.group(3)}" rel="nofollow noopener"'
        s = ART.sub(art, s)
        if s != o: open(p, 'w', encoding='utf-8').write(s); changed += 1
print(f'link_schools: {changed} city pages changed, {linked} links added, {missed} unmatched')
