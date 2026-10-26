# One page per Spanish school (es/escuelas/<slug>.html), same layout as the Polish/German school pages. Run after build_es.py.
import os, sys, re, io, json, contextlib, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import spain_data as P
import rank_variant as RV
from build import T, crumbs
import build_es as BE
t = T('es')
BASE = '/es/escuelas/'

ES_S = {
 'vote_btn': 'Votar por esta escuela', 'vote_mail': 'Tu correo electrónico', 'vote_send': 'Enviar mi voto',
 'news_opt': 'Sí, quiero recibir de vez en cuando noticias, eventos y ofertas sobre bachata por correo. Puedes darte de baja cuando quieras.',
 'vote_note': 'Un voto por persona. Te enviaremos un enlace de confirmación. Usamos tu correo solo para eso y para eliminar votos duplicados.',
 'vote_ok': 'Casi listo: te hemos enviado un correo. Haz clic en el enlace para que tu voto cuente. Mira también en la carpeta de spam.',
 'vote_done': 'Ya se ha votado desde este dispositivo. ¡Gracias!',
 'err_mail': 'Revisa tu correo electrónico e inténtalo de nuevo.',
 'rv_ok': 'Casi listo: te hemos enviado un correo. Haz clic en el enlace y tu reseña aparecerá aquí.',
 'rv_err': 'Elige las estrellas y escribe entre 10 y 600 caracteres, sin enlaces ni @.',
 'none': 'Todavía no hay reseñas. ¡Sé la primera persona!', 'report': 'Denunciar', 'anon': 'Anónimo',
 'of': 'reseñas', 'one': 'reseña', 'fail': 'No se han podido cargar las reseñas.', 'copied': 'Enlace copiado',
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
    js = js.replace('window.LANG==="en"?"EN":"DE"', 'window.LANG==="en"?"EN":"ES"')
    ep = re.search(r'var VOTE_ENDPOINT = "([^"]+)"', B.rank_js).group(1)
    return js.replace('__SCHOOL__', json.dumps({'name': nm, 'city': city}, ensure_ascii=False)).replace('__EP__', ep)

FAC = [('Años de actividad', 'Years teaching', 10), ('Oferta para principiantes', 'Beginner offer', 10), ('Eventos e invitados', 'Events and guests', 10),
       ('Valoración en Google', 'Google rating', 25), ('Número de reseñas', 'Number of reviews', 10), ('Redes sociales', 'Social media', 10)]
TBD = t("span", "Por confirmar", "To be confirmed")

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
    rows += f'<div class="sp-row"><b>{t("span", "Estilos (dominicana, sensual, moderna)", "Styles (Dominicana, Sensual, Moderna)")}</b> · {sty}</div>\n'
    for pl, en in (('Festivales', 'Festivals'), ('Reseñas recientes', 'Recent reviews'), ('Participación en concursos', 'Competitions entered'), ('Concursos ganados', 'Competitions won')):
        rows += f'<div class="sp-row"><b>{t("span", pl, en)}</b> · <span class="chip">{TBD}</span></div>\n'
    maps = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(f'{nm} {cpl}').replace('%20', '+')
    site = e['url']
    sitebtn = '' if 'google.com/maps' in site else f'<a class="btn btn-ghost" href="{site}" rel="noopener nofollow" target="_blank">{t("span", "Web de la escuela →", "School website →")}</a>'
    main = f'''
<section class="sp-hero" aria-labelledby="sp-title">
  <div class="wrap">
    <div>
      <p class="sp-crumb"><a href="/es/">{t("span", "Ranking España 2027", "Spain ranking 2027")}</a> › <a href="/es/bachata-{ck}.html">{cpl}</a></p>
      <span class="edition"><i></i>{t("span", "Clasificación provisional · no es el resultado final", "Interim standing · not final")}</span>
      <h1 id="sp-title">{nm}</h1>
      <p class="lede">{t("span", f"Escuela de bachata en {cpl}. Clasificación provisional: puesto {crank} en la ciudad ({cpl}), puesto {rank} en España. Las escuelas siguen compitiendo.", f"Bachata school in {cen}. Interim ranking: place {crank} in {cen}, place {rank} in Spain. Schools are still competing.")}</p>
      <div class="sp-links"><button type="button" class="btn btn-ghost" id="share">{t("span", "Compartir", "Share")}</button></div>
    </div>
    <div class="sp-score"><b>{f1(pts)}</b><small>/ 100 · {t("span", "provisional", "interim")}</small></div>
  </div>
</section>

<section class="block alt" aria-label="Details">
  <div class="wrap sp-grid">
    <div class="sp-card">
      {t("h2", "De qué se compone la puntuación", "How the score is made up")}
      {t("p", "Ya puntuamos seis de los nueve criterios (75 puntos como máximo). Lo que no hemos podido confirmar cuenta con el valor más bajo, y la escuela puede completarlo al inscribirse. Datos de octubre de 2026 (Google, Instagram, web de la escuela).", "Six of nine factors are scored so far (75 points at most). Anything we could not confirm counts at the lowest level, and a school can complete it in its application. Data as of October 2026 (Google, Instagram, school website).")}
      {rows}
      <div class="sp-links">{sitebtn}<a class="btn btn-ghost" href="{maps}" rel="noopener nofollow" target="_blank">{t("span", "Google Maps →", "Google Maps →")}</a></div>
    </div>
    <div class="sp-card">
      {t("h2", "Premio del público: vota", "Audience Award: vote")}
      {t("p", "Un voto por persona, confirmado por correo. El premio es independiente de los 100 puntos. El resultado se publicará junto con el ranking.", "One vote per person, confirmed by email. The award is separate from the 100 points. The result comes with the ranking.")}
      <button type="button" class="btn btn-gold" id="vbtn">&#9733; {t("span", "Votar por esta escuela", "Vote for this school")}</button>
      <form class="sp-form" id="vform" hidden novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <label>{t("span", "Tu correo electrónico", "Your email address")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {t("span", ES_S['news_opt'], "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{t("span", "Enviar mi voto", "Send my vote")}</button>
        <small>{t("span", ES_S['vote_note'], "One vote per person. We email you a confirmation link. We use your email only for that and to remove duplicate votes.")}</small>
      </form>
      <p class="sp-msg" id="vmsg" role="status" hidden></p>
    </div>
  </div>
</section>

<section class="block" aria-labelledby="rv-title">
  <div class="wrap sp-two">
    <div class="sp-card">
      <h2 id="rv-title">{t("span", "Reseñas", "Reviews")}</h2>
      <div class="sp-sum" id="rvsum"></div>
      <div id="rvlist"></div>
    </div>
    <div class="sp-card">
      {t("h2", "Escribe una reseña", "Write a review")}
      {t("p", "¿Has estado en esta escuela? Cuéntanos brevemente qué tal fue. Tu reseña aparece cuando haces clic en el enlace de nuestro correo. Escribe con honestidad y de forma objetiva.", "Have you been to this school? Tell us briefly how it was. Your review appears once you click the link in our email. Please stay factual and fair.")}
      <form class="sp-form" id="rvform" novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <div role="radiogroup" aria-label="Estrellas / Stars"><div class="sp-stars">
          <input type="radio" name="rating" value="5" id="st5"><label for="st5" title="5">★</label>
          <input type="radio" name="rating" value="4" id="st4"><label for="st4" title="4">★</label>
          <input type="radio" name="rating" value="3" id="st3"><label for="st3" title="3">★</label>
          <input type="radio" name="rating" value="2" id="st2"><label for="st2" title="2">★</label>
          <input type="radio" name="rating" value="1" id="st1"><label for="st1" title="1">★</label>
        </div></div>
        <label>{t("span", "Tu nombre (opcional)", "Your name (optional)")}<input type="text" name="name" maxlength="40" autocomplete="nickname"></label>
        <label>{t("span", "Tu reseña (de 10 a 600 caracteres, sin enlaces)", "Your review (10 to 600 characters, no links)")}<textarea name="text" maxlength="600" required></textarea></label>
        <label>{t("span", "Tu correo electrónico (no se publica)", "Your email address (not published)")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {t("span", ES_S['news_opt'], "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{t("span", "Enviar reseña", "Submit review")}</button>
      </form>
      <p class="sp-msg" id="rvmsg" role="status" hidden></p>
    </div>
  </div>
</section>

<section class="block alt" aria-labelledby="own-title">
  <div class="wrap">
    <div class="sp-card" style="max-width:760px">
      {t("h2", "¿Es tu escuela?", "Is this your school?").replace("<h2", '<h2 id="own-title"')}
      {t("p", "Puedes completar o corregir tus datos, por ejemplo festivales, concursos y año de fundación. Si no quieres aparecer en el ranking, escríbenos y retiraremos tu escuela.", "You can add or correct your data, for example festivals, competitions and founding year. If you do not want to be in the ranking, write to us and we will remove your school.")}
      <div class="sp-links"><a class="btn btn-gold" href="/bewerbung.html">{t("span", "Completar o corregir mis datos", "Add or correct my data")}</a><a class="btn btn-ghost" href="mailto:hello@latindanceawards.com?subject={urllib.parse.quote(nm)}">{t("span", "Escríbenos", "Write to us")}</a></div>
    </div>
  </div>
</section>
'''
    fn = f'es/escuelas/{slug}.html'
    schema = [crumbs(nm, fn), {"@context": "https://schema.org", "@type": "LocalBusiness", "name": nm, "url": site if 'google.com/maps' not in site else maps,
              "address": {"@type": "PostalAddress", "addressLocality": cpl, "addressCountry": "ES"}}]
    BE.es_page(fn, fn, f'{nm} · Bachata {cpl} · reseñas y valoración', f'{nm} en {cpl}: puntos, puesto {crank} en la clasificación provisional de bachata, reseñas y votación para el Premio del público.',
               f'{nm} · Bachata {cen} · Reviews', f'{nm} in {cen}: score, place {crank} in the interim Bachata ranking, reviews and voting for the Audience Award.',
               main, t.en, schema, js=school_js(nm, cpl))
    return fn

os.makedirs(os.path.join(B.ROOT, 'es', 'escuelas'), exist_ok=True)
files = [build(i, e, c) for i, (e, c) in enumerate(entries, 1)]
print('es school pages:', len(files), 'unique slugs:', len(set(files)))
