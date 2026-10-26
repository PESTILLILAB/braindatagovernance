// Renders the interactive workflow figure of the built Toolkit page to toolkit/pdf/Figure_Workflow_Toolkit.{svg,png}.
// Usage: node src/explorer/wffig.js  (after ./build.sh; needs Playwright)
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const http = require('http');
const root = path.join(__dirname, '..', '..'); const site = path.join(root, '_site'); const out = path.join(root, 'toolkit', 'pdf');
const mime = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.json': 'application/json' };
const srv = http.createServer((req, res) => { let p = path.join(site, decodeURIComponent(req.url.split('#')[0].split('?')[0])); if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html'); if (!fs.existsSync(p)) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': mime[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res); });
(async () => {
  await new Promise(r => srv.listen(0, r)); const port = srv.address().port;
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined }); const p = await b.newPage({ viewport: { width: 1700, height: 1200 }, deviceScaleFactor: 2 });
  await p.goto(`http://127.0.0.1:${port}/toolkit/#workflow`); await p.waitForSelector('#iwf .node');
  const svg = await p.evaluate(() => {
    const s = document.getElementById('iwf').cloneNode(true); const live = document.getElementById('iwf');
    const a = live.querySelectorAll('*'), c = s.querySelectorAll('*');
    for (let i = 0; i < a.length; i++) { const cs = getComputedStyle(a[i]); for (const k of ['fill', 'stroke', 'font-family', 'opacity']) { const v = cs.getPropertyValue(k); if (v && v !== 'none' && !(k === 'opacity' && v === '1')) c[i].setAttribute(k, v); } }
    s.setAttribute('xmlns', 'http://www.w3.org/2000/svg'); s.removeAttribute('id'); s.setAttribute('width', s.viewBox.baseVal.width); s.setAttribute('height', s.viewBox.baseVal.height);
    s.querySelectorAll('[opacity]').forEach(e => { if (e.getAttribute('opacity') === '0.22' || e.getAttribute('opacity') === '0.12') e.removeAttribute('opacity'); });
    return s.outerHTML;
  });
  fs.mkdirSync(out, { recursive: true }); fs.writeFileSync(path.join(out, 'Figure_Workflow_Toolkit.svg'), svg);
  const el = await p.$('#iwf'); await el.screenshot({ path: path.join(out, 'Figure_Workflow_Toolkit.png'), omitBackground: false });
  await b.close(); srv.close(); console.log('wrote Figure_Workflow_Toolkit.svg/png');
})();
