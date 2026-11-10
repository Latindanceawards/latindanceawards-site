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
# Stronger copy: being ranked among Europe's best is a big deal; visibility, advertising, followers; 15,000+ monthly visitors.
# {n} = school, {c} = city.  Keys: subj, intro, ph (price headline), pp (price paragraph), fp (free paragraph)
NEW = {
 'de': dict(subj='{n} kämpft um den Titel der besten Bachata-Schule Europas 🏆', intro='In einem Ranking der besten Bachata-Schulen Europas zu stehen, ist etwas Besonderes, und {n} ({c}) ist schon dabei. Über 15.000 Menschen besuchen unsere Seite jeden Monat, viele davon auf der Suche nach einem Ort zum Tanzen.',
   ph='Pläne ab 5 € im Monat', pp='Werde von über 15.000 Besuchern im Monat gesehen: Anfragen für Probestunden, Fotos und Videos, Links zu deinen Social-Media-Profilen, damit dir Leute folgen, und das Häkchen „geprüft“. Mit Spotlight bewerben wir deine Schule ganz oben in deiner Stadt.',
   fp='Noch nicht bereit für einen Plan? Bestätige deine Daten kostenlos: Mehr Punkte bedeuten einen besseren Platz und mehr Sichtbarkeit.'),
 'en': dict(subj='{n} is in the race for Europe’s best Bachata school 🏆', intro='Being in a ranking of Europe’s best Bachata schools is something special, and {n} ({c}) is already in it. More than 15,000 people visit our site every month, and many come to find a place to dance.',
   ph='Plans from €5 a month', pp='Get seen by 15,000+ visitors a month: trial-class requests, photos and videos, links to your social profiles so people follow you, and the verified check mark. With Spotlight, we advertise your school at the top of your city.',
   fp='Not ready for a plan? Confirm your details for free: more points mean a higher place and more visibility.'),
 'es': dict(subj='{n} compite por ser la mejor escuela de bachata de Europa 🏆', intro='Estar en un ranking de las mejores escuelas de bachata de Europa es algo especial, y {n} ({c}) ya está en él. Más de 15.000 personas visitan nuestra web cada mes, y muchas buscan un sitio donde bailar.',
   ph='Planes desde 5 € al mes', pp='Consigue que te vean más de 15.000 visitantes al mes: solicitudes de clase de prueba, fotos y vídeos, enlaces a tus redes para que la gente te siga y el sello de escuela verificada. Con Spotlight anunciamos tu escuela en lo más alto de tu ciudad.',
   fp='¿Todavía no quieres un plan? Confirma tus datos gratis: más puntos significan mejor puesto y más visibilidad.'),
 'fr': dict(subj='{n} est en lice pour la meilleure école de bachata d’Europe 🏆', intro='Figurer dans un classement des meilleures écoles de bachata d’Europe est une belle reconnaissance, et {n} ({c}) en fait déjà partie. Plus de 15 000 personnes visitent notre site chaque mois, et beaucoup cherchent un endroit où danser.',
   ph='Formules à partir de 5 € par mois', pp='Soyez vu par plus de 15 000 visiteurs par mois : demandes de cours d’essai, photos et vidéos, liens vers vos réseaux pour que l’on vous suive, et badge « école vérifiée ». Avec Spotlight, nous mettons votre école en avant tout en haut de votre ville.',
   fp='Pas encore prêt pour une formule ? Confirmez vos infos gratuitement : plus de points, c’est une meilleure place et plus de visibilité.'),
 'it': dict(subj='{n} è in corsa per la miglior scuola di bachata d’Europa 🏆', intro='Essere in una classifica delle migliori scuole di bachata d’Europa è qualcosa di speciale, e {n} ({c}) ci è già. Più di 15.000 persone visitano il nostro sito ogni mese, e molte cercano un posto dove ballare.',
   ph='Piani da 5 € al mese', pp='Fatti vedere da oltre 15.000 visitatori al mese: richieste di lezione di prova, foto e video, link ai tuoi social perché ti seguano e il segno di scuola verificata. Con Spotlight pubblicizziamo la tua scuola in cima alla tua città.',
   fp='Non sei ancora pronto per un piano? Conferma i tuoi dati gratis: più punti significano un posto migliore e più visibilità.'),
 'pt': dict(subj='{n} está na corrida pela melhor escola de bachata da Europa 🏆', intro='Estar num ranking das melhores escolas de bachata da Europa é algo especial, e a {n} ({c}) já faz parte dele. Mais de 15 000 pessoas visitam o nosso site todos os meses, e muitas procuram um sítio para dançar.',
   ph='Planos desde 5 € por mês', pp='Seja visto por mais de 15 000 visitantes por mês: pedidos de aula experimental, fotografias e vídeos, ligações às suas redes sociais para que o sigam e o selo de escola verificada. Com o Spotlight, anunciamos a sua escola no topo da sua cidade.',
   fp='Ainda não está pronto para um plano? Confirme os seus dados gratuitamente: mais pontos significam melhor posição e mais visibilidade.'),
 'pl': dict(subj='{n} walczy o miano najlepszej szkoły bachaty w Europie 🏆', intro='Bycie w rankingu najlepszych szkół bachaty w Europie to coś wyjątkowego, a {n} ({c}) już w nim jest. Ponad 15 000 osób odwiedza naszą stronę co miesiąc, a wiele z nich szuka miejsca do tańca.',
   ph='Plany od 5 € miesięcznie', pp='Zdobądź uwagę ponad 15 000 odwiedzających miesięcznie: zapytania o zajęcia próbne, zdjęcia i filmy, linki do Twoich social mediów, by ludzie Cię obserwowali, oraz znacznik zweryfikowanej szkoły. Z planem Spotlight reklamujemy Twoją szkołę na samej górze Twojego miasta.',
   fp='Jeszcze nie jesteś gotowy na plan? Potwierdź dane za darmo: więcej punktów to wyższe miejsce i większa widoczność.'),
 'nl': dict(subj='{n} strijdt om de beste bachata-school van Europa 🏆', intro='In een ranglijst van de beste bachata-scholen van Europa staan is iets bijzonders, en {n} ({c}) staat er al in. Meer dan 15.000 mensen bezoeken onze site elke maand, en velen zoeken een plek om te dansen.',
   ph='Pakketten vanaf € 5 per maand', pp='Word gezien door meer dan 15.000 bezoekers per maand: aanvragen voor proeflessen, foto’s en video’s, links naar je socials zodat mensen je volgen en het vinkje voor gecontroleerde school. Met Spotlight adverteren we je school bovenaan in jouw stad.',
   fp='Nog niet klaar voor een pakket? Bevestig je gegevens gratis: meer punten betekenen een hogere plaats en meer zichtbaarheid.'),
 'tr': dict(subj='{n}, Avrupa’nın en iyi bachata okulu yarışında 🏆', intro='Avrupa’nın en iyi bachata okullarının sıralamasında yer almak özel bir şey ve {n} ({c}) zaten bu sıralamada. Sitemizi her ay 15.000’den fazla kişi ziyaret ediyor ve birçoğu dans edecek bir yer arıyor.',
   ph='Ayda 5 €’dan başlayan planlar', pp='Ayda 15.000’den fazla ziyaretçi tarafından görülün: deneme dersi talepleri, fotoğraflar ve videolar, insanların sizi takip etmesi için sosyal medya bağlantıları ve doğrulanmış okul işareti. Spotlight ile okulunuzu şehrinizin en üstünde tanıtıyoruz.',
   fp='Henüz bir plan için hazır değil misiniz? Bilgilerinizi ücretsiz doğrulayın: daha fazla puan, daha iyi sıra ve daha fazla görünürlük demektir.'),
 'ro': dict(subj='{n} luptă pentru cea mai bună școală de bachata din Europa 🏆', intro='Să fii într-un clasament al celor mai bune școli de bachata din Europa este ceva special, iar {n} ({c}) este deja în el. Peste 15.000 de oameni vizitează site-ul nostru în fiecare lună, iar mulți caută un loc unde să danseze.',
   ph='Planuri de la 5 € pe lună', pp='Fii văzut de peste 15.000 de vizitatori pe lună: cereri pentru lecția de probă, fotografii și videoclipuri, linkuri către rețelele tale sociale ca oamenii să te urmărească și semnul de școală verificată. Cu Spotlight îți promovăm școala în topul orașului tău.',
   fp='Nu ești încă gata pentru un plan? Confirmă-ți datele gratuit: mai multe puncte înseamnă un loc mai bun și mai multă vizibilitate.'),
 'el': dict(subj='Η {n} διεκδικεί τον τίτλο της καλύτερης σχολής μπατσάτα της Ευρώπης 🏆', intro='Το να βρίσκεστε σε μια κατάταξη με τις καλύτερες σχολές μπατσάτα της Ευρώπης είναι κάτι ξεχωριστό, και η σχολή {n} ({c}) είναι ήδη εκεί. Πάνω από 15.000 άτομα επισκέπτονται τον ιστότοπό μας κάθε μήνα και πολλά ψάχνουν μέρος για να χορέψουν.',
   ph='Πακέτα από 5 € τον μήνα', pp='Γίνετε ορατοί σε πάνω από 15.000 επισκέπτες τον μήνα: αιτήματα για δοκιμαστικό μάθημα, φωτογραφίες και βίντεο, συνδέσμους στα social σας για να σας ακολουθούν και το σήμα επαληθευμένης σχολής. Με το Spotlight προβάλλουμε τη σχολή σας στην κορυφή της πόλης σας.',
   fp='Δεν είστε έτοιμοι για πακέτο; Επιβεβαιώστε δωρεάν τα στοιχεία σας: περισσότεροι πόντοι σημαίνουν καλύτερη θέση και μεγαλύτερη προβολή.')}
