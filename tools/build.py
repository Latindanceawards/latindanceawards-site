# Builds bewerbung.html and rankings.html, reusing the homepage's styles, header and footer.
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
idx = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

HEAD_CSS = idx[idx.index('<style>') + 7: idx.index('</style>')]
HEADER = idx[idx.index('<header class="nav">'): idx.index('</header>') + 9]
FOOTER = idx[idx.index('<footer>'): idx.index('</footer>') + 9]
EN_INDEX = json.loads(re.search(r'var EN=(\{.*?\});\n', idx, re.S).group(1))

def fix_links(h):
    for a in ['#why', '#method', '#categories']:
        h = h.replace(f'href="{a}"', f'href="index.html{a}"')
    return h.replace('href="#top"', 'href="index.html"')

HEADER = fix_links(HEADER)
FOOTER = fix_links(FOOTER)
SHARED_KEYS = set(re.findall(r'data-i18n="([^"]+)"', HEADER + FOOTER))
SHARED_EN = {k: EN_INDEX[k] for k in SHARED_KEYS if k in EN_INDEX}

PAGE_CSS = r'''
/* ---------- subpages ---------- */
.page-hero{position:relative;overflow:hidden;padding:110px 0 90px;
  background:radial-gradient(ellipse 55% 60% at 80% 20%,rgba(228,185,91,.10),transparent 60%),linear-gradient(180deg,var(--velvet-deep),var(--velvet))}
.page-hero .wrap{position:relative;display:grid;grid-template-columns:1.25fr .75fr;gap:50px;align-items:center}
.page-hero h1{font-family:var(--serif);font-weight:500;font-size:clamp(38px,5.2vw,72px);line-height:1.04;letter-spacing:-.015em;margin:24px 0 22px}
.page-hero h1 em{font-style:italic;font-weight:400}
.page-hero p.lede{font-size:19px;color:var(--muted);max-width:32em}
.page-hero .ctas{display:flex;flex-wrap:wrap;gap:14px;margin-top:34px}
.page-hero .seal{width:min(360px,80vw);justify-self:center;filter:drop-shadow(0 30px 60px rgba(0,0,0,.55))}
.page-hero .seal-cap{text-align:center;color:var(--muted);font-size:14px;margin-top:6px}
.facts{display:flex;flex-wrap:wrap;gap:12px;margin-top:34px}
.facts > span{display:inline-flex;align-items:center;gap:9px;padding:10px 16px;border-radius:999px;background:var(--card);border:1px solid var(--line);font-size:14.5px}
.facts b{color:var(--gold-light);font-weight:700}
.facts svg{width:18px;height:18px;color:var(--gold);flex:none}

.block{padding:110px 0}
.block.alt{background:var(--velvet)}

/* steps */
.steps{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.step{position:relative;padding:30px 26px 28px;border-radius:22px;background:var(--card);border:1px solid var(--line)}
.step .num{width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:var(--gold-soft);color:var(--gold-light);
  font-family:var(--serif);font-size:22px;font-weight:600;margin-bottom:20px}
.step .when{display:block;font-size:13px;font-weight:700;color:var(--gold);margin-bottom:6px}
.step h3{font-family:var(--serif);font-weight:500;font-size:25px;line-height:1.15;margin-bottom:8px}
.step p{color:var(--muted);font-size:15.5px}

/* checklist */
.need{display:grid;grid-template-columns:repeat(2,1fr);gap:14px 34px;list-style:none;max-width:980px}
.need li{display:grid;grid-template-columns:28px 1fr;gap:12px;padding:16px 20px;border-radius:16px;background:var(--card);border:1px solid var(--line);font-size:16px}
.need li svg{width:22px;height:22px;color:var(--gold);margin-top:2px}
.need li small{display:block;color:var(--muted);font-size:14px}
.need li em{font-style:normal;color:var(--gold-light);font-size:13px;font-weight:600}

/* form */
.form-card{max-width:860px;border-radius:28px;padding:44px;background:linear-gradient(170deg,var(--gold-soft),var(--card) 45%);border:1px solid rgba(228,185,91,.4)}
.form-card h2{font-family:var(--serif);font-weight:500;font-size:clamp(30px,3.6vw,44px);line-height:1.1;margin-bottom:10px}
.form-card > p{color:var(--muted);margin-bottom:28px}
.form-card iframe{width:100%;min-height:520px;border:0;border-radius:18px;background:transparent}
.form-fallback{padding:34px;border-radius:20px;border:1px dashed rgba(228,185,91,.45);text-align:center}
.form-fallback p{color:var(--muted);margin:0 auto 22px;max-width:30em}

/* faq */
.faq{display:grid;gap:12px;max-width:860px}
.faq details{border-radius:18px;background:var(--card);border:1px solid var(--line);transition:border-color .3s}
.faq details[open]{border-color:rgba(228,185,91,.45)}
.faq summary{cursor:pointer;list-style:none;padding:22px 26px;font-weight:600;font-size:17px;display:flex;justify-content:space-between;gap:20px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:24px;line-height:1;color:var(--gold);transition:transform .3s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{padding:0 26px 24px;color:var(--muted)}
.faq a{color:var(--gold-light)}

/* countdown */
.countdown{display:flex;gap:12px;margin-top:34px;flex-wrap:wrap}
.countdown div{min-width:96px;padding:18px 10px 14px;text-align:center;border-radius:20px;background:var(--card);border:1px solid var(--line)}
.countdown b{display:block;font-family:var(--serif);font-weight:500;font-size:44px;line-height:1;color:var(--gold-light);font-variant-numeric:tabular-nums}
.countdown small{display:block;margin-top:8px;font-size:13px;color:var(--muted)}

/* tabs */
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:40px}
.tabs button{font:inherit;font-size:15px;font-weight:600;color:var(--muted);background:var(--card);border:1px solid var(--line);
  padding:11px 20px;border-radius:999px;cursor:pointer;transition:all .25s}
.tabs button:hover{color:var(--cream);border-color:rgba(228,185,91,.45)}
.tabs button[aria-selected="true"]{background:var(--gold);color:var(--velvet-deep);border-color:var(--gold)}
.panel-title{font-family:var(--serif);font-weight:500;font-size:clamp(28px,3.4vw,42px);line-height:1.1;margin-bottom:8px}
.panel-sub{color:var(--muted);margin-bottom:40px}

/* podium */
.podium3{display:grid;grid-template-columns:1fr 1.15fr 1fr;gap:16px;align-items:end;margin-bottom:26px}
.pod{position:relative;border-radius:24px;padding:28px 22px 26px;text-align:center;background:var(--card);border:1px solid var(--line)}
.pod.p1{padding-top:40px;padding-bottom:40px;background:linear-gradient(170deg,var(--gold-soft),var(--card) 60%);border-color:rgba(228,185,91,.55)}
.pod .medal-n{width:58px;height:58px;margin:0 auto 18px;border-radius:50%;display:grid;place-items:center;font-family:var(--serif);font-weight:600;font-size:26px;color:#131011}
.pod.p1 .medal-n{width:70px;height:70px;font-size:32px;background:var(--foil)}
.pod.p2 .medal-n{background:linear-gradient(135deg,#F2F2F2,#A9ADB4)}
.pod.p3 .medal-n{background:linear-gradient(135deg,#E8B58A,#9C5F34)}
.pod h3{font-family:var(--serif);font-weight:500;font-size:22px;line-height:1.2;min-height:1.2em}
.pod .sc{margin-top:8px;font-size:15px;color:var(--muted)}
.pod .sc b{font-family:var(--serif);font-size:30px;color:var(--gold-light);font-weight:500}
.pod a{text-decoration:none}
.blur{display:block;height:16px;border-radius:8px;margin:10px auto;background:linear-gradient(90deg,rgba(255,255,255,.06),rgba(255,255,255,.14),rgba(255,255,255,.06));background-size:200% 100%;animation:shimmer 2.4s linear infinite}
@keyframes shimmer{to{background-position:-200% 0}}
.lock{display:inline-flex;align-items:center;gap:8px;margin-top:14px;font-size:13px;font-weight:600;color:var(--gold)}
.lock svg{width:15px;height:15px}

/* ranking list */
.rlist{list-style:none;display:grid;gap:10px}
.rrow{border-radius:18px;background:var(--card);border:1px solid var(--line)}
.rrow summary,.rrow .rr{display:grid;grid-template-columns:54px 1fr auto 26px;gap:16px;align-items:center;padding:16px 22px;cursor:pointer;list-style:none}
.rrow summary::-webkit-details-marker{display:none}
.rrow .pos{font-family:var(--serif);font-size:22px;color:var(--gold);font-weight:600}
.rrow .nm{font-weight:600}
.rrow .nm small{display:block;font-weight:400;color:var(--muted);font-size:13.5px}
.rrow .pts{font-family:var(--serif);font-size:24px;color:var(--gold-light)}
.rrow summary::after{content:"+";color:var(--gold);font-size:22px;transition:transform .3s;text-align:right}
.rrow[open] summary::after{transform:rotate(45deg)}
.rrow .rr{cursor:default;grid-template-columns:54px 1fr}
.breakdown{display:grid;grid-template-columns:repeat(3,1fr);gap:12px 26px;padding:6px 22px 22px 92px}
.breakdown div{font-size:13.5px;color:var(--muted)}
.breakdown div b{color:var(--cream);font-weight:600}
.breakdown .bar{height:5px;border-radius:5px;background:rgba(246,231,211,.1);margin-top:6px;overflow:hidden}
.breakdown .bar i{display:block;height:100%;border-radius:5px;background:var(--gold)}
.breakdown .links{grid-column:1/-1;display:flex;gap:16px}
.breakdown .links a{color:var(--gold-light);font-weight:600}
.preview-note{display:inline-flex;margin-bottom:24px;padding:8px 16px;border-radius:999px;background:var(--gold);color:#131011;font-size:13px;font-weight:700}
.note-card{margin-top:36px;padding:30px 32px;border-radius:22px;background:var(--card);border:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap}
.note-card h3{font-family:var(--serif);font-weight:500;font-size:26px;margin-bottom:4px}
.note-card p{color:var(--muted)}

@media (max-width:960px){
  .page-hero .wrap{grid-template-columns:1fr}
  .page-hero .seal-box{order:-1}
  .page-hero .seal{width:min(260px,70vw)}
  .steps{grid-template-columns:1fr 1fr}
  .need{grid-template-columns:1fr}
  .breakdown{grid-template-columns:1fr 1fr;padding-left:22px}
}
@media (max-width:620px){
  .page-hero{padding:70px 0 70px}
  .block{padding:80px 0}
  .steps{grid-template-columns:1fr}
  .form-card{padding:26px 20px}
  .countdown div{min-width:0;flex:1}
  .countdown b{font-size:32px}
  .podium3{grid-template-columns:1fr}
  .pod.p1{order:-1}
  .rrow summary,.rrow .rr{grid-template-columns:38px 1fr auto 18px;padding:14px 16px;gap:10px}
  .rrow .rr{grid-template-columns:38px 1fr}
  .breakdown{grid-template-columns:1fr;padding:4px 16px 18px}
  .page-hero .ctas .btn{flex:1 1 100%}
}
'''

