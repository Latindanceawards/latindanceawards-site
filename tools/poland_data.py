# Polish Bachata schools. Collected 26 Oct 2026: Google Maps rating and review count; Bachata offering confirmed on the school's own
# website (pages found via site search) or on a Salsa Vida listing. Only schools with confirmed Bachata classes are included.
# city key -> (Polish name, English name, locative "w ...")
CITIES = {
 'warszawa': ('Warszawa', 'Warsaw', 'Warszawie'), 'krakow': ('Kraków', 'Kraków', 'Krakowie'), 'wroclaw': ('Wrocław', 'Wrocław', 'Wrocławiu'),
 'poznan': ('Poznań', 'Poznań', 'Poznaniu'), 'gdansk': ('Gdańsk', 'Gdańsk', 'Gdańsku'), 'lodz': ('Łódź', 'Łódź', 'Łodzi'), 'katowice': ('Katowice', 'Katowice', 'Katowicach'),
}
# (name, city, rating, reviews, website)
SCHOOLS = [
 ('Salsa Libre', 'warszawa', 4.7, 312, 'https://salsalibre.pl'),
 ('The Cuban Place', 'warszawa', 4.6, 113, 'https://thecubanplace.pl'),
 ('ABRA Studio', 'warszawa', 4.8, 273, 'https://www.abra-studio.pl'),
 ('Warsaw Salsa Club', 'warszawa', 4.9, 100, 'http://warsawsalsaclub.pl'),
 ('Dos Mundos', 'warszawa', 4.6, 396, 'https://www.akademiatanca.com.pl/dos-mundos'),
 ('Salsa Passion', 'warszawa', 4.9, 61, 'https://www.salsapassion.eu'),
 ('Szkoła Tańców Karaibskich SHO', 'warszawa', 4.8, 247, 'https://sho.pl'),
 ('LOFToDANCE', 'krakow', 4.8, 396, 'https://loftodance.pl'),
 ('BachataDance.pl', 'krakow', 5.0, 42, 'https://bachatadance.pl'),
 ('KrakowBachata.pl', 'krakow', 5.0, 43, 'https://krakowbachata.pl'),
 ('Forum Tańca', 'krakow', 4.7, 169, 'https://forumtanca.pl'),
 ('Krambo Dance', 'krakow', 4.9, 71, 'https://www.krambo.pl'),
 ('Salsa House Kraków', 'krakow', 4.8, 107, 'https://salsahousekrakow.pl'),
 ('La Rosa Negra', 'wroclaw', 4.7, 317, 'https://www.larosanegra.wroclaw.pl'),
 ('Dance Fever', 'wroclaw', 4.8, 146, 'https://www.salsafever.pl'),
 ('Tropical Dance Studios', 'wroclaw', 4.9, 42, 'https://www.tropical-dance.pl'),
 ('No Limits', 'wroclaw', 4.5, 494, 'https://www.nolimits.art.pl'),
 ('Dance Flow', 'wroclaw', 4.8, 340, 'https://www.danceflow.pl'),
 ('Art Dance', 'poznan', 5.0, 307, 'https://art-dance.com.pl'),
 ('Salsa Siempre', 'poznan', 4.7, 147, 'https://salsasiempre.pl'),
 ('Bailando Poznań', 'poznan', 4.3, 184, 'https://bailandopoznan.pl'),
 ('Art of Move', 'poznan', 4.8, 133, 'https://artofmove.pl'),
 ('So!Salsa', 'gdansk', 4.6, 364, 'https://sosalsa.pl'),
 ('Dance Atelier', 'gdansk', 4.8, 167, 'https://danceatelier.pl'),
 ('Latin Dance Academy', 'lodz', 4.9, 207, 'https://latinacademy.pl'),
 ('TONdance', 'lodz', 4.9, 196, 'https://www.tondance.pl'),
 ('Urban Dance Zone', 'lodz', 4.6, 339, 'http://urbandance.pl'),
 ('Bachata Master Studio', 'lodz', 4.9, 39, 'https://www.bachatamasterstudio.pl'),
 ('La Clave', 'katowice', 4.6, 84, 'https://www.laclave.pl'),
 ('Good Mood', 'katowice', 4.8, 172, 'http://goodmood.dance'),
 ('Mil Pasos', 'katowice', 4.8, 79, 'https://milpasoskatowice.pl'),
]
import math
def pts(r, v):
    """Interim points (max 35): Bayesian Google rating (25) + review volume (10), same formulas as the German ranking."""
    b = (v * r + 25 * 4.32) / (v + 25)
    g = max(0.0, 25 - 17.2 * (5 - b))
    rv = 10 * min(1.0, math.log(1 + v) / math.log(251))
    return round(g + rv, 1)
