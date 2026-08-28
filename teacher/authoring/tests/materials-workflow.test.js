"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { spawnSync } = require("node:child_process");
const v = require("../../assets/js/materials-validation.js");
const root = path.join(__dirname, "../..");
const files = ["assets/js/databases/materials-data.js", "assets/js/databases/materials-data-base.js"];
function material(overrides = {}) { return { Acronym: "TEST", Name: "Test material", Hyperlink: "https://example.com/a", Category: "extra-resources", ...overrides }; }
function dated(overrides = {}) { return { Grade: 10, Term: 1, Section: "B", "Class #": "1-2", Date: "2026-08-18", Materials: [material()], ...overrides }; }
function base(overrides = {}) { return { Grade: 10, Term: 1, "Class #": "2", Materials: [material()], ...overrides }; }
function load(name) { const context = { window: {} }; const file = path.join(root, `assets/js/databases/${name}.js`); vm.runInNewContext(fs.readFileSync(file, "utf8"), context); return context.window; }
class Element {
  constructor(tag) { this.tagName = tag.toUpperCase(); this.children = []; this.attributes = {}; this.textContent = ""; this.className = ""; }
  append(...children) { this.children.push(...children); }
  appendChild(child) { this.children.push(child); return child; }
  replaceChildren(...children) { this.children = children; }
  setAttribute(name, value) { this.attributes[name] = value; }
}
function render(search, globals = {}) {
  const content = new Element("div"), heading = new Element("h1");
  const document = { title: "", getElementById: id => id === "materials-content" ? content : null, querySelector: selector => selector === "#materials-page > h1" ? heading : null, createElement: tag => new Element(tag) };
  const warnings = [], errors = [];
  const window = { location: { search }, MaterialsValidation: v, ...globals };
  vm.runInNewContext(fs.readFileSync(path.join(root, "assets/js/materials-page.js"), "utf8"), { window, document, console: { warn: (...args) => warnings.push(args), error: (...args) => errors.push(args) }, URLSearchParams, Map, Set });
  return { content, heading, document, warnings, errors };
}

test("expected dated meeting contains Term and all three accessible card values", () => {
  const data = load("materials-data").MATERIALS_DATA;
  const matches = data.filter(r => v.recordKey(r, "dated") === "10|B|2026-08-18");
  assert.equal(matches.length, 1); assert.equal(matches[0].Term, 1); assert.equal(matches[0]["Class #"], "1-2");
  assert.deepEqual(Array.from(matches[0].Materials, m => m.Acronym), ["C2S", "CA", "PA"]);
  matches[0].Materials.forEach(m => { assert.ok(m.Name); assert.ok(v.validUrl(m.Hyperlink)); });
});

test("dated page renders heading, class, safe cards, links, and accessible labels", () => {
  const data = load("materials-data").MATERIALS_DATA;
  const page = render("?grade=10&section=B&date=2026-08-18", { MATERIALS_DATA: data });
  assert.equal(page.heading.textContent, "Materials — Grade 10B — 2026-08-18");
  assert.equal(page.content.children[0].textContent, "Class 1-2");
  const cards = page.content.children[1].children; assert.equal(cards.length, 3);
  assert.deepEqual(cards.map(card => card.children[0].textContent), ["C2S", "CA", "PA"]);
  cards.forEach(card => { assert.equal(card.target, "_blank"); assert.equal(card.rel, "noopener noreferrer"); assert.match(card.href, /^https:/); assert.match(card.attributes["aria-label"], /^Open .* \(.+\) for Grade 10B/); assert.ok(card.className.includes(`material-card--${matchesCategory(card.children[2].textContent)}`)); });
});

test("Grade 10E example renders criteria name and unchanged category badge", () => {
  const data = load("materials-data").MATERIALS_DATA;
  const page = render("?grade=10&section=E&date=2026-08-27", { MATERIALS_DATA: data });
  const card = page.content.children[1].children.find(item => item.href.endsWith("G10_T1_C1C3_practice_activity2_print1_solved.pdf"));
  assert.ok(card);
  assert.equal(card.children[1].className, "class-label");
  assert.equal(card.children[1].textContent, "C1 & C3");
  assert.equal(card.children[2].className, "material-category");
  assert.equal(card.children[2].textContent, "Classroom activities");
});

function matchesCategory(label) { return v.CATEGORIES.find(category => category.label === label).value; }

test("canonical categories validate and invalid categories do not", () => {
  assert.deepEqual(Array.from(v.CATEGORY_VALUES), ["slides", "classroom-activities", "practice-activities", "extra-resources"]);
  v.CATEGORY_VALUES.forEach(Category => assert.equal(v.validateMaterials([material({ Category })]).valid, true));
  for (const Category of [undefined, "Slides", "slide", "unknown", 1]) {
    const candidate = material({ Category });
    if (Category === undefined) delete candidate.Category;
    const result = v.validateMaterials([candidate]);
    assert.equal(result.valid, false);
    assert.ok(result.errors.some(error => error.includes("Category")));
  }
  const warned = v.validateMaterials([material({ Unrelated: true })]);
  assert.equal(warned.valid, true);
  assert.deepEqual(warned.warnings, ["Materials[0] has unknown property Unrelated"]);
});

