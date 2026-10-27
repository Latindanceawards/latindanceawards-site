# Builds the France section (/fr/) in French + English. Same structure and the same 100-point scoring as build_pl.py.
# Run after build.py/build_guides.py:  python3 tools/build_fr.py
import os, sys, re, io, json, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import france_data as P
import rank_variant as RV
BASE = '/fr/ecoles/'
FULL = {e['name']: RV.total(e) for es in RV.polish_entries(P, BASE).values() for e in es}
from build import T, page, crumbs, faq_schema, ICON, ROOT
os.makedirs(os.path.join(ROOT, 'fr'), exist_ok=True)

def f1(x): return f'{x:.1f}'.replace('.', ',')
def f1en(x): return f'{x:.1f}'
ranked = sorted(P.SCHOOLS, key=lambda s: (-FULL[s[0]], s[0]))
_TOP = [FULL[ranked[0][0]]]
def by_city(k): return [s for s in ranked if s[1] == k]

# ---------- Portuguese header / footer ----------
_FRH = B.HEADER
_FRH = _FRH.replace('<a class="brand" href="index.html"', '<a class="brand" href="/"', 1)
_FRH = re.sub(r'<ul id="mnav">.*?</ul>', '''<ul id="mnav">
        <li><a href="fr/#ranking" data-i18n="sn1">Classement</a></li>
        <li><a href="fr/#villes" data-i18n="sn2">Villes</a></li>
        <li><a href="fr/#metodo" data-i18n="sn3">Méthode</a></li>
        <li><a href="index.html" data-i18n="sn4">Europe</a></li>
        <li><a href="deutschland.html" data-i18n="sn5">Allemagne</a></li>
        <li><a href="pl/" data-i18n="sn7">Pologne</a></li>
        <li><a href="es/" data-i18n="sn8">Espagne</a></li>
        <li><a href="it/" data-i18n="sn9">Italie</a></li>
        <li><a href="pt/" data-i18n="sn10">Portugal</a></li>
        <li><a href="nl/">Netherlands</a></li>
        <li><a href="uk/">UK</a></li>
        <li><a href="be/">Belgium</a></li>
        <li><a href="ie/">Ireland</a></li>
        <li><a href="at/">Austria</a></li>
        <li><a href="ch/">Switzerland</a></li>
        <li><a href="ee/">Eastern Europe</a></li>
        <li><a href="nd/">Nordics</a></li>
        <li><a href="em/">Eastern Mediterranean</a></li>
      </ul>''', _FRH, count=1, flags=re.S)
_FRH = _FRH.replace('data-lang="de" aria-pressed="true">DE<', 'data-lang="de" aria-pressed="true">FR<')
_FRH = re.sub(r'<a class="btn btn-gold" href="bewerbung.html" data-i18n="t5">.*?</a>', '<a class="btn btn-gold" href="bewerbung.html?lang=en" data-i18n="sn6">Inscrire une école</a>', _FRH, count=1)
_brand = re.search(r'<a class="brand" href="index.html">.*?</a>', B.FOOTER, re.S).group(0).replace('href="index.html"', 'href="/"', 1)
_FRF = f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        {_brand}
        <p class="indep" data-i18n="sf1">Projet indépendant qui met à l’honneur les écoles européennes de danse latine. Les classements reposent sur des données publiques et ne s’achètent pas.</p>
      </div>
      <div>
        <p class="fh" data-i18n="sf2">Rankings</p>
        <ul><li><a href="fr/#ranking" data-i18n="sf3">France 2027</a></li><li><a href="fr/#metodo" data-i18n="sf4">Comment nous notons</a></li>{''.join(f'<li><a href="fr/bachata-{k}.html">Bachata {v[0]}</a></li>' for k, v in list(P.CITIES.items())[:4])}<li><a href="index.html" data-i18n="sn4">Europa</a></li></ul>
      </div>
      <div>
        <p class="fh" data-i18n="sf5">Contact</p>
        <ul><li><a href="bewerbung.html?lang=en" data-i18n="sn6">Inscrire une école</a></li><li><a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a></li><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li></ul>
      </div>
    </div>
    <div class="legal"><span>© 2026 Latin Dance Awards</span><span data-i18n="sf6">Édition Bachata · France</span></div>
  </div>
