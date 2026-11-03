#!/usr/bin/env python3
"""Post-build step: generate crawlable static English pages under /en/ for the German-site pages
(root-level *.html and schools/*.html), and point every page's hreflang at the real URLs.

Why: English used to be the same URL with a JS swap (?lang=en), which search engines index as one page.
Run AFTER build.py, build_guides.py and clean_urls.py:  python3 tools/build_en.py
Idempotent. Reads the German pages, rewrites them in place (hreflang + language switch) and writes en/*.html."""
import os, re, json, html as H, shutil, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'https://latindanceawards.com/'
EXCLUDE = {'404.html', 'google4c8a12ba6ad82dd8.html'}

def clean_path(p):
    if p == 'index.html': return ''
    if p.endswith('/index.html'): return p[:-len('index.html')]
    if p.endswith('.html'): return p[:-5]
    return p

def source_pages():
    out = []
    for f in sorted(os.listdir(ROOT)):
        if f.endswith('.html') and f not in EXCLUDE: out.append(f)
    sd = os.path.join(ROOT, 'schools')
    if os.path.isdir(sd):
        out += ['schools/' + f for f in sorted(os.listdir(sd)) if f.endswith('.html')]
    return out

PAGES = source_pages()
PAGESET = set(PAGES)

def de_url(p): return HOST + clean_path(p)
def en_url(p): return HOST + 'en/' + clean_path(p)
def en_path(p): return '/en/' + clean_path(p)

def resolve(href, src):
    """Resolve a link as written in page `src` to a repo file path (or None)."""
    h = href.split('#')[0].split('?')[0]
    if h.startswith(HOST): h = h[len(HOST):] or './'
    base = '' if h.startswith('/') else os.path.dirname(src)
    p = os.path.normpath(os.path.join(base, h.lstrip('/')))
    if p == '.': return 'index.html'
    for c in (p, p + '.html', os.path.join(p, 'index.html')):
        if os.path.isfile(os.path.join(ROOT, c)): return c
    return None

# ---------- translate data-i18n nodes ----------
OPEN = re.compile(r'<([a-zA-Z0-9]+)((?:\s[^>]*?)?)\sdata-i18n="([^"]+)"([^>]*)>')
def translate_nodes(s, en):
    out, pos = [], 0
    while True:
        m = OPEN.search(s, pos)
        if not m: out.append(s[pos:]); break
        tag = m.group(1); key = m.group(3)
        out.append(s[pos:m.end()])
        # find matching close tag (balance same-tag nesting)
        depth, i = 1, m.end()
        tagre = re.compile(r'<(/?)' + tag + r'(?=[\s>/])[^>]*>')
        end = None
        for t in tagre.finditer(s, m.end()):
            depth += -1 if t.group(1) else 1
            if depth == 0: end = t; break
        if end is None: pos = m.end(); continue
        inner = s[m.end():end.start()]
        out.append(en[key] if key in en else inner)
        pos = end.start()
    return ''.join(out)

def txt(h): return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()

def de_en_map(s, en):
    """German visible text -> English text, from data-i18n pairs (used to translate FAQ JSON-LD)."""
    mp = {}
    for m in OPEN.finditer(s):
        tag, key = m.group(1), m.group(3)
        if key not in en: continue
        depth, end = 1, None
        for t in re.finditer(r'<(/?)' + tag + r'(?=[\s>/])[^>]*>', s[m.end():]):
            depth += -1 if t.group(1) else 1
            if depth == 0: end = t; break
        if end: mp[txt(s[m.end():m.end() + end.start()])] = txt(en[key])
    return mp

