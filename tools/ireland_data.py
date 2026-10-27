# Irish Bachata schools. Collected 27 Oct 2026: Google Maps rating and review count; Bachata offering confirmed on the school's own
# website (homepage or page title mentions Bachata) or in the Google Maps business name. Only schools with evidence of Bachata classes are included.
# city key -> (Irish name, English name, name used after "de bachata")
CITIES = {
 'dublin': ('Dublin', 'Dublin', 'in Dublin'),
 'galway': ('Galway', 'Galway', 'in Galway'),
}
def _m(n, c): return 'https://www.google.com/maps/search/?api=1&query=' + (n + ' ' + c).replace(' ', '+')
SCHOOLS = [
 ('Dublin Salsa Academy', 'dublin', 4.9, 393, _m('Dublin Salsa Academy', 'Dublin')),
 ('Galway Latin Dance', 'galway', 5.0, 28, 'https://latindance.ie/'),
]
# Scoring data not collected yet for Ireland (years active, beginner offer, events, Instagram, styles).
# Anything not confirmed counts at the lowest value; schools can confirm it through the application.
EXTRA = {}