LANG_JS = r'''
  var DE={}, nodes=document.querySelectorAll("[data-i18n]");
  nodes.forEach(function(el){ DE[el.dataset.i18n]=el.innerHTML; });
  window.LANG="de";
  function setLang(l){
    window.LANG=l;
    nodes.forEach(function(el){ var k=el.dataset.i18n; el.innerHTML = l==="en" ? (EN[k]||DE[k]) : DE[k]; });
    document.documentElement.lang=l;
    document.title=META[l].title;
    document.querySelector('meta[name="description"]').content=META[l].desc;
    document.querySelectorAll(".lang button").forEach(function(b){ b.setAttribute("aria-pressed", b.dataset.lang===l ? "true":"false"); });
    try{ localStorage.setItem("lda-lang",l); }catch(e){}
    document.dispatchEvent(new CustomEvent("langchange",{detail:l}));
  }
  document.querySelectorAll(".lang button").forEach(function(b){ b.addEventListener("click",function(){ setLang(b.dataset.lang); }); });
  var start="de";
  try{ var q=new URLSearchParams(location.search).get("lang"); if(q==="en"||q==="de") start=q; else if(localStorage.getItem("lda-lang")) start=localStorage.getItem("lda-lang"); }catch(e){}
  META.de={title:document.title, desc:document.querySelector('meta[name="description"]').content};
'''

