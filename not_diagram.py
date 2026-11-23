"""Draws "What Probanda is not, and what it does" (desktop + phone SVG) into src/pages/product.html, between the not markers.
Run: python3 not_diagram.py, then python3 build.py. Reuses the colours, helpers and .hub display rules of hub_diagram.py."""
import pathlib, re
from hub_diagram import T, B, MARK, NAVY, TEAL, MINT, MUT, GREY
R = pathlib.Path(__file__).resolve().parent
LEFT = [('Not an agent platform','Your agents keep theirs.'),('Not another registry','Pulls from the ones you have.'),('Not an identity platform','Reads yours on every call.'),('Not a gateway replacement','Works through yours.')]
RIGHT = [('Not an AI control tower','Feeds it evidence and status.'),('Not a monitoring tool','Feeds the one you have.'),('Not model testing','Gives your testers evidence.'),('Not a certifier','Your assessors decide.')]
DOES = [('Know','One view of every agent.','Unknown agents can’t act.'),('Check','Each write, before it runs.','Risky actions go to a person.'),('Prove','Replay any decision.','Your auditor checks it offline.')]
def dash(x,y,w,h): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#fff" stroke="{GREY}" stroke-width="2" stroke-dasharray="6 5"/>'
def arrow(x,y): return f'<path d="M{x} {y}h20" stroke="{TEAL}" stroke-width="2.5"/><path d="M{x+18} {y-6}l12 6l-12 6z" fill="{TEAL}"/>'
def mark(x,y,s): return f'<image href="data:image/svg+xml;base64,{MARK}" x="{x}" y="{y}" width="{s}" height="{s}"/>'
def wrap(w,h,cls,o): return f'<svg class="{cls}" viewBox="0 0 {w} {h}" aria-hidden="true" font-family="Inter,Arial,sans-serif">{"".join(o)}</svg>'
def desktop():
    o = [T(2,18,'Uses',18,600,MUT), T(840,18,'Feeds',18,600,MUT), B(380,32,420,472,NAVY,NAVY,20), mark(414,60,44)]
    for x,N,ax in ((2,LEFT,345),(840,RIGHT,805)):
        for i,(n,u) in enumerate(N):
            y = 32+i*122
            o += [dash(x,y,338,106), T(x+22,y+46,n,21,600), T(x+22,y+79,u,18,600,TEAL), arrow(ax,y+53)]
    for j,(k,a,b) in enumerate(DOES):
        y = 160+j*104; o += [T(414,y,k,26,600,MINT), T(514,y-9,a,18,400,'#fff'), T(514,y+18,b,18,400,'#fff')]
    o += ['<path d="M414 430h352" stroke="#fff" stroke-opacity=".25"/>', T(414,458,'Kept current as models, tools',17,500,'#fff'), T(414,482,'and rules change.',17,500,'#fff')]
    return wrap(1180,508,'hub-d',o)
def phone():
    o = [B(2,2,356,284,NAVY,NAVY,16), mark(18,18,32)]
    for j,(k,a,b) in enumerate(DOES):
        y = 86+j*60; o += [T(18,y,k,19,600,MINT), T(93,y-7,a,15,400,'#fff'), T(93,y+15,b,15,400,'#fff')]
    o.append(T(18,260,'Kept current as things change.',15,500,'#fff')); y = 318
    for h,N in (('Uses',LEFT),('Feeds',RIGHT)):
        o.append(T(2,y,h,15,600,MUT)); y += 12
        for n,u in N: o += [dash(2,y,356,62), T(18,y+26,n,16,600), T(18,y+49,u,15,600,TEAL)]; y += 70
        y += 22
    return wrap(360,y-26,'hub-m',o)
ALT = 'What Probanda is not, and what it does. '+' '.join(f'{n}: {u}' for n,u in LEFT+RIGHT)+' '+' '.join(f'{k}: {a} {b}' for k,a,b in DOES)+' Kept current as models, tools and rules change.'
if __name__ == '__main__':
    p = R/'src/pages/product.html'; s = p.read_text()
    new = f'<!--not--><div class="hub" role="img" aria-label="{ALT}" style="margin-top:18px">{desktop()}{phone()}</div><!--/not-->'
    s, n = re.subn(r'<!--not-->.*?<!--/not-->', lambda m: new, s, flags=re.S)
    assert n == 1, n
    p.write_text(s); print('not', len(new), 'bytes')
