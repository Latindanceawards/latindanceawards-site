# Recurring Bachata socials, sourced from public listings (Salsa Vida) and organizer sites. Stand: October 2026.
# Fields: city key, name, venue, address, rec (DE, EN), time (DE, EN), price, site (organizer, https only), src (listing).
# Only add entries you can source. Organizers can ask for changes or removal by email.
SV = 'https://www.salsavida.com/?p='
EVENTS = [
 # Berlin
 dict(city='berlin', name='Wednesday Salsa & Bachata Night', venue='HAVANNA Berlin', addr='Hauptstraße 30, 10827 Berlin',
      rec=('Jeden Mittwoch', 'Every Wednesday'), time=('Kurs 19:00, Party 20:00 bis 03:00', 'Class 7 pm, party 8 pm to 3 am'), price='7 €',
      site='https://www.havanna-berlin.de/wednesday', src=SV + '23773'),
 dict(city='berlin', name='Soda Social Club', venue='Soda Club Berlin', addr='Schönhauser Allee 36, 10435 Berlin',
      rec=('Jeden Donnerstag und Sonntag', 'Every Thursday and Sunday'), time=('Kurs 19:00, Party 20:00 bis 02:00', 'Class 7 pm, party 8 pm to 2 am'), price='8 € + 3 € Getränkegutschein',
      site='https://soda-berlin.de/soda-social-club', src=SV + '33767'),
 dict(city='berlin', name='SalsOli Salsa & Bachata Social', venue='Tanzschule Tangoloft', addr='Pfuelstraße 5, 10997 Berlin',
      rec=('Jeden Freitag', 'Every Friday'), time=('ab 19:00', 'from 7 pm'), price='8 €',
      site='', src=SV + '73386'),
 # Hamburg
 dict(city='hamburg', name='A Bailar Party (Salsa, Bachata, Kizomba)', venue='A Bailar Hamburg', addr='Eiffestraße 664b, 20537 Hamburg',
      rec=('Monatlich, meist samstags', 'Monthly, usually on a Saturday'), time=('Einlass 19:30, Workshop 20:00, Party 21:00 bis 03:00', 'Doors 7:30 pm, workshop 8 pm, party 9 pm to 3 am'), price='10 € (Studenten frei)',
      site='https://www.abailar-hamburg.de/a-bailarparty', src=SV + '97483'),
 dict(city='hamburg', name='Sensual Night', venue='A Bailar Hamburg', addr='Eiffestraße 664b, 20537 Hamburg',
      rec=('Jeden 2. Samstag im Monat', 'Every 2nd Saturday of the month'), time=('21:00 bis 03:00', '9 pm to 3 am'), price='10 € inkl. Workshop',
      site='https://www.abailar-hamburg.de/aktuelle-informationen', src=SV + '91958'),
 dict(city='hamburg', name='Bachata Loca', venue='Tango Chocolate', addr='Dehnhaide 55, 22081 Hamburg',
      rec=('Jeden 3. Samstag im Monat', 'Every 3rd Saturday of the month'), time=('Kurse 21:00, Social ab 22:00', 'Classes 9 pm, social from 10 pm'), price='',
      site='https://tango-chocolate.de/events', src=SV + '91957'),
 dict(city='hamburg', name='TIMBATON Fridays', venue='Tango Chocolate', addr='Dehnhaide 55, 22081 Hamburg',
      rec=('Jeden Freitag', 'Every Friday'), time=('Workshop 21:30, Party ab 22:15', 'Workshop 9:30 pm, party from 10:15 pm'), price='10 € inkl. Workshop',
      site='', src=SV + '92174'),
 dict(city='hamburg', name='ICB Sunday', venue='ICB Studios HafenCity', addr='Kehrwieder 5, 20457 Hamburg',
      rec=('Jeden Sonntag', 'Every Sunday'), time=('19:00 bis 23:00', '7 pm to 11 pm'), price='10 €',
      site='https://icbstudios.com/de/kurs-buchen/', src=SV + '91959'),
 # München
 dict(city='muenchen', name='Salsea Bachata Party', venue='Salsea Dance Academy', addr='Heßstraße 48b, 80798 München',
      rec=('Jeden Freitag', 'Every Friday'), time=('ab 20:00', 'from 8 pm'), price='8 € + 2 € Gutschein',
      site='https://salsea.de/das-studio/', src=SV + '91945'),
 dict(city='muenchen', name='Bachata Sensual & Salsa Sunday Party', venue='Salsa OnStage', addr='Neumarkter Straße 71, 81673 München',
      rec=('Jeden Sonntag', 'Every Sunday'), time=('ab 20:00', 'from 8 pm'), price='10 €',
      site='https://www.salsa-onstage.de/events/onstage-sunday/', src=SV + '91944'),
 dict(city='muenchen', name='Bachata Social Freitag', venue='Salsamás Pasing', addr='Am Schützeneck 3, 81241 München',
      rec=('Jeden Freitag', 'Every Friday'), time=('Social 20:30 bis 22:00', 'Social 8:30 pm to 10 pm'), price='7,50 €',
      site='https://www.salsamas-pasing.de/', src=SV + '96902'),
 # Köln
 dict(city='koeln', name='Latin Sunday', venue='Cuba-Bar', addr='Zülpicher Straße 25, 50674 Köln',
      rec=('Jeden Sonntag', 'Every Sunday'), time=('Bachata-Workshop 18:30, Social bis 01:00', 'Bachata workshop 6:30 pm, social until 1 am'), price='10 € inkl. Social',
      site='https://baila-tanzen-lernen.de/', src=SV + '23796'),
 dict(city='koeln', name='Radio Sabor', venue='Club Bahnhof Ehrenfeld', addr='Bartholomäus-Schink-Straße 67, 50825 Köln',
      rec=('Jeden 3. Samstag im Monat', 'Every 3rd Saturday of the month'), time=('23:00 bis 05:00', '11 pm to 5 am'), price='12 bis 24 €',
      site='https://radiosabor.de', src=SV + '23798'),
 # Frankfurt
 dict(city='frankfurt', name='Camino Dance: Salsa & Bachata Social', venue='Academia de Tango', addr='Sonnemannstraße 3, 60314 Frankfurt',
      rec=('Jeden Sonntag (Start 1. November 2026)', 'Every Sunday (starts November 1, 2026)'), time=('19:00 bis 00:00', '7 pm to midnight'), price='8 €',
      site='', src=SV + '97709'),
 dict(city='frankfurt', name='Bachata Nacht', venue='MyZeil', addr='Zeil 106, 60313 Frankfurt',
      rec=('Jeden Donnerstag', 'Every Thursday'), time=('Workshop 20:00, Party 22:00 bis 01:00', 'Workshop 8 pm, party 10 pm to 1 am'), price='10 €',
      site='https://www.myzeil.de/events/salsa-night-e43824/', src=SV + '33317'),
]
CITY_LABEL = {'berlin': ('Berlin', 'Berlin'), 'hamburg': ('Hamburg', 'Hamburg'), 'muenchen': ('München', 'Munich'),
              'koeln': ('Köln', 'Cologne'), 'frankfurt': ('Frankfurt', 'Frankfurt')}