# Search Console proof, styled like Google Search Console (real numbers, last 3 months: 15,448 clicks, 842K impressions)
PROOF = {'de':('15.448','Klicks insgesamt','842K','Impressionen insgesamt','Daten von Google Search Console, letzte 3 Monate'),
 'en':('15,448','Total clicks','842K','Total impressions','Data from Google Search Console, last 3 months'),
 'es':('15.448','Clics totales','842K','Impresiones totales','Datos de Google Search Console, últimos 3 meses'),
 'fr':('15 448','Total des clics','842K','Total des impressions','Données de Google Search Console, 3 derniers mois'),
 'it':('15.448','Clic totali','842K','Impressioni totali','Dati di Google Search Console, ultimi 3 mesi'),
 'pt':('15 448','Total de cliques','842K','Total de impressões','Dados do Google Search Console, últimos 3 meses'),
 'pl':('15 448','Łączna liczba kliknięć','842K','Łączna liczba wyświetleń','Dane z Google Search Console, ostatnie 3 miesiące'),
 'nl':('15.448','Totaal aantal klikken','842K','Totaal aantal vertoningen','Gegevens van Google Search Console, laatste 3 maanden'),
 'tr':('15.448','Toplam tıklama','842K','Toplam gösterim','Google Search Console verileri, son 3 ay'),
 'ro':('15.448','Total clicuri','842K','Total afișări','Date din Google Search Console, ultimele 3 luni'),
 'el':('15.448','Σύνολο κλικ','842K','Σύνολο εμφανίσεων','Δεδομένα από το Google Search Console, τελευταίοι 3 μήνες')}
