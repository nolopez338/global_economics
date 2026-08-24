#!/usr/bin/env node

/*
 * Generates the runtime schedule artifact from the authoring CSV and validates
 * every row against the registered 2026-2027 academic calendar.
 */

const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const calendar = require("../assets/js/databases/year-calendar-data.js");

const sourcePath = path.join(__dirname, "schedule.csv");
const outputPath = path.join(__dirname, "../assets/js/databases/schedule-data.js");
const materialsBasePath = path.join(__dirname, "../assets/js/databases/materials-data-base.js");
const materialsOutputPath = path.join(__dirname, "../assets/js/databases/materials-data.js");
const fields = [
  "Grade", "Section", "Class #", "Date", "Term", "Weekday", "Day",
  "Description", "Material", "Material teacher", "Summary"
];
const meetingDays = {
  "10A": [1, 3], "10B": [3, 4], "10C": [1, 5], "10D": [4, 6], "10E": [1, 5],
  "10Seminar": [4],
  "11A": [1, 3], "11B": [2, 3], "11C": [1, 6], "11D": [3, 5], "11E": [1, 6]
};
const weekdayNames = {
  mo: "Monday", tu: "Tuesday", we: "Wednesday", th: "Thursday",
  fr: "Friday", sa: "Saturday", su: "Sunday"
};

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = "";
  let quoted = false;

  for (let index = 0; index < text.length; index++) {
    const character = text[index];
    if (quoted && character === '"' && text[index + 1] === '"') {
      value += '"';
      index++;
    } else if (character === '"') {
      quoted = !quoted;
    } else if (!quoted && character === ",") {
      row.push(value);
      value = "";
    } else if (!quoted && (character === "\n" || character === "\r")) {
      if (character === "\r" && text[index + 1] === "\n") index++;
      row.push(value);
      if (row.some(cell => cell !== "")) rows.push(row);
      row = [];
      value = "";
    } else {
      value += character;
    }
  }
  if (value || row.length) {
    row.push(value);
    rows.push(row);
  }
  return rows;
}

function fail(message) {
  throw new Error(`schedule.csv: ${message}`);
}

const csvRows = parseCsv(fs.readFileSync(sourcePath, "utf8"));
const headers = csvRows.shift();
if (JSON.stringify(headers) !== JSON.stringify(fields)) {
  fail(`expected headers ${fields.join(",")}`);
}

const records = csvRows.map((values, index) => {
  if (values.length !== fields.length) fail(`row ${index + 2} has ${values.length} fields`);
  const record = Object.fromEntries(fields.map((field, fieldIndex) => [field, values[fieldIndex]]));
  record.Grade = Number(record.Grade);
  record.Term = record.Term === "" ? null : Number(record.Term);
  record.Day = Number(record.Day);
  return record;
});

