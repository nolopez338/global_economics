// Dev-only: NODE_PATH must provide Playwright; uses installed Chrome.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const screenshots = process.env.CLASS_INSTRUCTIONS_SCREENSHOTS || path.join(os.tmpdir(), 'class-instructions-qa');
  fs.mkdirSync(screenshots, { recursive: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
    await page.clock.install({ time: new Date('2026-11-10T12:55:00') });
    await page.clock.pauseAt(new Date('2026-11-10T12:55:00'));
    await page.goto(pathToFileURL(path.resolve(__dirname, '../../pages/class_instructions.html')).href);
    const tickAt = async time => {
      await page.clock.setFixedTime(new Date(`2026-11-10T${time}`));
      await page.clock.runFor(250);
    };
    const selected = () => page.locator('[role="tab"][aria-selected="true"]');
    assert.equal(await selected().textContent(), 'Before We Begin');

    async function checkLayout(fits) {
      const problems = await page.evaluate(fits => {
        const problems = [];
        const visible = el => el.getClientRects().length > 0;
        const box = el => el.getBoundingClientRect();
        const panel = document.querySelector('[role="tabpanel"]:not([hidden])');
        const header = document.querySelector('.page-header');
        const nav = document.querySelector('nav');
        const shell = document.fullscreenElement || document.documentElement;
        if (shell.scrollWidth > innerWidth + 1) problems.push('horizontal document overflow');
        if (fits && shell.scrollHeight > innerHeight + 1) problems.push('vertical document overflow');
        if (box(header).bottom > box(nav).top) problems.push('header/navigation overlap');
        if (box(nav).bottom > box(panel).top) problems.push('navigation/panel overlap');
        const digits = document.querySelector('.timer-digits');
        if (visible(digits)) {
          const d = box(digits), title = box(document.querySelector('h1'));
          if (d.left < 0 || d.right > innerWidth || d.bottom > box(nav).top) problems.push('timer outside reserved space');
          if (d.left < title.right && d.right > title.left && d.top < title.bottom && d.bottom > title.top) problems.push('timer/title overlap');
        }
        for (const el of [panel, ...panel.querySelectorAll('*')]) {
          const style = getComputedStyle(el);
          if (el.tagName !== 'IMG' && /hidden|clip|scroll|auto/.test(style.overflowY)) problems.push(`panel overflow rule: ${el.className}`);
          const r = box(el);
          if (r.left < -1 || r.right > innerWidth + 1 || (fits && (r.top < -1 || r.bottom > innerHeight + 1))) problems.push(`outside viewport: ${el.className || el.tagName}`);
          // Text ranges also catch lines that paint beyond otherwise fitting boxes.
          for (const node of el.childNodes) {
            if (node.nodeType !== Node.TEXT_NODE || !node.textContent.trim()) continue;
            const range = document.createRange();
            range.selectNodeContents(node);
            for (const r of range.getClientRects()) {
              if (r.left < -1 || r.right > innerWidth + 1 || (fits && r.bottom > innerHeight + 1)) problems.push(`text outside viewport: ${node.textContent.trim()}`);
            }
          }
        }
        if (document.querySelectorAll('[role="tabpanel"]:not([hidden])').length !== 1) problems.push('multiple active panels');
        for (const tab of document.querySelectorAll('[role="tab"]')) {
          const active = tab.getAttribute('aria-selected') === 'true';
          const target = document.getElementById(tab.getAttribute('aria-controls'));
          if (target.hidden === active || target.getAttribute('aria-labelledby') !== tab.id || tab.tabIndex !== (active ? 0 : -1)) problems.push('tab association/state');
          if (!active && visible(target)) problems.push('inactive panel visible');
        }
        return problems;
      }, fits);
      assert.deepEqual(problems, []);
    }

    // Actual fullscreen API at every requested viewport, with long, urgent and hidden timers.
    for (const [width, height] of [[1280, 720], [1366, 768], [1920, 1080]]) {
      await page.setViewportSize({ width, height });
      await page.locator('#fullscreen-toggle').click();
      await page.waitForFunction(() => document.fullscreenElement?.id === 'exam-page');
      assert.deepEqual(await page.evaluate(() => [innerWidth, innerHeight]), [width, height]);
      assert.equal(await page.locator('#fullscreen-toggle').getAttribute('aria-pressed'), 'true');
      for (const time of ['12:55:00', '07:54:30', '16:00:00']) {
        await tickAt(time);
        let header;
        for (const name of ['Before We Begin', 'Classroom Rules', 'Row Monitors']) {
          await page.getByRole('tab', { name, exact: true }).click();
          await checkLayout(true);
          const currentHeader = await page.locator('.page-header').boundingBox();
          if (header) assert.deepEqual(currentHeader, header, 'stable header across tabs');
          header = currentHeader;
          if (time === '12:55:00') await page.screenshot({ path: path.join(screenshots, `${width}-${name.replaceAll(' ', '-')}.png`) });
        }
      }
      await page.locator('#fullscreen-toggle').click();
      await page.waitForFunction(() => !document.fullscreenElement);
      assert.equal(await page.locator('#fullscreen-toggle').getAttribute('aria-pressed'), 'false');
    }

    await tickAt('12:55:00');
    // Automatic activation, wrapping, Home/End, roving focus and panel focus.
    await page.locator('#tab-begin').focus();
    for (const [key, id] of [['ArrowRight', 'tab-rules'], ['ArrowRight', 'tab-monitors'], ['ArrowRight', 'tab-begin'], ['ArrowLeft', 'tab-monitors'], ['Home', 'tab-begin'], ['End', 'tab-monitors']]) {
      await page.keyboard.press(key);
      assert.equal(await selected().getAttribute('id'), id);
      assert.equal(await page.evaluate(() => document.activeElement.id), id);
      assert.notEqual(await selected().evaluate(el => getComputedStyle(el).outlineStyle), 'none');
    }
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'panel-monitors');
    await page.keyboard.press('Shift+Tab');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'tab-monitors');
    await page.keyboard.press('Enter');
    assert.equal(await selected().getAttribute('id'), 'tab-monitors');

    for (const [width, height, fontSize] of [[390, 844, '100%'], [320, 568, '100%'], [1280, 720, '200%'], [390, 844, '200%']]) {
      await page.setViewportSize({ width, height });
      await page.evaluate(size => { document.documentElement.style.fontSize = size; }, fontSize);
      for (const name of ['Before We Begin', 'Classroom Rules', 'Row Monitors']) {
        await page.getByRole('tab', { name, exact: true }).click();
        await page.evaluate(() => scrollTo(0, 0));
        await checkLayout(false);
        const panel = page.getByRole('tabpanel');
        await panel.scrollIntoViewIfNeeded();
        await page.evaluate(() => scrollTo(0, document.documentElement.scrollHeight));
        const bottom = await panel.evaluate(el => el.getBoundingClientRect().bottom);
        assert(bottom <= height, 'panel end reachable by document scrolling');
        if (width === 390 && fontSize === '100%') await page.screenshot({ path: path.join(screenshots, `mobile-${name.replaceAll(' ', '-')}.png`), fullPage: true });
      }
      // A constrained fullscreen shell must also let users reach every instruction.
      await page.locator('#fullscreen-toggle').click();
      await page.waitForFunction(() => document.fullscreenElement);
      for (const name of ['Before We Begin', 'Classroom Rules', 'Row Monitors']) {
        await page.evaluate(() => document.fullscreenElement.scrollTo(0, 0));
        await page.getByRole('tab', { name, exact: true }).click();
        await page.evaluate(() => document.fullscreenElement.scrollTo(0, 0));
        await checkLayout(false);
        const reachable = await page.evaluate(() => {
          const shell = document.fullscreenElement;
          shell.scrollTop = shell.scrollHeight;
          return document.querySelector('[role="tabpanel"]:not([hidden])').getBoundingClientRect().bottom <= innerHeight;
        });
        assert(reachable, 'fullscreen panel end reachable by shell scrolling');
      }
      await page.evaluate(() => document.fullscreenElement.scrollTo(0, 0));
      await page.locator('#fullscreen-toggle').click();
      await page.waitForFunction(() => !document.fullscreenElement);
    }
    assert.equal(await page.locator('img').evaluateAll(images => images.every(img => img.complete && img.naturalWidth > 0)), true);
    assert.deepEqual(errors, []);
    console.log(`Class tabs passed: all fullscreen sizes/timer states, keyboard, mobile, enlarged text, images and console. Screenshots: ${screenshots}`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
