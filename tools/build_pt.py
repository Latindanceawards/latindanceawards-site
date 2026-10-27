# Builds the Portugal section (/pt/) in Portuguese + English. Same structure and the same 100-point scoring as build_pl.py.
# Run after build.py/build_guides.py:  python3 tools/build_pt.py
import os, sys, re, io, json, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import portugal_data as P
import rank_variant as RV
BASE = '/pt/escolas/'
FULL = {e['name']: RV.total(e) for es in RV.polish_entries(P, BASE).values() for e in es}
from build import T, page, crumbs, faq_schema, ICON, ROOT
os.makedirs(os.path.join(ROOT, 'pt'), exist_ok=True)

def f1(x): return f'{x:.1f}'.replace('.', ',')
def f1en(x): return f'{x:.1f}'
ranked = sorted(P.SCHOOLS, key=lambda s: (-FULL[s[0]], s[0]))
_TOP = [FULL[ranked[0][0]]]
def by_city(k): return [s for s in ranked if s[1] == k]

# ---------- Portuguese header / footer ----------
_PTH = B.HEADER
_PTH = _PTH.replace('<a class="brand" href="index.html"', '<a class="brand" href="/"', 1)
_PTH = re.sub(r'<ul id="mnav">.*?</ul>', '''<ul id="mnav">
        <li><a href="pt/#ranking" data-i18n="sn1">Classificação</a></li>
        <li><a href="pt/#cidades" data-i18n="sn2">Cidades</a></li>
        <li><a href="pt/#metodo" data-i18n="sn3">Método</a></li>
        <li><a href="index.html" data-i18n="sn4">Europa</a></li>
        <li><a href="deutschland.html" data-i18n="sn5">Alemanha</a></li>
        <li><a href="pl/" data-i18n="sn7">Polónia</a></li>
        <li><a href="es/" data-i18n="sn8">Espanha</a></li>
        <li><a href="it/" data-i18n="sn9">Itália</a></li>
      </ul>''', _PTH, count=1, flags=re.S)
_PTH = _PTH.replace('data-lang="de" aria-pressed="true">DE<', 'data-lang="de" aria-pressed="true">PT<')
_PTH = re.sub(r'<a class="btn btn-gold" href="bewerbung.html" data-i18n="t5">.*?</a>', '<a class="btn btn-gold" href="bewerbung.html?lang=en" data-i18n="sn6">Inscrever escola</a>', _PTH, count=1)
_brand = re.search(r'<a class="brand" href="index.html">.*?</a>', B.FOOTER, re.S).group(0).replace('href="index.html"', 'href="/"', 1)
_PTF = f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        {_brand}
        <p class="indep" data-i18n="sf1">Projeto independente que celebra as escolas europeias de dança latina. As classificações baseiam-se em dados públicos e não se compram.</p>
      </div>
      <div>
        <p class="fh" data-i18n="sf2">Rankings</p>
        <ul><li><a href="pt/#ranking" data-i18n="sf3">Portugal 2027</a></li><li><a href="pt/#metodo" data-i18n="sf4">Como pontuamos</a></li>{''.join(f'<li><a href="pt/bachata-{k}.html">Bachata {v[0]}</a></li>' for k, v in list(P.CITIES.items())[:4])}<li><a href="index.html" data-i18n="sn4">Europa</a></li></ul>
      </div>
      <div>
        <p class="fh" data-i18n="sf5">Contacto</p>
        <ul><li><a href="bewerbung.html?lang=en" data-i18n="sn6">Inscrever escola</a></li><li><a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a></li><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li></ul>
      </div>
    </div>
    <div class="legal"><span>© 2026 Latin Dance Awards</span><span data-i18n="sf6">Edição Bachata · Portugal</span></div>
  </div>
