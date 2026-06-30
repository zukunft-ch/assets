#!/usr/bin/env python3
"""Generate the Die Zukunft favicon from the hero SwissCross geometry.

Mirrors assets/scripts/favicon_studio.html exactly: same occlusion (hidden-line)
renderer, so a params line copied out of the studio reproduces the preview 1:1.

Usage:
  python3 gen_favicon.py "mode=hidden arm=4 thick=1 cubeSize=1 cameraZ=32 fov=60 \
      rotX=1.01 rotY=1.08 stroke=0.3 strokeMode=gradient strokeColor=#3b82f6 \
      fill=#ffffff fillOpacity=0.7 shade=false" > favicon.svg

  python3 gen_favicon.py            # no args -> the shipped defaults below
"""
import math, sys

GRAD = ('<linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#a855f7"/>'
        '<stop offset="50%" stop-color="#3b82f6"/>'
        '<stop offset="100%" stop-color="#06b6d4"/></linearGradient>')
cubeVerts = [(-.5,-.5,-.5),(.5,-.5,-.5),(-.5,.5,-.5),(.5,.5,-.5),
             (-.5,-.5,.5),(.5,-.5,.5),(-.5,.5,.5),(.5,.5,.5)]
faces = [(0,1,3,2,(0,0,-1)),(4,6,7,5,(0,0,1)),(0,2,6,4,(-1,0,0)),
         (1,5,7,3,(1,0,0)),(2,3,7,6,(0,1,0)),(0,4,5,1,(0,-1,0))]
edges = [(0,1),(1,3),(3,2),(2,0),(4,5),(5,7),(7,6),(6,4),(0,4),(1,5),(2,6),(3,7)]

# Shipped favicon parameters (mirror of the studio "Hero match", tuned).
DEFAULTS = dict(mode='hidden', arm=4, thick=1, cubeSize=1.0, cameraZ=32.0,
                fov=60.0, rotX=1.01, rotY=1.08, stroke=0.3, strokeMode='gradient',
                strokeColor='#3b82f6', fill='#ffffff', fillOpacity=0.7, shade=False)

def build(arm, thick):
    p, seen = [], set()
    def add(x,y,z):
        if (x,y,z) not in seen:
            seen.add((x,y,z)); p.append((x,y,z))
    for x in range(-arm,arm+1):
        for y in range(-thick,thick+1):
            for z in range(-thick,thick+1): add(x,y,z)
    for x in range(-thick,thick+1):
        for y in range(-arm,arm+1):
            for z in range(-thick,thick+1): add(x,y,z)
    for x in range(-thick,thick+1):
        for y in range(-thick,thick+1):
            for z in range(-arm,arm+1): add(x,y,z)
    return p

def rot(x,y,z,rx,ry):
    cx,sx = math.cos(rx),math.sin(rx); y1 = y*cx-z*sx; z1 = y*sx+z*cx
    cy,sy = math.cos(ry),math.sin(ry)
    return (x*cy+z1*sy, y1, -x*sy+z1*cy)

def render(o, box=64, pad=3):
    arm, thick, cs = int(o['arm']), int(o['thick']), o['cubeSize']
    cz, fov, rx, ry = o['cameraZ'], o['fov'], o['rotX'], o['rotY']
    pos = build(arm, thick); occ = set(pos)
    f = 1/math.tan((fov*math.pi/180)/2)
    def proj(w):
        pz = w[2]-cz
        if pz >= -0.1: return None
        return (f*w[0]/-pz, f*-w[1]/-pz)
    items = []
    if o['mode'] == 'wire':
        for (cx,cy,cz0) in pos:
            for (a,b) in edges:
                va = rot(cx+cubeVerts[a][0]*cs, cy+cubeVerts[a][1]*cs, cz0+cubeVerts[a][2]*cs, rx, ry)
                vb = rot(cx+cubeVerts[b][0]*cs, cy+cubeVerts[b][1]*cs, cz0+cubeVerts[b][2]*cs, rx, ry)
                pa, pb = proj(va), proj(vb)
                if pa and pb: items.append(('line',(va[2]+vb[2])/2,(pa,pb),0))
    else:
        for (cx,cy,cz0) in pos:
            for (a,b,c,d,n) in faces:
                if (cx+n[0],cy+n[1],cz0+n[2]) in occ: continue
                rw = [rot(cx+cubeVerts[i][0]*cs, cy+cubeVerts[i][1]*cs, cz0+cubeVerts[i][2]*cs, rx, ry)
                      for i in (a,b,c,d)]
                rn = rot(n[0],n[1],n[2],rx,ry)
                cc = [sum(p[k] for p in rw)/4 for k in range(3)]
                view = (-cc[0], -cc[1], cz-cc[2])
                if rn[0]*view[0]+rn[1]*view[1]+rn[2]*view[2] <= 0: continue
                pts = [proj(p) for p in rw]
                if any(p is None for p in pts): continue
                shade = 0.55+0.45*((rn[1]+1)/2)
                items.append(('poly', cc[2], pts, shade))
    if not items:
        return wrap('', box)
    items.sort(key=lambda it: it[1])
    xs, ys = [], []
    for t,_,g,_ in items:
        for p in ((g[0],g[1]) if t=='line' else g):
            xs.append(p[0]); ys.append(p[1])
    minx,maxx,miny,maxy = min(xs),max(xs),min(ys),max(ys)
    sc = (box-2*pad)/max(maxx-minx, maxy-miny)
    ox,oy = (minx+maxx)/2,(miny+maxy)/2
    def T(p): return ((p[0]-ox)*sc+box/2, -(p[1]-oy)*sc+box/2)
    stroke_ref = 'url(#g)' if o['strokeMode']=='gradient' else o['strokeColor']
    sw = o['stroke']
    body = []
    for t, depth, g, shade in items:
        if t == 'line':
            a,b = T(g[0]),T(g[1])
            body.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%s" stroke-linecap="round"/>'
                        % (a[0],a[1],b[0],b[1],stroke_ref,sw)); continue
        pstr = ' '.join('%.2f,%.2f'%T(p) for p in g)
        if o['mode']=='solid':
            fill='url(#g)'; fo=shade if o['shade'] else o['fillOpacity']
        elif o['mode']=='glass':
            fill=o['fill']; fo=(shade if o['shade'] else 1)*o['fillOpacity']
        else:  # hidden
            fill=o['fill']; fo=o['fillOpacity']*(shade if o['shade'] else 1)
        body.append('<polygon points="%s" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"/>'
                    % (pstr, fill, fo, stroke_ref, sw))
    return wrap(''.join(body), box)

def wrap(body, box):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d">'
            '<defs>%s</defs><g>%s</g></svg>\n' % (box, box, GRAD, body))

def parse(argv):
    o = dict(DEFAULTS)
    toks = []
    for a in argv:
        toks += a.split()
    for tok in toks:
        if '=' not in tok: continue
        k,v = tok.split('=',1)
        if k=='fill': k='fill'
        if k in ('mode','strokeMode','strokeColor','fill'):
            o[k]=v
        elif k=='shade':
            o[k]=(v.lower()=='true')
        elif k in o:
            o[k]=float(v)
    return o

if __name__ == '__main__':
    sys.stdout.write(render(parse(sys.argv[1:])))