def page(fname, title_de, desc_de, title_en, desc_en, canonical, main_html, en_dict, page_js):
    en = dict(SHARED_EN); en.update(en_dict)
    head = idx[:idx.index('<style>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{title_de}</title>', head, count=1)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc_de}">', head, count=1)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title_de}">', head, count=1)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc_de}">', head, count=1)
    head = head.replace('href="https://latindanceawards.com/"', f'href="https://latindanceawards.com/{canonical}"')
    head = head.replace('href="https://latindanceawards.com/?lang=en"', f'href="https://latindanceawards.com/{canonical}?lang=en"')
    head = head.replace('content="https://latindanceawards.com/"', f'content="https://latindanceawards.com/{canonical}"')
    html = (head + '<style>' + HEAD_CSS + PAGE_CSS + '</style>\n</head>\n<body>\n\n' + HEADER + '\n\n<main id="top">\n' + main_html
            + '\n</main>\n\n' + FOOTER + '\n\n<script>\n(function(){\n  var EN=' + json.dumps(en, ensure_ascii=False) + ';\n'
            + '  var META={en:{title:' + json.dumps(title_en, ensure_ascii=False) + ',desc:' + json.dumps(desc_en, ensure_ascii=False) + '}};\n'
            + LANG_JS + page_js + '\n  if(start==="en") setLang("en");\n})();\n</script>\n</body>\n</html>\n')
    open(os.path.join(ROOT, fname), 'w', encoding='utf-8').write(html)
    print('wrote', fname, len(html))

class T:
    """Collects German markup + English translations."""
    def __init__(self, prefix): self.p = prefix; self.en = {}; self.n = 0
    def __call__(self, tag, de, en, attrs=''):
        self.n += 1; k = f'{self.p}{self.n}'; self.en[k] = en
        a = (' ' + attrs) if attrs else ''
        return f'<{tag}{a} data-i18n="{k}">{de}</{tag}>'

ICON = {
 'cal': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
 'free': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12v8H4v-8M2 7h20v5H2zM12 22V7M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7zM12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>',
 'clock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 'trophy': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 4h10v5a5 5 0 0 1-10 0zM7 6H4c0 3 1.5 4.5 3.5 4.5M17 6h3c0 3-1.5 4.5-3.5 4.5M12 14v3M8 21h8l-1-4H9z"/></svg>',
 'check': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M8 12.5l2.7 2.7L16 9.8"/></svg>',
 'lock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>',
}