GF = "'Google Sans',Roboto,Arial,sans-serif"
def proof(l):
    a,al,b,bl,cap=PROOF[l]
    def tile(n,lab,col):
        chk = f'<span style="display:inline-block;width:14px;height:14px;line-height:14px;border:1.5px solid #ffffff;border-radius:3px;text-align:center;font:700 11px {GF};color:#ffffff;vertical-align:middle">&#10003;</span>'
        q = f'<span style="display:inline-block;width:18px;height:18px;line-height:18px;border:1.5px solid #ffffff;border-radius:50%;text-align:center;font:500 11px {GF};color:#ffffff">?</span>'
        return (f'<td width="50%" valign="top" bgcolor="{col}" style="background:{col};padding:16px 16px 14px">'
                f'<div style="font:500 14px/1.3 {GF};color:#ffffff">{chk}&nbsp;&nbsp;{lab}</div>'
                f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:10px"><tr><td valign="bottom" style="font:400 34px/1.1 {GF};color:#ffffff">{n}</td><td align="right" valign="bottom">{q}</td></tr></table></td>')
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="margin:6px 0 0;background:#ffffff;border-radius:8px"><tr><td style="padding:0;border-radius:8px;overflow:hidden">'
            '<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'+tile(a,al,'#4285f4')+tile(b,bl,'#5e35b1')+'</tr></table></td></tr></table>'
            f'<p style="margin:8px 0 22px;font:12px/1.5 {SANS};color:#b9aa98">{cap}</p>')
