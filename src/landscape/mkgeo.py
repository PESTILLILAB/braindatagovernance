import sys
"""Build geo.json: projected SVG paths (equirectangular, standard parallel 25°) for the Legal landscape maps."""
import json, math
T = json.load(open(sys.argv[1]))  # path to world-atlas countries-50m.json (npm package world-atlas)
M = json.load(open('matrix.json'))
sc, tr = T['transform']['scale'], T['transform']['translate']

def arc(i):
    rev = i < 0
    a = T['arcs'][~i if rev else i]
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy
        pts.append((x*sc[0]+tr[0], y*sc[1]+tr[1]))
    return pts[::-1] if rev else pts

def ring(arcs):
    pts = []
    for i in arcs:
        p = arc(i)
        pts += p if not pts else p[1:]
    return pts

# name mapping topo -> matrix
ALIAS = {'Congo': 'Republic of the Congo', "Côte d'Ivoire": "Cote d'Ivoire",
         'Dem. Rep. Congo': 'Democratic Republic of the Congo', 'eSwatini': 'Eswatini',
         'Gambia': 'The Gambia', 'São Tomé and Principe': 'Sao Tome and Principe',
         'Dominican Rep.': 'Dominican Republic'}
NAMES = set(M['names'])

# Equirectangular projection with standard parallel PHI1 (degrees). Shapes are close to true in the
# tropics and areas are only moderately distorted; Equal Earth (used earlier) kept areas exact but
# drew the tropics about a third taller than wide, which read as a stretched map.
LON0 = -35
PHI1 = 25
W, H = 980, 560
def proj(lon, lat):
    lam = math.radians(lon - LON0); phi = math.radians(lat)
    return lam*math.cos(math.radians(PHI1)), -phi
# window
xs = [proj(lo, la) for lo in (-170, 60) for la in (-58, 72)]
minx = proj(-128, 0)[0]; maxx = proj(60, 0)[0]
miny = proj(LON0, 72)[1]; maxy = proj(LON0, -58)[1]
S = W/(maxx-minx); H = int((maxy-miny)*S)
def px(lon, lat):
    x, y = proj(lon, lat)
    return (x-minx)*S, (y-miny)*S

def simplify(pts, tol=1.1):
    out = [pts[0]]
    for p in pts[1:]:
        if abs(p[0]-out[-1][0]) + abs(p[1]-out[-1][1]) >= tol:
            out.append(p)
    return out

def area(pts):
    return abs(sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))))/2

feats = []
for g in T['objects']['countries']['geometries']:
    nm = g['properties']['name']; key = ALIAS.get(nm, nm)
    polys = g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]
    d = []; cx = cy = n = 0; big = 0
    for poly in polys:
        for r in poly[:1]:  # outer rings only
            pts = [px(*p) for p in ring(r)]
            if not pts: continue
            if max(p[0] for p in pts) < 0 or min(p[0] for p in pts) > W or max(p[1] for p in pts) < 0 or min(p[1] for p in pts) > H:
                continue
            if max(p[0] for p in pts) - min(p[0] for p in pts) > 600: continue  # ring wraps the antimeridian (Russia, Fiji): would draw a line across the map
            a = area(pts)
            if a < 4 and key not in NAMES: continue
            if a > big:
                big = a; cx = sum(p[0] for p in pts)/len(pts); cy = sum(p[1] for p in pts)/len(pts)
            sp = simplify(pts)
            if len(sp) < 3: continue
            d.append('M' + ' '.join(f'{p[0]:.1f},{p[1]:.1f}' for p in sp) + 'Z')
    if not d and key not in NAMES: continue
    if not d and key in NAMES:  # tiny island: marker only
        pts = [px(*p) for p in ring(polys[0][0])]
        cx = sum(p[0] for p in pts)/len(pts); cy = sum(p[1] for p in pts)/len(pts); big = 0
    feats.append({'n': key, 'd': ''.join(d), 'c': [round(cx, 1), round(cy, 1)], 'a': round(big, 1),
                  'k': key in NAMES, 'na': nm in ('United States of America', 'Canada')})
have = {f['n'] for f in feats if f['k']}
print('missing', NAMES - have)
print('tiny', [f['n'] for f in feats if f['k'] and f['a'] < 20])
json.dump({'w': W, 'h': H, 'f': feats}, open('geo.json', 'w'), separators=(',', ':'))
import os; print(os.path.getsize('geo.json'), H)
