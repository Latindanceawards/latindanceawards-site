# One page per Polish school (pl/szkoly/<slug>.html), same layout as the German school pages. Run after build_pl.py.
import os, sys, re, io, json, contextlib, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import poland_data as P
import rank_variant as RV
from build import T, crumbs
import build_pl as BP
t = T('pl')

PL_S = {
 'vote_btn': 'Zagłosuj na tę szkołę', 'vote_mail': 'Twój adres e-mail', 'vote_send': 'Wyślij głos',
 'news_opt': 'Tak, wysyłajcie mi czasem wiadomości, wydarzenia i oferty związane z bachatą e-mailem. Wypisać się można w każdej chwili.',
 'vote_note': 'Jeden głos na osobę. Wyślemy Ci link potwierdzający. Twojego adresu e-mail używamy tylko do tego i do usuwania podwójnych głosów.',
 'vote_ok': 'Prawie gotowe: wysłaliśmy Ci e-mail. Kliknij w link, aby Twój głos się liczył. Sprawdź też folder ze spamem.',
 'vote_done': 'Na tym urządzeniu już głosowano. Dziękujemy!',
 'err_mail': 'Sprawdź adres e-mail i spróbuj ponownie.',
 'rv_ok': 'Prawie gotowe: wysłaliśmy Ci e-mail. Kliknij w link, a Twoja opinia pojawi się tutaj.',
 'rv_err': 'Wybierz gwiazdki i napisz od 10 do 600 znaków, bez linków i bez @.',
 'none': 'Nie ma jeszcze opinii. Bądź pierwszą osobą!', 'report': 'Zgłoś', 'anon': 'Anonim',
 'of': 'opinii', 'one': 'opinia', 'fail': 'Nie udało się wczytać opinii.', 'copied': 'Link skopiowany',
}
def school_js(nm, city_pl):
    js = B.SCHOOL_JS
    m = re.search(r'  var S = \{.*?\n  \};\n', js, re.S)
    blk = m.group(0)
    def rep(mm):
        k = mm.group(1)
        return f'{k}:[{json.dumps(PL_S[k], ensure_ascii=False)},{mm.group(3)}]' if k in PL_S else mm.group(0)
    blk2 = re.sub(r'(\w+):\[("(?:[^"\\]|\\.)*"),("(?:[^"\\]|\\.)*")\]', rep, blk)
    js = js.replace(blk, blk2)
    js = js.replace('window.LANG==="en"?"EN":"DE"', 'window.LANG==="en"?"EN":"PL"')
    ep = re.search(r'var VOTE_ENDPOINT = "([^"]+)"', B.rank_js).group(1)
    return js.replace('__SCHOOL__', json.dumps({'name': nm, 'city': city_pl}, ensure_ascii=False)).replace('__EP__', ep)

FAC = [('Lata działalności', 'Years teaching', 10), ('Oferta dla początkujących', 'Beginner offer', 10), ('Wydarzenia i gościnni instruktorzy', 'Events and guests', 10),
       ('Ocena w Google', 'Google rating', 25), ('Liczba opinii', 'Number of reviews', 10), ('Media społecznościowe', 'Social media', 10)]
TBD = t("span", "Do potwierdzenia", "To be confirmed")