# ---------- link rewriting for the /en/ copy ----------
ATTR = re.compile(r'''(<(a|link|img|source|script|use|image)\b[^>]*?\s(href|src|xlink:href)=")([^"]*)(")''')
def rewrite_url(val, src, is_a):
    if not val or val.startswith(('#', 'http:', 'https:', 'mailto:', 'tel:', 'javascript:', 'data:', '//')):
        if val.startswith(HOST):
            tgt = resolve(val, src)
            if is_a and tgt in PAGESET:
                frag = val[len(val.split('#')[0].split('?')[0]):]
                return en_path(tgt) + frag
        return val
    pth = re.split(r'[#?]', val)[0]
    frag = val[len(pth):]
    tgt = resolve(val, src)
    if is_a and tgt in PAGESET: return en_path(tgt) + frag
    if tgt:  # existing page/asset outside the English set: keep working from /en/
        return '/' + (clean_path(tgt) if tgt.endswith('.html') else tgt) + frag
    base = '' if pth.startswith('/') else os.path.dirname(src)
    return '/' + os.path.normpath(os.path.join(base, pth.lstrip('/'))).lstrip('./') + frag if pth else val

def rewrite_links(s, src):
    def sub(m):
        return m.group(1) + rewrite_url(m.group(4), src, m.group(2) == 'a') + m.group(5)
    s = ATTR.sub(sub, s)
    # relative url(...) in inline CSS (fonts) -> root absolute
    def cssu(m):
        u = m.group(1).strip('\'"')
        if u.startswith(('data:', '#', '/', 'http')): return m.group(0)
        base = os.path.dirname(src)
        return 'url(/' + os.path.normpath(os.path.join(base, u)).lstrip('./') + ')'
    return re.sub(r'url\(([^)]*)\)', cssu, s)

# ---------- script patches ----------
CLICK = 'b.addEventListener("click",function(){ setLang(b.dataset.lang); });'
START_RE = re.compile(r'var start="de";\s*try\{ var q=new URLSearchParams\(location\.search\)\.get\("lang"\);.*?\}catch\(e\)\{\}', re.S)

def patch_de_script(s, p):
    s = s.replace(CLICK, 'b.addEventListener("click",function(){ if(b.dataset.lang==="en"){ location.href="%s"; } else setLang(b.dataset.lang); });' % en_path(p))
    s = START_RE.sub('var start="de"; try{ if(new URLSearchParams(location.search).get("lang")==="en"){ location.replace("%s"+location.hash); return; } }catch(e){}' % en_path(p), s, count=1)
    return s

def patch_en_script(s, p):
    de_path = '/' + clean_path(p)
    s = s.replace(CLICK, 'b.addEventListener("click",function(){ if(b.dataset.lang==="de"){ location.href="%s"; } else setLang(b.dataset.lang); });' % de_path)
    s = START_RE.sub('var start="en";', s, count=1)
    return s

# ---------- head / hreflang ----------
def set_hreflang_de(s, p):
    return re.sub(r'(<link rel="alternate" hreflang="en" href=")[^"]*(")', r'\g<1>%s\g<2>' % en_url(p), s)

