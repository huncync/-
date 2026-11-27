const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:900,height:1300},deviceScaleFactor:2});
await p.goto('file://'+__dirname+'/kakao.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const pr=await p.$('#prof'); await pr.screenshot({path:__dirname+'/kakao_profile_2x.png'});
await (await p.$('#bg')).screenshot({path:__dirname+'/kakao_background_1600x1000.png'});await b.close();})();