</footer>'''

SHARED_ES_EN = {'sn1': 'Ranking', 'sn2': 'Cities', 'sn3': 'Method', 'sn4': 'Europe', 'sn5': 'Germany', 'sn6': 'Enter a school', 'sn7': 'Poland', 'sn8': 'Spain', 'sn9': 'Italy',
  'sf1': "An independent project celebrating Europe's Latin dance schools. Rankings are based on public data and can't be bought.",
  'sf2': 'Rankings', 'sf3': 'Portugal 2027', 'sf4': 'How we score', 'sf5': 'Contact', 'sf6': 'Bachata Edition · Portugal'}

def pt_page(fname, canon, title, desc, title_en, desc_en, main, en, schema, js=''):
    oh, of = B.HEADER, B.FOOTER
    B.HEADER, B.FOOTER = _PTH, _PTF
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            B.SHARED_EN = dict(B.SHARED_EN); B.SHARED_EN.update(SHARED_ES_EN)
            page(fname, title, desc, title_en, desc_en, canon, main, en, js, schema=schema)
    finally:
        B.HEADER, B.FOOTER = oh, of
    fp = os.path.join(ROOT, fname); h = open(fp, encoding='utf-8').read()
    h = h.replace('<html lang="de">', '<html lang="pt">', 1).replace('hreflang="de"', 'hreflang="pt"').replace('document.documentElement.lang=l;', 'document.documentElement.lang=(l==="en"?"en":"pt");')
    h = h.replace('og:locale" content="de_DE"', 'og:locale" content="pt_PT"')
    open(fp, 'w', encoding='utf-8').write(h)
    print('wrote', fname)

def school_list(ss, t, start=1):
    lis = []
    for i, s in enumerate(ss, start):
        lis.append(f'<li><b>{i}</b><a href="{s[4]}" rel="nofollow noopener" target="_blank">{s[0]}</a><span>{f1(FULL[s[0]])} pts · {f1(s[2])} ★ ({s[3]})</span></li>')
    return '<ol class="top">' + ''.join(lis) + '</ol>'

def hero(t, edition, h1, lede, facts, ctas, seal='badge-bachata-portugal-2027.svg', alt='Selo Bachata Awards Portugal 2027'):
    return f'''<section class="page-hero"><div class="wrap">
  <div>
    <span class="edition rise d1"><i></i>{t("span", *edition)}</span>
    <h1 class="rise d2">{t("span", *h1)}</h1>
    <p class="lede rise d3">{t("span", *lede)}</p>
    <div class="facts rise d4">{''.join(f'<span>{ICON[ic]}{t("span", d, e)}</span>' for ic, d, e in facts)}</div>
    <div class="ctas rise d5">{ctas}</div>
  </div>
  <div class="seal-box rise d3"><img class="seal" src="/{seal}" alt="{alt}" width="360" height="360" fetchpriority="low"></div>
