// Citeste canalul General al echipelor de anul acesta din Teams web (teams.cloud.microsoft), deja logat in
// browser pane-ul aplicatiei Claude (viewport ~1280x1000). Nu citeste tokenuri si nu posteaza nimic: doar da click
// pe echipe si citeste textul paginii.
// Folosire cu javascript_tool (limita 45 s pe apel, deci in loturi de cate 6 echipe):
//   1) lipeste tot fisierul (defineste window.__teamsSweep si intoarce numarul de echipe)
//   2) await window.__teamsSweep(0)   apoi   await window.__teamsSweep(6)
// Fiecare apel intoarce textul postarilor vizibile din General (cele mai noi sunt la final).
window.__teamsEchipe = [
  '04-ETTI-L-CTI-INF-A4-S1-PSPr-2026',
  '04-ETTI-L-CTI-INF-A4-S1-PS-A-2026',
  '04-ETTI-L-CTI-INF-A4-S1-RC-A-2026',
  '04-ETTI-L-CTI-INF-A4-S1-IARF-A-2026',
  '04-ETTI-L-CTI-INF-A4-S1-ISo-A-2026',
  '04-ETTI-L-CTI-INF-A4-S1-CFi-A-2026',
  '04-ETTI-L-CTI-INF-A4-S1-IO-Ma-A-2026',
  '04-ETTI-L-CTI-INF-A4-S1-PIm-A-2026',
  '04-ETTI-L-CTI-INF-A4-S1-PBDPr-A-2026',
  '04-ETTI-L-CTI-INF-A4-S1-PBDPr-2026',
  '04-ETTI-Administrativ-2026',
];
window.__teamsSweep = async (dela, cate = 6) => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  for (const nume of window.__teamsEchipe.slice(dela, dela + cate)) {
    const back = [...document.querySelectorAll('button')]
      .find(b => (b.getAttribute('aria-label') || '').includes('Back to All teams'));
    if (back) { back.click(); await sleep(1500); }
    const btn = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === nume);
    if (!btn) { out.push(`##### ${nume}: nu apare in lista de echipe`); continue; }
    btn.click();
    await sleep(4000);
    let t = (document.querySelector('main') || document.body).innerText;
    const i = t.indexOf('Posts\n');
    if (i >= 0) t = t.slice(i + 6);
    out.push(`##### ${nume}\n` + t.replace(/\n{2,}/g, '\n').slice(-6000));
  }
  return out.join('\n\n');
};
window.__teamsEchipe.length;
