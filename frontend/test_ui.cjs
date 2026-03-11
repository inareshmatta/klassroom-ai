const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    page.on('console', msg => {
        if (msg.type() === 'error') {
            console.log(`PAGE ERROR: ${msg.text()}`);
        } else {
            console.log(`PAGE LOG: ${msg.text()}`);
        }
    });

    page.on('pageerror', error => {
        console.log(`UNHANDLED EXCEPTION: ${error.message}`);
    });

    await page.goto('http://localhost:8080');
    
    // Click "Open App" or "Start Learning Free"
    console.log("Looking for enter button...");
    await page.waitForTimeout(1000);
    const enterBtn = await page.$('.btn-nav-cta, .btn-primary-cta');
    if (enterBtn) {
        await enterBtn.click();
        console.log("Clicked enter button.");
    }

    // Wait for the main app
    await page.waitForTimeout(2000);
    console.log("Looking for Start Tutor button...");
    const startTutorBtn = await page.$('#btn-start-tutor');
    
    if (startTutorBtn) {
        await startTutorBtn.click();
        console.log("Clicked Start Tutor button.");
        await page.waitForTimeout(5000);
    } else {
        console.log("Start Tutor button not found.");
    }

    await browser.close();
})();
