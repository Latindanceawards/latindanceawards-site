# One page per Ireland school (ie/schools/<slug>.html), same layout as the Polish/German school pages. Run after build_ie.py.
import os, sys, re, io, json, contextlib, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import ireland_data as P
import rank_variant as RV
from build import T, crumbs
import build_ie as BE
t = T('ie')
BASE = '/ie/schools/'

ES_S = {
 'vote_btn': 'Vote for this school', 'vote_mail': 'Your email address', 'vote_send': 'Send my vote',
 'news_opt': 'Yes, I would like to receive news, events and offers about Bachata by email from time to time. You can unsubscribe at any time.',
 'vote_note': 'One vote per person. We will send you a confirmation link. We only use your email for this and to remove duplicate votes.',
 'vote_ok': 'Almost done: we have sent you an email. Click the link so your vote counts. Check your spam folder too.',
 'vote_done': 'A vote has already been cast from this device. Thank you!',
 'err_mail': 'Check your email address and try again.',
 'rv_ok': 'Almost done: we have sent you an email. Click the link and your review will appear here.',
 'rv_err': 'Choose a star rating and write between 10 and 600 characters, with no links or @.',
 'none': 'No reviews yet. Be the first!', 'report': 'Report', 'anon': 'Anonymous',
 'of': 'reviews', 'one': 'review', 'fail': 'The reviews could not be loaded.', 'copied': 'Link copied',
}
def school_js(nm, city):
    js = B.SCHOOL_JS
    m = re.search(r'  var S = \{.*?\n  \};\n', js, re.S)
    blk = m.group(0)
    def rep(mm):
        k = mm.group(1)
        return f'{k}:[{json.dumps(ES_S[k], ensure_ascii=False)},{mm.group(3)}]' if k in ES_S else mm.group(0)
    blk2 = re.sub(r'(\w+):\[("(?:[^"\\]|\\.)*"),("(?:[^"\\]|\\.)*")\]', rep, blk)
    js = js.replace(blk, blk2)
    js = js.replace('window.LANG==="en"?"EN":"DE"', 'window.LANG==="en"?"EN":"IE"')
    ep = re.search(r'var VOTE_ENDPOINT = "([^"]+)"', B.rank_js).group(1)
    return js.replace('__SCHOOL__', json.dumps({'name': nm, 'city': city}, ensure_ascii=False)).replace('__EP__', ep)

FAC = [('Years teaching', 'Years teaching', 10), ('Beginner offer', 'Beginner offer', 10), ('Events and guests', 'Events and guests', 10),
       ('Google rating', 'Google rating', 25), ('Number of reviews', 'Number of reviews', 10), ('Social media', 'Social media', 10)]
TBD = t("span", "To be confirmed", "To be confirmed")

entries = [(e, c) for c, es in RV.polish_entries(P, BASE).items() for e in es]
entries.sort(key=lambda x: (-RV.total(x[0]), x[0]['name']))
by_city = {}
for e, c in entries: by_city.setdefault(c, []).append(e['name'])

