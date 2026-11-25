"use strict";
const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const path = require('node:path');
const w = require('../lesson-workflow');
const validateCalendar = require('../calendar-validation');
const cutoff = '2027 / 05 / 11';
const affected = m => m.Section !== 'Seminar' && m.Date > cutoff;
const hash = value => crypto.createHash('sha256').update(JSON.stringify(value)).digest('hex');
const withoutCorrectedLabels = rows => rows.map(m => {
  const copy = { ...m };
  if (affected(m)) delete copy['Class #'];
  return copy;
});

// Each section has its own preceding slot and finite calendar capacity.
const sections = [
  [10, 'A', '6-2', 7, '2027 / 06 / 11', '10-1'],
  [10, 'B', '6-2', 6, '2027 / 06 / 08', '9-2'],
  [10, 'C', '6-2', 7, '2027 / 06 / 11', '10-1'],
  [10, 'D', '6-1', 7, '2027 / 06 / 10', '9-2'],
  [10, 'E', '6-2', 7, '2027 / 06 / 11', '10-1'],
  [11, 'A', '6-2', 7, '2027 / 06 / 11', '10-1'],
  [11, 'B', '6-2', 6, '2027 / 06 / 04', '9-2'],
  [11, 'C', '6-1', 8, '2027 / 06 / 11', '10-1'],
  [11, 'D', '6-2', 6, '2027 / 06 / 09', '9-2'],
  [11, 'E', '6-1', 8, '2027 / 06 / 11', '10-1']
];

test('post-cutoff labels continue each regular section, including incomplete cycle 6', () => {
  const source = w.readSource(), data = w.build(source);
  const generated = w.readGlobal(path.join(__dirname, '../../assets/js/databases/schedule-data.js'), 'SCHEDULE_DATA');
  assert.deepEqual(generated, data.schedule);
  assert.equal(source.meetings.filter(affected).length, 69);
  for (const [grade, section, preceding, count, endDate, endLabel] of sections) {
    const rows = source.meetings.filter(m => m.Grade === grade && m.Section === section);
    assert.equal(rows.filter(m => m.Date <= cutoff).at(-1)['Class #'], preceding);
    const tail = rows.filter(affected);
    assert.equal(tail.length, count, `${grade}${section} coverage`);
    const [cycle, slot] = preceding.split('-').map(Number);
    const ordinal = (cycle - 1) * 2 + slot;
    const expected = tail.map((_, i) => `${Math.floor((ordinal + i) / 2) + 1}-${(ordinal + i) % 2 + 1}`);
    assert.deepEqual(tail.map(m => m['Class #']), expected, `${grade}${section} sequence`);
    assert.equal(tail.at(-1).Date, endDate);
    assert.equal(tail.at(-1)['Class #'], endLabel);
    for (const m of tail) {
      assert.equal(m.Term, null);
      assert.equal(m.Status, 'unassigned');
      assert.equal(m['Lesson ID'], '');
      assert.deepEqual(m.Overrides, {});
      const row = generated.find(r => w.key(r) === w.key(m));
      assert.equal(row['Class #'], m['Class #']);
      for (const f of w.contentFields) assert.equal(row[f], '-');
      assert.ok(!data.materials.some(r => r.Grade === grade && r.Section === section && r.Date === m.Date.replaceAll(' / ', '-')));
    }
  }
});

test('numbering correction preserves protected records, meeting metadata, materials and catalogs', () => {
  const source = w.readSource(), data = w.build(source);
  assert.equal(source.meetings.length, 594);
  assert.equal(data.materials.length, 522);
  // These fingerprints exclude only the 69 labels being corrected. They retain
  // dates, cycle Days, assignments, cancellations, content and every seminar row.
  assert.equal(hash(withoutCorrectedLabels(source.meetings)), '7b2279b40fe470d801f49bf151adb99dd65177a3579bcf0df6d09635d6fc3ae7');
  assert.equal(hash(source.meetings.filter(m => !affected(m))), '789abedb8bad78621e5fc483f4c2b5ffd5ddacc32649a2490c8379e5ff443154');
  assert.equal(hash(withoutCorrectedLabels(data.schedule)), '82a5ce53265b111173e1139b9055746fcef6df832024363f1e9f36a623e84ad3');
  assert.equal(hash(data.materials), '59cb6390bed0699e5e1f71de0b24c823701b6216346219c51bc1e8b89c48c896');
  assert.equal(hash(data.baseSchedule), '6e1eb5001334b6de962887c17e71c09d29e01f6546975baee272f2ac3342f016');
  assert.equal(hash(data.baseMaterials), '92f942803c282d17f9bd6a3e81fbd5f730e9ae8bf6501eddf443f3f8ebd3e44f');
});

test('calendar validation rejects resets, indiscriminate 7-1, and changed calendar coverage', () => {
  const meetings = w.readSource().meetings;
  for (const [grade, section] of sections) {
    const broken = structuredClone(meetings);
    const first = broken.find(m => affected(m) && m.Grade === grade && m.Section === section);
    first['Class #'] = first['Class #'] === '6-2' ? '1-2' : '2-1';
    assert.throws(() => validateCalendar(broken), /Class # must be/);
  }
  const skipped = structuredClone(meetings);
  skipped.find(m => affected(m) && m.Grade === 10 && m.Section === 'D')['Class #'] = '7-1';
  assert.throws(() => validateCalendar(skipped), /Class # must be 6-2/);
  const missing = structuredClone(meetings);
  missing.splice(missing.findIndex(m => m.Grade === 10 && m.Section === 'A' && m.Date === '2027 / 06 / 11'), 1);
  assert.throws(() => validateCalendar(missing), /meeting coverage differs/);
  const wrongDay = structuredClone(meetings);
  wrongDay.find(affected).Day = 6;
  assert.throws(() => validateCalendar(wrongDay), /Day must be/);
});