def build_en(s, p):
    m = re.search(r'var EN=(\{.*?\});\n', s)
    if not m: return None
    en = json.loads(m.group(1))
    en.setdefault('nav_countries', 'Country rankings')
    meta = re.search(r'en:\{\s*title:(".*?"),\s*desc:(".*?")\s*\}', s)
    t_en = json.loads(meta.group(1)) if meta else None
    d_en = json.loads(meta.group(2)) if meta else None
    mp = de_en_map(s, en)
    e = translate_nodes(s, en)
    e = e.replace('<html lang="de">', '<html lang="en">', 1)
    if t_en:
        e = re.sub(r'<title>.*?</title>', '<title>%s</title>' % H.escape(t_en, quote=False), e, count=1)
        e = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m_: m_.group(1) + H.escape(t_en) + m_.group(2), e, count=1)
        e = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda m_: m_.group(1) + H.escape(t_en) + m_.group(2), e, count=1)
    if d_en:
        e = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m_: m_.group(1) + H.escape(d_en) + m_.group(2), e, count=1)
        e = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m_: m_.group(1) + H.escape(d_en) + m_.group(2), e, count=1)
        e = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', lambda m_: m_.group(1) + H.escape(d_en) + m_.group(2), e, count=1)
    e = re.sub(r'(<link rel="canonical" href=")[^"]*(")', r'\g<1>%s\g<2>' % en_url(p), e, count=1)
    e = re.sub(r'(<meta property="og:url" content=")[^"]*(")', r'\g<1>%s\g<2>' % en_url(p), e, count=1)
    e = re.sub(r'(<link rel="alternate" hreflang="en" href=")[^"]*(")', r'\g<1>%s\g<2>' % en_url(p), e, count=1)
    e = e.replace('content="de_DE"', 'content="en_GB"', 1).replace('og:locale:alternate" content="en_GB"', 'og:locale:alternate" content="de_DE"', 1)
    # JSON-LD: English page URLs, English FAQ text
    def ld(mm):
        try: data = json.loads(mm.group(2))
        except Exception: return mm.group(0)
        def walk(o):
            if isinstance(o, dict):
                if o.get('@type') == 'Question':
                    o['name'] = mp.get(txt(o.get('name', '')), o.get('name'))
                    a = o.get('acceptedAnswer', {})
                    if 'text' in a: a['text'] = mp.get(txt(a['text']), a['text'])
                for k, v in list(o.items()):
                    if isinstance(v, str) and v.startswith(HOST) and k in ('item', 'url', '@id'):
                        tgt = resolve(v, p)
                        if tgt in PAGESET: o[k] = HOST + 'en/' + clean_path(tgt)
                    else: walk(v)
            elif isinstance(o, list):
                for x in o: walk(x)
        walk(data)
        return mm.group(1) + json.dumps(data, ensure_ascii=False, indent=1) + mm.group(3)
    e = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, e, flags=re.S)
    e = rewrite_links(e, p)
    e = patch_en_script(e, p)
    return e

def main():
    shutil.rmtree(os.path.join(ROOT, 'en'), ignore_errors=True)
    made, skipped = 0, []
    for p in PAGES:
        path = os.path.join(ROOT, p)
        s = open(path, encoding='utf-8').read()
        en_html = build_en(s, p)
        if en_html is None: skipped.append(p); continue
        s2 = patch_de_script(set_hreflang_de(s, p), p)
        if s2 != s: open(path, 'w', encoding='utf-8').write(s2)
        dst = os.path.join(ROOT, 'en', p)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'w', encoding='utf-8').write(en_html)
        made += 1
    # sitemap: real English URLs with full hreflang sets
    sm_path = os.path.join(ROOT, 'sitemap.xml')
    sm = open(sm_path, encoding='utf-8').read()
    sm = re.sub(r'\s*<url>\s*<loc>' + re.escape(HOST) + r'en/.*?</url>', '', sm, flags=re.S)
    blocks = []
    def fix(mm):
        blk = mm.group(0)
        loc = re.search(r'<loc>([^<]+)</loc>', blk).group(1)
        rel = loc[len(HOST):]
        tgt = resolve(rel or './', 'index.html') if loc.startswith(HOST) else None
        if tgt not in PAGESET or tgt in skipped: return blk
        blk = re.sub(r'(hreflang="en" href=")[^"]*(")', r'\g<1>%s\g<2>' % en_url(tgt), blk)
        enb = blk.replace('<loc>%s</loc>' % loc, '<loc>%s</loc>' % en_url(tgt), 1)
        blocks.append(enb)
        return blk
    sm = re.sub(r'<url>.*?</url>', fix, sm, flags=re.S)
    sm = sm.replace('</urlset>', ''.join('\n  ' + b for b in blocks) + '\n</urlset>')
    open(sm_path, 'w', encoding='utf-8').write(sm)
    print(f'build_en: wrote {made} English pages, {len(blocks)} sitemap entries, skipped {len(skipped)}: {skipped[:5]}')

if __name__ == '__main__':
    main()
