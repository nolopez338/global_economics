// Dev-only: run with Playwright on NODE_PATH and installed Chrome.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '../../..');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const screenshots = process.env.CLASS_VIEW_SCREENSHOTS || path.join(os.tmpdir(), 'class-view-qa');
  fs.mkdirSync(screenshots, { recursive: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    page.setDefaultTimeout(10000);
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.clock.install({ time: new Date('2026-11-10T10:05:00') });
    await page.goto(pathToFileURL(path.join(root, 'teacher/pages/class_view.html')).href + '?origin=schedule-teacher', { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => document.querySelector('.presentation-hour').textContent === '10');
    const triggers = ['fullscreen-toggle', 'minimal-toggle', 'page-fullscreen-toggle', 'resize-clock', 'resize-minimal', 'resize-page'];
    const visibleControls = () => page.locator('button:visible, a:visible, input:visible').evaluateAll(nodes => nodes.map(node => node.id));
    const settled = () => page.waitForFunction(() => !document.querySelector('#presentation-exit').disabled);
    async function restored(trigger) {
      await page.waitForFunction(() => !document.querySelector('.class-view').classList.contains('presentation-active'));
      assert.equal(await page.locator('#presentation-exit').isVisible(), false);
      for (const id of [...triggers, 'timer-toggle', 'dark-mode-toggle', 'return-link']) {
        assert.equal(await page.locator(`#${id}`).isVisible(), true, `${id} restored after ${trigger}`);
      }
      assert.equal(await page.evaluate(() => document.activeElement.id), trigger);
      assert.equal(await page.evaluate(() => document.fullscreenElement), null);
      assert.equal(await page.locator('.class-view').evaluate(el => el.classList.contains('window-fit')), false);
    }
    async function presentation(trigger) {
      await page.locator(`#${trigger}`).click();
      await settled();
      if (trigger === 'fullscreen-toggle' || trigger === 'page-fullscreen-toggle') {
        await page.waitForFunction(() => !!document.fullscreenElement || document.querySelector('#presentation-message').textContent);
        assert.equal(await page.evaluate(() => !!document.fullscreenElement), true, `${trigger}: ${await page.locator('#presentation-message').textContent()}`);
      }
      assert.deepEqual(await visibleControls(), ['presentation-exit'], trigger);
      assert.equal(await page.evaluate(() => document.activeElement.id), 'presentation-exit');
      assert.equal(await page.locator('#timer-dialog').isVisible(), false);
      assert.equal(await page.locator('#presentation-exit').textContent(), '‹');
      assert.equal(await page.locator('#presentation-exit').getAttribute('aria-label'), 'Return to the full page');
      assert.equal(await page.locator('#presentation-exit').evaluate(el => getComputedStyle(el).borderWidth), '0px');
    }
    async function icons() {
      for (const id of triggers) {
        const result = await page.locator(`#${id}`).evaluate(el => {
          const svg = el.querySelector('svg'), circle = svg.querySelector('circle');
          const box = el.getBoundingClientRect(), shape = circle.getBoundingClientRect();
          const text = svg.querySelector('text');
          const glyph = text?.getBBox();
          return { label: el.getAttribute('aria-label'), width: box.width, height: box.height,
            r: +circle.getAttribute('r'), stroke: getComputedStyle(circle).strokeWidth,
            text: text?.textContent || '', pen: !!svg.querySelector('path'),
            centered: Math.abs((shape.left + shape.right - box.left - box.right) / 2) < 1,
            textFits: !glyph || (glyph.width < circle.r.baseVal.value * 2 && glyph.height < circle.r.baseVal.value * 2) };
        });
        assert(result.label && result.width >= 44 && result.height >= 44 && result.centered && result.textFits, id);
        assert.equal(result.stroke, '1px');
        if (['fullscreen-toggle', 'resize-clock'].includes(id)) {
          assert.equal(result.text, '');
          assert.equal(result.pen, false);
          assert.equal(result.r, 8);
        } else {
          assert.equal(result.text, '10');
          const writing = ['page-fullscreen-toggle', 'resize-page'].includes(id);
          assert.equal(result.pen, writing);
          assert.equal(result.r, writing ? 6.5 : 8);
        }
      }
    }
    assert.equal(await page.locator('#return-link').getAttribute('href'), '../schedule-teacher.html');
    assert.equal(await page.locator('#return-link').textContent(), '‹');
    for (const [width, height] of [[1440, 900], [390, 844], [320, 568]]) {
      await page.setViewportSize({ width, height });
      await icons();
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
      await page.screenshot({ path: path.join(screenshots, `controls-${width}.png`) });
      for (const trigger of triggers) {
        await presentation(trigger);
        const exit = await page.locator('#presentation-exit').boundingBox();
        assert(exit.x >= 0 && exit.y >= 0 && exit.x + exit.width <= width && exit.y + exit.height <= height);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, trigger);
        if (width === 1440) await page.screenshot({ path: path.join(screenshots, `${trigger}.png`) });
        await page.locator('#presentation-exit').click();
        await restored(trigger);
      }
    }
    await page.setViewportSize({ width: 1440, height: 900 });
    // Browser/native exit must work for both fullscreen targets.
    for (const trigger of ['fullscreen-toggle', 'page-fullscreen-toggle']) {
      await presentation(trigger);
      await page.evaluate(() => document.exitFullscreen());
      await restored(trigger);
    }
    // The active timer and theme survive both presentation families and returning.
    await page.locator('#dark-mode-toggle').check();
    await page.locator('#timer-toggle').click();
    await page.locator('#timer-minutes').fill('8');
    await page.locator('#timer-form button[type=submit]').click();
    for (const trigger of triggers) {
      await presentation(trigger);
      assert.equal(await page.locator('#timer-visual').isVisible(), true);
      await page.locator('#presentation-exit').click();
      await restored(trigger);
      assert.equal(await page.locator('#timer-toggle').getAttribute('aria-pressed'), 'true');
      assert.equal(await page.locator('#dark-mode-toggle').isChecked(), true);
    }
    await page.screenshot({ path: path.join(screenshots, 'dark-timer.png') });
    // Keep keyboard checks after native fullscreen checks: Chromium may
    // suppress fullscreen reentry after keyboard-driven exits.
    // Every hidden control must also leave the keyboard tab order.
    await page.locator('#resize-page').focus();
    await page.keyboard.press('Enter');
    await settled();
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.closest('.class-view-controls')), null);
    await page.locator('#presentation-exit').focus();
    await page.keyboard.press('Space');
    await restored('resize-page');
    for (const trigger of ['minimal-toggle', 'resize-clock', 'resize-minimal', 'resize-page']) {
      await presentation(trigger);
      await page.keyboard.press('Escape');
      await restored(trigger);
    }
    await page.clock.setFixedTime(new Date('2026-11-10T11:05:00'));
    await page.waitForFunction(() => [...document.querySelectorAll('.presentation-hour')].every(el => el.textContent === '11'));
    await page.clock.setFixedTime(new Date('2026-11-11T00:05:00'));
    await page.waitForFunction(() => [...document.querySelectorAll('.presentation-hour')].every(el => el.textContent === '12'));
    // A denied fullscreen request must still leave a usable return-only view.
    await page.evaluate(() => { document.documentElement.requestFullscreen = () => Promise.reject(Error('blocked for test')); });
    await page.locator('#page-fullscreen-toggle').click();
    await settled();
    assert.deepEqual(await visibleControls(), ['presentation-exit']);
    assert.match(await page.locator('#presentation-message').textContent(), /blocked/);
    await page.locator('#presentation-exit').click();
    await restored('page-fullscreen-toggle');
    assert.deepEqual(errors, []);
    console.log(`PASS: six presentation controls, both fullscreen targets, return/Escape/focus, live-hour icons, timer/theme, and desktop/mobile layouts. Screenshots: ${screenshots}`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
