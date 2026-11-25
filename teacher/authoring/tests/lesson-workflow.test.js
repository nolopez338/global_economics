"use strict";
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');
const w = require('../lesson-workflow');
const { cancel, move, findMeeting } = require('../reschedule');
const options = { calendar: false };
const hash = value => crypto.createHash('sha256').update(JSON.stringify(value)).digest('hex');
// Frozen migration hashes predate the post-May-11 numbering correction. Restore
// only those displayed labels for audit comparisons; validate live data normally.
function migrationSnapshot(data) {
  const snapshot = structuredClone(data);
  const calendar = require('../../assets/js/databases/year-calendar-data');
  for (const row of snapshot.schedule) {
    if (row.Section !== 'Seminar' && row.Date > '2027 / 05 / 11') {
      const info = calendar.getAcademicDateInfo(row.Date.replaceAll(' / ', '-'));
      row['Class #'] = `${calendar.getTermCycleNumber(info.calendarYear, info.month, info.day)}-${row['Class #'].split('-')[1]}`;
    }
  }
  return snapshot;
}
function fixture() {
  const material = { Acronym: 'C1', Name: 'Criterion 1', Hyperlink: 'https://example.com/practice.pdf', Category: 'practice-activities' };
  const lesson = (id, Materials = [material], kind = 'instruction') => ({ id, Grade: 11, Term: 2, kind, Description: kind === 'extra' ? 'Extra Class' : id, Summary: kind === 'extra' ? 'Extra Class' : `${id} summary`, Material: '-', 'Material teacher': '-', Materials });
  const lessons = [lesson('intro'), lesson('assessment', []), lesson('practice'), lesson('extra-1', [], 'extra'), lesson('extra-2', [], 'extra')];
  const meetings = lessons.map((l, i) => ({ Grade: 11, Section: 'A', Term: 2, Date: `2026 / 11 / ${String(10 + i).padStart(2, '0')}`, 'Class #': `${i + 1}-1`, Weekday: 'Monday', Day: 1, Status: 'scheduled', Reason: '', 'Canceled summary': '', 'Lesson ID': l.id, Overrides: {} }));
  meetings[0].Overrides = { Summary: 'Section A introduction', Materials: [{ ...material, Name: 'Section A handout' }] };
  return { meetings, lessons, catalog: lessons.map((l, i) => ({ Grade: 11, Term: 2, 'Class #': String(i + 1), lessonId: l.id })) };
}
const ids = source => source.meetings.filter(m => m.Status === 'scheduled').map(m => m['Lesson ID']);

