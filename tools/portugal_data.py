# Portuguese Bachata schools. Collected 27 Oct 2026: Google Maps rating and review count; Bachata offering confirmed on the school's own
# website (homepage or page title mentions Bachata) or in the Google Maps business name. Only schools with evidence of Bachata classes are included.
# city key -> (Portuguese name, English name, name used after "de bachata", e.g. "em Lisboa")
CITIES = {
 'lisboa': ('Lisboa', 'Lisbon', 'em Lisboa'),
 'porto': ('Porto', 'Porto', 'no Porto'),
 'faro': ('Faro', 'Faro', 'em Faro'),
 'oeiras': ('Oeiras', 'Oeiras', 'em Oeiras'),
}
def _m(n, c): return 'https://www.google.com/maps/search/?api=1&query=' + (n + ' ' + c).replace(' ', '+')
SCHOOLS = [
 ('Estúdio Sabor & Dança', 'lisboa', 4.9, 116, 'https://www.estudiosaboredanca.pt'),
 ('Dança e Companhia', 'lisboa', 5.0, 19, 'https://www.dancacompanhia.com'),
 ('Latin Dance Hub', 'lisboa', 5.0, 11, _m('Latin Dance Hub', 'Lisboa')),
 ('Porto com Salsa', 'porto', 5.0, 350, 'https://www.portocomsalsa.com'),
 ('Academia Salsa Algarve', 'faro', 5.0, 114, 'https://www.salsa-algarve.com'),
 ('Marcos Figueirinha', 'faro', 5.0, 67, 'https://www.marcosfigueirinha.dance'),
 ('Oeiras Dance Academy', 'oeiras', 4.7, 71, 'https://www.oeirasdance.pt'),
]
# Scoring data not collected yet for Portugal (years active, beginner offer, events, Instagram followers/posts, styles).
# Anything not confirmed counts at the lowest value; schools can confirm it through the application.
EXTRA = {}
