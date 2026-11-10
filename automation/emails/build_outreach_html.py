"""Branded HTML version of the first-contact e-mail (11 languages, placeholders) + helper to personalise per school.
Run: python3 build_outreach_html.py  ->  outreach-html/outreach-<lang>.html"""
import os, re, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    import build_outreach as O
T = O.T
SERIF = "Georgia,'Times New Roman',serif"; SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
LAB = {  # free CTA, plans CTA, profile CTA, rank scope label
 'de': ('Daten kostenlos bestätigen', 'Pläne ansehen · ab 5 €', 'Mein Profil ansehen', 'in deinem Land'),
 'en': ('Confirm my details (free)', 'See plans · from €5', 'View my profile', 'in your country'),
 'es': ('Confirmar mis datos (gratis)', 'Ver planes · desde 5 €', 'Ver mi perfil', 'en tu país'),
 'fr': ('Confirmer mes infos (gratuit)', 'Voir les formules · dès 5 €', 'Voir mon profil', 'dans votre pays'),
 'it': ('Conferma i miei dati (gratis)', 'Vedi i piani · da 5 €', 'Vedi il mio profilo', 'nel tuo paese'),
 'pt': ('Confirmar os meus dados (grátis)', 'Ver planos · desde 5 €', 'Ver o meu perfil', 'no seu país'),
 'pl': ('Potwierdź dane (bezpłatnie)', 'Zobacz plany · od 5 €', 'Zobacz mój profil', 'w Twoim kraju'),
 'nl': ('Gegevens bevestigen (gratis)', 'Bekijk pakketten · vanaf € 5', 'Bekijk mijn profiel', 'in jouw land'),
 'tr': ('Bilgilerimi doğrula (ücretsiz)', 'Planları gör · 5 €’dan', 'Profilimi görüntüle', 'ülkenizde'),
 'ro': ('Confirmă datele (gratuit)', 'Vezi planurile · de la 5 €', 'Vezi profilul meu', 'în țara ta'),
 'el': ('Επιβεβαίωση στοιχείων (δωρεάν)', 'Δείτε τα πακέτα · από 5 €', 'Δείτε το προφίλ μου', 'στη χώρα σας')}
def paras(l):
    sub, body, sig, foot = T[l]
    ps = [p for p in body.split('\n\n')]
    clean = []
    for p in ps:
        p = re.sub(r'\n?https://latindanceawards\.com/\S+', '', p).strip()
        clean.append(p)
    return sub, clean, sig, foot
