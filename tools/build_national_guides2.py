# National "how to find a class" guides, part 2:
#   uk/bachata-classes     (keyword "bachata classes"/"bachata classes near me", 210 + 880/mo, SD 28; "bachata dance classes" 210)
#   it/corsi-di-bachata    (keyword "corsi di bachata", 390/mo, SD 17; "bachata per principianti" 320, "corsi di bachata vicino a me" 170)
# Facts come from the schools' own websites (read 9 Nov 2026) and our ranking data. Nothing is invented.
# Run after build_uk.py / build_it.py (and their *_schools.py):  python3 tools/build_national_guides2.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_uk as BU
import build_it as BI
from build import T, crumbs, faq_schema

def lk(u, n):
    return f'<a href="{u}" rel="noopener" target="_blank">{n}</a>'

# ===================================================================== UK
def uk():
    P = BU.P
    N = len(P.SCHOOLS); NC = len(P.CITIES)
    t = T('ng3')
    def p(a): return t('p', a, a)
    def ul(items): return '<ul>' + ''.join(f'<li>{t("span", a, a)}</li>' for a in items) + '</ul>'
    def sec(i, h2, blocks, alt=True): return BU.sec(t, i, (h2, h2), blocks, alt=alt)
    big = ['london', 'bristol', 'edinburgh', 'manchester', 'nottingham', 'glasgow', 'birmingham']
    cl = ', '.join(f'<a href="/uk/bachata-{k}">{P.CITIES[k][0]}</a> ({len(BU.by_city(k))})' for k in big)
    h = BU.hero(t, ('Guide · Bachata classes in the UK', 'Guide · Bachata classes in the UK'),
        ('Bachata classes in the UK: cities, prices and how to choose', 'Bachata classes in the UK: cities, prices and how to choose'),
        ('How Bachata classes work in the UK, what schools publish about levels, trial classes and prices, and how to find a class near you. Based on the schools\' own websites, nothing invented.',
         'How Bachata classes work in the UK, what schools publish about levels, trial classes and prices, and how to find a class near you. Based on the schools\' own websites, nothing invented.'),
        [('cal', f'<b>{N} schools</b> in {NC} cities', f'<b>{N} schools</b> in {NC} cities'), ('check', 'Websites checked in <b>November 2026</b>', 'Websites checked in <b>November 2026</b>')],
        f'<a class="btn btn-gold" href="/uk/">{t("span", "See the UK ranking", "See the UK ranking")}</a>')
    body = ''
    body += sec(1, 'Bachata classes in the UK at a glance',
        p(f'Our list has {N} schools in {NC} UK cities. The cities with the most schools are {cl}. Each city has its own page with the interim standing, based on October 2026 Google data; final results follow in spring 2027.')
        + p('Many schools teach salsa and Bachata together, so a "Bachata class" is often one evening on a salsa school\'s timetable. That is normal: check the day and level, not just the school name.'), alt=False)
    body += sec(2, 'Bachata classes near me: how to find one',
        p('Start from the city, not the postcode: most UK Bachata classes run one or two evenings a week in a hotel function room, church hall or studio, and schools list the venue by name. Open your city page below, pick two or three schools, and compare day, level and price on their own timetable pages.')
        + ul(['Check the <strong>day and time</strong>: Bachata is often a single slot, for example Tuesday evening or Friday at 19:00.',
              'Check the <strong>level label</strong>: "Beginners" and "Improvers" are the two most common names in the schools we read.',
              'Check <strong>whether you can drop in</strong> or must book a course; schools differ.',
              'Check the <strong>venue and how you get there</strong>: several classes are held in hotels or community halls rather than a dance studio.'])
        + p(f'Our city pages: {cl}.'))
    body += sec(3, 'What a class looks like: four real examples',
        p('We read the websites of several schools (November 2026). This is what they publish, as stated; timetables and prices change every term.')
        + '<h3>' + t('span', lk('https://salsa-tropical.com/', 'Salsatropical Dance Company') + ' (London, Holborn)', lk('https://salsa-tropical.com/', 'Salsatropical Dance Company') + ' (London, Holborn)') + '</h3>'
        + ul(['Bachata runs on Tuesdays at the Saw Swee Hock Centre, 1 Sheffield St, WC2A 2AP.',
              'Two levels: Beginners 19:00 to 20:00 and Improvers 20:00 to 21:00, each 60 minutes.',
              'A "Bachata Taster" lesson is listed, with no price or time on the page we read. Prices are on a separate booking page.'])
        + '<h3>' + t('span', lk('https://www.salsasouls.co.uk/', 'Salsa Souls') + ' (Bristol, Clifton)', lk('https://www.salsasouls.co.uk/', 'Salsa Souls') + ' (Bristol, Clifton)') + '</h3>'
        + ul(['Wednesday night at Victoria Methodist Church, 1A Whiteladies Rd: beginners class 8:00 to 9:15pm (75 minutes), doors 7:50pm, social dancing until 10:45pm. The page we read names Bachata as one of its dances but does not say which dance this night teaches, so confirm that before you go.',
              'Published price: £12.30 by card, £12 cash; students £11.30 or £11. There is no booking: "just come along and pay at the door".'])
        + '<h3>' + t('span', lk('https://salsamanchester.co.uk/', 'Salsa Freedom') + ' (Manchester, Castlefield)', lk('https://salsamanchester.co.uk/', 'Salsa Freedom') + ' (Manchester, Castlefield)') + '</h3>'
        + ul(['At The Castlefield Hotel, Liverpool Road, M3 4JR. Bachata Beginners on Fridays 19:00 to 20:00 and Beginners/Improvers on Saturdays 19:00 to 20:00.',
              'Group classes are "£12 per person for 1 hour (cash only)". The site says you can drop in to any class, with no booking or partner required.'])
        + '<h3>' + t('span', lk('https://latinroots.co.uk/', 'Latin Roots') + ' (Edinburgh)', lk('https://latinroots.co.uk/', 'Latin Roots') + ' (Edinburgh)') + '</h3>'
        + ul(['Classes and socials at Shanghai Club, Le Monde Hotel, 16a George Street, EH2 2PF, on Tuesday, Wednesday and Sunday options.',
              'A 4-week Beginner Course for complete beginners, with no partner or prior experience needed, plus an Introductory Session for people who already dance. The academy has four progressive stages; prices are on a separate page.']))
    body += sec(4, 'Prices: what is published and what is not',
        p('The two schools that print a drop-in price on their main page, Salsa Souls and Salsa Freedom, both charge about £12 for one class (£12.30 by card at Salsa Souls, for its Wednesday beginners night). The other schools we read put prices on a separate page or do not state them, so ask before you pay:')
        + ul(['Is the price per class, per term or per month?',
              'Is there a taster, an introductory session or a free first class, and is it deducted if you join?',
              'Is payment cash only, as at Salsa Freedom, or by card?',
              'Is there a student price? Salsa Souls lists one.']), alt=False)
    body += sec(5, 'Bachata for beginners: what to expect',
        p('Pick a class labelled Beginners, even if you have danced before. Beginner classes usually teach the basic step, the hold and how to lead and follow, and many schools say no partner is needed: Salsa Freedom and Latin Roots both state it. Wear comfortable clothes and shoes that slide a little, and arrive a few minutes early; Salsa Souls opens its doors 10 to 15 minutes before class.'))
    body += sec(6, 'How we prepared this guide',
        p('In November 2026 we read the websites of Salsatropical, Salsa Souls, Salsa Freedom and Latin Roots, and use the October 2026 Google figures from our list. Step By Me Dance Studios is on our list, but the page we read lists no Bachata class (it says it teaches ballroom and Latin only), so we do not describe its classes. We include nothing we could not check. Run a school and something is missing? <a href="/bewerbung.html?lang=en">Enter it for free</a> or write to us.'), alt=False)
    faq = [
        ('How much does a Bachata class cost in the UK?', 'How much does a Bachata class cost in the UK?',
         'It depends on the school. Two schools we read publish a drop-in price: Salsa Souls in Bristol charges £12.30 by card (£12 cash) for its Wednesday beginners night and Salsa Freedom in Manchester £12 cash for Bachata classes. Others put prices on a separate page, so ask first.',
         'It depends on the school. Two schools we read publish a drop-in price: Salsa Souls in Bristol charges £12.30 by card (£12 cash) for its Wednesday beginners night and Salsa Freedom in Manchester £12 cash for Bachata classes. Others put prices on a separate page, so ask first.'),
        ('Do I need a partner for a Bachata class?', 'Do I need a partner for a Bachata class?',
         'Usually not. Salsa Freedom and Latin Roots both say no partner is required.',
         'Usually not. Salsa Freedom and Latin Roots both say no partner is required.'),
        ('Can I try a Bachata class before I commit?', 'Can I try a Bachata class before I commit?',
         'Often yes. Salsatropical lists a Bachata Taster, Latin Roots an Introductory Session, and Salsa Souls and Salsa Freedom let you pay at the door. Check the terms with each school.',
         'Often yes. Salsatropical lists a Bachata Taster, Latin Roots an Introductory Session, and Salsa Souls and Salsa Freedom let you pay at the door. Check the terms with each school.'),
        ('Which UK cities have the most Bachata schools?', 'Which UK cities have the most Bachata schools?',
         f'On our list: London ({len(BU.by_city("london"))}), Bristol and Edinburgh ({len(BU.by_city("bristol"))} each), Manchester ({len(BU.by_city("manchester"))}) and Nottingham ({len(BU.by_city("nottingham"))}). Some schools teach salsa and Bachata together.',
         f'On our list: London ({len(BU.by_city("london"))}), Bristol and Edinburgh ({len(BU.by_city("bristol"))} each), Manchester ({len(BU.by_city("manchester"))}) and Nottingham ({len(BU.by_city("nottingham"))}). Some schools teach salsa and Bachata together.'),
        ('How do I find a Bachata class near me?', 'How do I find a Bachata class near me?',
         'Open your city page on our site, compare two or three schools on day, level and price, and confirm the venue before you go. Many classes are held in hotels or community halls.',
         'Open your city page on our site, compare two or three schools on day, level and price, and confirm the venue before you go. Many classes are held in hotels or community halls.'),
        ('When is the UK ranking published?', 'When is the UK ranking published?',
         'In spring 2027. Until then we show an interim standing based on public data from October 2026.',
         'In spring 2027. Until then we show an interim standing based on public data from October 2026.'),
    ]
    body += BU.faq_html(t, faq)
    BU.uk_page('uk/bachata-classes.html', 'uk/bachata-classes.html',
        'Bachata classes in the UK: cities, prices and how to choose',
        'Bachata classes in the UK: what Salsatropical, Salsa Souls, Salsa Freedom and Latin Roots publish about levels, trial classes and prices, and how to find a class near you.',
        'Bachata classes in the UK: cities, prices and how to choose',
        'Bachata classes in the UK: what Salsatropical, Salsa Souls, Salsa Freedom and Latin Roots publish about levels, trial classes and prices, and how to find a class near you.',
        h + body, t.en, [crumbs('Bachata UK', 'uk/index.html'), crumbs('Bachata classes', 'uk/bachata-classes.html'), faq_schema(faq)])

