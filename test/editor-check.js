// Smoke test of the local editor: click-to-edit save and find/replace. Run against `python3 editor.py 4399 --no-browser`.
const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ channel: 'chrome' });
  const pg = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await pg.goto('http://localhost:4399/');
  await pg.click('#pe-edit');
  const ok = await pg.evaluate(() => {
    const w = document.createTreeWalker(document.querySelector('main'), NodeFilter.SHOW_TEXT);
    let n; while ((n = w.nextNode())) if (n.data.includes('Accounts payable agent')) { n.data = 'Payables agent'; break; }
    document.querySelector('main').dispatchEvent(new Event('input')); return !!n;
  });
  console.log('found node', ok, 'save enabled', !(await pg.isDisabled('#pe-save')));
  await Promise.all([pg.waitForNavigation(), pg.click('#pe-save')]);
  console.log('after save has new text', (await pg.content()).includes('Payables agent'));
  await pg.click('#pe-find'); await pg.fill('#pe-q', 'Payables agent'); await pg.fill('#pe-r', 'Accounts payable agent');
  await pg.click('#pe-go'); await pg.waitForSelector('#pe-all');
  console.log((await pg.textContent('#pe-res')).slice(0, 40));
  await Promise.all([pg.waitForNavigation(), pg.click('#pe-all')]);
  console.log('restored', (await pg.content()).includes('Accounts payable agent'));
  await pg.click('#pe-chg'); await pg.waitForSelector('#pe-panel .hit');
  console.log('changes panel:', (await pg.textContent('#pe-panel')).replace(/\s+/g, ' ').slice(0, 160));
  await pg.screenshot({ path: '/tmp/ed.png' });
  await b.close();
})();
