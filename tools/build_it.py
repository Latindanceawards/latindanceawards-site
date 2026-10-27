# Builds the Italy section (/it/) in Italian + English. Same structure and the same 100-point scoring as build_pl.py.
# Run after build.py/build_guides.py:  python3 tools/build_it.py
import os, sys, re, io, json, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
import italy_data as P
import rank_variant as RV
BASE = '/it/scuole/'
FULL = {e['name']: RV.total(e) for es in RV.polish_entries(P, BASE).values() for e in es}
from build import T, page, crumbs, faq_schema, ICON, ROOT
os.makedirs(os.path.join(ROOT, 'it'), exist_ok=True)

def f1(x): return f'{x:.1f}'.replace('.', ',')
def f1en(x): return f'{x:.1f}'
ranked = sorted(P.SCHOOLS, key=lambda s: (-FULL[s[0]], s[0]))
_TOP = [FULL[ranked[0][0]]]
def by_city(k): return [s for s in ranked if s[1] == k]

# ---------- Italian header / footer ----------
_ITH = B.HEADER
_ITH = _ITH.replace('<a class="brand" href="index.html"', '<a class="brand" href="/"', 1)
_ITH = re.sub(r'<ul id="mnav">.*?</ul>', '''<ul id="mnav">
        <li><a href="it/#ranking" data-i18n="sn1">Classifica</a></li>
        <li><a href="it/#citta" data-i18n="sn2">Città</a></li>
        <li><a href="it/#metodo" data-i18n="sn3">Metodo</a></li>
        <li><a href="index.html" data-i18n="sn4">Europa</a></li>
        <li><a href="deutschland.html" data-i18n="sn5">Germania</a></li>
      </ul>''', _ITH, count=1, flags=re.S)
_ITH = _ITH.replace('data-lang="de" aria-pressed="true">DE<', 'data-lang="de" aria-pressed="true">IT<')
_ITH = re.sub(r'<a class="btn btn-gold" href="bewerbung.html" data-i18n="t5">.*?</a>', '<a class="btn btn-gold" href="bewerbung.html?lang=en" data-i18n="sn6">Iscrivi la scuola</a>', _ITH, count=1)
_brand = re.search(r'<a class="brand" href="index.html">.*?</a>', B.FOOTER, re.S).group(0).replace('href="index.html"', 'href="/"', 1)
_ITF = f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        {_brand}
        <p class="indep" data-i18n="sf1">Progetto indipendente che celebra le scuole europee di ballo latino. Le classifiche si basano su dati pubblici e non si possono comprare.</p>
      </div>
      <div>
        <p class="fh" data-i18n="sf2">Rankings</p>
        <ul><li><a href="it/#ranking" data-i18n="sf3">Italia 2027</a></li><li><a href="it/#metodo" data-i18n="sf4">Come assegniamo i punti</a></li>{''.join(f'<li><a href="it/bachata-{k}.html">Bachata {v[0]}</a></li>' for k, v in list(P.CITIES.items())[:4])}<li><a href="index.html" data-i18n="sn4">Europa</a></li></ul>
      </div>
      <div>
        <p class="fh" data-i18n="sf5">Contatti</p>
        <ul><li><a href="bewerbung.html?lang=en" data-i18n="sn6">Iscrivi la scuola</a></li><li><a href="mailto:hello@latindanceawards.com">hello@latindanceawards.com</a></li><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li></ul>
      </div>
    </div>
    <div class="legal"><span>© 2026 Latin Dance Awards</span><span data-i18n="sf6">Edizione Bachata · Italia</span></div>
  </div>
