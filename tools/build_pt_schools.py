# One page per Portuguese school (pt/escolas/<slug>.html), same layout as the Polish/German school pages. Run after build_pt.py.
import os, sys, re, io, json, contextlib, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import portugal_data as P
import rank_variant as RV
from build import T, crumbs
import build_pt as BE
t = T('pt')
BASE = '/pt/escolas/'

ES_S = {
 'vote_btn': 'Votar nesta escola', 'vote_mail': 'O teu e-mail', 'vote_send': 'Enviar o meu voto',
 'news_opt': 'Sim, quero receber de vez em quando novidades, eventos e ofertas sobre bachata por e-mail. Podes cancelar a subscrição a qualquer momento.',
 'vote_note': 'Um voto por pessoa. Vamos enviar-te uma ligação de confirmação. Usamos o teu e-mail apenas para isso e para eliminar votos duplicados.',
 'vote_ok': 'Quase pronto: enviámos-te um e-mail. Clica na ligação para o teu voto contar. Verifica também o spam.',
 'vote_done': 'Já se votou neste dispositivo. Obrigado!',
 'err_mail': 'Verifica o teu e-mail e tenta novamente.',
 'rv_ok': 'Quase pronto: enviámos-te um e-mail. Clica na ligação e a tua avaliação aparecerá aqui.',
 'rv_err': 'Escolhe as estrelas e escreve entre 10 e 600 caracteres, sem ligações nem @.',
 'none': 'Ainda não há avaliações. Sê a primeira pessoa!', 'report': 'Denunciar', 'anon': 'Anónimo',
 'of': 'avaliações', 'one': 'avaliação', 'fail': 'Não foi possível carregar as avaliações.', 'copied': 'Ligação copiada',
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
    js = js.replace('window.LANG==="en"?"EN":"DE"', 'window.LANG==="en"?"EN":"PT"')
    ep = re.search(r'var VOTE_ENDPOINT = "([^"]+)"', B.rank_js).group(1)
    return js.replace('__SCHOOL__', json.dumps({'name': nm, 'city': city}, ensure_ascii=False)).replace('__EP__', ep)

FAC = [('Anos de atividade', 'Years teaching', 10), ('Oferta para principiantes', 'Beginner offer', 10), ('Eventos e convidados', 'Events and guests', 10),
       ('Avaliação no Google', 'Google rating', 25), ('Número de avaliações', 'Number of reviews', 10), ('Redes sociais', 'Social media', 10)]
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
    for pl, en in (('Festivais', 'Festivals'), ('Avaliações recentes', 'Recent reviews'), ('Participação em concursos', 'Competitions entered'), ('Concursos ganhos', 'Competitions won')):
        rows += f'<div class="sp-row"><b>{t("span", pl, en)}</b> · <span class="chip">{TBD}</span></div>\n'
    maps = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(f'{nm} {cpl}').replace('%20', '+')
    site = e['url']
    sitebtn = '' if 'google.com/maps' in site else f'<a class="btn btn-ghost" href="{site}" rel="noopener nofollow" target="_blank">{t("span", "Site da escola →", "School website →")}</a>'
    main = f'''
<section class="sp-hero" aria-labelledby="sp-title">
  <div class="wrap">
    <div>
      <p class="sp-crumb"><a href="/pt/">{t("span", "Classificação Portugal 2027", "Portugal ranking 2027")}</a> › <a href="/pt/bachata-{ck}.html">{cpl}</a></p>
      <span class="edition"><i></i>{t("span", "Classificação provisória · não é o resultado final", "Interim standing · not final")}</span>
      <h1 id="sp-title">{nm}</h1>
      <p class="lede">{t("span", f"Escola de bachata em {cpl}. Classificação provisória: posição {crank} na cidade ({cpl}), posição {rank} em Portugal. As escolas continuam a competir.", f"Bachata school in {cen}. Interim ranking: place {crank} in {cen}, place {rank} in Portugal. Schools are still competing.")}</p>
      <div class="sp-links"><button type="button" class="btn btn-ghost" id="share">{t("span", "Partilhar", "Share")}</button></div>
    </div>
    <div class="sp-score"><b>{f1(pts)}</b><small>/ 100 · {t("span", "provisório", "interim")}</small></div>
  </div>
</section>

<section class="block alt" aria-label="Details">
  <div class="wrap sp-grid">
    <div class="sp-card">
      {t("h2", "Como se compõe a pontuação", "How the score is made up")}
      {t("p", "Por agora pontuamos seis dos nove critérios (no máximo 75 pontos). O que não conseguimos confirmar conta com o valor mais baixo, e a escola pode completá-lo ao inscrever-se. Dados de outubro de 2026 (Google, Instagram, site da escola).", "Six of nine factors are scored so far (75 points at most). Anything we could not confirm counts at the lowest level, and a school can complete it in its application. Data as of October 2026 (Google, Instagram, school website).")}
      {rows}
      <div class="sp-links">{sitebtn}<a class="btn btn-ghost" href="{maps}" rel="noopener nofollow" target="_blank">{t("span", "Google Maps →", "Google Maps →")}</a></div>
    </div>
    <div class="sp-card">
      {t("h2", "Prémio do público: vota", "Audience Award: vote")}
      {t("p", "Um voto por pessoa, confirmado por e-mail. O prémio é independente dos 100 pontos. O resultado será publicado junto com a classificação.", "One vote per person, confirmed by email. The award is separate from the 100 points. The result comes with the ranking.")}
      <button type="button" class="btn btn-gold" id="vbtn">&#9733; {t("span", "Votar nesta escola", "Vote for this school")}</button>
      <form class="sp-form" id="vform" hidden novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <label>{t("span", "O teu e-mail", "Your email address")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {t("span", ES_S['news_opt'], "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{t("span", "Enviar o meu voto", "Send my vote")}</button>
        <small>{t("span", ES_S['vote_note'], "One vote per person. We email you a confirmation link. We use your email only for that and to remove duplicate votes.")}</small>
      </form>
      <p class="sp-msg" id="vmsg" role="status" hidden></p>
    </div>
  </div>
</section>

<section class="block" aria-labelledby="rv-title">
  <div class="wrap sp-two">
    <div class="sp-card">
      <h2 id="rv-title">{t("span", "Avaliações", "Reviews")}</h2>
      <div class="sp-sum" id="rvsum"></div>
      <div id="rvlist"></div>
    </div>
    <div class="sp-card">
      {t("h2", "Escreve uma avaliação", "Write a review")}
      {t("p", "Estiveste nesta escola? Conta-nos brevemente como foi. A tua avaliação aparece quando clicares na ligação do nosso e-mail. Escreve com honestidade e de forma objetiva.", "Have you been to this school? Tell us briefly how it was. Your review appears once you click the link in our email. Please stay factual and fair.")}
      <form class="sp-form" id="rvform" novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <div role="radiogroup" aria-label="Estrelas / Stars"><div class="sp-stars">
          <input type="radio" name="rating" value="5" id="st5"><label for="st5" title="5">★</label>
          <input type="radio" name="rating" value="4" id="st4"><label for="st4" title="4">★</label>
          <input type="radio" name="rating" value="3" id="st3"><label for="st3" title="3">★</label>
          <input type="radio" name="rating" value="2" id="st2"><label for="st2" title="2">★</label>
          <input type="radio" name="rating" value="1" id="st1"><label for="st1" title="1">★</label>
        </div></div>
        <label>{t("span", "O teu nome (opcional)", "Your name (optional)")}<input type="text" name="name" maxlength="40" autocomplete="nickname"></label>
        <label>{t("span", "A tua avaliação (de 10 a 600 caracteres, sem ligações)", "Your review (10 to 600 characters, no links)")}<textarea name="text" maxlength="600" required></textarea></label>
        <label>{t("span", "O teu e-mail (não é publicado)", "Your email address (not published)")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {t("span", ES_S['news_opt'], "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{t("span", "Enviar avaliação", "Submit review")}</button>
      </form>
      <p class="sp-msg" id="rvmsg" role="status" hidden></p>
    </div>
  </div>
</section>

<section class="block alt" aria-labelledby="own-title">
  <div class="wrap">
    <div class="sp-card" style="max-width:760px">
      {t("h2", "É a tua escola?", "Is this your school?").replace("<h2", '<h2 id="own-title"')}
      {t("p", "Podes completar ou corrigir os teus dados, por exemplo festivais, concursos e ano de fundação. Se não queres aparecer na classificação, escreve-nos e retiraremos a tua escola.", "You can add or correct your data, for example festivals, competitions and founding year. If you do not want to be in the ranking, write to us and we will remove your school.")}
      <div class="sp-links"><a class="btn btn-gold" href="/bewerbung.html">{t("span", "Completar ou corrigir os meus dados", "Add or correct my data")}</a><a class="btn btn-ghost" href="mailto:hello@latindanceawards.com?subject={urllib.parse.quote(nm)}">{t("span", "Escreve-nos", "Write to us")}</a></div>
    </div>
  </div>
</section>
'''
    fn = f'pt/escolas/{slug}.html'
    schema = [crumbs(nm, fn), {"@context": "https://schema.org", "@type": "LocalBusiness", "name": nm, "url": site if 'google.com/maps' not in site else maps,
              "address": {"@type": "PostalAddress", "addressLocality": cpl, "addressCountry": "PT"}}]
    BE.pt_page(fn, fn, f'{nm} · Bachata {cpl} · avaliações e pontuação', f'{nm} em {cpl}: pontos, posição {crank} na classificação provisória de bachata, avaliações e voto para o Prémio do público.',
               f'{nm} · Bachata {cen} · Reviews', f'{nm} in {cen}: score, place {crank} in the interim Bachata ranking, reviews and voting for the Audience Award.',
               main, t.en, schema, js=school_js(nm, cpl))
    return fn

os.makedirs(os.path.join(B.ROOT, 'pt', 'escolas'), exist_ok=True)
files = [build(i, e, c) for i, (e, c) in enumerate(entries, 1)]
print('pt school pages:', len(files), 'unique slugs:', len(set(files)))
