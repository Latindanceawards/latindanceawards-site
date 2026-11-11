#!/usr/bin/env python3
"""Berlin pages: distinct school profiles per page intent (hub / course finder / school comparison),
curated internal links. Facts verified from school sites, Nov 2026. Idempotent. Run from repo root."""
import json, re

def S(slug, lang): return ('/en/schools/%s' % slug) if lang == 'en' else ('schools/%s' % slug)

def ext(url, label): return '<a href="%s" rel="noopener">%s</a>' % (url, label)

# ---- texts: {page: {key: (de, en)}}  (lang-specific profile links added by builder fn)
def hub(l):
    p = lambda s: S(s, l)
    pr = ('Profil', 'Profile')[l == 'en']
    return {
 'bb19': ('Friedrichshain, Samariterstraße 34. Bachata Sensual und Conscious Bachata, kostenlose Probestunde. <a href="%s">%s</a>',
          'Friedrichshain, Samariterstraße 34. Bachata Sensual and Conscious Bachata, free trial class. <a href="%s">%s</a>', 'bachatacademy'),
 'bb21': ('Schöneberg. Bachata Sensual und Moderna, dienstags vier Levels nacheinander. <a href="%s">%s</a>',
          'Schöneberg. Bachata Sensual and Moderna, four levels back to back on Tuesdays. <a href="%s">%s</a>', 'la-mambita'),
 'bb23': ('Schöneberg, Hauptstraße 30. Offene Salsa- und Bachata-Klassen für alle Level, dazu Club-Abende.',
          'Schöneberg, Hauptstraße 30. Open Salsa and Bachata classes for all levels, plus club nights.', None),
 'bb25': ('Kreuzberg. Bachata, Bachata Sensual und Salsa-&-Bachata-Kurse, dazu Wochenend-Bootcamps. <a href="%s">%s</a>',
          'Kreuzberg. Bachata, Bachata Sensual and Salsa & Bachata courses, plus weekend bootcamps. <a href="%s">%s</a>', 'cumbancha-tanzschule'),
 'bb27': ('Schöneberg, Kolonnenstraße 29. Bachata Sensual in vier Levels, Probestunde 5,50 €. <a href="%s">%s</a>',
          'Schöneberg, Kolonnenstraße 29. Bachata Sensual in four levels, trial class 5.50 €. <a href="%s">%s</a>', 'zapatissimo'),
 'bb29': ('Drei Standorte: Tempelhofer Flughafen, Westfälische Straße und Mariendorf. Bachata gehört zu den Trend- und Szenetänzen. <a href="%s">%s</a>',
          'Three sites: Tempelhof Airport, Westfälische Straße and Mariendorf. Bachata is listed under trend and scene dances. <a href="%s">%s</a>', 'tanzschule-traumtaenzer'),
    }