const expectedKeys = new Set();
for (const [classId, days] of Object.entries(meetingDays)) {
  for (const yearData of Object.values(calendar.cycleDayRegistry)) {
    for (const monthData of yearData.months) {
      const calendarMonth = calendar.calendarRegistry[yearData.year].months.find(item => item.month === monthData.month);
      monthData.weeks.forEach((week, weekIndex) => week.forEach((cycleDay, weekdayIndex) => {
        if (!days.includes(cycleDay)) return;
        const day = calendarMonth.weeks[weekIndex][weekdayIndex];
        const isoDate = `${yearData.year}-${String(monthData.month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
        expectedKeys.add(`${classId}|${isoDate}`);
      }));
    }
  }
}

const actualKeys = new Set();
for (const [index, record] of records.entries()) {
  const rowNumber = index + 2;
  const classId = `${record.Grade}${record.Section}`;
  const days = meetingDays[classId];
  if (!days) fail(`row ${rowNumber} has unsupported class ${classId}`);
  const dateMatch = /^(\d{4}) \/ (\d{2}) \/ (\d{2})$/.exec(record.Date);
  if (!dateMatch) fail(`row ${rowNumber} has invalid Date format`);
  const isoDate = `${dateMatch[1]}-${dateMatch[2]}-${dateMatch[3]}`;
  const info = calendar.getAcademicDateInfo(isoDate);
  const meetingNumber = days.indexOf(info.cycleDay) + 1;
  if (!meetingNumber) fail(`row ${rowNumber} is not a meeting day for ${classId}`);
  const expectedClassNumber = `${info.cycleNumber}-${meetingNumber}`;
  const expectedTerm = info.term === null ? null : Number(info.term.slice(-1));
  if (record["Class #"] !== expectedClassNumber) fail(`row ${rowNumber} Class # must be ${expectedClassNumber}`);
  if (record.Term !== expectedTerm) fail(`row ${rowNumber} Term must be ${expectedTerm}`);
  if (record.Weekday !== weekdayNames[info.weekday]) fail(`row ${rowNumber} Weekday is incorrect`);
  if (record.Day !== info.cycleDay) fail(`row ${rowNumber} Day must be ${info.cycleDay}`);
  for (const field of ["Description", "Material", "Material teacher", "Summary"]) {
    if (record[field] !== "-") fail(`row ${rowNumber} ${field} must be "-"`);
  }
  const key = `${classId}|${isoDate}`;
  if (actualKeys.has(key)) fail(`row ${rowNumber} duplicates ${key}`);
  actualKeys.add(key);
}

const missing = [...expectedKeys].filter(key => !actualKeys.has(key));
const unexpected = [...actualKeys].filter(key => !expectedKeys.has(key));
if (missing.length || unexpected.length) {
  fail(`meeting coverage differs (missing ${missing.length}, unexpected ${unexpected.length})`);
}

const sorted = [...records].sort((left, right) =>
  left.Grade - right.Grade || left.Section.localeCompare(right.Section) || left.Date.localeCompare(right.Date)
);
if (JSON.stringify(records) !== JSON.stringify(sorted)) fail("records are not ordered by grade, section, and date");

const header = `/*
  Purpose:
  Stores the dated schedule dataset generated from the authoring CSV source.

  Responsibilities:
  - Exposes window.SCHEDULE_DATA as the global schedule input for table rendering
  - Provides class entries with section, date, weekday, materials, and summary fields
  - Supplies content consumed by schedule/class page scripts without adding UI behavior
*/
// AUTO-GENERATED FILE
// Generated from teacher/authoring/schedule.csv by teacher/authoring/generate-schedule-data.js
// Do not edit manually.
`;
fs.writeFileSync(outputPath, `${header}window.SCHEDULE_DATA = ${JSON.stringify(records, null, 2)};\n`);
console.log(`Generated ${records.length} records in ${path.relative(process.cwd(), outputPath)}`);

const materialsContext = { window: {} };
vm.runInNewContext(fs.readFileSync(materialsBasePath, "utf8"), materialsContext, {
  filename: materialsBasePath
});
const materialsBase = materialsContext.window.MATERIALS_DATA_BASE;
if (!Array.isArray(materialsBase)) throw new Error("materials-data-base.js must expose an array");

const baseByClass = new Map();
for (const record of materialsBase) {
  const key = `${record.Grade}|${record["Class #"]}`;
  if (baseByClass.has(key)) throw new Error(`materials-data-base.js duplicates ${key}`);
  if (!Array.isArray(record.Materials)) throw new Error(`materials-data-base.js ${key} has invalid Materials`);
  baseByClass.set(key, record.Materials);
}

const datedKeys = new Set();
const datedMaterials = records.map((record) => {
  const date = record.Date.replace(/\s*\/\s*/g, "-");
  const section = String(record.Section).toUpperCase();
  const datedKey = `${record.Grade}|${section}|${date}`;
  if (datedKeys.has(datedKey)) throw new Error(`schedule-data.js duplicates meeting ${datedKey}`);
  datedKeys.add(datedKey);

  const baseClass = String(record["Class #"]).split("-")[0];
  const materials = baseByClass.get(`${record.Grade}|${baseClass}`);
  if (!materials) throw new Error(`missing base materials for Grade ${record.Grade}, Class ${baseClass}`);
  return {
    Grade: record.Grade,
    Section: section,
    "Class #": record["Class #"],
    Date: date,
    Materials: materials.map((material) => ({
      Acronym: material.Acronym,
      Name: material.Name,
      Hyperlink: material.Hyperlink
    }))
  };
});

const materialsHeader = `/*
  Purpose:
  Stores dated class materials generated from the schedule and base materials catalog.
*/
// AUTO-GENERATED FILE
// Generated from schedule.csv and materials-data-base.js by generate-schedule-data.js
// Do not edit manually.
`;
fs.writeFileSync(
  materialsOutputPath,
  `${materialsHeader}window.MATERIALS_DATA = ${JSON.stringify(datedMaterials, null, 2)};\n`
);
console.log(`Generated ${datedMaterials.length} records in ${path.relative(process.cwd(), materialsOutputPath)}`);