</div></section>'''

def sec(t, i, h2, blocks, alt=True):
    return f'<section class="block{" alt" if alt else ""}"><div class="wrap prose">{t("h2", *h2)}{blocks}</div></section>'

def faq_html(t, faq):
    return '<section class="block alt" id="faq"><div class="wrap"><div class="sec-head">' + t("h2", 'Perguntas frequentes', 'Frequently asked questions') + '</div><div class="faq">' + ''.join(f'<details>{t("summary", q, qe)}{t("p", a, ae)}</details>' for q, qe, a, ae in faq) + '</div></div></section>'

N = len(P.SCHOOLS); NC = len(P.CITIES)
METHOD_ES = ('Pontuamos as escolas como na Alemanha, com nove critérios e 100 pontos: anos de atividade, oferta para principiantes, eventos, avaliação no Google, número de avaliações e redes sociais (75 pontos no total), mais festivais, avaliações recentes e concursos (25 pontos, por agora «por confirmar»). Os dados vêm dos sites das escolas, do Google Maps e do Instagram. O que não se consegue confirmar conta com o valor mais baixo, e a escola pode completá-lo ao inscrever-se.',
             'We score schools exactly as in Germany, on nine factors and 100 points: years active, beginner offer, events, Google rating, number of reviews and social media (75 points together), plus festivals, recent reviews and competitions (25 points, still “to be confirmed”). The data comes from the schools’ websites, Google Maps and Instagram. Anything we cannot confirm counts at the lowest level, and a school can complete it in its application.')

# ---------- /pt/ index ----------
t = T('pt')
city_cards = ''.join(
    f'<article><h3>{t("span", "Bachata " + v[0], "Bachata " + v[1])}</h3>{t("p", f"{len(by_city(k))} escolas, à frente: {by_city(k)[0][0]}.", f"{len(by_city(k))} schools, led by {by_city(k)[0][0]}.")}<a href="/pt/bachata-{k}.html">{t("span", "Escolas da cidade →", "Schools in this city →")}</a></article>'
    for k, v in P.CITIES.items())
main = hero(t, ('Edição Bachata · Portugal 2027', 'Bachata Edition · Portugal 2027'),
  ('As melhores escolas de bachata de Portugal: classificação 2027', 'The best Bachata schools in Portugal: ranking 2027'),
  (f'Classificação independente das escolas de bachata em {NC} cidades portuguesas, baseada em dados públicos. Publicaremos os resultados na primavera de 2027.', f'An independent ranking of Bachata schools in {NC} Portuguese cities, based on public data. Results will be published in spring 2027.'),
  [('cal', f'<b>{N} escolas</b> em {NC} cidades', f'<b>{N} schools</b> in {NC} cities'), ('check', 'Independente, <b>não se compra</b>', 'Independent, <b>not for sale</b>'), ('clock', 'Resultados na <b>primavera de 2027</b>', 'Results <b>spring 2027</b>')],
  f'<a class="btn btn-gold" href="#ranking">{t("span", "Ver a classificação atual", "See the current standings")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Inscreve a tua escola", "Enter your school")}</a>')
PT_C = RV.polish_entries(P, BASE)
TX = {k: list(v) if isinstance(v, list) else v for k, v in B.R_TEXT.items()}
TX['cities'] = {'portugal': ['Todo o Portugal', 'All Portugal']}
TX['cities'].update({k: [v[0], v[1]] for k, v in P.CITIES.items()})
def _tx(k, es, en): TX[k] = [es, en]
_tx('title_city', 'As melhores escolas de bachata: {c}', 'Best Bachata schools in {c}')
_tx('title_de', 'As melhores escolas de bachata de Portugal', 'Best Bachata schools in Portugal')
_tx('sub_interim', 'Classificação provisória: as posições ainda podem mudar até à publicação dos resultados na primavera de 2027.', 'Interim standing: places can still change until the results are published in spring 2027.')
_tx('help_h', 'Como funciona a classificação?', 'How does the ranking work?')
_tx('help_p', 'Cada escola é avaliada com os mesmos critérios públicos, iguais em todos os países. As posições não se compram.', 'Every school is scored on the same public criteria, identical in every country. Places cannot be bought.')
_tx('help_how', 'Como pontuamos', 'How scoring works')
_tx('help_add', 'Adicionar a minha escola', 'Add my school')
_tx('help_tips_h', 'Como melhorar a posição da tua escola', "How to improve your school's place")
TX['help_tips'] = [[
  'Cuida da tua ficha no Google e pede aos alunos que deixem uma avaliação (avaliação Google 25 pts, número de avaliações 10 pts, avaliações recentes 5 pts)',
  'Indica no site o ano de fundação, a equipa de professores e os níveis dos cursos (anos de atividade 10 pts)',
  'Oferece uma aula experimental e turmas fixas para principiantes (oferta para principiantes 10 pts)',
  'Organiza festas e workshops, convida professores e mostra-o online (eventos 10 pts)',
  'Mantém o teu Instagram atualizado (redes sociais 10 pts)',
  'Confirma com um link os teus festivais e concursos (festivais 15 pts, concursos 5 pts)'], B.R_TEXT['help_tips'][1]]
_tx('pts', 'pontos', 'points'); _tx('site', 'Site', 'Website'); _tx('insta', 'Instagram', 'Instagram')
_tx('note_h', 'Falta a tua escola?', 'Is your school missing?')
_tx('note_p', 'Inscreve gratuitamente a tua escola na classificação de 2027.', 'Enter your school for the 2027 ranking for free.')
_tx('note_btn', 'Inscrever grátis', 'Apply for free')
_tx('page_link', 'Página da escola, avaliações e voto', 'School page, reviews and voting')
_tx('vote_h', 'Prémio do público', 'Audience Award')
_tx('vote_banner', 'Prémio do público: abre uma escola e vota. Um voto por pessoa, confirmado por e-mail. É independente dos pontos e o resultado será publicado junto com a classificação.', 'Audience Award: open a school and vote. One vote per person, confirmed by email. It is separate from the points, and the result comes with the ranking.')
_tx('vote_btn', 'Votar nesta escola', 'Vote for this school')
_tx('vote_mail', 'O teu e-mail', 'Your email address')
_tx('vote_send', 'Enviar o meu voto', 'Send my vote')
_tx('news_opt', 'Sim, quero receber de vez em quando novidades, eventos e ofertas sobre bachata por e-mail. Podes cancelar a subscrição a qualquer momento.', B.R_TEXT['news_opt'][1])
_tx('vote_note', 'Um voto por pessoa. Vamos enviar-te uma ligação de confirmação. Usamos o teu e-mail apenas para isso e para eliminar votos duplicados.', B.R_TEXT['vote_note'][1])
_tx('vote_ok', 'Quase pronto: enviámos-te um e-mail. Clica na ligação para o teu voto contar. Verifica também o spam.', B.R_TEXT['vote_ok'][1])
_tx('vote_err', 'Não funcionou. Verifica o teu e-mail e tenta novamente.', B.R_TEXT['vote_err'][1])
_tx('vote_done', 'Já se votou neste dispositivo. Obrigado!', B.R_TEXT['vote_done'][1])
_tx('prelim_badge', 'Classificação provisória · não é o resultado final, as escolas continuam a competir', 'Interim standing · not final, schools are still competing')
_tx('prelim_h', 'Como se calcula a classificação provisória', 'How the interim standing is calculated')
_tx('prelim_p', 'Calculamos os pontos como na Alemanha: até 75 pontos por seis critérios (anos de atividade, oferta para principiantes, eventos, avaliação no Google, número de avaliações, redes sociais) e até 25 pontos por festivais, avaliações recentes e concursos, que ainda estão «por confirmar». Dados: sites das escolas, Google Maps e Instagram, a outubro de 2026. O que não está confirmado conta com o valor mais baixo. As posições ainda podem mudar.', 'Points are calculated exactly as in Germany: up to 75 points for six factors (years active, beginner offer, events, Google rating, number of reviews, social media) and up to 25 points for festivals, recent reviews and competitions, which are still “to be confirmed”. Data: school websites, Google Maps and Instagram, status October 2026. Anything unconfirmed counts at the lowest level. Positions can still change.')
_tx('empty', 'Ainda não há resultados para esta cidade.', 'There are no results for this city yet.')
_ES_TBC = ['Festivais', 'Avaliações recentes', 'Participação em concursos', 'Concursos ganhos']
_EN_TBC = ['Festivals', 'Recent reviews', 'Competitions entered', 'Competitions won']
_MX = ['15', '5', '5', '5']
_QUICK = ['portugal', 'lisboa', 'porto', 'faro', 'oeiras']
es_js = RV.make_js('portugal', {}, TX, PT_C, _QUICK, 100, pl=True, code='PT', extra={
  'tbc': ([[n, m] for n, m in zip(_ES_TBC, _MX)], [[n, m] for n, m in zip(_EN_TBC, _MX)]),
  'literals': {
    '"Follower · Posts: "': '"Seguidores · publicações: "',
    '"Zu bestätigen"': '"Por confirmar"',
    '"Noch ohne Punkte. Schulen bestätigen diese Angaben mit Links bei der Bewerbung."': '"Ainda sem pontos. As escolas confirmam estes dados com ligações ao inscrever-se."',
    '"Jetzt bestätigen"': '"Confirmar agora"',
    '"Keine Stadt gefunden"': '"Nenhuma cidade encontrada"',
    '["Jahre im Unterricht","Einsteigerangebot","Events und Gastlehrer","Google-Bewertung","Anzahl Bewertungen","Social Media"]': '["Anos de ensino","Oferta para principiantes","Eventos e convidados","Avaliação no Google","Número de avaliações","Redes sociais"]',
    '"Alle "+pl.length+" Schulen anzeigen"': '"Ver as "+pl.length+" escolas"',
  }})
_tabs = RV.tabs_html(t, [(k, TX['cities'][k][0], TX['cities'][k][1]) for k in _QUICK])
RANK_SECTION = RV.ranking_section(_tabs, 'Procurar cidade …', 'Search city …', 'Cidades / Cities')
main += RANK_SECTION
main += f'''
{sec(t, 1, ("Bachata nas cidades portuguesas", "Bachata in Portuguese cities"), '<div class="cards two" id="cidades">' + city_cards + '</div>', alt=False).replace('<section class="block"', '<section class="block" id="cidades-sec"')}
{sec(t, 2, ("Como avaliamos as escolas de bachata", "How we score Bachata schools"), t("p", *METHOD_ES) + t("p", 'A classificação baseia-se apenas em dados públicos. As posições não se compram e as eventuais menções pagas serão assinaladas como publicidade e não influenciam os pontos. Recolhemos nós próprios os dados das escolas no Google Maps e nos seus sites, pelo que podem conter erros: <a href="/bewerbung.html?lang=en">inscreve uma escola ou envia-nos uma correção</a>.', 'The ranking is based only on public data. Places cannot be bought, and paid mentions, if any, will be labelled as ads and do not affect points. We collect the school data ourselves from Google Maps and the schools\' websites, so it may contain errors: <a href="/bewerbung.html?lang=en">enter a school or send a correction</a>.'), alt=True).replace('<section class="block alt"', '<section class="block alt" id="metodo"')}
{sec(t, 3, ("Classificação europeia e classificações por país", "Europe ranking and country rankings"), t("p", 'A Latin Dance Awards cria uma classificação das escolas de toda a Europa e uma classificação à parte para cada país. Portugal junta-se à Alemanha, Polónia, Espanha e Itália. Vê o <a href="/">panorama europeu</a>, a <a href="/deutschland.html">classificação da Alemanha</a>, a da <a href="/es/">Espanha</a> ou a da <a href="/pt/">Itália</a>.', 'Latin Dance Awards builds one ranking of schools across Europe plus a separate ranking for each country. Portugal joins Germany, Poland, Spain and Italy. See the <a href="/">Europe overview</a>, the <a href="/deutschland.html">Germany ranking</a>, the <a href="/es/">Spain ranking</a> or the <a href="/pt/">Italy ranking</a>.'), alt=False)}
'''
faq = [
 ('Qual é a melhor escola de bachata de Portugal?', 'What is the best Bachata school in Portugal?',
  f'Até hoje, segundo os nossos dados, lidera {ranked[0][0]} ({P.CITIES[ranked[0][1]][0]}) com {f1(_TOP[0])} pontos em 100. É uma classificação provisória; os resultados finais serão publicados na primavera de 2027.',
  f'As of today, by our data, {ranked[0][0]} ({P.CITIES[ranked[0][1]][1]}) leads with {f1en(_TOP[0])} of 100 points. This is an interim standing; final results come in spring 2027.'),
 ('De onde vêm os dados da classificação?', 'Where does the ranking data come from?',
  'De fontes públicas: a avaliação e o número de avaliações no Google Maps e os sites das próprias escolas, onde verificamos que se ensina bachata.', 'From public sources: ratings and review counts on Google Maps and the schools\' own websites, where we check that the school teaches Bachata.'),
 ('Posso comprar uma posição na classificação?', 'Can I buy a place in the ranking?', 'Não. As posições não se compram e as menções pagas não influenciam os pontos.', 'No. Places cannot be bought, and paid mentions do not affect points.'),
 ('Como inscrevo a minha escola?', 'How do I enter my school?', 'Usa o <a href="/bewerbung.html?lang=en">formulário de inscrição gratuito</a> (em inglês). Ao inscrever-te podes confirmar os teus dados e obter a pontuação completa.', 'Use the <a href="/bewerbung.html?lang=en">free application form</a> (in English). Applying lets you confirm your details and receive the full score.'),
 ('Que cidades abrange a classificação?', 'Which cities does the ranking cover?', f'Para começar: {", ".join(v[0] for v in P.CITIES.values())}. Vamos acrescentar mais cidades à medida que as escolas se inscreverem.', f'To start with: {", ".join(v[1] for v in P.CITIES.values())}. We will add more cities as schools apply.'),
]
main += faq_html(t, faq)
pt_page('pt/index.html', 'pt/', 'As melhores escolas de bachata de Portugal: classificação 2027',
  f'Classificação das escolas de bachata em Portugal: {N} escolas em {NC} cidades, com avaliações, pontos e método. Resultados na primavera de 2027. Independente e não se compra.',
  'The best Bachata schools in Portugal: 2027 ranking', f'Ranking of Bachata schools in Portugal: {N} schools in {NC} cities with ratings, points and method. Results in spring 2027. Independent and not for sale.',
  main, t.en, [crumbs('Portugal', 'pt/'), faq_schema(faq)], js=es_js)

# ---------- city pages ----------
for k, (cpl, cen, loc) in P.CITIES.items():
    ss = by_city(k); n = len(ss); t = T('pc' + k[:2])
    ranks = {s[0]: ranked.index(s) + 1 for s in ss}
    cards = ''.join(f'<article><h3>{s[0]}</h3>{t("p", f"Avaliação no Google: {f1(s[2])} ★ ({s[3]} avaliações). Posição {ranks[s[0]]} em Portugal.", f"Google rating: {f1en(s[2])} ★ ({s[3]} reviews). Rank {ranks[s[0]]} in Portugal.")}<a href="{s[4]}" rel="nofollow noopener" target="_blank">{t("span", "Site da escola", "School website")} →</a></article>' for s in ss)
    main = hero(t, (f'Bachata {cpl} · 2027', f'Bachata {cen} · 2027'),
      (f'Bachata {cpl}: as melhores escolas de dança 2027', f'Bachata {cen}: the best dance schools 2027'),
      (f'Escolas de bachata {loc}: {n} locais com aulas confirmadas, com avaliações Google e pontos da classificação provisória. Resultados na primavera de 2027.', f'Bachata schools in {cen}: {n} places with confirmed classes, with Google ratings and interim ranking points. Results in spring 2027.'),
      [('cal', f'<b>{n} escolas</b> {loc}', f'<b>{n} schools</b> in {cen}'), ('check', 'Dados de <b>outubro de 2026</b>', 'Data from <b>October 2026</b>')],
      f'<a class="btn btn-gold" href="#ranking">{t("span", "Ver a classificação", "See the ranking")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Inscreve a tua escola", "Enter your school")}</a>')
    main += f'''
