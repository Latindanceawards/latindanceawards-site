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
 'de': dict(subj='Kurze Frage zu {n}', intro='In einem Ranking der besten Bachata-Schulen Europas zu stehen, ist etwas Besonderes, und {n} ({c}) ist schon dabei. Über 15.000 Menschen besuchen unsere Seite jeden Monat, viele davon auf der Suche nach einem Ort zum Tanzen.',
   ph='Pläne ab 5 € im Monat', pp='Werde von über 15.000 Besuchern im Monat gesehen: Anfragen für Probestunden, Fotos und Videos, Links zu deinen Social-Media-Profilen, damit dir Leute folgen, und das Häkchen „geprüft“. Mit Spotlight bewerben wir deine Schule ganz oben in deiner Stadt.',
   fp='Noch nicht bereit für einen Plan? Bestätige deine Daten kostenlos: Mehr Punkte bedeuten einen besseren Platz und mehr Sichtbarkeit.'),
 'en': dict(subj='Quick question about {n}', intro='Being in a ranking of Europe’s best Bachata schools is something special, and {n} ({c}) is already in it. More than 15,000 people visit our site every month, and many come to find a place to dance.',
   ph='Plans from €5 a month', pp='Get seen by 15,000+ visitors a month: trial-class requests, photos and videos, links to your social profiles so people follow you, and the verified check mark. With Spotlight, we advertise your school at the top of your city.',
   fp='Not ready for a plan? Confirm your details for free: more points mean a higher place and more visibility.'),
 'es': dict(subj='Una pregunta rápida sobre {n}', intro='Estar en un ranking de las mejores escuelas de bachata de Europa es algo especial, y {n} ({c}) ya está en él. Más de 15.000 personas visitan nuestra web cada mes, y muchas buscan un sitio donde bailar.',
   ph='Planes desde 5 € al mes', pp='Consigue que te vean más de 15.000 visitantes al mes: solicitudes de clase de prueba, fotos y vídeos, enlaces a tus redes para que la gente te siga y el sello de escuela verificada. Con Spotlight anunciamos tu escuela en lo más alto de tu ciudad.',
   fp='¿Todavía no quieres un plan? Confirma tus datos gratis: más puntos significan mejor puesto y más visibilidad.'),
 'fr': dict(subj='Une petite question sur {n}', intro='Figurer dans un classement des meilleures écoles de bachata d’Europe est une belle reconnaissance, et {n} ({c}) en fait déjà partie. Plus de 15 000 personnes visitent notre site chaque mois, et beaucoup cherchent un endroit où danser.',
   ph='Formules à partir de 5 € par mois', pp='Soyez vu par plus de 15 000 visiteurs par mois : demandes de cours d’essai, photos et vidéos, liens vers vos réseaux pour que l’on vous suive, et badge « école vérifiée ». Avec Spotlight, nous mettons votre école en avant tout en haut de votre ville.',
   fp='Pas encore prêt pour une formule ? Confirmez vos infos gratuitement : plus de points, c’est une meilleure place et plus de visibilité.'),
 'it': dict(subj='Una domanda veloce su {n}', intro='Essere in una classifica delle migliori scuole di bachata d’Europa è qualcosa di speciale, e {n} ({c}) ci è già. Più di 15.000 persone visitano il nostro sito ogni mese, e molte cercano un posto dove ballare.',
   ph='Piani da 5 € al mese', pp='Fatti vedere da oltre 15.000 visitatori al mese: richieste di lezione di prova, foto e video, link ai tuoi social perché ti seguano e il segno di scuola verificata. Con Spotlight pubblicizziamo la tua scuola in cima alla tua città.',
   fp='Non sei ancora pronto per un piano? Conferma i tuoi dati gratis: più punti significano un posto migliore e più visibilità.'),
 'pt': dict(subj='Uma pergunta rápida sobre {n}', intro='Estar num ranking das melhores escolas de bachata da Europa é algo especial, e a {n} ({c}) já faz parte dele. Mais de 15 000 pessoas visitam o nosso site todos os meses, e muitas procuram um sítio para dançar.',
   ph='Planos desde 5 € por mês', pp='Seja visto por mais de 15 000 visitantes por mês: pedidos de aula experimental, fotografias e vídeos, ligações às suas redes sociais para que o sigam e o selo de escola verificada. Com o Spotlight, anunciamos a sua escola no topo da sua cidade.',
   fp='Ainda não está pronto para um plano? Confirme os seus dados gratuitamente: mais pontos significam melhor posição e mais visibilidade.'),
 'pl': dict(subj='Szybkie pytanie o {n}', intro='Bycie w rankingu najlepszych szkół bachaty w Europie to coś wyjątkowego, a {n} ({c}) już w nim jest. Ponad 15 000 osób odwiedza naszą stronę co miesiąc, a wiele z nich szuka miejsca do tańca.',
   ph='Plany od 5 € miesięcznie', pp='Zdobądź uwagę ponad 15 000 odwiedzających miesięcznie: zapytania o zajęcia próbne, zdjęcia i filmy, linki do Twoich social mediów, by ludzie Cię obserwowali, oraz znacznik zweryfikowanej szkoły. Z planem Spotlight reklamujemy Twoją szkołę na samej górze Twojego miasta.',
   fp='Jeszcze nie jesteś gotowy na plan? Potwierdź dane za darmo: więcej punktów to wyższe miejsce i większa widoczność.'),
 'nl': dict(subj='Korte vraag over {n}', intro='In een ranglijst van de beste bachata-scholen van Europa staan is iets bijzonders, en {n} ({c}) staat er al in. Meer dan 15.000 mensen bezoeken onze site elke maand, en velen zoeken een plek om te dansen.',
   ph='Pakketten vanaf € 5 per maand', pp='Word gezien door meer dan 15.000 bezoekers per maand: aanvragen voor proeflessen, foto’s en video’s, links naar je socials zodat mensen je volgen en het vinkje voor gecontroleerde school. Met Spotlight adverteren we je school bovenaan in jouw stad.',
   fp='Nog niet klaar voor een pakket? Bevestig je gegevens gratis: meer punten betekenen een hogere plaats en meer zichtbaarheid.'),
 'tr': dict(subj='{n} hakkında kısa bir soru', intro='Avrupa’nın en iyi bachata okullarının sıralamasında yer almak özel bir şey ve {n} ({c}) zaten bu sıralamada. Sitemizi her ay 15.000’den fazla kişi ziyaret ediyor ve birçoğu dans edecek bir yer arıyor.',
   ph='Ayda 5 €’dan başlayan planlar', pp='Ayda 15.000’den fazla ziyaretçi tarafından görülün: deneme dersi talepleri, fotoğraflar ve videolar, insanların sizi takip etmesi için sosyal medya bağlantıları ve doğrulanmış okul işareti. Spotlight ile okulunuzu şehrinizin en üstünde tanıtıyoruz.',
   fp='Henüz bir plan için hazır değil misiniz? Bilgilerinizi ücretsiz doğrulayın: daha fazla puan, daha iyi sıra ve daha fazla görünürlük demektir.'),
 'ro': dict(subj='O întrebare rapidă despre {n}', intro='Să fii într-un clasament al celor mai bune școli de bachata din Europa este ceva special, iar {n} ({c}) este deja în el. Peste 15.000 de oameni vizitează site-ul nostru în fiecare lună, iar mulți caută un loc unde să danseze.',
   ph='Planuri de la 5 € pe lună', pp='Fii văzut de peste 15.000 de vizitatori pe lună: cereri pentru lecția de probă, fotografii și videoclipuri, linkuri către rețelele tale sociale ca oamenii să te urmărească și semnul de școală verificată. Cu Spotlight îți promovăm școala în topul orașului tău.',
   fp='Nu ești încă gata pentru un plan? Confirmă-ți datele gratuit: mai multe puncte înseamnă un loc mai bun și mai multă vizibilitate.'),
 'el': dict(subj='Μια γρήγορη ερώτηση για τη σχολή {n}', intro='Το να βρίσκεστε σε μια κατάταξη με τις καλύτερες σχολές μπατσάτα της Ευρώπης είναι κάτι ξεχωριστό, και η σχολή {n} ({c}) είναι ήδη εκεί. Πάνω από 15.000 άτομα επισκέπτονται τον ιστότοπό μας κάθε μήνα και πολλά ψάχνουν μέρος για να χορέψουν.',
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
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 0"><tr><td><img src="{ASSET}gsc-tiles.png" width="507" alt="Google Search Console: {al} {a}, {bl} {b}" style="display:block;border:0;width:100%;max-width:507px;height:auto;border-radius:8px"></td></tr></table>'
            f'<p style="margin:8px 0 22px;font:12px/1.5 {SANS};color:#b9aa98">{cap}</p>')
