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
  assert.deepEqual(Array.from(v.CATEGORY_VALUES), ["slides", "classroom-activities", "practice-activities", "extra-resources", "mock-practices"]);
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
    material({ Name: "Class material", Category: "extra-resources" }),
    material({ Name: "Mock practice", Category: "mock-practices" })
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

test("Term 2 shared base and dated materials have synchronized metadata", () => {
  // Term 1 has pre-existing Grade 11 label differences; preserve that unrelated work.
  const baseMaterials = load("materials-data-base").MATERIALS_DATA_BASE.filter(affected).flatMap(record => record.Materials);
  const datedMaterials = load("materials-data").MATERIALS_DATA.filter(affected).flatMap(record => record.Materials);
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

test("page legend always lists all five category labels and controlled styles", () => {
  const html = fs.readFileSync(path.join(root, "pages/materials.html"), "utf8");
  assert.match(html, /aria-label="Material categories"/);
  v.CATEGORIES.forEach(category => assert.match(html, new RegExp(`>${category.label}<\\/li>`)));
  assert.equal((html.match(/<li class="material-legend--/g) || []).length, 5);
  v.CATEGORY_VALUES.forEach(category => {
    assert.ok(html.includes(`.material-card--${category}, .material-legend--${category}`));
    assert.equal((html.match(new RegExp(`--material-${category}:`, "g")) || []).length, 2);
  });
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

test("manual databases and schedule are unchanged by read-only validation", () => {
  const paths = files.map(file => path.join(root, file)); const before = paths.map(file => fs.readFileSync(file));
  const schedulePath = path.join(root, "assets/js/databases/schedule-data.js"); const scheduleBefore = fs.readFileSync(schedulePath);
  const result = spawnSync(process.execPath, [path.join(root, "authoring/validate-materials-data.js")], { encoding: "utf8" });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  paths.forEach((file, index) => assert.deepEqual(fs.readFileSync(file), before[index]));
  assert.deepEqual(fs.readFileSync(schedulePath), scheduleBefore);
  const generator = fs.readFileSync(path.join(root, "authoring/generate-schedule-data.js"), "utf8");
  assert.doesNotMatch(generator, /writeFileSync\([^\n]*materials/);
});

test("a manually inserted fixture validates and can be selected without a generator", () => {
  const fixture = dated({ Date: "2027-01-02" }); const data = [fixture];
  assert.equal(v.audit(data, "dated").valid, true); assert.equal(data.find(r => v.recordKey(r, "dated") === "10|B|2027-01-02"), fixture);
});

function affected(record) { return [10, 11].includes(record.Grade) && record.Term === 2; }
function plain(value) { return JSON.parse(JSON.stringify(value)); }
const site = "https://nolopez338.github.io/global_economics/";
const criterionMeetings = { 2: 1, 3: 2, 4: 3, 6: 4, 9: 5, 10: 6, 11: 7, 13: 8, 14: 9, 15: 10 };
const mockMeetings = { 4: [1, "C1C2"], 7: [1, "C3C4"], 11: [2, "C5C6C7"], 15: [3, "C8C9C10"] };
const emptyMeetings = [5, 8, 12, 16, 17, 18, 19, 20];

test("both Term 2 catalogs have the exact 20-class sequence and reference targets", () => {
  const all = plain(load("materials-data-base").MATERIALS_DATA_BASE);
  for (const grade of [10, 11]) {
    const records = all.filter(r => r.Grade === grade && r.Term === 2);
    assert.deepEqual(records.map(r => Number(r["Class #"])), Array.from({ length: 20 }, (_, i) => i + 1));
    const html = fs.readFileSync(path.join(root, `../grade${grade}/src/G${grade}_T2.html`), "utf8");
    const referenceLinks = Array.from(html.matchAll(/href="([^"]+)"/g), m => new URL(m[1], `${site}grade${grade}/src/G${grade}_T2.html`).href);
    for (const record of records) {
      const n = Number(record["Class #"]), resources = record.Materials;
      const ci = criterionMeetings[n], mock = mockMeetings[n];
      assert.equal(resources.length, n === 1 ? 2 : (ci ? 3 : 0) + (mock ? 2 : 0), `Grade ${grade} class ${n}`);
      if (emptyMeetings.includes(n)) assert.deepEqual(resources, []);
      if (n === 1) for (const term of [1, 2]) {
        const outlinePath = `grade${grade}/src/pages/term${term}/g${grade}-t${term}-outline.html`;
        assert.equal(resources[term - 1].Hyperlink, site + outlinePath);
        assert.equal(resources[term - 1].Category, "extra-resources");
        assert.equal(resources[term - 1].Name, `Term ${term} outline`);
        const outline = fs.readFileSync(path.join(root, "..", outlinePath), "utf8");
        assert.ok(outline.includes(`G${grade}_T${term}.html#general-information`));
      }
      if (ci) {
        const level = ci <= 4 ? 1 : ci <= 7 ? 2 : 3;
        for (const [index, category, folder, suffix] of [
          [0, "practice-activities", "1-practice_activities", grade === 11 ? "practice" : "practice_activity"],
          [1, "slides", "3-slides", "slides"],
          [2, "classroom-activities", "2-class_activities", "classroom_activity"]
        ]) {
          const item = resources[index];
          assert.equal(item.Category, category);
          assert.match(item.Name, new RegExp(`^C${ci} `));
          assert.equal(item.Hyperlink, `${site}book2026-2027/grade${grade}/term_2/${folder}/G${grade}_T2_L${level}_C${ci}_${suffix}.pdf`);
          if (!(grade === 10 && ci === 10)) assert.ok(referenceLinks.includes(item.Hyperlink));
          assert.ok(item.Acronym.length <= 4);
        }
      }
      if (mock) {
        const items = resources.filter(m => m.Category === "mock-practices");
        assert.equal(items.length, 2);
        const [level, criteria] = mock;
        assert.ok(fs.statSync(path.join(root, `../book2026-2027/grade${grade}/term_2/4-learning_evidences`)).isDirectory());
        for (const [index, suffix] of [[0, ""], [1, "_solution"]]) {
          assert.equal(items[index].Hyperlink, `${site}book2026-2027/grade${grade}/term_2/4-learning_evidences/G${grade}_T2_L${level}_${criteria}_exam${suffix}.pdf`);
          assert.ok(items[index].Name.includes(criteria.match(/C\d+/g).join(" & ")));
          assert.match(items[index].Name, index ? /mock solution$/ : /mock exam$/);
        }
      }
      resources.forEach(item => { assert.ok(item.Hyperlink.startsWith(site)); assert.equal(v.validateMaterials([item]).valid, true); });
    }
  }
});

test("all scheduled Term 2 sections map by sequential meeting with no omissions or duplicates", () => {
  const schedule = plain(load("schedule-data").SCHEDULE_DATA).filter(affected);
  const datedRecords = plain(load("materials-data").MATERIALS_DATA).filter(affected);
  const baseRecords = plain(load("materials-data-base").MATERIALS_DATA_BASE).filter(affected);
  assert.equal(schedule.length, 210);
  assert.equal(datedRecords.length, schedule.length);
  const key = r => `${r.Grade}|${r.Section.toUpperCase()}|${v.normalizeDate(r.Date)}`;
  assert.equal(new Set(schedule.map(key)).size, schedule.length);
  assert.equal(new Set(datedRecords.map(key)).size, datedRecords.length);
  assert.deepEqual(datedRecords.map(key).sort(), schedule.map(key).sort());
  const groups = Map.groupBy(schedule, r => `${r.Grade}|${r.Section.toUpperCase()}`);
  assert.deepEqual([...groups.keys()].sort(), ["10|A", "10|B", "10|C", "10|D", "10|E", "10|SEMINAR", "11|A", "11|B", "11|C", "11|D", "11|E"]);
  for (const [group, meetings] of groups) {
    meetings.sort((a, b) => v.normalizeDate(a.Date).localeCompare(v.normalizeDate(b.Date)));
    const seminar = group === "10|SEMINAR";
    assert.equal(meetings.length, seminar ? 10 : 20);
    meetings.forEach((meeting, index) => {
      const ordinal = index + 1;
      assert.equal(meeting["Class #"], seminar ? `${ordinal}-1` : `${Math.floor(index / 2) + 1}-${index % 2 + 1}`);
      const record = datedRecords.find(r => key(r) === key(meeting));
      assert.equal(record["Class #"], meeting["Class #"]);
      assert.equal(record.Term, meeting.Term);
      assert.deepEqual(record.Materials, baseRecords.find(r => r.Grade === record.Grade && r["Class #"] === String(ordinal)).Materials, `${group} sequential class ${ordinal}`);
    });
  }
});

test("every affected dated record renders all cards with safe category semantics or its empty state", () => {
  const data = load("materials-data").MATERIALS_DATA;
  for (const record of data.filter(affected)) {
    const page = render(`?grade=${record.Grade}&section=${record.Section}&date=${record.Date}`, { MATERIALS_DATA: data });
    assert.equal(page.errors.length, 0);
    if (!record.Materials.length) {
      assert.equal(page.content.children[0].textContent, `No materials found for Grade ${record.Grade}${record.Section} on ${record.Date}.`);
      continue;
    }
    assert.equal(page.content.children[0].textContent, `Class ${record["Class #"]}`);
    const cards = page.content.children[1].children;
    assert.equal(cards.length, record.Materials.length);
    cards.forEach((card, index) => {
      const item = record.Materials[index], label = v.CATEGORIES.find(c => c.value === item.Category).label;
      assert.equal(card.className, `class-card material-card material-card--${item.Category}`);
      assert.equal(card.children[2].textContent, label);
      assert.equal(card.attributes["aria-label"], `Open ${item.Name} (${label}) for Grade ${record.Grade}${record.Section} on ${record.Date}`);
      assert.equal(card.href, item.Hyperlink);
      assert.equal(card.target, "_blank"); assert.equal(card.rel, "noopener noreferrer");
    });
  }
});

test("base mode renders combined five-card meetings and mock-only meetings for both grades", () => {
  const data = load("materials-data-base").MATERIALS_DATA_BASE;
  const page = render("", { MATERIALS_DATA_BASE: data });
  assert.equal(page.errors.length, 0);
  for (const grade of [10, 11]) {
    const group = page.content.children.find(e => e.children[0].textContent === `Grade ${grade}`);
    for (const n of [4, 7, 11, 15]) {
      const section = group.children.find(e => e.children[0]?.textContent === `Term 2 — Class ${n}`);
      const cards = section.children[1].children;
      assert.equal(cards.length, n === 7 ? 2 : 5);
      const mocks = cards.filter(card => card.className.endsWith("material-card--mock-practices"));
      assert.equal(mocks.length, 2);
      mocks.forEach(card => { assert.equal(card.children[2].textContent, "Mock practices"); assert.ok(card.attributes["aria-label"].includes("(Mock practices)")); });
    }
  }
});

test("January 15 Grade 11B is scheduled class 4-2 with no assessment materials", () => {
  const schedule = load("schedule-data").SCHEDULE_DATA;
  const matches = schedule.filter(r => r.Grade === 11 && r.Section === "B" && v.normalizeDate(r.Date) === "2027-01-15");
  assert.equal(matches.length, 1); assert.equal(matches[0]["Class #"], "4-2");
  assert.match(matches[0].Description, /Learning Evidence C3 C4/);
  const data = load("materials-data").MATERIALS_DATA;
  const page = render("?grade=11&section=B&date=2027-01-15", { MATERIALS_DATA: data });
  assert.equal(page.content.children[0].textContent, "No materials found for Grade 11B on 2027-01-15.");
});

test("unrelated materials and every original record identity are preserved", () => {
  const hash = value => require("node:crypto").createHash("sha256").update(JSON.stringify(value)).digest("hex");
  // Baselines captured before this Term 2 update, including pre-existing Term 1 metadata differences.
  for (const [file, globalName, unrelatedHash, identityHash] of [
    ["materials-data-base", "MATERIALS_DATA_BASE", "8ff1e484a16df02ee6f6198768c8da234ae24281b46f9adca76675f68070d5df", "6f2f33efba1b76bfc5f7aa6298062d23f1a7d740e3127a0823453699c4aab17c"],
    ["materials-data", "MATERIALS_DATA", "515dca2d2fb86279bbc46dd5b76ee5a01da15d1edba942bf27d869d5c6b17620", "7a18e00bcbcd2d6202087ab822b17c5cd057095d473a7eca2083ef8750a7608f"]
  ]) {
    const data = plain(load(file)[globalName]);
    assert.equal(hash(data.filter(r => !affected(r))), unrelatedHash);
    assert.equal(hash(data.map(({ Materials, ...identity }) => identity)), identityHash);
  }
});
