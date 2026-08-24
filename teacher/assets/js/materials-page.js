(function () {
  "use strict";

  var content = document.getElementById("materials-content");
  var pageHeading = document.querySelector("#materials-page > h1");

  function showStatus(message) {
    content.replaceChildren();
    var status = document.createElement("p");
    status.className = "materials-status";
    status.setAttribute("role", "status");
    status.textContent = message;
    content.appendChild(status);
  }

  function normalizeDate(value) {
    var match = String(value || "").trim().match(/^(\d{4})\s*(?:-|\/)\s*(\d{1,2})\s*(?:-|\/)\s*(\d{1,2})$/);
    if (!match) return null;
    var iso = match[1] + "-" + match[2].padStart(2, "0") + "-" + match[3].padStart(2, "0");
    var date = new Date(iso + "T00:00:00Z");
    return !Number.isNaN(date.getTime()) && date.toISOString().slice(0, 10) === iso ? iso : null;
  }

  function validUrl(value) {
    try {
      var url = new URL(value);
      return url.protocol === "http:" || url.protocol === "https:" ? url.href : null;
    } catch (error) {
      return null;
    }
  }

  function validMaterials(materials) {
    return Array.isArray(materials) && materials.every(function (material) {
      return material && Object.keys(material).sort().join("|") === "Acronym|Hyperlink|Name" &&
        typeof material.Acronym === "string" && material.Acronym.trim().length > 0 && material.Acronym.trim().length <= 4 &&
        typeof material.Name === "string" && material.Name.trim().length > 0 &&
        typeof material.Hyperlink === "string" && Boolean(validUrl(material.Hyperlink));
    });
  }

  function createGrid(materials, context) {
    var grid = document.createElement("div");
    grid.className = "class-grid";
    materials.forEach(function (material) {
      var card = document.createElement("a");
      card.className = "class-card";
      card.href = validUrl(material.Hyperlink);
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

  if (!content || !pageHeading) return;
  var params = new URLSearchParams(window.location.search);
  var gradeParam = params.get("grade");
  var sectionParam = params.get("section");
  var dateParam = params.get("date");
  var hasDatedParam = gradeParam !== null || sectionParam !== null || dateParam !== null;

  if (hasDatedParam) {
    if (gradeParam === null || sectionParam === null || dateParam === null) {
      showStatus("Invalid materials request. Grade, section, and date are all required.");
      return;
    }
    var grade = gradeParam.trim();
    var section = sectionParam.trim().toUpperCase();
    var date = normalizeDate(dateParam);
    if (!/^\d+$/.test(grade) || !/^[A-Z]+$/.test(section) || !date) {
      showStatus("Invalid materials request. Check the grade, section, and date.");
      return;
    }
    if (!Array.isArray(window.MATERIALS_DATA)) {
      showStatus("Materials are currently unavailable. Please return to the schedule and try again later.");
      return;
    }
    var duplicateKeys = new Set();
    var datedDataValid = window.MATERIALS_DATA.every(function (record) {
      if (!record || Object.keys(record).sort().join("|") !== "Class #|Date|Grade|Materials|Section" ||
          !Number.isInteger(record.Grade) || typeof record.Section !== "string" ||
          record.Section !== record.Section.toUpperCase() || normalizeDate(record.Date) !== record.Date ||
          !validMaterials(record.Materials)) return false;
      var key = String(record.Grade) + "|" + String(record.Section).toUpperCase() + "|" + normalizeDate(record.Date);
      if (duplicateKeys.has(key)) return false;
      duplicateKeys.add(key);
      return typeof record["Class #"] === "string" && Boolean(record["Class #"].trim());
    });
    if (!datedDataValid) {
      showStatus("Materials could not be displayed because the dated database contains invalid records.");
      return;
    }
    var meeting = window.MATERIALS_DATA.find(function (record) {
      return String(record.Grade) === grade && String(record.Section).toUpperCase() === section && normalizeDate(record.Date) === date;
    });
    pageHeading.textContent = "Materials — Grade " + grade + section + " — " + date;
    document.title = pageHeading.textContent;
    if (!meeting || meeting.Materials.length === 0) {
      showStatus("No materials found for Grade " + grade + section + " on " + date + ".");
      return;
    }
    content.replaceChildren();
    var datedHeading = document.createElement("h2");
    datedHeading.textContent = "Class " + meeting["Class #"];
    content.append(datedHeading, createGrid(meeting.Materials, "Grade " + grade + section + " on " + date));
    return;
  }

  if (!Array.isArray(window.MATERIALS_DATA_BASE)) {
    showStatus("Materials are currently unavailable. Please return to the schedule and try again later.");
    return;
  }
  var baseValid = window.MATERIALS_DATA_BASE.every(function (record) {
    return record && Number.isInteger(record.Grade) && typeof record["Class #"] === "string" &&
      Boolean(record["Class #"].trim()) && validMaterials(record.Materials);
  });
  if (!baseValid) {
    showStatus("Materials could not be displayed because the database contains invalid records.");
    return;
  }
  var records = window.MATERIALS_DATA_BASE.slice().sort(function (a, b) {
    return a.Grade - b.Grade || Number(a["Class #"]) - Number(b["Class #"]);
  });
  if (!records.length) {
    showStatus("No materials found.");
    return;
  }
  content.replaceChildren();
  var grades = new Map();
  records.forEach(function (record) {
    if (!grades.has(record.Grade)) grades.set(record.Grade, []);
    grades.get(record.Grade).push(record);
  });
  grades.forEach(function (gradeRecords, grade) {
    var gradeSection = document.createElement("section");
    gradeSection.className = "grade-section";
    var gradeHeading = document.createElement("h2");
    gradeHeading.textContent = "Grade " + grade;
    gradeSection.appendChild(gradeHeading);
    gradeRecords.forEach(function (record) {
      var classSection = document.createElement("section");
      classSection.className = "class-section";
      var classHeading = document.createElement("h3");
      classHeading.textContent = "Class " + record["Class #"];
      classSection.appendChild(classHeading);
      if (record.Materials.length) {
        classSection.appendChild(createGrid(record.Materials, "Grade " + grade + ", Class " + record["Class #"]));
      } else {
        var empty = document.createElement("p");
        empty.className = "materials-status";
        empty.textContent = "No materials found for this class.";
        classSection.appendChild(empty);
      }
      gradeSection.appendChild(classSection);
    });
    content.appendChild(gradeSection);
  });
})();