<section class="block alt" id="ranking"><div class="wrap tp" style="max-width:860px">
  {t("h2", f"Classificação das escolas de bachata {loc}", f"Ranking of Bachata schools in {cen}")}
  {t("p", f"Classificação provisória segundo as avaliações Google de outubro de 2026 (máx. 100 pontos). Os resultados finais serão publicados na primavera de 2027.", "Interim standing by Google ratings as of October 2026 (max 100 points). The final results are published in spring 2027.", 'class="muted"')}
  <div class="box">{school_list(ss, t)}</div>
</div></section>
{sec(t, 1, (f"Escolas de bachata {loc} num relance", f"Bachata schools in {cen} at a glance"), t("p", f"Encontrámos {n} escolas {loc} onde se ensina bachata. A ordem baseia-se em pontos provisórios, não numa avaliação completa. Horários, preços e turmas mudam, por isso consulta-os no site da escola.", f"In {cen} we found {n} schools that teach Bachata. The order is based on interim points, not a full assessment. Times, prices and groups change, so check them on the school's website.") + '<div class="cards two">' + cards + '</div>', alt=False)}
{sec(t, 2, (f"Como escolher um curso de bachata {loc}", f"How to choose a Bachata class in {cen}"), t("p", "Um bom curso de bachata adapta-se ao teu nível, ao teu horário e ao teu trajeto. Estas dicas ajudam:", "A good Bachata class fits your level, schedule and journey. These tips help:") + '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in [
   ('<strong>Nível:</strong> começa numa turma de principiantes, mesmo que já tenhas dançado. O passo básico é a base de tudo.', '<strong>Level:</strong> start with a beginner group, even if you have danced before. The basic step is the base for everything.'),
   ('<strong>Aula experimental:</strong> pergunta por uma aula experimental ou pelo início de uma nova turma antes de comprar um passe.', '<strong>Trial class:</strong> ask for a trial class or a new group start before buying a pass.'),
   ('<strong>Par:</strong> normalmente não é preciso vir a par. Pergunta se os pares rodam.', '<strong>Partner:</strong> you usually do not need to bring a partner. Ask whether partners rotate.'),
   ('<strong>Estilo:</strong> a bachata dominicana, a moderna e a sensual têm um carácter diferente. Vê que estilo ensina a escola.', '<strong>Style:</strong> Dominicana, moderna and sensual bachata differ in character. Check which style the school teaches.')]) + '</ul>', alt=True)}
{sec(t, 3, ("Classificações de Portugal, Europa e Alemanha", "Portugal, Europe and Germany rankings"), t("p", 'Vê a <a href="/pt/">classificação de todo o Portugal</a>, o <a href="/">panorama europeu</a> ou a <a href="/deutschland.html">classificação da Alemanha</a>. Diriges uma escola ' + loc + '? <a href="/bewerbung.html?lang=en">Inscreve-a gratuitamente</a>.', f'See the <a href="/pt/">Portugal ranking</a>, the <a href="/">Europe overview</a> or the <a href="/rankings.html">Germany ranking</a>. Do you run a school in {cen}? <a href="/bewerbung.html?lang=en">Enter it for free</a>.'), alt=False)}
'''
    top = ss[0]
    faq = [
     (f'Onde posso aprender bachata {loc}?', f'Where can I learn Bachata in {cen}?', f'A bachata {loc} ensina-se em {", ".join(s[0] for s in ss[:3])} e noutras escolas. A lista completa está acima.', f'In {cen} Bachata is taught by {", ".join(s[0] for s in ss[:3])} and others. The full list is above.'),
     (f'Qual é a melhor escola de bachata {loc}?', f'What is the best Bachata school in {cen}?', f'Até hoje, segundo os nossos dados, lidera {top[0]} ({f1(top[2])} ★, {top[3]} avaliações). É uma classificação provisória, não a final.', f'As of today, by Google ratings, {top[0]} leads ({f1en(top[2])} ★, {top[3]} reviews). This is an interim standing, not the final ranking.'),
     ('Preciso de par para um curso de bachata?', 'Do I need a partner for a Bachata class?', 'Normalmente não. Em muitas escolas os pares rodam. Pergunta antes da primeira aula.', 'Usually not. Many schools rotate partners. Ask before your first class.'),
     ('Com que estilo de bachata devo começar?', 'Which Bachata style should I start with?', 'A maioria dos principiantes começa com bachata moderna ou sensual. O que conta é o passo básico e o ritmo; o estilo pode mudar-se mais tarde.', 'Most beginners start with moderna or sensual. What matters is the basic step and the rhythm, and you can change style later.'),
     ('Quando é publicada a classificação completa?', 'When is the full ranking published?', 'Na primavera de 2027. Até lá mostramos uma classificação provisória baseada nas avaliações Google.', 'In spring 2027. Until then we show an interim standing based on Google ratings.'),
    ]
    main += faq_html(t, faq)
    pt_page(f'pt/bachata-{k}.html', f'pt/bachata-{k}.html', f'Bachata {cpl}: as melhores escolas de dança 2027',
      f'Bachata {cpl}: {n} escolas com avaliações Google e pontos da classificação 2027. Escolhe um curso de bachata {loc} e consulta a classificação provisória.',
      f'Bachata {cen}: the best dance schools 2027', f'Bachata {cen}: {n} schools with Google ratings and 2027 ranking points. Choose a Bachata class in {cen} and see the interim ranking.',
      main, t.en, [crumbs(f'Bachata {cpl}', f'pt/bachata-{k}.html'), faq_schema(faq)])