</footer>'''

SHARED_ES_EN = {'sn1': 'Ranking', 'sn2': 'Cities', 'sn3': 'Method', 'sn4': 'Europe', 'sn5': 'Germany', 'sn6': 'Enter a school', 'sn7': 'Poland', 'sn8': 'Spain',
  'sf1': "An independent project celebrating Europe's Latin dance schools. Rankings are based on public data and can't be bought.",
  'sf2': 'Rankings', 'sf3': 'Italy 2027', 'sf4': 'How we score', 'sf5': 'Contact', 'sf6': 'Bachata Edition · Italy'}

def it_page(fname, canon, title, desc, title_en, desc_en, main, en, schema, js=''):
    oh, of = B.HEADER, B.FOOTER
    B.HEADER, B.FOOTER = _ITH, _ITF
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            B.SHARED_EN = dict(B.SHARED_EN); B.SHARED_EN.update(SHARED_ES_EN)
            page(fname, title, desc, title_en, desc_en, canon, main, en, js, schema=schema)
    finally:
        B.HEADER, B.FOOTER = oh, of
    fp = os.path.join(ROOT, fname); h = open(fp, encoding='utf-8').read()
    h = h.replace('<html lang="de">', '<html lang="it">', 1).replace('hreflang="de"', 'hreflang="it"').replace('document.documentElement.lang=l;', 'document.documentElement.lang=(l==="en"?"en":"it");')
    h = h.replace('og:locale" content="de_DE"', 'og:locale" content="it_IT"')
    open(fp, 'w', encoding='utf-8').write(h)
    print('wrote', fname)

def school_list(ss, t, start=1):
    lis = []
    for i, s in enumerate(ss, start):
        lis.append(f'<li><b>{i}</b><a href="{s[4]}" rel="nofollow noopener" target="_blank">{s[0]}</a><span>{f1(FULL[s[0]])} pt · {f1(s[2])} ★ ({s[3]})</span></li>')
    return '<ol class="top">' + ''.join(lis) + '</ol>'

def hero(t, edition, h1, lede, facts, ctas, seal='badge-bachata-italy-2027.svg', alt='Sigillo Bachata Awards Italia 2027'):
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
    return '<section class="block alt" id="faq"><div class="wrap"><div class="sec-head">' + t("h2", 'Domande frequenti', 'Frequently asked questions') + '</div><div class="faq">' + ''.join(f'<details>{t("summary", q, qe)}{t("p", a, ae)}</details>' for q, qe, a, ae in faq) + '</div></div></section>'

N = len(P.SCHOOLS); NC = len(P.CITIES)
METHOD_ES = ('Valutiamo le scuole come in Germania, con nove criteri e 100 punti: anni di attività, offerta per principianti, eventi, valutazione su Google, numero di recensioni e social media (75 punti in totale), più festival, recensioni recenti e concorsi (25 punti, per ora «da confermare»). I dati provengono dai siti delle scuole, da Google Maps e da Instagram. Ciò che non si può confermare conta con il valore più basso, e la scuola può completarlo iscrivendosi.',
             'We score schools exactly as in Germany, on nine factors and 100 points: years active, beginner offer, events, Google rating, number of reviews and social media (75 points together), plus festivals, recent reviews and competitions (25 points, still “to be confirmed”). The data comes from the schools’ websites, Google Maps and Instagram. Anything we cannot confirm counts at the lowest level, and a school can complete it in its application.')

# ---------- /it/ index ----------
t = T('it')
city_cards = ''.join(
    f'<article><h3>{t("span", "Bachata " + v[0], "Bachata " + v[1])}</h3>{t("p", f"{len(by_city(k))} scuole, in testa: {by_city(k)[0][0]}.", f"{len(by_city(k))} schools, led by {by_city(k)[0][0]}.")}<a href="/it/bachata-{k}.html">{t("span", "Scuole della città →", "Schools in this city →")}</a></article>'
    for k, v in P.CITIES.items())
main = hero(t, ('Edizione Bachata · Italia 2027', 'Bachata Edition · Italy 2027'),
  ('Le migliori scuole di bachata d’Italia: classifica 2027', 'The best Bachata schools in Italy: ranking 2027'),
  (f'Classifica indipendente delle scuole di bachata in {NC} città italiane, basata su dati pubblici. Pubblicheremo i risultati in primavera 2027.', f'An independent ranking of Bachata schools in {NC} Italian cities, based on public data. Results will be published in spring 2027.'),
  [('cal', f'<b>{N} scuole</b> in {NC} città', f'<b>{N} schools</b> in {NC} cities'), ('check', 'Indipendente, <b>non si compra</b>', 'Independent, <b>not for sale</b>'), ('clock', 'Risultati in <b>primavera 2027</b>', 'Results <b>spring 2027</b>')],
  f'<a class="btn btn-gold" href="#ranking">{t("span", "Vedi la classifica attuale", "See the current standings")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Iscrivi la tua scuola", "Enter your school")}</a>')
IT_C = RV.polish_entries(P, BASE)
TX = {k: list(v) if isinstance(v, list) else v for k, v in B.R_TEXT.items()}
TX['cities'] = {'italia': ['Tutta l’Italia', 'All Italy']}
TX['cities'].update({k: [v[0], v[1]] for k, v in P.CITIES.items()})
def _tx(k, es, en): TX[k] = [es, en]
_tx('title_city', 'Le migliori scuole di bachata: {c}', 'Best Bachata schools in {c}')
_tx('title_de', 'Le migliori scuole di bachata d’Italia', 'Best Bachata schools in Italy')
_tx('sub_interim', 'Classifica provvisoria: le posizioni possono ancora cambiare fino alla pubblicazione dei risultati in primavera 2027.', 'Interim standing: places can still change until the results are published in spring 2027.')
_tx('help_h', 'Come funziona la classifica?', 'How does the ranking work?')
_tx('help_p', 'Ogni scuola viene valutata con gli stessi criteri pubblici, uguali in tutti i paesi. Le posizioni non si possono comprare.', 'Every school is scored on the same public criteria, identical in every country. Places cannot be bought.')
_tx('help_how', 'Come assegniamo i punti', 'How scoring works')
_tx('help_add', 'Aggiungi la mia scuola', 'Add my school')
_tx('help_tips_h', 'Come migliorare la posizione della tua scuola', "How to improve your school's place")
TX['help_tips'] = [[
  'Cura la tua scheda Google e invita gli allievi a lasciare una recensione (valutazione Google 25 pt, numero di recensioni 10 pt, recensioni recenti 5 pt)',
  'Indica sul sito l’anno di fondazione, il team di insegnanti e i livelli dei corsi (anni di attività 10 pt)',
  'Offri una lezione di prova e gruppi fissi per principianti (offerta per principianti 10 pt)',
  'Organizza serate e workshop, invita insegnanti ospiti e mostralo online (eventi 10 pt)',
  'Tieni aggiornato il tuo Instagram (social media 10 pt)',
  'Conferma con un link i tuoi festival e concorsi (festival 15 pt, concorsi 5 pt)'], B.R_TEXT['help_tips'][1]]
_tx('pts', 'punti', 'points'); _tx('site', 'Sito', 'Website'); _tx('insta', 'Instagram', 'Instagram')
_tx('note_h', 'Manca la tua scuola?', 'Is your school missing?')
_tx('note_p', 'Iscrivi gratis la tua scuola alla classifica 2027.', 'Enter your school for the 2027 ranking for free.')
_tx('note_btn', 'Iscriviti gratis', 'Apply for free')
_tx('page_link', 'Pagina della scuola, recensioni e voto', 'School page, reviews and voting')
_tx('vote_h', 'Premio del pubblico', 'Audience Award')
_tx('vote_banner', 'Premio del pubblico: apri una scuola e vota. Un voto a persona, confermato via e-mail. È indipendente dai punti e il risultato sarà pubblicato insieme alla classifica.', 'Audience Award: open a school and vote. One vote per person, confirmed by email. It is separate from the points, and the result comes with the ranking.')
_tx('vote_btn', 'Vota questa scuola', 'Vote for this school')
_tx('vote_mail', 'La tua e-mail', 'Your email address')
_tx('vote_send', 'Invia il mio voto', 'Send my vote')
_tx('news_opt', 'Sì, voglio ricevere ogni tanto news, eventi e offerte sulla bachata via e-mail. Puoi annullare l’iscrizione in qualsiasi momento.', B.R_TEXT['news_opt'][1])
_tx('vote_note', 'Un voto a persona. Ti invieremo un link di conferma. Usiamo la tua e-mail solo per questo e per eliminare i voti doppi.', B.R_TEXT['vote_note'][1])
_tx('vote_ok', 'Quasi fatto: ti abbiamo inviato un’e-mail. Clicca sul link perché il tuo voto conti. Controlla anche lo spam.', B.R_TEXT['vote_ok'][1])
_tx('vote_err', 'Non ha funzionato. Controlla la tua e-mail e riprova.', B.R_TEXT['vote_err'][1])
_tx('vote_done', 'Da questo dispositivo si è già votato. Grazie!', B.R_TEXT['vote_done'][1])
_tx('prelim_badge', 'Classifica provvisoria · non è il risultato finale, le scuole stanno ancora gareggiando', 'Interim standing · not final, schools are still competing')
_tx('prelim_h', 'Come si calcola la classifica provvisoria', 'How the interim standing is calculated')
_tx('prelim_p', 'Calcoliamo i punti come in Germania: fino a 75 punti per sei criteri (anni di attività, offerta per principianti, eventi, valutazione su Google, numero di recensioni, social media) e fino a 25 punti per festival, recensioni recenti e concorsi, che sono ancora «da confermare». Dati: siti delle scuole, Google Maps e Instagram, aggiornati a ottobre 2026. Ciò che non è confermato conta con il valore più basso. Le posizioni possono ancora cambiare.', 'Points are calculated exactly as in Germany: up to 75 points for six factors (years active, beginner offer, events, Google rating, number of reviews, social media) and up to 25 points for festivals, recent reviews and competitions, which are still “to be confirmed”. Data: school websites, Google Maps and Instagram, status October 2026. Anything unconfirmed counts at the lowest level. Positions can still change.')
_tx('empty', 'Per questa città non ci sono ancora risultati.', 'There are no results for this city yet.')
_ES_TBC = ['Festival', 'Recensioni recenti', 'Concorsi a cui ha partecipato', 'Concorsi vinti']
_EN_TBC = ['Festivals', 'Recent reviews', 'Competitions entered', 'Competitions won']
_MX = ['15', '5', '5', '5']
_QUICK = ['italia', 'milano', 'roma', 'torino', 'bologna', 'napoli', 'firenze']
es_js = RV.make_js('italia', {}, TX, IT_C, _QUICK, 100, pl=True, code='IT', extra={
  'tbc': ([[n, m] for n, m in zip(_ES_TBC, _MX)], [[n, m] for n, m in zip(_EN_TBC, _MX)]),
  'literals': {
    '"Follower · Posts: "': '"Follower · post: "',
    '"Zu bestätigen"': '"Da confermare"',
    '"Noch ohne Punkte. Schulen bestätigen diese Angaben mit Links bei der Bewerbung."': '"Ancora senza punti. Le scuole confermano questi dati con dei link al momento dell’iscrizione."',
    '"Jetzt bestätigen"': '"Conferma ora"',
    '"Keine Stadt gefunden"': '"Nessuna città trovata"',
    '["Jahre im Unterricht","Einsteigerangebot","Events und Gastlehrer","Google-Bewertung","Anzahl Bewertungen","Social Media"]': '["Anni di insegnamento","Offerta per principianti","Eventi e ospiti","Valutazione su Google","Numero di recensioni","Social media"]',
    '"Alle "+pl.length+" Schulen anzeigen"': '"Vedi tutte le "+pl.length+" scuole"',
  }})
_tabs = RV.tabs_html(t, [(k, TX['cities'][k][0], TX['cities'][k][1]) for k in _QUICK])
RANK_SECTION = RV.ranking_section(_tabs, 'Cerca città …', 'Search city …', 'Città / Cities')
main += RANK_SECTION
main += f'''
{sec(t, 1, ("Bachata nelle città italiane", "Bachata in Italian cities"), '<div class="cards two" id="citta">' + city_cards + '</div>', alt=False).replace('<section class="block"', '<section class="block" id="citta-sec"')}
{sec(t, 2, ("Come valutiamo le scuole di bachata", "How we score Bachata schools"), t("p", *METHOD_ES) + t("p", 'La classifica si basa solo su dati pubblici. Le posizioni non si possono comprare e le eventuali menzioni a pagamento saranno segnalate come pubblicità e non influiscono sui punti. Raccogliamo noi stessi i dati delle scuole da Google Maps e dai loro siti, quindi possono contenere errori: <a href="/bewerbung.html?lang=en">iscrivi una scuola o inviaci una correzione</a>.', 'The ranking is based only on public data. Places cannot be bought, and paid mentions, if any, will be labelled as ads and do not affect points. We collect the school data ourselves from Google Maps and the schools\' websites, so it may contain errors: <a href="/bewerbung.html?lang=en">enter a school or send a correction</a>.'), alt=True).replace('<section class="block alt"', '<section class="block alt" id="metodo"')}
{sec(t, 3, ("Classifica europea e classifiche per paese", "Europe ranking and country rankings"), t("p", 'Latin Dance Awards crea una classifica delle scuole di tutta Europa e una classifica a parte per ogni paese. L’Italia si aggiunge a Germania, Polonia e Spagna. Guarda il <a href="/">panorama europeo</a>, la <a href="/deutschland.html">classifica della Germania</a>, quella della <a href="/pl/">Polonia</a> o quella della <a href="/es/">Spagna</a>.', 'Latin Dance Awards builds one ranking of schools across Europe plus a separate ranking for each country. Italy joins Germany, Poland and Spain. See the <a href="/">Europe overview</a>, the <a href="/deutschland.html">Germany ranking</a> or the <a href="/pl/">Poland ranking</a> or the <a href="/es/">Spain ranking</a>.'), alt=False)}
'''
faq = [
 ('Qual è la migliore scuola di bachata in Italia?', 'What is the best Bachata school in Italy?',
  f'Ad oggi, secondo i nostri dati, in testa c’è {ranked[0][0]} ({P.CITIES[ranked[0][1]][0]}) con {f1(_TOP[0])} punti su 100. È una classifica provvisoria; i risultati finali saranno pubblicati in primavera 2027.',
  f'As of today, by our data, {ranked[0][0]} ({P.CITIES[ranked[0][1]][1]}) leads with {f1en(_TOP[0])} of 100 points. This is an interim standing; final results come in spring 2027.'),
 ('Da dove arrivano i dati della classifica?', 'Where does the ranking data come from?',
  'Da fonti pubbliche: valutazione e numero di recensioni su Google Maps e i siti delle scuole stesse, dove verifichiamo che si insegni bachata.', 'From public sources: ratings and review counts on Google Maps and the schools\' own websites, where we check that the school teaches Bachata.'),
 ('Posso comprare una posizione in classifica?', 'Can I buy a place in the ranking?', 'No. Le posizioni non si possono comprare e le menzioni a pagamento non influiscono sui punti.', 'No. Places cannot be bought, and paid mentions do not affect points.'),
 ('Come iscrivo la mia scuola?', 'How do I enter my school?', 'Usa il <a href="/bewerbung.html?lang=en">modulo di iscrizione gratuito</a> (in inglese). Iscrivendoti puoi confermare i tuoi dati e ottenere il punteggio completo.', 'Use the <a href="/bewerbung.html?lang=en">free application form</a> (in English). Applying lets you confirm your details and receive the full score.'),
 ('Quali città copre la classifica?', 'Which cities does the ranking cover?', f'Per cominciare: {", ".join(v[0] for v in P.CITIES.values())}. Aggiungeremo altre città man mano che si iscrivono le scuole.', f'To start with: {", ".join(v[1] for v in P.CITIES.values())}. We will add more cities as schools apply.'),
]
main += faq_html(t, faq)
it_page('it/index.html', 'it/', 'Le migliori scuole di bachata d’Italia: classifica 2027',
  f'Classifica delle scuole di bachata in Italia: {N} scuole in {NC} città, con valutazioni, punti e metodo. Risultati in primavera 2027. Indipendente e non si compra.',
  'The best Bachata schools in Italy: 2027 ranking', f'Ranking of Bachata schools in Italy: {N} schools in {NC} cities with ratings, points and method. Results in spring 2027. Independent and not for sale.',
  main, t.en, [crumbs('Italia', 'it/'), faq_schema(faq)], js=es_js)

# ---------- city pages ----------
for k, (cpl, cen, loc) in P.CITIES.items():
    ss = by_city(k); n = len(ss); t = T('ic' + k[:2])
    ranks = {s[0]: ranked.index(s) + 1 for s in ss}
    cards = ''.join(f'<article><h3>{s[0]}</h3>{t("p", f"Valutazione su Google: {f1(s[2])} ★ ({s[3]} recensioni). Posizione {ranks[s[0]]} in Italia.", f"Google rating: {f1en(s[2])} ★ ({s[3]} reviews). Rank {ranks[s[0]]} in Italy.")}<a href="{s[4]}" rel="nofollow noopener" target="_blank">{t("span", "Sito della scuola", "School website")} →</a></article>' for s in ss)
    main = hero(t, (f'Bachata {cpl} · 2027', f'Bachata {cen} · 2027'),
      (f'Bachata {cpl}: le migliori scuole di ballo 2027', f'Bachata {cen}: the best dance schools 2027'),
      (f'Scuole di bachata {loc}: {n} posti con corsi confermati, con valutazioni Google e punti della classifica provvisoria. Risultati in primavera 2027.', f'Bachata schools in {cen}: {n} places with confirmed classes, with Google ratings and interim ranking points. Results in spring 2027.'),
      [('cal', f'<b>{n} scuole</b> {loc}', f'<b>{n} schools</b> in {cen}'), ('check', 'Dati di <b>ottobre 2026</b>', 'Data from <b>October 2026</b>')],
      f'<a class="btn btn-gold" href="#ranking">{t("span", "Vedi la classifica", "See the ranking")}</a><a class="btn btn-ghost" href="/bewerbung.html?lang=en">{t("span", "Iscrivi la tua scuola", "Enter your school")}</a>')
    main += f'''
