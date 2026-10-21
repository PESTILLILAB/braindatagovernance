const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
const p=await b.newPage({viewport:{width:1300,height:900},deviceScaleFactor:2});const path=require('path');const [,,BUILD,OUT]=process.argv;await p.goto('file://'+path.resolve(BUILD)+'/_tiers_fig.html');await p.waitForTimeout(300);
await p.locator('#fig').screenshot({path:OUT+'/Figure_Tiers.png'});
await p.pdf({path:OUT+'/Figure_Tiers.pdf',format:'A4',landscape:true,printBackground:true,margin:{top:'8mm',bottom:'8mm',left:'8mm',right:'8mm'}});
await b.close();})();
