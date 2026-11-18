"""Local editor for probanda.ai: live preview with click-to-edit text, find and replace across pages.

Run:  python3 editor.py   → opens http://localhost:4321
Edits go straight into src/pages/*.html. Nothing is published: publishing is a git push (ask Claude).
Only text between tags is changed; layout, links and styles stay as they are.
"""
import html
import json
import pathlib
import re
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import build

ROOT = pathlib.Path(__file__).resolve().parent
PAGES = ROOT / 'src' / 'pages'
LOG = ROOT / '.edits.json'
PORT = next((int(a) for a in sys.argv[1:] if a.isdigit()), 4321)
SLUG_TO_NAME = {slug: name for name, slug, _ in build.pages}
NAME_TO_TITLE = {name: title for name, _, title in build.pages}
SEGMENT = re.compile(r'>([^<]+)<')


def norm(s):
    return ' '.join(s.split())


def esc(s):
    return html.escape(s, quote=False)


def log_edit(entry):
    data = json.loads(LOG.read_text()) if LOG.exists() else []
    data.append(entry)
    LOG.write_text(json.dumps(data, indent=1, ensure_ascii=False))


def edit_text(name, old, new):
    """Replace every text segment of a page whose text equals `old`. Returns the number replaced."""
    f = PAGES / f'{name}.html'
    s = f.read_text()
    target, count = norm(old), 0

    def one(m):
        nonlocal count
        seg = m.group(1)
        if norm(html.unescape(seg)) != target:
            return m.group(0)
        count += 1
        lead = seg[:len(seg) - len(seg.lstrip())]
        trail = seg[len(seg.rstrip()):]
        return '>' + lead + esc(norm(new)) + trail + '<'

    s2 = SEGMENT.sub(one, s)
    if count:
        f.write_text(s2)
        log_edit({'page': NAME_TO_TITLE[name], 'from': norm(old), 'to': norm(new), 'places': count})
    return count


def find(q, case):
    out = []
    flags = 0 if case else re.I
    pat = re.compile(re.escape(q), flags)
    for name, _, title in build.pages:
        s = (PAGES / f'{name}.html').read_text()
        for m in SEGMENT.finditer(s):
            t = norm(html.unescape(m.group(1)))
            for hit in pat.finditer(t):
                a, b = max(0, hit.start() - 50), min(len(t), hit.end() + 50)
                out.append({'page': title, 'before': t[a:hit.start()], 'match': hit.group(0), 'after': t[hit.end():b]})
    return out


def replace_all(q, r, case):
    flags = 0 if case else re.I
    pat = re.compile(re.escape(q), flags)
    total = {}
    for name, _, title in build.pages:
        f = PAGES / f'{name}.html'
        s = f.read_text()
        n = 0

        def one(m):
            nonlocal n
            seg = m.group(1)
            t = html.unescape(seg)
            if not pat.search(t):
                return m.group(0)
            t2, k = pat.subn(lambda _: r, t)
            n += k
            return '>' + esc(t2) + '<'

        s2 = SEGMENT.sub(one, s)
        if n:
            f.write_text(s2)
            total[title] = n
    if total:
        log_edit({'page': 'all pages', 'from': q, 'to': r, 'places': sum(total.values())})
    return total


def changes():
    data = json.loads(LOG.read_text()) if LOG.exists() else []
    diff = subprocess.run(['git', 'diff', '--stat', '--', 'src'], cwd=ROOT, capture_output=True, text=True).stdout
    return {'edits': data, 'unpublished': bool(diff.strip())}


def discard():
    subprocess.run(['git', 'checkout', '--', 'src/pages'], cwd=ROOT, check=True)
    LOG.unlink(missing_ok=True)


