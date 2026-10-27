# French Bachata schools. Collected 27 Oct 2026: Google Maps rating and review count; Bachata offering confirmed on the school's own
# website (homepage or page title mentions Bachata) or in the Google Maps business name. Only schools with evidence of Bachata classes are included.
# city key -> (French name, English name, name used after "de bachata", e.g. "à Paris")
CITIES = {
 'paris': ('Paris', 'Paris', 'à Paris'),
 'lyon': ('Lyon', 'Lyon', 'à Lyon'),
 'marseille': ('Marseille', 'Marseille', 'à Marseille'),
 'toulouse': ('Toulouse', 'Toulouse', 'à Toulouse'),
 'bordeaux': ('Bordeaux', 'Bordeaux', 'à Bordeaux'),
 'nantes': ('Nantes', 'Nantes', 'à Nantes'),
 'strasbourg': ('Strasbourg', 'Strasbourg', 'à Strasbourg'),
 'montpellier': ('Montpellier', 'Montpellier', 'à Montpellier'),
 'rennes': ('Rennes', 'Rennes', 'à Rennes'),
 'grenoble': ('Grenoble', 'Grenoble', 'à Grenoble'),
}
def _m(n, c): return 'https://www.google.com/maps/search/?api=1&query=' + (n + ' ' + c).replace(' ', '+')
SCHOOLS = [
 ('SalsaNueva Paris', 'paris', 4.9, 443, 'https://www.salsanueva.fr'),
 ('Salsabor Paris', 'paris', 4.8, 171, 'https://salsabor.fr'),
 ('Salsa con Elegua', 'paris', 5.0, 409, 'https://www.elegua.fr'),
 ('VueltaSol', 'paris', 5.0, 49, 'https://vueltasol.com'),
 ('Bachata Vibe Paris', 'paris', 4.8, 33, _m('Bachata Vibe Paris', 'Paris')),
 ('Lyon Salsa Bachata', 'lyon', 4.9, 65, 'https://lyonsalsabachata.com'),
 ('Studio Dime Que Si', 'lyon', 4.8, 36, 'https://www.dimequesi.fr'),
 ('Full Dance', 'lyon', 5.0, 109, 'https://www.full-dance.com'),
 ('Salsaddict', 'lyon', 4.6, 28, 'https://www.salsaddict.fr'),
 ('Cindy Martin Danseuse', 'lyon', 5.0, 229, 'https://danselyon.fr'),
 ('Latin Wave', 'marseille', 4.8, 50, 'https://www.latinwave.fr'),
 ('Marseille Danse Academy', 'marseille', 4.7, 122, 'https://marseille-danse-academy.fr'),
 ('Latin Project', 'marseille', 5.0, 44, 'https://www.latinproject.fr'),
 ('Studio 2000', 'marseille', 4.8, 60, 'https://studio-2000.net'),
 ('Salsamars', 'marseille', 5.0, 69, 'https://www.salsamars.com'),
 ('Latino Caliente', 'toulouse', 4.4, 39, 'https://www.latinocaliente.fr'),
 ('Encas-Danses Studio', 'toulouse', 4.9, 364, 'https://www.encas-danses.com'),
 ('PuntaTalon Academy', 'toulouse', 5.0, 29, 'https://www.puntatalonacademy.com'),
 ('Republica Latina', 'bordeaux', 4.9, 12, 'https://republicalatinafr.blogspot.com'),
 ('Pulsación Bachata', 'nantes', 5.0, 1, 'https://www.pulsacionbachata.com'),
 ('Bachata Fusion Strasbourg', 'strasbourg', 5.0, 211, 'https://www.bachatafusionstrasbourg.fr'),
 ('Momoa Bachata', 'strasbourg', 5.0, 42, 'https://www.strasbourgbachata.com'),
 ('Bachata Club Strasbourg', 'strasbourg', 5.0, 9, 'https://www.bachataclub.fr'),
 ('Ritmo Loco', 'montpellier', 4.9, 63, 'https://www.ritmoloco.fr'),
 ('Alma Dance', 'montpellier', 4.9, 205, 'https://www.almadance.fr'),
 ('Urban Latino Dance Studio', 'montpellier', 4.9, 175, 'https://urbanlatinoacademy.com'),
 ('Zak y Giusy Bachata Sensual', 'montpellier', 5.0, 2, 'https://zakygiusy.com'),
 ("Salsolyk's Dance Company", 'rennes', 4.8, 5, 'https://www.salsolyk.com'),
 ('Bailasi Rennes', 'rennes', 5.0, 14, 'https://www.bailasi.fr'),
 ('Cubanizate', 'rennes', 5.0, 3, _m('Cubanizate', 'Rennes')),
 ('Kosta Danse', 'grenoble', 4.7, 252, 'https://www.ecole-kosta-danse.fr'),
 ('Studio Garlisi', 'grenoble', 4.8, 290, 'https://www.studio-garlisi.fr'),
]
# Scoring data not collected yet for France (years active, beginner offer, events, Instagram followers/posts, styles).
# Anything not confirmed counts at the lowest value; schools can confirm it through the application.
EXTRA = {}
