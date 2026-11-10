"""Builds the welcome e-mails (HTML + plain text) in 11 languages. Run: python3 build_welcome.py"""
import re, os
HERE = os.path.dirname(os.path.abspath(__file__))
SERIF = "Georgia,'Times New Roman',serif"; SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
FOOT = '<br><a href="https://latindanceawards.com" style="color:#E4B95B">latindanceawards.com</a>'
def L(**k): return k
T = {}
T['de'] = L(subject='Willkommen bei Latin Dance Awards: so geht es jetzt weiter', pre='Danke für deinen Plan! Das brauchen wir jetzt von dir.',
 hi='Hallo {{Vorname}},', p1='danke, dass <b>{{Schulname}}</b> jetzt den Plan <b>{{Plan}}</b> hat. Wir freuen uns sehr, dass deine Schule dabei ist.',
 h2='Das brauchen wir jetzt von dir', sub='Antworte einfach auf diese E-Mail, am besten mit allem auf einmal. Fehlt etwas, ergänzen wir es später.',
 items=['<b>Fotos</b>: bis zu 6, gern in hoher Qualität (Logo und Fotos aus dem Unterricht).','<b>Videos</b>: bis zu 3 Links, zum Beispiel von YouTube oder Instagram.','<b>Kurszeiten und Preise</b>: so, wie du sie anzeigen möchtest.','<b>Probestunde</b>: deine WhatsApp-Nummer oder E-Mail-Adresse für die Buchungen.','<b>Social Media</b>: Links zu Instagram, Facebook, TikTok und deiner Website.','<b>Lehrer</b> (optional): Name und Foto.','<b>Eigene Events</b> (optional): Name, Datum, Ort und Link.'],
 proof='Damit nur die Inhaber Daten ändern können, antworte bitte von der E-Mail-Adresse deiner Schule oder nenne uns den Instagram-Account der Schule.',
 next_h='Wie es weitergeht', next='Wir richten alles von Hand ein und melden uns, sobald dein Profil freigeschaltet ist. Das dauert in der Regel höchstens ein paar Tage.',
 cancel='Du kannst jederzeit kündigen: Den Link zur Verwaltung deines Abos findest du in der Quittung von Stripe.', btn='Mein Schulprofil ansehen',
 sig='Herzliche Grüße<br>Mateus<br>Latin Dance Awards', foot='Latin Dance Awards · unabhängiges Ranking für Latin-Dance-Schulen in Europa', plink='{{Profil-Link}}')
T['en'] = L(subject='Welcome to Latin Dance Awards: what happens next', pre='Thanks for your plan! Here is what we need from you.',
 hi='Hi {{First name}},', p1='thank you for putting <b>{{School name}}</b> on the <b>{{Plan}}</b> plan. We are really happy to have your school with us.',
 h2='What we need from you', sub='Just reply to this email, ideally with everything at once. If something is missing, we can add it later.',
 items=['<b>Photos</b>: up to 6, high quality if possible (logo and photos from class).','<b>Videos</b>: up to 3 links, for example from YouTube or Instagram.','<b>Class times and prices</b>: the way you want them shown.','<b>Trial class</b>: your WhatsApp number or email address for bookings.','<b>Social media</b>: links to Instagram, Facebook, TikTok and your website.','<b>Teachers</b> (optional): name and photo.','<b>Your own events</b> (optional): name, date, place and link.'],
 proof='So that only owners can change the data, please reply from your school’s email address or tell us the school’s Instagram account.',
 next_h='What happens next', next='We set everything up by hand and will let you know as soon as your profile is live. This usually takes a few days at most.',
 cancel='You can cancel at any time: the link to manage your subscription is in your Stripe receipt.', btn='View my school profile',
 sig='Warm regards<br>Mateus<br>Latin Dance Awards', foot='Latin Dance Awards · independent ranking of Latin dance schools in Europe', plink='{{Profile link}}')
