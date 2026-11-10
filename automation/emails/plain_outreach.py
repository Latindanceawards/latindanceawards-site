"""Plain-text outreach e-mail 1 (no images, no button, no links) in 11 languages.
Placeholders: {n}=school, {c}=city. Sent from info@latindanceawards.site.
"""
T = {
 'de': dict(subj='Kurze Frage zu {n}', hi='Hallo,',
  body=['Ich bin Mateus und betreibe Latin Dance Awards, ein Ranking der Bachata-Schulen in Europa. Ich habe {n} ({c}) aufgenommen, und die Schule tritt schon gegen einige der besten Schulen Europas an.',
        'Gründungsjahr, Anfängerkurse und Events habe ich online nicht gefunden. Jede Angabe, die du bestätigst, bringt deiner Schule mehr Punkte und einen besseren Platz, und die Seite hat viel Traffic, das können also neue Schüler für dich sein.',
        'Kannst du mir kurz auf diese drei Punkte antworten? Ich aktualisiere dann den Eintrag.',
        'Wenn du lieber nicht gelistet sein möchtest, schreib mir einfach, dann nehme ich die Schule raus.'],
  bye='Danke dir,'),
 'en': dict(subj='Quick question about {n}', hi='Hi,',
  body=['I’m Mateus and I run Latin Dance Awards, a ranking of Bachata schools in Europe. I added {n} ({c}) and it is already competing with some of the best schools in Europe.',
        'I couldn’t find your founding year, whether you offer beginner classes, or any events online. Each one you confirm gives your school more points and moves it up the ranking, and the site gets a lot of traffic, so that can mean new students for you.',
        'Could you reply with those three things? I’ll update your listing.',
        'If you’d rather not be listed, just tell me and I’ll take your school off.'],
  bye='Thanks,'),
 'es': dict(subj='Una pregunta rápida sobre {n}', hi='Hola,',
  body=['Soy Mateus y llevo Latin Dance Awards, un ranking de escuelas de bachata en Europa. He añadido {n} ({c}) y ya compite con algunas de las mejores escuelas de Europa.',
        'No he encontrado online el año de fundación, si tenéis clases para principiantes ni eventos. Cada dato que confirmes da más puntos a tu escuela y la sube en el ranking, y la web tiene mucho tráfico, así que puede traerte alumnos nuevos.',
        '¿Me puedes responder con esos tres datos? Actualizo vuestra ficha.',
        'Si prefieres no aparecer, dímelo y quito la escuela.'],
  bye='Gracias,'),
 'fr': dict(subj='Une petite question sur {n}', hi='Bonjour,',
  body=['Je suis Mateus et je gère Latin Dance Awards, un classement des écoles de bachata en Europe. J’ai ajouté {n} ({c}), qui est déjà en compétition avec certaines des meilleures écoles d’Europe.',
        'Je n’ai pas trouvé en ligne votre année de création, si vous proposez des cours pour débutants, ni vos événements. Chaque information confirmée donne plus de points à votre école et la fait monter dans le classement, et le site a beaucoup de trafic, ce qui peut vous amener de nouveaux élèves.',
        'Pourriez-vous me répondre avec ces trois points ? Je mettrai votre fiche à jour.',
        'Si vous préférez ne pas apparaître, dites-le-moi et je retire votre école.'],
  bye='Merci,'),
 'it': dict(subj='Una domanda veloce su {n}', hi='Ciao,',
  body=['Sono Mateus e gestisco Latin Dance Awards, una classifica delle scuole di bachata in Europa. Ho aggiunto {n} ({c}) e già è in gara con alcune delle migliori scuole d’Europa.',
        'Online non ho trovato l’anno di fondazione, se fate corsi per principianti né gli eventi. Ogni dato che confermi dà più punti alla tua scuola e la fa salire in classifica, e il sito ha molto traffico, quindi può portarti nuovi allievi.',
        'Puoi rispondermi con questi tre dati? Aggiorno la vostra scheda.',
        'Se preferisci non comparire, scrivimelo e tolgo la scuola.'],
  bye='Grazie,'),
 'pt': dict(subj='Uma pergunta rápida sobre {n}', hi='Olá,',
  body=['Sou o Mateus e giro o Latin Dance Awards, um ranking de escolas de bachata na Europa. Acrescentei a {n} ({c}) e ela já compete com algumas das melhores escolas da Europa.',
        'Não encontrei online o ano de fundação, se há aulas para principiantes nem os eventos. Cada dado que confirmar dá mais pontos à sua escola e faz com que suba no ranking, e o site recebe muito tráfego, por isso pode trazer-lhe novos alunos.',
        'Pode responder-me com esses três dados? Eu atualizo a ficha.',
        'Se preferir não aparecer, diga-me e eu retiro a escola.'],
  bye='Obrigado,'),
 'pl': dict(subj='Szybkie pytanie o {n}', hi='Cześć,',
  body=['Jestem Mateus i prowadzę Latin Dance Awards, ranking szkół bachaty w Europie. Dodałem {n} ({c}) i szkoła już rywalizuje z niektórymi z najlepszych szkół w Europie.',
        'Nie znalazłem w internecie roku założenia, informacji o kursach dla początkujących ani wydarzeń. Każda potwierdzona informacja daje Waszej szkole więcej punktów i wyższe miejsce, a strona ma duży ruch, więc może to oznaczać nowych uczniów.',
        'Czy możesz odpisać mi na te trzy rzeczy? Zaktualizuję wpis.',
        'Jeśli wolisz nie być na liście, napisz, a usunę szkołę.'],
  bye='Dzięki,'),
 'nl': dict(subj='Korte vraag over {n}', hi='Hoi,',
  body=['Ik ben Mateus en ik run Latin Dance Awards, een ranglijst van bachatascholen in Europa. Ik heb {n} ({c}) toegevoegd en de school doet al mee met een aantal van de beste scholen van Europa.',
        'Het oprichtingsjaar, beginnerslessen en evenementen kon ik online niet vinden. Elk gegeven dat je bevestigt geeft je school meer punten en een hogere plek, en de site heeft veel verkeer, dus dat kan nieuwe leerlingen opleveren.',
        'Kun je me op die drie punten antwoorden? Dan werk ik de vermelding bij.',
        'Als je liever niet vermeld wilt worden, laat het me weten en ik haal de school eraf.'],
  bye='Bedankt,'),
 'tr': dict(subj='{n} hakkında kısa bir soru', hi='Merhaba,',
  body=['Ben Mateus, Avrupa’daki bachata okullarının sıralamasını yapan Latin Dance Awards’ı yönetiyorum. {n} ({c}) okulunu ekledim ve okul şimdiden Avrupa’nın en iyi okullarından bazılarıyla yarışıyor.',
        'Kuruluş yılını, yeni başlayanlar için ders olup olmadığını ve etkinlikleri internette bulamadım. Onayladığınız her bilgi okulunuza daha fazla puan kazandırır ve sıralamada yükseltir, siteye de çok trafik geliyor, bu da size yeni öğrenciler getirebilir.',
        'Bu üç konuda bana yanıt verebilir misiniz? Kaydı güncellerim.',
        'Listede yer almak istemezseniz söyleyin, okulu kaldırırım.'],
  bye='Teşekkürler,'),
 'ro': dict(subj='O întrebare rapidă despre {n}', hi='Salut,',
  body=['Sunt Mateus și administrez Latin Dance Awards, un clasament al școlilor de bachata din Europa. Am adăugat {n} ({c}), care concurează deja cu unele dintre cele mai bune școli din Europa.',
        'Nu am găsit online anul înființării, dacă aveți cursuri pentru începători sau evenimente. Fiecare informație confirmată dă școlii mai multe puncte și o urcă în clasament, iar site-ul are mult trafic, deci poate aduce elevi noi.',
        'Ați putea să-mi răspundeți la aceste trei puncte? Voi actualiza fișa.',
        'Dacă preferați să nu apăreți, spuneți-mi și scot școala.'],
  bye='Mulțumesc,'),
 'el': dict(subj='Μια γρήγορη ερώτηση για τη σχολή {n}', hi='Γεια σας,',
  body=['Είμαι ο Mateus και διαχειρίζομαι το Latin Dance Awards, μια κατάταξη σχολών bachata στην Ευρώπη. Πρόσθεσα τη σχολή {n} ({c}) και ήδη ανταγωνίζεται μερικές από τις καλύτερες σχολές της Ευρώπης.',
        'Δεν βρήκα online το έτος ίδρυσης, αν έχετε μαθήματα για αρχάριους ή εκδηλώσεις. Κάθε στοιχείο που επιβεβαιώνετε δίνει περισσότερους πόντους στη σχολή σας και την ανεβάζει στην κατάταξη, και το site έχει πολλή κίνηση, άρα μπορεί να φέρει νέους μαθητές.',
        'Μπορείτε να μου απαντήσετε σε αυτά τα τρία; Θα ενημερώσω την καταχώριση.',
        'Αν προτιμάτε να μην εμφανίζεστε, πείτε μου και θα αφαιρέσω τη σχολή.'],
  bye='Ευχαριστώ,'),
}
SIG = 'Mateus\nLatin Dance Awards'


def render(lang, n, c):
    t = T[lang]
    parts = [t['hi']] + [p.format(n=n, c=c) for p in t['body']]
    return t['subj'].format(n=n), '\n\n'.join(parts) + '\n\n' + t['bye'] + '\n' + SIG


if __name__ == '__main__':
    for l in T:
        s, b = render(l, 'Example School', 'Berlin')
        print('==', l, '|', s)
    print(render('en', 'Example School', 'Berlin')[1])
