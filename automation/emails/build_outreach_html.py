"""Branded HTML version of the first-contact e-mail (11 languages, placeholders) + helper to personalise per school.
Run: python3 build_outreach_html.py  ->  outreach-html/outreach-<lang>.html"""
import os, re, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    import build_outreach as O
T = O.T
SERIF = "Fraunces,Georgia,'Times New Roman',serif"; SANS = "Inter,Helvetica,Arial,sans-serif"
FOIL = "linear-gradient(100deg,#A87424 0%,#F8E2A6 28%,#E4B95B 45%,#FFF1C9 55%,#C8952E 75%,#F2D27A 100%)"
ASSET = "https://latindanceawards.com/email-assets/"
FONTCSS = ('@font-face{font-family:Fraunces;font-weight:400 500;src:url(https://latindanceawards.com/fonts/fraunces-regular.woff) format("woff")}'
           '@font-face{font-family:Inter;font-weight:400;src:url(https://latindanceawards.com/fonts/inter-400.woff) format("woff")}'
           '@font-face{font-family:Inter;font-weight:600;src:url(https://latindanceawards.com/fonts/inter-600.woff) format("woff")}'
           '@font-face{font-family:Inter;font-weight:700;src:url(https://latindanceawards.com/fonts/inter-700.woff) format("woff")}')
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
PRICE = {
 'de': ('Pläne ab 5 € im Monat', 'Probestunde-Button, Fotos, Videos und das Häkchen „geprüft“ für deine Schule. Jederzeit kündbar.'),
 'en': ('Plans from €5 a month', 'A trial-class button, photos, videos and the verified check mark for your school. Cancel anytime.'),
 'es': ('Planes desde 5 € al mes', 'Botón de clase de prueba, fotos, vídeos y el sello de escuela verificada. Cancela cuando quieras.'),
 'fr': ('Formules à partir de 5 € par mois', 'Bouton de cours d’essai, photos, vidéos et badge « école vérifiée » pour votre école. Résiliable à tout moment.'),
 'it': ('Piani da 5 € al mese', 'Pulsante per la lezione di prova, foto, video e il segno di scuola verificata. Disdici quando vuoi.'),
 'pt': ('Planos desde 5 € por mês', 'Botão de aula experimental, fotografias, vídeos e o selo de escola verificada. Cancele quando quiser.'),
 'pl': ('Plany od 5 € miesięcznie', 'Przycisk zajęć próbnych, zdjęcia, filmy i znacznik zweryfikowanej szkoły. Rezygnacja w każdej chwili.'),
 'nl': ('Pakketten vanaf € 5 per maand', 'Proefles-knop, foto’s, video’s en het vinkje voor gecontroleerde school. Altijd opzegbaar.'),
 'tr': ('Ayda 5 €’dan başlayan planlar', 'Deneme dersi düğmesi, fotoğraflar, videolar ve doğrulanmış okul işareti. İstediğiniz zaman iptal edin.'),
 'ro': ('Planuri de la 5 € pe lună', 'Buton pentru lecția de probă, fotografii, videoclipuri și semnul de școală verificată. Anulezi oricând.'),
 'el': ('Πακέτα από 5 € τον μήνα', 'Κουμπί δοκιμαστικού μαθήματος, φωτογραφίες, βίντεο και σήμα επαληθευμένης σχολής. Ακύρωση οποιαδήποτε στιγμή.')}
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
    card = (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:22px 0"><tr><td bgcolor="#1b1612" style="background:#1b1612;background-image:radial-gradient(120% 140% at 0 0,rgba(228,185,91,.20),#1b1612 62%);border:1.5px solid #8a7440;border-radius:18px;padding:18px 20px">'
      f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td width="96" valign="middle"><img src="{ASSET}seal.png" width="84" height="84" alt="" style="display:block;border:0"></td>'
      f'<td valign="middle"><div style="font:600 13px {SANS};color:#F8E2A6">#{rank} {scope}</div><div style="font:500 22px/1.2 {SERIF};color:#F6E7D3;margin-top:3px">{name}</div><div style="font:14px/1.5 {SANS};color:#b9aa98;margin-top:2px">{city}</div></td></tr></table>'
      f'<div style="margin-top:12px"><a href="{link}" style="font:600 14px {SANS};color:#F8E2A6;text-decoration:underline">{prof}</a></div></td></tr></table>')
    def btn(label, href, gold):
        if gold: return f'<td bgcolor="#E4B95B" style="background:#E4B95B;background-image:{FOIL};border-radius:999px"><a href="{href}" style="display:inline-block;padding:15px 28px;font:700 15px {SANS};color:#131011;text-decoration:none">{label}</a></td>'
        return f'<td style="border:1px solid #8a7440;border-radius:999px"><a href="{href}" style="display:inline-block;padding:13px 24px;font:700 15px {SANS};color:#F6E7D3;text-decoration:none">{label}</a></td>'
    P = lambda t, c='#F6E7D3', sz=16: f'<p style="margin:0 0 16px;font:{sz}px/1.6 {SANS};color:{c}">{t}</p>'
    return f'''<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><style>{FONTCSS}</style><title>{sub}</title></head>
<body style="margin:0;padding:0;background:#080707">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#080707"><tr><td align="center" style="padding:28px 14px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%">
<tr><td align="center" style="padding:0 0 18px"><a href="https://latindanceawards.com"><img src="{ASSET}email-header.png" width="300" height="75" alt="Latin Dance Awards" style="display:block;border:0;font:600 22px {SERIF};color:#F6E7D3"></a></td></tr>
<tr><td bgcolor="#131011" style="background:#131011;background-image:radial-gradient(90% 70% at 85% 0,rgba(228,185,91,.14),#131011 60%);border:1.5px solid #8a7440;border-radius:24px;padding:34px 30px">
<p style="margin:0 0 14px;font:500 22px/1.25 {SERIF};color:#F8E2A6">{hi_txt}</p>
{P(intro)}
{card}
<p style="margin:0 0 6px;font:500 32px/1.15 {SERIF};color:#F8E2A6">{PRICE[l][0]}</p>
{P(PRICE[l][1])}
<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 26px"><tr>{btn(plans, 'https://latindanceawards.com/preise', True)}</tr></table>
{P(data)}
<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 26px"><tr>{btn(free, 'https://latindanceawards.com/bewerbung', False)}</tr></table>
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
