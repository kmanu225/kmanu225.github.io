// Local-only browser and generated-site regression tests.
// Usage: node tests/site-smoke.cjs /absolute/path/to/jekyll-output
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const site = path.resolve(process.argv[2] || path.join(root, '_site'));
const output = path.join(root, 'tmp/browser');
const mime = {'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.pdf':'application/pdf','.xml':'application/xml'};
async function fileFor(urlPath) {
  const decoded = decodeURIComponent(urlPath);
  const resolved = path.resolve(site, '.' + decoded);
  if (resolved !== site && !resolved.startsWith(site + path.sep)) throw Error('Path outside site');
  const stat = await fs.stat(resolved);
  return stat.isDirectory() ? path.join(resolved, 'index.html') : resolved;
}
(async () => {
  await fs.mkdir(output, {recursive:true});
  const sitemap = await fs.readFile(path.join(site,'sitemap.xml'),'utf8');
  const axeSource = await fs.readFile(process.env.AXE_PATH || require.resolve('axe-core/axe.min.js'), 'utf8');
  const paths = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m=>new URL(m[1]).pathname).filter(p=>!p.endsWith('.pdf'));
  assert(!paths.some(p=>p.includes('markdown_generator')), 'Template documentation must not be published');
  const server = http.createServer(async(req,res)=>{
    try {const file=await fileFor(new URL(req.url,'http://localhost').pathname);res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(await fs.readFile(file));}
    catch {res.writeHead(404);res.end('Not found');}
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const base = 'http://127.0.0.1:'+server.address().port;
  const browser = await chromium.launch({headless:true});
  const failures = [], errors = [], titles = new Set(), descriptions = new Set();
  const context = await browser.newContext({viewport:{width:1440,height:1000}});
  const page = await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  const requests = [];
  page.on('request',r=>requests.push(r.url()));
  let checkedLinks=0;
  try {
    for (const urlPath of paths) {
      await page.goto(base+urlPath);
      const result=await page.evaluate(()=>({
        lang:document.documentElement.lang,h1:document.querySelectorAll('h1').length,
        activeNavigation:document.querySelectorAll('#primary-nav [aria-current="page"]').length,
        title:document.title,description:document.querySelector('meta[name="description"]')?.content,
        canonical:document.querySelector('link[rel="canonical"]')?.href,
        image:document.querySelector('meta[property="og:image"]')?.content,
        json:[...document.querySelectorAll('script[type="application/ld+json"]')].map(n=>JSON.parse(n.textContent)),
        links:[...document.querySelectorAll('a[href],img[src],link[rel="stylesheet"],script[src]')].map(n=>n.getAttribute('href')||n.getAttribute('src')),
        missingAlt:document.querySelectorAll('img:not([alt])').length,
        emptyLinks:[...document.querySelectorAll('a')].filter(n=>!n.textContent.trim()&&!n.getAttribute('aria-label')&&!n.querySelector('img[alt]')).length
      }));
      const check=(condition,message)=>{if(!condition)failures.push(urlPath+': '+message);};
      await page.addScriptTag({content:axeSource});
      const accessibility = await page.evaluate(async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}}));
      for(const violation of accessibility.violations)failures.push(urlPath+': accessibility '+violation.id+' ('+violation.nodes.length+' elements)');
      check(result.lang==='en','English document language');
      check(result.activeNavigation<=1,'Only one active navigation item');
      check(result.h1===1,'Exactly one h1, found '+result.h1);
      check(Boolean(result.description),'Description required');
      check(!titles.has(result.title),'Duplicate title'); titles.add(result.title);
      check(!descriptions.has(result.description),'Duplicate description'); descriptions.add(result.description);
      check(result.canonical==='https://kmanu225.github.io'+urlPath,'Canonical URL');
      check(Boolean(result.image),'Social image required');
      check(!result.missingAlt,'Images need alternative text');
      check(!result.emptyLinks,'Links need accessible names');
      check(result.json.length>=1,'Structured data required');
      for(const href of result.links) {
        const url=new URL(href,base+urlPath);
        if(![base,'https://kmanu225.github.io'].includes(url.origin)) continue;
        try {
          const file=await fileFor(url.pathname);
          await fs.access(file); checkedLinks++;
          if(url.hash) {
            const html=await fs.readFile(file,'utf8');
            const id=decodeURIComponent(url.hash.slice(1));
            check(html.includes('id="'+id+'"')||html.includes("id='"+id+"'"),'Missing fragment '+href);
          }
        } catch {failures.push(urlPath+': Broken local resource '+href);}
      }
    }
    for(const width of [320,390,768,1024,1440]) {
      await page.setViewportSize({width,height:900});
      for(const urlPath of ['/','/cv/','/portfolio/','/blog-posts/','/portfolio/2026-06-22-eap-psk-256/','/pki-deployment-tutorial/','/ai-fluency/']) {
        await page.goto(base+urlPath);
        const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
        if(overflow)failures.push(urlPath+': Horizontal overflow at '+width+'px');
      }
    }
    await page.setViewportSize({width:1440,height:1000});
    await page.goto(base+'/');
    await page.screenshot({path:path.join(output,'home-desktop.png')});
    await page.screenshot({path:path.join(output,'home-full.png'),fullPage:true});
    await page.keyboard.press('Tab');
    assert.equal(await page.locator(':focus').textContent(),'Skip to content');
    await page.keyboard.press('Enter');
    assert.equal(await page.locator(':focus').getAttribute('id'),'main');
    await page.setViewportSize({width:390,height:844});
    await page.goto(base+'/');
    await page.screenshot({path:path.join(output,'home-mobile.png')});
    await page.addScriptTag({content:axeSource});
    const mobileAccessibility = await page.evaluate(async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}}));
    for(const violation of mobileAccessibility.violations)failures.push('Mobile home: accessibility '+violation.id);
    const toggle=page.getByRole('button',{name:'Menu'});
    await toggle.focus(); await page.keyboard.press('Enter');
    assert.equal(await toggle.getAttribute('aria-expanded'),'true');
    assert(await page.getByRole('navigation',{name:'Main navigation'}).isVisible());
    await page.keyboard.press('Tab');
    assert.equal(await page.locator(':focus').textContent(),'Expertise');
    await page.keyboard.press('Escape');
    assert.equal(await toggle.getAttribute('aria-expanded'),'false');
    assert.equal(await page.locator(':focus').getAttribute('aria-controls'),'primary-nav');
    await page.goto(base+'/portfolio/');
    await page.screenshot({path:path.join(output,'case-studies-mobile.png'),fullPage:true});
    await page.setViewportSize({width:1440,height:1000});
    await page.goto(base+'/cv/');
    await page.screenshot({path:path.join(output,'cv-desktop.png'),fullPage:true});
    // Legacy bookmarks still arrive at the new local summaries.
    for(const alias of ['/blog-post-1/','/blog-post-7/','/blog-post-10/','/about/']) {
      const response=await page.request.get(base+alias);
      assert.equal(response.status(),200,alias);
      assert((await response.text()).includes('https://kmanu225.github.io/'),alias);
    }
    const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
    const plain=await nojs.newPage(); await plain.goto(base+'/');
    assert(await plain.getByRole('navigation',{name:'Main navigation'}).isVisible(),'Navigation without JS');
    await nojs.close();
    assert.equal((await page.request.get(base+'/files/emmanuel-konan-cv.pdf')).status(),200);
    assert(!requests.some(url=>/googleapis|polyfill|jquery|mathjax/i.test(url)),'No unnecessary third-party rendering dependencies');
    assert.equal(errors.length,0,'Browser runtime errors: '+errors.join('; '));
    const report={pages:paths.length,checkedLinks,viewports:[320,390,768,1024,1440],failures,runtimeErrors:errors};
    await fs.writeFile(path.join(output,'report.json'),JSON.stringify(report,null,2));
    console.log(JSON.stringify(report,null,2));
    assert.equal(failures.length,0,failures.join('\n'));
  } finally {await browser.close(); await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);process.exitCode=1;});