T['es'] = L(subject='Te damos la bienvenida a Latin Dance Awards: los próximos pasos', pre='¡Gracias por tu plan! Esto es lo que necesitamos de ti.',
 hi='Hola {{Nombre}}:', p1='gracias por activar el plan <b>{{Plan}}</b> para <b>{{Nombre de la escuela}}</b>. Nos alegra mucho tener a tu escuela con nosotros.',
 h2='Lo que necesitamos de ti', sub='Responde a este correo, a ser posible con todo a la vez. Si falta algo, lo añadimos más tarde.',
 items=['<b>Fotos</b>: hasta 6, mejor en alta calidad (logotipo y fotos de las clases).','<b>Vídeos</b>: hasta 3 enlaces, por ejemplo de YouTube o Instagram.','<b>Horarios y precios</b>: tal como quieres que se muestren.','<b>Clase de prueba</b>: tu número de WhatsApp o tu correo para las reservas.','<b>Redes sociales</b>: enlaces a Instagram, Facebook, TikTok y tu web.','<b>Profesores</b> (opcional): nombre y foto.','<b>Tus propios eventos</b> (opcional): nombre, fecha, lugar y enlace.'],
 proof='Para que solo los responsables puedan cambiar los datos, responde desde el correo de tu escuela o indícanos la cuenta de Instagram de la escuela.',
 next_h='Qué pasa ahora', next='Lo configuramos todo a mano y te avisamos en cuanto tu perfil esté publicado. Normalmente tarda unos pocos días como máximo.',
 cancel='Puedes cancelar en cualquier momento: el enlace para gestionar tu suscripción está en el recibo de Stripe.', btn='Ver el perfil de mi escuela',
 sig='Un saludo cordial<br>Mateus<br>Latin Dance Awards', foot='Latin Dance Awards · ranking independiente de escuelas de baile latino en Europa', plink='{{Enlace al perfil}}')
T['fr'] = L(subject='Bienvenue chez Latin Dance Awards : la suite', pre='Merci pour votre formule ! Voici ce dont nous avons besoin.',
 hi='Bonjour {{Prénom}},', p1='merci d’avoir choisi la formule <b>{{Formule}}</b> pour <b>{{Nom de l’école}}</b>. Nous sommes ravis de vous compter parmi nous.',
 h2='Ce dont nous avons besoin', sub='Répondez simplement à cet e-mail, de préférence avec tout en une fois. S’il manque quelque chose, nous l’ajouterons plus tard.',
 items=['<b>Photos</b> : jusqu’à 6, de préférence en haute qualité (logo et photos des cours).','<b>Vidéos</b> : jusqu’à 3 liens, par exemple YouTube ou Instagram.','<b>Horaires et tarifs</b> : tels que vous souhaitez les afficher.','<b>Cours d’essai</b> : votre numéro WhatsApp ou votre e-mail pour les réservations.','<b>Réseaux sociaux</b> : liens vers Instagram, Facebook, TikTok et votre site.','<b>Professeurs</b> (facultatif) : nom et photo.','<b>Vos propres événements</b> (facultatif) : nom, date, lieu et lien.'],
 proof='Pour que seuls les responsables puissent modifier les données, répondez depuis l’adresse e-mail de votre école ou indiquez-nous le compte Instagram de l’école.',
 next_h='La suite', next='Nous mettons tout en place à la main et vous prévenons dès que votre profil est en ligne. Cela prend en général quelques jours au maximum.',
 cancel='Vous pouvez résilier à tout moment : le lien pour gérer votre abonnement se trouve dans le reçu Stripe.', btn='Voir le profil de mon école',
 sig='Cordialement<br>Mateus<br>Latin Dance Awards', foot='Latin Dance Awards · classement indépendant des écoles de danses latines en Europe', plink='{{Lien du profil}}')
T['it'] = L(subject='Benvenuto in Latin Dance Awards: cosa succede ora', pre='Grazie per il tuo piano! Ecco cosa ci serve da te.',
 hi='Ciao {{Nome}},', p1='grazie per aver attivato il piano <b>{{Piano}}</b> per <b>{{Nome della scuola}}</b>. Siamo felici di avere la tua scuola con noi.',
 h2='Cosa ci serve da te', sub='Rispondi semplicemente a questa e-mail, possibilmente con tutto insieme. Se manca qualcosa, lo aggiungiamo più avanti.',
 items=['<b>Foto</b>: fino a 6, meglio in alta qualità (logo e foto delle lezioni).','<b>Video</b>: fino a 3 link, ad esempio da YouTube o Instagram.','<b>Orari e prezzi</b>: come vuoi che vengano mostrati.','<b>Lezione di prova</b>: il tuo numero WhatsApp o il tuo indirizzo e-mail per le prenotazioni.','<b>Social media</b>: link a Instagram, Facebook, TikTok e al tuo sito.','<b>Insegnanti</b> (facoltativo): nome e foto.','<b>I tuoi eventi</b> (facoltativo): nome, data, luogo e link.'],
 proof='Perché solo i titolari possano modificare i dati, rispondi dall’indirizzo e-mail della tua scuola oppure indicaci l’account Instagram della scuola.',
 next_h='Cosa succede ora', next='Configuriamo tutto a mano e ti avvisiamo appena il tuo profilo è online. Di solito bastano al massimo pochi giorni.',
 cancel='Puoi disdire in qualsiasi momento: il link per gestire l’abbonamento si trova nella ricevuta di Stripe.', btn='Vedi il profilo della mia scuola',
 sig='Cordiali saluti<br>Mateus<br>Latin Dance Awards', foot='Latin Dance Awards · classifica indipendente delle scuole di ballo latino in Europa', plink='{{Link al profilo}}')