KURS = {  # course finder: formats, levels, trial, price, booking
 'bkb19': ('Wochenkurse im Studio. Einstieg über eine kostenlose, unverbindliche Probestunde, du brauchst weder Erfahrung noch Partner, die Partner wechseln im Kurs.',
           'Weekly courses at the studio. You can start with a free, no-obligation trial class, and you need neither experience nor a partner, because partners rotate in class.'),
 'bkb21': ('Wochenkurse (Buchung über Eversports), Wochenend-Bootcamps, mehrmonatige Intensivkurse und Privatstunden, auch ohne Partner. Neukunden bekommen laut Website einen kostenlosen Probeabend, zeitlich begrenzt. ' + ext('https://cumbancha.de/bachata-berlin/', 'Bachata-Seite'),
           'Weekly courses (booked via Eversports), weekend bootcamps, multi-month intensives and private lessons, also without a partner. According to the website, first-time customers get a free trial evening, for a limited time. ' + ext('https://cumbancha.de/bachata-berlin/', 'Bachata page')),
 'bkb23': ('Offene Salsa- und Bachata-Klassen mittwochs, freitags und samstags (laut Urban Sports Club), von Anfängern bis Fortgeschrittenen, ohne Partner, ab 18 Jahren. Gebucht wird über die Urban-Sports-Club-App.',
           'Open Salsa and Bachata classes on Wednesdays, Fridays and Saturdays (per Urban Sports Club), from beginners to advanced, no partner needed, 18 and over. Booking is through the Urban Sports Club app.'),
 'bkb25': ('Dienstags laufen vier Levels nacheinander, Drop-in ist möglich und Urban Sports Club wird akzeptiert. Schwerpunkt Bachata Sensual und Moderna.',
           'On Tuesdays four levels run back to back, drop-in is possible and Urban Sports Club is accepted. Focus on Bachata Sensual and Moderna.'),
 'bkb27': ('Bachata hat eine eigene Kursseite, Level und Preise sind dort nicht ausgewiesen. Die Schule nennt allgemein einen kostenlosen Schnuppertermin. ' + ext('https://www.traumtaenzer.de/tanzkurse/bachata/', 'Kursseite'),
           'Bachata has its own course page, which does not state levels or prices. The school mentions a free trial session in general. ' + ext('https://www.traumtaenzer.de/tanzkurse/bachata/', 'Course page')),
 'bkb29': ('Offene Klassen mit oder ohne Partner: montags 18:00 Anfänger und 19:00 Anfänger mit Vorkenntnissen, freitags 18:00 Anfänger mit Vorkenntnissen und 19:00 Mittelstufe. Einzelstunde 12 €, Probestunde 5,50 € (Stand November 2026). Anmeldung bis 18 Uhr am Vortag, die Kurse laufen bei genug Anmeldungen. Dazu Bootcamps, Workshops und Privatstunden. ' + ext('https://zapatissimo.de/bachata-kurse-berlin/', 'Kursseite'),
           'Open classes with or without a partner: Mondays 6 pm beginners and 7 pm beginners with some experience, Fridays 6 pm beginners with some experience and 7 pm intermediate. Single class 12 €, trial class 5.50 € (as of November 2026). Sign up by 6 pm the day before; classes run if enough people register. Plus bootcamps, workshops and private lessons. ' + ext('https://zapatissimo.de/bachata-kurse-berlin/', 'Course page')),
}
TANZ = {  # school character: who it suits
 'btb19': ('Studio in Friedrichshain (Samariterstraße 34) mit Bachata im Namen und im Programm: zwölf genannte Lehrer, Bachata Sensual und Conscious Bachata. Passt, wenn du den Fokus auf einen Tanz willst.',
           'Studio in Friedrichshain (Samariterstraße 34) with Bachata in its name and programme: twelve named teachers, Bachata Sensual and Conscious Bachata. Suits you if you want a focus on one dance.'),
 'btb21': ('Latin-Tanzschule in Kreuzberg, laut eigener Website seit mehr als 25 Jahren aktiv. Bachata läuft neben Salsa in den regulären Wochenkursen. Passt, wenn du beide Tänze an einem Ort lernen willst.',
           'Latin dance school in Kreuzberg, active for more than 25 years according to its own website. Bachata runs alongside Salsa in the regular weekly courses. Suits you if you want to learn both dances in one place.'),
 'btb23': ('Tanzschule im Club in Schöneberg (Hauptstraße 30): Kurs und Party am selben Ort, mittwochs gibt es eine Salsa-&-Bachata-Nacht. Passt, wenn du nach dem Kurs gleich tanzen gehen willst.',
           'Dance school inside the club in Schöneberg (Hauptstraße 30): class and party in the same place, with a Salsa & Bachata night on Wednesdays. Suits you if you want to go dancing right after class.'),
 'btb25': ('Studio in Schöneberg mit Schwerpunkt auf modernen Stilen: Bachata Sensual und Moderna, dazu kurze Ausflüge in Dominicana. Passt, wenn du einen festen Abend suchst, der vom Einstieg bis zur Fortgeschrittenen-Stufe aufbaut.',
           'Studio in Schöneberg focused on modern styles: Bachata Sensual and Moderna, with short excursions into Dominicana. Suits you if you want a fixed evening that builds from entry level to advanced.'),
 'btb27': ('Tanzschule mit drei Berliner Standorten (Tempelhofer Flughafen, Westfälische Straße, Mariendorf), Bachata zählt zu den Trend- und Szenetänzen im Programm. Passt, wenn du im Süden oder Westen Berlins wohnst und ein breites Tanzschul-Programm möchtest.',
           'Dance school with three Berlin sites (Tempelhof Airport, Westfälische Straße, Mariendorf); Bachata is listed among the trend and scene dances. Suits you if you live in the south or west of Berlin and want a broad dance school programme.'),
 'btb29': ('Studio in Schöneberg (Kolonnenstraße 29) mit klarem Stilfokus auf Bachata Sensual und festem Wochenplan über vier Level-Stufen. Passt, wenn du Sensual Schritt für Schritt nach Level lernen willst.',
           'Studio in Schöneberg (Kolonnenstraße 29) with a clear focus on Bachata Sensual and a fixed weekly schedule across four levels. Suits you if you want to learn Sensual step by step by level.'),
}
HUB_INTRO = {  # appended to bb17
 'de': ' Kursformate, Zeiten und Preise stehen auf <a href="bachata-kurs-berlin">Bachata Kurs Berlin</a>, den Vergleich der Schulen findest du auf <a href="bachata-tanzschule-berlin">Bachata Tanzschule Berlin</a>.',
 'en': ' Class formats, times and prices are on <a href="/en/bachata-kurs-berlin">Bachata class Berlin</a>, and the school comparison is on <a href="/en/bachata-tanzschule-berlin">Bachata dance school Berlin</a>.'}
