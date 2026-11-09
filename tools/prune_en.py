"""Shrink the inline English dictionary (var EN={...}) of every page to the keys that page
actually uses via data-i18n. Run LAST in the build sequence (after build_en.py). Idempotent."""
import re, json, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RE_EN = re.compile(r'var EN=(\{.*?\});\n', re.S)
saved = n = 0
for f in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    if '/.git/' in f: continue
    s = open(f, encoding='utf-8').read()
    m = RE_EN.search(s)
    if not m: continue
    try: d = json.loads(m.group(1))
    except Exception: continue
    rest = s[:m.start()] + s[m.end():]
    used = set(re.findall(r'data-i18n=\\?"([^"\\]+)', rest))
    keep = {k: v for k, v in d.items() if k in used}
    if len(keep) == len(d): continue
    new = 'var EN=' + json.dumps(keep, ensure_ascii=False, sort_keys=True) + ';\n'
    s2 = s[:m.start()] + new + s[m.end():]
    open(f, 'w', encoding='utf-8').write(s2)
    saved += len(s) - len(s2); n += 1
print('pruned', n, 'pages, saved %.1f MB' % (saved / 1e6))
