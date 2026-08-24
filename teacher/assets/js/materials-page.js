(function () {
  "use strict";

  var content = document.getElementById("materials-content");

  function showStatus(message) {
    content.replaceChildren();
    var status = document.createElement("p");
    status.className = "materials-status";
    status.setAttribute("role", "status");
    status.textContent = message;
    content.appendChild(status);
  }

  function validUrl(value) {
    try {
      var url = new URL(value);
      return url.protocol === "http:" || url.protocol === "https:" ? url.href : null;
    } catch (error) {
      return null;
    }
  }

  function validRecord(record) {
    if (!record || !Number.isInteger(record.Grade) || typeof record["Class #"] !== "string" || !record["Class #"].trim() || !Array.isArray(record.Materials)) return false;
    return record.Materials.length > 0 && record.Materials.every(function (material) {
      return material && Object.keys(material).length === 3 &&
        typeof material.Acronym === "string" && material.Acronym.trim().length > 0 && material.Acronym.trim().length <= 4 &&
        typeof material.Name === "string" && material.Name.trim().length > 0 &&
        typeof material.Hyperlink === "string" && Boolean(validUrl(material.Hyperlink));
    });
  }

  if (!content) return;
  if (!Array.isArray(window.MATERIALS_DATA_BASE)) {
    showStatus("Materials are currently unavailable. Please return to the schedule and try again later.");
    return;
  }

  var params = new URLSearchParams(window.location.search);
  var gradeFilter = params.get("grade");
  var classFilter = params.get("class");
  var invalidRecords = window.MATERIALS_DATA_BASE.filter(function (record) { return !validRecord(record); });
  if (invalidRecords.length) {
    showStatus("Materials could not be displayed because the database contains invalid records.");
    return;
  }

  var records = window.MATERIALS_DATA_BASE.filter(function (record) {
    return (gradeFilter === null || String(record.Grade) === gradeFilter) &&
      (classFilter === null || record["Class #"] === classFilter);
  });
  if (!records.length) {
    showStatus("No materials were found for the requested grade or class.");
    return;
  }

  records.sort(function (a, b) { return a.Grade - b.Grade || Number(a["Class #"]) - Number(b["Class #"]); });
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
      var grid = document.createElement("div");
      grid.className = "class-grid";

      record.Materials.forEach(function (material) {
        var card = document.createElement("a");
        card.className = "class-card";
        card.href = validUrl(material.Hyperlink);
        card.target = "_blank";
        card.rel = "noopener noreferrer";
        card.setAttribute("aria-label", "Open " + material.Name.trim() + " for Grade " + grade + ", Class " + record["Class #"]);
        var icon = document.createElement("span");
        icon.className = "class-icon";
        icon.textContent = material.Acronym.trim();
        var label = document.createElement("span");
        label.className = "class-label";
        label.textContent = material.Name.trim();
        card.append(icon, label);
        grid.appendChild(card);
      });
      classSection.appendChild(grid);
      gradeSection.appendChild(classSection);
    });
    content.appendChild(gradeSection);
  });
})();
