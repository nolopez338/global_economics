"use strict";
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { createHash } = require('node:crypto');
const w = require('../lesson-workflow');
const v = require('../../assets/js/materials-validation');
const source = w.readSource(), data = w.build(source);
const root = path.resolve(__dirname, '../../..');
const affected = r => r.Grade === 10 && String(r.Section).toUpperCase() === 'SEMINAR' && r.Term === 2;
const hash = x => createHash('sha256').update(JSON.stringify(x)).digest('hex');
const descriptions = [
  'Inter group presentation', 'In group presentation', 'C1 and C2 guide', 'C3 and C4 guide',
  'Presentación de prototipo (C4) — First learning evidence', 'C5 and C6 guide',
  'Prototipo final (C5 y C6)', 'C7 and C8 guide', 'C9 and C10 guide',
  'Informe final (todo acumulado) — Second learning evidence'
];
const targets = [
  ['first_class.html', 'checklist_evaluativo_feria.pdf', 'seminars_summary.pdf', 'seminars_summary_table.pdf'],
  ['checklist_evaluativo_feria2.pdf'], ['C1C2-Activity.pdf'], ['C3C4-Activity.pdf'],
  ['C3C4-Activity.pdf', 'G10_T2.html#first-learning-evidence'], ['C5C6-Activity.pdf'],
  ['C5C6-Activity.pdf'], ['C7C8-Activity.pdf'], ['C9C10-Activity.pdf'],
  ['G10_T2.html#introduction', 'G10_T2.html#second-learning-evidence', 'C5C6-Activity.pdf', 'C7C8-Activity.pdf', 'C9C10-Activity.pdf']
];

test('seminar Term 2 has ten dedicated lessons and matching dated/base descriptions and resources', () => {
  const dated = data.schedule.filter(affected).sort((a,b) => a.Date.localeCompare(b.Date));
  const base = data.baseSchedule.filter(r => r.Grade === '10S' && r.Term === 2);
  assert.deepEqual(dated.map(r => r.Description), descriptions);
  assert.deepEqual(base.map(r => r.Description), descriptions);
  dated.forEach((row, i) => {
    assert.equal(row.Summary, base[i].Summary);
    const material = data.materials.find(r => affected(r) && r.Date === row.Date.replaceAll(' / ', '-'));
    const baseMaterial = data.baseMaterials.find(r => r.Grade === '10S' && r.Term === 2 && r['Class #'] === String(i+1));
    assert.deepEqual(material.Materials, baseMaterial.Materials);
    assert.deepEqual(material.Materials.map(m => m.Hyperlink.split('/').pop()), targets[i]);
    const meeting = source.meetings.find(m => w.key(m) === w.key(row));
    assert.equal(source.meetings.filter(m => m['Lesson ID'] === meeting['Lesson ID']).length, 1);
  });
});

test('seminar base catalog has sequential 9/10/9 slots, preserved history, and no invented dated assignments', () => {
  for (const term of [1,2,3]) {
    const rows = data.baseSchedule.filter(r => r.Grade === '10S' && r.Term === term);
    assert.equal(rows.length, term === 2 ? 10 : 9);
    assert.deepEqual(rows.map(r => r['Class #']), rows.map((_,i) => String(i+1)));
    for (const row of rows) {
      const materials = data.baseMaterials.filter(m => m.Grade === row.Grade && m.Term === term && m['Class #'] === row['Class #']);
      assert.equal(materials.length, 1);
      if (term === 2) continue;
      const dated = data.schedule.find(r => r.Grade === 10 && r.Section === 'Seminar' && r.Term === term && r['Class #'] === row['Class #']+'-1');
      if (dated) {
        w.contentFields.forEach(f => assert.equal(row[f], dated[f]));
        assert.deepEqual(materials[0].Materials, data.materials.find(m => m.Grade === 10 && m.Section === 'SEMINAR' && m.Date === dated.Date.replaceAll(' / ', '-')).Materials);
      } else {
        w.contentFields.forEach(f => assert.equal(row[f], '-'));
        assert.deepEqual(materials[0].Materials, []);
      }
    }
  }
  const hashes = {
    // Includes the intentional regular-section continuation after May 11.
    schedule: 'aa6ba79702f89f21bf75a11393f3d351973df2f85051af3dd357827e7ea86d9a',
    materials: '85fac7c0e55f4301a3908d79d5ef90912d2e2c7ee4445f7d3affcba7e288ccfa',
    baseSchedule: '748590861628dac7102900311771a60ac0dfa5e501bc2be419c202afd269bfd2',
    baseMaterials: '2c87bc100caeeb70532116ae37d50f593fe492ebba65f6b544acbcf2293aa995'
  };
  for (const [name, expected] of Object.entries(hashes)) assert.equal(hash(data[name].filter(r => !affected(r) && r.Grade !== '10S')), expected, name);
  assert.equal(hash(data.schedule.map(r => Object.fromEntries(w.identityFields.map(f => [f,r[f]])))), 'b5b7fd023a64e7bc6f87b1695b4cf6d812f4f17e7cd890a58691536492a3a0a8');
});

test('seminar Term 2 material URLs resolve to source links, repository files and valid anchors', () => {
  const html = fs.readFileSync(path.join(root, 'seminars/src/G10_T2.html'), 'utf8');
  const sourceUrl = 'https://nolopez338.github.io/global_economics/seminars/src/G10_T2.html';
  const links = [...html.matchAll(/<a\b[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g)].map(m => ({ url: new URL(m[1], sourceUrl).href, name: m[2].replace(/<[^>]+>/g,'').trim() }));
  for (const m of data.materials.filter(affected).flatMap(r => r.Materials)) {
    const url = new URL(m.Hyperlink);
    assert.equal(url.origin, 'https://nolopez338.github.io');
    assert.ok(url.pathname.startsWith('/global_economics/'));
    const file = path.join(root, decodeURIComponent(url.pathname.slice('/global_economics/'.length)));
    assert.ok(fs.existsSync(file), file);
    if (url.hash) {
      assert.equal(url.origin + url.pathname, sourceUrl);
      assert.ok(html.includes('id="'+url.hash.slice(1)+'"'));
    } else assert.ok(links.some(l => l.url === m.Hyperlink && l.name === m.Name), m.Name);
  }
});

test('10S is accepted only as a base grade; dated seminar requests stay numeric and section-specific', () => {
  const base = data.baseMaterials.find(r => r.Grade === '10S');
  assert.ok(v.validateRecord(base, 'base').valid);
  assert.equal(v.validateRecord({ ...data.materials.find(affected), Grade: '10S' }, 'dated').valid, false);
  assert.deepEqual(v.normalizeRequest('?grade=10&section=Seminar&date=2026-11-12'), { mode: 'dated', grade: 10, section: 'SEMINAR', date: '2026-11-12' });
  const bad = structuredClone(source);
  bad.catalog.find(c => c.Grade === '10S').Grade = '11S';
  assert.throws(() => w.build(bad), /grade\/term mismatch/);
});
