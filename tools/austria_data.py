# Austrian Bachata schools. Collected 27 Oct 2026: Google Maps rating and review count; Bachata offering confirmed on the school's own
# website (homepage or page title mentions Bachata) or in the Google Maps business name. Only schools with evidence of Bachata classes are included.
# city key -> (Austrian name, English name, name used after "de bachata")
CITIES = {
 'vienna': ('Vienna', 'Vienna', 'in Vienna'),
 'graz': ('Graz', 'Graz', 'in Graz'),
}
def _m(n, c): return 'https://www.google.com/maps/search/?api=1&query=' + (n + ' ' + c).replace(' ', '+')
SCHOOLS = [
 ('Salsa & Latin Studio Julion', 'vienna', 5.0, 164, 'https://www.latinstudio.at/'),
 ('Salsa Vienna', 'vienna', 5.0, 80, 'https://www.salsavienna.at/'),
 ('MYDANCE Vienna', 'vienna', 4.8, 208, 'https://www.mydance.at/'),
 ('Salsanena Tanzstudio', 'vienna', 4.6, 123, 'https://salsanena.at/'),
 ('Tumbao Dance Studio', 'vienna', 4.9, 87, 'https://www.tumbao.at/'),
 ('Lento Dance Studio', 'vienna', 5.0, 297, 'https://www.lentodance.at/'),
 ('Bachata Bliss by Jules', 'graz', 5.0, 27, 'https://bachatabliss.at/de/'),
 ('Freude am Tanzen', 'graz', 5.0, 57, 'https://www.freudeamtanzen.at/'),
 ('Salsa Madras', 'graz', 4.8, 33, 'https://www.salsamadras.at/'),
]
# Scoring data not collected yet for Austria (years active, beginner offer, events, Instagram, styles).
# Anything not confirmed counts at the lowest value; schools can confirm it through the application.
EXTRA = {}
