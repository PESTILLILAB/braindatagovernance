const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
const path=require('path');const [,,BUILD,OUT]=process.argv;const files=JSON.parse(fs.readFileSync(BUILD+'/_files.json'));
for(const f of files){const p=await b.newPage();await p.goto('file://'+f);await p.pdf({path:path.join(OUT,path.basename(f).replace(/\.html$/,'.pdf')),format:'A4',landscape:true,printBackground:true,margin:{top:'14mm',bottom:'16mm',left:'12mm',right:'12mm'},displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:7pt;color:#666;width:100%;text-align:right;padding-right:12mm">Page <span class="pageNumber"></span> / <span class="totalPages"></span></div>'});await p.close();}
await b.close();})();