# ======================================================================
# APPLICATION PAGE
# ======================================================================
t = T('a')
steps = [
 ('Jetzt bis 30. November', 'Now until November 30', 'Bewerben', 'Apply', 'Fülle das Formular aus. Es dauert etwa fünf Minuten.', 'Fill in the form. It takes about five minutes.'),
 ('Nach 3 Tagen', 'After 3 days', 'Bestätigung', 'Confirmation', 'Du bekommst eine E-Mail: Deine Bewerbung ist angenommen. Wir bitten nur noch um ein paar Nachweise.', "You'll get an email: your application is accepted. We just ask for a few proofs."),
 ('Innerhalb von 10 Tagen', 'Within 10 days', 'Nachweise senden', 'Send proofs', 'Einfach Links schicken, zum Beispiel zum Festival-Lineup oder zu eurem Kursplan. Kein Papierkram.', 'Just send links, for example to a festival lineup or your class schedule. No paperwork.'),
 ('20. Dezember 2026', 'December 20, 2026', 'Ergebnisse', 'Results', 'Alle Rankings werden veröffentlicht. Gewinner erhalten ihr offizielles Award-Siegel.', 'All rankings are published. Winners receive their official award seal.'),
]
steps_html = '\n'.join(
    f'      <li class="step"><span class="num">{i+1}</span>{t("span", w_de, w_en, "class=\"when\"")}{t("h3", h_de, h_en)}{t("p", p_de, p_en)}</li>'
    for i, (w_de, w_en, h_de, h_en, p_de, p_en) in enumerate(steps))

need = [
 ('Name und Stadt der Schule', 'School name and city', 'Berlin, München, Hamburg, Köln, Frankfurt oder Düsseldorf', 'Berlin, Munich, Hamburg, Cologne, Frankfurt or Düsseldorf', False),
 ('Website, Instagram und TikTok', 'Website, Instagram and TikTok', 'Einfach die Links', 'Just the links', False),
 ('Link zu eurem Google-Maps-Eintrag', 'Link to your Google Maps listing', 'Für Bewertungen und Anzahl der Bewertungen', 'For your rating and number of reviews', False),
 ('Gründungsjahr', 'Year founded', 'Seit wann unterrichtet ihr Bachata?', 'Since when have you taught Bachata?', False),
 ('Kursplan und Levels', 'Class schedule and levels', 'Inklusive Probestunde und Starttermine für Anfänger', 'Including trial class and start dates for beginners', False),
 ('Eure Lehrer und ihre Festivals', 'Your teachers and their festivals', 'Festivals und Kongresse 2025–2026, auf denen sie unterrichtet haben', 'Festivals and congresses in 2025–2026 where they taught', False),
 ('Events und Gastlehrer', 'Events and guest teachers', 'Socials, Workshops und internationale Gäste der letzten 12 Monate', 'Socials, workshops and international guests from the last 12 months', False),
 ('Wettbewerbsergebnisse', 'Competition results', 'Turnier, Jahr und Platzierung', 'Competition, year and placement', True),
]
need_html = '\n'.join(
    f'      <li>{ICON["check"]}<div>{t("span", d, e)}{" " + t("em", "optional", "optional") if opt else ""}{t("small", sd, se)}</div></li>'
    for d, e, sd, se, opt in need)

faq = [
 ('Kostet die Teilnahme etwas?', 'Does it cost anything to take part?',
  'Nein. Bewerbung, Bewertung und Award-Siegel sind komplett kostenlos.', 'No. Applying, being scored and the award seal are completely free.'),
 ('Garantiert eine Bewerbung einen Preis?', 'Does applying guarantee an award?',
  'Nein. Jede Schule wird nach denselben neun Kriterien bewertet. Die Bewerbung hilft uns nur, eure Daten vollständig und korrekt zu erfassen. <a href="index.html#method">So bewerten wir</a>.',
  'No. Every school is scored on the same nine factors. Applying only helps us capture your data completely and correctly. <a href="index.html#method">How we score</a>.'),
 ('Erscheinen wir auch ohne Bewerbung im Ranking?', 'Can we appear in the ranking without applying?',
  'Ja, wir recherchieren alle Schulen selbst. Mit Bewerbung können wir aber mehr Angaben bestätigen, was meist zu einer genaueren Punktzahl führt.',
  'Yes, we research every school ourselves. But when you apply, we can confirm more of your information, which usually leads to a more accurate score.'),
 ('Wer darf sich bewerben?', 'Who can apply?',
  'Inhaber, Lehrer oder Mitarbeiter einer Bachata-Schule in Berlin, München, Hamburg, Köln, Frankfurt oder Düsseldorf. Eure Schule ist in einer anderen Stadt? Bewerbt euch trotzdem, wir nehmen euch für kommende Ausgaben auf.',
  "Owners, teachers or staff of a Bachata school in Berlin, Munich, Hamburg, Cologne, Frankfurt or Düsseldorf. Your school is in another city? Apply anyway and we'll include you in future editions."),
 ('Wie weisen wir unsere Angaben nach?', 'How do we prove our information?',
  'Mit Links, die es meistens schon gibt: ein Festival-Lineup, euer Kursplan, Posts zu euren Events. Damit wir wissen, dass die Bewerbung wirklich von euch kommt, schickt ihr uns außerdem eine kurze Nachricht von eurem offiziellen Instagram-Account.',
  "With links that usually already exist: a festival lineup, your class schedule, posts about your events. To confirm the application really comes from you, you'll also send us a short message from your official Instagram account."),
 ('Was passiert mit unseren Daten?', 'What happens to our data?',
  'Wir nutzen eure Angaben nur für die Awards. Öffentlich gezeigt werden nur Schulname, Stadt, Punktzahl, die Punkteaufschlüsselung und eure öffentlichen Links. Kontaktdaten bleiben privat.',
  'We only use your information for the awards. We only publish the school name, city, score, score breakdown and your public links. Contact details stay private.'),
]
faq_html = '\n'.join(f'      <details>{t("summary", q_de, q_en)}{t("p", a_de, a_en)}</details>' for q_de, q_en, a_de, a_en in faq)

