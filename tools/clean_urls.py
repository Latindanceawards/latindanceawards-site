#!/usr/bin/env python3
"""Post-build step: make every URL signal match what Cloudflare Pages actually serves.
Cloudflare 308-redirects /x.html -> /x and /dir/index.html -> /dir/, so canonical, hreflang,
og:url, JSON-LD, sitemap, llms.txt and internal <a href> must use the extensionless form.
Idempotent. Run AFTER all build scripts: python3 tools/clean_urls.py"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = ('tools', '.git', 'automation', 'node_modules')
SKIP_FILES = {'google4c8a12ba6ad82dd8.html'}  # Search Console verification file must stay as is
HOST = 'https://latindanceawards.com/'

def clean_path(p):
    """'es/index.html' -> 'es/', 'index.html' -> '', 'x.html' -> 'x'"""
    if p == 'index.html': return ''
    if p.endswith('/index.html'): return p[:-len('index.html')]
    if p.endswith('.html'): return p[:-5]
    return p

ABS = re.compile(re.escape(HOST) + r'([A-Za-z0-9_./-]*?\.html)(?=[#?"\'<\s)]|$)')
def abs_sub(m): return HOST + clean_path(m.group(1))

HREF = re.compile(r'''(<a\b[^>]*?\bhref=")([^"#?:]*?\.html)([#?][^"]*)?(")''')
def href_sub(m):
    pre, path, tail, q = m.group(1), m.group(2), m.group(3) or '', m.group(4)
    if path.endswith('google4c8a12ba6ad82dd8.html'): return m.group(0)
    lead = '/' if path.startswith('/') else ''
    core = path.lstrip('/')
    if core == 'index.html': new = lead or './'
    elif core.endswith('/index.html'): new = lead + core[:-len('index.html')]
    else: new = lead + core[:-5]
    return pre + new + tail + q

def process(path, is_html):
    s = open(path, encoding='utf-8').read()
    o = s
    s = ABS.sub(abs_sub, s)
    if is_html: s = HREF.sub(href_sub, s)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s); return 1
    return 0

n = 0
for d, dirs, files in os.walk(ROOT):
    rel = os.path.relpath(d, ROOT)
    if rel.split(os.sep)[0] in SKIP_DIRS: continue
    for f in files:
        if f in SKIP_FILES: continue
        if f.endswith('.html'): n += process(os.path.join(d, f), True)
        elif f in ('sitemap.xml', 'llms.txt'): n += process(os.path.join(d, f), False)
print('clean_urls: changed', n, 'files')