entries = [(e, c) for c, es in RV.polish_entries(P).items() for e in es]
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
    rows += f'<div class="sp-row"><b>{t("span", "Style (Dominicana, Sensual, Moderna)", "Styles (Dominicana, Sensual, Moderna)")}</b> · {sty}</div>\n'
    for pl, en in (('Festiwale', 'Festivals'), ('Aktualne opinie', 'Recent reviews'), ('Udział w konkursach', 'Competitions entered'), ('Wygrane konkursy', 'Competitions won')):
        rows += f'<div class="sp-row"><b>{t("span", pl, en)}</b> · <span class="chip">{TBD}</span></div>\n'
    maps = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(f'{nm} {cpl}').replace('%20', '+')
    site = e['url']
    sitebtn = '' if 'google.com/maps' in site else f'<a class="btn btn-ghost" href="{site}" rel="noopener nofollow" target="_blank">{t("span", "Strona szkoły →", "School website →")}</a>'
    main = f'''
<section class="sp-hero" aria-labelledby="sp-title">
  <div class="wrap">
    <div>
      <p class="sp-crumb"><a href="/pl/">{t("span", "Ranking Polska 2027", "Poland ranking 2027")}</a> › <a href="/pl/bachata-{ck}.html">{cpl}</a></p>
      <span class="edition"><i></i>{t("span", "Stan przejściowy · nie wynik końcowy", "Interim standing · not final")}</span>
      <h1 id="sp-title">{nm}</h1>
      <p class="lede">{t("span", f"Szkoła bachaty: {cpl}. Stan przejściowy: miejsce {crank} w mieście ({cpl}), miejsce {rank} w Polsce. Szkoły wciąż rywalizują.", f"Bachata school in {cen}. Interim ranking: place {crank} in {cen}, place {rank} in Poland. Schools are still competing.")}</p>
      <div class="sp-links"><button type="button" class="btn btn-ghost" id="share">{t("span", "Udostępnij", "Share")}</button></div>
    </div>
    <div class="sp-score"><b>{f1(pts)}</b><small>/ 100 · {t("span", "stan przejściowy", "interim")}</small></div>
  </div>
</section>

<section class="block alt" aria-label="Details">
  <div class="wrap sp-grid">
    <div class="sp-card">
      {t("h2", "Z czego składa się wynik", "How the score is made up")}
      {t("p", "Sześć z dziewięciu kryteriów jest już liczonych (maks. 75 punktów). Czego nie potwierdziliśmy, liczy się na najniższym poziomie, a szkoła może to uzupełnić w zgłoszeniu. Stan danych: październik 2026 (Google, Instagram, strona szkoły).", "Six of nine factors are scored so far (75 points at most). Anything we could not confirm counts at the lowest level, and a school can complete it in its application. Data as of October 2026 (Google, Instagram, school website).")}
      {rows}
      <div class="sp-links">{sitebtn}<a class="btn btn-ghost" href="{maps}" rel="noopener nofollow" target="_blank">{t("span", "Mapy Google →", "Google Maps →")}</a></div>
    </div>
    <div class="sp-card">
      {t("h2", "Nagroda publiczności: zagłosuj", "Audience Award: vote")}
      {t("p", "Jeden głos na osobę, potwierdzony e-mailem. Nagroda jest niezależna od 100 punktów. Wynik ogłosimy razem z rankingiem.", "One vote per person, confirmed by email. The award is separate from the 100 points. The result comes with the ranking.")}
      <button type="button" class="btn btn-gold" id="vbtn">&#9733; {t("span", "Zagłosuj na tę szkołę", "Vote for this school")}</button>
      <form class="sp-form" id="vform" hidden novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <label>{t("span", "Twój adres e-mail", "Your email address")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {t("span", PL_S['news_opt'], "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{t("span", "Wyślij głos", "Send my vote")}</button>
        <small>{t("span", PL_S['vote_note'], "One vote per person. We email you a confirmation link. We use your email only for that and to remove duplicate votes.")}</small>
      </form>
      <p class="sp-msg" id="vmsg" role="status" hidden></p>
    </div>
  </div>
</section>

<section class="block" aria-labelledby="rv-title">
  <div class="wrap sp-two">
    <div class="sp-card">
      <h2 id="rv-title">{t("span", "Opinie", "Reviews")}</h2>
      <div class="sp-sum" id="rvsum"></div>
      <div id="rvlist"></div>
    </div>
    <div class="sp-card">
      {t("h2", "Napisz opinię", "Write a review")}
      {t("p", "Byłeś lub byłaś w tej szkole? Napisz krótko, jak było. Opinia pojawi się po kliknięciu w link z naszego e-maila. Pisz rzeczowo i uczciwie.", "Have you been to this school? Tell us briefly how it was. Your review appears once you click the link in our email. Please stay factual and fair.")}
      <form class="sp-form" id="rvform" novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <div role="radiogroup" aria-label="Gwiazdki / Stars"><div class="sp-stars">
          <input type="radio" name="rating" value="5" id="st5"><label for="st5" title="5">★</label>
          <input type="radio" name="rating" value="4" id="st4"><label for="st4" title="4">★</label>
          <input type="radio" name="rating" value="3" id="st3"><label for="st3" title="3">★</label>
          <input type="radio" name="rating" value="2" id="st2"><label for="st2" title="2">★</label>
          <input type="radio" name="rating" value="1" id="st1"><label for="st1" title="1">★</label>
        </div></div>
        <label>{t("span", "Twoje imię (opcjonalnie)", "Your name (optional)")}<input type="text" name="name" maxlength="40" autocomplete="nickname"></label>
        <label>{t("span", "Twoja opinia (10 do 600 znaków, bez linków)", "Your review (10 to 600 characters, no links)")}<textarea name="text" maxlength="600" required></textarea></label>
        <label>{t("span", "Twój adres e-mail (nie będzie publikowany)", "Your email address (not published)")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {t("span", PL_S['news_opt'], "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{t("span", "Wyślij opinię", "Submit review")}</button>
      </form>
      <p class="sp-msg" id="rvmsg" role="status" hidden></p>
    </div>
  </div>
</section>

<section class="block alt" aria-labelledby="own-title">
  <div class="wrap">
    <div class="sp-card" style="max-width:760px">
      {t("h2", "To Twoja szkoła?", "Is this your school?").replace("<h2", '<h2 id="own-title"')}
      {t("p", "Możesz uzupełnić lub poprawić dane, na przykład festiwale, konkursy i rok założenia. Jeśli nie chcesz być w rankingu, napisz do nas, a usuniemy Twoją szkołę.", "You can add or correct your data, for example festivals, competitions and founding year. If you do not want to be in the ranking, write to us and we will remove your school.")}
      <div class="sp-links"><a class="btn btn-gold" href="/bewerbung.html">{t("span", "Uzupełnij lub popraw dane", "Add or correct my data")}</a><a class="btn btn-ghost" href="mailto:hello@latindanceawards.com?subject={urllib.parse.quote(nm)}">{t("span", "Napisz do nas", "Write to us")}</a></div>
    </div>
  </div>
</section>
'''
    fn = f'pl/szkoly/{slug}.html'
    schema = [crumbs(nm, fn), {"@context": "https://schema.org", "@type": "LocalBusiness", "name": nm, "url": site if 'google.com/maps' not in site else maps,
              "address": {"@type": "PostalAddress", "addressLocality": cpl, "addressCountry": "PL"}}]
    BP.pl_page(fn, fn, f'{nm} · Bachata {cpl} · opinie i ocena', f'{nm} w mieście {cpl}: punkty, miejsce {crank} w stanie przejściowym rankingu bachaty, opinie i głosowanie na nagrodę publiczności.',
               f'{nm} · Bachata {cen} · Reviews', f'{nm} in {cen}: score, place {crank} in the interim Bachata ranking, reviews and voting for the Audience Award.',
               main, t.en, schema, js=school_js(nm, cpl))
    return fn

os.makedirs(os.path.join(B.ROOT, 'pl', 'szkoly'), exist_ok=True)
files = [build(i, e, c) for i, (e, c) in enumerate(entries, 1)]
print('pl school pages:', len(files))
