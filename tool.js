// import puppeteer from "puppeteer";
const puppeteer = require("puppeteer");

(async () => {
    // or /usr/bin/chromium 
    const browser = await puppeteer.launch({ headless: false, executablePath: "/usr/bin/google-chrome", args: ["--no-sandbox"] });
    // const page = await browser.newPage();

    // await page.goto('https://developer.chrome.com/');

    // // Set screen size
    // await page.setViewport({ width: 1080, height: 1024 });
})();