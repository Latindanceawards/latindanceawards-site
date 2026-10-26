# Reuses the live Germany ranking panel (rankings.html: tabs, city picker, crown/medal cards, score bars, voting)
# for other scopes (Europe hub, country pages) by patching its JS and text. The design is not touched.
import re, json, math, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import build as B

def parts(r, v):
    """Google points (max 25) and review-volume points (max 10); same formulas as the German ranking."""
    b = (v * r + 25 * 4.32) / (v + 25)
    return round(max(0.0, 25 - 17.2 * (5 - b)), 1), round(10 * min(1.0, math.log(1 + v) / math.log(251)), 1)

def fx_str(r, v): return f'{r:.1f}'.replace('.', ',') + f' ★ · {v}'

def german_entries():
    """Germany on the common interim basis (Google rating + review volume), every other factor left out."""
    out = {}
    for e in B.SCH:
        m = re.match(r'([\d,]+) ★ · ([\d.]+)', e['fx'][0].replace('\xa0', ' '))
        if m:
            r, v = float(m.group(1).replace(',', '.')), int(m.group(2).replace('.', ''))
            g, rv = parts(r, v)
            sc, fx = [0, 0, 0, g, rv, 0], [fx_str(r, v), '–']
        else:
            sc, fx = [0, 0, 0, 0, 0, 0], ['–', '–']
        out.setdefault(e['city'], []).append(dict(name=e['name'], sc=sc, fx=fx, url=e['url']))
    return out

def polish_entries(P):
    out = {}
    for name, city, r, v, url in P.SCHOOLS:
        g, rv = parts(r, v)
        out.setdefault(city, []).append(dict(name=name, sc=[0, 0, 0, g, rv, 0], fx=[fx_str(r, v), '–'], url=url, np=1))
    return out

def cand_js(cands):
    lines = []
    for city, es in cands.items():
        items = ',\n'.join('      ' + json.dumps(e, ensure_ascii=False, separators=(', ', ':')).replace('{"name":', '{name:', 1)
                           .replace(', "sc":', ', sc:').replace(', "fx":', ', fx:').replace(', "url":', ', url:').replace(', "np":', ', np:')
                           for e in es)
        lines.append(f'    {json.dumps(city)}: [\n{items}\n    ]')
    return '{\n' + ',\n'.join(lines) + '\n  }'

def sub1(js, old, new, n=1):
    assert js.count(old) >= 1, 'missing: ' + old[:80]
    return js.replace(old, new) if n == 0 else js.replace(old, new, n)