def render(l, name='{{School}}', city='{{City}}', rank='{{Rank}}', link='{{Profile link}}', greeting=None):
    sub, ps, sig, foot = paras(l)
    free, plans, prof, scope = LAB[l]
    hi, intro, data, paid, optout = ps[0], ps[1], ps[2].rstrip(':') + '.', ps[3].rstrip(':') + '.', ps[4]
    # intro: drop the profile-link placeholder line, keep the sentence
    intro = re.sub(r'\n?\{\{[^}]*\}\}\s*$', '', intro).rstrip(':').rstrip() + '.'
    intro = re.sub(r'\{\{(?:Schulname|School name|Nombre de la escuela|Nom de l’école|Nome della scuola|Nome da escola|Nazwa szkoły|Naam van de school|Okul adı|Numele școlii|Όνομα σχολής)\}\}', name, intro)
    intro = re.sub(r'\{\{(?:Stadt|City|Ciudad|Ville|Città|Cidade|Miasto|Stad|Şehir|Oraș|Πόλη)\}\}', city, intro)
    # rank phrase is shown on the card instead of inside the sentence
    intro = re.sub(r',? ?(?:auf Platz|at position|en el puesto|à la place|al posto|na posição|na miejscu|op plaats|sırada yer alıyor|pe locul|στη θέση) ?\{\{[^}]*\}\}[^.]*', '', intro)
    intro = re.sub(r'\{\{(?:Platz|Rank|Puesto|Place|Posizione|Posição|Miejsce|Plaats|Sıra|Loc|Θέση)\}\}\.?\s*sırada yer alıyor', '', intro)
    if l == 'tr': intro = intro.replace('zaten.', 'zaten yer alıyor.')
    intro = intro.replace('  ', ' ').replace(' .', '.').replace('..', '.')
    hi_txt = greeting if greeting is not None else re.sub(r' \{\{[^}]+\}\}([,:])', r'\1', hi)
    sig_h = sig.replace('\n', '<br>')
    foot_h = re.sub(r'(https://\S+)', r'<a href="\1" style="color:#E4B95B">\1</a>', foot)
    card = (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:22px 0"><tr><td bgcolor="#1b1612" style="background:#1b1612;border:1px solid #6b5522;border-radius:16px;padding:18px 20px">'
      f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td width="64" valign="middle"><table role="presentation" cellpadding="0" cellspacing="0"><tr><td width="52" height="52" align="center" valign="middle" bgcolor="#E4B95B" style="background:#E4B95B;border-radius:26px;color:#131011;font:600 22px {SERIF}">{rank}</td></tr></table></td>'
      f'<td valign="middle"><div style="font:500 20px/1.25 {SERIF};color:#F6E7D3">{name}</div><div style="font:14px/1.5 {SANS};color:#b9aa98">{city} · {scope}</div></td></tr></table>'
      f'<div style="margin-top:12px"><a href="{link}" style="font:600 14px {SANS};color:#F8E2A6;text-decoration:underline">{prof}</a></div></td></tr></table>')
    def btn(label, href, gold):
        if gold: return f'<td bgcolor="#E4B95B" style="background:#E4B95B;border-radius:999px"><a href="{href}" style="display:inline-block;padding:14px 26px;font:700 15px {SANS};color:#131011;text-decoration:none">{label}</a></td>'
        return f'<td style="border:1px solid #8a7440;border-radius:999px"><a href="{href}" style="display:inline-block;padding:13px 24px;font:700 15px {SANS};color:#F6E7D3;text-decoration:none">{label}</a></td>'
    P = lambda t, c='#F6E7D3', sz=16: f'<p style="margin:0 0 16px;font:{sz}px/1.6 {SANS};color:{c}">{t}</p>'
    return f'''<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>{sub}</title></head>
<body style="margin:0;padding:0;background:#080707">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#080707"><tr><td align="center" style="padding:28px 14px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%">
<tr><td align="center" style="padding:6px 0 26px"><div style="font:600 26px {SERIF};color:#F6E7D3;letter-spacing:.5px">&#9733;&nbsp; Latin Dance</div><div style="font:700 11px {SANS};letter-spacing:.55em;color:#E4B95B;margin-top:6px;padding-left:.55em">AWARDS</div></td></tr>
<tr><td bgcolor="#131011" style="background:#131011;border:1px solid #6b5522;border-radius:22px;padding:32px 28px">
<p style="margin:0 0 14px;font:500 22px/1.25 {SERIF};color:#F8E2A6">{hi_txt}</p>
{P(intro)}
{card}
{P(data)}
<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 24px"><tr>{btn(free, 'https://latindanceawards.com/bewerbung', True)}</tr></table>
{P(paid)}
<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 26px"><tr>{btn(plans, 'https://latindanceawards.com/preise', False)}</tr></table>
{P(optout, '#b9aa98', 14)}
<p style="margin:22px 0 0;font:16px/1.6 {SANS};color:#F6E7D3">{sig_h}</p>
</td></tr>
<tr><td align="center" style="padding:22px 10px 0;font:12px/1.6 {SANS};color:#8a7d6c">{foot_h}</td></tr>
</table></td></tr></table></body></html>'''
if __name__ == '__main__':
    out = os.path.join(HERE, 'outreach-html'); os.makedirs(out, exist_ok=True)
    for l in T:
        open(os.path.join(out, f'outreach-{l}.html'), 'w', encoding='utf-8').write(render(l, '{{School name}}', '{{City}}', '{{Rank}}', '{{Profile link}}'))
    print(len(T), 'languages')
