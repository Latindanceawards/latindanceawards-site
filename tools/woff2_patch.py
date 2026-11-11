#!/usr/bin/env python3
"""Adds WOFF2 sources (and preloads) before the existing WOFF ones in all html. Idempotent."""
import re,glob
pat=re.compile(r'url\(([^)]*?)\.woff\)\s*format\("woff"\)')
pre=re.compile(r'(<link rel="preload" href="[^"]*?)\.woff(" as="font" type=")font/woff(")')
for f in glob.glob('**/*.html',recursive=True):
    s=open(f,encoding='utf8').read();o=s
    s=pat.sub(lambda m:'url(%s.woff2) format("woff2"),url(%s.woff) format("woff")'%(m[1],m[1]),s)
    s=pre.sub(lambda m:m[1]+'.woff2'+m[2]+'font/woff2'+m[3],s)
    if s!=o: open(f,'w',encoding='utf8').write(s)
