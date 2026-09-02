// Deterministic site assets: typography-based sharing card and image optimization.
// Usage: NODE_PATH=/path/to/node_modules node scripts/build_brand_assets.cjs
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('sharp');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
(async () => {
  // Keep the user's source portrait intact. Only encode an optimized derivative.
  await sharp(path.join(root, 'images/profile.png')).webp({ quality: 86 }).toFile(path.join(root, 'images/profile.webp'));
  const svg = '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">' +
    '<rect width="1200" height="630" fill="#14283b"/><rect x="64" y="64" width="52" height="5" fill="#86d9bd"/>' +
    '<text x="64" y="145" font-family="Arial,sans-serif" font-size="27" fill="#b8d3dc" letter-spacing="4">EMMANUEL KONAN</text>' +
    '<text x="60" y="270" font-family="Arial,sans-serif" font-size="72" font-weight="700" fill="#ffffff">Applied cryptography.</text>' +
    '<text x="60" y="363" font-family="Arial,sans-serif" font-size="65" font-weight="700" fill="#86d9bd">Practical cybersecurity.</text>' +
    '<line x1="64" x2="1136" y1="452" y2="452" stroke="#466074"/>' +
    '<text x="64" y="509" font-family="Arial,sans-serif" font-size="26" fill="#e0eaf0">PKI / HSM · IT / OT / IoT · Security consulting</text>' +
    '<text x="64" y="560" font-family="Arial,sans-serif" font-size="20" fill="#b8d3dc">kmanu225.github.io</text></svg>';
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
    await page.setContent('<style>body{margin:0}svg{display:block}</style>' + svg);
    await page.screenshot({ path: path.join(root, 'images/social-card.png') });
    await page.setViewportSize({ width: 192, height: 192 });
    const icon = await fs.readFile(path.join(root, 'images/ek-mark.svg'), 'utf8');
    await page.setContent('<style>body{margin:0}svg{display:block;width:192px;height:192px}</style>' + icon);
    await page.screenshot({ path: path.join(root, 'images/ek-icon-192.png') });
  } finally { await browser.close(); }
  for (const file of ['profile.webp','social-card.png','ek-icon-192.png']) {
    const data = await fs.stat(path.join(root,'images',file));
    console.log(file, data.size, 'bytes');
  }
})().catch(error => { console.error(error); process.exitCode=1; });
