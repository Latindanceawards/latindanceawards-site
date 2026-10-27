# Belgian Bachata schools. Collected 27 Oct 2026: Google Maps rating and review count; Bachata offering confirmed on the school's own
# website (homepage or page title mentions Bachata) or in the Google Maps business name. Only schools with evidence of Bachata classes are included.
# city key -> (Belgian name, English name, name used after "de bachata")
CITIES = {
 'brussels': ('Brussels', 'Brussels', 'in Brussels'),
 'charleroi': ('Charleroi', 'Charleroi', 'in Charleroi'),
}
def _m(n, c): return 'https://www.google.com/maps/search/?api=1&query=' + (n + ' ' + c).replace(' ', '+')
SCHOOLS = [
 ('Brussels Dance Project', 'brussels', 4.8, 50, 'https://www.danceproject.be/'),
 ('Salsa Bruxelles', 'brussels', 4.7, 96, 'https://www.salsabruxelles.be/'),
 ('Caribbean Dance Brussels', 'brussels', 5.0, 17, 'https://atomidance.com/'),
 ('Latin Dance Evolution School', 'brussels', 5.0, 40, 'http://www.latindanceevolution.com/'),
 ('Fuego Dance', 'brussels', 5.0, 15, 'http://www.fuegodance.be/'),
 ('Yuka Dance Academy', 'charleroi', 4.9, 192, 'https://www.yukadanceacademy.be/'),
]
# Scoring data not collected yet for Belgium (years active, beginner offer, events, Instagram, styles).
# Anything not confirmed counts at the lowest value; schools can confirm it through the application.
EXTRA = {}