</footer>'''

SHARED_ES_EN = {'sn1': 'Ranking', 'sn2': 'Cities', 'sn3': 'Method', 'sn4': 'Europe', 'sn5': 'Germany', 'sn6': 'Enter a school', 'sn7': 'Poland', 'sn8': 'Spain', 'sn9': 'Italy', 'sn10': 'Portugal',
  'sf1': "An independent project celebrating Europe's Latin dance schools. Rankings are based on public data and can't be bought.",
  'sf2': 'Rankings', 'sf3': 'France 2027', 'sf4': 'How we score', 'sf5': 'Contact', 'sf6': 'Bachata Edition · France'}

def fr_page(fname, canon, title, desc, title_en, desc_en, main, en, schema, js=''):
    oh, of = B.HEADER, B.FOOTER
    B.HEADER, B.FOOTER = _FRH, _FRF
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            B.SHARED_EN = dict(B.SHARED_EN); B.SHARED_EN.update(SHARED_ES_EN)
            page(fname, title, desc, title_en, desc_en, canon, main, en, js, schema=schema)
    finally:
        B.HEADER, B.FOOTER = oh, of
    fp = os.path.join(ROOT, fname); h = open(fp, encoding='utf-8').read()
    h = h.replace('<html lang="de">', '<html lang="fr">', 1).replace('hreflang="de"', 'hreflang="fr"').replace('document.documentElement.lang=l;', 'document.documentElement.lang=(l==="en"?"en":"fr");')
    h = h.replace('og:locale" content="de_DE"', 'og:locale" content="fr_FR"')
    open(fp, 'w', encoding='utf-8').write(h)
    print('wrote', fname)

def school_list(ss, t, start=1):
    lis = []
    for i, s in enumerate(ss, start):
        lis.append(f'<li><b>{i}</b><a href="{s[4]}" rel="nofollow noopener" target="_blank">{s[0]}</a><span>{f1(FULL[s[0]])} pts · {f1(s[2])} ★ ({s[3]})</span></li>')
    return '<ol class="top">' + ''.join(lis) + '</ol>'

def hero(t, edition, h1, lede, facts, ctas, seal='badge-bachata-france-2027.svg', alt='Sceau Bachata Awards France 2027'):
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
    return '<section class="block alt" id="faq"><div class="wrap"><div class="sec-head">' + t("h2", 'Questions fréquentes', 'Frequently asked questions') + '</div><div class="faq">' + ''.join(f'<details>{t("summary", q, qe)}{t("p", a, ae)}</details>' for q, qe, a, ae in faq) + '</div></div></section>'

N = len(P.SCHOOLS); NC = len(P.CITIES)
METHOD_ES = ('Nous notons les écoles comme en Allemagne, sur neuf critères et 100 points : années d’activité, offre pour débutants, événements, note Google, nombre d’avis et réseaux sociaux (75 points au total), plus festivals, avis récents et concours (25 points, pour l’instant « à confirmer »). Les données viennent des sites des écoles, de Google Maps et d’Instagram. Ce qui ne peut pas être confirmé compte avec la valeur la plus basse, et l’école peut le compléter en s’inscrivant.',
             'We score schools exactly as in Germany, on nine factors and 100 points: years active, beginner offer, events, Google rating, number of reviews and social media (75 points together), plus festivals, recent reviews and competitions (25 points, still “to be confirmed”). The data comes from the schools’ websites, Google Maps and Instagram. Anything we cannot confirm counts at the lowest level, and a school can complete it in its application.')

# ---------- /fr/ index ----------
t = T('fr')
city_cards = ''.join(
    f'<article><h3>{t("span", "Bachata " + v[0], "Bachata " + v[1])}</h3>{t("p", f"{len(by_city(k))} écoles, en tête : {by_city(k)[0][0]}.", f"{len(by_city(k))} schools, led by {by_city(k)[0][0]}.")}<a href="/fr/bachata-{k}.html">{t("span", "Écoles de la ville →", "Schools in this city →")}</a></article>'
    for k, v in P.CITIES.items())
main = hero(t, ('Édition Bachata · France 2027', 'Bachata Edition · France 2027'),
  ('Les meilleures écoles de bachata de France : classement 2027', 'The best Bachata schools in France: ranking 2027'),
  (f'Classement indépendant des écoles de bachata dans {NC} villes françaises, basé sur des données publiques. Nous publierons les résultats au printemps 2027.', f'An independent ranking of Bachata schools in {NC} French cities, based on public data. Results will be published in spring 2027.'),
  [('cal', f'<b>{N} écoles</b> dans {NC} villes', f'<b>{N} schools</b> in {NC} cities'), ('check', 'Indépendant, <b>ne s’achète pas</b>', 'Independent, <b>not for sale</b>'), ('clock', 'Résultats au <b>printemps 2027</b>', 'Results <b>spring 2027</b>')],
  f'<a class="btn btn-gold" href="#ranking">{t("span", "Voir le classement actuel", "See the current standings")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Inscrivez votre école", "Enter your school")}</a>')
FR_C = RV.polish_entries(P, BASE)
TX = {k: list(v) if isinstance(v, list) else v for k, v in B.R_TEXT.items()}
TX['cities'] = {'france': ['Toute la France', 'All France']}
TX['cities'].update({k: [v[0], v[1]] for k, v in P.CITIES.items()})
def _tx(k, es, en): TX[k] = [es, en]
_tx('title_city', 'Les meilleures écoles de bachata : {c}', 'Best Bachata schools in {c}')
_tx('title_de', 'Les meilleures écoles de bachata de France', 'Best Bachata schools in France')
_tx('sub_interim', 'Classement provisoire : les places peuvent encore changer jusqu’à la publication des résultats au printemps 2027.', 'Interim standing: places can still change until the results are published in spring 2027.')
_tx('help_h', 'Comment fonctionne le classement ?', 'How does the ranking work?')
_tx('help_p', 'Chaque école est évaluée selon les mêmes critères publics, identiques dans tous les pays. Les places ne s’achètent pas.', 'Every school is scored on the same public criteria, identical in every country. Places cannot be bought.')
_tx('help_how', 'Comment nous notons', 'How scoring works')
_tx('help_add', 'Ajouter mon école', 'Add my school')
_tx('help_tips_h', 'Comment améliorer la place de votre école', "How to improve your school's place")
TX['help_tips'] = [[
  'Soignez votre fiche Google et invitez vos élèves à laisser un avis (note Google 25 pts, nombre d’avis 10 pts, avis récents 5 pts)',
  'Indiquez sur votre site l’année de création, l’équipe de professeurs et les niveaux des cours (années d’activité 10 pts)',
  'Proposez un cours d’essai et des groupes fixes pour débutants (offre pour débutants 10 pts)',
  'Organisez des soirées et des stages, invitez des professeurs et montrez-le en ligne (événements 10 pts)',
  'Gardez votre Instagram à jour (réseaux sociaux 10 pts)',
  'Confirmez vos festivals et concours par un lien (festivals 15 pts, concours 5 pts)'], B.R_TEXT['help_tips'][1]]
_tx('pts', 'points', 'points'); _tx('site', 'Site', 'Website'); _tx('insta', 'Instagram', 'Instagram')
_tx('note_h', 'Votre école manque ?', 'Is your school missing?')
_tx('note_p', 'Inscrivez gratuitement votre école au classement 2027.', 'Enter your school for the 2027 ranking for free.')
_tx('note_btn', 'S’inscrire gratuitement', 'Apply for free')
_tx('page_link', 'Page de l’école, avis et vote', 'School page, reviews and voting')
_tx('vote_h', 'Prix du public', 'Audience Award')
_tx('vote_banner', 'Prix du public : ouvrez une école et votez. Un vote par personne, confirmé par e-mail. Il est indépendant des points et le résultat sera publié avec le classement.', 'Audience Award: open a school and vote. One vote per person, confirmed by email. It is separate from the points, and the result comes with the ranking.')
_tx('vote_btn', 'Voter pour cette école', 'Vote for this school')
_tx('vote_mail', 'Votre e-mail', 'Your email address')
_tx('vote_send', 'Envoyer mon vote', 'Send my vote')
_tx('news_opt', 'Oui, je souhaite recevoir de temps en temps des nouvelles, des événements et des offres sur la bachata par e-mail. Vous pouvez vous désabonner à tout moment.', B.R_TEXT['news_opt'][1])
_tx('vote_note', 'Un vote par personne. Nous vous enverrons un lien de confirmation. Nous utilisons votre e-mail uniquement pour cela et pour supprimer les votes en double.', B.R_TEXT['vote_note'][1])
_tx('vote_ok', 'Presque terminé : nous vous avons envoyé un e-mail. Cliquez sur le lien pour que votre vote compte. Vérifiez aussi vos courriers indésirables.', B.R_TEXT['vote_ok'][1])
_tx('vote_err', 'Cela n’a pas fonctionné. Vérifiez votre e-mail et réessayez.', B.R_TEXT['vote_err'][1])
_tx('vote_done', 'Un vote a déjà été enregistré depuis cet appareil. Merci !', B.R_TEXT['vote_done'][1])
_tx('prelim_badge', 'Classement provisoire · pas le résultat final, les écoles sont toujours en compétition', 'Interim standing · not final, schools are still competing')
_tx('prelim_h', 'Comment est calculé le classement provisoire', 'How the interim standing is calculated')
_tx('prelim_p', 'Nous calculons les points comme en Allemagne : jusqu’à 75 points pour six critères (années d’activité, offre pour débutants, événements, note Google, nombre d’avis, réseaux sociaux) et jusqu’à 25 points pour les festivals, les avis récents et les concours, encore « à confirmer ». Données : sites des écoles, Google Maps et Instagram, état d’octobre 2026. Ce qui n’est pas confirmé compte avec la valeur la plus basse. Les places peuvent encore changer.', 'Points are calculated exactly as in Germany: up to 75 points for six factors (years active, beginner offer, events, Google rating, number of reviews, social media) and up to 25 points for festivals, recent reviews and competitions, which are still “to be confirmed”. Data: school websites, Google Maps and Instagram, status October 2026. Anything unconfirmed counts at the lowest level. Positions can still change.')
_tx('empty', 'Aucun résultat pour cette ville pour le moment.', 'There are no results for this city yet.')
_ES_TBC = ['Festivals', 'Avis récents', 'Participation à des concours', 'Concours remportés']
_EN_TBC = ['Festivals', 'Recent reviews', 'Competitions entered', 'Competitions won']
_MX = ['15', '5', '5', '5']
_QUICK = ['france', 'paris', 'lyon', 'marseille', 'toulouse', 'strasbourg', 'montpellier']
es_js = RV.make_js('france', {}, TX, FR_C, _QUICK, 100, pl=True, code='FR', extra={
  'tbc': ([[n, m] for n, m in zip(_ES_TBC, _MX)], [[n, m] for n, m in zip(_EN_TBC, _MX)]),
  'literals': {
    '"Follower · Posts: "': '"Abonnés · publications : "',
    '"Zu bestätigen"': '"À confirmer"',
    '"Noch ohne Punkte. Schulen bestätigen diese Angaben mit Links bei der Bewerbung."': '"Pas encore de points. Les écoles confirment ces données par des liens lors de l’inscription."',
    '"Jetzt bestätigen"': '"Confirmer maintenant"',
    '"Keine Stadt gefunden"': '"Aucune ville trouvée"',
    '["Jahre im Unterricht","Einsteigerangebot","Events und Gastlehrer","Google-Bewertung","Anzahl Bewertungen","Social Media"]': '["Années d’enseignement","Offre pour débutants","Événements et invités","Note Google","Nombre d’avis","Réseaux sociaux"]',
    '"Alle "+pl.length+" Schulen anzeigen"': '"Voir les "+pl.length+" écoles"',
  }})
_tabs = RV.tabs_html(t, [(k, TX['cities'][k][0], TX['cities'][k][1]) for k in _QUICK])
RANK_SECTION = RV.ranking_section(_tabs, 'Rechercher une ville …', 'Search city …', 'Villes / Cities')
main += RANK_SECTION
main += f'''
{sec(t, 1, ("Bachata dans les villes françaises", "Bachata in French cities"), '<div class="cards two" id="villes">' + city_cards + '</div>', alt=False).replace('<section class="block"', '<section class="block" id="villes-sec"')}
{sec(t, 2, ("Comment nous évaluons les écoles de bachata", "How we score Bachata schools"), t("p", *METHOD_ES) + t("p", 'Le classement repose uniquement sur des données publiques. Les places ne s’achètent pas, et les éventuelles mentions payantes seront signalées comme publicité et n’influencent pas les points. Nous collectons nous-mêmes les données des écoles sur Google Maps et sur leurs sites, elles peuvent donc contenir des erreurs : <a href="/bewerbung.html?lang=en">inscrivez une école ou envoyez-nous une correction</a>.', 'The ranking is based only on public data. Places cannot be bought, and paid mentions, if any, will be labelled as ads and do not affect points. We collect the school data ourselves from Google Maps and the schools\' websites, so it may contain errors: <a href="/bewerbung.html?lang=en">enter a school or send a correction</a>.'), alt=True).replace('<section class="block alt"', '<section class="block alt" id="metodo"')}
{sec(t, 3, ("Classement européen et classements par pays", "Europe ranking and country rankings"), t("p", 'Latin Dance Awards établit un classement des écoles de toute l’Europe et un classement distinct pour chaque pays. La France rejoint l’Allemagne, la Pologne, l’Espagne, l’Italie et le Portugal. Voir l’<a href="/">aperçu de l’Europe</a>, le <a href="/deutschland.html">classement de l’Allemagne</a>, celui de l’<a href="/es/">Espagne</a> ou celui de l’<a href="/it/">Italie</a>.', 'Latin Dance Awards builds one ranking of schools across Europe plus a separate ranking for each country. France joins Germany, Poland, Spain, Italy and Portugal. See the <a href="/">Europe overview</a>, the <a href="/deutschland.html">Germany ranking</a>, the <a href="/es/">Spain ranking</a> or the <a href="/it/">Italy ranking</a>.'), alt=False)}
'''
faq = [
 ('Quelle est la meilleure école de bachata de France ?', 'What is the best Bachata school in France?',
  f'À ce jour, d’après nos données, {ranked[0][0]} ({P.CITIES[ranked[0][1]][0]}) est en tête avec {f1(_TOP[0])} points sur 100. C’est un classement provisoire ; les résultats définitifs seront publiés au printemps 2027.',
  f'As of today, by our data, {ranked[0][0]} ({P.CITIES[ranked[0][1]][1]}) leads with {f1en(_TOP[0])} of 100 points. This is an interim standing; final results come in spring 2027.'),
 ('D’où viennent les données du classement ?', 'Where does the ranking data come from?',
  'De sources publiques : la note et le nombre d’avis sur Google Maps et les sites des écoles elles-mêmes, où nous vérifions que la bachata est enseignée.', 'From public sources: ratings and review counts on Google Maps and the schools\' own websites, where we check that the school teaches Bachata.'),
 ('Puis-je acheter une place dans le classement ?', 'Can I buy a place in the ranking?', 'Non. Les places ne s’achètent pas et les mentions payantes n’influencent pas les points.', 'No. Places cannot be bought, and paid mentions do not affect points.'),
 ('Comment inscrire mon école ?', 'How do I enter my school?', 'Utilisez le <a href="/bewerbung.html?lang=en">formulaire d’inscription gratuit</a> (en anglais). En vous inscrivant, vous pouvez confirmer vos données et obtenir le score complet.', 'Use the <a href="/bewerbung.html?lang=en">free application form</a> (in English). Applying lets you confirm your details and receive the full score.'),
 ('Quelles villes le classement couvre-t-il ?', 'Which cities does the ranking cover?', f'Pour commencer : {", ".join(v[0] for v in P.CITIES.values())}. Nous ajouterons d’autres villes au fur et à mesure que les écoles s’inscrivent.', f'To start with: {", ".join(v[1] for v in P.CITIES.values())}. We will add more cities as schools apply.'),
]
main += faq_html(t, faq)
fr_page('fr/index.html', 'fr/', 'Les meilleures écoles de bachata de France : classement 2027',
  f'Classement des écoles de bachata en France : {N} écoles dans {NC} villes, avec notes, points et méthode. Résultats au printemps 2027. Indépendant et ne s’achète pas.',
  'The best Bachata schools in France: 2027 ranking', f'Ranking of Bachata schools in France: {N} schools in {NC} cities with ratings, points and method. Results in spring 2027. Independent and not for sale.',
  main, t.en, [crumbs('France', 'fr/'), faq_schema(faq)], js=es_js)

# ---------- city pages ----------
for k, (cpl, cen, loc) in P.CITIES.items():
    ss = by_city(k); n = len(ss); t = T('fc' + k[:2])
    ranks = {s[0]: ranked.index(s) + 1 for s in ss}
    cards = ''.join(f'<article><h3>{s[0]}</h3>{t("p", f"Note Google : {f1(s[2])} ★ ({s[3]} avis). Place {ranks[s[0]]} en France.", f"Google rating: {f1en(s[2])} ★ ({s[3]} reviews). Rank {ranks[s[0]]} in France.")}<a href="{s[4]}" rel="nofollow noopener" target="_blank">{t("span", "Site de l’école", "School website")} →</a></article>' for s in ss)
    main = hero(t, (f'Bachata {cpl} · 2027', f'Bachata {cen} · 2027'),
      (f'Bachata {cpl} : les meilleures écoles de danse 2027', f'Bachata {cen}: the best dance schools 2027'),
      (f'Écoles de bachata {loc} : {n} lieux avec cours confirmés, avec notes Google et points du classement provisoire. Résultats au printemps 2027.', f'Bachata schools in {cen}: {n} places with confirmed classes, with Google ratings and interim ranking points. Results in spring 2027.'),
      [('cal', f'<b>{n} écoles</b> {loc}', f'<b>{n} schools</b> in {cen}'), ('check', 'Données d’<b>octobre 2026</b>', 'Data from <b>October 2026</b>')],
      f'<a class="btn btn-gold" href="#ranking">{t("span", "Voir le classement", "See the ranking")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Inscrivez votre école", "Enter your school")}</a>')
    main += f'''
