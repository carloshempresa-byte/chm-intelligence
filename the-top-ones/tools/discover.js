// usage: node discover.js <outfile.json> <url1> [url2 ...]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const out = process.argv[2];
  const urls = process.argv.slice(3);
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy });
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 900 }, locale: 'en-US',
  });
  const items = {};
  const collect = (obj) => {
    if (!obj || typeof obj !== 'object') return;
    if (Array.isArray(obj)) { obj.forEach(collect); return; }
    if (obj.id && obj.author && (obj.stats || obj.statsV2) && obj.video) {
      const a = typeof obj.author === 'object' ? obj.author.uniqueId : obj.author;
      const st = obj.statsV2 || obj.stats;
      items[obj.id] = { id: obj.id, author: a, desc: obj.desc, plays: Number(st.playCount || 0),
        likes: Number(st.diggCount || 0), dur: obj.video.duration, created: obj.createTime,
        url: `https://www.tiktok.com/@${a}/video/${obj.id}` };
    }
    for (const k of Object.keys(obj)) collect(obj[k]);
  };
  for (const url of urls) {
    const page = await ctx.newPage();
    page.on('response', async (r) => {
      const u = r.url();
      if (!u.includes('/api/')) return;
      try { const j = await r.json(); collect(j); } catch (e) {}
    });
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(5000);
      for (let i = 0; i < 6; i++) { await page.mouse.wheel(0, 3000); await page.waitForTimeout(1500); }
      const html = await page.content();
      const m = html.match(/<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)<\/script>/s);
      if (m) { try { collect(JSON.parse(m[1])); } catch (e) {} }
      // fall back: scrape anchors
      const links = await page.$$eval('a[href*="/video/"]', as => as.map(a => a.href));
      for (const l of links) { const mm = l.match(/@([^/]+)\/video\/(\d+)/); if (mm && !items[mm[2]]) items[mm[2]] = { id: mm[2], author: mm[1], url: l.split('?')[0], plays: null }; }
      console.error(url, '->', Object.keys(items).length, 'items so far');
    } catch (e) { console.error('ERR', url, e.message); }
    await page.close();
  }
  fs.writeFileSync(out, JSON.stringify(Object.values(items), null, 1));
  await browser.close();
})();
