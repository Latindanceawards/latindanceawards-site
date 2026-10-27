# One page per French school (fr/ecoles/<slug>.html), same layout as the Polish/German school pages. Run after build_fr.py.
import os, sys, re, io, json, contextlib, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import france_data as P
import rank_variant as RV
from build import T, crumbs
import build_fr as BE
t = T('fr')
BASE = '/fr/ecoles/'

ES_S = {
 'vote_btn': 'Voter pour cette école', 'vote_mail': 'Votre e-mail', 'vote_send': 'Envoyer mon vote',
 'news_opt': 'Oui, je souhaite recevoir de temps en temps des nouvelles, des événements et des offres sur la bachata par e-mail. Vous pouvez vous désabonner à tout moment.',
 'vote_note': 'Un vote par personne. Nous vous enverrons un lien de confirmation. Nous utilisons votre e-mail uniquement pour cela et pour supprimer les votes en double.',
 'vote_ok': 'Presque terminé : nous vous avons envoyé un e-mail. Cliquez sur le lien pour que votre vote compte. Vérifiez aussi vos courriers indésirables.',
 'vote_done': 'Un vote a déjà été enregistré depuis cet appareil. Merci !',
 'err_mail': 'Vérifiez votre e-mail et réessayez.',
 'rv_ok': 'Presque terminé : nous vous avons envoyé un e-mail. Cliquez sur le lien et votre avis apparaîtra ici.',
 'rv_err': 'Choisissez les étoiles et écrivez entre 10 et 600 caractères, sans lien ni @.',
 'none': 'Pas encore d’avis. Soyez la première personne !', 'report': 'Signaler', 'anon': 'Anonyme',
 'of': 'avis', 'one': 'avis', 'fail': 'Impossible de charger les avis.', 'copied': 'Lien copié',
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
    js = js.replace('window.LANG==="en"?"EN":"DE"', 'window.LANG==="en"?"EN":"FR"')
    ep = re.search(r'var VOTE_ENDPOINT = "([^"]+)"', B.rank_js).group(1)
    return js.replace('__SCHOOL__', json.dumps({'name': nm, 'city': city}, ensure_ascii=False)).replace('__EP__', ep)

FAC = [('Années d’activité', 'Years teaching', 10), ('Offre pour débutants', 'Beginner offer', 10), ('Événements et invités', 'Events and guests', 10),
       ('Note Google', 'Google rating', 25), ('Nombre d’avis', 'Number of reviews', 10), ('Réseaux sociaux', 'Social media', 10)]
TBD = t("span", "À confirmer", "To be confirmed")

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
    rows += f'<div class="sp-row"><b>{t("span", "Styles (dominicaine, sensual, moderne)", "Styles (Dominicana, Sensual, Moderna)")}</b> · {sty}</div>\n'
    for pl, en in (('Festivals', 'Festivals'), ('Avis récents', 'Recent reviews'), ('Participation à des concours', 'Competitions entered'), ('Concours remportés', 'Competitions won')):
        rows += f'<div class="sp-row"><b>{t("span", pl, en)}</b> · <span class="chip">{TBD}</span></div>\n'
    maps = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(f'{nm} {cpl}').replace('%20', '+')
    site = e['url']
    sitebtn = '' if 'google.com/maps' in site else f'<a class="btn btn-ghost" href="{site}" rel="noopener nofollow" target="_blank">{t("span", "Site de l’école →", "School website →")}</a>'
    main = f'''
<section class="sp-hero" aria-labelledby="sp-title">
  <div class="wrap">
    <div>
      <p class="sp-crumb"><a href="/fr/">{t("span", "Classement France 2027", "France ranking 2027")}</a> › <a href="/fr/bachata-{ck}.html">{cpl}</a></p>
      <span class="edition"><i></i>{t("span", "Classement provisoire · pas le résultat final", "Interim standing · not final")}</span>
      <h1 id="sp-title">{nm}</h1>
      <p class="lede">{t("span", f"École de bachata à {cpl}. Classement provisoire : place {crank} dans la ville ({cpl}), place {rank} en France. Les écoles sont toujours en compétition.", f"Bachata school in {cen}. Interim ranking: place {crank} in {cen}, place {rank} in France. Schools are still competing.")}</p>
      <div class="sp-links"><button type="button" class="btn btn-ghost" id="share">{t("span", "Partager", "Share")}</button></div>
    </div>
    <div class="sp-score"><b>{f1(pts)}</b><small>/ 100 · {t("span", "provisoire", "interim")}</small></div>
  </div>
</section>

<section class="block alt" aria-label="Details">
  <div class="wrap sp-grid">
    <div class="sp-card">
      {t("h2", "Comment le score est composé", "How the score is made up")}
      {t("p", "Pour l’instant, nous notons six des neuf critères (75 points au maximum). Ce que nous n’avons pas pu confirmer compte avec la valeur la plus basse, et l’école peut le compléter en s’inscrivant. Données d’octobre 2026 (Google, Instagram, site de l’école).", "Six of nine factors are scored so far (75 points at most). Anything we could not confirm counts at the lowest level, and a school can complete it in its application. Data as of October 2026 (Google, Instagram, school website).")}
      {rows}
      <div class="sp-links">{sitebtn}<a class="btn btn-ghost" href="{maps}" rel="noopener nofollow" target="_blank">{t("span", "Google Maps →", "Google Maps →")}</a></div>
    </div>
    <div class="sp-card">
      {t("h2", "Prix du public : votez", "Audience Award: vote")}
      {t("p", "Un vote par personne, confirmé par e-mail. Le prix est indépendant des 100 points. Le résultat sera publié avec le classement.", "One vote per person, confirmed by email. The award is separate from the 100 points. The result comes with the ranking.")}
      <button type="button" class="btn btn-gold" id="vbtn">&#9733; {t("span", "Voter pour cette école", "Vote for this school")}</button>
      <form class="sp-form" id="vform" hidden novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <label>{t("span", "Votre e-mail", "Your email address")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {t("span", ES_S['news_opt'], "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{t("span", "Envoyer mon vote", "Send my vote")}</button>
        <small>{t("span", ES_S['vote_note'], "One vote per person. We email you a confirmation link. We use your email only for that and to remove duplicate votes.")}</small>
      </form>
      <p class="sp-msg" id="vmsg" role="status" hidden></p>
    </div>
  </div>
</section>

<section class="block" aria-labelledby="rv-title">
  <div class="wrap sp-two">
    <div class="sp-card">
      <h2 id="rv-title">{t("span", "Avis", "Reviews")}</h2>
      <div class="sp-sum" id="rvsum"></div>
      <div id="rvlist"></div>
    </div>
    <div class="sp-card">
      {t("h2", "Écrire un avis", "Write a review")}
      {t("p", "Vous avez fréquenté cette école ? Racontez-nous brièvement. Votre avis apparaît quand vous cliquez sur le lien de notre e-mail. Écrivez avec honnêteté et objectivité.", "Have you been to this school? Tell us briefly how it was. Your review appears once you click the link in our email. Please stay factual and fair.")}
      <form class="sp-form" id="rvform" novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <div role="radiogroup" aria-label="Étoiles / Stars"><div class="sp-stars">
          <input type="radio" name="rating" value="5" id="st5"><label for="st5" title="5">★</label>
          <input type="radio" name="rating" value="4" id="st4"><label for="st4" title="4">★</label>
          <input type="radio" name="rating" value="3" id="st3"><label for="st3" title="3">★</label>
          <input type="radio" name="rating" value="2" id="st2"><label for="st2" title="2">★</label>
          <input type="radio" name="rating" value="1" id="st1"><label for="st1" title="1">★</label>
        </div></div>
        <label>{t("span", "Votre nom (facultatif)", "Your name (optional)")}<input type="text" name="name" maxlength="40" autocomplete="nickname"></label>
        <label>{t("span", "Votre avis (de 10 à 600 caractères, sans lien)", "Your review (10 to 600 characters, no links)")}<textarea name="text" maxlength="600" required></textarea></label>
        <label>{t("span", "Votre e-mail (non publié)", "Your email address (not published)")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {t("span", ES_S['news_opt'], "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{t("span", "Envoyer l’avis", "Submit review")}</button>
      </form>
      <p class="sp-msg" id="rvmsg" role="status" hidden></p>
    </div>
  </div>
</section>

<section class="block alt" aria-labelledby="own-title">
  <div class="wrap">
    <div class="sp-card" style="max-width:760px">
      {t("h2", "C’est votre école ?", "Is this your school?").replace("<h2", '<h2 id="own-title"')}
      {t("p", "Vous pouvez compléter ou corriger vos données, par exemple festivals, concours et année de création. Si vous ne souhaitez pas figurer au classement, écrivez-nous et nous retirerons votre école.", "You can add or correct your data, for example festivals, competitions and founding year. If you do not want to be in the ranking, write to us and we will remove your school.")}
      <div class="sp-links"><a class="btn btn-gold" href="/bewerbung.html">{t("span", "Compléter ou corriger mes données", "Add or correct my data")}</a><a class="btn btn-ghost" href="mailto:hello@latindanceawards.com?subject={urllib.parse.quote(nm)}">{t("span", "Écrivez-nous", "Write to us")}</a></div>
    </div>
  </div>
</section>
'''
    fn = f'fr/ecoles/{slug}.html'
    schema = [crumbs(nm, fn), {"@context": "https://schema.org", "@type": "LocalBusiness", "name": nm, "url": site if 'google.com/maps' not in site else maps,
              "address": {"@type": "PostalAddress", "addressLocality": cpl, "addressCountry": "FR"}}]
    BE.fr_page(fn, fn, f'{nm} · Bachata {cpl} · avis et note', f'{nm} à {cpl} : points, place {crank} au classement provisoire de bachata, avis et vote pour le Prix du public.',
               f'{nm} · Bachata {cen} · Reviews', f'{nm} in {cen}: score, place {crank} in the interim Bachata ranking, reviews and voting for the Audience Award.',
               main, t.en, schema, js=school_js(nm, cpl))
    return fn

os.makedirs(os.path.join(B.ROOT, 'fr', 'ecoles'), exist_ok=True)
files = [build(i, e, c) for i, (e, c) in enumerate(entries, 1)]
print('fr school pages:', len(files), 'unique slugs:', len(set(files)))
