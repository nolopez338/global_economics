"use strict";
const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const calendar = require('../../assets/js/databases/year-calendar-data');
const hash = value => crypto.createHash('sha256').update(JSON.stringify(value)).digest('hex');
const dates = [];
for (const d = new Date('2026-08-01'); d <= new Date('2027-06-30'); d.setUTCDate(d.getUTCDate() + 1)) {
  dates.push(calendar.getAcademicDateInfo(d.toISOString().slice(0, 10)));
}

test('calendar continues six-day labels across May 11–12 and retains June 11', () => {
  for (const [date, label] of Object.entries({
    '2027-05-11': '6-5', '2027-05-12': '6-6', '2027-05-13': '7-1',
    '2027-05-14': '7-2', '2027-05-18': '7-3', '2027-06-10': '9-6',
    '2027-06-11': '10-1'
  })) {
    const info = calendar.getAcademicDateInfo(date);
    assert.equal(`${info.cycleNumber}-${info.cycleDay}`, label, date);
    assert.equal(calendar.getCycleNumber(info.calendarYear, info.month, info.day), info.cycleNumber);
  }
  const schoolDays = dates.filter(info => info.normalizedDate >= '2027-05-11' && info.cycleDay !== null);
  assert.equal(schoolDays.length, 21);
  for (let i = 1; i < schoolDays.length; i++) {
    const previous = schoolDays[i - 1], current = schoolDays[i];
    const wrap = previous.cycleDay === 6 && current.cycleDay === 1;
    assert.equal(current.cycleNumber, previous.cycleNumber + Number(wrap), current.normalizedDate);
    assert.equal(current.cycleDay, previous.cycleDay % 6 + 1);
    assert.equal(current.term, null);
  }
});

test('all earlier calendar records and all date/term/Day/holiday metadata retain their fingerprints', () => {
  assert.equal(hash(dates.filter(info => info.normalizedDate <= '2027-05-11')),
    'f2749f37d98fd713a2196b74b77c878e2bde8e915149c1cebf61c319cc751ca2');
  assert.equal(hash(dates.map(({ cycleNumber, ...info }) => info)),
    'cd63761ceca9499b65aaf8418b03bb7e33a3520a62689854f022bf37c4e89b1d');
});

// Execute the actual Calendar View script so styling regressions are covered
// without adding a browser dependency to the authoring test suite.
function renderCalendar() {
  class Element {
    constructor() {
      this.children = []; this.attributes = {}; this.className = '';
      this.style = { setProperty() {} };
      this.classList = {
        add: name => { this.className += ` ${name}`; },
        contains: name => this.className.split(/\s+/).includes(name),
        toggle: (name, enabled) => { if (enabled) this.classList.add(name); }
      };
    }
    append(...children) { this.children.push(...children); }
    appendChild(child) { this.append(child); }
    replaceChildren(...children) { this.children = children; }
    setAttribute(name, value) { this.attributes[name] = value; }
    addEventListener() {}
  }
  const elements = new Map();
  const document = {
    getElementById(id) { if (!elements.has(id)) elements.set(id, new Element()); return elements.get(id); },
    createElement: () => new Element(), createTextNode: text => ({ textContent: text }),
    documentElement: new Element()
  };
  const html = fs.readFileSync(path.join(__dirname, '../../pages/general_calendar.html'), 'utf8');
  const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];
  vm.runInNewContext(script, {
    document, window: { academicCalendar: calendar, location: { search: '' } },
    localStorage: { getItem: () => null }, URLSearchParams
  });
  const flatten = element => [element, ...(element.children || []).flatMap(flatten)];
  return flatten(elements.get('calendar-year'));
}

test('rendered continuing codes use the existing green style without claiming Term 3', () => {
  const rendered = renderCalendar();
  for (const info of dates.filter(info => info.normalizedDate > '2027-05-11' && info.cycleDay !== null)) {
    const cell = rendered.find(element => element.attributes?.['aria-label']?.startsWith(info.normalizedDate));
    assert.ok(cell, info.normalizedDate);
    assert.ok(!cell.classList.contains('term-3'));
    assert.ok(!cell.attributes['aria-label'].includes('Term 3'));
    const code = cell.children.find(element => element.classList.contains('cycle-day'));
    assert.equal(code.textContent, `${info.cycleNumber}-${info.cycleDay}`);
    assert.ok(code.classList.contains('term-3'), info.normalizedDate);
  }
  const css = fs.readFileSync(path.join(__dirname, '../../assets/css/general_calendar.css'), 'utf8');
  assert.match(css, /\.cycle-day\.term-3\s*\{\s*color: var\(--term-3-code\)/);
});

test('seminar term-scoped cycles retain their historical reset', () => {
  for (const [day, cycle] of [[19, 2], [27, 3]]) {
    assert.equal(calendar.getTermCycleNumber(2027, 5, day), cycle);
  }
  assert.equal(calendar.getTermCycleNumber(2027, 6, 8), 4);
});
