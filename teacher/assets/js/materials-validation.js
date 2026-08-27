(function (root, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.MaterialsValidation = api;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";
  var MAX_ACRONYM_LENGTH = 4;
  var CATEGORIES = Object.freeze([
    Object.freeze({ value: "slides", label: "Slides" }),
    Object.freeze({ value: "classroom-activities", label: "Classroom activities" }),
    Object.freeze({ value: "practice-activities", label: "Practice activities" }),
    Object.freeze({ value: "extra-resources", label: "Extra resources" })
  ]);
  var CATEGORY_VALUES = Object.freeze(CATEGORIES.map(function (category) { return category.value; }));
  var MATERIAL_FIELDS = ["Acronym", "Name", "Hyperlink", "Category"];
  var DATED_REQUIRED = ["Grade", "Term", "Section", "Class #", "Date", "Materials"];
  var BASE_REQUIRED = ["Grade", "Term", "Class #", "Materials"];

  // Compare what the user sees, rather than the stored category slug. Keeping
  // these aliases narrow prevents useful descriptions containing words such as
  // "slide" or "activity" from being rejected.
  var REDUNDANT_CATEGORY_NAMES = Object.freeze({
    "Slides": ["slide"],
    "Classroom activities": ["classroom activity"],
    "Practice activities": ["practice activity"],
    "Extra resources": ["extra resource", "class material"]
  });

  function normalizeUserFacingLabel(value) {
    return String(value || "").toLocaleLowerCase("en").replace(/[^a-z0-9]+/g, " ").trim().replace(/\s+/g, " ");
  }

  function isRedundantName(name, categoryValue) {
    var category = CATEGORIES.find(function (item) { return item.value === categoryValue; });
    if (!category) return false;
    var normalizedName = normalizeUserFacingLabel(name);
    var equivalents = [category.label].concat(REDUNDANT_CATEGORY_NAMES[category.label] || []);
    return equivalents.some(function (label) { return normalizedName === normalizeUserFacingLabel(label); });
  }

  function normalizeDate(value) {
    var match = String(value || "").trim().match(/^(\d{4})\s*(?:-|\/)\s*(\d{1,2})\s*(?:-|\/)\s*(\d{1,2})$/);
    if (!match) return null;
    var iso = match[1] + "-" + match[2].padStart(2, "0") + "-" + match[3].padStart(2, "0");
    var date = new Date(iso + "T00:00:00Z");
    return !Number.isNaN(date.getTime()) && date.toISOString().slice(0, 10) === iso ? iso : null;
  }

  function normalizeRequest(search) {
    var params = search instanceof URLSearchParams ? search : new URLSearchParams(search || "");
    var values = { grade: params.get("grade"), section: params.get("section"), date: params.get("date") };
    var supplied = Object.values(values).filter(function (value) { return value !== null; }).length;
    if (!supplied) return { mode: "base" };
    if (supplied !== 3) return { mode: "dated", error: "missing" };
    var gradeText = values.grade.trim();
    var section = values.section.trim().toUpperCase();
    var date = normalizeDate(values.date);
    if (!/^\d+$/.test(gradeText) || Number(gradeText) < 1 || !/^[A-Z]+$/.test(section) || !date) return { mode: "dated", error: "invalid" };
    return { mode: "dated", grade: Number(gradeText), section: section, date: date };
  }

  function validUrl(value) {
    if (typeof value !== "string") return null;
    try {
      var url = new URL(value);
      return url.protocol === "http:" || url.protocol === "https:" ? url.href : null;
    } catch (error) { return null; }
  }

  function properties(value, required, label, errors, warnings) {
    if (!value || typeof value !== "object" || Array.isArray(value)) { errors.push(label + " must be an object"); return; }
    required.forEach(function (field) { if (!Object.prototype.hasOwnProperty.call(value, field)) errors.push(label + " is missing " + field); });
    Object.keys(value).filter(function (field) { return !required.includes(field); }).forEach(function (field) { warnings.push(label + " has unknown property " + field); });
  }

  function validateMaterials(materials) {
    var errors = [], warnings = [];
    if (!Array.isArray(materials)) return { valid: false, errors: ["Materials must be an array"], warnings: warnings };
    if (!materials.length) warnings.push("Materials is empty");
    materials.forEach(function (material, index) {
      var label = "Materials[" + index + "]";
      properties(material, MATERIAL_FIELDS, label, errors, warnings);
      if (!material || typeof material !== "object") return;
      if (typeof material.Acronym !== "string" || !material.Acronym.trim()) errors.push(label + " Acronym must be a non-empty string");
      else if (material.Acronym.trim().length > MAX_ACRONYM_LENGTH) errors.push(label + " Acronym exceeds " + MAX_ACRONYM_LENGTH + " characters");
      if (typeof material.Name !== "string" || !material.Name.trim()) errors.push(label + " Name must be a non-empty string");
      else if (isRedundantName(material.Name, material.Category)) errors.push(label + " Name \"" + material.Name.trim() + "\" repeats category \"" + categoryDefinitionLabel(material.Category) + "\"");
      if (!validUrl(material.Hyperlink)) errors.push(label + " Hyperlink must be an HTTP or HTTPS URL");
      if (typeof material.Category !== "string" || !CATEGORY_VALUES.includes(material.Category)) errors.push(label + " Category must be one of: " + CATEGORY_VALUES.join(", "));
    });
    return { valid: !errors.length, errors: errors, warnings: warnings };
  }

  function categoryDefinitionLabel(value) {
    var category = CATEGORIES.find(function (item) { return item.value === value; });
    return category ? category.label : value;
  }

  function validateRecord(record, kind) {
    var errors = [], warnings = [], required = kind === "dated" ? DATED_REQUIRED : BASE_REQUIRED;
    properties(record, required, "Record", errors, warnings);
    if (!record || typeof record !== "object") return { valid: false, errors: errors, warnings: warnings };
    if (!Number.isInteger(record.Grade) || record.Grade < 1) errors.push("Grade must be a positive integer");
    if (!Number.isInteger(record.Term) || record.Term < 1) errors.push("Term must be a positive integer");
    if (typeof record["Class #"] !== "string" || !/^\d+(?:-\d+)?$/.test(record["Class #"].trim())) errors.push("Class # is invalid");
    if (kind === "dated") {
      if (typeof record.Section !== "string" || !/^[A-Z]+$/.test(record.Section)) errors.push("Section must contain uppercase letters");
      if (normalizeDate(record.Date) !== record.Date) errors.push("Date must be a real ISO date (YYYY-MM-DD)");
    }
    var materials = validateMaterials(record.Materials);
    errors.push.apply(errors, materials.errors); warnings.push.apply(warnings, materials.warnings);
    return { valid: !errors.length, errors: errors, warnings: warnings };
  }

  function recordKey(record, kind) {
    if (!record || typeof record !== "object") return null;
    return kind === "dated" ? [record.Grade, String(record.Section || "").toUpperCase(), normalizeDate(record.Date)].join("|") : [record.Grade, record.Term, record["Class #"]].join("|");
  }

  function audit(data, kind) {
    if (!Array.isArray(data)) return { valid: false, error: "Database global must be an array", total: 0, validCount: 0, invalidCount: 0, records: [], duplicates: [] };
    var keys = new Map();
    var records = data.map(function (record, index) {
      var result = validateRecord(record, kind), key = recordKey(record, kind);
      if (key) keys.set(key, (keys.get(key) || []).concat(index));
      return { index: index, key: key, record: record, valid: result.valid, errors: result.errors, warnings: result.warnings };
    });
    var duplicates = [];
    keys.forEach(function (indices, key) { if (indices.length > 1) duplicates.push({ key: key, indices: indices }); });
    return { valid: records.every(function (item) { return item.valid; }) && !duplicates.length, total: records.length, validCount: records.filter(function (item) { return item.valid; }).length, invalidCount: records.filter(function (item) { return !item.valid; }).length, records: records, duplicates: duplicates };
  }

  return { MAX_ACRONYM_LENGTH: MAX_ACRONYM_LENGTH, CATEGORIES: CATEGORIES, CATEGORY_VALUES: CATEGORY_VALUES, normalizeUserFacingLabel: normalizeUserFacingLabel, isRedundantName: isRedundantName, normalizeDate: normalizeDate, normalizeRequest: normalizeRequest, validUrl: validUrl, validateMaterials: validateMaterials, validateRecord: validateRecord, recordKey: recordKey, audit: audit };
});