T['pt'] = L(subject='Bem-vindo ao Latin Dance Awards: o que acontece agora', pre='Obrigado pelo seu plano! É isto que precisamos de si.',
 hi='Olá {{Nome}},', p1='obrigado por ativar o plano <b>{{Plano}}</b> para <b>{{Nome da escola}}</b>. Estamos muito contentes por ter a sua escola connosco.',
 h2='O que precisamos de si', sub='Basta responder a este e-mail, de preferência com tudo de uma vez. Se faltar alguma coisa, acrescentamos mais tarde.',
 items=['<b>Fotografias</b>: até 6, de preferência em alta qualidade (logótipo e fotos das aulas).','<b>Vídeos</b>: até 3 ligações, por exemplo do YouTube ou do Instagram.','<b>Horários e preços</b>: como quer que sejam apresentados.','<b>Aula experimental</b>: o seu número de WhatsApp ou e-mail para as marcações.','<b>Redes sociais</b>: ligações para Instagram, Facebook, TikTok e o seu site.','<b>Professores</b> (opcional): nome e fotografia.','<b>Os seus eventos</b> (opcional): nome, data, local e ligação.'],
 proof='Para que só os responsáveis possam alterar os dados, responda a partir do e-mail da sua escola ou indique-nos a conta de Instagram da escola.',
 next_h='O que acontece a seguir', next='Configuramos tudo à mão e avisamos assim que o seu perfil estiver publicado. Normalmente demora, no máximo, alguns dias.',
 cancel='Pode cancelar a qualquer momento: a ligação para gerir a subscrição está no recibo do Stripe.', btn='Ver o perfil da minha escola',
 sig='Com os melhores cumprimentos<br>Mateus<br>Latin Dance Awards', foot='Latin Dance Awards · ranking independente de escolas de dança latina na Europa', plink='{{Ligação do perfil}}')
T['pl'] = L(subject='Witamy w Latin Dance Awards: co dalej', pre='Dziękujemy za wybór planu! Oto, czego od Ciebie potrzebujemy.',
 hi='Cześć {{Imię}},', p1='dziękujemy za aktywację planu <b>{{Plan}}</b> dla <b>{{Nazwa szkoły}}</b>. Bardzo się cieszymy, że Twoja szkoła jest z nami.',
 h2='Czego od Ciebie potrzebujemy', sub='Wystarczy odpowiedzieć na tę wiadomość, najlepiej wysyłając wszystko naraz. Jeśli czegoś zabraknie, uzupełnimy to później.',
 items=['<b>Zdjęcia</b>: do 6, najlepiej w wysokiej jakości (logo i zdjęcia z zajęć).','<b>Filmy</b>: do 3 linków, na przykład z YouTube lub Instagrama.','<b>Godziny zajęć i ceny</b>: tak, jak chcesz je pokazać.','<b>Zajęcia próbne</b>: Twój numer WhatsApp lub adres e-mail do rezerwacji.','<b>Media społecznościowe</b>: linki do Instagrama, Facebooka, TikToka i Twojej strony.','<b>Nauczyciele</b> (opcjonalnie): imię i zdjęcie.','<b>Własne wydarzenia</b> (opcjonalnie): nazwa, data, miejsce i link.'],
 proof='Aby dane mogli zmieniać tylko właściciele, odpowiedz z adresu e-mail szkoły albo podaj nam konto szkoły na Instagramie.',
 next_h='Co dalej', next='Wszystko ustawiamy ręcznie i damy znać, gdy Twój profil zostanie opublikowany. Zwykle trwa to maksymalnie kilka dni.',
 cancel='Możesz zrezygnować w każdej chwili: link do zarządzania subskrypcją znajdziesz w potwierdzeniu płatności od Stripe.', btn='Zobacz profil mojej szkoły',
 sig='Pozdrawiamy serdecznie<br>Mateus<br>Latin Dance Awards', foot='Latin Dance Awards · niezależny ranking szkół tańców latynoamerykańskich w Europie', plink='{{Link do profilu}}')
