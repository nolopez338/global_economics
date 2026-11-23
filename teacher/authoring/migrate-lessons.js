#!/usr/bin/env node
"use strict";
// One-time import of the reviewed legacy CSV and catalogs. Never used by generation.
const fs = require('node:fs');
const path = require('node:path');
const { randomUUID, createHash } = require('node:crypto');
const { parseCsv } = require('./csv');
const w = require('./lesson-workflow');
const hash = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');
// Consolidate repeated legacy variants by explicit catalog reference and complete overrides.
// This is storage normalization during import, never a runtime identity heuristic.
function consolidateVariants(source) {
  const groups = new Map();
  for (const m of source.meetings) {
    if (!m['Lesson ID'] || !Object.keys(m.Overrides).length) continue;
    const signature = JSON.stringify([m['Lesson ID'], m.Overrides]);
    if (!groups.has(signature)) groups.set(signature, []);
    groups.get(signature).push(m);
  }
  for (const meetings of groups.values()) {
    if (meetings.length < 2) continue;
    const first = meetings[0];
    const original = source.lessons.find(l => l.id === first['Lesson ID']);
    const variant = { ...original, ...first.Overrides, id: randomUUID() };
    source.lessons.push(variant);
    for (const m of meetings) { m['Lesson ID'] = variant.id; m.Overrides = {}; }
  }
  return source;
}
function migrate(dir = __dirname, databases = path.join(dir, '../assets/js/databases')) {
  const csvPath = path.join(dir, 'schedule.csv');
  const text = fs.readFileSync(csvPath, 'utf8');
  if (text.split(/\r?\n/)[0].includes('Lesson ID')) {
    w.validateSource(w.readSource(dir));
    return 'Already migrated; no changes.';
  }
  if (fs.existsSync(path.join(dir, 'lessons.json'))) throw new Error('lessons.json exists beside a legacy CSV; refusing to overwrite');
  const [headers, ...rows] = parseCsv(text);
  const legacy = rows.map(values => {
    const r = Object.fromEntries(headers.map((f, i) => [f, values[i]]));
    for (const f of ['Grade', 'Term', 'Day']) r[f] = r[f] === '' ? null : Number(r[f]);
    return r;
  });
  const load = (file, global) => w.readGlobal(path.join(databases, file + '.js'), global);
  const original = { schedule: load('schedule-data', 'SCHEDULE_DATA'), materials: load('materials-data', 'MATERIALS_DATA'), baseSchedule: load('schedule-data-base', 'SCHEDULE_DATA'), baseMaterials: load('materials-data-base', 'MATERIALS_DATA_BASE') };
  if (hash(legacy) !== hash(original.schedule)) throw new Error('Legacy CSV/runtime differ: synchronize and review before migration');
  // Explicit reviewed exceptions: these cancellations were ALREADY shifted in both datasets.
  const cancellations = { '11|A|2': '2026 / 11 / 18', '11|B|2': '2026 / 11 / 23' };
  for (const [group, date] of Object.entries(cancellations)) {
    const rs = legacy.filter(r => `${r.Grade}|${r.Section}|${r.Term}` === group);
    const canceled = rs.find(r => r.Date === date);
    if (!canceled || !canceled.Description.startsWith('No Class')) throw new Error(`Review cancellation ${group} ${date} before migration`);
    const next = rs[rs.indexOf(canceled) + 1];
    const expected = group.includes('|A|') ? 'C2:' : 'C3:';
    if (!next.Description.startsWith(expected)) throw new Error(`Cancellation ${group} is not postponed correctly`);
    const cm = original.materials.find(r => r.Grade === canceled.Grade && r.Section === canceled.Section && r.Date === date.replaceAll(' / ', '-'));
    const nm = original.materials.find(r => r.Grade === next.Grade && r.Section === next.Section && r.Date === next.Date.replaceAll(' / ', '-'));
    if (!cm || cm.Materials.length || !nm || !nm.Materials[0]?.Acronym.startsWith(expected.slice(0, 2))) throw new Error(`Synchronize materials for ${group} before migration`);
  }
  const lessons = [], catalog = [], bySlot = new Map();
  for (const r of original.baseSchedule) {
    const slot = `${r.Grade}|${r.Term}|${r['Class #']}`;
    const material = original.baseMaterials.find(m => `${m.Grade}|${m.Term}|${m['Class #']}` === slot);
    if (!material) throw new Error(`Missing base material definition: ${slot}`);
    const lesson = { id: randomUUID(), Grade: r.Grade, Term: r.Term, kind: r.Description === 'Extra Class' ? 'extra' : 'instruction', ...Object.fromEntries(w.contentFields.map(f => [f, r[f]])), Materials: material.Materials };
    lessons.push(lesson); bySlot.set(slot, lesson);
    catalog.push({ Grade: r.Grade, Term: r.Term, 'Class #': r['Class #'], lessonId: lesson.id });
  }
  const ordinals = new Map(), removedCanceledMaterials = [], crosswalk = [];
  const meetings = legacy.map(r => {
    const group = `${r.Grade}|${r.Section}|${r.Term}`;
    const ordinal = (ordinals.get(group) || 0) + 1; ordinals.set(group, ordinal);
    const m = { ...Object.fromEntries(w.identityFields.map(f => [f, r[f]])), Status: r.Term === null ? 'unassigned' : r.Description.startsWith('No Class') ? 'canceled' : 'scheduled', Reason: '', 'Canceled summary': '', 'Lesson ID': '', Overrides: {} };
    const dated = original.materials.find(x => x.Grade === r.Grade && x.Section === r.Section.toUpperCase() && x.Date === r.Date.replaceAll(' / ', '-'));
    if (r.Term !== null && !dated) throw new Error(`Missing dated material reference ${w.key(m)}`);
    if (m.Status === 'canceled') {
      m.Reason = r.Description.slice('No Class'.length); m['Canceled summary'] = r.Summary;
      if (dated.Materials.length) removedCanceledMaterials.push({ meeting: w.key(m), Materials: dated.Materials });
    } else if (m.Status === 'scheduled') {
      // Import crosswalk only: existing legacy catalog slots, with the two reviewed offsets.
      // Materials ALWAYS join by dated identity; never copy a catalog list by ordinal.
      const offset = cancellations[group] && r.Date > cancellations[group] ? 1 : 0;
      const l = bySlot.get(`${r.Grade}|${r.Term}|${ordinal - offset}`);
      if (!l) throw new Error(`No reviewed legacy catalog slot for ${w.key(m)}`);
      m['Lesson ID'] = l.id;
      for (const f of [...w.contentFields, 'Materials']) {
        const value = f === 'Materials' ? dated.Materials : r[f];
        if (JSON.stringify(value) !== JSON.stringify(l[f])) m.Overrides[f] = value;
      }
      // Historical schedules may use a catalog Extra Class for different content.
      // Make that historical lesson explicit rather than allowing an Extra slot override.
      if (l.kind === 'extra' && Object.keys(m.Overrides).length) {
        const historical = { ...l, ...m.Overrides, id: randomUUID(), kind: 'instruction' };
        lessons.push(historical); m['Lesson ID'] = historical.id; m.Overrides = {};
      }
    }
    crosswalk.push({ meeting: w.key(m), lessonId: m['Lesson ID'] || null, status: m.Status });
    return m;
  });
  const source = consolidateVariants({ meetings, lessons, catalog });
  crosswalk.forEach((entry, i) => { entry.lessonId = meetings[i]['Lesson ID'] || null; });
  const generated = w.build(source);
  if (hash(generated.schedule) !== hash(original.schedule)) throw new Error('Migration changed schedule content');
  for (const name of ['baseSchedule', 'baseMaterials']) {
    if (hash(generated[name]) !== hash(original[name])) throw new Error(`Migration would change ${name}; review legacy data`);
  }
  const restoredMaterials = structuredClone(generated.materials);
  for (const removed of removedCanceledMaterials) {
    const [grade, section, date] = removed.meeting.split('|');
    restoredMaterials.find(m => m.Grade === +grade && m.Section === section.toUpperCase() && m.Date === date.replaceAll(' / ', '-')).Materials = removed.Materials;
  }
  if (hash(restoredMaterials) !== hash(original.materials)) throw new Error('Migration would change unrelated dated materials; review legacy data');
  const report = {
    note: 'Reviewed baseline: both Grade 11 Term 2 cancellations already synchronized; no second postponement. Older No Class material lists cleared without shifting historical assignments. Crosswalk is frozen; runtime never derives identity from text or ordinal.',
    originalHashes: Object.fromEntries(Object.entries(original).map(([k, v]) => [k, hash(v)])),
    baselineHashes: Object.fromEntries(Object.entries(generated).map(([k, v]) => [k, hash(v)])),
    counts: { meetings: meetings.length, datedMaterials: generated.materials.length, catalog: catalog.length, removedCanceledLists: removedCanceledMaterials.length },
    removedCanceledMaterials, crosswalk
  };
  const entries = [
    [csvPath, w.writeMeetings(meetings)],
    [path.join(dir, 'lessons.json'), JSON.stringify({ lessons, catalog }, null, 2) + '\n'],
    [path.join(dir, 'migration-baseline.json'), JSON.stringify(report, null, 2) + '\n'],
    ...w.artifacts(source).map(([file, content]) => [path.join(databases, file), content])
  ];
  w.replaceFiles(entries);
  return `Migrated ${meetings.length} meetings; cleared ${removedCanceledMaterials.length} canceled lists.`;
}
if (require.main === module) {
  try { console.log(migrate()); } catch (error) { console.error(error.message); process.exitCode = 1; }
}
module.exports = { migrate, consolidateVariants };
