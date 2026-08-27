(function () {
  "use strict";
  var content = document.getElementById("materials-content");
  var pageHeading = document.querySelector("#materials-page > h1");
  var validation = window.MaterialsValidation;

  function showStatus(message) {
    content.replaceChildren();
    var status = document.createElement("p");
    status.className = "materials-status";
    status.setAttribute("role", "status");
    status.textContent = message;
    content.appendChild(status);
  }

  function createGrid(materials, context) {
    var grid = document.createElement("div");
    grid.className = "class-grid";
    materials.forEach(function (material) {
      var card = document.createElement("a");
      card.className = "class-card";
      card.href = validation.validUrl(material.Hyperlink);
      card.target = "_blank";
      card.rel = "noopener noreferrer";
      card.setAttribute("aria-label", "Open " + material.Name.trim() + " for " + context);
      var icon = document.createElement("span");
      icon.className = "class-icon";
      icon.textContent = material.Acronym.trim();
      var label = document.createElement("span");
      label.className = "class-label";
      label.textContent = material.Name.trim();
      card.append(icon, label);
      grid.appendChild(card);
    });
    return grid;
  }

  function reportAudit(label, audit) {
    if (audit.error) console.error(label + " database is unavailable", audit.error);
    audit.records.forEach(function (item) {
      if (!item.valid) console.error(label + " record " + item.index + " is invalid", item.errors);
      if (item.warnings.length) console.warn(label + " record " + item.index + " warnings", item.warnings);
    });
    audit.duplicates.forEach(function (duplicate) { console.error(label + " duplicate key " + duplicate.key, duplicate.indices); });
  }

  if (!content || !pageHeading || !validation) return;
  var request = validation.normalizeRequest(window.location.search);
  if (request.mode === "dated") {
    if (request.error === "missing") { showStatus("Invalid materials request. Grade, section, and date are all required."); return; }
    if (request.error) { showStatus("Invalid materials request. Check the grade, section, and date."); return; }
    if (!Array.isArray(window.MATERIALS_DATA)) { console.error("MATERIALS_DATA is not an array"); showStatus("Materials are currently unavailable. Please return to the schedule and try again later."); return; }

    var audit = validation.audit(window.MATERIALS_DATA, "dated");
    reportAudit("Dated materials", audit);
    var key = [request.grade, request.section, request.date].join("|");
    var matches = audit.records.filter(function (item) { return item.key === key; });
    pageHeading.textContent = "Materials — Grade " + request.grade + request.section + " — " + request.date;
    document.title = pageHeading.textContent;
    if (!matches.length) { showStatus("No materials found for Grade " + request.grade + request.section + " on " + request.date + "."); return; }
    if (matches.length > 1) { showStatus("Materials could not be displayed because this meeting is ambiguous."); return; }
    if (!matches[0].valid) { showStatus("Materials could not be displayed for this meeting."); return; }
    var meeting = matches[0].record;
    if (!meeting.Materials.length) { showStatus("No materials found for Grade " + request.grade + request.section + " on " + request.date + "."); return; }
    content.replaceChildren();
    var heading = document.createElement("h2");
    heading.textContent = "Class " + meeting["Class #"];
    content.append(heading, createGrid(meeting.Materials, "Grade " + request.grade + request.section + " on " + request.date));
    return;
  }

  var baseAudit = validation.audit(window.MATERIALS_DATA_BASE, "base");
  reportAudit("Base materials", baseAudit);
  if (baseAudit.error) { showStatus("Materials are currently unavailable. Please return to the schedule and try again later."); return; }
  var records = baseAudit.records.filter(function (item) { return item.valid; }).map(function (item) { return item.record; }).sort(function (a, b) { return a.Grade - b.Grade || a.Term - b.Term || Number(a["Class #"]) - Number(b["Class #"]); });
  if (!records.length) { showStatus("No materials found."); return; }
  content.replaceChildren();
  var grades = new Map();
  records.forEach(function (record) { if (!grades.has(record.Grade)) grades.set(record.Grade, []); grades.get(record.Grade).push(record); });
  grades.forEach(function (gradeRecords, grade) {
    var gradeSection = document.createElement("section"), gradeHeading = document.createElement("h2");
    gradeSection.className = "grade-section"; gradeHeading.textContent = "Grade " + grade; gradeSection.appendChild(gradeHeading);
    gradeRecords.forEach(function (record) {
      var classSection = document.createElement("section"), classHeading = document.createElement("h3");
      classSection.className = "class-section"; classHeading.textContent = "Term " + record.Term + " — Class " + record["Class #"]; classSection.appendChild(classHeading);
      if (record.Materials.length) classSection.appendChild(createGrid(record.Materials, "Grade " + grade + ", Term " + record.Term + ", Class " + record["Class #"]));
      else { var empty = document.createElement("p"); empty.className = "materials-status"; empty.textContent = "No materials found for this class."; classSection.appendChild(empty); }
      gradeSection.appendChild(classSection);
    });
    content.appendChild(gradeSection);
  });
})();
