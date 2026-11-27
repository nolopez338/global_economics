// Dev-only: run with Playwright available on NODE_PATH and installed Chrome.
const assert = require('node:assert/strict');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    for (const name of ['class', 'exam']) {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.clock.install({ time: new Date('2026-11-10T07:05:00') });
      await page.clock.pauseAt(new Date('2026-11-10T07:05:00'));
      await page.goto(pathToFileURL(path.resolve(__dirname, `../../pages/${name}_instructions.html`)).href);
      const tickAt = async time => {
        await page.clock.setFixedTime(new Date(time.includes('T') ? time : `2026-11-10T${time}`));
        await page.clock.runFor(250);
      };
      const state = () => page.locator('#timer-value').evaluate(el => ({
        text: el.textContent, hidden: el.hidden, urgency: el.dataset.urgency || null,
        shaking: el.classList.contains('is-urgent'), color: getComputedStyle(el).color,
        animation: getComputedStyle(el).animationName,
        scale: getComputedStyle(el.firstElementChild).transform
      }));
      for (const [time, text, urgency, shaking] of [
        ['07:34:59.999', '20:01', 'green', false],
        ['07:35:00', '20:00', 'yellow', false],
        ['07:35:00.001', '20:00', 'yellow', false],
        ['07:49:59.999', '5:01', 'yellow', false],
        ['07:50:00', '5:00', 'yellow', false],
        ['07:50:00.001', '5:00', 'red', false],
        ['07:53:59.999', '1:01', 'red', false],
        ['07:54:00', '1:00', 'red', false],
        ['07:54:00.001', '1:00', 'red', true],
        ['07:59:59.999', '0:01', 'red', true],
        ['08:00:00', '50:00', 'green', false],
        ['12:55:00', '1:00:00', 'green', false]
      ]) {
        await tickAt(time);
        const actual = await state();
        assert.equal(actual.text, text, time);
        assert.equal(actual.urgency, urgency, time);
        assert.equal(actual.shaking, shaking, time);
        assert.equal(actual.animation, shaking ? 'countdown-shake' : 'none', time);
        assert.equal(actual.scale, 'matrix(2, 0, 0, 2, 0, 0)', time);
        assert.equal(actual.color, { green: 'rgb(145, 223, 154)', yellow: 'rgb(255, 224, 130)', red: 'rgb(255, 138, 128)' }[urgency]);
      }
      await tickAt('07:54:30');
      await page.emulateMedia({ reducedMotion: 'reduce' });
      assert.equal((await state()).animation, 'none');
      assert.equal((await state()).urgency, 'red');
      await page.emulateMedia({ reducedMotion: 'no-preference' });
      assert.equal((await state()).animation, 'countdown-shake');

      // Every change of schedule target must discard the previous target's urgency.
      const periods = await page.evaluate(() => window.SchoolDayTimer.periods);
      for (const period of periods) {
        const end = new Date(`2026-11-10T${period.endText}:00`);
        await tickAt(new Date(end - 1).toISOString());
        assert.equal((await state()).shaking, true);
        await tickAt(end.toISOString());
        assert.equal((await state()).shaking, false);
        await tickAt(`${period.startText}:00`);
        assert.equal(await page.locator('#timer-label').textContent(), `${period.name} ends in`);
      }
      for (const date of ['2026-11-10T16:00:00', '2026-11-14T08:00:00', '2026-11-16T08:00:00', '2026-12-24T08:00:00', '2028-01-03T08:00:00']) {
        await tickAt('07:54:30');
        await tickAt(date);
        const actual = await state();
        assert.equal(actual.hidden, true, date);
        assert.equal(actual.text, '', date);
        assert.equal(actual.urgency, null, date);
        assert.equal(actual.shaking, false, date);
        assert.equal(actual.animation, 'none', date);
      }
      await tickAt('07:54:30');
      await page.evaluate(() => {
        window.savedCalendar = window.academicCalendar;
        window.academicCalendar = { getAcademicDateInfo() { throw Error('offline'); } };
      });
      await page.clock.runFor(250);
      assert.equal((await state()).urgency, null);
      assert.equal((await state()).shaking, false);
      await page.evaluate(() => { window.academicCalendar = window.savedCalendar; });
      await page.clock.runFor(250);
      assert.equal((await state()).shaking, true);

      await page.clock.resume();
      for (const [width, height] of [[1440, 900], [390, 844], [320, 568], [1920, 1080]]) {
        await page.setViewportSize({ width, height });
        await tickAt('07:05:00');
        const before = await page.locator('.instructions').boundingBox();
        await page.locator('#fullscreen-toggle').click();
        await page.waitForFunction(() => document.fullscreenElement?.id === 'exam-page');
        await page.waitForFunction(() => document.querySelector('#fullscreen-toggle').getAttribute('aria-pressed') === 'true');
        assert.equal(await page.evaluate(() => document.fullscreenElement?.id), 'exam-page');
        assert.equal(await page.locator('#fullscreen-toggle').getAttribute('aria-pressed'), 'true');
        assert.equal((await state()).scale, 'matrix(2, 0, 0, 2, 0, 0)');
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
        await page.locator('#fullscreen-toggle').click();
        await page.waitForFunction(() => !document.fullscreenElement);
        await page.waitForFunction(() => document.querySelector('#fullscreen-toggle').getAttribute('aria-pressed') === 'false');
        assert.equal(await page.evaluate(() => document.fullscreenElement), null);
        assert.equal(await page.locator('#fullscreen-toggle').getAttribute('aria-pressed'), 'false');
        assert.deepEqual(await page.locator('.instructions').boundingBox(), before);
      }
      assert.deepEqual(errors, []);
      await page.close();
    }
    console.log('Both instruction pages passed: raw-time thresholds, target changes, inactive calendars, reduced motion, 2× scale, and desktop/mobile/fullscreen controls.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