KEEP = ['bachata-hamburg','bachata-leipzig','bachata-dresden','bachata-sensual','bachata-dominicana','bachata-grundschritt','bachata-fuer-anfaenger','bachata-festivals-deutschland','bachata-kurs-berlin','bachata-tanzschule-berlin','bachata-berlin','bachata-staedte-deutschland','rankings']

def get_dict(h):
    k = h.index('var EN=') + len('var EN=')
    d, e = json.JSONDecoder().raw_decode(h, k)
    return d, k, e

def set_p(h, key, txt):
    pat = re.compile(r'(<p data-i18n="%s">)(.*?)(</p>)' % key, re.S)
    assert pat.search(h), key
    return pat.sub(lambda m: m[1] + txt + m[3], h, 1)

def process(f, lang, texts, intro=None):
    h = open(f, encoding='utf8').read()
    if 'berlin_fix:done' in h: return
    d, k, e = get_dict(h)
    for key, v in texts.items():
        de_t, en_t = v[0], v[1]
        if len(v) > 2 and v[2]:   # profile link
            pr = ('Profil', 'Profile')
            de_t = de_t % (S(v[2], 'de'), pr[0]); en_t = en_t % (S(v[2], 'en'), pr[1])
        html_t = en_t if lang == 'en' else de_t
        h = set_p(h, key, html_t)
        d[key] = en_t
    if intro:
        key = intro
        m = re.search(r'<p data-i18n="%s">(.*?)</p>' % key, h, re.S)
        add_de, add_en = HUB_INTRO['de'], HUB_INTRO['en']
        base_de = re.sub(r'<a.*', '', m[1]) if False else m[1]
        h = h.replace(m[0], '<p data-i18n="%s">%s%s</p>' % (key, m[1], add_en if lang == 'en' else add_de), 1)
        d[key] = d.get(key, '') + add_en
    # curated links
    i = h.index('class="citylinks"'); j = h.index('</div>', i)
    seg = h[i:j]
    anchors = re.findall(r'<a href="[^"]+"><span data-i18n="[^"]+">[^<]*</span></a>', seg)
    keep = [a for a in anchors if re.match(r'<a href="(?:/en/)?(?:%s)(?:#.*)?"' % '|'.join(KEEP), a)]
    selfname = f.split('/')[-1][:-5]
    keep = [a for a in keep if not re.match(r'<a href="(?:/en/)?%s"' % selfname, a)]
    h = h[:i] + 'class="citylinks">' + ''.join(keep) + h[j:] if False else h[:i] + seg[:seg.index('>') + 1] + ''.join(keep) + h[j:]
    # rewrite dict
    ser = json.dumps(d, ensure_ascii=False)
    h = h[:k] + ser + h[e:]
    h = h.replace('</head>', '<!-- berlin_fix:done -->\n</head>', 1)
    open(f, 'w', encoding='utf8').write(h)

for lang, pre in (('de', ''), ('en', 'en/')):
    process(pre + 'bachata-berlin.html', lang, hub(lang), intro='bb17')
    process(pre + 'bachata-kurs-berlin.html', lang, KURS)
    process(pre + 'bachata-tanzschule-berlin.html', lang, TANZ)
print('done')