// Reconstruct only the corrected dates for tests of the frozen migration audit.
function migrationSource({ seminar = true } = {}) {
  const source = w.readSource();
  // Reconstruct the frozen migration snapshot, before the dedicated seminar catalog.
  if (seminar) source.catalog = source.catalog.filter(c => c.Grade !== '10S');
  const crosswalk = require('../migration-baseline.json').crosswalk;
  for (const m of source.meetings.filter(m => seminar && m.Grade === 10 && m.Section === 'Seminar' && m.Term === 2)) {
    m['Lesson ID'] = crosswalk.find(c => c.meeting === w.key(m)).lessonId;
    m.Overrides = { Description: '-', Summary: '-' };
  }
  const from = findMeeting(source, 11, 'B', '2026-11-19');
  const to = findMeeting(source, 11, 'B', '2026-11-23');
  Object.assign(from, { Status: 'scheduled', Reason: '', 'Canceled summary': '', 'Lesson ID': to['Lesson ID'], Overrides: structuredClone(to.Overrides) });
  Object.assign(to, { Status: 'canceled', Reason: '', 'Canceled summary': 'No Class', 'Lesson ID': '', Overrides: {} });
  return source;
}
test('cancellation cascades complete assignments, keeps empty assessments, consumes one trailing Extra', () => {
  const source = fixture(), before = structuredClone(source);
  const result = cancel(source, w.key(source.meetings[0]), 'School event', options);
  assert.deepEqual(source, before);
  assert.deepEqual(ids(result), ['intro', 'assessment', 'practice', 'extra-2']);
  source.meetings.forEach((m, i) => w.identityFields.forEach(f => assert.equal(result.meetings[i][f], m[f])));
  const generated = w.build(result, options);
  assert.equal(generated.schedule[0].Description, 'No Class - School event');
  assert.deepEqual(generated.materials[0].Materials, []);
  assert.equal(generated.schedule[1].Summary, 'Section A introduction');
  assert.equal(generated.materials[1].Materials[0].Name, 'Section A handout');
  assert.equal(generated.schedule[2].Description, 'assessment');
  assert.deepEqual(generated.materials[2].Materials, []);
  assert.deepEqual(cancel(result, w.key(result.meetings[0]), 'Different reason', options), result);
});
test('cancellation skips previously canceled meetings and isolates section and term', () => {
  const source = fixture();
  const otherSection = source.meetings.map(m => ({ ...structuredClone(m), Section: 'B' }));
  const otherTerm = source.meetings.map(m => ({ ...structuredClone(m), Term: 3, Date: m.Date.replace('2026 / 11', '2027 / 04'), 'Lesson ID': `t3-${m['Lesson ID']}` }));
  source.lessons.push(...source.lessons.map(l => ({ ...structuredClone(l), id: `t3-${l.id}`, Term: 3 })));
  source.meetings.push(...otherSection, ...otherTerm);
  let result = cancel(source, w.key(source.meetings[1]), '', options);
  result = cancel(result, w.key(source.meetings[0]), '', options);
  assert.equal(result.meetings[2]['Lesson ID'], 'intro');
  assert.equal(result.meetings[3]['Lesson ID'], 'assessment');
  assert.equal(result.meetings[4]['Lesson ID'], 'practice');
  assert.deepEqual(result.meetings.slice(5), source.meetings.slice(5));
  const before = structuredClone(result);
  assert.throws(() => cancel(result, w.key(result.meetings[2]), '', options), /Insufficient capacity/);
  assert.deepEqual(result, before);
});
test('canceling an Extra slot consumes only that slot', () => {
  const source = fixture();
  const result = cancel(source, w.key(source.meetings[3]), '', options);
  assert.deepEqual(ids(result), ['intro', 'assessment', 'practice', 'extra-2']);
});
test('move reorders occupied meetings together with overrides, in either direction', () => {
  const source = fixture();
  const result = move(source, w.key(source.meetings[0]), w.key(source.meetings[2]), options);
  assert.deepEqual(ids(result), ['assessment', 'practice', 'intro', 'extra-1', 'extra-2']);
  assert.deepEqual(result.meetings[2].Overrides, source.meetings[0].Overrides);
  assert.equal(w.build(result, options).materials[2].Materials[0].Name, 'Section A handout');
  assert.deepEqual(move(result, w.key(result.meetings[2]), w.key(result.meetings[0]), options), source);
  const isolated = fixture(); isolated.meetings[1].Section = 'B';
  assert.throws(() => move(isolated, w.key(isolated.meetings[0]), w.key(isolated.meetings[1]), options), /same section and term/);
});
test('reject invalid references, assignments, duplicates, material overrides, statuses and calendar fields', () => {
  const mutations = [
    s => { s.meetings[0]['Lesson ID'] = ''; },
    s => { s.meetings[0]['Lesson ID'] = 'unknown'; },
    s => { s.meetings[0]['Lesson ID'] = s.meetings[1]['Lesson ID']; },
    s => { s.meetings.push(structuredClone(s.meetings[0])); },
    s => { s.meetings[0].Term = 3; },
    s => { s.meetings[0].Overrides.Materials = null; },
    s => { s.meetings[0].Overrides.Term = 3; },
    s => { s.meetings[0].Status = 'canceled'; },
    s => { delete s.lessons[0].Materials; },
    s => { s.lessons[1].id = s.lessons[0].id; },
    s => { s.catalog.push(structuredClone(s.catalog[0])); }
  ];
  for (const mutate of mutations) { const source = fixture(); mutate(source); assert.throws(() => w.build(source, options)); }
  const source = w.readSource(); source.meetings[0].Day = 6;
  assert.throws(() => w.build(source), /Day must|meeting day/);
});
test('migration preserves all schedule content, base catalogs, and unrelated dated associations', () => {
  const source = migrationSource(), actual = migrationSnapshot(w.build(source)), baseline = require('../migration-baseline.json');
  assert.equal(actual.schedule.length, 594); assert.equal(actual.materials.length, 522);
  for (const [name, data] of Object.entries(actual)) assert.equal(hash(data), baseline.baselineHashes[name], name);
  for (const name of ['schedule', 'baseSchedule', 'baseMaterials']) assert.equal(hash(actual[name]), baseline.originalHashes[name]);
  const restored = structuredClone(actual.materials);
  for (const item of baseline.removedCanceledMaterials) {
    const [grade, section, date] = item.meeting.split('|');
    const row = restored.find(m => m.Grade === +grade && m.Section === section.toUpperCase() && m.Date === date.replaceAll(' / ', '-'));
    assert.deepEqual(row.Materials, []); row.Materials = item.Materials;
  }
  assert.equal(hash(restored), baseline.originalHashes.materials);
  for (const m of source.meetings.filter(m => m.Status === 'canceled')) assert.deepEqual(actual.materials.find(r => r.Grade === m.Grade && r.Section === m.Section.toUpperCase() && r.Date === m.Date.replaceAll(' / ', '-')).Materials, []);
});
test('corrected Grade 11 cancellations are idempotent and retain every assessment', () => {
  const source = w.readSource();
  for (const [section, date, expected] of [['A', '2026-11-18', 'C2:'], ['B', '2026-11-19', 'C2:']]) {
    const meeting = findMeeting(source, 11, section, date);
    assert.equal(meeting.Status, 'canceled'); assert.equal(meeting['Lesson ID'], '');
    assert.deepEqual(cancel(source, w.key(meeting)), source);
    const rows = w.build(source).schedule.filter(r => r.Grade === 11 && r.Section === section && r.Term === 2);
    assert.ok(rows[rows.findIndex(r => r.Date === meeting.Date) + 1].Description.startsWith(expected));
    assert.equal(rows.filter(r => r.Description.includes('Learning Evidence')).length, 5);
    assert.equal(rows.filter(r => r.Description === 'Extra Class').length, 2);
  }
});

