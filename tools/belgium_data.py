# Belgian Bachata schools. Collected 27 Oct 2026: Google Maps rating and review count; Bachata offering confirmed on the school's own
# website (homepage or page title mentions Bachata) or in the Google Maps business name. Only schools with evidence of Bachata classes are included.
# city key -> (Belgian name, English name, name used after "de bachata")
CITIES = {
 'brussels': ('Brussels', 'Brussels', 'in Brussels'),
 'charleroi': ('Charleroi', 'Charleroi', 'in Charleroi'),
 'antwerpen': ('Antwerpen', 'Antwerpen', 'in Antwerpen'),
 'gent': ('Gent', 'Gent', 'in Gent'),
 'leuven': ('Leuven', 'Leuven', 'in Leuven'),
 'brugge': ('Brugge', 'Brugge', 'in Brugge'),
 'hasselt': ('Hasselt', 'Hasselt', 'in Hasselt'),
 'kortrijk': ('Kortrijk', 'Kortrijk', 'in Kortrijk'),
 'mons': ('Mons', 'Mons', 'in Mons'),
}
def _m(n, c): return 'https://www.google.com/maps/search/?api=1&query=' + (n + ' ' + c).replace(' ', '+')
SCHOOLS = [
 ('Brussels Dance Project', 'brussels', 4.8, 50, 'https://www.danceproject.be/'),
 ('Salsa Bruxelles', 'brussels', 4.7, 96, 'https://www.salsabruxelles.be/'),
 ('Caribbean Dance Brussels', 'brussels', 5.0, 17, 'https://atomidance.com/'),
 ('Latin Dance Evolution School', 'brussels', 5.0, 40, 'http://www.latindanceevolution.com/'),
 ('Fuego Dance', 'brussels', 5.0, 15, 'http://www.fuegodance.be/'),
 ('Yuka Dance Academy', 'charleroi', 4.9, 192, 'https://www.yukadanceacademy.be/'),
 ('Salsadansen', 'antwerpen', 4.9, 36, 'https://salsadansen.be/'),
 ('Salsa Charanga', 'antwerpen', 4.8, 24, 'https://deleukstesalsafamilie.be/'),
 ('Bailando Latino', 'antwerpen', 4.9, 15, 'https://bailandolatino.be/'),
 ('WeDance Gent', 'gent', 5.0, 15, 'https://wedance.be/'),
 ('The Embassy Room', 'brussels', 4.4, 335, 'https://theembassyroombrussels.be/'),
 ('BeSalsa', 'brussels', 5.0, 13, 'https://besalsa.com/'),
 ('Quierobailar', 'brussels', 4.9, 19, 'https://quierobailar.be/'),
 ('Bachata Vice Dance School', 'brussels', 5.0, 29, 'https://bachatavice.com/'),
 ('LeuvenSalsa', 'leuven', 4.9, 64, 'https://leuvensalsa.com/'),
 ('Dance con Emoción', 'leuven', 4.9, 28, 'https://bachataconemocion.be/'),
 ('Cuban Salsa Leuven', 'leuven', 4.9, 83, 'https://cubansalsaleuven.be/'),
 ('Salsaflash', 'leuven', 5.0, 25, 'https://salsaflash.be/'),
 ('B-salsa', 'brugge', 5.0, 18, 'https://b-salsa.be/'),
 ("Ritmo Studio's", 'hasselt', 4.7, 71, 'https://ritmostudios.be/'),
 ('Pura Vida Bachata', 'kortrijk', 5.0, 11, 'https://puravida-bachata.be/'),
 ('Asisalsa', 'mons', 4.9, 19, 'https://asisalsa.be/'),
]
# Scoring data not collected yet for Belgium (years active, beginner offer, events, Instagram, styles).
# Anything not confirmed counts at the lowest value; schools can confirm it through the application.
EXTRA = {}
