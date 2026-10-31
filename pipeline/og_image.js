// Renders the share image (public/og.jpg): the web at 1200x630 @2x with a title block.
// Usage: npm i puppeteer-core && node pipeline/og_image.js public/index.html public/og.jpg
// The layout differs slightly per load, so run it a few times and keep the best take.
const puppeteer = require('puppeteer-core');
const path = require('path');
const [, , page_path, out] = process.argv;

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true,
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 630, deviceScaleFactor: 2 });
  await page.goto('file:///' + path.resolve(page_path).replace(/\\/g, '/'), { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);
  await page.addStyleTag({ content: `
    header.top,.hero,.controls,#tourMin,.zoom,#zhint,.web-sec .method,#findings,footer,.whispers{display:none!important}
    #tour{visibility:hidden!important}
    #web{margin:0!important;padding:0!important;max-width:none!important}
    #stage{position:fixed!important;inset:0!important;width:100vw!important;height:100vh!important;max-height:none!important;border:0!important;border-radius:0!important;margin:0!important}
    #og{position:fixed;left:56px;top:0;bottom:0;width:340px;display:flex;flex-direction:column;justify-content:center;z-index:50;color:var(--ink)}
    #og .k{font:700 13px/1.4 "Courier Prime",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:0 0 14px}
    #og h1{font:400 58px/1.02 "IM Fell English",serif;margin:0 0 16px}
    #og p{font:italic 21px/1.35 "Spectral",serif;color:var(--muted);margin:0 0 26px}
    #og .s{font:400 14px/1.6 "Courier Prime",monospace;color:var(--ink);opacity:.85;border-top:1px solid var(--line);padding-top:14px}
  `});
  await page.evaluate(() => {
    const stats = [...document.querySelectorAll('#stats li')].map(li => li.querySelector('b').textContent + ' ' + li.querySelector('span').textContent);
    const statsHtml = `${stats[0]} · ${stats[2]}<br>${stats[3]}`;
    const d = document.createElement('div'); d.id = 'og';
    d.innerHTML = `<p class="k">H. P. Lovecraft · a data deep dive</p><h1>The Arkham Index</h1><p>Every name in the Mythos, numbered and correlated.</p><div class="s">${statsHtml}</div>`;
    document.body.appendChild(d);
    window.dispatchEvent(new Event('resize'));
  });
  // the page refits itself (ResizeObserver) and again when its simulation settles
  await new Promise(r => setTimeout(r, 20000));
  await page.evaluate(() => document.getElementById('zFit').click());
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: out, type: 'jpeg', quality: 88 });
  await browser.close();
  console.log('wrote', out);
})().catch(e => { console.error(e); process.exit(1); });
