#!/usr/bin/env node
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const validation = require("../assets/js/materials-validation.js");

const databases = [
  ["dated", "MATERIALS_DATA", path.join(__dirname, "../assets/js/databases/materials-data.js")],
  ["base", "MATERIALS_DATA_BASE", path.join(__dirname, "../assets/js/databases/materials-data-base.js")]
];
let failed = false;
for (const [kind, globalName, file] of databases) {
  const context = { window: {} };
  vm.runInNewContext(fs.readFileSync(file, "utf8"), context, { filename: file });
  const report = validation.audit(context.window[globalName], kind);
  console.log(`${path.basename(file)}: total=${report.total} valid=${report.validCount} invalid=${report.invalidCount}`);
  console.log(`  duplicate keys: ${report.duplicates.length ? report.duplicates.map(item => item.key).join(", ") : "none"}`);
  for (const item of report.records) {
    if (item.errors.length) console.log(`  record ${item.index} (${item.key}): ${item.errors.join("; ")}`);
    if (item.warnings.length) console.log(`  record ${item.index} (${item.key}) warnings: ${item.warnings.join("; ")}`);
  }
  report.duplicates.forEach(item => console.log(`  duplicate ${item.key}: records ${item.indices.join(", ")}`));
  if (!report.valid) failed = true;
}
if (failed) process.exitCode = 1;