app_main = f'''
<section class="page-hero" aria-labelledby="app-title">
  <div class="wrap">
    <div>
      <span class="edition rise d1"><i></i>{t("span", "Bewerbung · Awards 2026", "Application · Awards 2026")}</span>
      <h1 id="app-title" class="rise d2">{t("span", "Bewirb deine Schule für die <em class=\"foil\">Bachata Awards 2026</em>", "Enter your school for the <em class=\"foil\">Bachata Awards 2026</em>")}</h1>
      <p class="lede rise d3">{t("span", "Kostenlos, in fünf Minuten erledigt und offen für jede Bachata-Schule in Deutschlands sechs größten Bachata-Städten.", "Free, done in five minutes, and open to every Bachata school in Germany's six biggest Bachata cities.")}</p>
      <div class="facts rise d4">
        <span>{ICON["free"]}{t("b", "Kostenlos", "Free")}</span>
        <span>{ICON["clock"]}{t("b", "5 Minuten", "5 minutes")}</span>
        <span>{ICON["cal"]}{t("span", "Bewerbungsschluss <b>30. November</b>", "Deadline <b>November 30</b>")}</span>
        <span>{ICON["trophy"]}{t("span", "Ergebnisse <b>20. Dezember</b>", "Results <b>December 20</b>")}</span>
      </div>
      <div class="ctas rise d5">
        <a class="btn btn-gold" href="#formular">{t("span", "Zum Formular", "Go to the form")}</a>
        <a class="btn btn-ghost" href="index.html#method">{t("span", "So bewerten wir", "How we score")}</a>
      </div>
    </div>
    <div class="seal-box rise d3">
      <img class="seal" src="badge-winner-template.svg" alt="" width="360" height="360">
      {t("p", "Dein Siegel, wenn deine Schule gewinnt", "Your seal, if your school wins", 'class="seal-cap"')}
    </div>
  </div>
</section>

<section class="block alt" aria-labelledby="steps-title">
  <div class="wrap">
    <div class="sec-head">
      {t("h2", "So läuft es ab", "How it works", 'id="steps-title"')}
      {t("p", "Vier einfache Schritte, ohne Papierkram.", "Four simple steps, no paperwork.")}
    </div>
    <ol class="steps">
{steps_html}
    </ol>
  </div>
</section>

<section class="block" aria-labelledby="need-title">
  <div class="wrap">
    <div class="sec-head">
      {t("h2", "Was du brauchst", "What you'll need", 'id="need-title"')}
      {t("p", "Halte diese Angaben bereit. Das meiste findest du auf eurer Website oder eurem Instagram.", "Have this information ready. You'll find most of it on your website or Instagram.")}
    </div>
    <ul class="need">
{need_html}
    </ul>
  </div>
</section>

<section class="block alt" id="formular" aria-labelledby="form-title">
  <div class="wrap">
    <div class="form-card">
      {t("h2", "Bewerbungsformular", "Application form", 'id="form-title"')}
      {t("p", "Alle Felder mit * sind Pflichtfelder. Nach dem Absenden bekommst du sofort eine Bestätigung per E-Mail.", "Fields marked * are required. You'll get a confirmation email right after you submit.")}
      <div id="form-slot"></div>
      <div class="form-fallback" id="form-fallback" hidden>
        {t("p", "Das Formular wird gerade eingerichtet. Schreib uns in der Zwischenzeit eine E-Mail, und wir nehmen deine Schule auf.", "The form is being set up. In the meantime, send us an email and we'll add your school.")}
        <a class="btn btn-gold" href="mailto:hello@latindanceawards.com?subject=Bewerbung%20Bachata%20Awards%202026">{t("span", "Per E-Mail bewerben", "Apply by email")}</a>
      </div>
    </div>
  </div>
</section>

<section class="block" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="sec-head">{t("h2", "Gut zu wissen", "Good to know", 'id="faq-title"')}</div>
    <div class="faq">
{faq_html}
    </div>
  </div>
</section>
'''

