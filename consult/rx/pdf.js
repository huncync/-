// node pdf.js <in.html> <out.pdf> <환자명>
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [inp, out, name] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + inp, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const f = 'font-family:"WenQuanYi Zen Hei",sans-serif;font-size:7.5pt;color:#8a8f8b;width:100%;padding:0 15mm;display:flex;justify-content:space-between;';
  await p.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `<div style='${f}'><span>남자심리 처방전 · ${name} 님</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
    margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' } });
  await b.close();
})();
