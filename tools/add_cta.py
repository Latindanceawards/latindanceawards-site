"""Adds the paid-plans call to action to the home page(s) and every school profile. Run LAST (after prune_en.py). Idempotent.
Text is bilingual (DE when <html lang=de>, otherwise EN) and follows the in-page language switch."""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRO = 'https://buy.stripe.com/fZuaEZ4xc9MJ3vBaetfMA0J'
SPOT = 'https://buy.stripe.com/28E9AV9Rw4sp4zFcmBfMA0L'
MARK = '<!--lda-cta-->'
SCHOOL_DIRS = ['schools', 'en/schools', 'es/escuelas', 'fr/ecoles', 'it/scuole', 'uk/schools', 'pl/szkoly', 'nl/scholen',
               'pt/escolas', 'at/schools', 'ch/schools', 'be/schools', 'ie/schools', 'ee/schools', 'em/schools', 'nd/schools']
HOMES = ['index.html', 'en/index.html']
CSS = ('<style>.cta{padding:8px 0 56px}.cta-box{max-width:980px;margin:0 auto;padding:clamp(26px,4vw,44px);border-radius:26px;'
 'border:1.5px solid rgba(228,185,91,.6);background:radial-gradient(120% 140% at 0 0,rgba(228,185,91,.22),var(--card,#161214) 60%);'
 'display:grid;gap:22px;text-align:center;justify-items:center}'
 '.cta .cta-n{font-family:var(--serif,Georgia,serif);font-size:clamp(46px,9vw,84px);line-height:1;color:var(--gold-light,#F8E2A6);margin:0}'
 '.cta .cta-n small{display:block;font-family:var(--sans,system-ui,sans-serif);font-size:clamp(14px,2vw,17px);font-weight:600;color:var(--cream,#F6E7D3);margin-top:8px}'
 '.cta h2{font-family:var(--serif,Georgia,serif);font-weight:500;font-size:clamp(22px,3.4vw,32px);line-height:1.2;margin:0;max-width:24em;color:var(--cream,#F6E7D3)}'
 '.cta p:not(.cta-n){margin:0;max-width:40em;color:var(--muted,#b9aa98);font-size:16px;line-height:1.55}'
 '.cta-b{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}.cta-b .btn{min-height:50px}'
 '.cta-m{font-size:14px;color:var(--gold-light,#F8E2A6)}.cta-m a{color:inherit;text-decoration:underline;text-underline-offset:3px}'
 '.cta-l{list-style:none;margin:0;padding:0;display:grid;gap:10px;text-align:left;max-width:30em}.cta-l li{position:relative;padding-left:30px;color:var(--cream,#F6E7D3);font-size:16px;line-height:1.45}.cta-l li:before{content:"\\2713";position:absolute;left:0;top:0;color:var(--gold,#E4B95B);font-weight:700}'
 '@media(max-width:560px){.cta-b{width:100%}.cta-b .btn{width:100%}}</style>')