app_js = r'''
  /* ===== Paste your Tally form IDs here (the part after tally.so/r/) ===== */
  var TALLY_FORM_DE = "";   // e.g. "w2XyZ1"
  var TALLY_FORM_EN = "";   // optional English version; leave empty to always use the German form

  var slot=document.getElementById("form-slot"), fb=document.getElementById("form-fallback");
  function loadForm(l){
    var id = (l==="en" && TALLY_FORM_EN) ? TALLY_FORM_EN : TALLY_FORM_DE;
    if(!id){ slot.innerHTML=""; fb.hidden=false; return; }
    fb.hidden=true;
    slot.innerHTML='<iframe data-tally-src="https://tally.so/embed/'+id+'?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" title="Bewerbungsformular / Application form"></iframe>';
    if(window.Tally){ window.Tally.loadEmbeds(); }
    else if(!document.getElementById("tally-js")){
      var s=document.createElement("script"); s.id="tally-js"; s.src="https://tally.so/widgets/embed.js";
      s.onload=function(){ window.Tally && window.Tally.loadEmbeds(); }; document.body.appendChild(s);
    }
  }
  document.addEventListener("langchange",function(e){ loadForm(e.detail); });
  loadForm("de");
'''

page('bewerbung.html',
     'Bewerbung · Bachata Awards 2026 · Latin Dance Awards',
     'Bewirb deine Bachata-Schule kostenlos für die Latin Dance Awards 2026. Bewerbungsschluss 30. November, Ergebnisse am 20. Dezember.',
     'Apply · Bachata Awards 2026 · Latin Dance Awards',
     'Enter your Bachata school for the Latin Dance Awards 2026 for free. Deadline November 30, results on December 20.',
     'bewerbung.html', app_main, t.en, app_js)

# ======================================================================
# RANKINGS PAGE
# ======================================================================
r = T('r')
CITIES = [('deutschland', 'Deutschland', 'Germany'), ('berlin', 'Berlin', 'Berlin'), ('muenchen', 'München', 'Munich'),
          ('hamburg', 'Hamburg', 'Hamburg'), ('koeln', 'Köln', 'Cologne'), ('frankfurt', 'Frankfurt', 'Frankfurt'),
          ('duesseldorf', 'Düsseldorf', 'Düsseldorf')]
tabs_html = '\n'.join(
    f'      <button type="button" role="tab" id="tab-{slug}" aria-controls="panel" aria-selected="{"true" if i==0 else "false"}" data-city="{slug}">{r("span", de, en)}</button>'
    for i, (slug, de, en) in enumerate(CITIES))

rank_main = f'''
<section class="page-hero" aria-labelledby="rk-title">
  <div class="wrap">
    <div>
      <span class="edition rise d1"><i></i>{r("span", "Rankings 2026 · Deutschland", "Rankings 2026 · Germany")}</span>
      <h1 id="rk-title" class="rise d2">{r("span", "Die besten Bachata-Schulen <em class=\"foil\">Deutschlands 2026</em>", "The best Bachata schools <em class=\"foil\">in Germany 2026</em>")}</h1>
      <p class="lede rise d3">{r("span", "Sechs Städte, ein nationaler Sieger. Die Ergebnisse werden am 20. Dezember 2026 um 19 Uhr veröffentlicht.", "Six cities, one national winner. Results will be published on December 20, 2026 at 7 pm (CET).")}</p>
      <div class="countdown rise d4" id="countdown" aria-live="off">
        <div><b data-u="d">00</b>{r("small", "Tage", "days")}</div>
        <div><b data-u="h">00</b>{r("small", "Stunden", "hours")}</div>
        <div><b data-u="m">00</b>{r("small", "Minuten", "minutes")}</div>
        <div><b data-u="s">00</b>{r("small", "Sekunden", "seconds")}</div>
      </div>
      <div class="ctas rise d5">
        <a class="btn btn-gold" href="https://instagram.com/" rel="noopener">{r("span", "Auf Instagram erinnern lassen", "Get notified on Instagram")}</a>
        <a class="btn btn-ghost" href="bewerbung.html">{r("span", "Schule kostenlos bewerben", "Enter a school for free")}</a>
      </div>
    </div>
    <div class="seal-box rise d3"><img class="seal" src="badge-bachata-2026.svg" alt="" width="360" height="360"></div>
  </div>
</section>

<section class="block alt" aria-label="Rankings">
  <div class="wrap">
    <div class="tabs" role="tablist" aria-label="Städte / Cities">
{tabs_html}
    </div>
    <div id="panel" role="tabpanel"></div>
  </div>
</section>
'''

