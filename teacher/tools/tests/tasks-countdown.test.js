const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

const source = fs.readFileSync(path.join(__dirname, '../../assets/js/tasks.js'), 'utf8');

// A small DOM adapter runs the actual page script, including its save listeners.
function page(data, now) {
  class Element {
    constructor(tag) {
      this.tagName = tag;
      this.children = [];
      this.dataset = {};
      this.listeners = {};
      this.hidden = false;
      this.isConnected = true;
      this.className = '';
      this.attributes = {};
      this.classes = new Set();
      this.classList = { toggle: (name, on) => on ? this.classes.add(name) : this.classes.delete(name) };
    }
    append(...children) { this.children.push(...children); }
    appendChild(child) { this.append(child); }
    replaceChildren(...children) { this.children = children; }
    closest() { return table; }
    setAttribute(name, value) { this.attributes[name] = value; }
    addEventListener(name, listener) { this.listeners[name] = listener; }
    querySelector(selector) { return this.querySelectorAll(selector)[0]; }
    querySelectorAll(selector) {
      return this.children.flatMap(child => [
        ...(selector === '[data-task-deadline]' ? child.dataset.taskDeadline !== undefined : child.className.split(' ').includes(selector.slice(1))) ? [child] : [],
        ...child.querySelectorAll(selector)
      ]);
    }
    click() { return this.listeners.click(); }
  }
  const table = new Element('table');
  const ids = {};
  for (const id of ['tasks-table-body', 'tasks-empty', 'connect-repository', 'add-task', 'save-tasks', 'task-save-status', 'task-dirty-status']) ids[id] = new Element('div');
  table.append(ids['tasks-table-body']);
  const back = new Element('a');
  let tick;
  let stored;
  const events = {};
  const handle = {
    getDirectoryHandle: async () => handle,
    getFileHandle: async () => handle,
    createWritable: async () => ({ write: async value => { stored = value; }, close: async () => {} })
  };
  const window = {
    location: { search: '' }, magisTasks: data,
    setInterval: fn => { tick = fn; },
    addEventListener: (name, fn) => { events[name] = fn; },
    showDirectoryPicker: async () => handle
  };
  class Clock extends Date { static now() { return now; } }
  vm.runInNewContext(source, {
    window, Date: Clock, URLSearchParams, Intl,
    document: {
      getElementById: id => ids[id], createElement: tag => new Element(tag),
      querySelector: () => back, querySelectorAll: selector => table.querySelectorAll(selector)
    }
  });
  return {
    ids, window, events,
    cells: () => table.querySelectorAll('[data-task-deadline]'),
    advance: ms => { now += ms; tick(); },
    saved: () => stored
  };
}

function text(cell) { return cell.querySelector('.task-countdown-text').textContent; }
function button(cell) { return cell.querySelector('.task-postpone-button'); }

test('elapsed time floors hours across day boundaries and preserves invalid/future formatting', () => {
  const now = Date.parse('2026-10-19T12:00:00-05:00');
  const elapsed = [0, 1, 3599999, 3600000, 86399999, 86400000, 183600000];
  const p = page(elapsed.map(ms => ({ dueDate: new Date(now - ms).toISOString() })).concat([
    { dueDate: 'invalid' }, { dueDate: '' }, { dueDate: new Date(now + 90061000).toISOString() }
  ]), now);
  assert.deepEqual(p.cells().map(text), [
    'Overdue by 0days-0hours', 'Overdue by 0days-0hours', 'Overdue by 0days-0hours',
    'Overdue by 0days-1hours', 'Overdue by 0days-23hours', 'Overdue by 1days-0hours',
    'Overdue by 2days-3hours', 'Invalid date', 'Invalid date', '1d 1h 1m 1s'
  ]);
  assert.deepEqual(p.cells().map(cell => button(cell).hidden), [false, false, false, false, false, false, false, true, true, true]);
});

test('timer transition retains the same button and activates its listener', () => {
  const now = Date.parse('2026-10-19T12:00:00-05:00');
  const p = page([{ dueDate: new Date(now + 1000).toISOString() }], now);
  const cell = p.cells()[0];
  const original = button(cell);
  assert.equal(original.hidden, true);
  p.advance(1001);
  assert.equal(text(cell), 'Overdue by 0days-0hours');
  assert.equal(button(cell), original);
  assert.equal(original.hidden, false);
  assert.equal(original.type, 'button');
  assert.match(original.attributes['aria-label'], /task 1/);
  original.click();
  assert.equal(text(cell), '0d 23h 59m 59s');
  assert.equal(original.hidden, true);
});

test('repeated postponements preserve the existing deadline, save and reload', async () => {
  const original = '2026-10-16T08:17:43-05:00';
  const data = [{ description: 'Example', dueDate: original }];
  const now = Date.parse('2026-10-19T12:00:00-05:00');
  const p = page(data, now);
  const cell = p.cells()[0];
  await p.ids['connect-repository'].click();
  for (let i = 1; i <= 4; i++) {
    button(cell).click();
    assert.equal(Number(cell.dataset.taskDeadline), Date.parse(original) + i * 86400000);
    assert.equal(button(cell).hidden, i === 4);
    if (i === 1) assert.equal(text(cell), 'Overdue by 2days-3hours');
  }
  assert.match(p.ids['tasks-table-body'].children[0].children[2].children[0].value, /20\/10\/2026 08:17/);
  assert.equal(p.ids['save-tasks'].disabled, false);
  let warned = false;
  p.events.beforeunload({ preventDefault() { warned = true; } });
  assert.equal(warned, true);
  await p.ids['save-tasks'].click();
  assert.equal(data[0].dueDate, original, 'source task data is untouched');
  const savedWindow = {};
  vm.runInNewContext(p.saved(), { window: savedWindow });
  assert.equal(savedWindow.magisTasks[0].dueDate, '2026-10-20T08:17:43-05:00');
  assert.equal(p.ids['task-dirty-status'].hidden, true);
  const reloaded = page(savedWindow.magisTasks, now);
  assert.equal(text(reloaded.cells()[0]), '0d 20h 17m 43s');
  assert.equal(button(reloaded.cells()[0]).hidden, true);
});