# NON-SALES copy: competing in the ranking; add details to earn more points. No plans/prices.
CP = {
 'de': dict(intro='Deine Schule {n} ({c}) tritt in unserem unabhängigen Ranking gegen die besten Bachata-Schulen Europas an. Dabei zu sein ist schon etwas, worauf man stolz sein kann. Damit deine Schule mehr Punkte bekommt und im Ranking aufsteigt, musst du aber einige Angaben bestätigen. Wir konnten sie online nicht finden.',
  mid='Die Platzierung beruht auf öffentlichen Daten, zum Beispiel Google-Bewertungen. Es fehlen: Gründungsjahr, Anfängerkurse und Events. Jede Angabe, die du bestätigst, bringt deiner Schule mehr Punkte.',
  note='Das ist kostenlos.', btn='Daten meiner Schule bestätigen'),
 'en': dict(intro='Your school {n} ({c}) is competing with the best Bachata schools in Europe in our independent ranking. Being in it is already something to be proud of. But to earn more points and climb the ranking, you need to confirm some details about your school. We could not find them online.',
  mid='The position is based on public data, such as Google reviews. What is missing: the founding year, beginner classes and events. Every detail you confirm earns your school more points.',
  note='It is free.', btn='Confirm my school’s details'),
 'es': dict(intro='Tu escuela {n} ({c}) compite con las mejores escuelas de bachata de Europa en nuestro ranking independiente. Estar en él ya es algo de lo que sentirse orgulloso. Pero para sumar más puntos y subir en el ranking, tienes que confirmar algunos datos de tu escuela. No hemos podido encontrarlos online.',
  mid='La posición se basa en datos públicos, como las reseñas de Google. Faltan: el año de fundación, las clases para principiantes y los eventos. Cada dato que confirmes da más puntos a tu escuela.',
  note='Es gratis.', btn='Confirmar los datos de mi escuela'),
 'fr': dict(intro='Votre école {n} ({c}) concourt avec les meilleures écoles de bachata d’Europe dans notre classement indépendant. En faire partie est déjà une fierté. Mais pour gagner des points et monter dans le classement, vous devez confirmer quelques informations sur votre école. Nous n’avons pas pu les trouver en ligne.',
  mid='La place repose sur des données publiques, comme les avis Google. Il manque : l’année de création, les cours pour débutants et les événements. Chaque information que vous confirmez rapporte plus de points à votre école.',
  note='C’est gratuit.', btn='Confirmer les infos de mon école'),
 'it': dict(intro='La tua scuola {n} ({c}) è in gara con le migliori scuole di bachata d’Europa nella nostra classifica indipendente. Esserci è già motivo di orgoglio. Ma per guadagnare più punti e salire in classifica, devi confermare alcuni dati della tua scuola. Non siamo riusciti a trovarli online.',
  mid='La posizione si basa su dati pubblici, come le recensioni di Google. Mancano: l’anno di fondazione, i corsi per principianti e gli eventi. Ogni dato che confermi dà più punti alla tua scuola.',
  note='È gratuito.', btn='Conferma i dati della mia scuola'),
 'pt': dict(intro='A sua escola {n} ({c}) está a competir com as melhores escolas de bachata da Europa no nosso ranking independente. Estar nele já é motivo de orgulho. Mas, para ganhar mais pontos e subir no ranking, precisa de confirmar alguns dados da sua escola. Não os conseguimos encontrar online.',
  mid='A posição baseia-se em dados públicos, como as avaliações do Google. Faltam: o ano de fundação, as aulas para principiantes e os eventos. Cada dado que confirmar dá mais pontos à sua escola.',
  note='É gratuito.', btn='Confirmar os dados da minha escola'),
 'pl': dict(intro='Twoja szkoła {n} ({c}) rywalizuje z najlepszymi szkołami bachaty w Europie w naszym niezależnym rankingu. Samo bycie w nim jest powodem do dumy. Aby jednak zdobyć więcej punktów i awansować w rankingu, musisz potwierdzić kilka informacji o swojej szkole. Nie udało nam się znaleźć ich w internecie.',
  mid='Pozycja opiera się na publicznych danych, takich jak opinie w Google. Brakuje: roku założenia, kursów dla początkujących i wydarzeń. Każda potwierdzona informacja daje Twojej szkole więcej punktów.',
  note='To bezpłatne.', btn='Potwierdź dane mojej szkoły'),
 'nl': dict(intro='Jouw school {n} ({c}) strijdt in onze onafhankelijke ranglijst mee met de beste bachata-scholen van Europa. Erin staan is al iets om trots op te zijn. Maar om meer punten te verdienen en te stijgen in de ranglijst, moet je enkele gegevens over je school bevestigen. We konden ze online niet vinden.',
  mid='De plaats is gebaseerd op openbare gegevens, zoals Google-recensies. Wat ontbreekt: het oprichtingsjaar, beginnerslessen en evenementen. Elk gegeven dat je bevestigt levert je school meer punten op.',
  note='Het is gratis.', btn='Gegevens van mijn school bevestigen'),
 'tr': dict(intro='Okulunuz {n} ({c}), bağımsız sıralamamızda Avrupa’nın en iyi bachata okullarıyla yarışıyor. Bu sıralamada yer almak başlı başına gurur verici. Ancak daha fazla puan kazanmak ve sıralamada yükselmek için okulunuzla ilgili bazı bilgileri doğrulamanız gerekiyor. Bunları internette bulamadık.',
  mid='Sıralama, Google yorumları gibi herkese açık verilere dayanıyor. Eksik olanlar: kuruluş yılı, yeni başlayanlara yönelik dersler ve etkinlikler. Doğruladığınız her bilgi okulunuza daha fazla puan kazandırır.',
  note='Ücretsizdir.', btn='Okulumun bilgilerini doğrula'),
 'ro': dict(intro='Școala ta {n} ({c}) concurează cu cele mai bune școli de bachata din Europa în clasamentul nostru independent. Faptul că ești în el este deja un motiv de mândrie. Dar pentru a câștiga mai multe puncte și a urca în clasament, trebuie să confirmi câteva informații despre școala ta. Nu le-am putut găsi online.',
  mid='Poziția se bazează pe date publice, cum ar fi recenziile Google. Lipsesc: anul înființării, cursurile pentru începători și evenimentele. Fiecare informație pe care o confirmi aduce școlii tale mai multe puncte.',
  note='Este gratuit.', btn='Confirmă datele școlii mele'),
 'el': dict(intro='Η σχολή σας {n} ({c}) διεκδικεί θέση ανάμεσα στις καλύτερες σχολές μπατσάτα της Ευρώπης στην ανεξάρτητη κατάταξή μας. Και μόνο η συμμετοχή είναι λόγος υπερηφάνειας. Για να κερδίσετε περισσότερους πόντους και να ανεβείτε στην κατάταξη, όμως, πρέπει να επιβεβαιώσετε μερικά στοιχεία της σχολής σας. Δεν καταφέραμε να τα βρούμε στο διαδίκτυο.',
  mid='Η θέση βασίζεται σε δημόσια δεδομένα, όπως οι κριτικές της Google. Λείπουν: το έτος ίδρυσης, τα μαθήματα για αρχάριους και οι εκδηλώσεις. Κάθε στοιχείο που επιβεβαιώνετε δίνει στη σχολή σας περισσότερους πόντους.',
  note='Είναι δωρεάν.', btn='Επιβεβαίωση στοιχείων της σχολής μου'),
}
# A/B alternative subject (pattern: quick personal question)
SUBJ_B = {'de': 'Kurze Frage zu {n}', 'en': 'Quick question about {n}', 'es': 'Una pregunta rápida sobre {n}', 'fr': 'Une petite question sur {n}', 'it': 'Una domanda veloce su {n}', 'pt': 'Uma pergunta rápida sobre {n}', 'pl': 'Szybkie pytanie o {n}', 'nl': 'Korte vraag over {n}', 'tr': '{n} hakkında kısa bir soru', 'ro': 'O întrebare rapidă despre {n}', 'el': 'Μια γρήγορη ερώτηση για τη σχολή {n}'}
# HUMAN voice (v3): first person, one real question, no marketing words. Keys: intro q ctx opt sig
HUM = {
 'de': dict(intro='Ich bin Mateus und betreibe Latin Dance Awards, ein Ranking der Bachata-Schulen in Europa. Ich habe {n} ({c}) aufgenommen, und die Schule tritt schon gegen einige der besten Schulen Europas an.',
  q='Kannst du mir bei ein paar Angaben helfen? Gründungsjahr, Anfängerkurse und Events habe ich online nicht gefunden. Jede Angabe, die du bestätigst, bringt deiner Schule mehr Punkte und einen besseren Platz.',
  ctx='Zur Einordnung: So viel Traffic bekommt die Seite über Google:', opt='Wenn du lieber nicht gelistet sein möchtest, antworte einfach kurz, dann nehme ich die Schule raus.', sig='Danke dir,\nMateus\nLatin Dance Awards'),
 'en': dict(intro='I’m Mateus and I run Latin Dance Awards, a ranking of Bachata schools in Europe. I added {n} ({c}) to it, and it is already competing with some of the best schools in Europe.',
  q='Could you help me with a few details? I couldn’t find your founding year, whether you offer beginner classes, or any events online. Each one you confirm gives your school more points and moves it up the ranking.',
  ctx='For context, this is the traffic the site gets from Google:', opt='If you’d rather not be listed, just reply and I’ll take your school off.', sig='Thanks,\nMateus\nLatin Dance Awards'),
 'es': dict(intro='Soy Mateus y llevo Latin Dance Awards, un ranking de escuelas de bachata en Europa. He añadido {n} ({c}) y ya compite con algunas de las mejores escuelas de Europa.',
  q='¿Me ayudas con unos datos? No he encontrado online el año de fundación, si hay clases para principiantes ni los eventos. Cada dato que confirmes da más puntos a tu escuela y la sube en el ranking.',
  ctx='Para que te hagas una idea, este es el tráfico que recibe la web desde Google:', opt='Si prefieres no aparecer, respóndeme a este correo y quito tu escuela.', sig='Gracias,\nMateus\nLatin Dance Awards'),
 'fr': dict(intro='Je suis Mateus, je gère Latin Dance Awards, un classement des écoles de bachata en Europe. J’y ai ajouté {n} ({c}), qui concourt déjà avec certaines des meilleures écoles d’Europe.',
  q='Pourriez-vous m’aider avec quelques informations ? Je n’ai pas trouvé en ligne l’année de création, les cours pour débutants ni les événements. Chaque information que vous confirmez rapporte des points à votre école et la fait monter dans le classement.',
  ctx='Pour situer, voici le trafic que le site reçoit depuis Google :', opt='Si vous préférez ne pas figurer dans le classement, répondez simplement à ce message et je retire votre école.', sig='Merci,\nMateus\nLatin Dance Awards'),
 'it': dict(intro='Sono Mateus e gestisco Latin Dance Awards, una classifica delle scuole di bachata in Europa. Ho aggiunto {n} ({c}) e già è in gara con alcune delle migliori scuole d’Europa.',
  q='Mi dai una mano con qualche dato? Online non ho trovato l’anno di fondazione, i corsi per principianti né gli eventi. Ogni dato che confermi dà più punti alla tua scuola e la fa salire in classifica.',
  ctx='Giusto per darti un’idea, questo è il traffico che il sito riceve da Google:', opt='Se preferisci non comparire, rispondi a questa email e tolgo la tua scuola.', sig='Grazie,\nMateus\nLatin Dance Awards'),
 'pt': dict(intro='Sou o Mateus e giro o Latin Dance Awards, um ranking de escolas de bachata na Europa. Acrescentei a {n} ({c}) e ela já compete com algumas das melhores escolas da Europa.',
  q='Pode ajudar-me com alguns dados? Não encontrei online o ano de fundação, se há aulas para principiantes nem os eventos. Cada dado que confirmar dá mais pontos à sua escola e faz com que suba no ranking.',
  ctx='Só para ter uma ideia, este é o tráfego que o site recebe do Google:', opt='Se preferir não aparecer, basta responder a este e-mail e eu retiro a sua escola.', sig='Obrigado,\nMateus\nLatin Dance Awards'),
 'pl': dict(intro='Jestem Mateus i prowadzę Latin Dance Awards, ranking szkół bachaty w Europie. Dodałem do niego {n} ({c}), a szkoła już rywalizuje z jednymi z najlepszych w Europie.',
  q='Czy pomożesz mi w kilku informacjach? Nie znalazłem w internecie roku założenia, kursów dla początkujących ani wydarzeń. Każda potwierdzona informacja daje Twojej szkole więcej punktów i podnosi ją w rankingu.',
  ctx='Dla kontekstu: tyle ruchu strona dostaje z Google:', opt='Jeśli wolisz nie być w rankingu, odpisz na tego maila, a usunę szkołę.', sig='Dzięki,\nMateus\nLatin Dance Awards'),
 'nl': dict(intro='Ik ben Mateus en beheer Latin Dance Awards, een ranglijst van bachata-scholen in Europa. Ik heb {n} ({c}) toegevoegd en de school strijdt al mee met een paar van de beste scholen van Europa.',
  q='Kun je me helpen met een paar gegevens? Het oprichtingsjaar, beginnerslessen en evenementen kon ik online niet vinden. Elk gegeven dat je bevestigt levert je school meer punten op en brengt je hoger in de ranglijst.',
  ctx='Ter indicatie: dit is het verkeer dat de site via Google krijgt:', opt='Wil je liever niet in de lijst staan? Stuur gewoon een reply, dan haal ik je school eruit.', sig='Bedankt,\nMateus\nLatin Dance Awards'),
 'tr': dict(intro='Ben Mateus, Latin Dance Awards’ı yönetiyorum; Avrupa’daki bachata okullarının sıralaması. {n} ({c}) okulunu ekledim ve Avrupa’nın en iyi okullarından bazılarıyla zaten yarışıyor.',
  q='Birkaç bilgi konusunda yardımcı olur musunuz? Kuruluş yılını, yeni başlayanlara yönelik dersleri ve etkinlikleri internette bulamadım. Doğruladığınız her bilgi okulunuza puan kazandırır ve sıralamada yükseltir.',
  ctx='Fikir vermesi için, sitenin Google’dan aldığı trafik şu:', opt='Listede yer almak istemezseniz bu e-postayı yanıtlamanız yeterli, okulunuzu kaldırırım.', sig='Teşekkürler,\nMateus\nLatin Dance Awards'),
 'ro': dict(intro='Sunt Mateus și administrez Latin Dance Awards, un clasament al școlilor de bachata din Europa. Am adăugat {n} ({c}), iar școala concurează deja cu unele dintre cele mai bune din Europa.',
  q='Mă poți ajuta cu câteva informații? Nu am găsit online anul înființării, cursurile pentru începători și evenimentele. Fiecare informație pe care o confirmi aduce școlii tale mai multe puncte și o urcă în clasament.',
  ctx='Ca să-ți faci o idee, acesta este traficul pe care îl primește site-ul de la Google:', opt='Dacă preferi să nu apari în clasament, răspunde la acest e-mail și îți scot școala.', sig='Mulțumesc,\nMateus\nLatin Dance Awards'),
 'el': dict(intro='Είμαι ο Mateus και διαχειρίζομαι το Latin Dance Awards, μια κατάταξη σχολών μπατσάτα στην Ευρώπη. Πρόσθεσα τη σχολή {n} ({c}) και ήδη διεκδικεί θέση ανάμεσα στις καλύτερες της Ευρώπης.',
  q='Μπορείτε να με βοηθήσετε με μερικά στοιχεία; Δεν βρήκα στο διαδίκτυο το έτος ίδρυσης, τα μαθήματα για αρχάριους και τις εκδηλώσεις. Κάθε στοιχείο που επιβεβαιώνετε δίνει περισσότερους πόντους στη σχολή σας και την ανεβάζει στην κατάταξη.',
  ctx='Για να έχετε μια ιδέα, αυτή είναι η επισκεψιμότητα που παίρνει ο ιστότοπος από την Google:', opt='Αν προτιμάτε να μην εμφανίζεστε, απαντήστε σε αυτό το μήνυμα και θα αφαιρέσω τη σχολή.', sig='Ευχαριστώ,\nMateus\nLatin Dance Awards'),
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
    intro = HUM[l]['intro'].replace('{n}', name).replace('{c}', city)
    hi_txt = greeting if greeting is not None else re.sub(r' \{\{[^}]+\}\}([,:])', r'\1', hi)
    sig_h = HUM[l]['sig'].replace('\n', '<br>')
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
<tr><td style="padding:6px 4px 0">
<p style="margin:0 0 14px;font:500 22px/1.25 {SERIF};color:#F8E2A6">{hi_txt}</p>
{P(intro)}
{P(HUM[l]['q'])}
{P(HUM[l]['ctx'])}
{proof(l)}
{card}
<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 26px"><tr>{btn(CP[l]['btn'], 'https://latindanceawards.com/bewerbung', True)}</tr></table>
{P(HUM[l]['opt'], '#b9aa98', 14)}
<p style="margin:22px 0 0;font:16px/1.6 {SANS};color:#F6E7D3">{sig_h}</p>
</td></tr>
<tr><td align="center" style="padding:22px 10px 0;font:12px/1.6 {SANS};color:#8a7d6c">{foot_h}</td></tr>
</table></td></tr></table></body></html>'''
if __name__ == '__main__':
    out = os.path.join(HERE, 'outreach-html'); os.makedirs(out, exist_ok=True)
    for l in T:
        open(os.path.join(out, f'outreach-{l}.html'), 'w', encoding='utf-8').write(render(l, '{{School name}}', '{{City}}', '{{Rank}}', '{{Profile link}}'))
    print(len(T), 'languages')