test("redundant material names are normalized narrowly and rejected", () => {
  for (const candidate of [
    material({ Name: "Slides", Category: "slides" }),
    material({ Name: "  sLiDeS  ", Category: "slides" }),
    material({ Name: "Slides!!!", Category: "slides" }),
    material({ Name: "Slide", Category: "slides" }),
    material({ Name: " Classroom---  activities ", Category: "classroom-activities" }),
    material({ Name: "Classroom activity", Category: "classroom-activities" }),
    material({ Name: "Practice activity", Category: "practice-activities" }),
    material({ Name: "Class material", Category: "extra-resources" })
  ]) {
    const result = v.validateMaterials([candidate]);
    assert.equal(result.valid, false);
    assert.match(result.errors.join("; "), /Materials\[0\].*repeats category/);
  }
  for (const candidate of [
    material({ Name: "C1 & C3", Category: "classroom-activities" }),
    material({ Name: "Term 1 outline", Category: "extra-resources" }),
    material({ Name: "Introductory slide", Category: "slides" }),
    material({ Name: "Probability practice", Category: "practice-activities" })
  ]) assert.equal(v.validateMaterials([candidate]).valid, true);
});

test("both complete databases contain only canonical categories and pass audit", () => {
  for (const [file, kind, globalName] of [["materials-data", "dated", "MATERIALS_DATA"], ["materials-data-base", "base", "MATERIALS_DATA_BASE"]]) {
    const data = load(file)[globalName];
    assert.equal(v.audit(data, kind).valid, true);
    data.flatMap(record => record.Materials).forEach(item => {
      assert.ok(v.CATEGORY_VALUES.includes(item.Category));
      assert.equal(v.isRedundantName(item.Name, item.Category), false, `${file}: ${item.Name} / ${item.Category}`);
    });
  }
});

test("shared base and dated materials have synchronized metadata", () => {
  const baseMaterials = load("materials-data-base").MATERIALS_DATA_BASE.flatMap(record => record.Materials);
  const datedMaterials = load("materials-data").MATERIALS_DATA.flatMap(record => record.Materials);
  const metadataByUrl = new Map();
  baseMaterials.forEach(item => {
    const metadata = JSON.stringify({ Acronym: item.Acronym, Name: item.Name, Category: item.Category });
    if (metadataByUrl.has(item.Hyperlink)) assert.equal(metadataByUrl.get(item.Hyperlink), metadata);
    metadataByUrl.set(item.Hyperlink, metadata);
  });
  datedMaterials.forEach(item => {
    if (metadataByUrl.has(item.Hyperlink)) assert.equal(
      JSON.stringify({ Acronym: item.Acronym, Name: item.Name, Category: item.Category }),
      metadataByUrl.get(item.Hyperlink),
      item.Hyperlink
    );
  });
  const datedOnly = material({ Name: "Dated handout", Hyperlink: "https://example.com/dated-only.pdf" });
  assert.equal(v.audit([dated({ Materials: [datedOnly] })], "dated").valid, true);
  assert.equal(metadataByUrl.has(datedOnly.Hyperlink), false);
});

test("dated and base cards use controlled classes, visible labels, and category accessible names", () => {
  for (const [search, globals] of [
    ["?grade=10&section=B&date=2026-08-18", { MATERIALS_DATA: [dated({ Materials: [material({ Category: "slides" })] })] }],
    ["", { MATERIALS_DATA_BASE: [base({ Materials: [material({ Category: "classroom-activities" })] })] }]
  ]) {
    const page = render(search, globals);
    const grid = search ? page.content.children[1] : page.content.children[0].children[1].children[1];
    const card = grid.children[0], category = card.children[2];
    assert.match(card.className, /material-card--(?:slides|classroom-activities)$/);
    assert.ok(v.CATEGORIES.some(item => item.label === category.textContent));
    assert.ok(card.attributes["aria-label"].includes(`(${category.textContent})`));
  }
});

test("page legend always lists all four category labels", () => {
  const html = fs.readFileSync(path.join(root, "pages/materials.html"), "utf8");
  assert.match(html, /aria-label="Material categories"/);
  v.CATEGORIES.forEach(category => assert.match(html, new RegExp(`>${category.label}<\\/li>`)));
});

test("dated page states distinguish bad requests, not found, bad requested data, and ambiguity", () => {
  assert.match(render("?grade=10&section=B", {}).content.children[0].textContent, /all required/);
  assert.match(render("?grade=x&section=B&date=bad", {}).content.children[0].textContent, /Check/);
  assert.match(render("?grade=10&section=B&date=2026-08-18", {}).content.children[0].textContent, /unavailable/);
  assert.match(render("?grade=10&section=B&date=2026-08-18", { MATERIALS_DATA: [] }).content.children[0].textContent, /No materials/);
  assert.match(render("?grade=10&section=B&date=2026-08-18", { MATERIALS_DATA: [dated({ Materials: "bad" })] }).content.children[0].textContent, /this meeting/);
  assert.match(render("?grade=10&section=B&date=2026-08-18", { MATERIALS_DATA: [dated(), dated()] }).content.children[0].textContent, /ambiguous/);
  const isolated = render("?grade=10&section=B&date=2026-08-18", { MATERIALS_DATA: [dated(), dated({ Date: "bad" })] }); assert.equal(isolated.content.children[0].textContent, "Class 1-2"); assert.equal(isolated.errors.length, 1);
});