T['nl'] = L(subject='Welkom bij Latin Dance Awards: dit gebeurt er nu', pre='Bedankt voor je abonnement! Dit hebben we van je nodig.',
 hi='Hallo {{Voornaam}},', p1='bedankt dat <b>{{Naam van de school}}</b> nu het pakket <b>{{Pakket}}</b> heeft. We zijn blij dat jouw school erbij is.',
 h2='Dit hebben we van je nodig', sub='Antwoord gewoon op deze e-mail, het liefst met alles in één keer. Ontbreekt er iets, dan vullen we dat later aan.',
 items=['<b>Foto’s</b>: maximaal 6, bij voorkeur in hoge kwaliteit (logo en foto’s van de lessen).','<b>Video’s</b>: maximaal 3 links, bijvoorbeeld van YouTube of Instagram.','<b>Lestijden en prijzen</b>: zoals je ze wilt laten zien.','<b>Proefles</b>: je WhatsApp-nummer of e-mailadres voor reserveringen.','<b>Social media</b>: links naar Instagram, Facebook, TikTok en je website.','<b>Docenten</b> (optioneel): naam en foto.','<b>Eigen evenementen</b> (optioneel): naam, datum, plaats en link.'],
 proof='Zodat alleen eigenaren gegevens kunnen wijzigen, antwoord je vanaf het e-mailadres van je school of geef je ons het Instagram-account van de school door.',
 next_h='Hoe het verdergaat', next='We richten alles met de hand in en laten het je weten zodra je profiel online staat. Dat duurt meestal hooguit een paar dagen.',
 cancel='Je kunt altijd opzeggen: de link om je abonnement te beheren staat in je Stripe-ontvangstbewijs.', btn='Bekijk het profiel van mijn school',
 sig='Met vriendelijke groet<br>Mateus<br>Latin Dance Awards', foot='Latin Dance Awards · onafhankelijke ranglijst van Latin-dansscholen in Europa', plink='{{Profiellink}}')
T['tr'] = L(subject='Latin Dance Awards’a hoş geldiniz: sırada ne var', pre='Planınız için teşekkürler! Sizden şunlara ihtiyacımız var.',
 hi='Merhaba {{Ad}},', p1='<b>{{Okul adı}}</b> için <b>{{Plan}}</b> planını seçtiğiniz için teşekkür ederiz. Okulunuzun aramızda olmasından çok memnunuz.',
 h2='Sizden neye ihtiyacımız var', sub='Bu e-postayı yanıtlamanız yeterli, mümkünse her şeyi tek seferde gönderin. Eksik olan bir şey olursa sonra ekleriz.',
 items=['<b>Fotoğraflar</b>: en fazla 6, mümkünse yüksek kalitede (logo ve ders fotoğrafları).','<b>Videolar</b>: en fazla 3 bağlantı, örneğin YouTube veya Instagram.','<b>Ders saatleri ve fiyatlar</b>: göstermek istediğiniz şekilde.','<b>Deneme dersi</b>: rezervasyonlar için WhatsApp numaranız veya e-posta adresiniz.','<b>Sosyal medya</b>: Instagram, Facebook, TikTok ve web sitenizin bağlantıları.','<b>Öğretmenler</b> (isteğe bağlı): ad ve fotoğraf.','<b>Kendi etkinlikleriniz</b> (isteğe bağlı): ad, tarih, yer ve bağlantı.'],
 proof='Verileri yalnızca okul sahiplerinin değiştirebilmesi için lütfen okulunuzun e-posta adresinden yanıtlayın veya bize okulun Instagram hesabını bildirin.',
 next_h='Sırada ne var', next='Her şeyi elle ayarlıyoruz ve profiliniz yayına girer girmez size haber veriyoruz. Bu genellikle en fazla birkaç gün sürer.',
 cancel='İstediğiniz zaman iptal edebilirsiniz: aboneliğinizi yönetme bağlantısı Stripe makbuzunda yer alır.', btn='Okul profilimi görüntüle',
 sig='Saygılarımızla<br>Mateus<br>Latin Dance Awards', foot='Latin Dance Awards · Avrupa’daki Latin dans okulları için bağımsız sıralama', plink='{{Profil bağlantısı}}')