# NON-SALES copy: competing in the ranking; add details to earn more points. No plans/prices.
CP = {
 'de': dict(intro='Deine Schule {n} ({c}) tritt in unserem unabhängigen Ranking gegen die besten Bachata-Schulen Europas an. Dabei zu sein ist schon etwas, worauf man stolz sein kann.',
  mid='Die Platzierung beruht auf öffentlichen Daten, zum Beispiel Google-Bewertungen. Bei vielen Schulen konnten wir Angaben wie das Gründungsjahr, Anfängerkurse oder Events nicht finden. Jede Angabe, die du ergänzt, bringt deiner Schule mehr Punkte und einen besseren Platz.',
  note='Das ist kostenlos.', btn='Daten meiner Schule ergänzen'),
 'en': dict(intro='Your school {n} ({c}) is competing with the best Bachata schools in Europe in our independent ranking. Being in it is already something to be proud of.',
  mid='The position is based on public data, such as Google reviews. For many schools we could not find details like the founding year, beginner classes or events. Every detail you add earns your school more points and a higher place.',
  note='It is free.', btn='Add my school’s details'),
 'es': dict(intro='Tu escuela {n} ({c}) compite con las mejores escuelas de bachata de Europa en nuestro ranking independiente. Estar en él ya es algo de lo que sentirse orgulloso.',
  mid='La posición se basa en datos públicos, como las reseñas de Google. De muchas escuelas no hemos podido encontrar datos como el año de fundación, las clases para principiantes o los eventos. Cada dato que añadas da más puntos a tu escuela y un mejor puesto.',
  note='Es gratis.', btn='Añadir los datos de mi escuela'),
 'fr': dict(intro='Votre école {n} ({c}) concourt avec les meilleures écoles de bachata d’Europe dans notre classement indépendant. En faire partie est déjà une fierté.',
  mid='La place repose sur des données publiques, comme les avis Google. Pour beaucoup d’écoles, nous n’avons pas trouvé d’informations comme l’année de création, les cours pour débutants ou les événements. Chaque information que vous ajoutez rapporte plus de points à votre école et une meilleure place.',
  note='C’est gratuit.', btn='Ajouter les infos de mon école'),
 'it': dict(intro='La tua scuola {n} ({c}) è in gara con le migliori scuole di bachata d’Europa nella nostra classifica indipendente. Esserci è già motivo di orgoglio.',
  mid='La posizione si basa su dati pubblici, come le recensioni di Google. Di molte scuole non abbiamo trovato informazioni come l’anno di fondazione, i corsi per principianti o gli eventi. Ogni dato che aggiungi dà più punti alla tua scuola e un posto migliore.',
  note='È gratuito.', btn='Aggiungi i dati della mia scuola'),
 'pt': dict(intro='A sua escola {n} ({c}) está a competir com as melhores escolas de bachata da Europa no nosso ranking independente. Estar nele já é motivo de orgulho.',
  mid='A posição baseia-se em dados públicos, como as avaliações do Google. De muitas escolas não encontrámos informações como o ano de fundação, as aulas para principiantes ou os eventos. Cada dado que acrescentar dá mais pontos à sua escola e uma posição melhor.',
  note='É gratuito.', btn='Adicionar os dados da minha escola'),
 'pl': dict(intro='Twoja szkoła {n} ({c}) rywalizuje z najlepszymi szkołami bachaty w Europie w naszym niezależnym rankingu. Samo bycie w nim jest powodem do dumy.',
  mid='Pozycja opiera się na publicznych danych, takich jak opinie w Google. W przypadku wielu szkół nie znaleźliśmy informacji, takich jak rok założenia, kursy dla początkujących czy wydarzenia. Każda informacja, którą dodasz, daje Twojej szkole więcej punktów i wyższe miejsce.',
  note='To bezpłatne.', btn='Dodaj dane mojej szkoły'),
 'nl': dict(intro='Jouw school {n} ({c}) strijdt in onze onafhankelijke ranglijst mee met de beste bachata-scholen van Europa. Erin staan is al iets om trots op te zijn.',
  mid='De plaats is gebaseerd op openbare gegevens, zoals Google-recensies. Van veel scholen konden we gegevens als het oprichtingsjaar, beginnerslessen of evenementen niet vinden. Elk gegeven dat je toevoegt levert je school meer punten en een hogere plaats op.',
  note='Het is gratis.', btn='Gegevens van mijn school toevoegen'),
 'tr': dict(intro='Okulunuz {n} ({c}), bağımsız sıralamamızda Avrupa’nın en iyi bachata okullarıyla yarışıyor. Bu sıralamada yer almak başlı başına gurur verici.',
  mid='Sıralama, Google yorumları gibi herkese açık verilere dayanıyor. Birçok okul için kuruluş yılı, yeni başlayanlara yönelik dersler veya etkinlikler gibi bilgileri bulamadık. Eklediğiniz her bilgi okulunuza daha fazla puan ve daha iyi bir sıra kazandırır.',
  note='Ücretsizdir.', btn='Okulumun bilgilerini ekle'),
 'ro': dict(intro='Școala ta {n} ({c}) concurează cu cele mai bune școli de bachata din Europa în clasamentul nostru independent. Faptul că ești în el este deja un motiv de mândrie.',
  mid='Poziția se bazează pe date publice, cum ar fi recenziile Google. Pentru multe școli nu am găsit informații precum anul înființării, cursurile pentru începători sau evenimentele. Fiecare informație pe care o adaugi aduce școlii tale mai multe puncte și un loc mai bun.',
  note='Este gratuit.', btn='Adaugă datele școlii mele'),
 'el': dict(intro='Η σχολή σας {n} ({c}) διεκδικεί θέση ανάμεσα στις καλύτερες σχολές μπατσάτα της Ευρώπης στην ανεξάρτητη κατάταξή μας. Και μόνο η συμμετοχή είναι λόγος υπερηφάνειας.',
  mid='Η θέση βασίζεται σε δημόσια δεδομένα, όπως οι κριτικές της Google. Για πολλές σχολές δεν βρήκαμε στοιχεία όπως το έτος ίδρυσης, τα μαθήματα για αρχάριους ή οι εκδηλώσεις. Κάθε στοιχείο που προσθέτετε δίνει στη σχολή σας περισσότερους πόντους και καλύτερη θέση.',
  note='Είναι δωρεάν.', btn='Προσθήκη στοιχείων της σχολής μου'),
}
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
    hi, optout = ps[0], ps[4]
    data = NEW[l]['fp']
    intro = CP[l]['intro'].replace('{n}', name).replace('{c}', city)
    hi_txt = greeting if greeting is not None else re.sub(r' \{\{[^}]+\}\}([,:])', r'\1', hi)
    sig_h = sig.replace('\n', '<br>')
    foot_h = re.sub(r'(https://\S+)', r'<a href="\1" style="color:#E4B95B">\1</a>', foot)
    card = (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 22px"><tr><td bgcolor="#1b1612" style="background:#1b1612;;border:1.5px solid #8a7440;border-radius:18px;padding:18px 20px">'
      f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td width="96" valign="middle"><img src="{ASSET}seal.png" width="84" height="84" alt="" style="display:block;border:0"></td>'
      f'<td valign="middle"><div style="font:600 13px {SANS};color:#F8E2A6">#{rank} {scope}</div><div style="font:500 22px/1.2 {SERIF};color:#F6E7D3;margin-top:3px">{name}</div><div style="font:14px/1.5 {SANS};color:#b9aa98;margin-top:2px">{city}</div></td></tr></table>'
      f'<div style="margin-top:12px"><a href="{link}" style="font:600 14px {SANS};color:#F8E2A6;text-decoration:underline">{prof}</a></div></td></tr></table>')
    def btn(label, href, gold):
        if gold: return f'<td bgcolor="#E4B95B" style="background:#E4B95B;border-radius:999px"><a href="{href}" style="display:inline-block;padding:15px 28px;font:700 15px {SANS};color:#131011;text-decoration:none">{label}</a></td>'
        return f'<td style="border:1px solid #8a7440;border-radius:999px"><a href="{href}" style="display:inline-block;padding:13px 24px;font:700 15px {SANS};color:#F6E7D3;text-decoration:none">{label}</a></td>'
    P = lambda t, c='#F6E7D3', sz=16: f'<p style="margin:0 0 16px;font:{sz}px/1.6 {SANS};color:{c}">{t}</p>'
    return f'''<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><style>{FONTCSS}</style><title>{sub}</title></head>
<body style="margin:0;padding:0;background:#080707">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#080707" style="background:#080707"><tr><td align="center" bgcolor="#080707" style="background:#080707;padding:28px 14px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%">
<tr><td align="center" style="padding:0 0 18px"><a href="https://latindanceawards.com"><img src="{ASSET}email-header.png" width="300" height="75" alt="Latin Dance Awards" style="display:block;border:0;font:600 22px {SERIF};color:#F6E7D3"></a></td></tr>
<tr><td bgcolor="#131011" style="background:#131011;;border:1.5px solid #8a7440;border-radius:24px;padding:34px 30px">
<p style="margin:0 0 14px;font:500 22px/1.25 {SERIF};color:#F8E2A6">{hi_txt}</p>
{P(intro)}
{proof(l)}
{card}
{P(CP[l]['mid'])}
<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 12px"><tr>{btn(CP[l]['btn'], 'https://latindanceawards.com/bewerbung', True)}</tr></table>
<p style="margin:0 0 26px;font:14px/1.6 {SANS};color:#b9aa98">{CP[l]['note']}</p>
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
