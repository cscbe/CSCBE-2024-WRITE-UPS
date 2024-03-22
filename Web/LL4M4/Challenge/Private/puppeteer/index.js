const puppeteer = require('puppeteer');
const jwt = require('jsonwebtoken');

const CONFIG = {
  APPNAME: process.env['APPNAME'],
  APPURL: process.env['APPURL'],
  APPLIMITTIME: Number(process.env['APPLIMITTIME'] || "60"),
  APPLIMIT: Number(process.env['APPLIMIT'] || "5"),
}
console.table(CONFIG)

const secretKey = process.env['SECRET'];
const payload = { flag: process.env['FLAG'], username: 'admin' };
const token = jwt.sign(payload, secretKey);

const initBrowser = puppeteer.launch({
  executablePath: "/usr/bin/chromium-browser",
  headless: 'new',
  args: [
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-gpu',
    '--no-gpu',
    '--disable-default-apps',
    '--disable-translate',
    '--disable-device-discovery-notifications',
    '--disable-software-rasterizer',
    '--disable-xss-auditor'
  ],
  ipDataDir: '/home/admin-bot/data/',
  ignoreHTTPSErrors: true
});

console.log("Admin bot started...");

const bot = async (urlToVisit) => {
  const browser = await initBrowser;
  const context = await browser.createIncognitoBrowserContext()
  try {
    const page = await context.newPage();

    await page.setCookie({
      name: "Cookie",
      httpOnly: false,
      value: token,
      url: CONFIG.APPURL
    })

    // Visit admin dashboard
    await page.goto(urlToVisit, {
      waitUntil: 'networkidle2'
    });
    await page.waitForTimeout(5000);
    await context.close()
    return true;
  } catch (e) {
    console.error(e);
    await context.close();
    return false;
  }
}

setInterval(() => {
  bot(CONFIG.APPURL);
}, 30000);

