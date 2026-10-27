# Swiss Bachata schools. Collected 27 Oct 2026: Google Maps rating and review count; Bachata offering confirmed on the school's own
# website (homepage or page title mentions Bachata) or in the Google Maps business name. Only schools with evidence of Bachata classes are included.
# city key -> (Swiss name, English name, name used after "de bachata")
CITIES = {
 'zurich': ('Zurich', 'Zurich', 'in Zurich'),
 'bern': ('Bern', 'Bern', 'in Bern'),
 'lausanne': ('Lausanne', 'Lausanne', 'in Lausanne'),
 'geneva': ('Geneva', 'Geneva', 'in Geneva'),
}
def _m(n, c): return 'https://www.google.com/maps/search/?api=1&query=' + (n + ' ' + c).replace(' ', '+')
SCHOOLS = [
 ('Salsa People', 'zurich', 4.7, 499, 'https://salsapeople.ch/'),
 ('SalsaRica', 'zurich', 4.7, 207, 'https://www.salsarica.ch/'),
 ('BachaSuave', 'zurich', 5.0, 56, 'https://www.bachasuave.com/'),
 ('Fuego y Pasion', 'zurich', 4.9, 55, 'https://www.salsafuegoypasion.ch/'),
 ('Bachata Bern', 'bern', 5.0, 16, 'https://bachata-bern.ch/'),
 ('Salsaluca', 'bern', 4.8, 45, 'https://www.salsaluca.ch/'),
 ('Bailamos Salsa', 'bern', 4.9, 174, 'https://www.bailamos-salsa.ch/'),
 ('Abailar Tanzschule', 'bern', 5.0, 21, 'https://www.abailar-bern.ch/'),
 ('Aliasalsa', 'lausanne', 4.9, 16, 'https://www.aliasalsa.ch/'),
 ('Salsa y Dulzura', 'lausanne', 4.9, 77, 'https://www.salsalausanne.ch/'),
 ("K'danse Lausanne", 'lausanne', 4.9, 121, 'https://www.kdanse.ch/'),
 ('Rumba y Salsa Lausanne', 'lausanne', 5.0, 39, 'https://rumbaysalsa.ch/'),
 ('Bachata Geneva Dance Studio', 'geneva', 5.0, 73, 'https://bachatagenevastudio.com/'),
]
# Scoring data not collected yet for Switzerland (years active, beginner offer, events, Instagram, styles).
# Anything not confirmed counts at the lowest value; schools can confirm it through the application.
EXTRA = {}
