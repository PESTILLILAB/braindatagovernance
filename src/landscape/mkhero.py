"""Write templates/hero-map.svg (the faint map behind the home-page hero) from geo.json.
Run after mkgeo.py: python3 src/landscape/mkhero.py"""
import json, re, os
H = os.path.join(os.path.dirname(__file__))
g = json.load(open(os.path.join(H, 'geo.json')))
def rnd(d): return re.sub(r'(-?\d+)\.\d', r'\1', d)
paths = ''.join(f'<path d="{rnd(f["d"])}"/>' for f in g['f'] if f['d'])
svg = (f'<svg class="herobg" viewBox="0 0 {g["w"]} {g["h"]}" preserveAspectRatio="xMaxYMid slice" aria-hidden="true">'
       f'<g fill="rgba(255,255,255,.07)" stroke="rgba(255,255,255,.22)" stroke-width="1">{paths}</g></svg>')
open(os.path.join(H, '..', '..', 'templates', 'hero-map.svg'), 'w').write(svg)
print('hero-map.svg', len(svg))
