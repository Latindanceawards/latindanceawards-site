# Dutch Bachata schools. Collected 27 Oct 2026: Google Maps rating and review count; Bachata offering confirmed on the school's own
# website (homepage or page title mentions Bachata) or in the Google Maps business name. Only schools with evidence of Bachata classes are included.
# city key -> (Dutch name, English name, name used after "de bachata", e.g. "in Amsterdam")
CITIES = {
 'amsterdam': ('Amsterdam', 'Amsterdam', 'in Amsterdam'),
 'rotterdam': ('Rotterdam', 'Rotterdam', 'in Rotterdam'),
 'utrecht': ('Utrecht', 'Utrecht', 'in Utrecht'),
 'denhaag': ('Den Haag', 'Den Haag', 'in Den Haag'),
 'eindhoven': ('Eindhoven', 'Eindhoven', 'in Eindhoven'),
 'groningen': ('Groningen', 'Groningen', 'in Groningen'),
 'tilburg': ('Tilburg', 'Tilburg', 'in Tilburg'),
 'breda': ('Breda', 'Breda', 'in Breda'),
 'nijmegen': ('Nijmegen', 'Nijmegen', 'in Nijmegen'),
 'arnhem': ('Arnhem', 'Arnhem', 'in Arnhem'),
}
def _m(n, c): return 'https://www.google.com/maps/search/?api=1&query=' + (n + ' ' + c).replace(' ', '+')
SCHOOLS = [
 ('Salsa4Fun', 'amsterdam', 5.0, 107, 'https://salsa4fun.com/'),
 ('Baila Bel Air', 'amsterdam', 4.7, 46, 'http://www.bailabelair.nl/'),
 ('Salsa District', 'amsterdam', 4.9, 115, 'https://www.salsadistrict.nl/'),
 ('Onda Latin Dance', 'amsterdam', 5.0, 27, 'https://ondadance.nl/'),
 ('Extremos Salsa & Bachata', 'amsterdam', 4.8, 333, _m('Extremos Salsa & Bachata', 'Amsterdam')),
 ('Typical Tropical Events', 'rotterdam', 4.8, 53, 'https://typicaltropical.nl/'),
 ('Latin Bootcamp', 'rotterdam', 4.9, 101, 'https://latinbootcamp.nl/'),
 ('Dansschool MamboMike', 'rotterdam', 4.8, 17, 'https://www.mambomike.nl/'),
 ('Latin Supreme', 'rotterdam', 5.0, 200, 'http://www.latinsupreme.nl/'),
 ('Salsadansschool SuriHarold', 'rotterdam', 4.9, 69, 'http://www.suriharold4salsa.nl/'),
 ('Union Dance Company', 'utrecht', 4.7, 107, 'http://www.unionsalsadancecompany.nl/'),
 ('Nova Dance Utrecht', 'utrecht', 4.9, 118, 'https://www.novadance.nl/'),
 ('Bachata Passion Utrecht', 'utrecht', 5.0, 21, 'https://www.bachata-passion.com/utrecht'),
 ('MUSIQUITA Dance Community', 'utrecht', 5.0, 45, 'https://musiquita.nl/'),
 ('La Bodeguita', 'denhaag', 4.6, 138, 'http://www.labodeguita.nl/'),
 ('Dansschool El Ritmo', 'denhaag', 5.0, 26, 'https://www.elritmo.nl/'),
 ('Bachata Passion Den Haag', 'denhaag', 4.9, 121, 'http://www.bachata-passion.com/den-haag'),
 ('Salsa Prisiri', 'denhaag', 4.8, 23, 'http://www.salsaprisiri.nl/'),
 ('The Latin Dance Studio', 'eindhoven', 4.8, 75, 'https://www.thelatindancestudio.nl/'),
 ('Salsa Sensation Dansschool', 'eindhoven', 4.9, 65, 'https://salsasensation.online/'),
 ('Passion2Dance', 'eindhoven', 4.9, 68, 'https://www.passion2dance.nl/'),
 ('Bachata Dansschool El Bachatero', 'groningen', 5.0, 8, _m('Bachata Dansschool El Bachatero', 'Groningen')),
 ('Latin Touch Dance Academy', 'tilburg', 5.0, 29, 'https://latintouch.nl/'),
 ('Marlon Salsipuedes', 'tilburg', 5.0, 177, 'http://www.dansenintilburg.nl/'),
 ('ZoukMotion', 'breda', 4.2, 19, 'https://www.zoukmotion.nl/'),
 ('Bachata Passion Nijmegen', 'nijmegen', 5.0, 20, 'http://www.bachata-passion.com/nijmegen'),
 ('Watapana Dance Company', 'arnhem', 5.0, 81, 'https://watapanadc.com/'),
 ('Salsa Contigo', 'arnhem', 4.9, 159, 'https://www.salsacontigo.nl/'),
]
# Scoring data not collected yet for the Netherlands (years active, beginner offer, events, Instagram, styles).
# Anything not confirmed counts at the lowest value; schools can confirm it through the application.
EXTRA = {}