test("undated page renders valid base records while isolating malformed ones", () => {
  const page = render("", { MATERIALS_DATA_BASE: [base(), base({ Grade: "bad" })] });
  assert.equal(page.content.children[0].children[0].textContent, "Grade 10");
  assert.equal(page.content.children[0].children[1].children[0].textContent, "Term 1 — Class 2");
  assert.equal(page.errors.length, 1);
});

test("query validation and normalization", () => {
  for (const search of ["?section=B&date=2026-08-18", "?grade=10&date=2026-08-18", "?grade=10&section=B", "?grade=x&section=B&date=2026-08-18", "?grade=10&section=1&date=2026-08-18", "?grade=10&section=B&date=no", "?grade=10&section=B&date=2026-02-30"]) assert.ok(v.normalizeRequest(search).error);
  assert.deepEqual(v.normalizeRequest("?grade=%2010%20&section=%20b%20&date=%202026-8-18%20"), { mode: "dated", grade: 10, section: "B", date: "2026-08-18" });
  assert.deepEqual(v.normalizeRequest(""), { mode: "base" });
});

test("dated database isolates unrelated invalid and duplicate records", () => {
  let report = v.audit([dated(), dated({ Date: "bad" })], "dated"); assert.equal(report.records[0].valid, true); assert.equal(report.records[1].valid, false);
  report = v.audit([dated(), dated()], "dated"); assert.equal(report.duplicates[0].key, "10|B|2026-08-18");
  report = v.audit([dated(), dated({ Section: "A", Date: "2026-08-17" }), dated({ Section: "A", Date: "2026-08-17" })], "dated"); assert.equal(report.duplicates[0].key, "10|A|2026-08-17");
  assert.equal(v.audit(undefined, "dated").error, "Database global must be an array");
  assert.equal(v.audit([dated({ Materials: [] })], "dated").records[0].valid, true);
  assert.equal(v.audit([], "dated").records.length, 0);
});

test("unknown record and material properties are accepted with warnings", () => {
  const result = v.validateRecord(dated({ Note: "intentional", Materials: [material({ Note: "intentional" })] }), "dated");
  assert.equal(result.valid, true); assert.equal(result.warnings.length, 2);
});

test("material field, length, and URL rules", () => {
  assert.equal(v.validateMaterials([material({ Acronym: "ABCD" })]).valid, true);
  for (const bad of [material({ Acronym: "" }), material({ Acronym: "ABCDE" }), material({ Name: "" }), material({ Hyperlink: "bad" }), material({ Hyperlink: "ftp://example.com/a" })]) assert.equal(v.validateMaterials([bad]).valid, false);
  for (const missing of ["Acronym", "Name", "Hyperlink", "Category"]) { const value = material(); delete value[missing]; assert.equal(v.validateMaterials([value]).valid, false); }
  assert.ok(v.validUrl("http://example.com")); assert.ok(v.validUrl("https://example.com"));
});

test("base catalog validates grouping fields, empty lists, and malformed records", () => {
  assert.equal(v.validateRecord(base(), "base").valid, true); assert.equal(v.validateRecord(base({ Materials: [] }), "base").valid, true);
  assert.equal(v.validateRecord(base({ Term: "1" }), "base").valid, false);
  const data = load("materials-data-base").MATERIALS_DATA_BASE; assert.ok(data.some(r => r.Grade === 10 && r["Class #"] === "2"));
});

test("manual databases and read-only validator are unchanged by schedule generation and validation", () => {
  const paths = files.map(file => path.join(root, file)); const before = paths.map(file => fs.readFileSync(file));
  const schedulePath = path.join(root, "assets/js/databases/schedule-data.js"); const scheduleBefore = fs.readFileSync(schedulePath);
  try {
    for (const script of ["authoring/validate-materials-data.js", "authoring/generate-schedule-data.js"]) { const result = spawnSync(process.execPath, [path.join(root, script)], { encoding: "utf8" }); assert.equal(result.status, 0, result.stderr || result.stdout); }
    paths.forEach((file, index) => assert.deepEqual(fs.readFileSync(file), before[index]));
  } finally { fs.writeFileSync(schedulePath, scheduleBefore); }
});

test("a manually inserted fixture validates and can be selected without a generator", () => {
  const fixture = dated({ Date: "2027-01-02" }); const data = [fixture];
  assert.equal(v.audit(data, "dated").valid, true); assert.equal(data.find(r => v.recordKey(r, "dated") === "10|B|2027-01-02"), fixture);
});