# ===================================================================== ITALIA
def italia():
    P = BI.P
    N = len(P.SCHOOLS); NC = len(P.CITIES)
    t = T('ng4')
    def ul(items): return '<ul>' + ''.join(f'<li>{t("span", a, b)}</li>' for a, b in items) + '</ul>'
    big = ['roma', 'milano', 'torino', 'napoli', 'bologna', 'padova', 'firenze']
    cl_it = ', '.join(f'<a href="/it/bachata-{k}">{P.CITIES[k][0]}</a> ({len(BI.by_city(k))})' for k in big)
    cl_en = ', '.join(f'<a href="/it/bachata-{k}">{P.CITIES[k][1]}</a> ({len(BI.by_city(k))})' for k in big)
    h = BI.hero(t, ('Guida · Corsi di bachata in Italia', 'Guide · Bachata classes in Italy'),
        ('Corsi di bachata in Italia: città, livelli e prezzi', 'Bachata classes in Italy: cities, levels and prices'),
        ('Come funzionano i corsi di bachata in Italia, cosa pubblicano le scuole su livelli, lezioni di prova e prezzi, e come trovare un corso vicino a te. Dai siti delle scuole, senza inventare nulla.',
         'How Bachata classes work in Italy, what schools publish about levels, trial lessons and prices, and how to find a class near you. From the schools\' own websites, nothing invented.'),
        [('cal', f'<b>{N} scuole</b> in {NC} città', f'<b>{N} schools</b> in {NC} cities'), ('check', 'Siti consultati a <b>novembre 2026</b>', 'Websites checked in <b>November 2026</b>')],
        f'<a class="btn btn-gold" href="/it/">{t("span", "Vedi la classifica dell\'Italia", "See the Italy ranking")}</a>')
    body = ''
    body += BI.sec(t, 1, ('Corsi di bachata in Italia a colpo d\'occhio', 'Bachata classes in Italy at a glance'),
        t('p', f'Nel nostro elenco ci sono {N} scuole (alcune con più sedi) in {NC} città italiane. Le città con più scuole sono {cl_it}. Ognuna ha la sua pagina con la classifica provvisoria, basata su dati di ottobre 2026; i risultati definitivi saranno pubblicati in primavera 2027.',
               f'Our list has {N} schools (some with several locations) in {NC} Italian cities. The cities with the most schools are {cl_en}. Each has its own page with the interim standing, based on October 2026 data; final results follow in spring 2027.')
        + t('p', 'In Italia molte scuole insegnano salsa e bachata insieme: alla Timba Tumba di Torino il corso per principianti combina le due danze, mentre i corsi di bachata più avanzati sono separati e più brevi. Prima di iscriverti verifica quindi se il corso che ti interessa è solo di bachata o misto, e quante lezioni di bachata contiene davvero.',
                 'In Italy many schools teach salsa and Bachata together: at Timba Tumba in Turin the beginner course combines the two dances, while the more advanced Bachata courses are separate and shorter. Before enrolling, check whether the course you want is Bachata only or mixed, and how many Bachata lessons it really contains.'), alt=False)
    body += BI.sec(t, 2, ('Come sono organizzati i corsi: esempi reali', 'How classes are organised: real examples'),
        t('p', 'Abbiamo letto i siti di alcune scuole (novembre 2026). Ecco cosa pubblicano, così com\'è; orari e prezzi cambiano ogni anno accademico.',
               'We read the websites of several schools (November 2026). This is what they publish, as stated; timetables and prices change every academic year.')
        + '<h3>' + t('span', lk('https://www.timbatumbadanceacademy.it', 'Timba Tumba Dance Academy') + ' (Torino)', lk('https://www.timbatumbadanceacademy.it', 'Timba Tumba Dance Academy') + ' (Turin)') + '</h3>'
        + ul([('Sede in Via Arnaldo da Brescia 63. Insegna salsa, bachata e bachata sensual, in presenza e online, per tutti i livelli.', 'Based at Via Arnaldo da Brescia 63. Teaches salsa, Bachata and Bachata sensual, in person and online, for all levels.'),
              ('Durata dei corsi dichiarata sul sito: Principiante Salsa&Bachata 4 mesi (16 lezioni); Bachata Style (intermedio) 2 mesi (8 lezioni); Bachata Moderna (avanzato) 2 mesi (8 lezioni); Bachata Sensual 2 mesi (8 lezioni).', 'Course lengths stated on the site: Beginner Salsa&Bachata 4 months (16 lessons); Bachata Style (intermediate) 2 months (8 lessons); Bachata Moderna (advanced) 2 months (8 lessons); Bachata Sensual 2 months (8 lessons).'),
              ('La lezione di prova è gratuita, dura un\'ora ed è disponibile in qualsiasi livello. Il sito non riporta i prezzi dei corsi.', 'The trial lesson is free, lasts an hour and is available at any level. The site does not state course prices.')])
        + '<h3>' + t('span', lk('https://www.phoenixstudiodance.com', 'Phoenix Studio Dance') + ' (Milano)', lk('https://www.phoenixstudiodance.com', 'Phoenix Studio Dance') + ' (Milan)') + '</h3>'
        + ul([('La pagina del corso di Bachata Dominicana lo descrive come adatto a chi vuole compiere i primi passi. Orari e prezzi stanno in pagine separate (calendario corsi e listino prezzi).', 'The Bachata Dominicana course page describes it as suited to those taking their first steps. Timetable and prices are on separate pages (course calendar and price list).'),
              ('Attenzione: la pagina principale segnala che i corsi di Bachata Dominicana non sono disponibili per l\'anno accademico corrente. Conferma con la scuola se il corso è attivo prima di iscriverti.', 'Note: the main page says Bachata Dominicana courses are not available for the current academic year. Confirm with the school whether the course is running before you enrol.')])
        + '<h3>' + t('span', lk('https://latino51.it/', 'Latino51 Academy') + ' (Bologna, San Lazzaro di Savena)', lk('https://latino51.it/', 'Latino51 Academy') + ' (Bologna, San Lazzaro di Savena)') + '</h3>'
        + ul([('Sede in Via Caselle 45, con fermata del bus 19C davanti alla scuola e ampio parcheggio.', 'Located at Via Caselle 45, with the 19C bus stop in front of the school and ample parking.'),
              ('Due corsi di bachata con nome proprio: "Bachata Figurata" e "Bachata Sensual". Il sito ha una voce "Iscrizioni Prove Gratuite" per le prove; livelli, orari e prezzi non sono sulla pagina principale.', 'Two named Bachata courses: "Bachata Figurata" and "Bachata Sensual". The site has an "Iscrizioni Prove Gratuite" (free trial registration) entry; levels, timetable and prices are not on the main page.')])
        + '<h3>' + t('span', lk('https://bailadance.it/', 'Baila Dance') + ' (Roma)', lk('https://bailadance.it/', 'Baila Dance') + ' (Rome)') + '</h3>'
        + ul([('Zona Aurelia, Boccea, Battistini e Cornelia, con due sedi; indirizzo indicato: Via Gregorio XI 211. Dichiara oltre dieci anni di attività e oltre 1300 allievi ogni anno.', 'Aurelia, Boccea, Battistini and Cornelia area, with two locations; stated address: Via Gregorio XI 211. It states over ten years of activity and over 1,300 students a year.'),
              ('Il corso "Salsa e Bachata" ha un pulsante "Prenota una prova"; prezzi, livelli e orari non sono sulla pagina principale.', 'The "Salsa e Bachata" course has a "Prenota una prova" (book a trial) button; prices, levels and timetable are not on the main page.')]))
    body += BI.sec(t, 3, ('Bachata per principianti: da dove cominciare', 'Bachata for beginners: where to start'),
        t('p', 'Se non hai mai ballato, scegli un corso per principianti e non saltare il livello base anche se conosci altri balli. Alla Timba Tumba il corso principianti combina salsa e bachata su 4 mesi e 16 lezioni; la bachata sensual, moderna e "style" arrivano dopo, in corsi più brevi. Il passo base della bachata sono tre passi e un quarto tempo di accento con un tocco di piede o di anca, ripetuto da un lato e dall\'altro.',
               'If you have never danced, choose a beginner course and do not skip the basic level even if you know other dances. At Timba Tumba the beginner course combines salsa and Bachata over 4 months and 16 lessons; sensual, moderna and "style" Bachata come later, in shorter courses. The basic Bachata step is three steps and a fourth beat of accent with a foot or hip tap, repeated to one side and the other.')
        + t('p', 'Quasi tutte le scuole offrono una lezione di prova: Timba Tumba la dà gratis a qualsiasi livello, e la Scuola di Ballo Sampaoli di Torino indica sul suo sito una lezione di prova gratuita. Provala prima di pagare un corso.',
                 'Almost all schools offer a trial lesson: Timba Tumba gives it free at any level, and the Scuola di Ballo Sampaoli in Turin lists a free trial lesson on its website. Try it before paying for a course.'
        + t('p', 'Occhio ai nomi dei corsi: nelle scuole che abbiamo letto compaiono "Bachata Dominicana" (Phoenix Studio, a Milano), "Bachata Sensual" (Timba Tumba, Latino51), "Bachata Moderna" e "Bachata Style" (Timba Tumba) e "Bachata Figurata" (Latino51). Non sono sinonimi: ogni scuola usa i suoi termini, quindi chiedi che cosa si impara in concreto e a quale livello è rivolto il corso, soprattutto se hai già qualche base.',
                 'Watch the course names: the schools we read list "Bachata Dominicana" (Phoenix Studio, Milan), "Bachata Sensual" (Timba Tumba, Latino51), "Bachata Moderna" and "Bachata Style" (Timba Tumba) and "Bachata Figurata" (Latino51). They are not synonyms: each school uses its own terms, so ask what you actually learn and which level the course is aimed at, especially if you already have some basics.')))
    body += BI.sec(t, 4, ('Corsi di bachata vicino a me: come trovarne uno', 'Bachata classes near me: how to find one'),
        t('p', 'Parti dalla città: apri la pagina della tua città nel nostro elenco, scegli due o tre scuole e confronta tipo di bachata (dominicana, sensual, moderna, figurata), livello e sede. Molte scuole hanno più sedi nella stessa città, quindi controlla l\'indirizzo.',
               'Start from the city: open your city page in our list, pick two or three schools and compare the Bachata type (dominicana, sensual, moderna, figurata), level and location. Many schools have several locations in the same city, so check the address.')
        + t('p', f'Le nostre pagine di città: {cl_it}.', f'Our city pages: {cl_en}.'), alt=False)
    body += BI.sec(t, 5, ('Prezzi e domande da fare', 'Prices and what to ask'),
        t('p', 'Nelle pagine che abbiamo letto non c\'è nessun prezzo dei corsi: le scuole li mettono in un listino a parte o li comunicano su richiesta. Anche un annuncio su Emagister per un corso a Roma riporta "Prezzo da consultare". Prima di iscriverti chiedi:',
               'In the pages we read there are no course prices: schools put them on a separate price list or give them on request. Even an Emagister listing for a course in Rome says "Prezzo da consultare" (price on request). Before you enrol, ask:')
        + ul([('Quanto costa il corso intero e quante lezioni comprende (per esempio 8 o 16)?', 'How much does the whole course cost and how many lessons does it include (for example 8 or 16)?'),
              ('La lezione di prova è gratuita o si paga e viene scalata?', 'Is the trial lesson free, or paid and deducted?'),
              ('Il corso è attivo quest\'anno? (Phoenix Studio segnala la Bachata Dominicana come non disponibile sulla pagina principale.)', 'Is the course running this year? (Phoenix Studio flags Bachata Dominicana as unavailable on its main page.)'),
              ('Che stile di bachata si insegna e a quale livello?', 'Which Bachata style is taught and at what level?')]))
    body += BI.sec(t, 6, ('Come abbiamo preparato questa guida', 'How we prepared this guide'),
        t('p', 'A novembre 2026 abbiamo letto i siti di Timba Tumba Dance Academy, Phoenix Studio Dance, Latino51 Academy, Baila Dance e Scuola di Ballo Sampaoli, e usiamo le cifre del nostro elenco di ottobre 2026. Dove un sito non riporta orari o prezzi non li inventiamo. Hai una scuola e manca qualcosa? <a href="/bewerbung.html?lang=en">Iscrivila gratis</a> o scrivici.',
               'In November 2026 we read the websites of Timba Tumba Dance Academy, Phoenix Studio Dance, Latino51 Academy, Baila Dance and Scuola di Ballo Sampaoli, and use the figures from our October 2026 list. Where a site gives no timetable or price we do not invent one. Run a school and something is missing? <a href="/bewerbung.html?lang=en">Enter it for free</a> or write to us.'), alt=False)
    faq = [
        ('Quanto costa un corso di bachata in Italia?', 'How much does a Bachata course in Italy cost?',
         'Dipende dalla scuola, e nelle pagine che abbiamo letto non ci sono prezzi: li comunicano su richiesta o in un listino separato. Chiedi sempre il costo dell\'intero corso e quante lezioni comprende.',
         'It depends on the school, and the pages we read show no prices: they give them on request or in a separate price list. Always ask for the cost of the whole course and how many lessons it includes.'),
        ('Posso provare una lezione di bachata gratis?', 'Can I try a Bachata lesson for free?',
         'Spesso sì. Timba Tumba (Torino) offre una lezione di prova gratuita di un\'ora a qualsiasi livello; anche la Scuola di Ballo Sampaoli (Torino) indica una prova gratuita, e Latino51 (Bologna) ha una voce "Iscrizioni Prove Gratuite".',
         'Often yes. Timba Tumba (Turin) offers a free one-hour trial lesson at any level; the Scuola di Ballo Sampaoli (Turin) also lists a free trial, and Latino51 (Bologna) has a "Iscrizioni Prove Gratuite" entry.'),
        ('Quanto dura un corso di bachata?', 'How long is a Bachata course?',
         'Alla Timba Tumba il corso principianti di salsa e bachata dura 4 mesi (16 lezioni), mentre Bachata Style, Bachata Moderna e Bachata Sensual durano 2 mesi (8 lezioni). Altre scuole non indicano la durata sulla pagina principale.',
         'At Timba Tumba the beginner salsa and Bachata course lasts 4 months (16 lessons), while Bachata Style, Bachata Moderna and Bachata Sensual last 2 months (8 lessons). Other schools do not state the length on the main page.'),
        ('Serve un partner per i corsi di bachata?', 'Do I need a partner for Bachata courses?',
         'Di solito no: nei corsi di gruppo si cambia partner. Chiedilo alla scuola prima della prima lezione.',
         'Usually not: in group courses partners change. Ask the school before the first lesson.'),
        ('In quali città italiane ci sono più scuole di bachata?', 'Which Italian cities have the most Bachata schools?',
         f'Nel nostro elenco: Roma ({len(BI.by_city("roma"))}), Milano ({len(BI.by_city("milano"))}), Torino e Napoli ({len(BI.by_city("torino"))} ciascuna), Bologna e Padova ({len(BI.by_city("bologna"))} ciascuna). Alcune scuole hanno più sedi.',
         f'On our list: Rome ({len(BI.by_city("roma"))}), Milan ({len(BI.by_city("milano"))}), Turin and Naples ({len(BI.by_city("torino"))} each), Bologna and Padua ({len(BI.by_city("bologna"))} each). Some schools have several locations.'),
        ('Quando sarà pubblicata la classifica dell\'Italia?', 'When is the Italy ranking published?',
         'In primavera 2027. Fino ad allora mostriamo una classifica provvisoria basata su dati pubblici di ottobre 2026.',
         'In spring 2027. Until then we show an interim standing based on public data from October 2026.'),
    ]
    body += BI.faq_html(t, faq)
    BI.it_page('it/corsi-di-bachata.html', 'it/corsi-di-bachata.html',
        'Corsi di bachata in Italia: città, livelli e prezzi',
        'Corsi di bachata in Italia: come funzionano livelli, lezioni di prova e durata dei corsi a Torino, Milano, Bologna e Roma, e cosa chiedere alla scuola prima di iscriverti.',
        'Bachata classes in Italy: cities, levels and prices',
        'Bachata classes in Italy: how levels, trial lessons and course length work in Turin, Milan, Bologna and Rome, and what to ask the school before you enrol.',
        h + body, t.en, [crumbs('Bachata Italia', 'it/index.html'), crumbs('Corsi di bachata', 'it/corsi-di-bachata.html'), faq_schema(faq)])

uk(); italia()
