# UK Bachata schools. Collected 27 Oct 2026: Google Maps rating and review count; Bachata offering confirmed on the school's own
# website (homepage or page title mentions Bachata) or in the Google Maps business name. Only schools with evidence of Bachata classes are included.
# city key -> (UK name, English name, name used after "de bachata")
CITIES = {
 'london': ('London', 'London', 'in London'),
 'manchester': ('Manchester', 'Manchester', 'in Manchester'),
 'bristol': ('Bristol', 'Bristol', 'in Bristol'),
 'glasgow': ('Glasgow', 'Glasgow', 'in Glasgow'),
 'edinburgh': ('Edinburgh', 'Edinburgh', 'in Edinburgh'),
 'nottingham': ('Nottingham', 'Nottingham', 'in Nottingham'),
 'cardiff': ('Cardiff', 'Cardiff', 'in Cardiff'),
}
def _m(n, c): return 'https://www.google.com/maps/search/?api=1&query=' + (n + ' ' + c).replace(' ', '+')
SCHOOLS = [
 ('Salsatropical Dance Company', 'london', 4.8, 507, 'https://salsa-tropical.com/'),
 ('Salsateca Dance School', 'london', 4.9, 113, 'http://www.salsateca.co.uk/'),
 ('Rhythm & Vibes Dance Co', 'london', 4.6, 53, 'https://rvdance.co.uk/events-and-dates/kizomba-party-in-london/'),
 ('Hammersmith Salsa & Bachata Club', 'london', 4.9, 239, 'https://www.incognitodance.com/wednesdays-at-hammersmith-salsa-club-hammersmith-london/'),
 ('Pura Nights Ealing', 'london', 5.0, 137, 'https://linktr.ee/pura.nights'),
 ('Caramelo Latin Dance Academy', 'london', 4.7, 136, 'https://caramelolatindance.co.uk/'),
 ('Rogue Bachata', 'london', 4.9, 8, 'https://roguebachata.com/'),
 ('Salsa Freedom Dance Classes', 'manchester', 4.9, 182, 'https://salsamanchester.co.uk/'),
 ('La Suerte Dance School', 'manchester', 4.8, 71, 'http://www.salsa-manchester.co.uk/'),
 ('Floridita Dance', 'manchester', 5.0, 38, 'https://www.floriditadance.com/'),
 ('Bristol Bachata', 'bristol', 4.9, 39, 'https://bristolbachata.co.uk/'),
 ('Bachatify', 'bristol', 5.0, 59, 'http://www.salsify.co.uk/bachatify'),
 ('Salsa Souls', 'bristol', 4.9, 82, 'https://www.salsasouls.co.uk/'),
 ('Dance4Water Glasgow', 'glasgow', 4.9, 10, 'http://4water.org/glasgow/dance'),
 ('Academia de Salsa', 'glasgow', 4.8, 26, 'http://www.academiadesalsa.com/'),
 ('Latin Roots', 'edinburgh', 4.9, 179, 'https://latinroots.co.uk/'),
 ('Bachata Blues Edinburgh', 'edinburgh', 4.4, 45, 'https://www.bachatablues.com/'),
 ('Bailarte Dance Academy', 'edinburgh', 5.0, 41, 'https://bailarte.co.uk/'),
 ('La Clave Salsa & Bachata', 'nottingham', 4.9, 19, 'https://www.laclaveevents.co.uk/'),
 ('Bachata Movement Cardiff', 'cardiff', 5.0, 17, 'https://www.bachatamovement.co.uk/'),
]
# Scoring data not collected yet for the UK (years active, beginner offer, events, Instagram, styles).
# Anything not confirmed counts at the lowest value; schools can confirm it through the application.
EXTRA = {}