def block(slug):
    import json
    ref = ('?school=' + slug) if slug else ''
    de = dict(n='15.000+', s='Besucher pro Monat', h='Deine Schule ist hier schon gelistet. Mach daraus neue Schüler.',
      l1='Anfragen für Probestunden direkt per WhatsApp oder E-Mail', l2='Fotos, Videos und das Häkchen „geprüft“',
      l3='Ganz oben in deiner Stadt (mit Spotlight)', l4='Ab 2027 neue Stimmen im Ranking sammeln',
      b='Pläne ansehen · ab 5 €', m='Jederzeit kündbar · <a href="/preise">Alle Vorteile ansehen</a>')
    en = dict(n='15,000+', s='visitors per month', h='Your school is already listed here. Turn it into new students.',
      l1='Trial-class requests straight to your WhatsApp or e-mail', l2='Photos, videos and the verified check mark',
      l3='Top of your city (with Spotlight)', l4='Collect new votes in the ranking from 2027',
      b='See plans · from €5', m='Cancel anytime · <a href="/preise">See everything included</a>')
    d = json.dumps({'de': de, 'en': en}, ensure_ascii=False).replace('</', '<\\/')
    return (MARK + CSS + '<section class="cta" aria-label="Pläne / Plans"><div class="wrap"><div class="cta-box">'
      '<p class="cta-n"><span data-c="n"></span><small data-c="s"></small></p><h2 data-c="h"></h2>'
      '<ul class="cta-l"><li data-c="l1"></li><li data-c="l2"></li><li data-c="l3"></li><li data-c="l4"></li></ul>'
      '<div class="cta-b"><a class="btn btn-gold" href="/preise" data-c="b"></a></div><div class="cta-m" data-c="m"></div></div></div></section>'
      '<script>(function(){var T=%s,r=document.currentScript.previousElementSibling;'
      'function f(){var l=/^de/i.test(document.documentElement.lang||"de")?"de":"en";r.querySelectorAll("[data-c]").forEach(function(e){e.innerHTML=T[l][e.dataset.c]})}'
      'f();new MutationObserver(f).observe(document.documentElement,{attributes:true,attributeFilter:["lang"]})})();</script>'
      % d)
OWN_MARK = '<!--lda-own-->'
OWN_CSS = ('<style>.own{padding:18px 0 0}.own-box{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px 24px;'
 'padding:18px 24px;border-radius:18px;border:1.5px solid rgba(228,185,91,.55);background:linear-gradient(100deg,rgba(228,185,91,.18),var(--card,#161214) 70%)}'
 '.own-t{margin:0;flex:1 1 320px;color:var(--muted,#b9aa98);font-size:15px;line-height:1.5}.own-t b{display:block;font-family:var(--serif,Georgia,serif);font-weight:500;'
 'font-size:clamp(19px,2.6vw,24px);color:var(--cream,#F6E7D3);margin-bottom:2px}@media(max-width:560px){.own .btn{width:100%}}</style>')
def own():
    import json
    T = {'de': {'h': 'Gehört dir diese Schule?', 'p': 'Schick uns deine Infos. Mit bestätigten Daten bekommt sie mehr Punkte und steigt im Ranking.', 'b': 'Infos senden und höher platziert werden'},
         'en': {'h': 'Do you own this school?', 'p': 'Send us your information. Confirmed details earn more points and move it up the ranking.', 'b': 'Send information and rank higher'}}
    return (OWN_MARK + OWN_CSS + '<section class="own" aria-label="Own"><div class="wrap"><div class="own-box"><p class="own-t"><b data-c="h"></b><span data-c="p"></span></p>'
      '<a class="btn btn-gold" href="/bewerbung" data-c="b"></a></div></div></section>'
      '<script>(function(){var T=%s,r=document.currentScript.previousElementSibling;function f(){var l=/^de/i.test(document.documentElement.lang||"de")?"de":"en";'
      'r.querySelectorAll("[data-c]").forEach(function(e){e.innerHTML=T[l][e.dataset.c]})}f();new MutationObserver(f).observe(document.documentElement,{attributes:true,attributeFilter:["lang"]})})();</script>' % json.dumps(T, ensure_ascii=False))
files = [(h, None) for h in HOMES]
for d in SCHOOL_DIRS:
    for f in glob.glob(os.path.join(ROOT, d, '*.html')): files.append((os.path.relpath(f, ROOT), os.path.basename(f)[:-5]))
n = 0
for rel, slug in files:
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read()
    if '</main>' not in s: continue
    t = s
    if MARK not in t:
        i = t.rindex('</main>'); t = t[:i] + block(slug) + '\n' + t[i:]
    if slug and OWN_MARK not in t and '<section class="sp-hero"' in t:
        j = t.index('</section>', t.index('<section class="sp-hero"')) + len('</section>')
        t = t[:j] + '\n' + own() + t[j:]
    if t != s: open(p, 'w', encoding='utf-8').write(t); n += 1
print('cta added on', n, 'pages')