T['ro'] = L(subject='Bun venit la Latin Dance Awards: ce urmează', pre='Mulțumim pentru plan! Iată de ce avem nevoie de la tine.',
 hi='Bună {{Prenume}},', p1='îți mulțumim că ai ales planul <b>{{Plan}}</b> pentru <b>{{Numele școlii}}</b>. Ne bucurăm foarte mult că școala ta este alături de noi.',
 h2='De ce avem nevoie de la tine', sub='Răspunde pur și simplu la acest e-mail, de preferat cu toate informațiile deodată. Dacă lipsește ceva, completăm mai târziu.',
 items=['<b>Fotografii</b>: până la 6, de preferat de înaltă calitate (siglă și fotografii de la cursuri).','<b>Videoclipuri</b>: până la 3 linkuri, de exemplu de pe YouTube sau Instagram.','<b>Orarul și prețurile</b>: așa cum vrei să fie afișate.','<b>Lecție de probă</b>: numărul tău de WhatsApp sau adresa de e-mail pentru rezervări.','<b>Rețele sociale</b>: linkuri către Instagram, Facebook, TikTok și site-ul tău.','<b>Profesori</b> (opțional): nume și fotografie.','<b>Evenimentele tale</b> (opțional): nume, dată, loc și link.'],
 proof='Pentru ca doar proprietarii să poată modifica datele, răspunde de pe adresa de e-mail a școlii sau spune-ne contul de Instagram al școlii.',
 next_h='Ce urmează', next='Configurăm totul manual și te anunțăm imediat ce profilul tău este publicat. De obicei durează cel mult câteva zile.',
 cancel='Poți anula oricând: linkul pentru gestionarea abonamentului se află în chitanța de la Stripe.', btn='Vezi profilul școlii mele',
 sig='Cu drag<br>Mateus<br>Latin Dance Awards', foot='Latin Dance Awards · clasament independent al școlilor de dans latino din Europa', plink='{{Link profil}}')
T['el'] = L(subject='Καλώς ήρθατε στο Latin Dance Awards: τα επόμενα βήματα', pre='Ευχαριστούμε για το πακέτο σας! Να τι χρειαζόμαστε από εσάς.',
 hi='Γεια σας {{Όνομα}},', p1='ευχαριστούμε που επιλέξατε το πακέτο <b>{{Πακέτο}}</b> για τη σχολή <b>{{Όνομα σχολής}}</b>. Χαιρόμαστε πολύ που η σχολή σας είναι μαζί μας.',
 h2='Τι χρειαζόμαστε από εσάς', sub='Απαντήστε απλώς σε αυτό το e-mail, κατά προτίμηση με όλα μαζί. Αν λείπει κάτι, θα το προσθέσουμε αργότερα.',
 items=['<b>Φωτογραφίες</b>: έως 6, κατά προτίμηση σε υψηλή ποιότητα (λογότυπο και φωτογραφίες από τα μαθήματα).','<b>Βίντεο</b>: έως 3 σύνδεσμοι, για παράδειγμα από YouTube ή Instagram.','<b>Ωράρια και τιμές</b>: όπως θέλετε να εμφανίζονται.','<b>Δοκιμαστικό μάθημα</b>: ο αριθμός WhatsApp ή η διεύθυνση e-mail σας για κρατήσεις.','<b>Κοινωνικά δίκτυα</b>: σύνδεσμοι για Instagram, Facebook, TikTok και την ιστοσελίδα σας.','<b>Δάσκαλοι</b> (προαιρετικά): όνομα και φωτογραφία.','<b>Δικές σας εκδηλώσεις</b> (προαιρετικά): όνομα, ημερομηνία, τόπος και σύνδεσμος.'],
 proof='Για να μπορούν να αλλάζουν τα στοιχεία μόνο οι ιδιοκτήτες, απαντήστε από τη διεύθυνση e-mail της σχολής σας ή πείτε μας τον λογαριασμό της σχολής στο Instagram.',
 next_h='Τι ακολουθεί', next='Τα ρυθμίζουμε όλα χειροκίνητα και σας ενημερώνουμε μόλις το προφίλ σας γίνει ορατό. Συνήθως χρειάζονται το πολύ λίγες ημέρες.',
 cancel='Μπορείτε να ακυρώσετε οποιαδήποτε στιγμή: ο σύνδεσμος για τη διαχείριση της συνδρομής σας βρίσκεται στην απόδειξη του Stripe.', btn='Δείτε το προφίλ της σχολής μου',
 sig='Με εκτίμηση<br>Mateus<br>Latin Dance Awards', foot='Latin Dance Awards · ανεξάρτητη κατάταξη σχολών λατινικών χορών στην Ευρώπη', plink='{{Σύνδεσμος προφίλ}}')