def make_js(scope, groups, tx, cands, quick, scale, pl=False, extra=None):
    js = B.rank_js
    js = re.sub(r'var RESULTS = \{.*?\n  \};', 'var RESULTS = {};', js, count=1, flags=re.S)
    js = re.sub(r'var CANDIDATES = \{.*?\n  \};', lambda m: 'var CANDIDATES = ' + cand_js(cands) + ';', js, count=1, flags=re.S)
    js = re.sub(r'var TX = \{[^\n]*\};\n', lambda m: 'var TX = ' + json.dumps(tx, ensure_ascii=False) + ';\n', js, count=1)
    js = sub1(js, 'new Date("2026-12-20T19:00:00+01:00")', 'new Date("2099-01-01T00:00:00+00:00")')
    helpers = ('var SCOPE=' + json.dumps(scope) + ', GROUPS=' + json.dumps(groups) + ', SCALE=' + str(scale) + ';\n'
               '  function inScope(c,k){ if(c===SCOPE) return true; var g=GROUPS[c]; return g?g.indexOf(k)>-1:c===k; }\n'
               '  function isCountry(c){ return c===SCOPE||!!GROUPS[c]; }\n  ')
    js = sub1(js, 'var PUBLISH_DATE', helpers + 'var PUBLISH_DATE')
    js = sub1(js, 'if(city==="deutschland"){', 'if(city===SCOPE){')
    js = sub1(js, 'current="deutschland"', 'current=SCOPE')
    js = sub1(js, '(current==="deutschland"?', '(isCountry(current)?')
    js = sub1(js, 'if(c==="deutschland"||c===k) CANDIDATES', 'if(inScope(c,k)) CANDIDATES')
    js = sub1(js, '(c==="deutschland"||c===k)', 'inScope(c,k)', 0)
    js = sub1(js, 'c==="deutschland" ? L("title_de")', 'c===SCOPE ? L("title_de")')
    js = sub1(js, '(c==="deutschland"?\'<small>\'', '(isCountry(c)?\'<small>\'', 0)
    js = re.sub(r'var QUICK=\[[^\]]*\];', 'var QUICK=' + json.dumps(quick) + ';', js, count=1)
    js = sub1(js, 'if(!TX.cities[c]) c="deutschland";', 'if(!TX.cities[c]) c=SCOPE;')
    js = sub1(js, '||"deutschland",false)', '||SCOPE,false)')
    js = sub1(js, 'tick(); setInterval(tick,1000);', '')
    # common interim basis: only Google rating and review volume are scored, so the bars and the total use that scale
    js = sub1(js, '<small> / 100</small></span><span class="meter"><i style="width:\'+e.pts+\'%"></i>',
              '<small> / \'+SCALE+\'</small></span><span class="meter"><i style="width:\'+(e.pts/SCALE*100)+\'%"></i>')
    js = sub1(js, 'FAC.forEach(function(f,k){ var fx=', 'FAC.forEach(function(f,k){ if(k<3||k===5) return; var fx=')
    js = re.sub(r"why\+='<div class=\"tbc\"><b>'\+esc\(en\?\"Style variety[^\n]*\n", '', js, count=1)
    # schools without an own page here link to their website
    js = sub1(js, '<b><a href="schools/\'+slug(e.name)+\'.html">',
              '<b><a href="\'+(e.np?(safeUrl(e.url)||"#"):"schools/"+slug(e.name)+".html")+\'"\'+(e.np?\' rel="nofollow noopener" target="_blank"\':"")+\'>')
    js = sub1(js, "why+='<div class=\"lk\"><a href=\"schools/'", "if(!e.np) why+='<div class=\"lk\"><a href=\"schools/'")
    # factors that no country has collected yet are shown as "to be confirmed"
    old_tbc = re.search(r'var TBC=en\?\[.*?\]\]:\[\[.*?\]\];', js, re.S).group(0)
    ff = extra['tbc']
    new_tbc = 'var TBC=en?' + json.dumps(ff[1], ensure_ascii=False) + ':' + json.dumps(ff[0], ensure_ascii=False) + ';'
    js = js.replace(old_tbc, new_tbc)
    if pl:
        for a, b in extra['literals'].items():
            assert a in js, 'literal missing: ' + a
            js = js.replace(a, b)
        js = js.replace('?"EN":"DE"', '?"EN":"PL"')
        js = js.replace('replace(/ß/g,"ss")', 'replace(/ß/g,"ss").replace(/ł/g,"l")')
    return js

def ranking_section(tabs, ph_de, ph_en, aria):
    s = re.search(r'<section class="block alt" id="ranking".*?</section>', B.rank_main, re.S).group(0)
    s = re.sub(r'(<div class="tabs"[^>]*>\n).*?(\n      <div class="citypick")', lambda m: m.group(1) + tabs + m.group(2), s, count=1, flags=re.S)
    s = s.replace('data-ph-de="Stadt suchen …"', f'data-ph-de="{ph_de}"').replace('data-ph-en="Search city …"', f'data-ph-en="{ph_en}"')
    s = re.sub(r'aria-label="Stadt suchen / Search city[^"]*"', f'aria-label="{aria}"', s)
    s = s.replace('aria-label="Städte / Cities"', f'aria-label="{aria}"')
    return s

def tabs_html(t, items):
    return '\n'.join(
        f'      <button type="button" role="tab" id="tab-{k}" aria-controls="panel" aria-selected="{"true" if i == 0 else "false"}" data-city="{k}">{t("span", de, en)}</button>'
        for i, (k, de, en) in enumerate(items))