EDITOR = r"""
<style>
#pe-bar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:9999;display:flex;gap:8px;flex-wrap:wrap;justify-content:center;
 background:#16211F;color:#fff;padding:10px 12px;border-radius:14px;box-shadow:0 8px 30px rgba(0,0,0,.25);font:600 14px Inter,Arial,sans-serif;max-width:calc(100vw - 32px)}
#pe-bar button{font:inherit;border:0;border-radius:9px;padding:9px 14px;cursor:pointer;background:#2B4A45;color:#fff}
#pe-bar button.pri{background:#7FB8B1;color:#0F1B1A}#pe-bar button[disabled]{opacity:.45;cursor:default}
#pe-msg{align-self:center;font-weight:500;padding:0 6px}
body.pe-on main [contenteditable]{outline:none}
body.pe-on main *:hover{outline:1px dashed rgba(43,122,120,.5)}
.pe-changed{background:rgba(252,233,168,.7)!important}
#pe-panel{position:fixed;right:16px;top:16px;bottom:90px;width:min(440px,calc(100vw - 32px));z-index:9999;background:#fff;color:#16211F;border:1px solid #E4E1D8;
 border-radius:14px;box-shadow:0 8px 30px rgba(0,0,0,.2);padding:18px;overflow:auto;font:14px/1.5 Inter,Arial,sans-serif}
#pe-panel h3{font:600 18px Inter,Arial,sans-serif;margin:0 0 10px}#pe-panel input[type=text]{width:100%;box-sizing:border-box;padding:9px 10px;border:1px solid #ccc;border-radius:8px;margin:4px 0 10px;font:inherit}
#pe-panel button{font:600 14px Inter,Arial,sans-serif;border:0;border-radius:9px;padding:9px 14px;cursor:pointer;background:#16211F;color:#fff;margin:4px 6px 4px 0}
#pe-panel .hit{border-top:1px solid #eee;padding:8px 0}#pe-panel .hit b{background:#FCE9A8}#pe-panel .pg{font-size:12px;color:#667;text-transform:uppercase;letter-spacing:.05em}
#pe-panel .x{float:right;background:#eee;color:#16211F}
</style>
<div id="pe-bar"><button id="pe-edit" class="pri">✎ Edit text</button><button id="pe-save" disabled>Save</button>
<button id="pe-find">Find &amp; replace</button><button id="pe-chg">My changes</button><span id="pe-msg"></span></div>
<script>
(()=>{
const main=document.querySelector('main'),bar=document.getElementById('pe-bar'),msg=document.getElementById('pe-msg');
const slug=location.pathname.replace(/^\/|\/$/g,'');
let on=false,orig=new Map();
const say=t=>{msg.textContent=t};
const texts=()=>{const w=document.createTreeWalker(main,NodeFilter.SHOW_TEXT,{acceptNode:n=>n.data.trim()&&!n.parentElement.closest('svg,style,script')?1:2});const a=[];let n;while(n=w.nextNode())a.push(n);return a};
function pending(){let c=0;for(const [n,o] of orig) if(n.isConnected&&n.data!==o)c++;return c}
document.getElementById('pe-edit').onclick=e=>{
 on=!on;document.body.classList.toggle('pe-on',on);
 if(on){if(slug==='contact'){on=false;say('The contact page is changed by Claude. Ask Claude.');return}
  orig=new Map(texts().map(n=>[n,n.data]));main.contentEditable='true';main.spellcheck=true;e.target.textContent='✓ Done editing';say('Click any text and type.')}
 else{main.contentEditable='false';e.target.textContent='✎ Edit text';say(pending()?pending()+' unsaved change(s). Press Save.':'')}
};
main.addEventListener('keydown',e=>{if(on&&e.key==='Enter'){e.preventDefault();say('New lines and new paragraphs: ask Claude.')}});
main.addEventListener('paste',e=>{if(!on)return;e.preventDefault();document.execCommand('insertText',false,(e.clipboardData.getData('text/plain')||'').replace(/\s+/g,' '))});
main.addEventListener('click',e=>{if(on&&e.target.closest('a'))e.preventDefault()},true);
main.addEventListener('input',()=>{const c=pending();document.getElementById('pe-save').disabled=!c;say(c?c+' unsaved change(s)':'');
 for(const [n,o] of orig) if(n.isConnected&&n.parentElement)n.parentElement.classList.toggle('pe-changed',n.data!==o)});
const api=(p,b)=>fetch('/api/'+p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b||{})}).then(r=>r.json());
document.getElementById('pe-save').onclick=async()=>{
 const ch=[];for(const [n,o] of orig) if(n.isConnected&&n.data!==o)ch.push({old:o,new:n.data});
 const lost=[...orig.keys()].filter(n=>!n.isConnected).length;
 let ok=0,miss=[];for(const c of ch){const r=await api('edit',{slug,old:c.old,new:c.new});r.count?ok++:miss.push(c.new)}
 if(miss.length||lost){alertBox('Saved '+ok+'. Not saved: '+(miss.length+lost)+'. These edits changed formatting or text Claude must place by hand. Tell Claude: “'+(miss[0]||'my last edit on this page')+'”')}
 else location.reload();
};
function panel(h){let p=document.getElementById('pe-panel');if(!p){p=document.createElement('div');p.id='pe-panel';document.body.appendChild(p)}p.innerHTML='<button class="x">Close</button>'+h;p.querySelector('.x').onclick=()=>p.remove();return p}
function alertBox(t){panel('<h3>Please check</h3><p>'+t+'</p>')}
const escH=s=>s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
document.getElementById('pe-find').onclick=()=>{
 const p=panel('<h3>Find &amp; replace on all pages</h3><label>Find</label><input type=text id=pe-q><label>Replace with</label><input type=text id=pe-r>'+
 '<label><input type=checkbox id=pe-case> Match upper/lower case</label><br><button id=pe-go>Show where it appears</button><div id=pe-res></div>');
 p.querySelector('#pe-go').onclick=async()=>{const q=p.querySelector('#pe-q').value;if(!q)return;const hits=await api('find',{q,case:p.querySelector('#pe-case').checked});
  const r=p.querySelector('#pe-r').value;
  p.querySelector('#pe-res').innerHTML='<p><b>'+hits.length+'</b> place(s) found.</p>'+(hits.length?'<button id=pe-all>Replace all '+hits.length+' with “'+escH(r)+'”</button>':'')+
   hits.map(h=>'<div class=hit><div class=pg>'+escH(h.page)+'</div>…'+escH(h.before)+'<b>'+escH(h.match)+'</b>'+escH(h.after)+'…</div>').join('');
  const b=p.querySelector('#pe-all');if(b)b.onclick=async()=>{const t=await api('replace',{q,r,case:p.querySelector('#pe-case').checked});
   p.querySelector('#pe-res').innerHTML='<p>Replaced: '+Object.entries(t).map(([k,v])=>escH(k)+' '+v).join(', ')+'. Reloading…</p>';setTimeout(()=>location.reload(),900)}};
};
document.getElementById('pe-chg').onclick=async()=>{
 const c=await fetch('/api/changes').then(r=>r.json());
 const p=panel('<h3>My changes (not yet on probanda.ai)</h3>'+(c.edits.length?c.edits.map(e=>'<div class=hit><div class=pg>'+escH(e.page)+' · '+e.places+' place(s)</div>“'+escH(e.from)+'” → “'+escH(e.to)+'”</div>').join(''):'<p>No changes yet.</p>')+
  '<p style="margin-top:14px">To put these live, tell Claude: <b>“publish my changes”</b>.</p>'+(c.unpublished?'<button id=pe-undo style="background:#9B2C2C">Throw away all my changes</button>':''));
 const u=p.querySelector('#pe-undo');if(u)u.onclick=async()=>{if(u.dataset.sure){await api('discard');location.reload()}else{u.dataset.sure=1;u.textContent='Sure? Click again to throw away'}};
};
})();
</script>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype='text/html; charset=utf-8'):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/api/changes':
            return self.send(200, json.dumps(changes()), 'application/json')
        slug = path.strip('/')
        page = build.render(slug)
        if page is None:
            return self.send(404, build.page('Not found', '404', build.NOT_FOUND))
        self.send(200, page.replace('</body>', EDITOR + '</body>'))

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
        p = self.path
        if p == '/api/edit':
            name = SLUG_TO_NAME.get(body.get('slug', ''))
            n = edit_text(name, body['old'], body['new']) if name else 0
            return self.send(200, json.dumps({'count': n}), 'application/json')
        if p == '/api/find':
            return self.send(200, json.dumps(find(body['q'], body.get('case'))), 'application/json')
        if p == '/api/replace':
            return self.send(200, json.dumps(replace_all(body['q'], body.get('r', ''), body.get('case'))), 'application/json')
        if p == '/api/discard':
            discard()
            return self.send(200, '{}', 'application/json')
        self.send(404, '{}', 'application/json')


if __name__ == '__main__':
    srv = ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
    url = f'http://localhost:{PORT}/'
    print(f'Editor running at {url}  (stop with Ctrl+C)')
    if '--no-browser' not in sys.argv:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    srv.serve_forever()
