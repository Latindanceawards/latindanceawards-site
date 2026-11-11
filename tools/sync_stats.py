#!/usr/bin/env python3
"""Single source for headline counts: data/stats.json. Rewrites count sentences on pages. Idempotent.
Usage: python3 tools/sync_stats.py [--check]"""
import json,re,sys
S=json.load(open('data/stats.json'));n=S['de']['schools']
FILES=['deutschland.html','en/deutschland.html']
PATS=[(r'(scores |Germany, |aktuell |bewertet )\d+( Bachata schools| schools so far| Schulen| Bachata-Schulen)',lambda m:m[1]+str(n)+m[2])]
bad=0
for f in FILES:
    s=open(f,encoding='utf8').read();o=s
    for p,r in PATS:s=re.sub(p,r,s)
    if s!=o:
        bad+=1
        if '--check' not in sys.argv:open(f,'w',encoding='utf8').write(s)
print('changed' if bad else 'ok',bad)