<section class="block alt" id="ranking"><div class="wrap tp" style="max-width:860px">
  {t("h2", f"Classifica delle scuole di bachata {loc}", f"Ranking of Bachata schools in {cen}")}
  {t("p", f"Classifica provvisoria in base alle valutazioni Google di ottobre 2026 (max 100 punti). I risultati finali saranno pubblicati in primavera 2027.", "Interim standing by Google ratings as of October 2026 (max 100 points). The final results are published in spring 2027.", 'class="muted"')}
  <div class="box">{school_list(ss, t)}</div>
</div></section>
{sec(t, 1, (f"Scuole di bachata {loc} in breve", f"Bachata schools in {cen} at a glance"), t("p", f"Abbiamo trovato {n} scuole {loc} dove si insegna bachata. L’ordine si basa su punti provvisori, non su una valutazione completa. Orari, prezzi e gruppi cambiano, quindi controllali sul sito della scuola.", f"In {cen} we found {n} schools that teach Bachata. The order is based on interim points, not a full assessment. Times, prices and groups change, so check them on the school's website.") + '<div class="cards two">' + cards + '</div>', alt=False)}
{sec(t, 2, (f"Come scegliere un corso di bachata {loc}", f"How to choose a Bachata class in {cen}"), t("p", "Un buon corso di bachata si adatta al tuo livello, ai tuoi orari e al tuo tragitto. Questi consigli ti aiutano:", "A good Bachata class fits your level, schedule and journey. These tips help:") + '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in [
   ('<strong>Livello:</strong> inizia in un gruppo di principianti, anche se hai già ballato. Il passo base è la base di tutto.', '<strong>Level:</strong> start with a beginner group, even if you have danced before. The basic step is the base for everything.'),
   ('<strong>Lezione di prova:</strong> chiedi una lezione di prova o l’inizio di un nuovo gruppo prima di comprare un abbonamento.', '<strong>Trial class:</strong> ask for a trial class or a new group start before buying a pass.'),
   ('<strong>Partner:</strong> di solito non serve venire in coppia. Chiedi se i partner ruotano.', '<strong>Partner:</strong> you usually do not need to bring a partner. Ask whether partners rotate.'),
   ('<strong>Stile:</strong> bachata dominicana, moderna e sensual hanno un carattere diverso. Guarda quale stile insegna la scuola.', '<strong>Style:</strong> Dominicana, moderna and sensual bachata differ in character. Check which style the school teaches.')]) + '</ul>', alt=True)}
{sec(t, 3, ("Classifiche d’Italia, Europa e Germania", "Italy, Europe and Germany rankings"), t("p", 'Guarda la <a href="/it/">classifica di tutta l’Italia</a>, il <a href="/">panorama europeo</a> o la <a href="/deutschland.html">classifica della Germania</a>. Gestisci una scuola ' + loc + '? <a href="/bewerbung.html?lang=en">Iscrivila gratis</a>.', f'See the <a href="/it/">Italy ranking</a>, the <a href="/">Europe overview</a> or the <a href="/rankings.html">Germany ranking</a>. Do you run a school in {cen}? <a href="/bewerbung.html?lang=en">Enter it for free</a>.'), alt=False)}
'''
    top = ss[0]
    faq = [
     (f'Dove posso imparare la bachata {loc}?', f'Where can I learn Bachata in {cen}?', f'La bachata {loc} si insegna presso {", ".join(s[0] for s in ss[:3])} e altre scuole. L’elenco completo è qui sopra.', f'In {cen} Bachata is taught by {", ".join(s[0] for s in ss[:3])} and others. The full list is above.'),
     (f'Qual è la migliore scuola di bachata {loc}?', f'What is the best Bachata school in {cen}?', f'Ad oggi, secondo i nostri dati, in testa c’è {top[0]} ({f1(top[2])} ★, {top[3]} recensioni). È una classifica provvisoria, non quella finale.', f'As of today, by Google ratings, {top[0]} leads ({f1en(top[2])} ★, {top[3]} reviews). This is an interim standing, not the final ranking.'),
     ('Serve un partner per un corso di bachata?', 'Do I need a partner for a Bachata class?', 'Di solito no. In molte scuole i partner ruotano. Chiedilo prima della prima lezione.', 'Usually not. Many schools rotate partners. Ask before your first class.'),
     ('Con quale stile di bachata devo iniziare?', 'Which Bachata style should I start with?', 'La maggior parte dei principianti inizia con la bachata moderna o sensual. Contano il passo base e il ritmo; lo stile si può cambiare più avanti.', 'Most beginners start with moderna or sensual. What matters is the basic step and the rhythm, and you can change style later.'),
     ('Quando viene pubblicata la classifica completa?', 'When is the full ranking published?', 'In primavera 2027. Fino ad allora mostriamo una classifica provvisoria basata sulle valutazioni Google.', 'In spring 2027. Until then we show an interim standing based on Google ratings.'),
    ]
    main += faq_html(t, faq)
    it_page(f'it/bachata-{k}.html', f'it/bachata-{k}.html', f'Bachata {cpl}: le migliori scuole di ballo 2027',
      f'Bachata {cpl}: {n} scuole con valutazioni Google e punti della classifica 2027. Scegli un corso di bachata {loc} e consulta la classifica provvisoria.',
      f'Bachata {cen}: the best dance schools 2027', f'Bachata {cen}: {n} schools with Google ratings and 2027 ranking points. Choose a Bachata class in {cen} and see the interim ranking.',
      main, t.en, [crumbs(f'Bachata {cpl}', f'it/bachata-{k}.html'), faq_schema(faq)])
