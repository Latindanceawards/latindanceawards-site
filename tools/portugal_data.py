# Portuguese Bachata schools. Collected 27 Oct 2026: Google Maps rating and review count; Bachata offering confirmed on the school's own
# website (homepage or page title mentions Bachata) or in the Google Maps business name. Only schools with evidence of Bachata classes are included.
# city key -> (Portuguese name, English name, name used after "de bachata", e.g. "em Lisboa")
CITIES = {
 'lisboa': ('Lisboa', 'Lisbon', 'em Lisboa'),
 'porto': ('Porto', 'Porto', 'no Porto'),
 'faro': ('Faro', 'Faro', 'em Faro'),
 'oeiras': ('Oeiras', 'Oeiras', 'em Oeiras'),
 'braga': ('Braga', 'Braga', 'em Braga'),
 'coimbra': ('Coimbra', 'Coimbra', 'em Coimbra'),
 'aveiro': ('Aveiro', 'Aveiro', 'em Aveiro'),
 'funchal': ('Funchal', 'Funchal', 'em Funchal'),
 'almada': ('Almada', 'Almada', 'em Almada'),
 'leiria': ('Leiria', 'Leiria', 'em Leiria'),
 'sintra': ('Sintra', 'Sintra', 'em Sintra'),
 'portimao': ('Portimão', 'Portimão', 'em Portimão'),
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
 ('Nuno y Rita', 'braga', 4.9, 69, 'https://nunoyrita.com/'),
 ("Ent'Artes Escola de Dança", 'braga', 4.8, 109, 'https://entartes.pt/'),
 ('Backstage Escola de Dança', 'braga', 4.9, 136, 'https://backstage.com.pt/'),
 ('Bracara Team', 'braga', 4.9, 110, 'https://bracarateam.com/'),
 ('Danças Latinas UMinho', 'braga', 4.8, 18, _m('Danças Latinas UMinho', 'Braga')),
 ('Escola de Dança Ritmo Latino', 'coimbra', 4.5, 20, 'https://ritmolatino.pt/'),
 ('Dancenter Academia', 'aveiro', 4.9, 109, 'https://dancenter.pt/'),
 ('Academia R&D', 'aveiro', 4.9, 127, 'https://academiard.com/'),
 ('Dance Soul Academy', 'aveiro', 4.8, 45, 'https://dancesoulacademy.pt/'),
 ('Lpstudio', 'aveiro', 4.8, 25, 'https://lpstudio.pt/'),
 ('Escola de Dança Sandra Leite', 'aveiro', 4.9, 36, 'https://escolasandraleite.pt/'),
 ('OpenDance Madeira', 'funchal', 4.9, 35, 'https://opendancemadeira.com/'),
 ('AS Dance Studios', 'almada', 5.0, 20, 'https://asdancestudios.pt/'),
 ('Passocubano', 'leiria', 4.8, 59, _m('Passocubano', 'Leiria')),
 ('noRITMO', 'leiria', 4.9, 12, 'https://gonza-rodrigues.pt/'),
 ('Escola de Dança Sintra', 'sintra', 5.0, 23, _m('Escola de Dança Sintra', 'Sintra')),
 ('Sintra Dance Academy', 'sintra', 4.7, 47, 'https://aiadanca.com/'),
 ('Soul Dance', 'sintra', 4.8, 47, 'https://souldancestudio.pt/'),
 ('Dance Factory Studios', 'sintra', 4.6, 177, 'https://dancefactory.com.pt/'),
 ('Dança Mais', 'portimao', 5.0, 70, _m('Dança Mais', 'Portimão')),
]
# Scoring data not collected yet for Portugal (years active, beginner offer, events, Instagram followers/posts, styles).
# Anything not confirmed counts at the lowest value; schools can confirm it through the application.
EXTRA = {}