def build(rank, e, ck):
    nm = e['name']; cpl, cen = P.CITIES[ck][0], P.CITIES[ck][1]
    slug = RV.pl_slug(nm); pts = RV.total(e); crank = by_city[ck].index(nm) + 1
    f1 = lambda x: f'{x:.1f}'.replace('.', ',')
    rows = ''
    for k, (pl, en, mx) in enumerate(FAC):
        fx = e['fx'][0] if k == 3 else (e['fx'][0].split(' · ')[1] if k == 4 else (e['fx'][1] if k == 5 else ''))
        small = f' <small>({fx})</small>' if fx and fx != '–' else ''
        rows += f'<div class="sp-row"><b>{t("span", pl, en)}</b> · {f"{e['sc'][k]:g}".replace('.', ',')} / {mx}{small}<div class="bar"><i style="width:{e["sc"][k]/mx*100:.0f}%"></i></div></div>\n'
    sty = ' '.join(f'<span class="chip st">{x}</span>' for x in e['st']) or f'<span class="chip">{TBD}</span>'
    rows += f'<div class="sp-row"><b>{t("span", "Styles (Dominican, sensual, modern)", "Styles (Dominicana, Sensual, Moderna)")}</b> · {sty}</div>\n'
    for pl, en in (('Festivals', 'Festivals'), ('Recent reviews', 'Recent reviews'), ('Competitions entered', 'Competitions entered'), ('Competitions won', 'Competitions won')):
        rows += f'<div class="sp-row"><b>{t("span", pl, en)}</b> · <span class="chip">{TBD}</span></div>\n'
    maps = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(f'{nm} {cpl}').replace('%20', '+')
    site = e['url']
    sitebtn = '' if 'google.com/maps' in site else f'<a class="btn btn-ghost" href="{site}" rel="noopener nofollow" target="_blank">{t("span", "School website →", "School website →")}</a>'
    main = f'''
<section class="sp-hero" aria-labelledby="sp-title">
  <div class="wrap">
    <div>
      <p class="sp-crumb"><a href="/ie/">{t("span", "Ireland ranking 2027", "Ireland ranking 2027")}</a> › <a href="/ie/bachata-{ck}.html">{cpl}</a></p>
      <span class="edition"><i></i>{t("span", "Interim standing · not final", "Interim standing · not final")}</span>
      <h1 id="sp-title">{nm}</h1>
      <p class="lede">{t("span", f"Bachata school in {cpl}. Interim standing: place {crank} in the city ({cpl}), place {rank} in Ireland. Schools are still competing.", f"Bachata school in {cen}. Interim ranking: place {crank} in {cen}, place {rank} in Ireland. Schools are still competing.")}</p>
      <div class="sp-links"><button type="button" class="btn btn-ghost" id="share">{t("span", "Share", "Share")}</button></div>
    </div>
    <div class="sp-score"><b>{f1(pts)}</b><small>/ 100 · {t("span", "interim", "interim")}</small></div>
  </div>
</section>

<section class="block alt" aria-label="Details">
  <div class="wrap sp-grid">
    <div class="sp-card">
      {t("h2", "How the score is made up", "How the score is made up")}
      {t("p", "For now we score six of the nine criteria (75 points at most). Anything we could not confirm counts at the lowest value, and a school can fill it in by applying. Data from October 2026 (Google, Instagram, school website).", "Six of nine factors are scored so far (75 points at most). Anything we could not confirm counts at the lowest level, and a school can complete it in its application. Data as of October 2026 (Google, Instagram, school website).")}
      {rows}
      <div class="sp-links">{sitebtn}<a class="btn btn-ghost" href="{maps}" rel="noopener nofollow" target="_blank">{t("span", "Google Maps →", "Google Maps →")}</a></div>
    </div>
    <div class="sp-card">
      {t("h2", "Audience Award: cast your vote", "Audience Award: vote")}
      {t("p", "One vote per person, confirmed by email. The prize is separate from the 100 points. The result is published with the ranking.", "One vote per person, confirmed by email. The award is separate from the 100 points. The result comes with the ranking.")}
      <button type="button" class="btn btn-gold" id="vbtn">&#9733; {t("span", "Vote for this school", "Vote for this school")}</button>
      <form class="sp-form" id="vform" hidden novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <label>{t("span", "Your email address", "Your email address")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {t("span", ES_S['news_opt'], "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{t("span", "Send my vote", "Send my vote")}</button>
        <small>{t("span", ES_S['vote_note'], "One vote per person. We email you a confirmation link. We use your email only for that and to remove duplicate votes.")}</small>
      </form>
      <p class="sp-msg" id="vmsg" role="status" hidden></p>
    </div>
  </div>
</section>

<section class="block" aria-labelledby="rv-title">
  <div class="wrap sp-two">
    <div class="sp-card">
      <h2 id="rv-title">{t("span", "Reviews", "Reviews")}</h2>
      <div class="sp-sum" id="rvsum"></div>
      <div id="rvlist"></div>
    </div>
    <div class="sp-card">
      {t("h2", "Write a review", "Write a review")}
      {t("p", "Did you take classes at this school? Tell us briefly. Your review appears once you click the link in our email. Please be honest and factual.", "Have you been to this school? Tell us briefly how it was. Your review appears once you click the link in our email. Please stay factual and fair.")}
      <form class="sp-form" id="rvform" novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <div role="radiogroup" aria-label="Stars"><div class="sp-stars">
          <input type="radio" name="rating" value="5" id="st5"><label for="st5" title="5">★</label>
          <input type="radio" name="rating" value="4" id="st4"><label for="st4" title="4">★</label>
          <input type="radio" name="rating" value="3" id="st3"><label for="st3" title="3">★</label>
          <input type="radio" name="rating" value="2" id="st2"><label for="st2" title="2">★</label>
          <input type="radio" name="rating" value="1" id="st1"><label for="st1" title="1">★</label>
        </div></div>
        <label>{t("span", "Your name (optional)", "Your name (optional)")}<input type="text" name="name" maxlength="40" autocomplete="nickname"></label>
        <label>{t("span", "Your review (10 to 600 characters, no links)", "Your review (10 to 600 characters, no links)")}<textarea name="text" maxlength="600" required></textarea></label>
        <label>{t("span", "Your email address (not published)", "Your email address (not published)")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {t("span", ES_S['news_opt'], "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{t("span", "Submit review", "Submit review")}</button>
      </form>
      <p class="sp-msg" id="rvmsg" role="status" hidden></p>
    </div>
  </div>
</section>

<section class="block alt" aria-labelledby="own-title">
  <div class="wrap">
    <div class="sp-card" style="max-width:760px">
      {t("h2", "Is this your school?", "Is this your school?").replace("<h2", '<h2 id="own-title"')}
      {t("p", "You can complete or correct your data, for example festivals, competitions and founding year. If you do not want to be in the ranking, write to us and we will remove your school.", "You can add or correct your data, for example festivals, competitions and founding year. If you do not want to be in the ranking, write to us and we will remove your school.")}
      <div class="sp-links"><a class="btn btn-gold" href="/bewerbung.html">{t("span", "Complete or correct my data", "Add or correct my data")}</a><a class="btn btn-ghost" href="mailto:hello@latindanceawards.com?subject={urllib.parse.quote(nm)}">{t("span", "Write to us", "Write to us")}</a></div>
    </div>
  </div>
</section>
'''
    fn = f'ie/schools/{slug}.html'
    schema = [crumbs(nm, fn), {"@context": "https://schema.org", "@type": "LocalBusiness", "name": nm, "url": site if 'google.com/maps' not in site else maps,
              "address": {"@type": "PostalAddress", "addressLocality": cpl, "addressCountry": "IE"}}]
    BE.ie_page(fn, fn, f'{nm} · Bachata {cpl} · reviews and rating', f'{nm} in {cpl}: points, place {crank} in the interim Bachata ranking, reviews and a vote for the Audience Award.',
               f'{nm} · Bachata {cen} · Reviews', f'{nm} in {cen}: score, place {crank} in the interim Bachata ranking, reviews and voting for the Audience Award.',
               main, t.en, schema, js=school_js(nm, cpl))
    return fn

os.makedirs(os.path.join(B.ROOT, 'ie', 'schools'), exist_ok=True)
files = [build(i, e, c) for i, (e, c) in enumerate(entries, 1)]
print('ie school pages:', len(files), 'unique slugs:', len(set(files)))
