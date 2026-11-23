"""Draws the animated "Where it sits" diagram (desktop + phone SVG) into src/pages/product.html, between the hub markers.
Run: python3 hub_diagram.py, then python3 build.py. Reduced-motion viewers get the still picture.
Colours: grey = data from systems, teal = recorded evidence, navy = changed run, orange = active step."""
import base64, math, pathlib, re
R = pathlib.Path(__file__).resolve().parent
MARK = base64.b64encode((R/'assets/probanda-mark-on-dark.svg').read_bytes()).decode()
NAVY, TEAL, MINT, MUT, RULE, SURF, GREY, ORG = '#0E1B2D','#11786F','#2FD3C0','#5F646A','#D3DCDB','#EEF2F3','#8A949E','#E8650A'
D = 12  # loop, seconds
def k(*v): return ';'.join(f'{x/D:.4f}' for x in v)
def T(x,y,s,size=15,w=400,c=NAVY,a='start'): return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{c}" text-anchor="{a}">{s}</text>'
def B(x,y,w,h,fill='#fff',st=RULE,r=12,sw=1.5): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{st}" stroke-width="{sw}"/>'
def line(p,c,m,w=2.5): return f'<path d="{p}" fill="none" stroke="{c}" stroke-width="{w}" marker-end="url(#{m})"/>'
def on(el,a,b): # show el from a to b seconds
    tag = el[1:el.index(' ')]
    return el.replace('/>',f' opacity="0"><animate attributeName="opacity" dur="{D}s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;{k(a,a+.2,b,b+.25)};1"/></{tag}>')
def glow(x,y,w,h,a,b,sw=4): return on(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" stroke="{ORG}" stroke-width="{sw}"/>',a,b)
def lit(p,a,b): return on(f'<path d="{p}" fill="none" stroke="{ORG}" stroke-width="4"/>',a,b)
def dot(p,a,b,r=7): return (f'<circle r="{r}" fill="{ORG}" opacity="0"><animateMotion dur="{D}s" repeatCount="indefinite" calcMode="linear" path="{p}" keyPoints="0;0;1;1" keyTimes="0;{k(a,b)};1"/>'
    f'<animate attributeName="opacity" dur="{D}s" repeatCount="indefinite" calcMode="discrete" values="0;1;0" keyTimes="0;{k(a,b)}"/></circle>')
def block(cx,cy,i,a,b): return on(f'<rect x="{cx-112+i*60}" y="{cy+4}" width="44" height="44" rx="8" fill="{ORG}" fill-opacity=".6" stroke="{ORG}" stroke-width="3"/>',a,b)
SRC = [('Agent platforms','Joule, AgentCore, Agentforce'),('Gateways','Tool calls, MCP, APIs'),('Identity','Who acted, for whom'),
       ('Business systems','SAP, Salesforce, Workday'),('Policy and approvals','Rule applied, who approved'),('Monitoring','Traces, logs, alerts')]
USE = [('Replay','See what happened, step by step.'),('Re-run','Run it many times: how stable is the result?'),('What-if re-run','Change one factor: how far does it move?')]
PACK = 'Evidence pack for audit, risk and incident review'
def hub(cx,cy,r):
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{NAVY}"/><image href="data:image/svg+xml;base64,{MARK}" x="{cx-24}" y="{cy-132}" width="48" height="48"/>',
         T(cx,cy-52,'Probanda AI',22,600,'#fff','middle'), T(cx,cy-26,'Tamper-evident record',16,500,MINT,'middle')]
    for i in range(4):
        x = cx-112+i*60
        if i: o.append(f'<path d="M{x-16} {cy+26}H{x}" stroke="{MINT}" stroke-width="2.5"/>')
        o.append(f'<rect x="{x}" y="{cy+4}" width="44" height="44" rx="8" fill="#172638" stroke="{MINT}" stroke-width="2"/><path d="M{x+11} {cy+20}h22M{x+11} {cy+32}h14" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>')
    return o+[T(cx,cy+80,'Each entry is linked to the last.',14,400,'#D6E2F2','middle'), T(cx,cy+100,'Edits and deletions are detectable.',14,400,'#D6E2F2','middle')]
def bars(x,base,hs,c,cls): return ''.join(f'<rect class="{cls}" style="--k:{i}" x="{x+i*13}" y="{base-h}" width="11" height="{h}" rx="2" fill="{c}"/>' for i,h in enumerate(hs) if h)
def card(i,x,y):
    o = [B(x,y,356,128), T(x+20,y+32,USE[i][0],19,600), T(x+20,y+55,USE[i][1],15,400,'#4A5058')]
    base = y+116
    if i == 0:
        o.append(f'<path d="M{x+28} {y+92}H{x+220}" stroke="{TEAL}" stroke-width="2.5"/>'+''.join(f'<circle cx="{x+28+j*48}" cy="{y+92}" r="6" fill="{TEAL}"/>' for j in range(5))+T(x+242,y+97,'Recorded',13,600,TEAL))
    else: o.append(f'<path d="M{x+20} {base+1}H{x+228}" stroke="#8A939C" stroke-width="1.5"/>')
    if i == 1: o += [bars(x+24,base,[0,0,0,2,5,12,25,42,27,13,5,2],TEAL,'hub-br'), f'<path d="M{x+120.5} {base}V{base-50}" stroke="{NAVY}" stroke-width="2" stroke-dasharray="4 3"/>', T(x+138,base-36,'Recorded result',13,500), T(x+242,base-3,'Many runs',13,600,TEAL)]
    if i == 2: o += [bars(x+24,base,[2,5,13,27,42,26,12,5,2],TEAL,'hub-bb'), bars(x+102,base,[2,5,12,24,36,25,11,4,1],NAVY,'hub-bw'), T(x+242,base-25,'Same rule',13,600,TEAL), T(x+242,base-3,'Rule changed',13,600)]
    return o