R_TEXT = {
 'title_city': ['Beste Bachata-Schulen in {c}', 'Best Bachata schools in {c}'],
 'title_de': ['Beste Bachata-Schulen Deutschlands', 'Best Bachata schools in Germany'],
 'sub_locked': ['Die Top 10 werden am 20. Dezember 2026 enthüllt.', 'The top 10 will be revealed on December 20, 2026.'],
 'sub_open': ['Endergebnis der Bachata Awards 2026. Tippe auf eine Schule, um ihre Punkteaufschlüsselung zu sehen.', 'Final results of the Bachata Awards 2026. Tap a school to see its score breakdown.'],
 'locked': ['Wird am 20. Dezember enthüllt', 'Revealed on December 20'],
 'pts': ['Punkte', 'points'],
 'site': ['Website', 'Website'],
 'insta': ['Instagram', 'Instagram'],
 'note_h': ['Deine Schule fehlt noch?', 'Is your school missing?'],
 'note_p': ['Bewirb dich bis zum 30. November kostenlos für die Awards 2026.', 'Enter for the 2026 awards for free by November 30.'],
 'note_btn': ['Kostenlos bewerben', 'Apply for free'],
 'preview': ['Vorschau mit Beispieldaten', 'Preview with sample data'],
 'empty': ['Für diese Stadt gibt es noch keine Ergebnisse.', 'There are no results for this city yet.'],
 'cities': {slug: [de, en] for slug, de, en in CITIES},
 'factors': {
   'google': [25, 'Google-Bewertung', 'Google rating'], 'fest': [15, 'Festivals & Kongresse', 'Festivals & congresses'],
   'revs': [10, 'Anzahl der Bewertungen', 'Review volume'], 'years': [10, 'Jahre aktiv', 'Years active'],
   'class': [10, 'Kurse & Einsteiger', 'Classes & beginners'], 'events': [10, 'Events & Gastlehrer', 'Events & guest teachers'],
   'social': [10, 'Social Media', 'Social media'], 'recent': [5, 'Aktuelle Bewertungen', 'Recent reviews'], 'comp': [5, 'Wettbewerbe', 'Competitions']},
}

