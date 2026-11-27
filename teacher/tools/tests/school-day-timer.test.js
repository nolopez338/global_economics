const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

const context = vm.createContext({ window: {} });
for (const file of ['databases/year-calendar-data.js', 'school-day-timer.js']) {
  vm.runInContext(fs.readFileSync(path.join(__dirname, '../../assets/js', file), 'utf8'), context);
}
const timer = context.window.SchoolDayTimer;
const at = time => new Date(`2026-11-10T${time}`);

test('local calendar and countdown across a complete school day', () => {
  for (const [time, label, remaining] of [
    ['06:30:00', 'Contact starts in', '15:00'],
    ['06:45:00', 'Contact ends in', '15:00'],
    ['07:00:00', '1st Hour starts in', '5:00'],
    ['07:05:00', '1st Hour ends in', '50:00'],
    ['07:30:00', '1st Hour ends in', '25:00'],
    ['07:55:00', '2nd Hour starts in', '5:00'],
    ['07:59:59.999', '2nd Hour starts in', '0:01'],
    ['08:00:00', '2nd Hour ends in', '50:00'],
    ['09:45:00', 'Break ends in', '30:00'],
    ['10:15:00', '4th Hour ends in', '50:00'],
    ['12:55:00', 'Lunch ends in', '1:00:00'],
    ['13:55:00', '7th Hour ends in', '50:00'],
    ['14:45:00', 'Pause ends in', '15:00'],
    ['15:00:00', 'Final Hour ends in', '1:00:00'],
    ['16:00:00', 'School day ended', ''],
    ['23:59:59', 'School day ended', '']
  ]) {
    const state = timer.countdownAt(at(time));
    assert.deepEqual({ label: state.label, remaining: state.remaining }, { label, remaining }, time);
    assert.equal(Number.isFinite(state.remainingSeconds), Boolean(remaining), time);
  }
});

test('every period uses start-inclusive, end-exclusive intervals', () => {
  for (const period of timer.periods) {
    assert.equal(timer.countdownAt(at(`${period.startText}:00`)).label, `${period.name} ends in`);
    assert.notEqual(timer.countdownAt(at(`${period.endText}:00`)).label, `${period.name} ends in`);
  }
});

test('non-school days and failed or absent calendar data have no countdown', () => {
  for (const [date, label] of [
    ['2026-11-14', 'Weekend · no school'],
    ['2026-11-16', 'School holiday'],
    ['2026-12-24', 'Not a school day'],
    ['2028-01-03', 'Calendar unavailable']
  ]) {
    assert.deepEqual({ ...timer.countdownAt(new Date(`${date}T08:00:00`)) }, { label, remaining: '', remainingSeconds: null });
  }
  for (const calendar of [null, {}, { getAcademicDateInfo() { throw Error('offline'); } }]) {
    assert.deepEqual({ ...timer.countdownAt(at('08:00:00'), calendar) }, { label: 'Calendar unavailable', remaining: '', remainingSeconds: null });
  }
});

test('raw remaining seconds retain subsecond precision at urgency boundaries', () => {
  for (const [time, seconds, remaining] of [
    ['07:34:59.999', 1200.001, '20:01'],
    ['07:35:00', 1200, '20:00'],
    ['07:35:00.001', 1199.999, '20:00'],
    ['07:49:59.999', 300.001, '5:01'],
    ['07:50:00', 300, '5:00'],
    ['07:50:00.001', 299.999, '5:00'],
    ['07:53:59.999', 60.001, '1:01'],
    ['07:54:00', 60, '1:00'],
    ['07:54:00.001', 59.999, '1:00']
  ]) {
    const state = timer.countdownAt(at(time));
    assert.ok(Math.abs(state.remainingSeconds - seconds) < 1e-9, time);
    assert.equal(state.remaining, remaining, time);
  }
});

test('format matches the original timer view and clamps negative values', () => {
  for (const [seconds, text] of [[-10, '0:00'], [0, '0:00'], [.001, '0:01'], [59.1, '1:00'], [3599, '59:59'], [3600, '1:00:00'], [3661, '1:01:01']]) {
    assert.equal(timer.durationText(seconds), text);
  }
});
