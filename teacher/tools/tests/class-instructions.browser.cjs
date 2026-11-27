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

    async function checkSeating() {
      assert.deepEqual(await page.evaluate(() => {
        const problems = [];
        const seats = [...document.querySelectorAll('.classroom-seat')];
        const monitors = [...document.querySelectorAll('.monitor-seat')];
        const rows = [...document.querySelectorAll('.classroom-row')];
        const board = document.querySelector('.classroom-board').getBoundingClientRect();
        if (seats.length !== 20 || monitors.length !== 4 || rows.length !== 4) problems.push('seat/monitor/row count');
        if (seats.some(seat => seat.getBoundingClientRect().bottom >= board.top)) problems.push('board must be below all seats');
        rows.forEach((row, index) => {
          const rowSeats = [...row.querySelectorAll('.classroom-seat')];
          if (row.querySelector('.row-label').textContent !== `Row ${index + 1}`) problems.push('row label');
          if (rowSeats.length !== 5 || row.querySelectorAll('.monitor-seat').length !== 1) problems.push('five seats and one monitor per row');
          if (!rowSeats[0].classList.contains('monitor-seat')) problems.push('monitor is not the farthest seat');
          if (rowSeats.slice(1).some(seat => seat.getBoundingClientRect().top <= rowSeats[0].getBoundingClientRect().bottom)) problems.push('monitor position/seat overlap');
          rowSeats.forEach((seat, position) => {
            const reference = rows[0].querySelectorAll('.classroom-seat')[position].getBoundingClientRect();
            if (Math.abs(seat.getBoundingClientRect().top - reference.top) > 1) problems.push('seats staggered across columns');
          });
          const label = rowSeats[0].querySelector('.monitor-name');
          const range = document.createRange();
          range.selectNodeContents(label);
          for (const r of range.getClientRects()) {
            const seat = rowSeats[0].getBoundingClientRect();
            if (r.left < seat.left || r.right > seat.right || r.bottom > seat.bottom) problems.push('name outside monitor seat');
          }
        });
        return problems;
      }), []);
    }

    const monitor = row => page.locator(`.monitor-seat[data-row="${row}"]`);
    const assignedName = row => monitor(row).locator('.monitor-name');
    const input = page.getByLabel('Monitor’s name', { exact: true });
    const dialog = page.getByRole('dialog');
    async function checkEditorLayout(target) {
      const editor = target.getByRole('dialog');
      assert.deepEqual(await editor.evaluate(el => {
        const r = el.getBoundingClientRect();
        const problems = [];
        if (r.left < 0 || r.top < 0 || r.right > innerWidth || r.bottom > innerHeight) problems.push('editor outside viewport');
        if (el.scrollWidth > el.clientWidth) problems.push('editor horizontal overflow');
        return problems;
      }), []);
      for (const control of await editor.locator('input, button').all()) {
        await control.scrollIntoViewIfNeeded();
        const r = await control.boundingBox();
        const bounds = await editor.boundingBox();
        assert(r.x >= bounds.x && r.x + r.width <= bounds.x + bounds.width, 'editor control fits horizontally');
        assert(r.y >= bounds.y && r.y + r.height <= bounds.y + bounds.height, 'editor control reachable vertically');
      }
    }
    const requests = [];
    const recordRequest = request => requests.push(request.url());
    page.on('request', recordRequest);
    await page.setViewportSize({ width: 1280, height: 720 });
    await checkSeating();
    await monitor(1).dblclick();
    assert(await dialog.isVisible());
    assert(await input.evaluate(el => el === document.activeElement));
    await input.fill('  Ana María  ');
    await input.press('Enter');
    assert.equal(await assignedName(1).textContent(), 'Ana María');
    assert(await dialog.isHidden());
    assert(await monitor(1).evaluate(el => el === document.activeElement));

    await monitor(1).press('Enter');
    assert.equal(await input.inputValue(), 'Ana María');
    await input.fill('Cancelled edit');
    await input.press('Escape');
    assert.equal(await assignedName(1).textContent(), 'Ana María');
    await monitor(2).press('Space');
    const literalName = '<img src=x onerror=alert(1)>';
    await input.fill(literalName);
    await page.getByRole('button', { name: 'Save', exact: true }).click();
    assert.equal(await assignedName(2).textContent(), literalName);
    assert.equal(await monitor(2).locator('img').count(), 0, 'entered markup stays text');

    await page.getByRole('button', { name: 'Assign or edit Row 2 monitor', exact: true }).click();
    await page.getByRole('button', { name: 'Clear name', exact: true }).click();
    assert.equal(await assignedName(2).textContent(), '—');
    await monitor(1).dblclick();
    await input.fill('   ');
    await input.press('Enter');
    assert.equal(await assignedName(1).textContent(), '—', 'blank submission clears assignment');

    const names = ['Ana María', 'Juan Sebastián', 'Camila', 'Mateo'];
    for (let row = 1; row <= 4; row++) {
      await monitor(row).press('Enter');
      await input.fill(names[row - 1]);
      await input.press('Enter');
    }
    await page.getByRole('tab', { name: 'Classroom Rules', exact: true }).click();
    await page.getByRole('tab', { name: 'Before We Begin', exact: true }).click();
    await page.getByRole('tab', { name: 'Row Monitors', exact: true }).click();
    assert.deepEqual(await page.locator('.monitor-name').allTextContents(), names);
    await checkSeating();
    await checkLayout(true);
    await page.screenshot({ path: path.join(screenshots, 'desktop-assigned-monitors.png') });

    await page.locator('#fullscreen-toggle').click();
    await page.waitForFunction(() => document.fullscreenElement);
    await monitor(3).dblclick();
    await input.fill('Cancelled fullscreen edit');
    await checkEditorLayout(page);
    await page.screenshot({ path: path.join(screenshots, 'fullscreen-monitor-editor.png') });
    await input.press('Escape');
    assert.equal(await assignedName(3).textContent(), 'Camila');
    assert(await page.evaluate(() => document.fullscreenElement?.id === 'exam-page'));
    await monitor(3).press('Space');
    await input.fill('Valentina');
    await input.press('Enter');

    // The editor remains usable with a narrow viewport and enlarged text.
    await page.setViewportSize({ width: 320, height: 568 });
    await page.evaluate(() => { document.documentElement.style.fontSize = '200%'; });
    await monitor(4).press('Enter');
    await checkEditorLayout(page);
    await page.getByRole('button', { name: 'Cancel', exact: true }).click();
    await page.evaluate(() => { document.documentElement.style.fontSize = ''; });
    await page.setViewportSize({ width: 1280, height: 720 });
    await page.evaluate(() => document.fullscreenElement.scrollTo(0, 0));
    await checkSeating();
    await checkLayout(true);
    await page.locator('#fullscreen-toggle').click();
    await page.waitForFunction(() => !document.fullscreenElement);
    assert.deepEqual(requests, [], 'editing and switching tabs make no network requests');
    page.off('request', recordRequest);

    await page.reload();
    await page.getByRole('tab', { name: 'Row Monitors', exact: true }).click();
    assert.deepEqual(await page.locator('.monitor-name').allTextContents(), Array(4).fill('—'));
    // Exercise a maximum-length, unbroken name at narrow widths and enlarged text.
    await monitor(4).press('Enter');
    await input.fill('A'.repeat(40));
    await input.press('Enter');

    for (const [width, height, fontSize] of [[390, 844, '100%'], [320, 568, '100%'], [1280, 720, '200%'], [390, 844, '200%']]) {
      await page.setViewportSize({ width, height });
      await page.evaluate(size => { document.documentElement.style.fontSize = size; }, fontSize);
      for (const name of ['Before We Begin', 'Classroom Rules', 'Row Monitors']) {
        await page.getByRole('tab', { name, exact: true }).click();
        await page.evaluate(() => scrollTo(0, 0));
        await checkLayout(false);
        if (name === 'Row Monitors') await checkSeating();
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
        if (name === 'Row Monitors') await checkSeating();
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

    const touchContext = await browser.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
    try {
      const touchPage = await touchContext.newPage();
      await touchPage.goto(page.url());
      await touchPage.getByRole('tab', { name: 'Row Monitors', exact: true }).tap();
      await touchPage.getByRole('button', { name: 'Assign or edit Row 1 monitor', exact: true }).tap();
      await touchPage.getByLabel('Monitor’s name', { exact: true }).fill('Isabella');
      await touchPage.getByRole('button', { name: 'Save', exact: true }).tap();
      assert.equal(await touchPage.locator('.monitor-name').first().textContent(), 'Isabella');
      await touchPage.getByRole('button', { name: 'Assign or edit Row 1 monitor', exact: true }).tap();
      await touchPage.getByLabel('Monitor’s name', { exact: true }).fill('Cancelled touch edit');
      await checkEditorLayout(touchPage);
      await touchPage.screenshot({ path: path.join(screenshots, 'mobile-monitor-editor.png'), fullPage: true });
      await touchPage.getByRole('button', { name: 'Cancel', exact: true }).tap();
      assert.equal(await touchPage.locator('.monitor-name').first().textContent(), 'Isabella');
    } finally {
      await touchContext.close();
    }
    assert.equal(await page.locator('img').evaluateAll(images => images.every(img => img.complete && img.naturalWidth > 0)), true);
    assert.deepEqual(errors, []);
    console.log(`Class tabs passed: 20 seats/four rear monitors, editing/clearing/cancelling, keyboard/touch, safe names, tab retention/reload reset, no edit requests, all fullscreen sizes/timer states, mobile, enlarged text, images and console. Screenshots: ${screenshots}`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
