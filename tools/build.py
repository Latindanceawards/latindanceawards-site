# Builds bewerbung.html and rankings.html, reusing the homepage's styles, header and footer.
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
idx = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
NAV_JS = re.search(r'<script>\n\(function\(\)\{var n=document\.querySelector\("\.nav"\).*?</script>\n', idx, re.S).group(0)

HEAD_CSS = idx[idx.index('<style>') + 7: idx.index('</style>')]
HEADER = idx[idx.index('<header class="nav">'): idx.index('</header>') + 9]
FOOTER = idx[idx.index('<footer>'): idx.index('</footer>') + 9]
EN_INDEX = json.loads(re.search(r'var EN=(\{.*?\});\n', idx, re.S).group(1))

def fix_links(h):
    for a in ['#why', '#method', '#categories', '#faq']:
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


/* application wizard */
.wiz{max-width:760px}
#lda-form,#form-ok{scroll-margin-top:110px}
.fld{scroll-margin-top:130px}
.wiz-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px;font-size:14px;color:var(--muted);margin-bottom:10px}
.wiz-top b{color:var(--gold-light);font-weight:700}
.wiz-bar{height:8px;border-radius:8px;background:rgba(246,231,211,.12);overflow:hidden;margin-bottom:8px}
.wiz-bar i{display:block;height:100%;width:12%;border-radius:8px;background:var(--foil,var(--gold));transition:width .5s cubic-bezier(.2,.8,.2,1)}
.wiz-dots{display:flex;gap:8px;margin-bottom:26px}
.wiz-dots > span{flex:1;font-size:12.5px;font-weight:600;color:var(--muted);padding-top:6px;border-top:2px solid rgba(246,231,211,.14);transition:all .3s}
.wiz-dots > span.on{color:var(--gold-light);border-color:var(--gold)}
.wiz-dots > span.done{color:var(--cream);border-color:var(--gold)}
.step-pane{padding:0;display:none;animation:stepin .45s cubic-bezier(.2,.8,.2,1)}
.step-pane.on{display:block}
@keyframes stepin{from{opacity:0;transform:translateX(18px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.step-pane{animation:none}.wiz-bar i{transition:none}}
.step-pane h3{font-family:var(--serif);font-weight:500;font-size:clamp(26px,3.4vw,34px);line-height:1.15;margin-bottom:6px}
.step-pane .sub{color:var(--muted);margin-bottom:24px}
.fld{margin-bottom:18px}
.fld label,.fld .lab{display:block;font-weight:600;font-size:15px;margin-bottom:7px}
.fld .opt{font-weight:400;color:var(--muted);font-size:13px;margin-left:6px}
.fld input[type=text],.fld input[type=email],.fld input[type=url],.fld input[type=number],.fld textarea{width:100%;font:inherit;font-size:17px;color:var(--cream);
  background:rgba(255,255,255,.05);border:1.5px solid var(--line);border-radius:16px;padding:15px 18px;min-height:52px;transition:border-color .2s,background .2s,box-shadow .2s}
.fld textarea{min-height:96px;resize:vertical}
.fld input:focus,.fld textarea:focus{outline:none;border-color:var(--gold);background:rgba(255,255,255,.08);box-shadow:0 0 0 4px rgba(228,185,91,.14)}
.fld.bad input,.fld.bad textarea{border-color:#e0685c}
.fld .help{font-size:13px;color:var(--muted);margin-top:6px}
.fld .errtxt{font-size:13.5px;color:#f2a299;margin-top:4px;height:20px;line-height:20px;visibility:hidden}
.fld.bad .errtxt{visibility:visible}
.chips,.cards2{display:flex;flex-wrap:wrap;gap:10px}
.chips label,.cards2 label{position:relative;margin:0;cursor:pointer}
.chips input,.cards2 input{position:absolute;opacity:0;inset:0;width:100%;height:100%;cursor:pointer}
.chips label > span{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;border-radius:999px;border:1.5px solid var(--line);background:rgba(255,255,255,.04);font-weight:600;font-size:15.5px;transition:all .2s}
.chips input:checked + span{background:var(--gold);color:#131011;border-color:var(--gold)}
.chips input:focus-visible + span,.cards2 input:focus-visible + span{outline:3px solid var(--gold-light);outline-offset:2px}
.cards2 label > span{display:block;min-width:160px;padding:16px 22px;border-radius:18px;border:1.5px solid var(--line);background:rgba(255,255,255,.04);font-weight:600;transition:all .2s}
.cards2 label > span small{display:block;font-weight:400;color:var(--muted);font-size:13px;margin-top:2px}
.cards2 input:checked + span{border-color:var(--gold);background:var(--gold-soft)}
.bonus{display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border-radius:999px;background:var(--gold-soft);color:var(--gold-light);font-size:13px;font-weight:700;margin-bottom:14px}
.wiz-nav{display:flex;gap:12px;align-items:center;margin-top:26px}
.wiz-nav .btn{min-height:52px}
.wiz-nav .back{background:none;border:0;color:var(--muted);font:inherit;font-weight:600;cursor:pointer;padding:12px 6px}
.wiz-nav .back:hover{color:var(--cream)}
.wiz-nav .btn-gold{flex:1;justify-content:center}
.consent{display:grid;grid-template-columns:24px 1fr;gap:12px;align-items:start;font-size:14.5px;color:var(--muted);margin-top:8px}
.consent input{width:22px;height:22px;accent-color:var(--gold);margin-top:2px}
.wiz .hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.wiz .msg{padding:14px 18px;border-radius:14px;font-size:15px;margin-top:16px;background:rgba(220,80,70,.14);border:1px solid rgba(220,80,70,.5)}
.trust{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:22px;font-size:13px;color:var(--muted)}
.trust > span::before{content:"✓";color:var(--gold);margin-right:6px;font-weight:700}
.form-ok{padding:40px 30px;border-radius:24px;border:1px solid rgba(228,185,91,.5);background:linear-gradient(170deg,var(--gold-soft),var(--card) 70%);text-align:center}
.form-ok h3{font-family:var(--serif);font-weight:500;font-size:clamp(28px,4vw,38px);margin-bottom:8px}
.form-ok p{color:var(--muted);max-width:34em;margin:0 auto 18px}
.form-ok ol{list-style:none;text-align:left;max-width:30em;margin:22px auto 0;display:grid;gap:10px}
.form-ok li{padding:12px 16px;border-radius:14px;background:var(--card);border:1px solid var(--line);font-size:15px}
.form-ok li b{color:var(--gold-light)}
@media (max-width:620px){.wiz-dots > span{font-size:11px}.cards2 label > span{min-width:0}.cards2 label{flex:1 1 140px}}

.wiz-nav .skip{background:none;border:0;color:var(--gold-light);font:inherit;font-weight:600;cursor:pointer;padding:12px 8px}
.chips label,.cards2 label{margin:0}
.chips span span,.cards2 span span{display:inline}
.fld.reveal{margin-top:-6px}
.fld[hidden]{display:none}
.fld .chips{margin-bottom:2px}
.step-pane .fld + .fld{margin-top:26px}
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
.citypick{position:relative;flex:1 1 230px;max-width:330px}
.citypick input{width:100%;font:inherit;font-size:15px;font-weight:600;color:var(--cream);background:var(--card) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23b9ad98' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E") no-repeat right 16px center;border:1px solid var(--line);padding:11px 38px 11px 20px;border-radius:999px;outline:none;transition:all .25s}
.citypick input::placeholder{color:var(--muted);opacity:1}
.citypick input:hover,.citypick input:focus{border-color:rgba(228,185,91,.55)}
.citypick.sel input{background-color:var(--gold);color:var(--velvet-deep);border-color:var(--gold)}
#citylist{position:absolute;z-index:30;left:0;right:0;top:calc(100% + 8px);max-height:340px;overflow:auto;margin:0;padding:6px;list-style:none;background:#1a1612;border:1px solid rgba(228,185,91,.4);border-radius:16px;box-shadow:0 18px 40px rgba(0,0,0,.55)}
#citylist[hidden]{display:none}
#citylist li{display:flex;justify-content:space-between;gap:12px;padding:10px 14px;border-radius:10px;cursor:pointer;color:var(--cream);font-size:15px}
#citylist li small{color:var(--muted);font-size:13px}
#citylist li.act,#citylist li:hover{background:rgba(228,185,91,.16)}
#citylist li.none{cursor:default;color:var(--muted)}
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
.prelim{margin-top:40px}
.prelim .prelim-badge{display:inline-flex;margin-bottom:14px;padding:7px 14px;border-radius:999px;border:1px solid rgba(228,185,91,.6);color:var(--gold-light);font-size:13px;font-weight:700}
.prelim h3{font-family:var(--serif);font-weight:500;font-size:26px;margin-bottom:8px}
.prelim>p{color:var(--muted);max-width:760px;margin-bottom:18px}
.plist{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.plist li{padding:14px 18px;border-radius:16px;background:var(--card);border:1px solid var(--line);display:flex;flex-direction:column;gap:2px}
.plist li a,.plist li span.n{font-weight:600;color:var(--cream);text-decoration:none}
.plist li a:hover{color:var(--gold-light)}
.plist li small{color:var(--muted);font-size:13px}
.ilist{list-style:none;display:grid;gap:12px;margin:0;padding:0}
.irk{border-radius:20px;background:var(--card);border:1px solid var(--line);transition:border-color .25s,transform .25s}
.irk:hover{border:1px solid rgba(228,185,91,.5)}
.irk[open]{border-color:rgba(228,185,91,.6)}
.irk.g1{background:linear-gradient(170deg,var(--gold-soft),var(--card) 65%);border-color:rgba(228,185,91,.55)}
.irk summary{display:grid;grid-template-columns:48px minmax(0,1fr) auto 22px;align-items:center;gap:16px;padding:18px 22px 18px;cursor:pointer;list-style:none}
.irk summary::-webkit-details-marker{display:none}
.irk summary::after{content:"";grid-column:4;grid-row:1;justify-self:center;width:9px;height:9px;border-right:2px solid var(--gold);border-bottom:2px solid var(--gold);transform:rotate(45deg);margin-top:-5px;transition:transform .3s,margin .3s}
.irk[open] summary::after{transform:rotate(-135deg);margin-top:5px}
.irk .who b a{color:inherit;text-decoration:none;border-bottom:1px solid transparent;transition:color .2s,border-color .2s}
.irk .who b a:hover,.irk .who b a:focus-visible{color:var(--gold-light);border-bottom-color:var(--gold)}
.irk summary:hover::after{border-color:var(--gold-light)}
.irk .rk{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-family:var(--serif);font-weight:600;font-size:20px;color:var(--gold);border:1px solid var(--line)}
.irk.g1 .rk{background:var(--foil);color:#131011;border:0}
.irk.g2 .rk{background:linear-gradient(135deg,#F2F2F2,#A9ADB4);color:#131011;border:0}
.irk.g3 .rk{background:linear-gradient(135deg,#E8B58A,#9C5F34);color:#131011;border:0}
.irk .who{min-width:0}
.irk .who b{display:block;font-family:var(--serif);font-weight:500;font-size:21px;line-height:1.2;overflow-wrap:anywhere}
.irk .who small{display:block;color:var(--muted);font-size:13.5px;margin-top:2px}
.irk .score{text-align:right;font-family:var(--serif);font-size:30px;line-height:1;color:var(--gold-light);white-space:nowrap}
.irk .score small{font-family:var(--sans);font-size:13px;color:var(--muted)}
.irk .meter{grid-column:1/-1;grid-row:2;display:block;height:5px;margin:0;border-radius:5px;background:rgba(255,255,255,.07);overflow:hidden}
.irk .meter i{display:block;height:100%;background:var(--foil);border-radius:5px}
.irk .iwhy{padding:2px 22px 20px 86px;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px 28px;font-size:14px;color:var(--muted)}
.irk .iwhy b{color:var(--cream);font-weight:600}
.irk .iwhy .bar{height:4px;margin-top:6px;border-radius:4px;background:rgba(255,255,255,.07);overflow:hidden}
.irk .iwhy .bar i{display:block;height:100%;background:var(--gold)}
.vote [hidden],.vote[hidden]{display:none!important}
.votebanner{margin:0 0 16px;padding:12px 16px;border-radius:14px;border:1px solid rgba(228,185,91,.35);background:rgba(228,185,91,.07);color:var(--cream);font-size:14px;line-height:1.5}
.votebanner b{color:var(--gold-light)}
.irk .iwhy .vote{grid-column:1/-1;margin-top:6px;padding-top:16px;border-top:1px solid rgba(255,255,255,.08)}
.vote .vform{display:grid;gap:10px;max-width:420px}
.vote .vform label{display:grid;gap:6px;color:var(--cream);font-size:14px}
.vote .vform input[type=email]{width:100%;padding:12px 14px;border-radius:12px;border:1px solid rgba(246,231,211,.35);background:rgba(255,255,255,.06);color:var(--cream);font:inherit;font-size:16px}
.vote .vform .newsopt,.sp-form .newsopt{display:flex!important;grid-template-columns:none;gap:10px;align-items:flex-start;font-size:13px;line-height:1.45;color:var(--muted)}.newsopt input{margin-top:3px;flex:none;width:18px;height:18px;accent-color:#e4b95b}
.vote .vform small,.vote .vmsg{color:var(--muted);font-size:13px;line-height:1.5}
.vote .vmsg{margin:10px 0 0;color:var(--gold-light)}
.vote .vform button[type=submit]{justify-content:center}
.vote button.btn{font:inherit;font-weight:600;cursor:pointer;-webkit-appearance:none;appearance:none}
button.btn.showall{background:transparent;-webkit-appearance:none;appearance:none;font:inherit;font-weight:600;color:var(--cream);border:1px solid rgba(246,231,211,.35);cursor:pointer}
.showall:hover{border-color:var(--gold);color:var(--gold-light)}
.irk .iwhy .tbc .chip.st{background:rgba(228,185,91,.16);color:#E4B95B;border:1px solid rgba(228,185,91,.5)}
  .tbc .chip{display:inline-block;padding:2px 10px;border-radius:999px;border:1px dashed rgba(228,185,91,.55);color:var(--gold-light);font-size:12px;font-weight:600}
.irk .iwhy .bar.dash{background:none;border-top:2px dashed rgba(255,255,255,.14);height:0;margin-top:9px}
.irk .iwhy .lk{grid-column:1/-1}
.irk .iwhy .lk a{color:var(--gold-light);font-weight:600;text-decoration:none}
@media(max-width:560px){.irk summary{grid-template-columns:40px minmax(0,1fr) auto 14px;gap:10px;padding:16px}
.irk .rk{width:38px;height:38px;font-size:17px}.irk .who b{font-size:18px}.irk .score{font-size:26px}.irk .meter{margin:0}.irk .iwhy{padding:0 16px 18px}}

/* podium motion */
@property --ang{syntax:"<angle>";initial-value:0deg;inherits:false}
@keyframes irkIn{from{opacity:0;transform:translateY(16px) scale(.985)}to{opacity:1;transform:none}}
@keyframes irkFill{from{width:0}}
@keyframes irkSpin{to{--ang:360deg}}
@keyframes irkGlow{0%,100%{box-shadow:0 0 0 0 rgba(228,185,91,0),0 12px 44px -20px rgba(228,185,91,.4)}50%{box-shadow:0 0 38px 0 rgba(228,185,91,.3),0 16px 54px -16px rgba(228,185,91,.6)}}
@keyframes irkGlowS{0%,100%{box-shadow:0 0 0 0 rgba(200,208,222,0)}50%{box-shadow:0 0 26px -2px rgba(200,208,222,.22)}}
@keyframes irkGlowB{0%,100%{box-shadow:0 0 0 0 rgba(214,148,96,0)}50%{box-shadow:0 0 26px -2px rgba(214,148,96,.26)}}
@keyframes irkSheen{0%{transform:translateX(-130%) skewX(-18deg)}50%,100%{transform:translateX(330%) skewX(-18deg)}}
@keyframes irkFloat{0%,100%{transform:translateY(0) rotate(-5deg)}50%{transform:translateY(-5px) rotate(5deg)}}
@keyframes irkRing{0%{transform:scale(.92);opacity:.9}100%{transform:scale(1.5);opacity:0}}
@keyframes irkTw{0%,100%{opacity:0;transform:scale(.2) rotate(0)}50%{opacity:1;transform:scale(1) rotate(45deg)}}
@keyframes irkMedal{from{background-position:0 0}to{background-position:-300% 0}}
@keyframes irkText{to{background-position:-200% center}}
.ilist>li{animation:irkIn .7s cubic-bezier(.2,.7,.2,1) both}
.ilist>li:nth-child(1){animation-delay:.35s}.ilist>li:nth-child(2){animation-delay:.1s}.ilist>li:nth-child(3){animation-delay:.2s}
.ilist>li:nth-child(n+4){animation-delay:.45s}
.irk{transition:border-color .25s,transform .25s}.irk:hover{transform:translateY(-2px)}
.irk .meter i{animation:irkFill 1.4s cubic-bezier(.2,.7,.2,1) .5s both}
/* 1st: rotating gold border, glow, sheen, crown, sparkles */
.irk.g1{position:relative;overflow:hidden;border:1.5px solid transparent;
 background:linear-gradient(170deg,rgba(228,185,91,.16),rgba(228,185,91,0) 65%) padding-box,linear-gradient(#1c1715,#1c1715) padding-box,conic-gradient(from var(--ang),#7a5a1c,#F6DFA2,#E4B95B,#7a5a1c,#E4B95B,#F6DFA2,#7a5a1c) border-box;
 animation:irkGlow 3.6s ease-in-out infinite,irkSpin 6s linear infinite,irkIn .7s cubic-bezier(.2,.7,.2,1) .35s both}
.irk.g1::before{content:"";position:absolute;top:0;bottom:0;left:0;width:28%;background:linear-gradient(100deg,transparent,rgba(255,236,170,.2),transparent);animation:irkSheen 5s ease-in-out 1.4s infinite;pointer-events:none}
.irk.g1 .rk{position:relative;overflow:visible;background:linear-gradient(115deg,#B8862B,#F6DFA2,#E4B95B,#B8862B);background-size:300% 100%;animation:irkMedal 4s linear infinite}
.irk.g1 .rk::after{content:"";position:absolute;inset:0;border-radius:50%;border:2px solid rgba(228,185,91,.7);animation:irkRing 2.4s ease-out infinite}
.irk.g1 .rk svg{position:absolute;left:50%;top:-19px;width:28px;height:21px;margin-left:-14px;animation:irkFloat 3.2s ease-in-out infinite;filter:drop-shadow(0 2px 6px rgba(228,185,91,.7))}
.irk .sp{position:absolute;width:9px;height:9px;pointer-events:none;background:#F6DFA2;clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%);animation:irkTw 2.4s ease-in-out infinite}
.irk .sp.a{left:-9px;top:-6px}.irk .sp.b{right:-10px;top:2px;width:7px;height:7px;animation-delay:.8s}.irk .sp.c{right:-3px;bottom:-9px;width:6px;height:6px;animation-delay:1.5s}.irk .sp.d{left:-12px;bottom:4px;width:6px;height:6px;animation-delay:2s}
.irk.g1 .score{text-shadow:0 0 20px rgba(228,185,91,.5)}
.irk.g1 .who b{background:linear-gradient(90deg,var(--cream) 0,var(--gold-light) 25%,var(--cream) 50%,var(--gold-light) 75%,var(--cream) 100%);background-size:200% auto;-webkit-background-clip:text;background-clip:text;color:transparent;animation:irkText 5s linear infinite}
.irk.g1 summary{padding-top:28px}
/* 2nd silver, 3rd bronze */
.irk.g2{border-color:rgba(200,208,222,.35);animation:irkGlowS 4s ease-in-out infinite,irkIn .7s cubic-bezier(.2,.7,.2,1) .1s both}
.irk.g3{border-color:rgba(214,148,96,.38);animation:irkGlowB 4s ease-in-out 1s infinite,irkIn .7s cubic-bezier(.2,.7,.2,1) .2s both}
.irk.g2 .rk{background:linear-gradient(115deg,#8E939C,#FFFFFF,#C4C8CF,#8E939C);background-size:300% 100%;animation:irkMedal 5s linear infinite}
.irk.g3 .rk{background:linear-gradient(115deg,#8A4E26,#F0BE92,#C07842,#8A4E26);background-size:300% 100%;animation:irkMedal 5.5s linear infinite}
.irk.g2::before,.irk.g3::before{content:"";position:absolute;top:0;bottom:0;left:0;width:22%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.07),transparent);animation:irkSheen 7s ease-in-out 2s infinite;pointer-events:none}
.irk.g2,.irk.g3{position:relative;overflow:hidden}
.irk.g2 .score{color:#E6E9EE}.irk.g3 .score{color:#F0C9A4}
@media(prefers-reduced-motion:reduce){.ilist>li,.irk,.irk .meter i,.irk::before,.irk .rk,.irk .rk svg,.irk .rk::after,.irk .sp,.irk .who b{animation:none!important}.irk.g1 .who b{color:var(--cream);background:none}.irk .sp{display:none}}
.helpbox{margin-top:36px;padding:26px 28px;border-radius:22px;background:var(--card);border:1px solid var(--line)}
.helpbox h3{font-family:var(--serif);font-weight:500;font-size:26px;margin-bottom:6px}
.helpbox>p{color:var(--muted);margin-bottom:18px;max-width:640px}
.helpbox .hb-btns{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px}
.helpbox details{border-top:1px solid var(--line);padding-top:14px}
.helpbox summary{cursor:pointer;color:var(--gold-light);font-weight:600}
.helpbox ul{margin:12px 0 0 18px;color:var(--muted);display:grid;gap:8px}
.howto{margin-top:22px;color:var(--muted);font-size:14.5px}.howto summary{cursor:pointer;color:var(--gold-light);font-weight:600}.howto p{margin-top:10px;max-width:760px}
.plist li{position:relative;padding-left:52px}
.plist .ipos{position:absolute;left:16px;top:12px;font-family:var(--serif);font-size:24px;color:var(--gold-light);line-height:1}
.plist .ipts{color:var(--gold-light);font-size:14px;font-weight:600;margin-top:2px}
.note-card{margin-top:36px;padding:30px 32px;border-radius:22px;background:var(--card);border:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap}
.note-card h3{font-family:var(--serif);font-weight:500;font-size:26px;margin-bottom:4px}
.note-card p{color:var(--muted)}

.prose > *{max-width:760px}
.prose h2,.sec-h2{font-family:var(--serif);font-weight:500;font-size:clamp(32px,4vw,50px);line-height:1.1;letter-spacing:-.01em;margin-bottom:18px}
.prose h3{font-family:var(--serif);font-weight:500;font-size:24px;line-height:1.2;margin:30px 0 8px}
.prose p{color:var(--muted);margin-bottom:14px}
.prose p strong{color:var(--cream)}
.prose ul{color:var(--muted);padding-left:20px;margin-bottom:14px}
.prose li{margin-bottom:8px}
.prose a{color:var(--gold-light)}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.cards article{padding:28px 26px;border-radius:22px;background:var(--card);border:1px solid var(--line)}
.cards h3{font-family:var(--serif);font-weight:500;font-size:23px;line-height:1.2;margin-bottom:8px}
.cards p{color:var(--muted);font-size:15.5px}
.citylinks{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}
.citylinks a{padding:10px 18px;border-radius:999px;background:var(--card);border:1px solid var(--line);font-weight:600;font-size:15px;text-decoration:none}
.citylinks a:hover{border-color:rgba(228,185,91,.5);color:var(--gold-light)}
@media (max-width:960px){
  .cards{grid-template-columns:1fr}
  .page-hero .wrap{grid-template-columns:1fr}
  .page-hero .seal-box{order:-1;margin-top:16px}
  .page-hero .seal{width:min(260px,70vw)}
  .steps{grid-template-columns:1fr 1fr}
  .need{grid-template-columns:1fr}
  .breakdown{grid-template-columns:1fr 1fr;padding-left:22px}
}
@media (max-width:620px){
  .page-hero{padding:34px 0 70px}
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

SITE = 'https://latindanceawards.com/'

def crumbs(name, url):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Latin Dance Awards", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + url}]}

def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}}
        for q, _, a, _ in items]}

def page(fname, title_de, desc_de, title_en, desc_en, canonical, main_html, en_dict, page_js, schema=()):
    en = dict(SHARED_EN); en.update(en_dict)
    head = idx[:idx.index('<style>')]
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', head, flags=re.S)
    head += '<script type="application/ld+json">\n' + json.dumps(list(schema), ensure_ascii=False, indent=1) + '\n</script>\n'
    head = re.sub(r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="article">' if False else '<meta property="og:type" content="website">', head, count=1)
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
            + LANG_JS + page_js + '\n  if(start==="en") setLang("en");\n})();\n</script>\n' + NAV_JS + '</body>\n</html>\n')
    if '/' in fname:
        html = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|tel:|data:|javascript:)', r'\1="/', html)
        html = re.sub(r'(href|src)=\\"(?!https?:|/|#|mailto:|tel:|data:|javascript:)', r'\1=\\"/', html)
        html = html.replace('url(fonts/', 'url(/fonts/')
    open(os.path.join(ROOT, fname), 'w', encoding='utf-8').write(html)
    print('wrote', fname, len(html))

def _noop(): pass
class T:
    """Collects German markup + English translations."""
    def __init__(self, prefix): self.p = prefix; self.en = {}; self.n = 0
    def key(self, de, en):
        self.n += 1; k = f'{self.p}{self.n}'; self.en[k] = en; return k
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
 ('Name und Stadt der Schule', 'School name and city', 'Berlin, München, Hamburg, Köln, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nürnberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen oder Bremerhaven', 'Berlin, Munich, Hamburg, Cologne, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nuremberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen or Bremerhaven', False),
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
  'Inhaber, Lehrer oder Mitarbeiter einer Bachata-Schule in Berlin, München, Hamburg, Köln, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nürnberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen oder Bremerhaven. Eure Schule ist in einer anderen Stadt? Bewerbt euch trotzdem, wir nehmen euch für kommende Ausgaben auf.',
  "Owners, teachers or staff of a Bachata school in Berlin, Munich, Hamburg, Cologne, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nuremberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen or Bremerhaven. Your school is in another city? Apply anyway and we'll include you in future editions."),
 ('Wie weisen wir unsere Angaben nach?', 'How do we prove our information?',
  'Mit Links, die es meistens schon gibt: ein Festival-Lineup, euer Kursplan, Posts zu euren Events. Damit wir wissen, dass die Bewerbung wirklich von euch kommt, schickt ihr uns außerdem eine kurze Nachricht von eurem offiziellen Instagram-Account.',
  "With links that usually already exist: a festival lineup, your class schedule, posts about your events. To confirm the application really comes from you, you'll also send us a short message from your official Instagram account."),
 ('Was passiert mit unseren Daten?', 'What happens to our data?',
  'Wir nutzen eure Angaben nur für die Awards. Öffentlich gezeigt werden nur Schulname, Stadt, Punktzahl, die Punkteaufschlüsselung und eure öffentlichen Links. Kontaktdaten bleiben privat.',
  'We only use your information for the awards. We only publish the school name, city, score, score breakdown and your public links. Contact details stay private.'),
]
faq_html = '\n'.join(f'      <details>{t("summary", q_de, q_en)}{t("p", a_de, a_en)}</details>' for q_de, q_en, a_de, a_en in faq)


# ---------- stepped application wizard (one or two questions per screen) ----------
def _opt(kind, name, val, de, en, sub=None):
    inner = t("span", de, en) + (f'<small>{t("span", sub[0], sub[1])}</small>' if sub else '')
    return f'<label><input type="{kind}" name="{name}" value="{val}"><span>{inner}</span></label>'
def _text(name, de, en, typ='text', ph='', help_=None, err=None, req=True, auto='', optional=False):
    opt = f' <span class="opt">{t("span", "optional", "optional")}</span>' if optional else ''
    h = f'<p class="help">{t("span", help_[0], help_[1])}</p>' if help_ else ''
    er = f'<p class="errtxt">{t("span", err[0], err[1])}</p>' if err else '<p class="errtxt"></p>'
    return (f'<div class="fld"><label for="f-{name}">{t("span", de, en)}{opt}</label>'
            f'<input id="f-{name}" name="{name}" type="{typ}" maxlength="400"{" required" if req else ""}{(" autocomplete=" + chr(34) + auto + chr(34)) if auto else ""}'
            f'{(" placeholder=" + chr(34) + ph + chr(34)) if ph else ""}{" inputmode=" + chr(34) + "url" + chr(34) if typ == "url" or ph.startswith("https") else ""}>{h}{er}</div>')
def _choice(name, lab_de, lab_en, opts, cls='chips', kind='radio', err=None, req=True):
    er = f'<p class="errtxt">{t("span", err[0], err[1])}</p>' if err else '<p class="errtxt"></p>'
    lid = f'{name}-l'
    items = ''.join(_opt(kind, name, *o) for o in opts)
    return (f'<div class="fld" data-group="{name}"{" data-req=" + chr(34) + "1" + chr(34) if req else ""}><span class="lab" id="{lid}">{t("span", lab_de, lab_en)}</span>'
            f'<div class="{cls}" role="{"radiogroup" if kind == "radio" else "group"}" aria-labelledby="{lid}">{items}</div>{er}</div>')
def _yn_text(name, lab_de, lab_en, ph_de, ph_en):
    yn = [('Yes', 'Ja', 'Yes'), ('No', 'Nein', 'No')]
    items = ''.join(_opt('radio', name + '_has', *o) for o in yn)
    return (f'<div class="fld" data-group="{name}_has" data-req="1"><span class="lab" id="{name}-l">{t("span", lab_de, lab_en)}</span>'
            f'<div class="chips" role="radiogroup" aria-labelledby="{name}-l">{items}</div><p class="errtxt">{t("span", "Bitte wähle eine Antwort.", "Please choose an answer.")}</p></div>'
            f'<div class="fld reveal" id="rv-{name}" hidden><label for="f-{name}">{t("span", ph_de, ph_en)}</label><textarea id="f-{name}" name="{name}" maxlength="1500"></textarea></div>')
_ERR_URL = ("Bitte gib einen vollständigen Link ein (mit https://).", "Please enter a full link (starting with https://).")
_ERR_PICK = ("Bitte wähle eine Antwort.", "Please choose an answer.")
YEARS = [('2024–2026', '2024–2026', '2024–2026'), ('2021–2023', '2021–2023', '2021–2023'), ('2018–2020', '2018–2020', '2018–2020'),
         ('2015–2017', '2015–2017', '2015–2017'), ('2012–2014', '2012–2014', '2012–2014'), ('Before 2012', 'Vor 2012', 'Before 2012')]
CITIES_O = [('Berlin', 'Berlin', 'Berlin'), ('München / Munich', 'München', 'Munich'), ('Hamburg', 'Hamburg', 'Hamburg'), ('Köln / Cologne', 'Köln', 'Cologne'),
            ('Frankfurt', 'Frankfurt', 'Frankfurt'), ('Düsseldorf', 'Düsseldorf', 'Düsseldorf'), ('Stuttgart', 'Stuttgart', 'Stuttgart'), ('Leipzig', 'Leipzig', 'Leipzig'), ('Dortmund', 'Dortmund', 'Dortmund'), ('Essen', 'Essen', 'Essen'), ('Bremen', 'Bremen', 'Bremen'), ('Dresden', 'Dresden', 'Dresden'), ('Hannover', 'Hannover', 'Hannover'), ('Nürnberg / Nuremberg', 'Nürnberg', 'Nuremberg'), ('Duisburg', 'Duisburg', 'Duisburg'), ('Bochum', 'Bochum', 'Bochum'), ('Bielefeld', 'Bielefeld', 'Bielefeld'), ('Bonn', 'Bonn', 'Bonn'), ('Karlsruhe', 'Karlsruhe', 'Karlsruhe'), ('Mannheim', 'Mannheim', 'Mannheim'), ('Augsburg', 'Augsburg', 'Augsburg'), ('Wiesbaden', 'Wiesbaden', 'Wiesbaden'), ('Gelsenkirchen', 'Gelsenkirchen', 'Gelsenkirchen'), ('Mönchengladbach', 'Mönchengladbach', 'Mönchengladbach'), ('Braunschweig', 'Braunschweig', 'Braunschweig'), ('Aachen', 'Aachen', 'Aachen'), ('Chemnitz', 'Chemnitz', 'Chemnitz'), ('Kiel', 'Kiel', 'Kiel'), ('Freiburg', 'Freiburg', 'Freiburg'), ('Krefeld', 'Krefeld', 'Krefeld'), ('Mainz', 'Mainz', 'Mainz'), ('Oberhausen', 'Oberhausen', 'Oberhausen'), ('Kassel', 'Kassel', 'Kassel'), ('Darmstadt', 'Darmstadt', 'Darmstadt'), ('Hamm', 'Hamm', 'Hamm'), ('Saarbrücken', 'Saarbrücken', 'Saarbrücken'), ('Ludwigshafen', 'Ludwigshafen', 'Ludwigshafen'), ('Potsdam', 'Potsdam', 'Potsdam'), ('Oldenburg', 'Oldenburg', 'Oldenburg'), ('Paderborn', 'Paderborn', 'Paderborn'), ('Würzburg', 'Würzburg', 'Würzburg'), ('Heilbronn', 'Heilbronn', 'Heilbronn'), ('Göttingen', 'Göttingen', 'Göttingen'), ('Reutlingen', 'Reutlingen', 'Reutlingen'), ('Koblenz', 'Koblenz', 'Koblenz'), ('Trier', 'Trier', 'Trier'), ('Erlangen', 'Erlangen', 'Erlangen'), ('Bremerhaven', 'Bremerhaven', 'Bremerhaven'), ('Offenburg', 'Offenburg', 'Offenburg'), ('Konstanz', 'Konstanz', 'Konstanz'), ('Tübingen', 'Tübingen', 'Tübingen'), ('Ludwigsburg', 'Ludwigsburg', 'Ludwigsburg'), ('Bamberg', 'Bamberg', 'Bamberg'), ('Landshut', 'Landshut', 'Landshut'), ('Kempten', 'Kempten', 'Kempten'), ('Aschaffenburg', 'Aschaffenburg', 'Aschaffenburg'), ('Speyer', 'Speyer', 'Speyer'), ('Fulda', 'Fulda', 'Fulda'), ('Lüneburg', 'Lüneburg', 'Lüneburg'), ('Flensburg', 'Flensburg', 'Flensburg'), ('Celle', 'Celle', 'Celle'), ('Ulm', 'Ulm', 'Ulm'), ('Gera', 'Gera', 'Gera'), ('Remscheid', 'Remscheid', 'Remscheid'), ('Bottrop', 'Bottrop', 'Bottrop'), ('Witten', 'Witten', 'Witten'), ('Böblingen', 'Böblingen', 'Böblingen'), ('Friedrichshafen', 'Friedrichshafen', 'Friedrichshafen'), ('Schweinfurt', 'Schweinfurt', 'Schweinfurt'), ('Straubing', 'Straubing', 'Straubing'), ('Coburg', 'Coburg', 'Coburg'), ('Hameln', 'Hameln', 'Hameln'), ('Nürtingen', 'Nürtingen', 'Nürtingen'), ('Norderstedt', 'Norderstedt', 'Norderstedt'), ('Leonberg', 'Leonberg', 'Leonberg'), ('Ansbach', 'Ansbach', 'Ansbach'), ('Moers', 'Moers', 'Moers'), ('Heidenheim', 'Heidenheim', 'Heidenheim'), ('Minden', 'Minden', 'Minden'), ('Other', 'Andere', 'Other')]
# (chapter, title_de, title_en, sub_de, sub_en, body_html, optional, auto)
WIZ = [
 (0, 'Wie heißt deine Schule?', 'What is your school called?', 'Jetzt noch ein paar Angaben zu eurer Schule.', 'Now a few details about your school.',
  _text('school', 'Name der Schule', 'School name', err=("Bitte gib den Namen deiner Schule ein.", "Please enter your school's name."), auto='organization'), False, False),
 (0, 'In welcher Stadt unterrichtet ihr?', 'Which city do you teach in?', 'Nur antippen, keine Tipparbeit.', 'Just tap, no typing.',
  _choice('city', 'Stadt', 'City', CITIES_O, err=_ERR_PICK), False, True),
 (0, 'Wie erreichen wir dich?', 'How can we reach you?', 'Dorthin schicken wir deine Bestätigung. Kein Spam.', "We'll send your confirmation there. No spam.",
  _text('contact', 'Dein Name', 'Your name', err=("Bitte gib deinen Namen ein.", "Please enter your name."), auto='name') +
  _text('email', 'E-Mail', 'Email', 'email', 'name@schule.de', err=("Bitte gib eine gültige E-Mail-Adresse ein.", "Please enter a valid email address."), auto='email'), False, False),
 (1, 'Wie sieht eure Website aus?', 'What is your website?', 'Kopiere einfach den Link aus dem Browser.', 'Just copy the link from your browser.',
  _text('website', 'Website', 'Website', 'url', 'https://', err=_ERR_URL), False, False),
 (1, 'Und euer Google-Maps-Eintrag?', 'And your Google Maps listing?', 'Dort holen wir Bewertungen und Rezensionen.', 'That is where we read your rating and reviews.',
  _text('maps', 'Google-Maps-Link', 'Google Maps link', 'url', 'https://maps.app.goo.gl/…', help_=("In Google Maps nach eurer Schule suchen, auf Teilen tippen, Link kopieren.", "Search your school in Google Maps, tap Share, copy the link."), err=_ERR_URL), False, False),
 (1, 'Seid ihr in den sozialen Medien?', 'Are you on social media?', 'Beides ist freiwillig, bringt aber Punkte.', 'Both are optional but earn points.',
  _text('instagram', 'Instagram', 'Instagram', 'text', 'https://instagram.com/…', req=False, optional=True) + _text('tiktok', 'TikTok', 'TikTok', 'text', 'https://tiktok.com/@…', req=False, optional=True), True, False),
 (2, 'Seit wann unterrichtet ihr Bachata?', 'Since when have you taught Bachata?', 'Eine grobe Angabe reicht.', 'A rough answer is fine.',
  _choice('year', 'Gründungsjahr', 'Year founded', YEARS, err=_ERR_PICK), False, True),
 (2, 'Wie sieht euer Angebot aus?', 'What do you offer?', 'Tippe auf alles, was zutrifft.', 'Tap everything that applies.',
  _choice('trial', 'Probestunde für Anfänger?', 'Trial class for beginners?', [('Yes', 'Ja', 'Yes'), ('No', 'Nein', 'No')], err=_ERR_PICK) +
  _choice('levels', 'Welche Levels bietet ihr an?', 'Which levels do you teach?', [('Beginner', 'Anfänger', 'Beginner'), ('Intermediate', 'Mittelstufe', 'Intermediate'), ('Advanced', 'Fortgeschrittene', 'Advanced')], kind='checkbox', err=("Bitte wähle mindestens ein Level.", "Please choose at least one level.")), False, False),
 (2, 'Wo finden wir euren Kursplan?', 'Where can we find your class schedule?', 'Ein Link zur Seite mit euren Kursen genügt.', 'A link to the page with your classes is enough.',
  _text('schedule', 'Link zum Kursplan', 'Link to your schedule', 'url', 'https://', err=_ERR_URL), False, False),
 (3, 'Haben eure Lehrer auf Festivals unterrichtet?', 'Have your teachers taught at festivals?', 'Bonuspunkte: 2025–2026 zählt.', 'Bonus points: 2025–2026 counts.',
  _yn_text('festivals', 'Festivals und Kongresse', 'Festivals and congresses', 'Auf welchen Festivals?', 'Which festivals?'), False, False),
 (3, 'Wie oft habt ihr Events?', 'How often do you run events?', 'Socials, Workshops und Gäste der letzten 12 Monate.', 'Socials, workshops and guests in the last 12 months.',
  _choice('social', 'Eigene Socials oder Workshops', 'Own socials or workshops', [('Weekly', 'Wöchentlich', 'Weekly'), ('Monthly', 'Monatlich', 'Monthly'), ('Few per year', 'Ein paar im Jahr', 'A few a year'), ('None', 'Keine', 'None')], err=_ERR_PICK) +
  _choice('guests', 'Gastlehrer aus dem Ausland?', 'International guest teachers?', [('Yes', 'Ja', 'Yes'), ('No', 'Nein', 'No')], err=_ERR_PICK), False, False),
 (3, 'Habt ihr Wettbewerbe gewonnen?', 'Have you won competitions?', 'Schüler oder Lehrer, mit online veröffentlichten Ergebnissen.', 'Students or teachers, with results published online.',
  _yn_text('competitions', 'Wettbewerbe', 'Competitions', 'Welcher Wettbewerb, welches Jahr, welcher Platz?', 'Which competition, which year, which place?'), False, False),
 (3, 'Fast geschafft!', 'Almost done!', 'Noch ein Haken, dann bist du dabei.', 'One last tick and you are in.',
  '<label class="consent"><input type="checkbox" name="consent" required><span>' + t("span", "Ich stimme zu, dass meine Angaben für die Latin Dance Awards gespeichert und ausgewertet werden. Öffentlich gezeigt werden nur Schulname, Stadt, Punktzahl und öffentliche Links.", "I agree that my information is stored and evaluated for the Latin Dance Awards. Only the school name, city, score and public links are shown publicly.") + '</span></label>'
  '<p class="errtxt" id="consent-err" style="display:none;color:#f2a299;font-size:13.5px;margin-top:6px">' + t("span", "Bitte stimme zu, damit wir deine Bewerbung speichern dürfen.", "Please agree so we can save your application.") + '</p>', False, False),
]
_ORDER = [(1, 0), (6, 0), (7, 0), (10, 0), (9, 0), (11, 0), (0, 1), (3, 1), (4, 1), (8, 1), (5, 1), (2, 2), (12, 2)]
WIZ = [(ch,) + WIZ[k][1:] for k, ch in _ORDER]
_panes = ''
for i, (ch, td, te, sd, se, body, optional, auto) in enumerate(WIZ):
    _panes += (f'<section class="step-pane{" on" if i == 0 else ""}" data-ch="{ch}"{" data-opt=" + chr(34) + "1" + chr(34) if optional else ""}{" data-auto=" + chr(34) + "1" + chr(34) if auto else ""} aria-labelledby="sh{i}">'
               f'{t("h3", td, te, f"id=" + chr(34) + f"sh{i}" + chr(34) + " tabindex=" + chr(34) + "-1" + chr(34))}{t("p", sd, se, "class=" + chr(34) + "sub" + chr(34))}{body}</section>\n')
wiz_html = f"""      <div class="wiz">
      <form id="lda-form" novalidate hidden data-total="{len(WIZ)}">
        <div class="hp" aria-hidden="true"><label>Website2 <input type="text" name="hp" tabindex="-1" autocomplete="off"></label></div>
        <div class="wiz-top"><span>{t("span", "Schritt", "Step")} <b id="w-n">1</b> {t("span", "von", "of")} {len(WIZ)}</span><span id="w-left">{t("span", "noch ca. 2 Min.", "about 2 min left")}</span></div>
        <div class="wiz-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="8" id="w-bar"><i></i></div>
        <div class="wiz-dots" aria-hidden="true"><span class="on">{t("span", "Fragen", "Questions")}</span><span>{t("span", "Eure Schule", "Your school")}</span><span>{t("span", "Kontakt", "Contact")}</span></div>
{_panes}        <div class="msg" id="form-err" hidden role="alert"></div>
        <div class="wiz-nav">
          <button type="button" class="back" id="w-back" hidden>← {t("span", "Zurück", "Back")}</button>
          <button type="button" class="skip" id="w-skip" hidden>{t("span", "Überspringen", "Skip")}</button>
          <button class="btn btn-gold" type="button" id="w-next">{t("span", "Weiter", "Continue")} →</button>
        </div>
        <div class="trust"><span>{t("span", "Kostenlos", "Free")}</span><span>{t("span", "Keine Zahlung", "No payment")}</span><span>{t("span", "Bewerbungsschluss 30. November", "Deadline November 30")}</span></div>
      </form>
      <div class="form-ok" id="form-ok" hidden>
        {t("h3", "Geschafft, deine Schule ist dabei!", "Done, your school is in!")}
        {t("p", "Wir haben deine Bewerbung erhalten. Schau auch im Spam-Ordner nach der Bestätigung.", "We've received your application. Check your spam folder for the confirmation too.")}
        <ol><li><b>{t("span", "In 3 Tagen", "In 3 days")}</b> · {t("span", "Wir melden uns per E-Mail und bitten um ein paar Nachweise.", "We email you and ask for a few proofs.")}</li><li><b>{t("span", "Bis 30. November", "By November 30")}</b> · {t("span", "Nachweise als einfache Links schicken.", "Send the proofs as simple links.")}</li><li><b>{t("span", "20. Dezember, 19 Uhr", "December 20, 7 pm")}</b> · {t("span", "Ergebnisse und Award-Siegel.", "Results and award seal.")}</li></ol>
      </div>
      </div>"""

app_main = f'''
<section class="page-hero" aria-labelledby="app-title">
  <div class="wrap">
    <div>
      <span class="edition rise d1"><i></i>{t("span", "Bewerbung · Awards 2026", "Application · Awards 2026")}</span>
      <h1 id="app-title" class="rise d2">{t("span", "Bachata-Schule anmelden für die <em class=\"foil\">Bachata Awards 2026</em>", "Enter your Bachata school for the <em class=\"foil\">Bachata Awards 2026</em>")}</h1>
      <p class="lede rise d3">{t("span", "Melde deine Bachata-Schule kostenlos an: Die Bewerbung dauert fünf Minuten und ist offen für jede Bachata-Schule in Berlin, München, Hamburg, Köln, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nürnberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen, Bremerhaven, Offenburg, Konstanz, Tübingen, Ludwigsburg, Bamberg, Landshut, Kempten, Aschaffenburg, Speyer, Fulda, Lüneburg, Flensburg, Celle, Ulm, Gera, Remscheid, Bottrop, Witten, Böblingen, Friedrichshafen, Schweinfurt, Straubing, Coburg, Hameln, Nürtingen, Norderstedt, Leonberg, Ansbach, Moers, Heidenheim und Minden.", "Enter your Bachata school for free: applying takes five minutes and is open to every Bachata school in Berlin, Munich, Hamburg, Cologne, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nuremberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen, Bremerhaven, Offenburg, Konstanz, Tübingen, Ludwigsburg, Bamberg, Landshut, Kempten, Aschaffenburg, Speyer, Fulda, Lüneburg, Flensburg, Celle, Ulm, Gera, Remscheid, Bottrop, Witten, Böblingen, Friedrichshafen, Schweinfurt, Straubing, Coburg, Hameln, Nürtingen, Norderstedt, Leonberg, Ansbach, Moers, Heidenheim and Minden.")}</p>
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
      <img class="seal" src="badge-winner-template.svg" alt="Siegel Best School · Official Winner der Bachata Awards 2026" width="360" height="360" fetchpriority="low">
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

<section class="block" aria-labelledby="why-title">
  <div class="wrap">
    <div class="sec-head">
      {t("h2", "Warum sich die Anmeldung lohnt", "Why entering is worth it", 'id="why-title"')}
      {t("p", "Die Teilnahme kostet nichts und bringt deiner Schule Sichtbarkeit bei Tänzern, die gerade eine Bachata-Schule suchen.", "Taking part costs nothing and puts your school in front of dancers who are looking for a Bachata school right now.")}
    </div>
    <div class="cards">
      <article>{t("h3", "Ein offizielles Siegel", "An official seal", "")}{t("p", "Gewinner bekommen das Award-Siegel für Website, Studio und Social Media. Es zeigt neuen Schülern auf einen Blick, dass eure Qualität unabhängig bestätigt wurde.", "Winners get the award seal for their website, studio and social media. It shows new students at a glance that your quality has been confirmed independently.")}</article>
      <article>{t("h3", "Sichtbar in deiner Stadt", "Visible in your city", "")}{t("p", "Jede Stadt bekommt eine eigene Ranking-Seite. Dort landen Tänzer, die nach einer Bachata-Schule in Berlin, München oder Köln suchen.", "Every city gets its own ranking page. That is where dancers land when they look for a Bachata school in Berlin, Munich or Cologne.")}</article>
      <article>{t("h3", "Ehrliches Feedback", "Honest feedback", "")}{t("p", "Du siehst deine Punkte in allen neun Kriterien. So weißt du genau, wo eure Schule stark ist und wo noch Potenzial liegt.", "You see your points in all nine factors, so you know exactly where your school is strong and where there is room to grow.")}</article>
    </div>
  </div>
</section>

<section class="block alt" aria-labelledby="score-title">
  <div class="wrap prose">
    {t("h2", "So bewerten wir die Schulen", "How we score the schools", 'id="score-title" class="sec-h2"')}
    {t("p", "Alle Bachata-Schulen werden nach denselben neun Kriterien bewertet, zusammen <strong>100 Punkte</strong>. Die meisten Punkte gibt es für die Google-Bewertung (25), Festivals und Kongresse (15), die Anzahl der Bewertungen, die Jahre im Unterricht, das Kursangebot für Einsteiger, eigene Events und Social Media (je 10). Aktuelle Bewertungen und Wettbewerbe zählen je 5 Punkte.", "All Bachata schools are scored on the same nine factors, <strong>100 points</strong> in total. The most points come from the Google rating (25), festivals and congresses (15), and review volume, years of teaching, the beginner offer, own events and social media (10 each). Recent reviews and competitions count 5 points each.")}
    {t("p", "Mit deiner Bewerbung bestätigst du die Angaben, die wir sonst nur schätzen könnten. Was wir nicht bestätigen können, zählt mit 0 Punkten. Die vollständige Methode steht auf der <a href=\"index.html#method\">Startseite</a>.", "Your application confirms the information we could otherwise only estimate. Anything we can't confirm counts as 0 points. The full method is on the <a href=\"index.html#method\">homepage</a>.")}
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
      {t("h2", "In 2 Minuten bewerben", "Apply in 2 minutes", 'id="form-title"')}
      {t("p", "Eine kleine Frage nach der anderen, meist mit einem Tipp. Kostenlos, ohne Zahlung.", "One small question at a time, mostly with a tap. Free, no payment.")}
{wiz_html}
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
  /* ===== Paste the Google Apps Script web-app URL here (see automation/collect.gs) ===== */
  var FORM_ENDPOINT = "https://script.google.com/macros/s/AKfycbzAANOuM7cA3QgqeXZXOKZEYumNFsENBZaIicJSaJluR90rTl2iw30Sk522vxIurDsg/exec";

  var form=document.getElementById("lda-form"), fb=document.getElementById("form-fallback"), ok=document.getElementById("form-ok"),
      err=document.getElementById("form-err"), nextB=document.getElementById("w-next"), backB=document.getElementById("w-back"), skipB=document.getElementById("w-skip"),
      bar=document.getElementById("w-bar"), nEl=document.getElementById("w-n"), leftEl=document.getElementById("w-left"),
      panes=[].slice.call(document.querySelectorAll(".step-pane")), dots=[].slice.call(document.querySelectorAll(".wiz-dots > span"));
  var STEPS=panes.length, cur=0, timer=null;
  var MSG={
    de:{next:"Weiter", send:"Bewerbung absenden", wait:"Wird gesendet …", fail:"Das Senden hat nicht geklappt. Bitte versuche es noch einmal oder schreib uns an hello@latindanceawards.com.", left:["noch ca. 2 Min.","noch ca. 1 Min.","noch ca. 30 Sek.","fast fertig"]},
    en:{next:"Continue", send:"Submit application", wait:"Sending …", fail:"Sending failed. Please try again or email us at hello@latindanceawards.com.", left:["about 2 min left","about 1 min left","about 30 sec left","almost done"]}
  };
  function M(){ return MSG[window.LANG==="en"?"en":"de"]; }
  if(FORM_ENDPOINT){ form.hidden=false; fb.hidden=true; } else { form.hidden=true; fb.hidden=false; }

  function checked(n){ return [].slice.call(form.querySelectorAll('[name="'+n+'"]:checked')).map(function(x){return x.value;}); }
  var TEXT=["school","contact","email","website","maps","instagram","tiktok","schedule","festivals","competitions"];
  var PICK=["city","year","trial","social","guests","festivals_has","competitions_has"], MULTI=["levels"];
  function save(){ try{ var o={}; TEXT.forEach(function(k){ o[k]=form.elements[k].value; }); PICK.forEach(function(k){ o[k]=checked(k)[0]||""; }); o.levels=checked("levels").join("|"); localStorage.setItem("lda-apply2",JSON.stringify(o)); }catch(e){} }
  function restore(){ try{ var o=JSON.parse(localStorage.getItem("lda-apply2")||"{}");
      TEXT.forEach(function(k){ if(o[k]) form.elements[k].value=o[k]; });
      PICK.forEach(function(k){ if(o[k]){ var r=form.querySelector('[name="'+k+'"][value="'+o[k].replace(/"/g,"")+'"]'); if(r) r.checked=true; } });
      (o.levels||"").split("|").forEach(function(v){ var r=v&&form.querySelector('[name="levels"][value="'+v+'"]'); if(r) r.checked=true; }); }catch(e){}
    ["festivals","competitions"].forEach(reveal); }
  function reveal(n){ var has=checked(n+"_has")[0]; document.getElementById("rv-"+n).hidden=(has!=="Yes"); }
  form.addEventListener("input",save); form.addEventListener("change",save);

  function urlOK(v){ return /^https?:\/\/\S+\.\S+/i.test(v); }
  function setBad(box,bad){ if(box) box.classList.toggle("bad",bad); }
  function validPane(p){
    var first=null;
    [].slice.call(p.querySelectorAll(".fld[data-req]")).forEach(function(box){
      var n=box.dataset.group, good=checked(n).length>0; setBad(box,!good); if(!good&&!first) first=box.querySelector("input"); });
    [].slice.call(p.querySelectorAll("input[required]:not([type=radio]):not([type=checkbox])")).forEach(function(el){
      var v=el.value.trim(), good=!!v;
      if(good&&el.type==="email") good=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v);
      if(good&&el.type==="url") good=urlOK(v);
      setBad(el.closest(".fld"),!good); if(!good&&!first) first=el; });
    if(p.querySelector('[name="consent"]')){ var c=form.elements.consent, ce=document.getElementById("consent-err"); ce.style.display=c.checked?"none":"block"; if(!c.checked&&!first) first=c; }
    if(first){ first.focus({preventScroll:false}); return false; } return true; }
  form.addEventListener("focusout",function(e){ var el=e.target; if(el.name&&el.required&&el.type!=="radio"&&el.type!=="checkbox"&&(el.value||"").length){
      var v=el.value.trim(), good=(el.type==="email"?/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v):el.type==="url"?urlOK(v):true); setBad(el.closest(".fld"),!good); } });

  function show(i,focus){
    cur=i; panes.forEach(function(p,k){ p.classList.toggle("on",k===i); });
    var ch=+panes[i].dataset.ch; dots.forEach(function(d,k){ d.className=k<ch?"done":(k===ch?"on":""); });
    var pct=Math.round(8+(i/(STEPS-1))*86); bar.firstElementChild.style.width=pct+"%"; bar.setAttribute("aria-valuenow",pct);
    nEl.textContent=i+1; var rem=(STEPS-i)*8; leftEl.textContent=M().left[rem>75?0:rem>45?1:rem>20?2:3];
    backB.hidden=(i===0); skipB.hidden=!panes[i].dataset.opt; renderBtn(); err.hidden=true;
    // pure single-choice screens advance by themselves, so hide the button there
    nextB.style.display=(panes[i].dataset.auto?"none":"");
    if(focus){ var h=panes[i].querySelector("h3"); h.focus({preventScroll:true}); form.scrollIntoView({behavior:"smooth",block:"start"}); }
  }
  function renderBtn(){ var last=(cur===STEPS-1); nextB.innerHTML=(last?M().send:M().next)+(last?"":" →"); }
  function go(){ if(!validPane(panes[cur])) return; if(cur<STEPS-1) show(cur+1,true); else submit(); }
  nextB.addEventListener("click",go);
  skipB.addEventListener("click",function(){ show(cur+1,true); });
  backB.addEventListener("click",function(){ clearTimeout(timer); if(cur>0) show(cur-1,true); });
  form.addEventListener("keydown",function(e){ if(e.key==="Enter"&&e.target.tagName!=="TEXTAREA"&&e.target.type!=="checkbox"&&e.target.type!=="radio"){ e.preventDefault(); go(); } });
  form.addEventListener("submit",function(e){ e.preventDefault(); });
  form.addEventListener("change",function(e){
    var t=e.target; if(t.type!=="radio"&&t.type!=="checkbox") return;
    setBad(t.closest(".fld"),false);
    if(t.name==="festivals_has"||t.name==="competitions_has") reveal(t.name.replace("_has",""));
    var p=t.closest(".step-pane"); if(!p) return;
    var advance=(p.dataset.auto&&t.type==="radio")||((t.name==="festivals_has"||t.name==="competitions_has")&&t.value==="No");
    if(advance){ clearTimeout(timer); timer=setTimeout(function(){ if(cur<STEPS-1&&panes[cur]===p) show(cur+1,true); },320); }
  });

  function submit(){
    var f=form.elements; if(f.hp.value) return;
    nextB.disabled=true; nextB.textContent=M().wait;
    var body=new URLSearchParams(), v=function(n){ return f[n].value.trim(); };
    ["school","contact","email","website","maps","instagram","tiktok","schedule"].forEach(function(k){ body.append(k,v(k)); });
    ["city","year","trial","social","guests"].forEach(function(k){ body.append(k,checked(k)[0]||""); });
    body.append("levels",checked("levels").join(", "));
    ["festivals","competitions"].forEach(function(k){ var h=checked(k+"_has")[0]; body.append(k,h==="No"?"No":(v(k)||(h==="Yes"?"Yes":""))); });
    body.append("language", window.LANG==="en"?"EN":"DE");
    fetch(FORM_ENDPOINT,{method:"POST",mode:"no-cors",body:body}).then(function(){
      try{ localStorage.removeItem("lda-apply2"); }catch(e){}
      form.hidden=true; ok.hidden=false; ok.scrollIntoView({behavior:"smooth",block:"center"});
    }).catch(function(){ nextB.disabled=false; renderBtn(); err.textContent=M().fail; err.hidden=false; });
  }
  document.addEventListener("langchange",function(){ if(!nextB.disabled){ renderBtn(); var rem=(STEPS-cur)*8; leftEl.textContent=M().left[rem>75?0:rem>45?1:rem>20?2:3]; } });
  restore(); show(0,false);
'''

page('bewerbung.html',
     'Bachata-Schule anmelden · Bachata Awards 2026',
     'Bachata-Schule kostenlos anmelden für die Bachata Awards 2026: Bewerbung in fünf Minuten, Bewerbungsschluss 30. November, Ergebnisse am 20. Dezember.',
     'Enter your Bachata school · Bachata Awards 2026',
     'Enter your Bachata school for the Latin Dance Awards 2026 for free. Deadline November 30, results on December 20.',
     'bewerbung.html', app_main, t.en, app_js,
     schema=[crumbs('Bewerbung', 'bewerbung.html'), faq_schema(faq)])

# ======================================================================
# RANKINGS PAGE
# ======================================================================
r = T('r')
CITIES = [('deutschland', 'Ganz Deutschland', 'All Germany'), ('berlin', 'Berlin', 'Berlin'), ('muenchen', 'München', 'Munich'),
          ('hamburg', 'Hamburg', 'Hamburg'), ('koeln', 'Köln', 'Cologne'), ('frankfurt', 'Frankfurt', 'Frankfurt'),
          ('duesseldorf', 'Düsseldorf', 'Düsseldorf'), ('stuttgart', 'Stuttgart', 'Stuttgart'), ('leipzig', 'Leipzig', 'Leipzig'),
          ('dortmund', 'Dortmund', 'Dortmund'), ('essen', 'Essen', 'Essen'), ('bremen', 'Bremen', 'Bremen'), ('dresden', 'Dresden', 'Dresden'),
          ('hannover', 'Hannover', 'Hannover'), ('nuernberg', 'Nürnberg', 'Nuremberg'),
          ('duisburg', 'Duisburg', 'Duisburg'), ('bochum', 'Bochum', 'Bochum'), ('bielefeld', 'Bielefeld', 'Bielefeld'), ('bonn', 'Bonn', 'Bonn'),
          ('karlsruhe', 'Karlsruhe', 'Karlsruhe'), ('mannheim', 'Mannheim', 'Mannheim'), ('augsburg', 'Augsburg', 'Augsburg'), ('wiesbaden', 'Wiesbaden', 'Wiesbaden'),
          ('gelsenkirchen', 'Gelsenkirchen', 'Gelsenkirchen'), ('moenchengladbach', 'Mönchengladbach', 'Mönchengladbach'), ('braunschweig', 'Braunschweig', 'Braunschweig'), ('aachen', 'Aachen', 'Aachen'), ('chemnitz', 'Chemnitz', 'Chemnitz'), ('kiel', 'Kiel', 'Kiel'), ('freiburg', 'Freiburg', 'Freiburg'), ('krefeld', 'Krefeld', 'Krefeld'), ('mainz', 'Mainz', 'Mainz'), ('oberhausen', 'Oberhausen', 'Oberhausen'), ('kassel', 'Kassel', 'Kassel'), ('darmstadt', 'Darmstadt', 'Darmstadt'),
          ('hamm', 'Hamm', 'Hamm'), ('saarbruecken', 'Saarbrücken', 'Saarbrücken'), ('ludwigshafen', 'Ludwigshafen', 'Ludwigshafen'), ('potsdam', 'Potsdam', 'Potsdam'), ('oldenburg', 'Oldenburg', 'Oldenburg'), ('paderborn', 'Paderborn', 'Paderborn'), ('wuerzburg', 'Würzburg', 'Würzburg'), ('heilbronn', 'Heilbronn', 'Heilbronn'),
          ('goettingen', 'Göttingen', 'Göttingen'), ('reutlingen', 'Reutlingen', 'Reutlingen'), ('koblenz', 'Koblenz', 'Koblenz'), ('trier', 'Trier', 'Trier'), ('erlangen', 'Erlangen', 'Erlangen'), ('bremerhaven', 'Bremerhaven', 'Bremerhaven'), ('offenburg', 'Offenburg', 'Offenburg'), ('konstanz', 'Konstanz', 'Konstanz'), ('tuebingen', 'Tübingen', 'Tübingen'), ('ludwigsburg', 'Ludwigsburg', 'Ludwigsburg'), ('bamberg', 'Bamberg', 'Bamberg'), ('landshut', 'Landshut', 'Landshut'), ('kempten', 'Kempten', 'Kempten'), ('aschaffenburg', 'Aschaffenburg', 'Aschaffenburg'), ('speyer', 'Speyer', 'Speyer'), ('fulda', 'Fulda', 'Fulda'), ('lueneburg', 'Lüneburg', 'Lüneburg'), ('flensburg', 'Flensburg', 'Flensburg'), ('celle', 'Celle', 'Celle'), ('ulm', 'Ulm', 'Ulm'), ('gera', 'Gera', 'Gera'), ('remscheid', 'Remscheid', 'Remscheid'), ('bottrop', 'Bottrop', 'Bottrop'), ('witten', 'Witten', 'Witten'), ('boeblingen', 'Böblingen', 'Böblingen'), ('friedrichshafen', 'Friedrichshafen', 'Friedrichshafen'), ('schweinfurt', 'Schweinfurt', 'Schweinfurt'), ('straubing', 'Straubing', 'Straubing'), ('coburg', 'Coburg', 'Coburg'), ('hameln', 'Hameln', 'Hameln'), ('nuertingen', 'Nürtingen', 'Nürtingen'), ('norderstedt', 'Norderstedt', 'Norderstedt'), ('leonberg', 'Leonberg', 'Leonberg'), ('ansbach', 'Ansbach', 'Ansbach'), ('moers', 'Moers', 'Moers'), ('heidenheim', 'Heidenheim', 'Heidenheim'), ('minden', 'Minden', 'Minden')]
tabs_html = '\n'.join(
    f'      <button type="button" role="tab" id="tab-{slug}" aria-controls="panel" aria-selected="{"true" if i==0 else "false"}" data-city="{slug}">{r("span", de, en)}</button>'
    for i, (slug, de, en) in enumerate(CITIES) if i < 7)


rfaq = [
 ('Wann wird das Bachata-Ranking veröffentlicht?', 'When is the Bachata ranking published?',
  'Alle Rankings erscheinen am 20. Dezember 2026 um 19 Uhr auf dieser Seite, zuerst für die 79 Städte und gleichzeitig für ganz Deutschland.',
  'All rankings go live on December 20, 2026 at 7 pm (CET) on this page, for the 79 cities and for Germany as a whole.'),
 ('Welche Städte sind im Ranking 2026?', 'Which cities are in the 2026 ranking?',
  'Berlin, München, Hamburg, Köln, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nürnberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen, Bremerhaven, Offenburg, Konstanz, Tübingen, Ludwigsburg, Bamberg, Landshut, Kempten, Aschaffenburg, Speyer, Fulda, Lüneburg, Flensburg, Celle, Ulm, Gera, Remscheid, Bottrop, Witten, Böblingen, Friedrichshafen, Schweinfurt, Straubing, Coburg, Hameln, Nürtingen, Norderstedt, Leonberg, Ansbach, Moers, Heidenheim und Minden. Weitere Städte und Länder folgen in den nächsten Ausgaben.',
  'Berlin, Munich, Hamburg, Cologne, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nuremberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen, Bremerhaven, Offenburg, Konstanz, Tübingen, Ludwigsburg, Bamberg, Landshut, Kempten, Aschaffenburg, Speyer, Fulda, Lüneburg, Flensburg, Celle, Ulm, Gera, Remscheid, Bottrop, Witten, Böblingen, Friedrichshafen, Schweinfurt, Straubing, Coburg, Hameln, Nürtingen, Norderstedt, Leonberg, Ansbach, Moers, Heidenheim and Minden. More cities and countries follow in future editions.'),
 ('Kann eine Schule für einen besseren Platz bezahlen?', 'Can a school pay for a better place?',
  'Nein. Plätze sind nicht käuflich. Jede Schule wird nach denselben neun Kriterien bewertet, und die Punkteaufschlüsselung ist öffentlich.',
  'No. Places cannot be bought. Every school is scored on the same nine factors, and the score breakdown is public.'),
 ('Brauche ich einen Tanzpartner für einen Bachata-Kurs?', 'Do I need a partner for a Bachata class?',
  'In den meisten Bachata-Kursen nicht. Viele Schulen lassen die Paare regelmäßig wechseln, sodass du auch allein kommen kannst. Frag am besten vorher bei der Schule nach.',
  'In most Bachata classes you don\'t. Many schools rotate partners regularly, so you can come on your own. It is best to ask the school beforehand.'),
 ('Meine Schule fehlt. Was kann ich tun?', 'My school is missing. What can I do?',
  'Melde sie bis zum 30. November kostenlos über die <a href="bewerbung.html">Bewerbungsseite</a> an. Wir nehmen jede Bachata-Schule in den 79 Städten auf.',
  'Enter it for free by November 30 on the <a href="bewerbung.html">application page</a>. We include every Bachata school in the 79 cities.'),
 ('Wie oft wird das Ranking aktualisiert?', 'How often is the ranking updated?',
  'Das Ranking erscheint einmal im Jahr. Korrekturen an falschen Daten prüfen wir laufend und übernehmen sie nach der Prüfung.',
  'The ranking is published once a year. We review corrections to wrong data on an ongoing basis and apply them once checked.'),
]
rfaq_html = '\n'.join(f'      <details>{r("summary", q_de, q_en)}{r("p", a_de, a_en)}</details>' for q_de, q_en, a_de, a_en in rfaq)
city_links = ''.join(f'<a href="#{slug}">{r("span", de, en)}</a>' for slug, de, en in CITIES[1:])

rank_main = f'''
<section class="page-hero" aria-labelledby="rk-title">
  <div class="wrap">
    <div>
      <span class="edition rise d1"><i></i>{r("span", "Rankings 2026 · Deutschland", "Rankings 2026 · Germany")}</span>
      <h1 id="rk-title" class="rise d2">{r("span", "Beste Bachata-Schulen in <em class=\"foil\">Deutschland 2026</em>", "Best Bachata schools in <em class=\"foil\">Germany 2026</em>")}</h1>
      <p class="lede rise d3">{r("span", "Die besten Bachata-Schulen in Deutschland, bewertet nach neun öffentlichen Kriterien: 79 Städte, ein nationaler Sieger. Die Ergebnisse erscheinen am 20. Dezember 2026 um 19 Uhr.", "The best Bachata schools in Germany, scored on nine public factors: 79 cities, one national winner. Results are published on December 20, 2026 at 7 pm (CET).")}</p>
      <div class="countdown rise d4" id="countdown" aria-live="off">
        <div><b data-u="d">00</b>{r("small", "Tage", "days")}</div>
        <div><b data-u="h">00</b>{r("small", "Stunden", "hours")}</div>
        <div><b data-u="m">00</b>{r("small", "Minuten", "minutes")}</div>
        <div><b data-u="s">00</b>{r("small", "Sekunden", "seconds")}</div>
      </div>
      <div class="ctas rise d5">
        <a class="btn btn-gold" href="#ranking">{r("span", "Zwischenstand ansehen ↓", "See the interim standing ↓")}</a>
        <a class="btn btn-ghost" href="bewerbung.html">{r("span", "Schule kostenlos bewerben", "Enter a school for free")}</a>
      </div>
    </div>
    <div class="seal-box rise d3"><img class="seal" src="badge-bachata-2026.svg" alt="Siegel der Bachata Awards 2026, Deutschland" width="360" height="360" fetchpriority="low"></div>
  </div>
</section>

<section class="block alt" id="ranking" aria-label="Rankings">
  <div class="wrap">
    <div class="tabs" role="tablist" aria-label="Städte / Cities">
{tabs_html}
      <div class="citypick" id="citypick">
        <input id="cityq" type="text" role="combobox" aria-expanded="false" aria-controls="citylist" aria-autocomplete="list" autocomplete="off" spellcheck="false" data-ph-de="Stadt suchen …" data-ph-en="Search city …" aria-label="Stadt suchen / Search city">
        <ul id="citylist" role="listbox" hidden></ul>
      </div>
    </div>
    <div id="panel" role="tabpanel"></div>
  </div>
</section>

<section class="block" aria-labelledby="why-title">
  <div class="wrap">
    {r("h2", "Warum das Ranking wichtig ist", "Why the ranking matters", 'id="why-title" class="sec-h2"')}
    {r("p", "Ein faires, öffentliches Ranking hilft allen, die Bachata in Deutschland lieben.", "A fair, public ranking helps everyone who loves Bachata in Germany.", 'class="lede" style="color:var(--muted);max-width:640px;margin-bottom:34px"')}
    <div class="cards">
      <article>
        {r("h3", "Für Tänzer", "For dancers")}
        {r("p", "Statt Raten gibt es eine klare Orientierung: Du siehst, welche Schule in deiner Stadt zu dir passt, ob es eine Probestunde gibt und wie gut die Schule bewertet ist. Das spart Zeit und schützt vor Fehlstarts.", "Instead of guessing, you get clear guidance: see which school in your city suits you, whether there is a trial class and how well the school is rated. It saves time and avoids a bad start.")}
      </article>
      <article>
        {r("h3", "Für Schulen", "For schools")}
        {r("p", "Gute Arbeit wird sichtbar, auch bei kleinen Schulen. Die Punkteaufschlüsselung zeigt, wo ihr stark seid und wo ihr wachsen könnt. Gewinner erhalten ein offizielles Siegel für Website, Studio und Social Media.", "Good work becomes visible, even for small schools. The score breakdown shows where you are strong and where you can grow. Winners receive an official seal for their website, studio and social media.")}
      </article>
      <article>
        {r("h3", "Für die Community", "For the community")}
        {r("p", "Wettbewerb motiviert, bessere Kurse, mehr Socials und mehr Gastlehrer anzubieten. Davon profitiert die ganze Szene: Mehr Tänzer finden den Einstieg, und die Bachata-Community in Deutschland wächst gemeinsam.", "Friendly competition motivates schools to offer better classes, more socials and more guest teachers. The whole scene benefits: more dancers find their way in, and the German Bachata community grows together.")}
      </article>
    </div>
  </div>
</section>

<section class="block alt" aria-labelledby="how-title">
  <div class="wrap prose">
    {r("h2", "So entsteht das Bachata-Ranking 2026", "How the 2026 Bachata ranking is made", 'id="how-title"')}
    {r("p", "Wir recherchieren jede Bachata-Schule in Berlin, München, Hamburg, Köln, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nürnberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen, Bremerhaven, Offenburg, Konstanz, Tübingen, Ludwigsburg, Bamberg, Landshut, Kempten, Aschaffenburg, Speyer, Fulda, Lüneburg, Flensburg, Celle, Ulm, Gera, Remscheid, Bottrop, Witten, Böblingen, Friedrichshafen, Schweinfurt, Straubing, Coburg, Hameln, Nürtingen, Norderstedt, Leonberg, Ansbach, Moers, Heidenheim und Minden und bewerten sie nach denselben <strong>neun Kriterien</strong>, zusammen 100 Punkte. Die wichtigsten sind die gewichtete Google-Bewertung (25 Punkte) und Auftritte der Lehrer auf Festivals und Kongressen (15 Punkte).", "We research every Bachata school in Berlin, Munich, Hamburg, Cologne, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nuremberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen, Bremerhaven, Offenburg, Konstanz, Tübingen, Ludwigsburg, Bamberg, Landshut, Kempten, Aschaffenburg, Speyer, Fulda, Lüneburg, Flensburg, Celle, Ulm, Gera, Remscheid, Bottrop, Witten, Böblingen, Friedrichshafen, Schweinfurt, Straubing, Coburg, Hameln, Nürtingen, Norderstedt, Leonberg, Ansbach, Moers, Heidenheim and Minden and score each one on the same <strong>nine factors</strong>, 100 points in total. The most important are the weighted Google rating (25 points) and teachers' appearances at festivals and congresses (15 points).")}
    {r("p", "Dazu kommen die Anzahl der Bewertungen, die Jahre im Unterricht, das Kursangebot für Einsteiger, eigene Events und Gastlehrer sowie Social Media mit je 10 Punkten. Aktuelle Bewertungen der letzten 12 Monate und Wettbewerbsergebnisse zählen je 5 Punkte. Alle Daten sind öffentlich und werden von Hand geprüft. Schulen, die sich bewerben, können ihre Angaben zusätzlich mit Links belegen.", "Review volume, years of teaching, the beginner offer, own events and guest teachers, and social media add 10 points each. Recent reviews from the last 12 months and competition results count 5 points each. All data is public and checked by hand. Schools that apply can also back up their information with links.")}
    {r("p", "Damit kleine Schulen eine faire Chance haben, gewichten wir Bewertungen nach ihrer Anzahl: Eine 5,0 aus vier Bewertungen schlägt keine 4,8 aus dreihundert. Die vollständige Methode findest du auf der <a href=\"index.html#method\">Startseite</a>.", "To give small schools a fair chance, ratings are weighted by their number: a 5.0 from four reviews does not beat a 4.8 from three hundred. The full method is on the <a href=\"index.html#method\">homepage</a>.")}
  </div>
</section>

<section class="block" aria-labelledby="awards-title">
  <div class="wrap prose">
    {r("h2", "Die fünf Bachata Awards 2026 im Überblick", "The five Bachata Awards 2026 at a glance", 'id="awards-title"')}
    {r("p", "Neben den Ranglisten vergeben wir fünf Auszeichnungen. Jeder Gewinner erhält ein offizielles Siegel für Website, Studio und Social Media.", "Alongside the rankings we give five awards. Every winner receives an official seal for their website, studio and social media.")}
    <ul>
      <li>{r("span", "<strong>Beste Bachata-Schule Deutschlands:</strong> die höchste Gesamtpunktzahl aller 79 Städte.", "<strong>Best Bachata School in Germany:</strong> the highest total score across all 79 cities.")}</li>
      <li>{r("span", "<strong>Beste Schule der Stadt:</strong> die bestplatzierte Schule in Berlin, München, Hamburg, Köln, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nürnberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen, Bremerhaven, Offenburg, Konstanz, Tübingen, Ludwigsburg, Bamberg, Landshut, Kempten, Aschaffenburg, Speyer, Fulda, Lüneburg, Flensburg, Celle, Ulm, Gera, Remscheid, Bottrop, Witten, Böblingen, Friedrichshafen, Schweinfurt, Straubing, Coburg, Hameln, Nürtingen, Norderstedt, Leonberg, Ansbach, Moers, Heidenheim und Minden.", "<strong>Best School of the City:</strong> the top-ranked school in Berlin, Munich, Hamburg, Cologne, Frankfurt, Düsseldorf, Stuttgart, Leipzig, Dortmund, Essen, Bremen, Dresden, Hannover, Nuremberg, Duisburg, Bochum, Bielefeld, Bonn, Karlsruhe, Mannheim, Augsburg, Wiesbaden, Gelsenkirchen, Mönchengladbach, Braunschweig, Aachen, Chemnitz, Kiel, Freiburg, Krefeld, Mainz, Oberhausen, Kassel, Darmstadt, Hamm, Saarbrücken, Ludwigshafen, Potsdam, Oldenburg, Paderborn, Würzburg, Heilbronn, Göttingen, Reutlingen, Koblenz, Trier, Erlangen, Bremerhaven, Offenburg, Konstanz, Tübingen, Ludwigsburg, Bamberg, Landshut, Kempten, Aschaffenburg, Speyer, Fulda, Lüneburg, Flensburg, Celle, Ulm, Gera, Remscheid, Bottrop, Witten, Böblingen, Friedrichshafen, Schweinfurt, Straubing, Coburg, Hameln, Nürtingen, Norderstedt, Leonberg, Ansbach, Moers, Heidenheim and Minden.")}</li>
      <li>{r("span", "<strong>Aufsteiger des Jahres:</strong> die bestbewertete Schule, die in den letzten drei Jahren gegründet wurde.", "<strong>Rising School of the Year:</strong> the best-rated school founded in the last three years.")}</li>
      <li>{r("span", "<strong>Legacy Award:</strong> für eine Schule, die ihre lokale Bachata-Szene seit zehn Jahren oder länger prägt.", "<strong>Legacy Award:</strong> for a school that has shaped its local Bachata scene for ten years or more.")}</li>
      <li>{r("span", "<strong>Festival Stage Award:</strong> für die Schule, deren Lehrer am häufigsten auf europäischen Festivals und Kongressen unterrichten.", "<strong>Festival Stage Award:</strong> for the school whose teachers teach most often at European festivals and congresses.")}</li>
    </ul>
  </div>
</section>

<section class="block alt" aria-labelledby="use-title">
  <div class="wrap prose">
    {r("h2", "So nutzt du das Ranking bei der Schulwahl", "How to use the ranking to choose a school", 'id="use-title"')}
    {r("p", "Die Gesamtpunktzahl zeigt, welche Schulen insgesamt am stärksten sind. Für deine Wahl lohnt sich aber ein Blick in die <strong>Punkteaufschlüsselung</strong>: Tippe nach der Veröffentlichung auf eine Schule und sieh dir an, wo sie ihre Punkte holt.", "The total score shows which schools are strongest overall. For your own choice, look at the <strong>score breakdown</strong>: after publication, tap a school to see where its points come from.")}
    {r("p", "Du bist Anfänger? Dann achte vor allem auf <strong>Kurse und Einsteiger</strong> sowie auf eigene Socials. Du willst auf Festival-Niveau trainieren? Dann zählen Festivalauftritte und Gastlehrer mehr. Wähle zwei oder drei Schulen aus deiner Stadt, besuche jeweils eine Probestunde und entscheide nach Gefühl: Am Ende ist die beste Schule die, in der du gern wiederkommst.", "Are you a beginner? Then focus on <strong>classes and beginners</strong> and on the school's own socials. Want to train at festival level? Then festival appearances and guest teachers matter more. Pick two or three schools in your city, take a trial class at each and go with your gut: in the end, the best school is the one you love coming back to.")}
  </div>
</section>

<section class="block" aria-labelledby="good-title">
  <div class="wrap prose">
    {r("h2", "Woran du eine gute Bachata-Schule erkennst", "How to recognise a good Bachata school", 'id="good-title"')}
    {r("p", "Ein Platz im Ranking ist ein guter Startpunkt. Ob eine Schule zu dir passt, merkst du aber erst im Unterricht. Achte auf diese Punkte:", "A place in the ranking is a good starting point, but you only find out whether a school suits you in class. Look out for these points:")}
    <ul>
      <li>{r("span", "<strong>Probestunde oder feste Einsteigertermine:</strong> Du kannst ohne Risiko anfangen und mit einer neuen Gruppe starten.", "<strong>Trial class or fixed beginner start dates:</strong> you can start without risk and join a new group.")}</li>
      <li>{r("span", "<strong>Partnerwechsel im Kurs:</strong> Du lernst mit vielen Partnern zu tanzen und brauchst niemanden mitzubringen.", "<strong>Partner rotation in class:</strong> you learn to dance with many partners and don't need to bring anyone.")}</li>
      <li>{r("span", "<strong>Technik statt nur Figuren:</strong> Gute Lehrer erklären Führen, Folgen und Musikalität, nicht nur Schrittfolgen.", "<strong>Technique, not just moves:</strong> good teachers explain leading, following and musicality, not just step sequences.")}</li>
      <li>{r("span", "<strong>Klare Levels:</strong> Getrennte Kurse für Anfänger, Mittelstufe und Fortgeschrittene, damit niemand über- oder unterfordert ist.", "<strong>Clear levels:</strong> separate classes for beginners, intermediate and advanced dancers, so nobody is over- or under-challenged.")}</li>
      <li>{r("span", "<strong>Socials und Übungsabende:</strong> Auf Partys wendest du das Gelernte an. Schulen mit eigenen Socials bringen dich schneller voran.", "<strong>Socials and practice nights:</strong> parties are where you use what you learned. Schools with their own socials help you progress faster.")}</li>
      <li>{r("span", "<strong>Lehrer mit Festivalerfahrung:</strong> Wer auf Festivals unterrichtet, kennt aktuelle Stile und bringt Ideen aus der ganzen Szene mit.", "<strong>Teachers with festival experience:</strong> teachers who teach at festivals know current styles and bring ideas from the whole scene.")}</li>
    </ul>
  </div>
</section>

<section class="block alt" aria-labelledby="style-title">
  <div class="wrap prose">
    {r("h2", "Bachata-Stile: Dominicana, Sensual und Moderna", "Bachata styles: Dominican, Sensual and Moderna", 'id="style-title"')}
    {r("p", "Bachata kommt aus der Dominikanischen Republik und steht seit 2019 auf der <a href=\"https://de.wikipedia.org/wiki/Bachata\" rel=\"noopener\">UNESCO-Liste des immateriellen Kulturerbes</a>. In Deutschland unterrichten die meisten Schulen einen oder mehrere dieser Stile:", "Bachata comes from the Dominican Republic and has been on the <a href=\"https://en.wikipedia.org/wiki/Bachata_(music)\" rel=\"noopener\">UNESCO Intangible Cultural Heritage list</a> since 2019. Most schools in Germany teach one or more of these styles:")}
    {r("h3", "Bachata Dominicana", "Dominican Bachata")}
    {r("p", "Der ursprüngliche Stil: schnelle Fußarbeit, verspielte Rhythmen und eher offene Haltung. Ideal, wenn du Musikalität und Footwork liebst.", "The original style: fast footwork, playful rhythms and a more open hold. Ideal if you love musicality and footwork.")}
    {r("h3", "Bachata Sensual", "Bachata Sensual")}
    {r("p", "In Europa entstanden und dort sehr beliebt: enge Verbindung, Wellen, Körperbewegungen und fließende Drehungen. Auf vielen Festivals der Hauptstil.", "Developed in Europe and very popular there: close connection, body waves and flowing turns. The main style at many festivals.")}
    {r("h3", "Bachata Moderna", "Bachata Moderna")}
    {r("p", "Eine Mischung aus dem Grundschritt mit Drehfiguren und Elementen aus anderen Tänzen. Viele Einsteigerkurse beginnen hier, weil er leicht zugänglich ist.", "A mix of the basic step with turn patterns and elements from other dances. Many beginner classes start here because it is easy to get into.")}
  </div>
</section>

<section class="block alt" aria-labelledby="tips-title">
  <div class="wrap prose">
    {r("h2", "Tipps für deine erste Bachata-Stunde", "Tips for your first Bachata class", 'id="tips-title"')}
    <ul>
      <li>{r("span", "<strong>Bequeme Schuhe mit glatter Sohle:</strong> Turnschuhe mit viel Grip machen Drehungen schwer.", "<strong>Comfortable shoes with a smooth sole:</strong> trainers with lots of grip make turns hard.")}</li>
      <li>{r("span", "<strong>Mit einer neuen Gruppe starten:</strong> Frag nach dem nächsten Einsteigertermin, statt mitten in einen laufenden Kurs zu springen.", "<strong>Start with a new group:</strong> ask for the next beginner start date instead of jumping into a running course.")}</li>
      <li>{r("span", "<strong>Allein kommen ist normal:</strong> Durch den Partnerwechsel tanzt du ohnehin mit vielen Leuten.", "<strong>Coming alone is normal:</strong> with partner rotation you dance with many people anyway.")}</li>
      <li>{r("span", "<strong>Dranbleiben:</strong> Ein Kurs pro Woche über mehrere Monate bringt dich weiter als ein einzelner Intensiv-Workshop. Der Grundschritt sitzt meist nach wenigen Wochen.", "<strong>Stick with it:</strong> one class a week over several months gets you further than a single intensive workshop. The basic step usually feels natural after a few weeks.")}</li>
      <li>{r("span", "<strong>Bachata-Musik hören:</strong> Wer den Takt kennt, findet im Unterricht schneller den Einstieg. Achte auf die Zählweise 1-2-3-Tap, die sich durch jeden Bachata-Song zieht.", "<strong>Listen to Bachata music:</strong> knowing the beat helps you get going faster in class. Listen for the 1-2-3-tap count that runs through every Bachata song.")}</li>
      <li>{r("span", "<strong>Zum ersten Social gehen:</strong> Schon nach wenigen Stunden kannst du auf einer Party den Grundschritt üben.", "<strong>Go to your first social:</strong> after just a few classes you can practise the basic step at a party.")}</li>
    </ul>
  </div>
</section>

<section class="block" aria-labelledby="cities-title">
  <div class="wrap prose">
    {r("h2", "Die 79 Städte im Ranking", "The 79 cities in the ranking", 'id="cities-title"')}
    {r("p", "Für die erste Ausgabe haben wir 79 Städte in ganz Deutschland gewählt, von den größten bis zu mittleren Städten. Dort gibt es genug Schulen für einen fairen Vergleich, und viele Tänzer suchen hier gezielt nach einem Kurs. Weitere Städte kommen in den nächsten Ausgaben dazu.", "For the first edition we chose 79 cities across Germany, from the biggest to mid-sized ones. They have enough schools for a fair comparison, and many dancers there search specifically for a class. More cities join in future editions.")}
    {r("p", "Jede Stadt bekommt ein eigenes Top-10-Ranking. Die beste Schule jeder Stadt erhält den Award <strong>Beste Schule der Stadt</strong>, die höchste Punktzahl im ganzen Land den Award <strong>Beste Bachata-Schule Deutschlands</strong>.", "Every city gets its own top 10. The best school in each city receives the <strong>Best School of the City</strong> award, and the highest score in the country wins <strong>Best Bachata School in Germany</strong>.")}
    <div class="citylinks">{city_links}</div>
    {r("p", "Mehr zu den Schulen vor Ort: <a href=\"bachata-berlin.html\">Berlin</a>, <a href=\"bachata-hamburg.html\">Hamburg</a>, <a href=\"bachata-muenchen.html\">München</a>.", "More on the schools locally: <a href=\"bachata-berlin.html\">Berlin</a>, <a href=\"bachata-hamburg.html\">Hamburg</a>, <a href=\"bachata-muenchen.html\">Munich</a>.")}
  </div>
</section>

<section class="block alt" id="faq" aria-labelledby="rfaq-title">
  <div class="wrap">
    <div class="sec-head">{r("h2", "Häufige Fragen zum Bachata-Ranking", "Bachata ranking FAQ", 'id="rfaq-title"')}</div>
    <div class="faq">
{rfaq_html}
    </div>
  </div>
</section>
'''

R_TEXT = {
 'title_city': ['Beste Bachata-Schulen in {c}', 'Best Bachata schools in {c}'],
 'title_de': ['Beste Bachata-Schulen Deutschlands', 'Best Bachata schools in Germany'],
 'sub_interim': ['Zwischenstand: Die Platzierungen können sich bis zum 20. Dezember noch ändern.', 'Interim standing: places can still change until December 20.'],
 'help_h': ['Wie funktioniert das Ranking?', 'How does the ranking work?'],
 'help_p': ['Jede Schule wird nach denselben neun öffentlichen Kriterien bewertet (100 Punkte). Platzierungen sind nicht käuflich.', 'Every school is scored on the same nine public criteria (100 points). Places cannot be bought.'],
 'help_how': ['So wird bewertet', 'How scoring works'],
 'help_add': ['Meine Schule hinzufügen', 'Add my school'],
 'help_tips_h': ['So verbesserst du die Platzierung deiner Schule', 'How to improve your school\'s place'],
 'help_tips': [['Google-Eintrag pflegen und Schüler um eine Bewertung bitten (Google-Bewertung 25 P., Anzahl 10 P., aktuelle 5 P.)', 'Gründungsjahr, Lehrerteam und Kursstufen auf der Website nennen (Jahre 10 P.)', 'Probestunde und feste Einsteigertermine anbieten (Einsteigerangebot 10 P.)', 'Socials, Workshops und Gastlehrer veranstalten und online zeigen (Events 10 P.)', 'Instagram regelmäßig bespielen (Social Media 10 P.)', 'Festivalauftritte und Wettbewerbe per Link nachweisen (Festivals 15 P., Wettbewerbe 5 P.)'], ['Keep your Google listing up to date and ask students for a review (rating 25 pts, number 10, recent 5)', 'State founding year, teaching team and course levels on your website (years 10 pts)', 'Offer a trial class and fixed beginner start dates (beginner offer 10 pts)', 'Run socials, workshops and guest teachers and show them online (events 10 pts)', 'Post on Instagram regularly (social media 10 pts)', 'Prove festival appearances and competitions with links (festivals 15 pts, competitions 5 pts)']],
 'sub_locked': ['Die Top 10 werden am 20. Dezember 2026 enthüllt.', 'The top 10 will be revealed on December 20, 2026.'],
 'sub_open': ['Endergebnis der Bachata Awards 2026. Tippe auf eine Schule, um ihre Punkteaufschlüsselung zu sehen.', 'Final results of the Bachata Awards 2026. Tap a school to see its score breakdown.'],
 'locked': ['Wird am 20. Dezember enthüllt', 'Revealed on December 20'],
 'pts': ['Punkte', 'points'],
 'site': ['Website', 'Website'],
 'insta': ['Instagram', 'Instagram'],
 'note_h': ['Deine Schule fehlt noch?', 'Is your school missing?'],
 'note_p': ['Bewirb dich bis zum 30. November kostenlos für die Awards 2026.', 'Enter for the 2026 awards for free by November 30.'],
 'note_btn': ['Kostenlos bewerben', 'Apply for free'],
 'page_link': ['Schulseite, Bewertungen und Abstimmung', 'School page, reviews and voting'],
 'vote_h': ['Publikumspreis', 'Audience Award'],
 'vote_banner': ['Publikumspreis: Öffne eine Schule und stimme ab. Eine Stimme pro Person, bestätigt per E-Mail. Der Publikumspreis ist unabhängig von den 100 Punkten, das Ergebnis kommt am 20. Dezember.', 'Audience Award: open a school and vote. One vote per person, confirmed by email. It is separate from the 100 points, and the result comes on December 20.'],
 'vote_btn': ['Für diese Schule abstimmen', 'Vote for this school'],
 'vote_mail': ['Deine E-Mail-Adresse', 'Your email address'],
 'vote_send': ['Stimme abschicken', 'Send my vote'],
 'news_opt': ['Ja, schickt mir gelegentlich Neuigkeiten, Events und Angebote rund um Bachata per E-Mail. Abmeldung jederzeit möglich.', 'Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.'],
 'vote_note': ['Eine Stimme pro Person. Wir schicken dir einen Bestätigungslink. Deine E-Mail nutzen wir nur dafür und zum Entfernen doppelter Stimmen.', 'One vote per person. We email you a confirmation link. We use your email only for that and to remove duplicate votes.'],
 'vote_ok': ['Fast geschafft: Wir haben dir eine E-Mail geschickt. Klicke auf den Link darin, damit deine Stimme zählt. Schau auch im Spam-Ordner nach.', 'Almost done: we sent you an email. Click the link in it so your vote counts. Check your spam folder too.'],
 'vote_err': ['Das hat nicht geklappt. Bitte prüfe deine E-Mail-Adresse und versuche es noch einmal.', 'That did not work. Please check your email address and try again.'],
 'vote_done': ['Du hast auf diesem Gerät schon abgestimmt. Danke!', 'You already voted on this device. Thank you!'],
 'prelim_badge': ['Zwischenstand · kein Endergebnis, die Schulen sind noch im Wettbewerb', 'Interim standing · not final, schools are still competing'],
 'prelim_h': ['So entsteht der Zwischenstand', 'How the interim standing is calculated'],
 'prelim_p': ['Dieselbe 100-Punkte-Skala wie im Endergebnis. Bisher gewertet sind 6 von 9 Kriterien (zusammen höchstens 75 Punkte): Google-Bewertung und Anzahl der Bewertungen (Stand heute, aus Google Maps), Jahre im Unterricht, Einsteigerangebot, Events und Gastlehrer sowie Social Media (Follower und Beiträge auf Instagram). Festivalauftritte, aktuelle Bewertungen und Wettbewerbe sind als „zu bestätigen“ markiert und zählen vorerst 0. Alle Daten sind öffentlich. Weitere Schulen können sich bis 30. November bewerben, und Schulen können Angaben mit Links ergänzen. Die Platzierungen können sich noch ändern. Endergebnis am 20. Dezember 2026.', 'The same 100-point scale as the final result. So far 6 of 9 criteria are scored (75 points at most together): Google rating and number of reviews (as of today, from Google Maps), years teaching, beginner offer, events and guest teachers, and social media (Instagram followers and posts). Festival appearances, recent reviews and competitions are marked “to be confirmed” and score 0 for now. All data is public. More schools can apply until November 30, and schools can add information with links. Positions can still change. Final results on December 20, 2026.'],
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
    duesseldorf: [],
    stuttgart: [],
    leipzig: [],
    dortmund: [],
    essen: [],
    bremen: [],
    dresden: [],
    hannover: [],
    nuernberg: [],
    duisburg: [],
    bochum: [],
    bielefeld: [],
    bonn: [],
    karlsruhe: [],
    mannheim: [],
    augsburg: [],
    wiesbaden: [],
    gelsenkirchen: [],
    moenchengladbach: [],
    braunschweig: [],
    aachen: [],
    chemnitz: [],
    kiel: [],
    freiburg: [],
    krefeld: [],
    mainz: [],
    oberhausen: [],
    kassel: [],
    darmstadt: [],
    hamm: [],
    saarbruecken: [],
    ludwigshafen: [],
    potsdam: [],
    oldenburg: [],
    paderborn: [],
    wuerzburg: [],
    heilbronn: [],
    goettingen: [],
    reutlingen: [],
    koblenz: [],
    trier: [],
    erlangen: [],
    bremerhaven: [],
    offenburg: [],
    konstanz: [],
    tuebingen: [],
    ludwigsburg: [],
    bamberg: [],
    landshut: [],
    kempten: [],
    aschaffenburg: [],
    speyer: [],
    fulda: [],
    lueneburg: [],
    flensburg: [],
    celle: [],
    ulm: [],
    gera: [],
    remscheid: [],
    bottrop: [],
    witten: [],
    boeblingen: [],
    friedrichshafen: [],
    schweinfurt: [],
    straubing: [],
    coburg: [],
    hameln: [],
    nuertingen: [],
    norderstedt: [],
    leonberg: [],
    ansbach: [],
    moers: [],
    heidenheim: [],
    minden: []
  };
  /* PRELIMINARY LIST: schools verified on their own website. Alphabetical, no scores. Not a ranking. */
  var CANDIDATES = {
    berlin: [
      {name:"BachatAcademy", sc:[0, 10, 7, 19.9, 6.3, 8.6], fx:["5,0 ★ · 32","2.857 · 238"], url:"https://www.bachatacademy.de/"},
      {name:"La Mambita", sc:[10, 8, 7, 22.4, 10, 7.9], fx:["4,9 ★ · 252","1.642 · 138"], url:"https://www.mambita.de/"},
      {name:"Zapatissimo", st:["Sensual"], sc:[0, 8, 7, 20.9, 9.9, 7.8], fx:["4,8 ★ · 234","2.583 · 48"], url:"https://www.zapatissimo.de/"},
      {name:"Cumbancha Tanzschule", sc:[10, 10, 4, 23.9, 9.9, 9.7], fx:["5,0 ★ · 243","5.739 · 1.483"], url:"https://www.cumbancha.de/"},
      {name:"Tumba'o Danzas", sc:[0, 0, 3, 13.8, 1.3, 5.8], fx:["5,0 ★ · 1","186 · 54"], url:"https://tumbao-danzas.de/"},
      {name:"Bailaconsol", st:["Sensual"], sc:[0, 7, 4, 22.4, 8.1, 8.0], fx:["5,0 ★ · 87","2.660 · 106"], url:"http://www.bailaconsol.com/"},
      {name:"Dolce Vita Dance Studio", sc:[0, 8, 4, 22.0, 9.3, 0], fx:["4,9 ★ · 168","–"], url:"https://www.dolce-vita-dance.com/"},
      {name:"MiSalsa", sc:[0, 8, 3, 11.3, 6.1, 0], fx:["4,1 ★ · 28","–"], url:"https://misalsa.de/"},
      {name:"Tanzschule Traumtänzer", sc:[10, 10, 10, 16.1, 9.7, 8.9], fx:["4,5 ★ · 212","1.470 · 864"], url:"https://www.traumtaenzer.de/"},
      {name:"MAXIXE Tanzschule", sc:[10, 8, 7, 21.2, 8.3, 0], fx:["4,9 ★ · 97","–"], url:"https://www.maxixe.de/"},
      {name:"TanzSuite", sc:[10, 10, 10, 20.9, 8.0, 6.6], fx:["4,9 ★ · 82","393 · 82"], url:"https://www.tanzsuite.de/"},
      {name:"Elite Dance Studio", sc:[10, 8, 8, 20.7, 7.7, 0], fx:["4,9 ★ · 71","–"], url:"https://www.elitedancestudio.de/"},
      {name:"Artdance Tanzstudio", st:["Moderna"], sc:[0, 5, 0, 19.6, 8.0, 0], fx:["4,8 ★ · 81","–"], url:"https://www.artdance-tanzstudio.de/"}
    ],
    muenchen: [
      {name:"Salsea Dance Academy", sc:[0, 10, 10, 21.2, 8.2, 8.8], fx:["4,9 ★ · 94","4.395 · 175"], url:"https://salsea.de/"},
      {name:"Dance With George", sc:[0, 7, 8, 20.8, 9.7, 9.0], fx:["4,8 ★ · 211","2.706 · 656"], url:"https://www.dancewithgeorge.com/"},
      {name:"Salsa Y Corazon", sc:[10, 7, 8, 21.4, 8.4, 8.3], fx:["4,9 ★ · 103","2.000 · 254"], url:"https://www.salsa-y-corazon.de/"},
      {name:"Salsa Club Munich", sc:[5, 7, 5, 19.9, 8.2, 9.6], fx:["4,8 ★ · 90","8.876 · 427"], url:"http://www.salsaclub-munich.de/"},
      {name:"Lazarte Dance Academy", sc:[0, 10, 6, 21.5, 7.3, 6.0], fx:["5,0 ★ · 58","404 · 31"], url:"https://www.lazartedanceacademy.de/"},
      {name:"Salsamás Munich", sc:[10, 8, 6, 21.0, 7.0, 0], fx:["5,0 ★ · 48","–"], url:"https://www.salsamas.de/"},
      {name:"Salsa OnStage", st:["Dominicana"], sc:[0, 7, 9, 22.5, 8.2, 9.8], fx:["5,0 ★ · 93","7.070 · 606"], url:"http://www.salsa-onstage.de/"},
      {name:"Mike Dance", sc:[0, 6, 9, 20.2, 6.7, 7.9], fx:["4,9 ★ · 40","763 · 211"], url:"https://mike-dance.de/"},
      {name:"Salsa Tanzen Munich", st:["Sensual"], sc:[0, 10, 5, 18.5, 6.0, 6.9], fx:["4,9 ★ · 27","761 · 61"], url:"https://salsatanzenmunich.com/"},
      {name:"Casa Ritmo Dance Academy", st:["Sensual"], sc:[0, 8, 8, 17.5, 4.9, 5.8], fx:["5,0 ★ · 14","436 · 20"], url:"https://casaritmo.de/"},
      {name:"Dance Munich", sc:[0, 8, 3, 0, 0, 0], fx:["–","–"], url:"https://dancemunich.de/"},
      {name:"KULT Tanzschule", sc:[0, 10, 7, 18.8, 8.9, 9.8], fx:["4,7 ★ · 139","5.176 · 906"], url:"https://www.kult-tanzschule.de/"},
      {name:"Tanzhaus Emotion", st:["Sensual"], sc:[10, 8, 6, 21.9, 9.2, 7.5], fx:["4,9 ★ · 158","959 · 128"], url:"https://www.tanzhausemotion.de/"}
    ],
    hamburg: [
      {name:"A Bailar Hamburg", st:["Dominicana"], sc:[0, 10, 9, 18.4, 7.9, 9.3], fx:["4,7 ★ · 77","4.363 · 532"], url:"https://www.abailar-hamburg.de/"},
      {name:"SalsaHH", sc:[10, 7, 7, 16.1, 6.2, 0], fx:["4,6 ★ · 30","–"], url:"http://www.salsahh.de/"},
      {name:"ICB Studios", st:["Sensual"], sc:[0, 7, 7, 20.0, 6.4, 8.2], fx:["5,0 ★ · 33","2.579 · 116"], url:"https://icbstudios.com/"},
      {name:"Bachata Hamburg", st:["Sensual"], sc:[0, 10, 6, 19.7, 6.2, 8.7], fx:["5,0 ★ · 30","2.566 · 259"], url:"https://www.bachata-hamburg.de/"},
      {name:"BachataSalsaHamburg", sc:[0, 10, 0, 19.6, 6.1, 9.6], fx:["5,0 ★ · 29","11.000 · 316"], url:"https://www.bachatasalsahamburg.de/"},
      {name:"BellasArtes Latin DanceSchool", sc:[0, 8, 3, 21.6, 7.7, 5.0], fx:["4,9 ★ · 72","344 · 9"], url:"https://salsahamburg.info/"},
      {name:"Mi Pasión Dance School", sc:[0, 3, 9, 22.2, 7.9, 9.6], fx:["5,0 ★ · 80","4.592 · 1.209"], url:"http://mipasiondanceschool.com/"},
      {name:"AH-DanceCompany", st:["Sensual"], sc:[0, 10, 3, 20.1, 6.5, 8.2], fx:["5,0 ★ · 35","1.435 · 272"], url:"https://ahdancecompany.de/"},
      {name:"Hamburg Dance Academy", sc:[10, 10, 9, 22.4, 10, 7.6], fx:["4,9 ★ · 254","609 · 257"], url:"https://hamburg-dance-academy.de/"},
      {name:"Tanzschule die2", sc:[10, 8, 6, 21.6, 8.8, 7.3], fx:["4,9 ★ · 128","1.054 · 82"], url:"https://tanzschuledie2.de/"}
    ],
    koeln: [
      {name:"La Danza Tanzzentrum", st:["Sensual","Dominicana"], sc:[0, 5, 5, 15.1, 8.1, 9.9], fx:["4,4 ★ · 87","7.376 · 980"], url:"https://la-danza.de/"},
      {name:"Bachata Mastery Köln", st:["Sensual"], sc:[0, 10, 9, 24.2, 10, 9.3], fx:["5,0 ★ · 327","5.100 · 493"], url:"https://www.bachatakoeln.de/bachata-kurse-koeln"},
      {name:"Tanzen Lernen In Köln", sc:[0, 7, 7, 21.1, 7.3, 6.1], fx:["4,9 ★ · 57","302 · 40"], url:"https://salsaundbachatalerneninkoeln.de/"},
      {name:"LatinSalsa", sc:[0, 10, 6, 17.9, 6.2, 0], fx:["4,8 ★ · 30","–"], url:"https://latinsalsa.de/"},
      {name:"Salsa Köln", sc:[0, 5, 9, 21.1, 7.0, 7.8], fx:["5,0 ★ · 49","3.312 · 73"], url:"http://salsakoeln.de/"},
      {name:"Salsa in Köln", sc:[0, 8, 5, 21.3, 7.2, 8.8], fx:["5,0 ★ · 53","2.316 · 334"], url:"https://www.salsainkoeln.de/"},
      {name:"Tanzraum Köln", st:["Sensual","Dominicana"], sc:[0, 10, 4, 23.1, 9.4, 10], fx:["4,9 ★ · 180","13.000 · 1.001"], url:"https://tanzschule-tanzraum.de/"},
      {name:"Bailando Köln", st:["Dominicana","Sensual","Moderna"], sc:[0, 8, 8, 23.5, 9.3, 7.4], fx:["5,0 ★ · 172","1.715 · 63"], url:"https://bailando-koeln.de/"},
      {name:"Baila Colonia", st:["Dominicana","Moderna"], sc:[0, 8, 8, 23.7, 9.5, 6.1], fx:["5,0 ★ · 198","205 · 52"], url:"https://baila-tanzen-lernen.de/"},
      {name:"DanSazón Tanzschule", st:["Sensual","Dominicana"], sc:[0, 3, 4, 21.4, 7.6, 7.0], fx:["4,9 ★ · 66","811 · 66"], url:"http://www.dansazon.de/"}
    ],
    frankfurt: [
      {name:"FluxDance", sc:[1, 8, 9, 0, 0.0, 6.5], fx:["–","612 · 32"], url:"https://www.fluxdance.de/"},
      {name:"LaCalidad Dance Center", sc:[0, 10, 5, 22.2, 9.6, 9.8], fx:["4,9 ★ · 205","5.958 · 1.017"], url:"https://www.lacalidad.de/"},
      {name:"Movida Dance Academy", st:["Dominicana"], sc:[0, 8, 8, 23.9, 10, 0], fx:["4,9 ★ · 478","–"], url:"https://www.bachata-frankfurt.de/"},
      {name:"Alma Dance Frankfurt", st:["Sensual","Dominicana"], sc:[10, 10, 10, 23.4, 9.1, 9.5], fx:["5,0 ★ · 155","4.123 · 490"], url:"https://alma-dance-frankfurt.de/"},
      {name:"Salsa Auténtica", sc:[7, 5, 5, 22.1, 8.1, 8.0], fx:["4,9 ★ · 90","1.726 · 142"], url:"http://www.salsa-autentica.de/"},
      {name:"Tanzschule Conexión", sc:[0, 5, 9, 21.4, 9.4, 0], fx:["4,5 ★ · 188","–"], url:"http://www.conexion.de/"},
      {name:"Momento Cubano", sc:[10, 10, 2, 19.8, 6.2, 0], fx:["5,0 ★ · 31","–"], url:"https://momentocubano.com/"},
      {name:"DNA Dance Studios", sc:[0, 10, 4, 22.4, 8.1, 9.1], fx:["5,0 ★ · 87","3.379 · 346"], url:"https://www.dna-dance.com/"},
      {name:"Tanzschule Monika Bauer", sc:[8, 7, 8, 17.3, 8.8, 8.4], fx:["4,6 ★ · 126","1.694 · 307"], url:"https://www.monika-bauer.de/"},
      {name:"Tanzstudio Andres", sc:[0, 5, 0, 19.0, 5.8, 0], fx:["5,0 ★ · 24","–"], url:"https://tanzmitandres.de/"}
    ],
    duesseldorf: [
      {name:"La Cati Dance", sc:[0, 5, 5, 23.5, 9.3, 8.9], fx:["5,0 ★ · 165","1.843 · 1.073"], url:"https://www.lacatidance.de/"},
      {name:"Anima Dance Community", sc:[0, 10, 5, 18.4, 6.6, 7.7], fx:["4,8 ★ · 38","2.420 · 38"], url:"https://anima-dance.de/"},
      {name:"Salsa 'n' Fun", sc:[0, 10, 8, 19.8, 8.0, 8.2], fx:["4,8 ★ · 84","1.935 · 195"], url:"http://www.salsanfun.de/"},
      {name:"Salsa-Teaching", sc:[0, 7, 3, 19.9, 6.5, 6.8], fx:["4,9 ★ · 35","1.192 · 42"], url:"http://www.salsa-teaching.de/"},
      {name:"Salsa Cubana Düsseldorf", sc:[0, 8, 6, 17.0, 5.0, 7.4], fx:["4,9 ★ · 15","1.368 · 70"], url:"https://www.salsa-cubana-duesseldorf.de/"},
      {name:"Salsa Flow", sc:[0, 8, 8, 17.7, 5.0, 7.7], fx:["5,0 ★ · 15","567 · 338"], url:"https://salsa-flow.de/"}
    ],
    stuttgart: [
      {name:"Salsa Company Stuttgart", sc:[10, 7, 10, 17.5, 9.2, 10], fx:["4,6 ★ · 160","23.000 · 545"], url:"https://www.salsa-company.de/"},
      {name:"Tanzfitness Stuttgart", sc:[0, 8, 0, 20.3, 7.4, 6.8], fx:["4,9 ★ · 58","595 · 68"], url:"https://www.tanzfitness-stuttgart.de/"},
      {name:"Esencia Latina Dance Company", sc:[0, 8, 0, 18.9, 5.8, 0], fx:["5,0 ★ · 23","–"], url:"https://esencialatinadancecompany.com/"},
      {name:"Tanzschule Clavisol", sc:[0, 7, 6, 19.0, 5.8, 0], fx:["5,0 ★ · 24","–"], url:"https://clavisol.com/"},
      {name:"Alma Latina", st:["Sensual", "Dominicana"], sc:[0, 10, 5, 21.5, 7.4, 0], fx:["5,0 ★ · 59","–"], url:"https://www.almalatina.de/"},
      {name:"el pasito", sc:[10, 7, 8, 17.7, 5.0, 0], fx:["5,0 ★ · 15","–"], url:"https://www.elpasito.de/"},
      {name:"víaDanza Salsa-Tanzschule", sc:[10, 0, 5, 17.4, 6.8, 8.6], fx:["4,7 ★ · 42","2.104 · 314"], url:"https://www.viadanza-tanzschule.de/"}
    ],
    leipzig: [
      {name:"Fuego Latino Leipzig", st:["Sensual"], sc:[10, 5, 0, 18.8, 6.3, 8.3], fx:["4,9 ★ · 31","860 · 598"], url:"https://www.fuego-latino.de/"},
      {name:"Känguru Salsa", sc:[0, 5, 0, 18.9, 5.8, 7.9], fx:["5,0 ★ · 23","722 · 343"], url:"https://www.kangurusalsa.com/"}
    ],
    dortmund: [
      {name:"Tanzen in Dortmund", sc:[0, 5, 8, 18.3, 6.7, 8.9], fx:["4,8 ★ · 39","2.135 · 507"], url:"https://tanzen-dortmund.de/"},
      {name:"La Klave", sc:[0, 7, 6, 20.8, 7.8, 9.3], fx:["4,9 ★ · 74","3.195 · 687"], url:"https://www.laklave.de/"}
    ],
    essen: [
      {name:"Salsational Dance Academy", st:["Sensual", "Dominicana"], sc:[8, 9, 5, 20.8, 7.8, 0], fx:["4,9 ★ · 74","–"], url:"https://www.kizomba-essen.de/"},
      {name:"Tanz Galerie Essen", sc:[0, 10, 5, 20.4, 7.5, 7.6], fx:["4,9 ★ · 62","1.237 · 117"], url:"https://tanzgalerie-essen.de/"},
      {name:"Pedro's Cuba Lounge", sc:[8, 3, 8, 13.1, 7.6, 0], fx:["4,3 ★ · 67","–"], url:"https://pedros-cuba-lounge.de/"}
    ],
    bremen: [
      {name:"Bachata LAB Bremen", sc:[0, 0, 0, 18.6, 5.6, 0], fx:["5,0 ★ · 21","–"], url:"https://bachatalab.de/"},
      {name:"Casa Cultural Bremen", sc:[0, 10, 5, 16.0, 9.3, 9.6], fx:["4,5 ★ · 173","2.893 · 1.111"], url:"https://www.casa-cultural.de/"},
      {name:"Tanz-Fluss Tanzstudio", st:["Sensual", "Moderna"], sc:[0, 10, 3, 17.9, 7.4, 7.9], fx:["4,7 ★ · 58","1.261 · 193"], url:"https://www.tanz-fluss.de/"},
      {name:"Tanzarena Bremen", sc:[0, 10, 7, 15.7, 8.0, 9.6], fx:["4,5 ★ · 80","3.779 · 913"], url:"https://www.tanzarena.de/"}
    ],
    dresden: [
      {name:"Kubáname", sc:[0, 8, 7, 20.4, 7.5, 10], fx:["4,9 ★ · 63","11.000 · 955"], url:"https://kubana.me/"},
      {name:"BachaDDa", st:["Sensual", "Moderna"], sc:[7, 8, 3, 16.1, 4.8, 7.6], fx:["4,8 ★ · 13","1.217 · 129"], url:"https://www.bachadda.de/"},
      {name:"Bailamor Dresden", st:["Sensual"], sc:[0, 8, 6, 13.1, 7.2, 9.4], fx:["4,3 ★ · 52","3.942 · 611"], url:"https://www.bailamor.de/"},
      {name:"Elementio Tanzstudio", sc:[0, 10, 7, 17.1, 4.6, 7.4], fx:["5,0 ★ · 12","784 · 149"], url:"https://www.elementio.de/"}
    ],
    hannover: [
      {name:"Salsa del Alma", st:["Sensual"], sc:[0, 10, 6, 22.0, 9.3, 10], fx:["4,9 ★ · 171","7.730 · 1.015"], url:"https://www.salsa-del-alma.de/"},
      {name:"You Dance Latin Art Studio", sc:[7, 8, 9, 16.7, 7.4, 0], fx:["4,6 ★ · 59","–"], url:"https://www.u-dance.de/"}
    ],
    nuernberg: [
      {name:"Latin Groove Tanzschule", sc:[3, 8, 5, 22.5, 10, 0], fx:["4,9 ★ · 282","–"], url:"https://www.latin-groove.de/"},
      {name:"Tanzschule WILFEGO", st:["Sensual"], sc:[0, 8, 7, 21.5, 8.6, 0], fx:["4,9 ★ · 118","–"], url:"https://www.wilfego.de/"},
      {name:"CubaDanza Tanzschule", sc:[0, 8, 6, 21.0, 7.0, 7.5], fx:["5,0 ★ · 48","553 · 264"], url:"https://www.cubadanza.de/"},
      {name:"Dance Cube Nürnberg", sc:[0, 10, 6, 19.0, 7.3, 8.7], fx:["4,8 ★ · 57","2.509 · 300"], url:"https://dance-cube-nuernberg.de/"}
    ],
    duisburg: [
      {name:"Salsa con Corazón Duisburg", st:["Sensual", "Moderna"], sc:[0, 8, 0, 22.7, 8.4, 0], fx:["5,0 ★ · 103","–"], url:"https://www.salsacon-corazon.de/"}
    ],
    bochum: [
      {name:"Salsa Flavors", sc:[0, 8, 3, 17.9, 5.1, 6.0], fx:["5,0 ★ · 16","662 · 17"], url:"https://salsaflavors.de/"},
      {name:"Karina's World Dance Training", sc:[10, 7, 4, 19.9, 6.3, 0], fx:["5,0 ★ · 32","–"], url:"https://karinasworlddancetraining.com/"}
    ],
    bielefeld: [
      {name:"Tanzstudio Schrittweise", st:["Sensual"], sc:[0, 8, 6, 17.2, 5.1, 0], fx:["4,9 ★ · 16","–"], url:"https://www.tanzstudio-schrittweise.de/"}
    ],
    bonn: [
      {name:"Tanzschule Max7", sc:[0, 7, 7, 21.9, 9.2, 8.5], fx:["4,9 ★ · 156","3.215 · 183"], url:"https://www.max7.de/"},
      {name:"bonn tanzt", sc:[10, 10, 6, 20.1, 8.7, 9.6], fx:["4,8 ★ · 120","4.100 · 777"], url:"https://www.bonntanzt.de/"},
      {name:"YOUnited Dance", sc:[0, 8, 6, 21.2, 7.2, 7.1], fx:["5,0 ★ · 51","955 · 69"], url:"https://www.younited.dance/"}
    ],
    karlsruhe: [
      {name:"Havanna Star", sc:[0, 10, 8, 19.8, 8.3, 9.2], fx:["4,8 ★ · 95","3.727 · 498"], url:"https://www.havannastar.de/"},
      {name:"Caricia Tanzschule", sc:[10, 0, 6, 15.0, 4.9, 6.2], fx:["4,6 ★ · 14","273 · 63"], url:"https://www.caricia.de/"},
      {name:"Tanzstudio Palladium", sc:[0, 8, 8, 17.9, 6.3, 8.1], fx:["4,8 ★ · 32","859 · 394"], url:"https://www.palladium-karlsruhe.de/"}
    ],
    mannheim: [
      {name:"Chantal Miller Academy", sc:[0, 10, 5, 19.6, 7.9, 8.3], fx:["4,8 ★ · 79","1.983 · 221"], url:"https://www.chantal-miller.academy/"}
    ],
    augsburg: [
      {name:"Cuban Salsa Power", st:["Sensual"], sc:[0, 8, 8, 19.7, 8.1, 0], fx:["4,8 ★ · 85","–"], url:"https://www.emilito.de/"}
    ],
    wiesbaden: [
      {name:"Tanzschule Hohmann", sc:[10, 3, 7, 14.4, 8.0, 7.8], fx:["4,4 ★ · 81","851 · 257"], url:"https://www.tanzschule-hohmann.com/"}
    ],
    gelsenkirchen: [
      {name:"Isabel Kulessa Bachata", sc:[0, 0, 0, 17.5, 4.9, 9.8], fx:["5,0 ★ · 14","2.955 · 1.628"], url:"https://isabel-kulessa.de/"},
      {name:"Tanz bei Schwarz", sc:[8, 10, 3, 23.9, 10.0, 9.8], fx:["5,0 ★ · 245","9.119 · 438"], url:"https://www.tanz-bei-schwarz.de/"},
      {name:"Tanzpott", sc:[0, 10, 3, 15.7, 5.9, 0], fx:["4,6 ★ · 25","–"], url:"https://tanzpott.de/"}
    ],
    moenchengladbach: [
      {name:"La Mirella", sc:[0, 7, 9, 22.2, 9.6, 8.7], fx:["4,9 ★ · 201","1.470 · 602"], url:"https://www.la-mirella.de/"}
    ],
    braunschweig: [
      {name:"BAYRA Dance Academy", sc:[7, 10, 8, 17.8, 6.2, 6.0], fx:["4,8 ★ · 30","464 · 27"], url:"https://bayra.dance/"},
      {name:"Bailando Braunschweig", sc:[0, 10, 3, 23.4, 9.2, 8.9], fx:["5,0 ★ · 158","3.619 · 285"], url:"https://www.bailando-bs.de/"}
    ],
    aachen: [
      {name:"Dance Fusion Aachen", sc:[0, 10, 3, 21.7, 8.9, 10], fx:["4,9 ★ · 132","7.890 · 1.343"], url:"https://www.dancefusionaachen.de/"}
    ],
    chemnitz: [
      {name:"Tanzstudio Chemnitz", sc:[0, 5, 5, 20.1, 6.5, 0], fx:["5,0 ★ · 35","–"], url:"https://www.tanzstudio-chemnitz.de/"}
    ],
    kiel: [
      {name:"Salsa am Meer", st:["Moderna"], sc:[6, 7, 6, 15.2, 5.1, 8.2], fx:["4,6 ★ · 16","931 · 419"], url:"https://www.salsa-am-meer.de/"},
      {name:"Tanzschule Hand zu Hand", sc:[0, 8, 0, 20.4, 6.6, 0], fx:["5,0 ★ · 38","–"], url:"https://handzuhand-kiel.de/"}
    ],
    freiburg: [
      {name:"Salsa con Pasión", st:["Sensual", "Dominicana", "Moderna"], sc:[8, 10, 6, 21.7, 8.9, 8.9], fx:["4,9 ★ · 135","2.542 · 408"], url:"https://www.salsa-con-pasion.de/"},
      {name:"AYA Latin Dance Academy", sc:[8, 10, 6, 22.6, 8.3, 9.4], fx:["5,0 ★ · 96","6.570 · 361"], url:"https://aya-dance.de/"},
      {name:"Saltango", sc:[0, 7, 3, 19.7, 6.2, 0], fx:["5,0 ★ · 30","–"], url:"https://www.kizomba-freiburg.com/"},
      {name:"Timbalaye", sc:[0, 5, 8, 18.2, 6.6, 0], fx:["4,8 ★ · 37","–"], url:"https://salsa-freiburg.de/"},
      {name:"Gregorio Dance School", sc:[0, 8, 3, 19.8, 6.3, 7.8], fx:["5,0 ★ · 31","1.184 · 167"], url:"https://gregoriodance.com/"}
    ],
    krefeld: [
      {name:"LaTinas Dancestudio", sc:[1, 10, 3, 22.9, 8.5, 7.6], fx:["5,0 ★ · 111","714 · 206"], url:"https://www.latinas-dancestudio.de/"}
    ],
    mainz: [
      {name:"Salsa Deli", st:["Sensual"], sc:[0, 8, 3, 21.8, 9.0, 0], fx:["4,9 ★ · 142","–"], url:"https://salsa-deli.com/"}
    ],
    oberhausen: [
      {name:"Tanz-Bianca", sc:[3, 3, 7, 22.4, 8.1, 7.0], fx:["5,0 ★ · 89","627 · 90"], url:"https://www.tanz-bianca.de/"}
    ],
    kassel: [
      {name:"Baila Tanzschule Kassel", sc:[0, 10, 7, 17.2, 5.7, 8.1], fx:["4,8 ★ · 22","1.620 · 193"], url:"https://www.salsa-tanzschule-kassel.de/"},
      {name:"Latin Dance Community Kassel", st:["Sensual"], sc:[6, 8, 0, 21.6, 7.5, 7.8], fx:["5,0 ★ · 62","2.755 · 67"], url:"https://salsa-ks.de/"}
    ],
    darmstadt: [
      {name:"Salon Latino", sc:[0, 0, 5, 18.9, 9.1, 0], fx:["4,7 ★ · 151","–"], url:"https://www.salon-latino.de/"},
      {name:"BachaDa", sc:[0, 0, 0, 17.5, 4.9, 0], fx:["5,0 ★ · 14","–"], url:"https://www.bachada.de/"}
    ],
    hamm: [
      {name:"Annelieses Tanzschule", sc:[0, 8, 5, 17.3, 5.8, 0], fx:["4,8 ★ · 24","–"], url:"https://annelieses-tanzschule.de/"}
    ],
    saarbruecken: [
      {name:"Cubaila", sc:[8, 7, 10, 22.9, 8.6, 9.3], fx:["5,0 ★ · 116","3.623 · 551"], url:"https://www.cubaila.de/"},
      {name:"Bachatasaar", st:["Sensual"], sc:[0, 10, 9, 22.9, 8.6, 8.3], fx:["5,0 ★ · 116","1.512 · 284"], url:"https://bachatasaar.de/"},
      {name:"Salsa con Corazón Saarbrücken", sc:[0, 7, 3, 17.9, 5.1, 0], fx:["5,0 ★ · 16","–"], url:"https://salsa-con-corazon-sb.com/"},
      {name:"Belinda Brandl Tanzschule", sc:[10, 8, 5, 17.3, 5.8, 6.9], fx:["4,8 ★ · 23","425 · 123"], url:"https://www.salsa-dancing.de/"}
    ],
    ludwigshafen: [
      {name:"Habaneando", sc:[0, 8, 6, 21.3, 8.3, 9.3], fx:["4,9 ★ · 99","4.848 · 419"], url:"https://habaneando.com/"}
    ],
    potsdam: [
      {name:"Bachata Academy Potsdam", sc:[0, 10, 6, 20.9, 7.0, 0], fx:["5,0 ★ · 46","–"], url:"https://bachatacademy-potsdam.de/"}
    ],
    oldenburg: [
      {name:"Salsa y Sabor", st:["Sensual"], sc:[0, 8, 7, 20.8, 6.9, 0], fx:["5,0 ★ · 44","–"], url:"https://www.salsaysabor.de/"},
      {name:"Bachataraum", st:["Sensual"], sc:[0, 7, 8, 23.2, 9.0, 7.7], fx:["5,0 ★ · 141","1.798 · 95"], url:"https://www.bachataraum.de/"},
      {name:"Bailando Oldenburg", sc:[7, 10, 5, 22.9, 8.6, 8.6], fx:["5,0 ★ · 112","1.756 · 420"], url:"https://www.bailando-oldenburg.de/"}
    ],
    paderborn: [
      {name:"Spax Danceacademy", st:["Sensual"], sc:[0, 5, 6, 16.1, 4.8, 0], fx:["4,8 ★ · 13","–"], url:"https://www.spax-danceacademy.de/"}
    ],
    wuerzburg: [
      {name:"Bailamos Würzburg", sc:[0, 8, 9, 19.1, 6.5, 0], fx:["4,9 ★ · 35","–"], url:"https://www.bailamos-wuerzburg.de/"},
      {name:"DanceEncore", st:["Sensual", "Moderna"], sc:[8, 10, 6, 21.3, 8.4, 10], fx:["4,9 ★ · 103","9.861 · 1.079"], url:"https://danceencore.de/"}
    ],
    heilbronn: [
      {name:"Salsa Company Heilbronn", st:["Sensual"], sc:[10, 7, 5, 16.7, 7.4, 7.5], fx:["4,6 ★ · 59","1.366 · 97"], url:"https://salsa-tanzschule-heilbronn.de/"}
    ],
    goettingen: [
      {name:"Bachatisimo", st:["Dominicana"], sc:[0, 8, 3, 16.6, 4.3, 0], fx:["5,0 ★ · 10","–"], url:"https://www.bachatisimo.com/"},
      {name:"Baila Salsa Göttingen", sc:[0, 8, 5, 0, 0, 0], fx:["–","–"], url:"https://www.tanzboot.de/"}
    ],
    reutlingen: [
      {name:"Luna Latina Tanzpalast", sc:[0, 7, 6, 17.1, 6.4, 0], fx:["4,7 ★ · 34","–"], url:"https://www.el-padre-de-la-salsa.de/"}
    ],
    koblenz: [
      {name:"Tanzstudio CHANGA!", st:["Dominicana"], sc:[7, 10, 9, 16.4, 6.9, 9.7], fx:["4,6 ★ · 45","11.000 · 289"], url:"https://www.changa.de/"}
    ],
    trier: [
      {name:"Salsa y Sol Trier", st:["Sensual"], sc:[0, 8, 5, 16.6, 4.3, 0], fx:["5,0 ★ · 10","–"], url:"https://www.salsaysol.de/"},
      {name:"Tanzschule DANCE in Trier", sc:[0, 10, 6, 21.0, 7.0, 0], fx:["5,0 ★ · 48","–"], url:"https://www.dance-in-trier.de/"}
    ],
    erlangen: [
      {name:"Salsa Tanzstudio Erlangen", st:["Sensual", "Moderna"], sc:[0, 8, 7, 18.6, 6.1, 0], fx:["4,9 ★ · 28","–"], url:"https://salsa-erlangen.dance/"},
      {name:"Gillet Rupprecht Die Tanzschule", sc:[0, 7, 8, 22.3, 9.8, 8.6], fx:["4,9 ★ · 224","2.172 · 334"], url:"https://www.rupprecht-gillet.de/"}
    ],
    bremerhaven: [
      {name:"Salsa Loca", sc:[8, 5, 6, 16.6, 4.3, 5.7], fx:["5,0 ★ · 10","267 · 30"], url:"https://www.salsa-loca-bremerhaven.de/"}
    ],
    offenburg: [
      {name:"LaNi-Dance", sc:[0, 8, 4, 18.4, 5.4, 5.4], fx:["5,0 ★ · 19","190 · 21"], url:"https://www.lani-dance.de/"}
    ],
    konstanz: [
      {name:"Tanzwerk Konstanz", sc:[10, 10, 4, 18.2, 7.9, 8.2], fx:["4,7 ★ · 76","15.000 · 20"], url:"https://www.tanzwerk.dance/"},
      {name:"flamemotions", sc:[0, 5, 4, 17.3, 4.8, 0.0], fx:["5,0 ★ · 13","–"], url:"https://www.flamemotions.com/"}
    ],
    tuebingen: [
      {name:"Tanzschule Salsamara", sc:[10, 10, 10, 18.1, 7.7, 0.0], fx:["4,7 ★ · 68","–"], url:"https://salsa-mara-tuebingen.de/"}
    ],
    ludwigsburg: [
      {name:"Salsa Company Ludwigsburg", sc:[10, 8, 10, 15.0, 6.3, 7.1], fx:["4,5 ★ · 32","968 · 62"], url:"https://salsa-company-ludwigsburg.de/"},
      {name:"MiSalsa Ludwigsburg", sc:[5, 10, 7, 20.9, 7.9, 8.8], fx:["4,9 ★ · 78","2.058 · 484"], url:"https://www.misalsa-lb.de/"}
    ],
    bamberg: [
      {name:"Salsa Samstag Bamberg", sc:[0, 5, 4, 16.6, 4.3, 0.0], fx:["5,0 ★ · 10","–"], url:"https://www.salsasamstag-bamberg.de/"}
    ],
    landshut: [
      {name:"Tanz-Länd", sc:[0, 5, 4, 17.9, 6.3, 0.0], fx:["4,8 ★ · 32","–"], url:"https://tanz-laend.de/"},
      {name:"Tanzschule Tanzparadies", sc:[0, 8, 4, 21.0, 7.1, 0.0], fx:["5,0 ★ · 49","–"], url:"https://tanzpa.de/"}
    ],
    kempten: [
      {name:"Tanzschule TANZLATION", sc:[0, 10, 4, 20.5, 7.6, 8.1], fx:["4,9 ★ · 64","3.266 · 102"], url:"https://www.tanzlation.de/"},
      {name:"J&J Dance Tanzschule", sc:[0, 10, 2, 17.0, 6.3, 8.9], fx:["4,7 ★ · 32","1.622 · 786"], url:"https://jj-dance.com/"},
      {name:"Tanzzentrum Allgäu", sc:[0, 5, 0, 17.6, 7.1, 0.0], fx:["4,7 ★ · 49","–"], url:"https://merengue.de/"}
    ],
    aschaffenburg: [
      {name:"Tanzstudio La Pasion", sc:[0, 10, 7, 21.3, 8.3, 0.0], fx:["4,9 ★ · 99","–"], url:"https://tanzstudio-lapasion.de/"}
    ],
    speyer: [
      {name:"Salsa Tanzschule Habaneando", sc:[0, 8, 7, 21.3, 8.3, 9.2], fx:["4,9 ★ · 99","4.848 · 419"], url:"https://habaneando.com/"}
    ],
    fulda: [
      {name:"Latin Dance Community Fulda", sc:[0, 10, 7, 20.1, 7.3, 6.9], fx:["4,9 ★ · 54","987 · 45"], url:"https://salsa-fd.de/"},
      {name:"Tanzschule MoTaBa", sc:[10, 10, 7, 20.8, 7.8, 6.4], fx:["4,9 ★ · 74","577 · 35"], url:"https://www.motaba.org/"}
    ],
    lueneburg: [
      {name:"ConFlow Latin Dance Studio", sc:[0, 8, 4, 17.9, 5.1, 0.0], fx:["5,0 ★ · 16","–"], url:"https://conflow-lueneburg.de/"}
    ],
    flensburg: [
      {name:"Demis Salsa Cubana", sc:[10, 5, 4, 19.0, 5.8, 8.2], fx:["5,0 ★ · 24","839 · 518"], url:"https://www.demis-salsa-cubana.de/"}
    ],
    celle: [
      {name:"TanzHaus Celle", sc:[10, 10, 4, 18.2, 6.6, 7.6], fx:["4,8 ★ · 37","1.468 · 104"], url:"https://www.tanzhaus-celle.de/"}
    ],
    ulm: [
      {name:"Ritmo Latino Tanzschule", sc:[10, 8, 10, 21.9, 9.1, 8.3], fx:["4,9 ★ · 154","1.590 · 291"], url:"https://www.ritmolatino.de/"}
    ],
    gera: [
      {name:"Salsa Picante Gera", sc:[0, 10, 7, 0.0, 0.0, 0.0], fx:["–","–"], url:"https://tanzeningera.de/"}
    ],
    remscheid: [
      {name:"Tanzraum Remscheid", sc:[5, 10, 4, 22.5, 8.2, 8.0], fx:["5,0 ★ · 90","1.470 · 200"], url:"https://www.tanzraum-rs.de/"}
    ],
    bottrop: [
      {name:"Cantina di Danza", sc:[0, 10, 0, 18.6, 5.6, 6.6], fx:["5,0 ★ · 21","504 · 55"], url:"https://cantinadidanza.de/"}
    ],
    witten: [
      {name:"Tanzschule mit Marc", sc:[0, 5, 4, 20.3, 7.4, 0.0], fx:["4,9 ★ · 60","–"], url:"https://tanzschulemitmarc.de/"}
    ],
    boeblingen: [
      {name:"Salsa Company Böblingen", sc:[10, 8, 10, 12.0, 7.0, 0.0], fx:["4,2 ★ · 46","–"], url:"https://www.tanzschule-boeblingen.de/"}
    ],
    friedrichshafen: [
      {name:"Love to Dance! Studio", sc:[0, 10, 10, 17.0, 5.5, 0.0], fx:["4,8 ★ · 20","–"], url:"https://www.love-to-dance.de/"}
    ],
    schweinfurt: [
      {name:"Tanzschule Pelzer", sc:[0, 8, 4, 17.2, 8.4, 0.0], fx:["4,6 ★ · 101","–"], url:"https://tanzen-bei-pelzer.de/"},
      {name:"Tanz an!", sc:[0, 5, 4, 18.1, 6.4, 0.0], fx:["4,8 ★ · 34","–"], url:"https://www.tanzan.de/"}
    ],
    straubing: [
      {name:"SALSA Straubing", sc:[0, 8, 7, 14.6, 2.5, 0.0], fx:["5,0 ★ · 3","–"], url:"https://salsa-straubing.de/"}
    ],
    coburg: [
      {name:"TANZTRAUM Tanzlounge", sc:[0, 5, 0, 16.9, 6.2, 0.0], fx:["4,7 ★ · 30","–"], url:"https://tanz-traum.de/"}
    ],
    hameln: [
      {name:"Tanzschule FÜR SIE", sc:[0, 5, 7, 19.9, 8.3, 0.0], fx:["4,8 ★ · 98","–"], url:"https://www.tsfuersie.de/"}
    ],
    nuertingen: [
      {name:"Excelencia 4 Ever Dance", sc:[0, 8, 0, 18.9, 5.8, 0.0], fx:["5,0 ★ · 23","–"], url:"https://tanzstudio-excelencia.de/"}
    ],
    norderstedt: [
      {name:"TanzCentrum Die 3", sc:[10, 5, 0, 15.2, 6.8, 0.0], fx:["4,5 ★ · 42","–"], url:"https://www.tanzen-in-norderstedt.de/"}
    ],
    leonberg: [
      {name:"Tanzschule Danceworld", sc:[0, 5, 7, 15.1, 6.5, 0.0], fx:["4,5 ★ · 36","–"], url:"https://www.tanzschule-danceworld.de/"}
    ],
    ansbach: [
      {name:"Tanzschule Springer", sc:[0, 5, 4, 20.4, 9.2, 0.0], fx:["4,8 ★ · 156","–"], url:"https://www.tanzschule-springer.de/"}
    ],
    moers: [
      {name:"Tanzschule Helfer", sc:[0, 5, 4, 19.6, 6.8, 0.0], fx:["4,9 ★ · 43","–"], url:"https://www.tshelfer.de/"}
    ],
    heidenheim: [
      {name:"Tanzhaus Heidenheim", sc:[0, 5, 4, 18.1, 6.4, 0.0], fx:["4,8 ★ · 34","–"], url:"https://tanzen-heidenheim.de/"}
    ],
    minden: [
      {name:"Tanzschule Am Ring", sc:[0, 5, 0, 12.0, 6.7, 0.0], fx:["4,2 ★ · 39","–"], url:"https://www.tanzschule-am-ring.de/"}
    ]
  };
  var VOTE_ENDPOINT = "https://script.google.com/macros/s/AKfycbzAANOuM7cA3QgqeXZXOKZEYumNFsENBZaIicJSaJluR90rTl2iw30Sk522vxIurDsg/exec";
  var PUBLISH_DATE = new Date("2026-12-20T19:00:00+01:00");

  var TX = ''' + json.dumps(R_TEXT, ensure_ascii=False) + r''';
  function L(k){ return TX[k][window.LANG==="en"?1:0]; }
  function esc(s){ return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];}); }
  function slug(n){ return n.toLowerCase().replace(/ä/g,"ae").replace(/ö/g,"oe").replace(/ü/g,"ue").replace(/ß/g,"ss").normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,""); }
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
  function hasCand(c){ var r=false; Object.keys(CANDIDATES).forEach(function(k){ if((c==="deutschland"||c===k)&&CANDIDATES[k].length) r=true; }); return r; }
  function render(){
    var c=current, cityName=TX.cities[c][window.LANG==="en"?1:0];
    var title = c==="deutschland" ? L("title_de") : L("title_city").replace("{c}",cityName);
    var list=listFor(c), open=isOpen()&&list.length>0;
    var h=(preview?'<span class="preview-note">'+esc(L("preview"))+'</span>':'')
      +'<h2 class="panel-title">'+esc(title)+'</h2><p class="panel-sub">'+esc(open?L("sub_open"):(hasCand(c)?L("sub_interim"):L("sub_locked")))+'</p>';
    var hasPl=false;
    if(!open){ Object.keys(CANDIDATES).forEach(function(k){ if((c==="deutschland"||c===k)&&CANDIDATES[k].length) hasPl=true; }); }
    var locked=!open;
    if(!(locked&&hasPl)){
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
    }
    if(!open){
      var pl=[];
      Object.keys(CANDIDATES).forEach(function(k){ if(c==="deutschland"||c===k) CANDIDATES[k].forEach(function(e){ pl.push(Object.assign({city:k},e)); }); });
      pl.forEach(function(e){ e.pts=Math.round(e.sc.reduce(function(x,y){return x+y;},0)*10)/10; });
      pl.sort(function(a,b){ return (b.pts-a.pts)||a.name.localeCompare(b.name); });
      if(pl.length){
        var en=window.LANG==="en", cn=function(e){return esc(TX.cities[e.city][en?1:0]);};
        var FAC=en?["Years teaching","Beginner offer","Events and guests","Google rating","Number of reviews","Social media"]:["Jahre im Unterricht","Einsteigerangebot","Events und Gastlehrer","Google-Bewertung","Anzahl Bewertungen","Social Media"];
        var CROWN='<svg viewBox="0 0 26 20" aria-hidden="true"><path d="M2 17 0.5 5l6.5 5L13 1l6 9 6.500-5L24 17z" fill="#E4B95B" stroke="#F6DFA2" stroke-width="1" stroke-linejoin="round"/><rect x="2" y="17.5" width="22" height="2" rx="1" fill="#C9962F"/></svg>';
        var MAX=[10,10,10,25,10,10], NYC=en?"Not counted yet: festivals (15), recent reviews (5), competitions (5)":"Noch nicht gewertet: Festivals (15), aktuelle Bewertungen (5), Wettbewerbe (5)";
        h+='<div class="prelim"><span class="prelim-badge">'+esc(L("prelim_badge"))+'</span><p class="votebanner"><b>&#9733; '+esc(L("vote_h"))+'</b> · '+esc(L("vote_banner"))+'</p><ol class="ilist">';
        pl.forEach(function(e,i){
          var u=safeUrl(e.url), g=i<3?" g"+(i+1):"", why="";
          FAC.forEach(function(f,k){ var fx=(k===3?e.fx[0]:(k===4?e.fx[0].split(" · ")[1]:(k===5?e.fx[1]:"")));
            why+='<div><b>'+esc(f)+'</b> · '+num(e.sc[k])+' / '+MAX[k]+(fx&&fx!=="–"?' <small>('+esc(k===5?(en?"followers · posts: ":"Follower · Posts: ")+fx:fx)+')</small>':'')+'<div class="bar"><i style="width:'+(e.sc[k]/MAX[k]*100)+'%"></i></div></div>'; });
          var sty=e.st&&e.st.length?e.st.map(function(x){return '<span class="chip st">'+esc(x)+'</span>';}).join(" "):'<span class="chip">'+esc(en?"To be confirmed":"Zu bestätigen")+'</span>';
          why+='<div class="tbc"><b>'+esc(en?"Style variety (Dominicana, Sensual, Moderna)":"Stilvielfalt (Dominicana, Sensual, Moderna)")+'</b> · '+sty+'</div>';
          var TBC=en?[["Festivals","15"],["Recent reviews","5"],["Competitions entered","5"],["Competitions won","5"]]:[["Festivals","15"],["Aktuelle Bewertungen","5"],["Teilnahme an Wettbewerben","5"],["Wettbewerbe gewonnen","5"]];
          TBC.forEach(function(x){ why+='<div class="tbc"><b>'+esc(x[0])+'</b> · <span class="chip">'+esc(en?"To be confirmed":"Zu bestätigen")+'</span><div class="bar dash"></div></div>'; });
          why+='<div class="lk" style="color:var(--muted)">'+esc(en?"Not scored yet. Schools confirm these with links when they apply.":"Noch ohne Punkte. Schulen bestätigen diese Angaben mit Links bei der Bewerbung.")+' <a href="bewerbung.html">'+esc(en?"Confirm now":"Jetzt bestätigen")+' →</a></div>';
          why+='<div class="vote"><button type="button" class="btn btn-gold vbtn" data-s="'+esc(e.name)+'" data-c="'+cn(e)+'">&#9733; '+esc(L("vote_btn"))+'</button>'
            +'<form class="vform" hidden novalidate><input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px"><label>'+esc(L("vote_mail"))+'<input type="email" name="email" required autocomplete="email" inputmode="email"></label><label class="newsopt"><input type="checkbox" name="news" value="1"> <span>'+esc(L("news_opt"))+'</span></label><button type="submit" class="btn btn-gold">'+esc(L("vote_send"))+'</button><small>'+esc(L("vote_note"))+'</small></form><p class="vmsg" role="status" hidden></p></div>';
          why+='<div class="lk"><a href="schools/'+slug(e.name)+'.html"><b>'+esc(L("page_link"))+' →</b></a></div>';
          if(u) why+='<div class="lk"><a href="'+u+'" rel="noopener">'+esc(L("site"))+' →</a></div>';
          h+='<li'+(i>=10?' class="more" hidden':'')+'><details class="irk'+g+'"><summary><span class="rk">'+(i===0?CROWN+'<i class="sp a"></i><i class="sp b"></i><i class="sp c"></i><i class="sp d"></i>':'')+(i+1)+'</span><span class="who"><b><a href="schools/'+slug(e.name)+'.html">'+esc(e.name)+'</a></b>'
            +(c==="deutschland"?'<small>'+cn(e)+'</small>':'')+'</span><span class="score">'+num(e.pts)+'<small> / 100</small></span><span class="meter"><i style="width:'+e.pts+'%"></i></span></summary>'
            +'<div class="iwhy">'+why+'</div></details></li>';
        });
        h+='</ol>';
        if(pl.length>10) h+='<button type="button" class="btn btn-ghost showall" style="margin-top:16px">'+esc(en?"Show all "+pl.length+" schools":"Alle "+pl.length+" Schulen anzeigen")+'</button>';
        h+='<details class="howto"><summary>'+esc(L("prelim_h"))+'</summary><p>'+esc(L("prelim_p"))+'</p></details></div>';
      }
      var tips=TX.help_tips[window.LANG==="en"?1:0].map(function(x){return '<li>'+esc(x)+'</li>';}).join("");
      h+='<div class="helpbox"><h3>'+esc(L("help_h"))+'</h3><p>'+esc(L("help_p"))+'</p><div class="hb-btns"><a class="btn btn-ghost" href="index.html#method">'+esc(L("help_how"))+'</a><a class="btn btn-gold" href="bewerbung.html">'+esc(L("help_add"))+'</a></div><details><summary>'+esc(L("help_tips_h"))+'</summary><ul>'+tips+'</ul></details></div>';
      h+='<div class="note-card"><div><h3>'+esc(L("note_h"))+'</h3><p>'+esc(L("note_p"))+'</p></div><a class="btn btn-gold" href="bewerbung.html">'+esc(L("note_btn"))+'</a></div>';
    }
    panel.innerHTML=h;
    var voted=false; try{ voted=!!localStorage.getItem("lda-voted"); }catch(x){}
    panel.querySelectorAll(".vote").forEach(function(v){ if(voted){ var m=v.querySelector(".vmsg"); v.querySelector(".vbtn").hidden=true; m.textContent=L("vote_done"); m.hidden=false; } });
    panel.querySelectorAll(".vbtn").forEach(function(b){ b.addEventListener("click",function(){ var f=b.parentNode.querySelector(".vform"); f.hidden=false; b.hidden=true; f.elements.email.focus(); }); });
    panel.querySelectorAll(".vform").forEach(function(f){ f.addEventListener("submit",function(ev){ ev.preventDefault();
      var v=f.parentNode, b=v.querySelector(".vbtn"), msg=v.querySelector(".vmsg"), em=f.elements.email.value.trim();
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)){ msg.textContent=L("vote_err"); msg.hidden=false; return; }
      var sub=f.querySelector("button[type=submit]"); sub.disabled=true;
      var body=new URLSearchParams(); body.append("action","vote"); body.append("school",b.getAttribute("data-s")); body.append("city",b.getAttribute("data-c")); body.append("email",em); body.append("hp",f.elements.hp.value); body.append("news",f.elements.news&&f.elements.news.checked?"1":"0"); body.append("language",window.LANG==="en"?"EN":"DE");
      fetch(VOTE_ENDPOINT,{method:"POST",mode:"no-cors",body:body}).then(function(){ try{ localStorage.setItem("lda-voted","1"); }catch(x){} f.hidden=true; msg.textContent=L("vote_ok"); msg.hidden=false; }).catch(function(){ sub.disabled=false; msg.textContent=L("vote_err"); msg.hidden=false; });
    }); });
    var sa=panel.querySelector(".showall"); if(sa) sa.addEventListener("click",function(){ panel.querySelectorAll("li.more").forEach(function(l){ l.hidden=false; }); sa.remove(); });
    try{ if(!window.matchMedia("(prefers-reduced-motion: reduce)").matches){ panel.querySelectorAll(".irk .score").forEach(function(el){ var tn=el.firstChild, to=parseFloat(String(tn.nodeValue).replace(",",".")); if(!(to>0)) return; var t0=null; function st(ts){ t0=t0||ts; var k=Math.min(1,(ts-t0)/1200), v=to*(1-Math.pow(1-k,3)); tn.nodeValue=num(v); if(k<1) requestAnimationFrame(st); } requestAnimationFrame(st); }); } }catch(e){}
    if(document.getElementById("tab-"+c)) panel.setAttribute("aria-labelledby","tab-"+c); else panel.setAttribute("aria-label",cname(c));
  }
  var QUICK=["deutschland","berlin","muenchen","hamburg","koeln","frankfurt","duesseldorf"];
  var cq=document.getElementById("cityq"), cl=document.getElementById("citylist"), cp=document.getElementById("citypick"), actI=-1, shown=[];
  function cname(c){ return TX.cities[c][window.LANG==="en"?1:0]; }
  function norm(t){ return String(t).toLowerCase().replace(/ä/g,"a").replace(/ö/g,"o").replace(/ü/g,"u").replace(/ß/g,"ss").normalize("NFD").replace(/[\u0300-\u036f]/g,""); }
  function cityList(q){
    q=norm(q||"").trim();
    var o=Object.keys(TX.cities).filter(function(c){ return QUICK.indexOf(c)<0 && (!q || norm(TX.cities[c][0]).indexOf(q)>-1 || norm(TX.cities[c][1]).indexOf(q)>-1); });
    o.sort(function(a,b){ return norm(cname(a)).localeCompare(norm(cname(b))); });
    return o;
  }
  function openList(q){
    shown=cityList(q); actI=-1;
    cl.innerHTML=shown.length ? shown.map(function(c,i){ var n=(CANDIDATES[c]||[]).length; return '<li role="option" data-c="'+c+'" id="co-'+c+'">'+esc(cname(c))+'<small>'+n+'</small></li>'; }).join("") : '<li class="none">'+(window.LANG==="en"?"No city found":"Keine Stadt gefunden")+'</li>';
    cl.hidden=false; cq.setAttribute("aria-expanded","true");
  }
  function closeList(){ cl.hidden=true; cq.setAttribute("aria-expanded","false"); }
  function setAct(i){
    var li=cl.querySelectorAll("li[data-c]"); if(!li.length) return;
    actI=(i+li.length)%li.length; li.forEach(function(x,k){ x.classList.toggle("act",k===actI); });
    li[actI].scrollIntoView({block:"nearest"}); cq.setAttribute("aria-activedescendant",li[actI].id);
  }
  function syncPicker(){
    cq.placeholder = cq.getAttribute(window.LANG==="en"?"data-ph-en":"data-ph-de");
    var inQ = QUICK.indexOf(current)>-1;
    cp.classList.toggle("sel",!inQ);
    cq.value = inQ ? "" : cname(current);
  }
  cq.addEventListener("focus",function(){ cq.select(); openList(""); });
  cq.addEventListener("click",function(){ if(cl.hidden){ cq.select(); openList(""); } });
  cq.addEventListener("input",function(){ openList(cq.value); });
  cq.addEventListener("keydown",function(ev){
    if(ev.key==="ArrowDown"){ ev.preventDefault(); if(cl.hidden) openList(cq.value); setAct(actI+1); }
    else if(ev.key==="ArrowUp"){ ev.preventDefault(); setAct(actI-1); }
    else if(ev.key==="Enter"){ ev.preventDefault(); var c = actI>-1 ? shown[actI] : (shown.length===1?shown[0]:null); if(c){ select(c,true); closeList(); cq.blur(); } }
    else if(ev.key==="Escape"){ closeList(); syncPicker(); cq.blur(); }
  });
  cl.addEventListener("mousedown",function(ev){ var li=ev.target.closest("li[data-c]"); if(!li) return; ev.preventDefault(); select(li.getAttribute("data-c"),true); closeList(); cq.blur(); });
  document.addEventListener("click",function(ev){ if(!cp.contains(ev.target)){ if(!cl.hidden){ closeList(); syncPicker(); } } });
  cq.addEventListener("blur",function(){ setTimeout(function(){ closeList(); syncPicker(); },120); });
  function select(c, push){
    if(!TX.cities[c]) c="deutschland";
    current=c;
    document.querySelectorAll(".tabs button").forEach(function(b){ b.setAttribute("aria-selected", b.dataset.city===c?"true":"false"); });
    if(push){ try{ history.replaceState(null,"","#"+c); }catch(e){} }
    syncPicker();
    render();
  }
  document.querySelectorAll(".tabs button").forEach(function(b){ b.addEventListener("click",function(){ select(b.dataset.city,true); }); });
  window.addEventListener("hashchange",function(){ var c=location.hash.slice(1); if(TX.cities[c]){ select(c,false); document.querySelector(".tabs").scrollIntoView({behavior:"smooth",block:"start"}); } });
  document.addEventListener("langchange",function(){ syncPicker(); render(); });
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
     'Beste Bachata-Schulen Deutschland 2026 · Ranking',
     'Die besten Bachata-Schulen in Deutschland: unabhängiges Ranking für 79 Städte, mit Punkten, Bewertungen und Abstimmung. Ergebnisse am 20. Dezember 2026.',
     'Best Bachata schools in Germany 2026 · Ranking',
     'The best Bachata schools in Germany: independent ranking for 79 cities, with scores, reviews and voting. Results on December 20, 2026.',
     'rankings.html', rank_main, r.en, rank_js,
     schema=[crumbs('Rankings 2026', 'rankings.html'), faq_schema(rfaq)])


# ======================================================================
# 404 PAGE
# ======================================================================
n = T('n')
nf_main = f'''
<section class="page-hero" aria-labelledby="nf-title">
  <div class="wrap">
    <div>
      <h1 id="nf-title">{n("span", "Diese Seite gibt es nicht", "This page doesn't exist")}</h1>
      <p class="lede">{n("span", "Der Link ist veraltet oder falsch geschrieben. Hier geht es weiter:", "The link is outdated or mistyped. Continue here:")}</p>
      <div class="ctas">
        <a class="btn btn-gold" href="/">{n("span", "Zur Startseite", "Go to the homepage")}</a>
        <a class="btn btn-ghost" href="/rankings.html">{n("span", "Zu den Rankings", "See the rankings")}</a>
      </div>
    </div>
  </div>
</section>
'''
page('404.html', 'Seite nicht gefunden · Latin Dance Awards', 'Diese Seite gibt es nicht. Zur Startseite der Bachata Awards 2026.',
     'Page not found · Latin Dance Awards', 'This page does not exist.', '404.html', nf_main, n.en, '', schema=[])
p404 = os.path.join(ROOT, '404.html')
h = open(p404, encoding='utf-8').read()
h = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex">', h)
h = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n', '', h)
# absolute links so the 404 works on any path
h = h.replace('href="index.html', 'href="/index.html').replace('href="rankings.html', 'href="/rankings.html').replace('href="bewerbung.html', 'href="/bewerbung.html').replace('href="favicon.svg"', 'href="/favicon.svg"').replace('href="apple-touch-icon.png"', 'href="/apple-touch-icon.png"')
open(p404, 'w', encoding='utf-8').write(h)

# ======================================================================
# LEGAL PAGES (drafts: noindex, not linked until operator details are filled in)
# ======================================================================
def legal(fname, tid, title_de, title_en, h_de, h_en, blocks):
    L = T(tid)
    body = ''.join(
        f'<h2>{L("span", hd, he)}</h2><p>{L("span", bd, be)}</p>' for hd, he, bd, be in blocks)
    main = f'''
<section class="page-hero" aria-labelledby="{tid}-t"><div class="wrap"><div>
  <h1 id="{tid}-t">{L("span", h_de, h_en)}</h1>
  <p class="lede">{L("span", "ENTWURF: Die Felder in [eckigen Klammern] müssen vor der Veröffentlichung ausgefüllt werden.", "DRAFT: fields in [square brackets] must be filled in before publishing.")}</p>
</div></div></section>
<section class="section"><div class="wrap" style="max-width:760px;line-height:1.7">{body}</div></section>
'''
    page(fname, title_de, title_de, title_en, title_en, fname, main, L.en, '', schema=[])
    pth = os.path.join(ROOT, fname)
    h = open(pth, encoding='utf-8').read()
    h = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex">', h)
    open(pth, 'w', encoding='utf-8').write(h)

legal('impressum.html', 'i', 'Impressum · Latin Dance Awards', 'Legal notice · Latin Dance Awards', 'Impressum', 'Legal notice', [
 ('Angaben gemäß § 5 DDG', 'Information pursuant to § 5 DDG',
  '[Vor- und Nachname bzw. Firma und Rechtsform] · [Straße und Hausnummer] · [PLZ und Ort] · [Land]',
  '[Full name or company and legal form] · [Street and number] · [Postcode and city] · [Country]'),
 ('Kontakt', 'Contact', 'E-Mail: info@latindanceawards.com', 'Email: info@latindanceawards.com'),
 ('Umsatzsteuer-ID', 'VAT ID', '[Umsatzsteuer-Identifikationsnummer, falls vorhanden]', '[VAT identification number, if any]'),
 ('Verantwortlich für den Inhalt', 'Responsible for content', '[Name und Anschrift wie oben]', '[Name and address as above]'),
 ('Unabhängigkeit', 'Independence', 'Latin Dance Awards ist ein unabhängiges Ranking. Die Platzierung kann nicht gekauft werden. Alle Bewertungen beruhen auf öffentlich zugänglichen Angaben.', 'Latin Dance Awards is an independent ranking. Places cannot be bought. All scores are based on publicly available information.'),
])

legal('datenschutz.html', 'd', 'Datenschutzerklärung · Latin Dance Awards', 'Privacy policy · Latin Dance Awards', 'Datenschutzerklärung', 'Privacy policy', [
 ('Verantwortlicher', 'Controller', '[Name und Anschrift wie im Impressum] · E-Mail: info@latindanceawards.com', '[Name and address as in the legal notice] · Email: info@latindanceawards.com'),
 ('Hosting', 'Hosting', 'Diese Website wird bei Cloudflare, Inc. gehostet. Dabei werden technisch notwendige Daten (z. B. IP-Adresse, Zeitpunkt, aufgerufene Seite) in Server-Logs verarbeitet. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (sicherer und stabiler Betrieb).', 'This website is hosted by Cloudflare, Inc. Technically necessary data (e.g. IP address, time, page requested) is processed in server logs. Legal basis: Art. 6(1)(f) GDPR (secure and stable operation).'),
 ('Bewerbungsformular', 'Application form', 'Wenn du dich bewirbst, speichern wir deine Angaben (Schulname, Stadt, Ansprechpartner, E-Mail, Angaben zu Kursen, Events und Links) in einer Google-Tabelle (Google Sheets / Apps Script, Google Ireland Ltd.). Wir nutzen sie ausschließlich, um deine Bewerbung zu prüfen und dich zu kontaktieren. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b und f DSGVO. Wir löschen die Daten spätestens 12 Monate nach Ende der Awards-Edition, sofern keine gesetzliche Pflicht entgegensteht.', 'When you apply, we store your details (school name, city, contact person, email, information on classes, events and links) in a Google spreadsheet (Google Sheets / Apps Script, Google Ireland Ltd.). We use them only to review your application and contact you. Legal basis: Art. 6(1)(b) and (f) GDPR. We delete the data at the latest 12 months after the end of the awards edition unless a legal duty requires otherwise.'),
 ('Publikumspreis (Abstimmung)', 'Audience Award (voting)', 'Wenn du beim Publikumspreis abstimmst, speichern wir deine E-Mail-Adresse, die gewählte Schule und den Zeitpunkt in einer Google-Tabelle (Google Sheets / Apps Script, Google Ireland Ltd.) und senden dir einen Bestätigungslink per E-Mail. Wir nutzen die Daten nur, um pro Person eine Stimme zu zählen und doppelte oder missbräuchliche Stimmen zu entfernen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. a und f DSGVO. Die Daten werden nach Abschluss der Auswertung gelöscht. [Löschfrist prüfen.]', 'When you vote in the Audience Award, we store your email address, the chosen school and the time in a Google spreadsheet (Google Sheets / Apps Script, Google Ireland Ltd.) and email you a confirmation link. We use the data only to count one vote per person and to remove duplicate or abusive votes. Legal basis: Art. 6(1)(a) and (f) GDPR. The data is deleted after the results are evaluated. [Review retention period.]'),
 ('Öffentlich zugängliche Daten über Schulen', 'Publicly available data about schools', 'Für das Ranking verwenden wir Angaben, die Schulen selbst öffentlich auf ihren Websites und Profilen veröffentlicht haben (z. B. Kursangebot, Gründungsjahr). Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Wenn du Angaben korrigieren oder entfernen lassen möchtest, schreibe uns an info@latindanceawards.com.', 'For the ranking we use information schools have published themselves on their websites and profiles (e.g. classes, founding year). Legal basis: Art. 6(1)(f) GDPR. To correct or remove information, email info@latindanceawards.com.'),
 ('Schriftarten', 'Fonts', 'Die Website lädt Schriftarten von Google Fonts (Google Ireland Ltd.). Dabei wird deine IP-Adresse an Google übertragen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. [Prüfen: Schriftarten idealerweise lokal einbinden.]', 'The website loads fonts from Google Fonts (Google Ireland Ltd.), which transmits your IP address to Google. Legal basis: Art. 6(1)(f) GDPR. [Review: ideally self-host the fonts.]'),
 ('E-Mail-Kontakt', 'Email contact', 'Wenn du uns schreibst, verarbeiten wir deine Nachricht, um sie zu beantworten. Unser E-Mail-Dienst ist Spacemail (Namecheap/Spaceship).', 'If you write to us, we process your message to answer it. Our email provider is Spacemail (Namecheap/Spaceship).'),
 ('Deine Rechte', 'Your rights', 'Du hast das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch. Du kannst dich außerdem bei einer Datenschutz-Aufsichtsbehörde beschweren. Schreibe uns einfach an info@latindanceawards.com.', 'You have the right of access, rectification, erasure, restriction, data portability and objection. You may also lodge a complaint with a data protection authority. Just email info@latindanceawards.com.'),
 ('Cookies und Tracking', 'Cookies and tracking', 'Wir setzen derzeit keine Tracking- oder Werbe-Cookies ein. [Prüfen und anpassen, falls später Analyse-Tools hinzukommen.]', 'We currently do not use tracking or advertising cookies. [Review and update if analytics tools are added later.]'),
])


# ======================================================================
# SCHOOL PAGES  (schools/<slug>.html)  generated from the interim list
# ======================================================================
import unicodedata

def slugify(name):
    s = name.lower()
    for a, b in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss')):
        s = s.replace(a, b)
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def parse_candidates():
    blk = re.search(r'var CANDIDATES = \{(.*?)\n  \};', rank_js, re.S).group(1)
    out, city = [], None
    for line in blk.split('\n'):
        m = re.match(r'\s*(\w+): \[\s*$', line)
        if m: city = m.group(1); continue
        if '{name:' not in line: continue
        name = re.search(r'name:"([^"]+)"', line).group(1)
        st = re.search(r'st:\[([^\]]*)\]', line)
        sc = [float(x) for x in re.search(r'sc:\[([^\]]*)\]', line).group(1).split(',')]
        fx = re.findall(r'"([^"]*)"', re.search(r'fx:\[([^\]]*)\]', line).group(1))
        url = re.search(r'url:"([^"]+)"', line).group(1)
        out.append(dict(name=name, city=city, st=re.findall(r'"([^"]+)"', st.group(1)) if st else [], sc=sc, fx=fx, url=url, pts=round(sum(sc), 1), slug=slugify(name)))
    return out

CITY_NAMES = {c[0]: (c[1], c[2]) for c in CITIES}
CITY_NAMES.update({'berlin': ('Berlin', 'Berlin'), 'muenchen': ('München', 'Munich'), 'koeln': ('Köln', 'Cologne'), 'duesseldorf': ('Düsseldorf', 'Düsseldorf')})
SCH = parse_candidates()
SCH.sort(key=lambda e: (-e['pts'], e['name']))
for i, e in enumerate(SCH): e['rank'] = i + 1
for c in {e['city'] for e in SCH}:
    for i, e in enumerate([x for x in SCH if x['city'] == c]): e['crank'] = i + 1

SCHOOL_CSS = r'''
.sp-hero{padding:96px 0 56px;background:radial-gradient(ellipse 55% 60% at 85% 10%,rgba(228,185,91,.10),transparent 60%),linear-gradient(180deg,var(--velvet-deep),var(--velvet))}
.sp-crumb{font-size:14px;color:var(--muted);margin-bottom:20px}.sp-crumb a{color:var(--gold-light);text-decoration:none}
.sp-hero .wrap{display:grid;grid-template-columns:1fr auto;gap:36px;align-items:end}
.sp-hero h1{font-family:var(--serif);font-weight:500;font-size:clamp(34px,5vw,64px);line-height:1.05;margin:16px 0 14px}
.sp-hero .lede{color:var(--muted);font-size:18px;max-width:34em}
.sp-score{text-align:center;padding:22px 30px;border-radius:24px;background:var(--card);border:1px solid rgba(228,185,91,.4)}
.sp-score b{display:block;font-family:var(--serif);font-weight:500;font-size:clamp(46px,7vw,76px);line-height:1;color:var(--gold-light)}
.sp-score small{color:var(--muted);font-size:14px}
.sp-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:22px;align-items:start}
.sp-card{padding:30px;border-radius:24px;background:var(--card);border:1px solid var(--line)}
.sp-card h2{font-family:var(--serif);font-weight:500;font-size:28px;margin-bottom:6px}
.sp-card > p{color:var(--muted);margin-bottom:16px}
.sp-row{padding:12px 0;border-top:1px solid rgba(255,255,255,.07);font-size:15px;color:var(--muted)}
.sp-row:first-of-type{border-top:0}
.sp-row b{color:var(--cream);font-weight:600}
.sp-row .bar{height:5px;margin-top:8px;border-radius:5px;background:rgba(255,255,255,.07);overflow:hidden}
.sp-row .bar i{display:block;height:100%;background:var(--gold)}
.sp-row .chip{display:inline-block;padding:2px 10px;border-radius:999px;border:1px dashed rgba(228,185,91,.55);color:var(--gold-light);font-size:12px;font-weight:600}
.sp-row .chip.st{border:1px solid rgba(228,185,91,.5);background:rgba(228,185,91,.16);color:#E4B95B}
.sp-links{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.sp-form{display:grid;gap:12px;max-width:520px}
.sp-form label{display:grid;gap:6px;color:var(--cream);font-size:14px}
.sp-form input[type=email],.sp-form input[type=text],.sp-form textarea{width:100%;padding:12px 14px;border-radius:12px;border:1px solid rgba(246,231,211,.35);background:rgba(255,255,255,.06);color:var(--cream);font:inherit;font-size:16px}
.sp-form textarea{min-height:110px;resize:vertical}
.sp-form small,.sp-msg{color:var(--muted);font-size:13px;line-height:1.5}
.sp-msg{margin:12px 0 0;color:var(--gold-light);font-size:14.5px}
.sp-card [hidden]{display:none!important}
.sp-hero button.btn:not(.btn-gold),.sp-card button.btn:not(.btn-gold){background:transparent;color:var(--cream);border:1px solid rgba(246,231,211,.35)}
.sp-hero button.btn,.sp-card button.btn{font:inherit;font-weight:600;cursor:pointer;-webkit-appearance:none;appearance:none}
.sp-stars{display:flex;gap:6px;flex-direction:row-reverse;justify-content:flex-end}
.sp-stars input{position:absolute;opacity:0;width:1px;height:1px}
.sp-stars label{font-size:32px;line-height:1;color:rgba(246,231,211,.28);cursor:pointer;display:block}
.sp-stars input:checked ~ label,.sp-stars label:hover,.sp-stars label:hover ~ label{color:var(--gold)}
.sp-stars input:focus-visible + label{outline:2px solid var(--gold);outline-offset:3px;border-radius:6px}
.sp-sum{display:flex;align-items:center;gap:12px;margin:10px 0 18px;color:var(--muted)}
.sp-sum b{font-family:var(--serif);font-size:38px;color:var(--gold-light);font-weight:500}
.sp-rv{padding:16px 0;border-top:1px solid rgba(255,255,255,.08)}
.sp-rv .top{display:flex;justify-content:space-between;gap:12px;color:var(--muted);font-size:13px}
.sp-rv .st{color:var(--gold);letter-spacing:2px}
.sp-rv p{margin:6px 0;color:var(--cream);font-size:15.5px;white-space:pre-line;overflow-wrap:anywhere}
.sp-rv a{color:var(--muted);font-size:12.5px}
.sp-two{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}
@media(max-width:860px){.sp-hero .wrap,.sp-grid,.sp-two{grid-template-columns:1fr}.sp-hero{padding-top:84px}.sp-score{justify-self:start}}
'''

SCHOOL_JS = r'''
  var SCHOOL = __SCHOOL__, EP = "__EP__", MAILTO = "hello@latindanceawards.com";
  var S = {
    vote_btn:["Für diese Schule abstimmen","Vote for this school"], vote_mail:["Deine E-Mail-Adresse","Your email address"], vote_send:["Stimme abschicken","Send my vote"],
    news_opt:["Ja, schickt mir gelegentlich Neuigkeiten, Events und Angebote rund um Bachata per E-Mail. Abmeldung jederzeit möglich.","Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time."],
    vote_note:["Eine Stimme pro Person. Wir schicken dir einen Bestätigungslink. Deine E-Mail nutzen wir nur dafür und zum Entfernen doppelter Stimmen.","One vote per person. We email you a confirmation link. We use your email only for that and to remove duplicate votes."],
    vote_ok:["Fast geschafft: Wir haben dir eine E-Mail geschickt. Klicke auf den Link darin, damit deine Stimme zählt. Schau auch im Spam-Ordner nach.","Almost done: we sent you an email. Click the link in it so your vote counts. Check your spam folder too."],
    vote_done:["Du hast auf diesem Gerät schon abgestimmt. Danke!","You already voted on this device. Thank you!"],
    err_mail:["Bitte prüfe deine E-Mail-Adresse und versuche es noch einmal.","Please check your email address and try again."],
    rv_ok:["Fast geschafft: Wir haben dir eine E-Mail geschickt. Klicke auf den Link darin, dann erscheint deine Bewertung hier.","Almost done: we sent you an email. Click the link in it and your review will appear here."],
    rv_err:["Bitte wähle Sterne und schreibe 10 bis 600 Zeichen, ohne Links und ohne @.","Please pick a star rating and write 10 to 600 characters, with no links and no @."],
    none:["Noch keine Bewertungen. Sei die erste Person!","No reviews yet. Be the first!"], report:["Melden","Report"], anon:["Anonym","Anonymous"],
    of:["Bewertungen","reviews"], one:["Bewertung","review"], fail:["Bewertungen konnten nicht geladen werden.","Reviews could not be loaded."],
    copied:["Link kopiert","Link copied"]
  };
  function L(k){ return S[k][window.LANG==="en"?1:0]; }
  function esc(s){ return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];}); }
  var mailRe=/^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  /* vote */
  var vb=document.getElementById("vbtn"), vf=document.getElementById("vform"), vm=document.getElementById("vmsg");
  try{ if(localStorage.getItem("lda-voted")){ vb.hidden=true; vm.textContent=L("vote_done"); vm.hidden=false; document.addEventListener("langchange",function(){ if(!vm.hidden&&vb.hidden&&vf.hidden) vm.textContent=L("vote_done"); }); } }catch(x){}
  vb.addEventListener("click",function(){ vf.hidden=false; vb.hidden=true; vf.elements.email.focus(); });
  vf.addEventListener("submit",function(ev){ ev.preventDefault(); var em=vf.elements.email.value.trim();
    if(!mailRe.test(em)){ vm.textContent=L("err_mail"); vm.hidden=false; return; }
    var sub=vf.querySelector("button[type=submit]"); sub.disabled=true;
    var b=new URLSearchParams({action:"vote",school:SCHOOL.name,city:SCHOOL.city,email:em,news:vf.elements.news.checked?"1":"0",hp:vf.elements.hp.value,language:window.LANG==="en"?"EN":"DE"});
    fetch(EP,{method:"POST",mode:"no-cors",body:b}).then(function(){ try{localStorage.setItem("lda-voted","1");}catch(x){} vf.hidden=true; vm.textContent=L("vote_ok"); vm.hidden=false; }).catch(function(){ sub.disabled=false; vm.textContent=L("err_mail"); vm.hidden=false; });
  });

  /* reviews: list */
  var rl=document.getElementById("rvlist"), rs=document.getElementById("rvsum");
  function stars(n){ return "★★★★★".slice(0,n)+"☆☆☆☆☆".slice(0,5-n); }
  function loadReviews(){
    fetch(EP+"?action=reviews&school="+encodeURIComponent(SCHOOL.name)).then(function(r){return r.json();}).then(function(d){
      rs.innerHTML = d.count ? '<b>'+String(d.avg).replace(".",window.LANG==="en"?".":",")+'</b><span><span class="st" style="color:var(--gold)">'+stars(Math.round(d.avg))+'</span><br>'+d.count+' '+L(d.count===1?"one":"of")+'</span>' : "";
      rl.innerHTML = d.count ? d.items.map(function(x){ return '<div class="sp-rv"><div class="top"><span class="st">'+stars(x.r)+'</span><span>'+esc(x.n||L("anon"))+' · '+esc(x.d)+'</span></div><p>'+esc(x.t)+'</p><a href="mailto:'+MAILTO+'?subject='+encodeURIComponent("Report review: "+SCHOOL.name)+'&body='+encodeURIComponent(x.d+" / "+(x.n||"")+" / "+x.t.slice(0,60))+'">'+esc(L("report"))+'</a></div>'; }).join("") : '<p class="sp-msg" style="color:var(--muted)">'+esc(L("none"))+'</p>';
    }).catch(function(){ rl.innerHTML='<p class="sp-msg" style="color:var(--muted)">'+esc(L("fail"))+'</p>'; });
  }
  loadReviews(); document.addEventListener("langchange",loadReviews);

  /* reviews: submit */
  var rf=document.getElementById("rvform"), rm=document.getElementById("rvmsg");
  rf.addEventListener("submit",function(ev){ ev.preventDefault();
    var rating=(rf.querySelector("input[name=rating]:checked")||{}).value, text=rf.elements.text.value.trim(), name=rf.elements.name.value.trim(), em=rf.elements.email.value.trim();
    if(!rating||text.length<10||text.length>600||/https?:|www\.|@/i.test(text+" "+name)){ rm.textContent=L("rv_err"); rm.hidden=false; return; }
    if(!mailRe.test(em)){ rm.textContent=L("err_mail"); rm.hidden=false; return; }
    var sub=rf.querySelector("button[type=submit]"); sub.disabled=true;
    var b=new URLSearchParams({action:"review",school:SCHOOL.name,city:SCHOOL.city,name:name,rating:rating,text:text,email:em,news:rf.elements.news.checked?"1":"0",hp:rf.elements.hp.value,language:window.LANG==="en"?"EN":"DE"});
    fetch(EP,{method:"POST",mode:"no-cors",body:b}).then(function(){ rf.hidden=true; rm.textContent=L("rv_ok"); rm.hidden=false; }).catch(function(){ sub.disabled=false; rm.textContent=L("err_mail"); rm.hidden=false; });
  });

  /* share */
  var sh=document.getElementById("share");
  sh.addEventListener("click",function(){ var u=location.origin+location.pathname;
    if(navigator.share){ navigator.share({title:document.title,url:u}).catch(function(){}); }
    else if(navigator.clipboard){ navigator.clipboard.writeText(u).then(function(){ var o=sh.textContent; sh.textContent=L("copied"); setTimeout(function(){ sh.innerHTML=o; },1600); }); } });
'''


# ======================================================================
# SHARE KIT (caption + story image per school)
# ======================================================================
KIT_CSS = r"""
.kit{border:1px solid var(--line);border-radius:22px;background:var(--card);padding:28px;max-width:760px}
.kit h2{font-family:var(--serif);font-weight:500;font-size:clamp(24px,4vw,32px);margin-bottom:8px}
.kit p.lead{color:var(--muted);margin-bottom:20px;line-height:1.55}
.kit .kit-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.kit label{display:grid;gap:6px;font-size:13.5px;color:var(--muted)}
.kit textarea{width:100%;padding:12px 14px;border-radius:12px;border:1px solid rgba(246,231,211,.3);background:rgba(255,255,255,.05);color:var(--cream);font:inherit;font-size:14px;line-height:1.5;resize:vertical}
.kit .kit-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.kit .kit-row .btn{padding:12px 20px;font-size:14px}
.kit .btn-ghost{background:transparent!important;color:var(--cream)!important;border:1px solid var(--line)!important}
.kit .btn-ghost:hover{border-color:var(--gold)!important;color:var(--gold-light)!important}
.kit .kit-grid{align-items:end}
.kit textarea{min-height:190px}
.kit .kit-link{margin:0 0 18px;padding:12px 14px;border-radius:12px;background:rgba(228,185,91,.08);border:1px dashed var(--line);font-size:14px;word-break:break-all;color:var(--gold-light)}
.kit .kit-msg{min-height:20px;margin-top:10px;font-size:13.5px;color:var(--gold-light)}
.kit select{width:100%;padding:12px 14px;border-radius:12px;border:1px solid rgba(246,231,211,.35);background:#14100f;color:var(--cream);font:inherit;margin-bottom:18px}
@media (max-width:620px){.kit{padding:20px}.kit .kit-grid{grid-template-columns:1fr}.kit .kit-row .btn{flex:1 1 100%}}
"""

KIT_JS = r"""
  function initKit(root, name, city, slug){
    var base="https://latindanceawards.com/schools/"+slug+".html";
    var $=function(q){return root.querySelector(q);};
    var link=$(".kit-link"), de=$(".kit-de"), en=$(".kit-en"), msg=$(".kit-msg");
    link.textContent=base;
    var tag=city.toLowerCase().replace(/ä/g,"ae").replace(/ö/g,"oe").replace(/ü/g,"ue").replace(/ß/g,"ss").replace(/[^a-z0-9]/g,"");
    de.value="🏆 Stimmt für "+name+" ab!\n\nWir sind im Rennen um den Publikumspreis der Bachata Awards Deutschland 2026. Deine Stimme dauert 30 Sekunden (eine Stimme pro Person, bestätigt per E-Mail):\n"+base+"\n\n#bachata #bachata"+tag+" #latindanceawards";
    en.value="🏆 Vote for "+name+"!\n\nWe are in the running for the Audience Award of the Bachata Awards Germany 2026. Voting takes 30 seconds (one vote per person, confirmed by email):\n"+base+"\n\n#bachata #bachata"+tag+" #latindanceawards";
    function say(t){msg.textContent=t;setTimeout(function(){msg.textContent="";},3500);}
    function copy(txt){
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(function(){say(window.LANG==="en"?"Copied.":"Kopiert.");},function(){fallback(txt);});}
      else fallback(txt);
    }
    function fallback(txt){var t=document.createElement("textarea");t.value=txt;document.body.appendChild(t);t.select();try{document.execCommand("copy");say(window.LANG==="en"?"Copied.":"Kopiert.");}catch(e){}document.body.removeChild(t);}
    $(".kit-copy-de").onclick=function(){copy(de.value);};
    $(".kit-copy-en").onclick=function(){copy(en.value);};
    $(".kit-copy-link").onclick=function(){copy(base);};
    $(".kit-wa").onclick=function(){var t=(window.LANG==="en"?en:de).value;window.open("https://wa.me/?text="+encodeURIComponent(t),"_blank","noopener");};
    var sh=$(".kit-share");
    if(navigator.share){sh.hidden=false;sh.onclick=function(){navigator.share({title:name,text:(window.LANG==="en"?en:de).value,url:base}).catch(function(){});};}
    function wrap(ctx,text,x,y,maxW,lh){var words=text.split(" "),line="",lines=[];words.forEach(function(w){var t=line?line+" "+w:w;if(ctx.measureText(t).width>maxW&&line){lines.push(line);line=w;}else line=t;});lines.push(line);lines.forEach(function(l,i){ctx.fillText(l,x,y+i*lh);});return lines.length;}
    function image(W,H,file){
      var c=document.createElement("canvas");c.width=W;c.height=H;var x=c.getContext("2d");
      x.fillStyle="#080707";x.fillRect(0,0,W,H);
      var rg=x.createRadialGradient(W/2,H*0.62,50,W/2,H*0.62,H*0.6);rg.addColorStop(0,"rgba(228,185,91,.28)");rg.addColorStop(1,"rgba(228,185,91,0)");x.fillStyle=rg;x.fillRect(0,0,W,H);
      var g=x.createLinearGradient(0,0,W,H);g.addColorStop(0,"#fcebb6");g.addColorStop(.45,"#e2b457");g.addColorStop(1,"#b07a27");
      x.strokeStyle=g;x.lineWidth=6;x.strokeRect(40,40,W-80,H-80);x.lineWidth=2;x.strokeRect(62,62,W-124,H-124);
      x.textAlign="center";var en_=window.LANG==="en";var s=W/1080;
      x.fillStyle=g;x.font="bold "+Math.round(120*s)+"px Georgia,serif";x.fillText("★",W/2,H*0.2);
      x.fillStyle="#f6e7d3";x.font=Math.round(46*s)+"px Georgia,serif";x.fillText(en_?"Vote for":"Stimme für",W/2,H*0.2+90*s);
      x.fillStyle=g;x.font="bold "+Math.round(96*s)+"px Georgia,serif";
      var n=wrap(x,name,W/2,H*0.36,W-200*s,110*s);
      var yy=H*0.36+n*110*s+30*s;
      x.fillStyle="#f6e7d3";x.font=Math.round(48*s)+"px Georgia,serif";x.fillText(city,W/2,yy);
      x.fillStyle="#b9ab98";x.font=Math.round(36*s)+"px Arial,sans-serif";
      x.fillText(en_?"Audience Award · Bachata Awards Germany 2026":"Publikumspreis · Bachata Awards Deutschland 2026",W/2,yy+90*s);
      x.fillStyle=g;x.fillRect(W/2-120*s,H*0.74,240*s,4);
      x.fillStyle="#f6e7d3";x.font="bold "+Math.round(44*s)+"px Arial,sans-serif";x.fillText(en_?"One vote takes 30 seconds":"Eine Stimme dauert 30 Sekunden",W/2,H*0.74+90*s);
      x.fillStyle=g;x.font="bold "+Math.round(50*s)+"px Arial,sans-serif";x.fillText("latindanceawards.com",W/2,H*0.74+170*s);
      x.fillStyle="#b9ab98";x.font=Math.round(30*s)+"px Arial,sans-serif";x.fillText(en_?"Results on December 20, 2026":"Ergebnisse am 20. Dezember 2026",W/2,H-110*s);
      c.toBlob(function(b){var a=document.createElement("a");a.href=URL.createObjectURL(b);a.download=file+".png";document.body.appendChild(a);a.click();document.body.removeChild(a);setTimeout(function(){URL.revokeObjectURL(a.href);},2000);say(window.LANG==="en"?"Image saved.":"Bild gespeichert.");},"image/png");
    }
    $(".kit-story").onclick=function(){image(1080,1920,"vote-story-"+slug);};
    $(".kit-post").onclick=function(){image(1080,1350,"vote-post-"+slug);};
  }
"""

def kit_body(s, with_select=False, opts=''):
    sel = ''
    if with_select:
        sel = f'<label>{s("span", "Deine Schule", "Your school")}<select class="kit-select" aria-label="School">{opts}</select></label>'
    return f"""
    {sel}
    <p class="kit-link" aria-live="polite"></p>
    <div class="kit-grid">
      <label>{s("span", "Text für Instagram, Facebook und WhatsApp (Deutsch)", "Caption for Instagram, Facebook and WhatsApp (German)")}<textarea class="kit-de" readonly></textarea></label>
      <label>{s("span", "Caption (English)", "Caption (English)")}<textarea class="kit-en" readonly></textarea></label>
    </div>
    <div class="kit-row">
      <button type="button" class="btn btn-gold kit-copy-de">{s("span", "Text kopieren (DE)", "Copy text (DE)")}</button>
      <button type="button" class="btn btn-ghost kit-copy-en">{s("span", "Copy text (EN)", "Copy text (EN)")}</button>
      <button type="button" class="btn btn-ghost kit-copy-link">{s("span", "Link kopieren", "Copy link")}</button>
      <button type="button" class="btn btn-ghost kit-wa">{s("span", "Per WhatsApp teilen", "Share on WhatsApp")}</button>
      <button type="button" class="btn btn-ghost kit-share" hidden>{s("span", "Teilen…", "Share…")}</button>
    </div>
    <div class="kit-row">
      <button type="button" class="btn btn-gold kit-story">{s("span", "Story-Bild laden (1080×1920)", "Download story image (1080×1920)")}</button>
      <button type="button" class="btn btn-ghost kit-post">{s("span", "Post-Bild laden (1080×1350)", "Download post image (1080×1350)")}</button>
    </div>
    <p class="kit-msg" role="status"></p>"""

GUIDE_CITIES = {'berlin','hamburg','muenchen','koeln','frankfurt','stuttgart','duesseldorf','freiburg','dresden','nuernberg','bremen','saarbruecken','gelsenkirchen','bonn','kempten','oldenburg','essen','karlsruhe'}

def kit_section(s, nm, de_city, slug, ckey=None):
    more = ''
    if ckey in GUIDE_CITIES:
        more = f'''<section class="block"><div class="wrap"><div class="kit" style="padding:20px 28px">{s("p", f'Mehr Schulen, Kurse und Partys: <a href="/bachata-{ckey}.html">Bachata {de_city}: alle Schulen im Überblick</a>.', f'More schools, classes and parties: <a href="/bachata-{ckey}.html">Bachata {de_city}: all schools at a glance</a>.')}</div></div></section>
'''
    return more + f"""<section class="block" aria-labelledby="kit-title">
  <div class="wrap">
    <div class="kit" id="share">
      {s("h2", "Teile diese Seite und hol dir Stimmen", "Share this page and collect votes").replace("<h2", '<h2 id="kit-title"')}
      {s("p", "Für Schulen: Hier ist ein fertiger Text und ein Bild für deine Story. Poste beides und bitte deine Schüler, in 30 Sekunden abzustimmen.", "For schools: here is a ready-made caption and an image for your story. Post both and ask your students to vote in 30 seconds.", 'class="lead"')}
      {kit_body(s)}
    </div>
  </div>
</section>
"""

def build_school(e):
    s = T('s')
    en_city = CITY_NAMES[e['city']][1]; de_city = CITY_NAMES[e['city']][0]
    nm = e['name']
    FAC = [('Jahre im Unterricht', 'Years teaching', 10), ('Einsteigerangebot', 'Beginner offer', 10), ('Events und Gastlehrer', 'Events and guests', 10),
           ('Google-Bewertung', 'Google rating', 25), ('Anzahl Bewertungen', 'Number of reviews', 10), ('Social Media', 'Social media', 10)]
    rows = ''
    for k, (de, en, mx) in enumerate(FAC):
        fx = e['fx'][0] if k == 3 else (e['fx'][0].split(' · ')[1] if k == 4 and ' · ' in e['fx'][0] else (e['fx'][1] if k == 5 else ''))
        small = f' <small>({fx})</small>' if fx and fx != '–' else ''
        pts = f"{e['sc'][k]:g}".replace('.', ',')
        rows += f'<div class="sp-row"><b>{s("span", de, en)}</b> · {pts} / {mx}{small}<div class="bar"><i style="width:{e["sc"][k]/mx*100:.0f}%"></i></div></div>\n'
    sty = ' '.join(f'<span class="chip st">{x}</span>' for x in e['st']) or f'<span class="chip">{s("span", "Zu bestätigen", "To be confirmed")}</span>'
    rows += f'<div class="sp-row"><b>{s("span", "Stilvielfalt (Dominicana, Sensual, Moderna)", "Style variety (Dominicana, Sensual, Moderna)")}</b> · {sty}</div>\n'
    for de, en in (('Festivals', 'Festivals'), ('Aktuelle Bewertungen', 'Recent reviews'), ('Teilnahme an Wettbewerben', 'Competitions entered'), ('Wettbewerbe gewonnen', 'Competitions won')):
        rows += f'<div class="sp-row"><b>{s("span", de, en)}</b> · <span class="chip">{s("span", "Zu bestätigen", "To be confirmed")}</span></div>\n'
    maps = 'https://www.google.com/maps/search/?api=1&query=' + re.sub(r'%20', '+', __import__('urllib.parse', fromlist=['quote']).quote(f'{nm} {de_city}'))
    pts_s = f"{e['pts']:g}".replace('.', ',')
    crank, rank = e['crank'], e['rank']
    h1 = f'{nm}'
    main = f'''
<section class="sp-hero" aria-labelledby="sp-title">
  <div class="wrap">
    <div>
      <p class="sp-crumb"><a href="/rankings.html">{s("span", "Rankings 2026", "Rankings 2026")}</a> › {de_city if True else ''}</p>
      <span class="edition"><i></i>{s("span", "Zwischenstand · kein Endergebnis", "Interim standing · not final")}</span>
      <h1 id="sp-title">{h1}</h1>
      <p class="lede">{s("span", f"Bachata-Schule in {de_city}. Zwischenstand im Ranking: Platz {crank} in {de_city}, Platz {rank} in Deutschland. Die Schulen sind noch im Wettbewerb.", f"Bachata school in {en_city}. Interim ranking: place {crank} in {en_city}, place {rank} in Germany. The schools are still competing.")}</p>
      <div class="sp-links"><button type="button" class="btn btn-ghost" id="share">{s("span", "Teilen", "Share")}</button></div>
    </div>
    <div class="sp-score"><b>{pts_s}</b><small>/ 100 · {s("span", "Zwischenstand", "interim")}</small></div>
  </div>
</section>

<section class="block alt" aria-label="Details">
  <div class="wrap sp-grid">
    <div class="sp-card">
      {s("h2", "So setzt sich die Punktzahl zusammen", "How the score is made up")}
      {s("p", "Sechs von neun Kriterien sind bisher gewertet (höchstens 75 Punkte). Offene Kriterien zählen noch nicht und können Schulen bei der Bewerbung bestätigen. Datenstand: Oktober 2026 (Google, Instagram, Website der Schule).", "Six of nine factors are scored so far (75 points at most). Open factors do not count yet, and schools can confirm them when they apply. Data as of October 2026 (Google, Instagram, the school's website).")}
      {rows}
      <div class="sp-links"><a class="btn btn-ghost" href="{e['url']}" rel="noopener nofollow" target="_blank">{s("span", "Website der Schule →", "School website →")}</a><a class="btn btn-ghost" href="{maps}" rel="noopener nofollow" target="_blank">{s("span", "Auf Google Maps →", "On Google Maps →")}</a></div>
    </div>
    <div class="sp-card">
      {s("h2", "Publikumspreis: abstimmen", "Audience Award: vote")}
      {s("p", "Eine Stimme pro Person, bestätigt per E-Mail. Der Publikumspreis ist unabhängig von den 100 Punkten. Das Ergebnis kommt am 20. Dezember.", "One vote per person, confirmed by email. The Audience Award is separate from the 100 points. The result comes on December 20.")}
      <button type="button" class="btn btn-gold" id="vbtn">&#9733; {s("span", "Für diese Schule abstimmen", "Vote for this school")}</button>
      <form class="sp-form" id="vform" hidden novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <label>{s("span", "Deine E-Mail-Adresse", "Your email address")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {s("span", "Ja, schickt mir gelegentlich Neuigkeiten, Events und Angebote rund um Bachata per E-Mail. Abmeldung jederzeit möglich.", "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{s("span", "Stimme abschicken", "Send my vote")}</button>
        <small>{s("span", "Eine Stimme pro Person. Wir schicken dir einen Bestätigungslink. Deine E-Mail nutzen wir nur dafür und zum Entfernen doppelter Stimmen. Mehr in der <a href=\"/datenschutz.html\">Datenschutzerklärung</a>.", "One vote per person. We email you a confirmation link. We use your email only for that and to remove duplicate votes. More in the <a href=\"/datenschutz.html\">privacy policy</a>.")}</small>
      </form>
      <p class="sp-msg" id="vmsg" role="status" hidden></p>
    </div>
  </div>
</section>

<section class="block" aria-labelledby="rv-title">
  <div class="wrap sp-two">
    <div class="sp-card">
      <h2 id="rv-title">{s("span", "Bewertungen", "Reviews")}</h2>
      <div class="sp-sum" id="rvsum"></div>
      <div id="rvlist"></div>
    </div>
    <div class="sp-card">
      {s("h2", "Schreibe eine Bewertung", "Write a review")}
      {s("p", "Warst du in dieser Schule? Erzähle kurz, wie es war. Deine Bewertung erscheint, sobald du den Link in unserer E-Mail anklickst. Bitte bleib sachlich und fair.", "Have you been to this school? Tell us briefly how it was. Your review appears once you click the link in our email. Please stay factual and fair.")}
      <form class="sp-form" id="rvform" novalidate>
        <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
        <div role="radiogroup" aria-label="Sterne / Stars"><div class="sp-stars">
          <input type="radio" name="rating" value="5" id="st5"><label for="st5" title="5">★</label>
          <input type="radio" name="rating" value="4" id="st4"><label for="st4" title="4">★</label>
          <input type="radio" name="rating" value="3" id="st3"><label for="st3" title="3">★</label>
          <input type="radio" name="rating" value="2" id="st2"><label for="st2" title="2">★</label>
          <input type="radio" name="rating" value="1" id="st1"><label for="st1" title="1">★</label>
        </div></div>
        <label>{s("span", "Dein Name (freiwillig)", "Your name (optional)")}<input type="text" name="name" maxlength="40" autocomplete="nickname"></label>
        <label>{s("span", "Deine Bewertung (10 bis 600 Zeichen, keine Links)", "Your review (10 to 600 characters, no links)")}<textarea name="text" maxlength="600" required></textarea></label>
        <label>{s("span", "Deine E-Mail-Adresse (wird nicht veröffentlicht)", "Your email address (not published)")}<input type="email" name="email" required autocomplete="email" inputmode="email"></label>
        <label class="newsopt"><input type="checkbox" name="news" value="1"> {s("span", "Ja, schickt mir gelegentlich Neuigkeiten, Events und Angebote rund um Bachata per E-Mail. Abmeldung jederzeit möglich.", "Yes, send me occasional news, events and offers about Bachata by email. You can unsubscribe at any time.")}</label>
        <button type="submit" class="btn btn-gold">{s("span", "Bewertung abschicken", "Submit review")}</button>
        <small>{s("span", "Wir nutzen deine E-Mail nur zur Bestätigung. Eine Bewertung pro Person und Schule. Unpassende Bewertungen entfernen wir. Mehr in der <a href=\"/datenschutz.html\">Datenschutzerklärung</a>.", "We use your email only for confirmation. One review per person and school. We remove inappropriate reviews. More in the <a href=\"/datenschutz.html\">privacy policy</a>.")}</small>
      </form>
      <p class="sp-msg" id="rvmsg" role="status" hidden></p>
    </div>
  </div>
</section>

{kit_section(s, nm, de_city, e['slug'], e['city'])}
<section class="block alt" aria-labelledby="own-title">
  <div class="wrap">
    <div class="sp-card" style="max-width:760px">
      {s("h2", "Ist das deine Schule?", "Is this your school?").replace("<h2", '<h2 id="own-title"')}
      {s("p", "Du kannst deine Daten ergänzen oder korrigieren, zum Beispiel Festivals, Wettbewerbe und Gründungsjahr. Wenn du nicht im Ranking stehen möchtest, schreib uns kurz, dann entfernen wir deine Schule.", "You can add or correct your data, for example festivals, competitions and founding year. If you would rather not be listed, send us a short message and we will remove your school.")}
      <div class="sp-links"><a class="btn btn-gold" href="/bewerbung.html">{s("span", "Daten ergänzen oder korrigieren", "Add or correct my data")}</a><a class="btn btn-ghost" href="mailto:hello@latindanceawards.com?subject={__import__('urllib.parse', fromlist=['quote']).quote('Remove or correct: ' + nm)}">{s("span", "Schule entfernen lassen", "Remove my school")}</a></div>
    </div>
  </div>
</section>
'''
    title_de = f'{nm} · Bachata {de_city} · Bewertungen'
    desc_de = f'{nm} in {de_city}: Punkte, Platz {crank} im Zwischenstand des Bachata-Rankings, Bewertungen und Abstimmung für den Publikumspreis.'
    title_en = f'{nm} · Bachata {en_city} · Reviews'
    desc_en = f'{nm} in {en_city}: score, place {crank} in the interim Bachata ranking, reviews and voting for the Audience Award.'
    js = KIT_JS + SCHOOL_JS.replace('__SCHOOL__', json.dumps({'name': nm, 'city': de_city}, ensure_ascii=False)).replace('__EP__', re.search(r'var VOTE_ENDPOINT = "([^"]+)"', rank_js).group(1)) + '\n  initKit(document.querySelector(".kit"), ' + json.dumps(nm, ensure_ascii=False) + ', ' + json.dumps(de_city, ensure_ascii=False) + ', ' + json.dumps(e['slug']) + ');\n'
    schema = [crumbs(nm, f'schools/{e["slug"]}.html'), {"@context": "https://schema.org", "@type": "LocalBusiness", "name": nm, "url": e['url'],
              "address": {"@type": "PostalAddress", "addressLocality": de_city, "addressCountry": "DE"}}]
    page(f'schools/{e["slug"]}.html', title_de, desc_de, title_en, desc_en, f'schools/{e["slug"]}.html', main, s.en, js, schema=schema)

PAGE_CSS += SCHOOL_CSS
PAGE_CSS += KIT_CSS
os.makedirs(os.path.join(ROOT, 'schools'), exist_ok=True)
for _e in SCH: build_school(_e)
print('school pages:', len(SCH))

# ---- Share kit page for schools (not in sitemap, noindex)
_ts = T('sh')
_opts = ''.join(f'<option value="{e["slug"]}" data-n="{e["name"]}" data-c="{CITY_NAMES[e["city"]][0]}">{CITY_NAMES[e["city"]][0]}: {e["name"]}</option>'
                for e in sorted(SCH, key=lambda e: (CITY_NAMES[e['city']][0], e['name'])))
_main = f'''<section class="page-hero"><div class="wrap">
  {_ts("h1", "Teilen-Paket für Schulen", "Share kit for schools")}
  {_ts("p", "Wähle deine Schule. Du bekommst einen fertigen Text, deinen Abstimmungs-Link und ein Bild für Story oder Post. Alles ist kostenlos.", "Choose your school. You get a ready-made caption, your voting link and an image for your story or post. It is all free.", 'class="lead"')}
</div></section>
<section class="block"><div class="wrap"><div class="kit" id="share">{kit_body(_ts, True, _opts)}</div></div></section>'''
_js = KIT_JS + '''
  var _r=document.querySelector(".kit"),_sel=_r.querySelector(".kit-select");
  function _go(){var o=_sel.options[_sel.selectedIndex];initKit(_r,o.getAttribute("data-n"),o.getAttribute("data-c"),o.value);}
  var _q=(location.search.match(/[?&]s=([a-z0-9-]+)/)||[])[1];
  if(_q){for(var i=0;i<_sel.options.length;i++){if(_sel.options[i].value===_q){_sel.selectedIndex=i;break;}}}
  _sel.addEventListener("change",_go);_go();
'''
page('teilen.html', 'Teilen-Paket für Schulen · Latin Dance Awards', 'Fertiger Text und Bild für Instagram, Facebook und WhatsApp, damit deine Schüler für deine Schule abstimmen.',
     'Share kit for schools · Latin Dance Awards', 'A ready-made caption and image for Instagram, Facebook and WhatsApp so your students vote for your school.',
     'teilen.html', _main, _ts.en, _js, schema=[crumbs('Teilen-Paket', 'teilen.html')])
_f = os.path.join(ROOT, 'teilen.html'); _h = open(_f, encoding='utf-8').read()
open(_f, 'w', encoding='utf-8').write(_h.replace('<head>', '<head>\n<meta name="robots" content="noindex,follow">', 1))

# ======================================================================
# COMMUNITY PAGES: travel mode (reisen.html) + teachers and DJs (lehrer-djs.html)
# ======================================================================
# Fill in WhatsApp community invite links per city key (e.g. 'berlin': 'https://chat.whatsapp.com/XXXX'). Empty = "become admin" call to action.
WHATSAPP = {}
# Stripe Payment Link (or PayPal) for the verified badge. Empty = e-mail contact instead.
PROFILE_PAY_URL = ''
EP_URL = re.search(r'var VOTE_ENDPOINT = "([^"]+)"', rank_js).group(1)

COMM_CSS = r"""
.tp{max-width:860px}
.tp select,.tp input[type=text],.tp input[type=email],.tp input[type=url],.tp textarea{width:100%;padding:12px 14px;border-radius:12px;border:1px solid rgba(246,231,211,.35);background:#14100f;color:var(--cream);font:inherit}
.tp textarea{min-height:110px;resize:vertical}
.tp label{display:grid;gap:6px;font-size:14px;color:var(--muted)}
.tp .row2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.tp .box{border:1px solid var(--line);border-radius:20px;background:var(--card);padding:24px;margin-top:18px}
.tp .box h3{font-family:var(--serif);font-weight:500;font-size:22px;margin-bottom:10px}
.tp ol.top{list-style:none;display:grid;gap:10px;margin:0;padding:0}
.tp ol.top li{display:flex;align-items:center;gap:14px;padding:12px 14px;border-radius:14px;background:rgba(255,255,255,.04)}
.tp ol.top li b{font-family:var(--serif);color:var(--gold);font-size:20px;min-width:24px}
.tp ol.top li a{color:var(--cream);font-weight:600;text-decoration:none;flex:1}
.tp ol.top li span{color:var(--gold-light);font-size:14px}
.tp .btnrow{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.tp .btn-ghost{background:transparent!important;color:var(--cream)!important;border:1px solid var(--line)!important}
.tp .muted{color:var(--muted);font-size:14px;line-height:1.55}
.tp .filters{display:grid;grid-template-columns:1fr 1fr auto;gap:12px;align-items:end;margin-bottom:18px}
.tp .chk{display:flex!important;gap:10px;align-items:center;font-size:14px;color:var(--cream);padding-bottom:12px}
.tp .chk input{accent-color:#e4b95b;width:18px;height:18px}
.tp .people{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.tp .person{border:1px solid var(--line);border-radius:18px;background:var(--card);padding:18px}
.tp .person h3{font-family:var(--serif);font-weight:500;font-size:21px;margin:0 0 4px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.tp .person .meta{color:var(--gold);font-size:13px;margin-bottom:8px}
.tp .person p{color:var(--muted);font-size:14.5px;line-height:1.5;margin:0 0 10px}
.tp .person .soc{display:flex;flex-wrap:wrap;gap:8px}
.tp .person .soc a{padding:6px 12px;border-radius:999px;border:1px solid var(--line);font-size:13px;text-decoration:none;color:var(--cream)}
.tp .person .soc a:hover{border-color:var(--gold);color:var(--gold-light)}
.tp .vbadge{font-family:system-ui,sans-serif;font-size:11.5px;font-weight:700;letter-spacing:.04em;padding:3px 9px;border-radius:999px;background:var(--foil);color:#131011}
.tp .checks{display:flex;flex-wrap:wrap;gap:8px 18px}
.tp .checks label{display:flex;gap:8px;align-items:center;color:var(--cream)}
.tp .checks input{accent-color:#e4b95b}
.tp .consent{display:flex!important;gap:10px;align-items:flex-start;font-size:13px;line-height:1.45}
.tp .consent input{margin-top:3px;accent-color:#e4b95b}
@media (max-width:700px){.tp .row2,.tp .people,.tp .filters{grid-template-columns:1fr}}
"""
PAGE_CSS += COMM_CSS

import json as _json
_cities_sorted = sorted(CITY_NAMES.items(), key=lambda kv: kv[1][0].lower())
_copts = ''.join(f'<option value="{k}">{v[0]}</option>' for k, v in _cities_sorted)
_copts_n = ''.join(f'<option value="{v[0]}">{v[0]}</option>' for k, v in _cities_sorted)

# ---------- travel mode ----------
_tdata = {}
for _k, (_de, _en) in CITY_NAMES.items():
    _top = sorted([e for e in SCH if e['city'] == _k], key=lambda e: (-e['pts'], e['name']))[:3]
    _tdata[_k] = {'n': [_de, _en], 'top': [[e['name'], e['slug'], e['pts']] for e in _top], 'guide': _k in GUIDE_CITIES, 'wa': WHATSAPP.get(_k, '')}
_tr = T('tr')
_tmain = f"""<section class="page-hero"><div class="wrap" style="grid-template-columns:1fr">
  <div>
  {_tr("h1", "Tanzreise: Bachata, wo du gerade bist", "Dance trip: Bachata wherever you are")}
  {_tr("p", "Du bist übers Wochenende in einer anderen Stadt? Wähle die Stadt und sieh die Schulen mit dem aktuellen Zwischenstand, die Community und Lehrer und DJs vor Ort.", "Spending the weekend in another city? Choose the city and see the schools with the current interim score, the community and the teachers and DJs there.", 'class="lede"')}
  </div>
</div></section>
<section class="block"><div class="wrap tp">
  <label>{_tr("span", "Stadt wählen", "Choose a city")}<select id="tcity"><option value="">&#8211;</option>{_copts}</select></label>
  <div id="tres" hidden>
    <div class="box"><h3 id="tt1"></h3><ol class="top" id="ttop"></ol>
      <p class="muted" style="margin-top:10px">{_tr("span", "Zwischenstand mit sechs von neun Kriterien, nicht das Endergebnis. Das Ranking erscheint am 20. Dezember 2026.", "Interim score with six of nine factors, not the final result. The ranking is published on December 20, 2026.")}</p>
      <div class="btnrow"><a class="btn btn-gold" id="tguide" href="#">{_tr("span", "Alle Schulen der Stadt", "All schools in this city")}</a></div></div>
    <div class="box"><h3>{_tr("span", "Heute oder am Wochenende tanzen?", "Dancing tonight or this weekend?")}</h3>
      {_tr("p", "Socials und Übungsabende kündigen die Schulen auf ihren Websites und in Instagram an. Frag direkt nach, ob Gäste willkommen sind. Größere Veranstaltungen findest du bei Salsa Vida.", "Schools announce socials and practice nights on their websites and Instagram. Ask directly whether guests are welcome. You can find bigger events on Salsa Vida.", 'class="muted"')}
      <div class="btnrow"><a class="btn btn-ghost" href="https://www.salsavida.com/de/event/germany/" target="_blank" rel="noopener">{_tr("span", "Veranstaltungen bei Salsa Vida", "Events on Salsa Vida")}</a></div></div>
    <div class="box"><h3>{_tr("span", "Community vor Ort", "Local community")}</h3><div id="twa"></div></div>
    <div class="box"><h3>{_tr("span", "Lehrer und DJs vor Ort", "Teachers and DJs here")}</h3><div class="people" id="tpeople"></div>
      <p class="muted" id="tpnone" hidden>{_tr("span", "Noch keine Profile in dieser Stadt.", "No profiles in this city yet.")} <a href="lehrer-djs.html#anmelden">{_tr("span", "Eigenes Profil anlegen", "Create your profile")}</a></p></div>
  </div>
</div></section>"""
_tjs = r"""
  var TD=__TD__, EP="__EP__";
  var S={wa:["Der Community-Chat dieser Stadt auf WhatsApp. Bitte bleib respektvoll, keine Werbung ohne Absprache.","This city's community chat on WhatsApp. Please stay respectful, no advertising without agreement."],
    wab:["WhatsApp-Gruppe beitreten","Join the WhatsApp group"], none:["Für diese Stadt gibt es noch keine Gruppe. Du kennst die Szene und willst eine starten? Wir helfen dir dabei.","There is no group for this city yet. Do you know the scene and want to start one? We will help you."],
    nob:["Admin werden","Become an admin"], t:["Beste Schulen in ","Top schools in "], nos:["Noch keine Schulen erfasst.","No schools listed yet."], pts:["Punkte","points"], ver:["Verifiziert","Verified"]};
  function L(k){return S[k][window.LANG==="en"?1:0];}
  function esc(x){return String(x==null?"":x).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
  var sel=document.getElementById("tcity"),res=document.getElementById("tres");
  function render(){
    var k=sel.value; if(!k||!TD[k]){res.hidden=true;return;} res.hidden=false; var d=TD[k], en=window.LANG==="en", nm=d.n[en?1:0];
    document.getElementById("tt1").textContent=L("t")+nm;
    var ol=document.getElementById("ttop"); ol.innerHTML="";
    if(!d.top.length) ol.innerHTML="<li>"+esc(L("nos"))+"</li>";
    d.top.forEach(function(x,i){ ol.innerHTML+='<li><b>'+(i+1)+'</b><a href="schools/'+esc(x[1])+'.html">'+esc(x[0])+'</a><span>'+String(x[2]).replace(".",en?".":",")+' '+esc(L("pts"))+'</span></li>'; });
    document.getElementById("tguide").href=d.guide?("bachata-"+k+".html"):("rankings.html#"+k);
    var wa=document.getElementById("twa");
    if(d.wa&&/^https:\/\/chat\.whatsapp\.com\//.test(d.wa)) wa.innerHTML='<p class="muted">'+esc(L("wa"))+'</p><div class="btnrow"><a class="btn btn-gold" target="_blank" rel="noopener" href="'+esc(d.wa)+'">'+esc(L("wab"))+'</a></div>';
    else wa.innerHTML='<p class="muted">'+esc(L("none"))+'</p><div class="btnrow"><a class="btn btn-ghost" href="mailto:hello@latindanceawards.com?subject='+encodeURIComponent("WhatsApp "+d.n[0])+'">'+esc(L("nob"))+'</a></div>';
    loadPeople(k);
  }
  function loadPeople(k){
    var box=document.getElementById("tpeople"),none=document.getElementById("tpnone"); box.innerHTML=""; none.hidden=true;
    fetch(EP+"?action=profiles&city="+encodeURIComponent(TD[k].n[0])).then(function(r){return r.json();}).then(function(j){
      if(sel.value!==k) return; var a=j.items||[]; if(!a.length){none.hidden=false;return;}
      a.slice(0,6).forEach(function(p){ box.innerHTML+='<div class="person"><h3>'+esc(p.name)+(p.verified?' <span class="vbadge">&#10003; '+esc(L("ver"))+'</span>':'')+'</h3><div class="meta">'+esc(p.role)+'</div></div>'; });
    }).catch(function(){none.hidden=false;});
  }
  sel.addEventListener("change",function(){ try{history.replaceState(null,"","?c="+sel.value);}catch(e){} render(); });
  document.addEventListener("langchange",render);
  var q=(location.search.match(/[?&]c=([a-z0-9]+)/)||[])[1]; if(q&&TD[q]){sel.value=q;} render();
""".replace('__TD__', _json.dumps(_tdata, ensure_ascii=False)).replace('__EP__', EP_URL)
page('reisen.html', 'Tanzreise: Bachata in deiner Stadt finden · Latin Dance Awards',
     'Bachata unterwegs: Wähle eine Stadt und sieh Schulen mit Zwischenstand, Community-Gruppe sowie Lehrer und DJs vor Ort.',
     'Dance trip: find Bachata in any city · Latin Dance Awards',
     'Bachata on the road: choose a city and see schools with interim scores, the community group, plus teachers and DJs there.',
     'reisen.html', _tmain, _tr.en, _tjs, schema=[crumbs('Tanzreise', 'reisen.html')])

# ---------- teachers and DJs ----------
_tp = T('tp')
_pay = (f'<a class="btn btn-gold" href="{PROFILE_PAY_URL}" target="_blank" rel="noopener">' if PROFILE_PAY_URL else '<a class="btn btn-gold" href="mailto:hello@latindanceawards.com?subject=Profil%20verifizieren">') 
_pmain = f"""<section class="page-hero"><div class="wrap" style="grid-template-columns:1fr"><div>
  {_tp("h1", "Bachata-Lehrer und DJs in Deutschland", "Bachata teachers and DJs in Germany")}
  {_tp("p", "Finde Lehrer und DJs mit ihren Social-Media-Links. Du unterrichtest oder legst auf? Leg dein Profil kostenlos an. Mit der Verifizierung bekommst du das Häkchen.", "Find teachers and DJs with their social media links. Do you teach or DJ? Create your profile for free. Verification gets you the check mark.", 'class="lede"')}
  <div class="ctas"><a class="btn btn-gold" href="#anmelden">{_tp("span", "Profil anlegen", "Create a profile")}</a></div>
</div></div></section>
<section class="block"><div class="wrap tp">
  <div class="filters">
    <label>{_tp("span", "Stadt", "City")}<select id="pcity"><option value="">{_tp("span", "Alle Städte", "All cities")}</option>{_copts_n}</select></label>
    <label>{_tp("span", "Rolle", "Role")}<select id="prole"><option value="">{_tp("span", "Alle", "All")}</option><option value="teacher">{_tp("span", "Lehrer", "Teacher")}</option><option value="dj">DJ</option></select></label>
    <label class="chk"><input type="checkbox" id="pver"><span>{_tp("span", "Nur verifiziert", "Verified only")}</span></label>
  </div>
  <div class="people" id="plist"></div>
  <p class="muted" id="pnone" hidden>{_tp("span", "Noch keine Profile. Leg das erste an!", "No profiles yet. Create the first one!")}</p>
  <p class="muted" id="perr" hidden>{_tp("span", "Profile konnten nicht geladen werden.", "Profiles could not be loaded.")}</p>

  <div class="box" id="verify"><h3>{_tp("span", "Verifiziert für 5 € im Monat", "Verified for €5 a month")}</h3>
    {_tp("p", "Wir prüfen, dass du die Person hinter dem Profil bist und dass deine Social-Media-Links dir gehören. Dann zeigt dein Profil das Häkchen &#10003; Verifiziert. Jederzeit kündbar. Die Verifizierung ändert nichts am Ranking der Schulen, und Profile sind alphabetisch sortiert, nicht nach Zahlung.", "We check that you are the person behind the profile and that your social media links are yours. Your profile then shows the check mark &#10003; Verified. Cancel any time. Verification changes nothing about the school ranking, and profiles are sorted alphabetically, not by payment.", 'class="muted"')}
    <div class="btnrow">{_pay}{_tp("span", "Profil verifizieren", "Verify my profile")}</a></div></div>

  <div class="box" id="anmelden"><h3>{_tp("span", "Profil kostenlos anlegen", "Create your profile for free")}</h3>
    <form id="pform" novalidate style="display:grid;gap:14px">
      <input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
      <div class="row2"><label>{_tp("span", "Name oder Künstlername", "Name or stage name")}<input type="text" name="name" maxlength="60" required></label>
      <label>{_tp("span", "Rolle", "Role")}<select name="role"><option value="Lehrer">{_tp("span", "Lehrer", "Teacher")}</option><option value="DJ">DJ</option><option value="Lehrer und DJ">{_tp("span", "Lehrer und DJ", "Teacher and DJ")}</option></select></label></div>
      <div class="row2"><label>{_tp("span", "Stadt", "City")}<select name="city">{_copts}</select></label>
      <label>{_tp("span", "Schule (optional)", "School (optional)")}<input type="text" name="school" maxlength="80"></label></div>
      <div class="checks">{_tp("span", "Stile:", "Styles:")}<label><input type="checkbox" name="st" value="Dominicana"> Dominicana</label><label><input type="checkbox" name="st" value="Sensual"> Sensual</label><label><input type="checkbox" name="st" value="Moderna"> Moderna</label></div>
      <label>{_tp("span", "Kurzvorstellung (höchstens 300 Zeichen, ohne Links)", "Short bio (up to 300 characters, no links)")}<textarea name="bio" maxlength="300"></textarea></label>
      <div class="row2"><label>Instagram<input type="text" name="instagram" placeholder="@name" maxlength="100"></label><label>TikTok<input type="text" name="tiktok" placeholder="@name" maxlength="100"></label></div>
      <div class="row2"><label>YouTube<input type="url" name="youtube" placeholder="https://" maxlength="200"></label><label>Spotify / SoundCloud<input type="url" name="music" placeholder="https://" maxlength="200"></label></div>
      <label>Website<input type="url" name="website" placeholder="https://" maxlength="200"></label>
      <label>{_tp("span", "Deine E-Mail (wird nicht veröffentlicht)", "Your email (not published)")}<input type="email" name="email" maxlength="120" required></label>
      <label class="consent"><input type="checkbox" name="consent"><span>{_tp("span", "Ich bestätige, dass die Angaben von mir sind, und stimme zu, dass sie auf dieser Website öffentlich angezeigt werden. Ich kann die Löschung jederzeit per E-Mail verlangen.", "I confirm that the details are mine and I agree that they are shown publicly on this website. I can ask for deletion at any time by email.")}</span></label>
      <div class="btnrow"><button type="submit" class="btn btn-gold">{_tp("span", "Profil einreichen", "Submit profile")}</button></div>
      <p class="muted" id="pmsg" role="status" hidden></p>
    </form></div>
</div></section>"""
_pjs = r"""
  var EP="__EP__";
  var S={ver:["Verifiziert","Verified"],all:["Alle","All"],err:["Bitte Name, E-Mail und Zustimmung ausfüllen. Die Kurzvorstellung darf keine Links enthalten.","Please fill in name, email and consent. The bio must not contain links."],ok:["Danke! Wir prüfen dein Profil und schalten es danach frei.","Thank you! We will review your profile and then publish it."],fail:["Das hat nicht geklappt. Bitte versuche es noch einmal.","That did not work. Please try again."]};
  function L(k){return S[k][window.LANG==="en"?1:0];}
  function esc(x){return String(x==null?"":x).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
  var HOSTS=/^https:\/\/([a-z0-9-]+\.)*(instagram\.com|tiktok\.com|youtube\.com|youtu\.be|spotify\.com|soundcloud\.com|facebook\.com)(\/|$)/i;
  function safe(u,own){ u=String(u||""); return /^https:\/\//i.test(u)&&(own||HOSTS.test(u))?u:""; }
  var data=[],list=document.getElementById("plist");
  function draw(){
    var c=document.getElementById("pcity").value,r=document.getElementById("prole").value,v=document.getElementById("pver").checked;
    var a=data.filter(function(p){ if(c&&p.city!==c) return false; if(v&&!p.verified) return false;
      if(r==="teacher"&&!/Lehrer/.test(p.role)) return false; if(r==="dj"&&!/DJ/.test(p.role)) return false; return true; });
    list.innerHTML=""; document.getElementById("pnone").hidden=a.length>0||!!document.getElementById("perr").offsetParent;
    a.forEach(function(p){
      var soc=[["Instagram",p.instagram],["TikTok",p.tiktok],["YouTube",p.youtube],["Music",p.music]].map(function(x){var u=safe(x[1]);return u?'<a href="'+esc(u)+'" target="_blank" rel="noopener nofollow ugc">'+x[0]+'</a>':"";}).join("");
      var w=safe(p.website,true); if(w) soc+='<a href="'+esc(w)+'" target="_blank" rel="noopener nofollow ugc">Website</a>';
      list.innerHTML+='<article class="person"><h3>'+esc(p.name)+(p.verified?' <span class="vbadge">&#10003; '+esc(L("ver"))+'</span>':'')+'</h3><div class="meta">'+esc(p.role)+' · '+esc(p.city)+(p.school?' · '+esc(p.school):'')+(p.styles?' · '+esc(p.styles):'')+'</div>'+(p.bio?'<p>'+esc(p.bio)+'</p>':'')+'<div class="soc">'+soc+'</div></article>';
    });
  }
  fetch(EP+"?action=profiles").then(function(r){return r.json();}).then(function(j){ data=(j.items||[]).sort(function(a,b){return a.name.localeCompare(b.name);}); draw(); }).catch(function(){ document.getElementById("perr").hidden=false; });
  ["pcity","prole","pver"].forEach(function(id){ document.getElementById(id).addEventListener("change",draw); });
  document.addEventListener("langchange",draw);
  var f=document.getElementById("pform"),m=document.getElementById("pmsg"); var mailRe=/^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  f.addEventListener("submit",function(ev){ ev.preventDefault();
    var e=f.elements; if(!e.name.value.trim()||!mailRe.test(e.email.value.trim())||!e.consent.checked||/https?:|www\./i.test(e.bio.value)){ m.textContent=L("err"); m.hidden=false; return; }
    var st=[].slice.call(f.querySelectorAll("input[name=st]:checked")).map(function(x){return x.value;}).join(", ");
    var b=new URLSearchParams({action:"profile",name:e.name.value.trim(),role:e.role.value,city:e.city.options[e.city.selectedIndex].text,school:e.school.value.trim(),styles:st,bio:e.bio.value.trim(),instagram:e.instagram.value.trim(),tiktok:e.tiktok.value.trim(),youtube:e.youtube.value.trim(),music:e.music.value.trim(),website:e.website.value.trim(),email:e.email.value.trim(),hp:e.hp.value,language:window.LANG==="en"?"EN":"DE"});
    var btn=f.querySelector("button[type=submit]"); btn.disabled=true;
    fetch(EP,{method:"POST",mode:"no-cors",body:b}).then(function(){ f.reset(); m.textContent=L("ok"); m.hidden=false; }).catch(function(){ btn.disabled=false; m.textContent=L("fail"); m.hidden=false; });
  });
""".replace('__EP__', EP_URL)
page('lehrer-djs.html', 'Bachata-Lehrer und DJs in Deutschland · Latin Dance Awards',
     'Bachata-Lehrer und DJs in Deutschland mit Social-Media-Links. Kostenloses Profil, Verifizierung für 5 Euro im Monat.',
     'Bachata teachers and DJs in Germany · Latin Dance Awards',
     'Bachata teachers and DJs in Germany with social media links. Free profile, verification for 5 euros a month.',
     'lehrer-djs.html', _pmain, _tp.en, _pjs, schema=[crumbs('Lehrer und DJs', 'lehrer-djs.html')])