<section class="block alt" id="ranking"><div class="wrap tp" style="max-width:860px">
  {t("h2", f"Classement des écoles de bachata {loc}", f"Ranking of Bachata schools in {cen}")}
  {t("p", f"Classement provisoire selon les notes Google d’octobre 2026 (max. 100 points). Les résultats définitifs seront publiés au printemps 2027.", "Interim standing by Google ratings as of October 2026 (max 100 points). The final results are published in spring 2027.", 'class="muted"')}
  <div class="box">{school_list(ss, t)}</div>
</div></section>
{sec(t, 1, (f"Écoles de bachata {loc} en un coup d’œil", f"Bachata schools in {cen} at a glance"), t("p", f"Nous avons trouvé {n} écoles {loc} où l’on enseigne la bachata. L’ordre repose sur des points provisoires, pas sur une évaluation complète. Les horaires, tarifs et groupes changent, consultez donc le site de l’école.", f"In {cen} we found {n} schools that teach Bachata. The order is based on interim points, not a full assessment. Times, prices and groups change, so check them on the school's website.") + '<div class="cards two">' + cards + '</div>', alt=False)}
{sec(t, 2, (f"Comment choisir un cours de bachata {loc}", f"How to choose a Bachata class in {cen}"), t("p", "Un bon cours de bachata s’adapte à votre niveau, à vos horaires et à votre trajet. Ces conseils vous aideront :", "A good Bachata class fits your level, schedule and journey. These tips help:") + '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in [
   ('<strong>Niveau :</strong> commencez dans un groupe de débutants, même si vous avez déjà dansé. Le pas de base est la base de tout.', '<strong>Level:</strong> start with a beginner group, even if you have danced before. The basic step is the base for everything.'),
   ('<strong>Cours d’essai :</strong> demandez un cours d’essai ou le début d’un nouveau groupe avant d’acheter un forfait.', '<strong>Trial class:</strong> ask for a trial class or a new group start before buying a pass.'),
   ('<strong>Partenaire :</strong> en général, il n’est pas nécessaire de venir en couple. Demandez si les partenaires tournent.', '<strong>Partner:</strong> you usually do not need to bring a partner. Ask whether partners rotate.'),
   ('<strong>Style :</strong> la bachata dominicaine, moderne et sensual ont chacune leur caractère. Regardez quel style l’école enseigne.', '<strong>Style:</strong> Dominicana, moderna and sensual bachata differ in character. Check which style the school teaches.')]) + '</ul>', alt=True)}
{sec(t, 3, ("Classements de France, d’Europe et d’Allemagne", "France, Europe and Germany rankings"), t("p", 'Consultez le <a href="/fr/">classement de toute la France</a>, l’<a href="/">aperçu de l’Europe</a> ou le <a href="/deutschland.html">classement de l’Allemagne</a>. Vous dirigez une école ' + loc + ' ? <a href="/bewerbung.html?lang=en">Inscrivez-la gratuitement</a>.', f'See the <a href="/fr/">France ranking</a>, the <a href="/">Europe overview</a> or the <a href="/rankings.html">Germany ranking</a>. Do you run a school in {cen}? <a href="/bewerbung.html?lang=en">Enter it for free</a>.'), alt=False)}
'''
    top = ss[0]
    faq = [
     (f'Où apprendre la bachata {loc} ?', f'Where can I learn Bachata in {cen}?', f'La bachata {loc} s’enseigne chez {", ".join(s[0] for s in ss[:3])} et dans d’autres écoles. La liste complète est ci-dessus.', f'In {cen} Bachata is taught by {", ".join(s[0] for s in ss[:3])} and others. The full list is above.'),
     (f'Quelle est la meilleure école de bachata {loc} ?', f'What is the best Bachata school in {cen}?', f'À ce jour, d’après nos données, {top[0]} est en tête ({f1(top[2])} ★, {top[3]} avis). C’est un classement provisoire, pas le classement final.', f'As of today, by Google ratings, {top[0]} leads ({f1en(top[2])} ★, {top[3]} reviews). This is an interim standing, not the final ranking.'),
     ('Faut-il un partenaire pour un cours de bachata ?', 'Do I need a partner for a Bachata class?', 'En général, non. Dans beaucoup d’écoles, les partenaires tournent. Posez la question avant le premier cours.', 'Usually not. Many schools rotate partners. Ask before your first class.'),
     ('Par quel style de bachata commencer ?', 'Which Bachata style should I start with?', 'La plupart des débutants commencent par la bachata moderne ou sensual. Ce qui compte, c’est le pas de base et le rythme ; on peut changer de style plus tard.', 'Most beginners start with moderna or sensual. What matters is the basic step and the rhythm, and you can change style later.'),
     ('Quand le classement complet est-il publié ?', 'When is the full ranking published?', 'Au printemps 2027. D’ici là, nous affichons un classement provisoire basé sur les notes Google.', 'In spring 2027. Until then we show an interim standing based on Google ratings.'),
    ]
    main += faq_html(t, faq)
    fr_page(f'fr/bachata-{k}.html', f'fr/bachata-{k}.html', f'Bachata {cpl} : les meilleures écoles de danse 2027',
      f'Bachata {cpl} : {n} écoles avec notes Google et points du classement 2027. Choisissez un cours de bachata {loc} et consultez le classement provisoire.',
      f'Bachata {cen}: the best dance schools 2027', f'Bachata {cen}: {n} schools with Google ratings and 2027 ranking points. Choose a Bachata class in {cen} and see the interim ranking.',
      main, t.en, [crumbs(f'Bachata {cpl}', f'fr/bachata-{k}.html'), faq_schema(faq)])