def steps(cx,cy,outs,cards): # record, replay, re-run, what-if
    o = [block(cx,cy,i,3.1+i*.45,3.45+i*.45) for i in range(4)]
    for i,(x,y) in enumerate(cards):
        a = 5+i*2.0
        o += [block(cx,cy,b,a,a+.25) for b in ((2,) if i == 2 else range(4))]
        if outs[i]: o += [lit(outs[i],a+.2,a+.55), dot(outs[i],a+.2,a+.65)]
        o.append(glow(x,y,356,128,a+.6,a+1.65))
        if i == 0: o.append(dot(f'M{x+28} {y+92}H{x+220}',a+.65,a+1.75,9))
    return o
def wrap(vb,cls,base,anim):
    def mk(n,c): return f'<marker id="{cls}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="{c}"/></marker>'
    body = ''.join(base).replace('url(#','url(#'+cls+'-')
    return f'<svg viewBox="{vb}" class="{cls}" aria-hidden="true" focusable="false" font-family="Inter,Arial,sans-serif"><defs>{mk("t",TEAL)}{mk("g",GREY)}</defs>{body}<g class="hub-anim">{"".join(anim)}</g></svg>'
def desktop():
    cx,cy,r = 610,368,158
    b = [T(52,136,'Evidence from any system',15,600,MUT), T(1228,136,'Use the record',15,600,MUT,'end')]; an = []
    for i,(n,s) in enumerate(SRC):
        y = 152+i*73; m = y+31; ey = cy+(m-cy)*.34; ex = cx-math.sqrt((r+10)**2-(ey-cy)**2)
        p = f'M316 {m} C 390 {m}, 390 {ey:.0f}, {ex:.0f} {ey:.0f}'; a = .2+i*.42
        b += [B(52,y,262,62), T(70,y+26,n,17,600), T(70,y+47,s,14,400,MUT), line(p,GREY,'g',2)]
        an += [glow(52,y,262,62,a,a+.3,3), lit(p,a+.1,a+.5), dot(p,a+.1,a+.75)]
    b += hub(cx,cy,r); outs = []; cards = [(872,152+i*145) for i in range(3)]
    for i,(x,y) in enumerate(cards):
        m = y+64; ey = cy+(m-cy)*.5; sx = cx+math.sqrt((r+4)**2-(ey-cy)**2)
        outs.append(f'M{sx:.0f} {ey:.0f} C 820 {ey:.0f}, 800 {m}, 862 {m}')
        b += card(i,x,y)+[line(outs[i],TEAL,'t')]
    b += [line('M610 530V594',TEAL,'t'), B(340,600,540,50,SURF,SURF), T(cx,631,PACK,17,600,NAVY,'middle')]
    an += steps(cx,cy,outs,cards)+[lit('M610 530V590',10.95,11.2), dot('M610 530V590',10.9,11.2), glow(340,600,540,50,11.15,11.55)]
    return wrap('48 116 1184 540','hub-d',b,an)
def pcard(i,x,y,h): # compact card for phones
    o = [B(x,y,356,h), T(x+16,y+26,USE[i][0],17,600), T(x+16,y+47,USE[i][1],15,400,'#4A5058')]
    base = y+h-12
    if i == 0: return o+[f'<path d="M{x+22} {base-8}H{x+214}" stroke="{TEAL}" stroke-width="2.5"/>'+''.join(f'<circle cx="{x+22+j*48}" cy="{base-8}" r="6" fill="{TEAL}"/>' for j in range(5)), T(x+238,base-3,'Recorded',13.5,600,TEAL)]
    o.append(f'<path d="M{x+16} {base+1}H{x+224}" stroke="#8A939C" stroke-width="1.5"/>')
    if i == 1: o += [bars(x+20,base,[0,0,0,2,4,10,21,36,23,11,4,2],TEAL,'hub-br'), f'<path d="M{x+116.5} {base}V{base-42}" stroke="{NAVY}" stroke-width="2" stroke-dasharray="4 3"/>', T(x+134,base-28,'Recorded result',13.5,500), T(x+238,base-3,'Many runs',13.5,600,TEAL)]
    if i == 2: o += [bars(x+20,base,[2,4,11,23,36,22,10,4,2],TEAL,'hub-bb'), bars(x+98,base,[2,4,10,20,31,21,9,4,1],NAVY,'hub-bw'), T(x+238,base-22,'Same rule',13.5,600,TEAL), T(x+238,base-3,'Rule changed',13.5,600)]
    return o
