const { chromium } = require('playwright-core');
const base = process.argv[2], out = process.argv[3];
const pages = ['', 'product', 'how-we-work', 'services', 'use-cases', 'use-cases-supplier-bank-details-change', 'who-we-are', 'product-new', 'contact'];
(async () => {
  const b = await chromium.launch({ channel: 'chrome' });
  for (const [label, vp] of [['m', { width: 390, height: 844 }], ['d', { width: 1440, height: 900 }]]) {
    const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1, isMobile: label === 'm', hasTouch: label === 'm' });
    const pg = await ctx.newPage();
    for (const p of pages) {
      await pg.goto(base + '/' + (p ? p + '/' : ''), { waitUntil: 'networkidle' });
      await pg.waitForTimeout(400);
      const r = await pg.evaluate(() => {
        const W = document.documentElement.clientWidth, issues = [];
        if (document.documentElement.scrollWidth > W + 1) issues.push('hscroll ' + document.documentElement.scrollWidth);
        const scrollable = e => { for (let x = e.parentElement; x; x = x.parentElement) { const s = getComputedStyle(x); if (/(auto|scroll)/.test(s.overflowX) && x.scrollWidth > x.clientWidth) return true; } return false; };
        const name = e => (e.tagName + '.' + (e.className || '') + ' "' + (e.innerText || '').trim().slice(0, 30) + '"').replace(/\s+/g, ' ');
        const els = [...document.querySelectorAll('main *')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
        for (const e of els) {
          const r = e.getBoundingClientRect(), s = getComputedStyle(e);
          if (r.right > W + 1 && !scrollable(e)) issues.push('offright ' + name(e));
          if (s.overflow !== 'visible' && s.overflowY !== 'visible' && !/(auto|scroll)/.test(s.overflowY) && e.scrollHeight > e.clientHeight + 4 && e.innerText.trim()) issues.push('clipped ' + name(e));
        }
        // sibling overlap among element children
        for (const e of els) {
          const kids = [...e.children].filter(k => { const r = k.getBoundingClientRect(); return r.width > 4 && r.height > 4 && getComputedStyle(k).position !== 'absolute'; });
          for (let i = 0; i < kids.length; i++) for (let j = i + 1; j < kids.length; j++) {
            const a = kids[i].getBoundingClientRect(), c = kids[j].getBoundingClientRect();
            const ox = Math.min(a.right, c.right) - Math.max(a.left, c.left), oy = Math.min(a.bottom, c.bottom) - Math.max(a.top, c.top);
            if (ox > 4 && oy > 4) issues.push('overlap ' + name(kids[i]) + ' × ' + name(kids[j]));
          }
        }
        // text overflowing its own box horizontally (words cut)
        return [...new Set(issues)].slice(0, 25);
      });
      console.log(`[${label}] /${p} ${r.length ? 'ISSUES ' + r.length : 'ok'}`); r.forEach(x => console.log('   ' + x));
      await pg.screenshot({ path: `${out}/${label}-${p || 'home'}.png`, fullPage: true });
    }
    await ctx.close();
  }
  await b.close();
})();
