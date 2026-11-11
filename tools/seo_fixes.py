#!/usr/bin/env python3
"""Idempotent SEO patch for index.html (audit 2026-11). Run from repo root."""
import hashlib, json, re, os
P = 'index.html'
h = open(P, encoding='utf8').read()
if 'seo_fixes:done' in h:
    print('already applied'); raise SystemExit

# 1. externalise CANDIDATES (347 KB) -> lazy-loaded script
a = h.index('  var CANDIDATES = {')
b = h.index('  var VOTE_ENDPOINT')
block = h[a:b]
body = block.strip()
assert body.endswith('};')
js = 'window.__CAND=' + body[len('var CANDIDATES = '):]
hs = hashlib.sha256(js.encode()).hexdigest()[:8]
fn = 'data/candidates.%s.js' % hs
open(fn, 'w', encoding='utf8').write(js + '\n')
h = h[:a] + '  var CANDIDATES = {};\n' + h[b:]
loader = ('(function(){var s=document.createElement("script");s.src="/%s";s.async=true;'
          's.onload=function(){if(window.__CAND){CANDIDATES=window.__CAND;try{syncPicker();}catch(e){}render();}};'
          'document.head.appendChild(s);})();\n' % fn)
anchor = '  select((location.hash||"").slice(1)||SCOPE,false);\n'
assert h.count(anchor) == 1
h = h.replace(anchor, anchor + '  ' + loader)

# 2. mobile hero: text and CTAs first, badge after, no low fetch priority
old = '  .page-hero .seal-box{order:-1;margin-top:16px}\n  .page-hero .seal{width:min(260px,70vw)}'
assert old in h
h = h.replace(old, '  .page-hero .seal-box{margin-top:8px}\n  .page-hero .seal{width:min(200px,52vw)}')
h = h.replace(' height="360" fetchpriority="low">', ' height="360" decoding="async">')

# 3. meta description
md = ('Bachata-Ranking für Europa: 1803 Schulen in 39 Ländern, bewertet nach neun öffentlichen Kriterien. '
      'Zwischenstand, Endergebnis für Deutschland am 20. Dezember 2026. Unabhängig, nicht käuflich, Anmeldung kostenlos.')
h = h.replace('content="Bachata-Ranking für Europa: alle 1803 Schulen in einer Liste plus Ranking pro Land (39 Länder). Unabhängig und nicht käuflich."', 'content="%s"' % md)

# 4. JSON-LD: Organization, WebSite, ItemList
g = [
 {"@context": "https://schema.org", "@type": "Organization", "@id": "https://latindanceawards.com/#org",
  "name": "Latin Dance Awards", "url": "https://latindanceawards.com/",
  "logo": "https://latindanceawards.com/badge-bachata-europe.svg",
  "founder": {"@type": "Person", "name": "Mateus Alves"},
  "address": {"@type": "PostalAddress", "addressLocality": "München", "addressCountry": "DE"}},
 {"@context": "https://schema.org", "@type": "WebSite", "@id": "https://latindanceawards.com/#site",
  "url": "https://latindanceawards.com/", "name": "Latin Dance Awards", "inLanguage": ["de", "en"],
  "publisher": {"@id": "https://latindanceawards.com/#org"}},
 {"@context": "https://schema.org", "@type": "ItemList", "name": "Bachata-Schulen Deutschland: Zwischenstand",
  "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Alma Dance Frankfurt", "url": "https://latindanceawards.com/schools/alma-dance-frankfurt"},
   {"@type": "ListItem", "position": 2, "name": "Hamburg Dance Academy", "url": "https://latindanceawards.com/schools/hamburg-dance-academy"},
   {"@type": "ListItem", "position": 3, "name": "Cumbancha Tanzschule", "url": "https://latindanceawards.com/schools/cumbancha-tanzschule"}]}]
add = ',\n' + ',\n'.join(json.dumps(x, ensure_ascii=False, indent=1) for x in g)
i = h.index('<script type="application/ld+json">'); j = h.index('\n]\n</script>', i)
h = h[:j] + add + h[j:]

# 5. Zwischenstand label + 6. "Wer steht dahinter"
note = '<p class="zw" data-i18n="eu231">Zwischenstand: Wertung aus 2 von 9 Kriterien. Endergebnis für Deutschland am 20. Dezember 2026.</p>'
k = h.index('<section class="spon"'); e = h.index('</div></div>', h.index('spon-stage', k))
sec_end = h.index('</section>', k)
h = h[:sec_end] + note + h[sec_end:]
who = ('<section class="block"><div class="wrap prose"><h2 data-i18n="eu232">Wer steht dahinter</h2>'
       '<p data-i18n="eu233">Latin Dance Awards betreibt Mateus Alves aus München, unabhängig und ohne bezahlte Plätze. '
       'Die Daten stammen aus öffentlichen Quellen, Schulen können ihre Angaben kostenlos bestätigen. '
       'Alle Angaben stehen im <a href="impressum">Impressum</a>.</p></div></section>')
m = '<section class="block alt"><div class="wrap prose"><h2 data-i18n="eu225">'
assert h.count(m) == 1
h = h.replace(m, who + m)
en = ('"eu231": "Interim standing: scored on 2 of 9 criteria. Final results for Germany on December 20, 2026.", '
      '"eu232": "Who is behind this", '
      '"eu233": "Latin Dance Awards is run by Mateus Alves in Munich, independently and with no paid placements. The data comes from public sources, and schools can confirm their details for free. Full details are in the <a href=\\"impressum\\">legal notice</a>.", ')
t = '"eu108": "Enter a school for free"'
assert h.count(t) == 1
h = h.replace(t, en + t)
h = h.replace('</head>', '<!-- seo_fixes:done -->\n<style>.zw{margin:10px auto 0;text-align:center;color:var(--muted);font-size:14px}</style>\n</head>', 1)
open(P, 'w', encoding='utf8').write(h)

# 7. headers
H = open('_headers', encoding='utf8').read()
H = H.replace('max-age=31536000\n', 'max-age=31536000; includeSubDomains\n', 1)
if '/data/*' not in H:
    H += '/data/*\n  Cache-Control: public, max-age=31536000, immutable\n'
open('_headers', 'w', encoding='utf8').write(H)
print('ok', fn, len(js))
