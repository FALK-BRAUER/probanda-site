"""Build the static site: src/pages/*.html + src/probanda.css -> <page>/index.html at the repo root."""
import re, pathlib, sys
root = pathlib.Path(__file__).resolve().parent
src = root/'src'
out = pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else root
css = (src/'probanda.css').read_text()
pages = [('home','', 'Home'),('product','product','Product'),('how-we-work','how-we-work','How we work'),
         ('partners','partners','Partners'),('use-cases','use-cases','Use cases'),
         ('uc-supplier-bank-details-change','use-cases-supplier-bank-details-change','Supplier bank details change'),
         ('who-we-are','who-we-are','Who we are')]
nav = [('/product/','Product'),('/use-cases/','Use cases'),('/how-we-work/','How we work'),('/partners/','Partners'),('/who-we-are/','Who we are')]
# Old pages merged into How we work: the address still works and forwards there.
REDIRECTS = {'method':'/how-we-work/#measure','services':'/how-we-work/','offer':'/how-we-work/#path'}
CHROME = """<style>
body{margin:0;background:#FFFFFF;color:#0E1B2D;font-family:Inter,Arial,sans-serif}
.sh{display:flex;flex-wrap:wrap;gap:12px 28px;align-items:center;justify-content:space-between;padding:22px max(16px,4vw);border-bottom:1px solid #D3DCDB;background:#FFFFFF}
.sh a{color:#0E1B2D;text-decoration:none}.sh .brand{display:flex;align-items:center}.sh .brand img{height:36px;width:auto;display:block}
.sh nav{display:flex;flex-wrap:wrap;align-items:center;gap:8px 22px;font-size:15px}.sh .cta{background:#0E1B2D;color:#fff!important;border-radius:999px;padding:9px 18px;font-weight:600}.sh nav a.on{text-decoration:underline;text-decoration-color:#11786F;text-decoration-thickness:2px;text-underline-offset:6px}
.sf{padding:40px max(16px,4vw);background:#0E1B2D;color:#D6E2F2;font-size:14px;line-height:1.6;display:flex;flex-wrap:wrap;gap:16px 40px;align-items:flex-end;justify-content:space-between}.sf img{height:36px;width:auto;display:block;margin-bottom:12px}.sf .tl{color:#2FD3C0;font-weight:500}
.ct{max-width:720px;margin:0 auto;padding:96px max(16px,4vw) 120px}.ct h1{font-family:Inter,Arial,sans-serif;font-weight:600;letter-spacing:-.02em;font-size:clamp(36px,5vw,56px);line-height:1.1;margin:0 0 20px}
.ct p{font-size:18px;line-height:1.6;max-width:60ch}.ct a.mail{display:inline-block;margin-top:16px;padding:14px 22px;background:#0E1B2D;color:#fff;border-radius:999px;text-decoration:none;font-weight:600}
.stairs-m{display:none}\n@media(max-width:900px){.pb svg[viewBox="0 0 1200 230"],.pb svg[viewBox="0 0 700 240"]{display:none!important}.stairs-m{display:flex;flex-direction:column-reverse;gap:6px;list-style:none;padding:0!important;margin:20px 0 0!important}.stairs-m li{border-radius:8px;padding:10px 14px!important;margin:0!important;font-size:14px}.stairs-m li span{display:block;font-size:12px;opacity:.85;margin-top:2px}}\n</style>"""
def page(title, slug, body):
    links = ''.join(f'<a href="{h}"{" class=on" if h.strip("/")==slug else ""}>{t}</a>' for h,t in nav)
    t = 'Probanda AI' if not slug else f'{title} · Probanda AI'
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="Reliable, provable AI agents for business-critical work.">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{css}{CHROME}</head><body>
<header class="sh"><a class="brand" href="/" aria-label="Probanda AI home"><img src="/assets/probanda-lockup-on-light.svg" alt="Probanda AI" width="150" height="32"></a><nav>{links}<a class="cta{' on' if slug=='contact' else ''}" href="/contact/">Book a call</a></nav></header>
<main>{body}</main>
<footer class="sf"><div><img src="/assets/probanda-lockup-on-dark.svg" alt="Probanda AI" width="150" height="32">AI agent governance. Reliable, provable AI agents for business-critical work.</div><div class="tl">Proof, complete.</div></footer>
</body></html>"""
def stack(h):
    def one(m):
        t=m.group(0)
        rows=re.findall(r'<tr[^>]*>.*?</tr>',t,re.S)
        if not rows or '<th' not in rows[0]: return t
        heads=[re.sub(r'<[^>]+>','',c).strip() for c in re.findall(r'<th[^>]*>(.*?)</th>',rows[0],re.S)]
        def lab(r):
            i=[0]
            def td(c):
                k=i[0]; i[0]+=1
                return c.group(0)[:-1]+f' data-label="{heads[k]}">' if k<len(heads) and heads[k] else c.group(0)
            return re.sub(r'<td[^>]*>',td,r.group(0))
        t=re.sub(r'<tr[^>]*>.*?</tr>',lambda r: r.group(0) if '<th' in r.group(0) else lab(r),t,flags=re.S)
        return t.replace('<table','<table class="stack"',1)
    return re.sub(r'<table.*?</table>',one,h,flags=re.S)
def stairs(h):
    def one(m):
        svg=m.group(0)
        items=[]
        for r in re.finditer(r'<rect[^>]*fill="([^"]+)"[^>]*></rect>((?:\s*<text[^>]*>[^<]*</text>)*)',svg):
            texts=re.findall(r'<text[^>]*fill="([^"]+)"[^>]*>([^<]*)</text>',r.group(2))
            if not texts: continue
            col=texts[0][0]; main=texts[0][1]; rest=[t for _,t in texts[1:]]
            big=len(texts)>1 and 'font-size="12"' not in r.group(2).split('</text>')[1]
            if big: main=main+' '+rest.pop(0)
            items.append(f'<li style="background:{r.group(1)};color:{col}"><b>{main}</b>{"<span>"+" ".join(rest)+"</span>" if rest else ""}</li>')
        return svg+'<ol class="stairs-m">'+''.join(items)+'</ol>'
    return re.sub(r'<svg viewBox="0 0 (?:1200 230|700 240)".*?</svg>',one,h,flags=re.S)
def fix(h):
    h = stack(h)
    h = stairs(h)
    h = re.sub(r'href="/(contact|partners|product|how-we-work|use-cases|use-cases-supplier-bank-details-change|who-we-are)"', r'href="/\1/"', h)
    return h
CONTACT = """<div class="ct"><h1>Talk to us.</h1><p>Tell us which agent and which business process you want to make reliable and provable.</p>
<p>Email us at <b>falk@probanda.ai</b></p><a class="mail" href="mailto:falk@probanda.ai?subject=probanda">Write to us</a></div>"""
NOT_FOUND = '<div class="ct"><h1>Page not found.</h1><p><a href="/">Back to home</a></p></div>'

def css_now():
    return (src/'probanda.css').read_text()

def render(slug):
    """Full HTML for one page, read fresh from src/ (used by build and by the editor preview)."""
    global css
    css = css_now()
    for name, s, title in pages:
        if s == slug:
            return page(title, slug, fix((src/'pages'/f'{name}.html').read_text()))
    if slug == 'contact':
        return page('Contact', 'contact', CONTACT)
    return None

def main(out):
    for name, slug, title in pages:
        d = out/slug; d.mkdir(parents=True, exist_ok=True)
        (d/'index.html').write_text(render(slug))
    (out/'contact').mkdir(exist_ok=True); (out/'contact'/'index.html').write_text(render('contact'))
    (out/'CNAME').write_text('probanda.ai\n')
    (out/'404.html').write_text(page('Not found','404',NOT_FOUND))
    for old, to in REDIRECTS.items():
        d = out/old; d.mkdir(exist_ok=True)
        (d/'index.html').write_text(f'<!doctype html><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="{to}"><meta http-equiv="refresh" content="0; url={to}"><a href="{to}">This page has moved to How we work.</a>')
    print('ok')

if __name__ == '__main__':
    main(out)