test('Grade 11B transfers only the November 19 assignment to November 23', () => {
  const source = w.readSource(), before = migrationSource({ seminar: false });
  const from = findMeeting(source, 11, 'B', '2026-11-19');
  const to = findMeeting(source, 11, 'B', '2026-11-23');
  const original = findMeeting(before, 11, 'B', '2026-11-19');
  assert.equal(from.Status, 'canceled');
  assert.equal(from.Reason, ': Godchildren meeting');
  assert.equal(from['Canceled summary'], '');
  assert.equal(from['Lesson ID'], '');
  assert.deepEqual(from.Overrides, {});
  assert.equal(to.Status, 'scheduled');
  assert.equal(to.Reason, ''); assert.equal(to['Canceled summary'], '');
  assert.equal(to['Lesson ID'], '055bbd52-a251-4622-8f76-6adc7d87fb6e');
  assert.equal(to['Lesson ID'], original['Lesson ID']);
  assert.deepEqual(to.Overrides, original.Overrides);
  const data = w.build(source), oldData = w.build(before);
  const affected = row => row.Grade === 11 && row.Section === 'B' && ['2026 / 11 / 19', '2026 / 11 / 23', '2026-11-19', '2026-11-23'].includes(row.Date);
  for (const name of Object.keys(data)) {
    assert.deepEqual(data[name].filter(r => !affected(r)), oldData[name].filter(r => !affected(r)), name);
  }
  source.meetings.forEach((m, i) => w.identityFields.forEach(f => assert.equal(m[f], before.meetings[i][f])));
  assert.deepEqual(source.meetings.filter(m => !affected(m)), before.meetings.filter(m => !affected(m)));
  const schedule = data.schedule.filter(affected), materials = data.materials.filter(affected);
  assert.equal(schedule[0].Description, 'No Class: Godchildren meeting');
  assert.equal(schedule[1].Description, 'C2: Interpret estimates and long-run confidence coverage');
  w.contentFields.forEach(f => assert.equal(schedule[1][f], oldData.schedule.find(r => r.Grade === 11 && r.Section === 'B' && r.Date === original.Date)[f]));
  assert.deepEqual(materials[0].Materials, []);
  assert.deepEqual(materials[1].Materials, oldData.materials.find(r => r.Grade === 11 && r.Section === 'B' && r.Date === '2026-11-19').Materials);
});
test('CSV round trip, deterministic generation, stale-output detection, failure before writes, migration rerun', () => {
  const source = w.readSource(); assert.deepEqual(w.readMeetings(w.writeMeetings(source.meetings)), source.meetings);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'teacher-lessons-'));
  try {
    w.generate(source, { dir });
    const before = w.artifacts(source).map(([file]) => fs.readFileSync(path.join(dir, file)));
    w.generate(source, { dir });
    w.artifacts(source).forEach(([file], i) => assert.deepEqual(fs.readFileSync(path.join(dir, file)), before[i]));
    w.generate(source, { dir, check: true });
    const invalid = structuredClone(source); invalid.meetings[1]['Lesson ID'] = 'bad';
    assert.throws(() => w.generate(invalid, { dir }), /lesson ID/);
    w.artifacts(source).forEach(([file], i) => assert.deepEqual(fs.readFileSync(path.join(dir, file)), before[i]));
    fs.appendFileSync(path.join(dir, 'materials-data.js'), '// stale');
    assert.throws(() => w.generate(source, { dir, check: true }), /Stale generated/);
    const result = spawnSync(process.execPath, [path.join(__dirname, '../migrate-lessons.js')], { encoding: 'utf8' });
    assert.equal(result.status, 0, result.stderr); assert.match(result.stdout, /Already migrated/);
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});
test('frontend schedule links find the exact generated material record after postponement', () => {
  const vm = require('node:vm');
  const source = w.readSource(), m = source.meetings.find(m => m.Grade === 11 && m.Section === 'C' && m.Term === 2 && m.Status === 'scheduled');
  const result = cancel(source, w.key(m));
  const data = w.build(result);
  const context = { window: { MATERIALS_DATA: data.materials }, document: { addEventListener() {} } };
  let code = fs.readFileSync(path.join(__dirname, '../../assets/js/schedule-renderer.js'), 'utf8');
  // The renderer has no top-level DOM effects; exercise its real lookup used for links.
  vm.runInNewContext(code + '\nthis.lookup = findMaterialsRecord;', context);
  for (const entry of data.schedule.filter(r => r.Term)) {
    const record = context.lookup(entry, entry.Date.replaceAll(' / ', '-'));
    assert.ok(record, w.key(entry)); assert.equal(record['Class #'], entry['Class #']);
  }
});
test('one-time migration imports the legacy snapshot without changing unrelated data', () => {
  const source = migrationSource(), data = w.build(source), baseline = require('../migration-baseline.json');
  for (const removed of baseline.removedCanceledMaterials) {
    const [grade, section, date] = removed.meeting.split('|');
    data.materials.find(m => m.Grade === +grade && m.Section === section.toUpperCase() && m.Date === date.replaceAll(' / ', '-')).Materials = removed.Materials;
  }
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'teacher-migration-'));
  try {
    const headers = [...w.identityFields, ...w.contentFields];
    const csv = require('../csv').stringifyCsv([headers, ...data.schedule.map(r => headers.map(f => r[f]))]);
    fs.writeFileSync(path.join(dir, 'schedule.csv'), csv);
    for (const [name, file, global] of [['schedule', 'schedule-data', 'SCHEDULE_DATA'], ['materials', 'materials-data', 'MATERIALS_DATA'], ['baseSchedule', 'schedule-data-base', 'SCHEDULE_DATA'], ['baseMaterials', 'materials-data-base', 'MATERIALS_DATA_BASE']]) {
      fs.writeFileSync(path.join(dir, file + '.js'), `window.${global} = ${JSON.stringify(data[name])};\n`);
    }
    const { migrate } = require('../migrate-lessons');
    // Unmatched legacy records must be reviewed, never silently discarded.
    const legacyFile = path.join(dir, 'materials-data.js');
    const originalText = fs.readFileSync(legacyFile, 'utf8');
    fs.writeFileSync(legacyFile, `window.MATERIALS_DATA = ${JSON.stringify([...data.materials, { ...data.materials[0], Date: '2028-01-01' }])};`);
    assert.throws(() => migrate(dir, dir), /unrelated dated materials/);
    assert.equal(fs.readFileSync(path.join(dir, 'schedule.csv'), 'utf8'), csv);
    assert.equal(fs.existsSync(path.join(dir, 'lessons.json')), false);
    fs.writeFileSync(legacyFile, originalText);
    assert.match(migrate(dir, dir), /Migrated 594/);
    const imported = migrationSnapshot(w.build(w.readSource(dir)));
    for (const [name, rows] of Object.entries(imported)) assert.equal(hash(rows), baseline.baselineHashes[name], name);
    assert.deepEqual(w.readSource(dir).meetings.map(m => [m.Status, Object.keys(m.Overrides)]), source.meetings.map(m => [m.Status, Object.keys(m.Overrides)]));
    assert.match(migrate(dir, dir), /Already migrated/);
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});