rank_js = r'''
  /* =====================================================================
     RESULTS: fill this in ON DECEMBER 20 (not before: anything in this file is public).
     One list per city, any order. The page sorts by score and builds the national top 10 itself.
     Example entry:
       { name:"Schule A", score:84.2, url:"https://...", instagram:"https://instagram.com/...",
         scores:{google:23.4, fest:12.6, revs:8.1, years:9, class:8.5, events:8, social:7.2, recent:4.4, comp:3} }
     ===================================================================== */
  var RESULTS = {
    berlin: [],
    muenchen: [],
    hamburg: [],
    koeln: [],
    frankfurt: [],
    duesseldorf: []
  };
  var PUBLISH_DATE = new Date("2026-12-20T19:00:00+01:00");

  var TX = ''' + json.dumps(R_TEXT, ensure_ascii=False) + r''';
  function L(k){ return TX[k][window.LANG==="en"?1:0]; }
  function esc(s){ return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];}); }
  function safeUrl(u){ return /^https?:\/\//i.test(u||"") ? esc(u) : ""; }
  function num(n){ var s=(Math.round(n*10)/10).toFixed(1); return window.LANG==="en"?s:s.replace(".",","); }

  // Preview mode (?preview=1) shows sample data so you can see the finished layout
  var preview=false;
  try{ preview = new URLSearchParams(location.search).get("preview")==="1"; }catch(e){}
  if(preview){
    var demo=["Schule A","Schule B","Schule C","Schule D","Schule E","Schule F","Schule G","Schule H"];
    Object.keys(RESULTS).forEach(function(c,ci){
      RESULTS[c]=demo.map(function(n,i){
        var f=1-(i*0.07)-(ci*0.01);
        return {name:n+" ("+TX.cities[c][0]+")", url:"https://example.com", instagram:"https://instagram.com/",
          scores:{google:23*f,fest:13*f,revs:8.5*f,years:9*f,class:8.6*f,events:8.2*f,social:7.4*f,recent:4.4*f,comp:3*f}};
      });
    });
  }
  function total(e){ if(typeof e.score==="number") return e.score; var t=0,s=e.scores||{}; for(var k in s) t+=s[k]; return t; }
  function listFor(city){
    var out=[];
    if(city==="deutschland"){
      Object.keys(RESULTS).forEach(function(c){ (RESULTS[c]||[]).forEach(function(e){ out.push(Object.assign({city:c},e)); }); });
    } else { (RESULTS[city]||[]).forEach(function(e){ out.push(Object.assign({city:city},e)); }); }
    out.sort(function(a,b){ return total(b)-total(a); });
    return out.slice(0,10);
  }
  function isOpen(){ return preview || new Date()>=PUBLISH_DATE; }

  var panel=document.getElementById("panel"), current="deutschland";
  var LOCK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>';

  function podCard(pos, e){
    if(!e){
      return '<div class="pod p'+pos+'"><div class="medal-n">'+pos+'</div><span class="blur" style="width:70%"></span><span class="blur" style="width:40%"></span><span class="lock">'+LOCK+esc(L("locked"))+'</span></div>';
    }
    var name=esc(e.name), u=safeUrl(e.url);
    return '<div class="pod p'+pos+'"><div class="medal-n">'+pos+'</div><h3>'+(u?'<a href="'+u+'" rel="noopener">'+name+'</a>':name)+'</h3>'
      +(current==="deutschland"?'<div class="sc">'+esc(TX.cities[e.city][window.LANG==="en"?1:0])+'</div>':'')
      +'<div class="sc"><b>'+num(total(e))+'</b> '+esc(L("pts"))+'</div></div>';
  }
  function render(){
    var c=current, cityName=TX.cities[c][window.LANG==="en"?1:0];
    var title = c==="deutschland" ? L("title_de") : L("title_city").replace("{c}",cityName);
    var list=listFor(c), open=isOpen()&&list.length>0;
    var h=(preview?'<span class="preview-note">'+esc(L("preview"))+'</span>':'')
      +'<h2 class="panel-title">'+esc(title)+'</h2><p class="panel-sub">'+esc(open?L("sub_open"):L("sub_locked"))+'</p>';
    h+='<div class="podium3">'+podCard(2,open?list[1]:null)+podCard(1,open?list[0]:null)+podCard(3,open?list[2]:null)+'</div>';
    h+='<ol class="rlist">';
    for(var i=3;i<10;i++){
      var e=open?list[i]:null;
      if(open&&!e) break;
      if(!e){
        h+='<li class="rrow"><div class="rr"><span class="pos">'+(i+1)+'</span><span class="blur" style="width:'+(60-i*3)+'%;margin:0"></span></div></li>';
      } else {
        var bd='', s=e.scores||{};
        Object.keys(TX.factors).forEach(function(k){
          if(s[k]==null) return; var f=TX.factors[k];
          bd+='<div><b>'+esc(f[window.LANG==="en"?2:1])+'</b> · '+num(s[k])+' / '+f[0]+'<div class="bar"><i style="width:'+Math.min(100,s[k]/f[0]*100)+'%"></i></div></div>';
        });
        var links='';
        if(safeUrl(e.url)) links+='<a href="'+safeUrl(e.url)+'" rel="noopener">'+esc(L("site"))+'</a>';
        if(safeUrl(e.instagram)) links+='<a href="'+safeUrl(e.instagram)+'" rel="noopener">'+esc(L("insta"))+'</a>';
        h+='<li><details class="rrow"><summary><span class="pos">'+(i+1)+'</span><span class="nm">'+esc(e.name)
          +(c==="deutschland"?'<small>'+esc(TX.cities[e.city][window.LANG==="en"?1:0])+'</small>':'')+'</span><span class="pts">'+num(total(e))+'</span></summary>'
          +'<div class="breakdown">'+bd+(links?'<div class="links">'+links+'</div>':'')+'</div></details></li>';
      }
    }
    h+='</ol>';
    if(!open){
      h+='<div class="note-card"><div><h3>'+esc(L("note_h"))+'</h3><p>'+esc(L("note_p"))+'</p></div><a class="btn btn-gold" href="bewerbung.html">'+esc(L("note_btn"))+'</a></div>';
    }
    panel.innerHTML=h;
    panel.setAttribute("aria-labelledby","tab-"+c);
  }
  function select(c, push){
    if(!TX.cities[c]) c="deutschland";
    current=c;
    document.querySelectorAll(".tabs button").forEach(function(b){ b.setAttribute("aria-selected", b.dataset.city===c?"true":"false"); });
    if(push){ try{ history.replaceState(null,"","#"+c); }catch(e){} }
    render();
  }
  document.querySelectorAll(".tabs button").forEach(function(b){ b.addEventListener("click",function(){ select(b.dataset.city,true); }); });
  window.addEventListener("hashchange",function(){ select(location.hash.slice(1),false); });
  document.addEventListener("langchange",render);
  select((location.hash||"").slice(1)||"deutschland",false);

  // Countdown
  var cells={}; document.querySelectorAll("#countdown b").forEach(function(b){ cells[b.dataset.u]=b; });
  function pad(n){ return (n<10?"0":"")+n; }
  function tick(){
    var ms=Math.max(0,PUBLISH_DATE-new Date()), s=Math.floor(ms/1000);
    cells.d.textContent=pad(Math.floor(s/86400)); cells.h.textContent=pad(Math.floor(s%86400/3600));
    cells.m.textContent=pad(Math.floor(s%3600/60)); cells.s.textContent=pad(s%60);
    if(ms===0 && !tick.done){ tick.done=true; render(); }
  }
  tick(); setInterval(tick,1000);
'''

page('rankings.html',
     'Rankings 2026 · Die besten Bachata-Schulen Deutschlands · Latin Dance Awards',
     'Die besten Bachata-Schulen in Berlin, München, Hamburg, Köln, Frankfurt und Düsseldorf. Ergebnisse der Latin Dance Awards am 20. Dezember 2026.',
     'Rankings 2026 · The best Bachata schools in Germany · Latin Dance Awards',
     'The best Bachata schools in Berlin, Munich, Hamburg, Cologne, Frankfurt and Düsseldorf. Latin Dance Awards results on December 20, 2026.',
     'rankings.html', rank_main, r.en, rank_js)
