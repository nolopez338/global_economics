"use strict";
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { parseCsv, stringifyCsv } = require('./csv');
const validateCalendar = require('./calendar-validation');
const materialValidation = require('../assets/js/materials-validation');
const fields = ['Grade', 'Section', 'Class #', 'Date', 'Term', 'Weekday', 'Day', 'Status', 'Reason', 'Canceled summary', 'Lesson ID', 'Overrides'];
const contentFields = ['Description', 'Material', 'Material teacher', 'Summary'];
const overrideFields = [...contentFields, 'Materials'];
const identityFields = ['Grade', 'Section', 'Class #', 'Date', 'Term', 'Weekday', 'Day'];
const clone = value => structuredClone(value);
const key = m => `${m.Grade}|${m.Section}|${m.Date}`;
const fail = message => { throw new Error(message); };
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
function readMeetings(text) {
  const [headers, ...rows] = parseCsv(text.replace(/^\uFEFF/, ''));
  if (!same(headers, fields)) fail(`schedule.csv: expected headers ${fields.join(',')}`);
  return rows.map((cells, i) => {
    if (cells.length !== fields.length) fail(`schedule.csv: row ${i + 2} has ${cells.length} fields`);
    const m = Object.fromEntries(fields.map((f, j) => [f, cells[j]]));
    for (const f of ['Grade', 'Term', 'Day']) m[f] = m[f] === '' ? null : Number(m[f]);
    try { m.Overrides = JSON.parse(m.Overrides || '{}'); } catch { fail(`Invalid Overrides at row ${i + 2}`); }
    return m;
  });
}
function writeMeetings(meetings) {
  return stringifyCsv([fields, ...meetings.map(m => fields.map(f => f === 'Overrides' ? JSON.stringify(m[f]) : m[f]))]);
}
function readSource(dir = __dirname) {
  return { meetings: readMeetings(fs.readFileSync(path.join(dir, 'schedule.csv'), 'utf8')), ...JSON.parse(fs.readFileSync(path.join(dir, 'lessons.json'), 'utf8')) };
}
function validateSource(source, { calendar = true } = {}) {
  const { meetings, lessons, catalog } = source;
  if (!Array.isArray(meetings) || !Array.isArray(lessons) || !Array.isArray(catalog)) fail('Expected meetings, lessons, and catalog arrays');
  const byId = new Map();
  for (const l of lessons) {
    if (typeof l.id !== 'string' || !l.id.trim() || byId.has(l.id)) fail(`Missing or duplicate lesson ID: ${l.id}`);
    if (!Number.isInteger(l.Grade) || ![1, 2, 3].includes(l.Term) || !['instruction', 'extra'].includes(l.kind)) fail(`Invalid lesson metadata: ${l.id}`);
    for (const f of contentFields) if (typeof l[f] !== 'string' || !l[f].trim()) fail(`Lesson ${l.id}: missing ${f}`);
    const result = materialValidation.validateMaterials(l.Materials);
    if (!result.valid) fail(`Lesson ${l.id}: ${result.errors.join('; ')}`);
    if (l.kind === 'extra' && (l.Description !== 'Extra Class')) fail(`Invalid Extra Class lesson ${l.id}`);
    byId.set(l.id, l);
  }
  const keys = new Set(), assignments = new Set();
  function resolve(id, grade, term) {
    const l = byId.get(id);
    if (!l) fail(`Missing or unknown lesson ID: ${id}`);
    if (l.Grade !== grade || l.Term !== term) fail(`Invalid assignment ${id}: grade/term mismatch`);
    return l;
  }
  for (const m of meetings) {
    if (keys.has(key(m))) fail(`Duplicate meeting identity: ${key(m)}`);
    keys.add(key(m));
    if (!['scheduled', 'canceled', 'unassigned'].includes(m.Status)) fail(`Invalid status at ${key(m)}`);
    if (!m.Overrides || typeof m.Overrides !== 'object' || Array.isArray(m.Overrides)) fail(`Invalid Overrides at ${key(m)}`);
    for (const f of Object.keys(m.Overrides)) if (!overrideFields.includes(f)) fail(`Unknown override ${f}`);
    if (typeof m.Reason !== 'string' || typeof m['Canceled summary'] !== 'string') fail(`Invalid cancellation metadata at ${key(m)}`);
    if (m.Status !== 'canceled' && (m.Reason || m['Canceled summary'])) fail(`Cancellation metadata on active meeting ${key(m)}`);
    if (m.Status === 'scheduled') {
      const l = resolve(m['Lesson ID'], m.Grade, m.Term);
      const assignmentKey = `${m.Grade}|${m.Section}|${m.Term}|${l.id}`;
      if (assignments.has(assignmentKey)) fail(`Duplicate lesson assignment: ${assignmentKey}`);
      assignments.add(assignmentKey);
      const effective = { ...l, ...m.Overrides };
      for (const f of contentFields) if (typeof effective[f] !== 'string' || !effective[f].trim()) fail(`Invalid ${f} override at ${key(m)}`);
      const result = materialValidation.validateMaterials(effective.Materials);
      if (!result.valid) fail(`Invalid material override at ${key(m)}: ${result.errors.join('; ')}`);
      if (l.kind === 'extra' && Object.keys(m.Overrides).length) fail(`Extra Class cannot have overrides at ${key(m)}`);
    } else {
      if (m['Lesson ID'] || Object.keys(m.Overrides).length) fail(`Canceled/unassigned meeting has an assignment: ${key(m)}`);
      if ((m.Status === 'unassigned') !== (m.Term === null)) fail(`Invalid unassigned meeting: ${key(m)}`);
    }
  }
  const catalogKeys = new Set();
  for (const c of catalog) {
    resolve(c.lessonId, c.Grade, c.Term);
    const k = `${c.Grade}|${c.Term}|${c['Class #']}`;
    if (!/^\d+$/.test(c['Class #']) || catalogKeys.has(k)) fail(`Invalid/duplicate catalog slot: ${k}`);
    catalogKeys.add(k);
  }
  if (calendar) validateCalendar(meetings);
  return byId;
}
function build(source, options) {
  const byId = validateSource(source, options);
  const schedule = [], materials = [];
  for (const m of source.meetings) {
    const content = m.Status === 'scheduled' ? { ...byId.get(m['Lesson ID']), ...m.Overrides } : {
      Description: m.Status === 'canceled' ? `No Class${m.Reason}` : '-',
      Summary: m.Status === 'canceled' ? m['Canceled summary'] || 'No Class' : '-',
      Material: '-', 'Material teacher': '-', Materials: []
    };
    schedule.push(Object.fromEntries([...identityFields.map(f => [f, m[f]]), ...contentFields.map(f => [f, content[f]])]));
    if (m.Term !== null) materials.push({ Grade: m.Grade, Term: m.Term, Section: m.Section.toUpperCase(), 'Class #': m['Class #'], Date: m.Date.replaceAll(' / ', '-'), Materials: clone(content.Materials) });
  }
  const baseSchedule = source.catalog.map(c => ({ Grade: c.Grade, 'Class #': c['Class #'], Term: c.Term, ...Object.fromEntries(contentFields.map(f => [f, byId.get(c.lessonId)[f]])) }));
  const baseMaterials = source.catalog.map(c => ({ Grade: c.Grade, Term: c.Term, 'Class #': c['Class #'], Materials: clone(byId.get(c.lessonId).Materials) }));
  for (const [data, kind] of [[materials, 'dated'], [baseMaterials, 'base']]) {
    const report = materialValidation.audit(data, kind);
    if (!report.valid) fail(`Invalid ${kind} materials output: ${JSON.stringify(report)}`);
  }
  return { schedule, materials, baseSchedule, baseMaterials };
}
const outputNames = [
  ['schedule', 'schedule-data.js', 'SCHEDULE_DATA'],
  ['materials', 'materials-data.js', 'MATERIALS_DATA'],
  ['baseSchedule', 'schedule-data-base.js', 'SCHEDULE_DATA'],
  ['baseMaterials', 'materials-data-base.js', 'MATERIALS_DATA_BASE']
];
function artifacts(source, options) {
  const data = build(source, options);
  return outputNames.map(([name, file, global]) => [file, `// AUTO-GENERATED from teacher/authoring/schedule.csv and lessons.json.\n// Run: node teacher/authoring/generate-schedule-data.js\n// Do not edit manually.\nwindow.${global} = ${JSON.stringify(data[name], null, 2)};\n`]);
}
// Stage every file before replacement. Roll back earlier replacements on an I/O error.
function replaceFiles(entries) {
  const originals = entries.map(([file]) => fs.existsSync(file) ? fs.readFileSync(file) : null);
  const staged = entries.map(([file]) => `${file}.tmp-${process.pid}`);
  let replaced = 0;
  try {
    entries.forEach(([, text], i) => fs.writeFileSync(staged[i], text));
    entries.forEach(([file], i) => { fs.renameSync(staged[i], file); replaced++; });
  } catch (error) {
    for (let i = 0; i < replaced; i++) {
      if (originals[i] === null) fs.unlinkSync(entries[i][0]);
      else fs.writeFileSync(entries[i][0], originals[i]);
    }
    throw error;
  } finally {
    for (const file of staged) if (fs.existsSync(file)) fs.unlinkSync(file);
  }
}
function generate(source = readSource(), { check = false, dir = path.join(__dirname, '../assets/js/databases'), sourcePath } = {}) {
  const entries = artifacts(source).map(([file, text]) => [path.join(dir, file), text]);
  if (check) {
    for (const [file, text] of entries) if (fs.readFileSync(file, 'utf8').replaceAll('\r\n', '\n') !== text) fail(`Stale generated file: ${file}`);
  } else {
    if (sourcePath) entries.unshift([sourcePath, writeMeetings(source.meetings)]);
    replaceFiles(entries);
  }
  return entries.length;
}
function readGlobal(file, global) {
  const context = { window: {} };
  vm.runInNewContext(fs.readFileSync(file, 'utf8'), context, { filename: file });
  return JSON.parse(JSON.stringify(context.window[global]));
}
module.exports = { fields, contentFields, identityFields, readMeetings, writeMeetings, readSource, validateSource, build, artifacts, generate, replaceFiles, readGlobal, key };