def phone():
    cx = 180; b = [T(2,16,'Evidence from any system',15,600,MUT)]; an = []
    for i,(n,_) in enumerate(SRC): # names only, two columns
        x = 2+i%2*182; y = 26+i//2*48; a = .2+i*.42
        b += [B(x,y,174,40,r=10), T(x+87,y+26,n,15,600,NAVY,'middle')]
        an.append(glow(x,y,174,40,a,a+.3,3))
    p = 'M180 164V186'; b.append(line(p,GREY,'g',2)); an += [lit(p,.3,2.8)]+[dot(p,.35+i*.42,.75+i*.42,6) for i in range(6)]
    cy = 250 # panel 192-374
    b += [B(2,192,356,182,NAVY,NAVY,16), f'<image href="data:image/svg+xml;base64,{MARK}" x="68" y="206" width="36" height="36"/>', T(116,222,'Probanda AI',18,600,'#fff'), T(116,242,'Tamper-evident record',15,500,MINT)]
    for i in range(4):
        x = cx-112+i*60
        if i: b.append(f'<path d="M{x-16} {cy+26}H{x}" stroke="{MINT}" stroke-width="2.5"/>')
        b.append(f'<rect x="{x}" y="{cy+4}" width="44" height="44" rx="8" fill="#172638" stroke="{MINT}" stroke-width="2"/><path d="M{x+11} {cy+20}h22M{x+11} {cy+32}h14" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>')
    b += [T(cx,326,'Each entry is linked to the last.',14,400,'#D6E2F2','middle'), T(cx,348,'Edits and deletions are detectable.',14,400,'#D6E2F2','middle')]
    q = 'M180 378V400'; b += [line(q,TEAL,'t'), T(2,402,'Use the record',15,600,MUT)]
    cards = [(2,412,88),(2,508,112),(2,628,112)]
    for i,c in enumerate(cards): b += pcard(i,*c)
    an += [block(cx,cy,i,3.1+i*.45,3.45+i*.45) for i in range(4)]
    for i,(x,y,h) in enumerate(cards):
        a = 5+i*2.0
        an += [block(cx,cy,j,a,a+.25) for j in ((2,) if i == 2 else range(4))]
        an += [lit(q,a+.2,a+.55), dot(q,a+.2,a+.65,6), glow(x,y,356,h,a+.6,a+1.65)]
        if i == 0: an.append(dot(f'M{x+22} {y+68}H{x+214}',a+.65,a+1.75,9))
    e = 'M180 744V766'; b += [line(e,TEAL,'t'), B(2,772,356,44,SURF,SURF), T(cx,799,PACK,14.5,600,NAVY,'middle')]
    an += [lit(e,10.95,11.2), dot(e,10.9,11.2,6), glow(2,772,356,44,11.15,11.55)]
    return wrap('0 0 360 820','hub-m',b,an)
def kf(n,a): return (f'@keyframes {n}{{0%,{(a-.2)/D*100:.2f}%{{transform:scaleY(1)}}{a/D*100:.2f}%,{(a+.5)/D*100:.2f}%{{transform:scaleY(0)}}{(a+1.1)/D*100:.2f}%,100%{{transform:scaleY(1)}}}}'
    f'.{n}{{transform-box:fill-box;transform-origin:50% 100%;animation:{n} {D}s linear infinite;animation-delay:calc(var(--k)*25ms)}}')
CSS = kf('hub-br',7)+kf('hub-bw',9)+'.hub svg{display:block;width:100%;height:auto}.pb.pb .hub .hub-m{display:none}@media(max-width:900px){.pb.pb .hub .hub-d{display:none}.pb.pb .hub .hub-m{display:block;max-width:420px!important;margin:0 auto}}@media(prefers-reduced-motion:reduce){.hub-anim{display:none}.hub-br,.hub-bw{animation:none}}'
ALT = 'Diagram: Probanda AI takes evidence from '+', '.join(n.lower() for n,_ in SRC)+'. It keeps one tamper-evident record: each entry is linked to the last, edits and deletions are detectable. From the record: replay (see what happened, step by step), re-run (run it many times to see how stable the result is) and what-if re-run (change one factor and see how far the result moves). Output: evidence pack for audit, risk and incident review.'
if __name__ == '__main__':
    p = R/'src/pages/product.html'; s = p.read_text()
    new = f'<!--hub--><div class="hub" role="img" aria-label="{ALT}" style="margin-top:36px"><style>{CSS}</style>{desktop()}{phone()}</div><!--/hub-->'
    s, n = re.subn(r'<!--hub-->.*?<!--/hub-->', lambda m: new, s, flags=re.S)
    if not n: s, n = re.subn(r'<div style="margin-top:36px;border:2px dashed[^>]*><b[^>]*>Architecture diagram</b><br>Placeholder: Falk to add</div>', lambda m: new, s)
    assert n == 1, n
    p.write_text(s); print('hub', len(new), 'bytes')