def html(k, d):
    li = ''.join(f'<tr><td valign="top" width="30" style="padding:6px 0;color:#E4B95B;font:700 16px {SANS}">&#10003;</td><td style="padding:6px 0;color:#F6E7D3;font:16px/1.5 {SANS}">{x}</td></tr>' for x in d['items'])
    return f'''<!doctype html><html lang="{k}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>{d['subject']}</title></head>
<body style="margin:0;padding:0;background:#080707">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">{d['pre']}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#080707"><tr><td align="center" style="padding:28px 14px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%">
<tr><td align="center" style="padding:6px 0 26px"><div style="font:600 26px {SERIF};color:#F6E7D3;letter-spacing:.5px">&#9733;&nbsp; Latin Dance</div><div style="font:700 11px {SANS};letter-spacing:.55em;color:#E4B95B;margin-top:6px;padding-left:.55em">AWARDS</div></td></tr>
<tr><td bgcolor="#131011" style="background:#131011;border:1px solid #6b5522;border-radius:22px;padding:34px 30px">
<p style="margin:0 0 14px;font:500 24px/1.25 {SERIF};color:#F8E2A6">{d['hi']}</p>
<p style="margin:0 0 26px;font:16px/1.6 {SANS};color:#F6E7D3">{d['p1']}</p>
<h2 style="margin:0 0 6px;font:500 21px/1.3 {SERIF};color:#F8E2A6">{d['h2']}</h2>
<p style="margin:0 0 14px;font:15px/1.55 {SANS};color:#b9aa98">{d['sub']}</p>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%">{li}</table>
<p style="margin:18px 0 0;padding:14px 16px;border:1px solid #4a3a18;border-radius:12px;background:#1b1612;font:14px/1.55 {SANS};color:#b9aa98">{d['proof']}</p>
<h2 style="margin:28px 0 6px;font:500 21px/1.3 {SERIF};color:#F8E2A6">{d['next_h']}</h2>
<p style="margin:0 0 22px;font:16px/1.6 {SANS};color:#F6E7D3">{d['next']}</p>
<table role="presentation" cellpadding="0" cellspacing="0"><tr><td bgcolor="#E4B95B" style="background:#E4B95B;border-radius:999px"><a href="{d['plink']}" style="display:inline-block;padding:14px 28px;font:700 15px {SANS};color:#131011;text-decoration:none">{d['btn']}</a></td></tr></table>
<p style="margin:24px 0 0;font:14px/1.55 {SANS};color:#b9aa98">{d['cancel']}</p>
<p style="margin:26px 0 0;font:16px/1.6 {SANS};color:#F6E7D3">{d['sig']}</p>
</td></tr>
<tr><td align="center" style="padding:22px 10px 0;font:12px/1.6 {SANS};color:#8a7d6c">{d['foot']}{FOOT}</td></tr>
</table></td></tr></table></body></html>'''
def txt(d):
    f = lambda x: re.sub(r'<br>', '\n', re.sub(r'<a [^>]*>(.*?)</a>', r'\1', x)).replace('<b>', '').replace('</b>', '')
    return (f"Subject: {d['subject']}\n\n{f(d['hi'])}\n\n{f(d['p1'])}\n\n{f(d['h2'])}\n{f(d['sub'])}\n" + ''.join('- ' + f(x) + '\n' for x in d['items'])
            + f"\n{f(d['proof'])}\n\n{f(d['next_h'])}\n{f(d['next'])}\n\n{f(d['cancel'])}\n\n{f(d['sig'])}\n\n{f(d['foot'])}\nlatindanceawards.com\n")
for k, d in T.items():
    open(os.path.join(HERE, f'welcome-{k}.html'), 'w', encoding='utf-8').write(html(k, d))
    open(os.path.join(HERE, f'welcome-{k}.txt'), 'w', encoding='utf-8').write(txt(d))
print(len(T), 'languages')
