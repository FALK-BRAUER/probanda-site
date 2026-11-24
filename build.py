"""Build the static site: src/pages/*.html + src/probanda.css -> <page>/index.html at the repo root."""
import re, pathlib, sys
root = pathlib.Path(__file__).resolve().parent
src = root/'src'
out = pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else root
css = (src/'probanda.css').read_text()
pages = [('home','', 'Home'),('product','product','Product'),('how-we-work','how-we-work','How we work'),
         # ('services','services','Services'),  merged into How we work (src/pages/services.html kept)
         # ('partners','partners','Partners'),  hidden for now (src/pages/partners.html kept)
        # ('use-cases','use-cases','Use cases'),  hidden for now (src/pages/use-cases.html kept)
         # ('uc-supplier-bank-details-change','use-cases-supplier-bank-details-change','Supplier bank details change'),  hidden for now
         ('who-we-are','who-we-are','Who we are'),
         ('product-old','product-old','Product (previous)')]  # previous product page, not in the menu
HIDDEN = {'product-old'}  # built but not in the menu, kept out of search engines
nav = [('/product/','Product'),('/how-we-work/','How we work'),('/who-we-are/','Who we are')]
# Old pages merged into How we work: the address still works and forwards there.
REDIRECTS = {'method':'/how-we-work/#measure','offer':'/how-we-work/#path','partners':'/how-we-work/#partners','product-new':'/product/','services':'/how-we-work/#more','use-cases':'/product/#usecases','use-cases-supplier-bank-details-change':'/product/#usecases'}
SITE = 'https://probanda.ai'
# Search and sharing: title shown in Google and on link previews, plus the line under it.
SEO = {
 '': ('Probanda AI · Govern and prove every AI agent action',
      'Run AI agents on business-critical work. Probanda Safeguard checks each agent action before it reaches your ERP, CRM or finance systems, and keeps a record your auditor can verify.'),
 'product': ('Probanda Safeguard · accountability ledger for AI agents',
      'Probanda Safeguard checks every AI agent action before it runs, records it in a tamper-evident ledger, and lets you replay any decision. Works with your identity platform, gateways and monitoring.'),
 'how-we-work': ('How we work · Build or govern AI agents · Probanda AI',
      'Build new AI agents or govern the ones you already run. One process at a time, with a sign-off at every step, until your agents are governed and ready for production.'),
 'who-we-are': ('Who we are · Probanda AI',
      'Probanda is Latin for “things that must be proved”. Meet the team that makes every AI agent action checked, recorded and provable.'),
 'contact': ('Talk to us · Probanda AI',
      'Tell us which AI agent and which business process you want to make reliable and provable.'),
}
SITEMAP = ['', 'product', 'how-we-work', 'who-we-are', 'contact']
ORG = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Probanda AI","url":"https://probanda.ai/","logo":"https://probanda.ai/assets/apple-touch-icon.png","description":"AI agent governance. Probanda Safeguard checks, records and proves every AI agent action."}</script>'
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
    t, desc = SEO.get(slug, ('Probanda AI' if not slug else f'{title} · Probanda AI', 'Reliable, provable AI agents for business-critical work.'))
    url = SITE + '/' + (slug + '/' if slug else '')
    meta = '' if slug in HIDDEN or slug == '404' else (f'<link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="Probanda AI">'
            f'<meta property="og:title" content="{t}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">'
            f'<meta property="og:image" content="{SITE}/assets/share.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image">' + (ORG if not slug else ''))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{desc}">{meta}
{'<meta name="robots" content="noindex">' if slug in HIDDEN or slug == '404' else ''}<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
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
    h = re.sub(r'href="/(contact|partners|product|how-we-work|services|use-cases|use-cases-supplier-bank-details-change|who-we-are)"', r'href="/\1/"', h)
    return h
CONTACT = """<div class="ct"><h1>Talk to us.</h1><p>Tell us which agent and which business process you want to make reliable and provable.</p>
<a class="mail" style="margin-top:28px" href="mailto:khor@probanda.ai,falk@probanda.ai?subject=probanda">Email the founders</a></div>"""
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
    (out/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + ''.join(f'  <url><loc>{SITE}/{s + "/" if s else ""}</loc></url>\n' for s in SITEMAP) + '</urlset>\n')
    (out/'404.html').write_text(page('Not found','404',NOT_FOUND))
    for old, to in REDIRECTS.items():
        d = out/old; d.mkdir(exist_ok=True)
        (d/'index.html').write_text(f'<!doctype html><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="{SITE}{to}"><meta http-equiv="refresh" content="0; url={to}"><a href="{to}">This page has moved.</a>')
    print('ok')

if __name__ == '__main__':
    main(out)