# Weekday numbers (0=Monday) and whether a class or workshop runs before the party (from the listings). Monthly events: weekday only.
META = {
 'Wednesday Salsa & Bachata Night': ([2], True, False), 'Soda Social Club': ([3, 6], True, False), 'SalsOli Salsa & Bachata Social': ([4], None, False),
 'A Bailar Party (Salsa, Bachata, Kizomba)': ([5], True, True), 'Sensual Night': ([5], True, True), 'Bachata Loca': ([5], True, True),
 'TIMBATON Fridays': ([4], True, False), 'ICB Sunday': ([6], None, False),
 'Salsea Bachata Party': ([4], True, False), 'Bachata Sensual & Salsa Sunday Party': ([6], None, False), 'Bachata Social Freitag': ([4], True, False),
 'Latin Sunday': ([6], True, False), 'Radio Sabor': ([5], False, True),
 'Camino Dance: Salsa & Bachata Social': ([6], None, False), 'Bachata Nacht': ([3], True, False),
}  # name -> (weekdays, class_before (None = not stated), monthly)
WD = [('Montag', 'Monday'), ('Dienstag', 'Tuesday'), ('Mittwoch', 'Wednesday'), ('Donnerstag', 'Thursday'), ('Freitag', 'Friday'), ('Samstag', 'Saturday'), ('Sonntag', 'Sunday')]
