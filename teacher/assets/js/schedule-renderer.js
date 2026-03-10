const formatScheduleDate = (value) => {
  const [year, month, day] = value.split("/").map((part) => part.trim());
  if (!year || !month || !day) {
    return value;
  }

  return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
};

const getScheduleData = () => {
  if (Array.isArray(window.SCHEDULE_DATA)) {
    return Promise.resolve(window.SCHEDULE_DATA);
  }

  return Promise.resolve([]);
};

const getColumnCount = (table) =>
  table.tHead?.rows[0]?.cells.length ?? 1;

const normalizeScheduleDate = (raw) => {
  if (!raw) {
    return null;
  }

  const match = String(raw).trim().match(/^(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})$/);
  if (!match) {
    return null;
  }

  const [, year, month, day] = match;
  return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
};

const getTodayISODate = () => {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, "0");
  const dd = String(today.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
};

const renderEmptyRow = (table) => {
  const body = table.tBodies[0] ?? table.createTBody();
  body.innerHTML = "";

  const row = document.createElement("tr");
  const cell = document.createElement("td");
  cell.colSpan = getColumnCount(table);
  cell.textContent = "No scheduled entries.";
  row.append(cell);
  body.append(row);
};

const renderScheduleRows = (table, entries) => {
  table.querySelectorAll("tbody").forEach((body) => body.remove());

  const mainBody = table.createTBody();

  const todayISO = getTodayISODate();
  const currentAndFutureEntries = [];
  const pastEntries = [];

  entries.forEach((entry) => {
    const normalizedDate = normalizeScheduleDate(entry.Date);
    if (normalizedDate && normalizedDate < todayISO) {
      pastEntries.push(entry);
      return;
    }

    currentAndFutureEntries.push(entry);
  });

  const appendEntryRow = (entry, body) => {
    const row = document.createElement("tr");
    row.dataset.date = entry.Date;
    row.dataset.weekday = entry.Weekday;
    row.dataset.description = entry.Description;
    row.dataset.classId = `${entry.Grade}${entry.Section}`;
    if (entry.Summary) {
      row.dataset.summary = entry.Summary;
      row.dataset.title = entry.Summary;
    }

    const classCell = document.createElement("th");
    classCell.scope = "row";
    classCell.textContent = entry["Class #"];

    const dateCell = document.createElement("td");
    dateCell.textContent = formatScheduleDate(entry.Date);

    const weekdayCell = document.createElement("td");
    weekdayCell.textContent = entry.Weekday;

    const dayCell = document.createElement("td");
    dayCell.textContent = entry.Day;

    const descriptionCell = document.createElement("td");
    descriptionCell.textContent = entry.Description;

    const materialCell = document.createElement("td");
    materialCell.textContent = entry.Material || "";

    row.append(
      classCell,
      dateCell,
      weekdayCell,
      dayCell,
      descriptionCell,
      materialCell
    );

    body.append(row);
    return row;
  };

  if (pastEntries.length > 0) {
    const sectionId = `${table.dataset.grade || "class"}-${table.dataset.section || "section"}-past-dates`;
    const toggleRow = document.createElement("tr");
    toggleRow.className = "past-dates-toggle-row";

    const toggleCell = document.createElement("td");
    toggleCell.colSpan = getColumnCount(table);

    const toggleButton = document.createElement("button");
    toggleButton.type = "button";
    toggleButton.className = "past-dates-toggle";
    toggleButton.setAttribute("aria-expanded", "false");
    toggleButton.setAttribute("aria-controls", sectionId);

    const label = document.createElement("span");
    label.className = "toggle-label";
    label.textContent = "Past dates";

    const icon = document.createElement("span");
    icon.className = "toggle-icon";
    icon.setAttribute("aria-hidden", "true");
    icon.textContent = "+";

    toggleButton.append(label, icon);

    toggleCell.append(toggleButton);
    toggleRow.append(toggleCell);
    mainBody.append(toggleRow);

    const pastRows = pastEntries.map((entry, index) => {
      const row = appendEntryRow(entry, mainBody);
      if (index === 0) {
        row.id = sectionId;
      }
      row.hidden = true;
      return row;
    });

    toggleButton.addEventListener("click", () => {
      const isExpanded = toggleButton.getAttribute("aria-expanded") === "true";
      const nextExpanded = !isExpanded;
      toggleButton.setAttribute("aria-expanded", nextExpanded ? "true" : "false");
      icon.textContent = nextExpanded ? "−" : "+";
      pastRows.forEach((row) => {
        row.hidden = !nextExpanded;
      });
    });
  }

  currentAndFutureEntries.forEach((entry) => appendEntryRow(entry, mainBody));

  if (mainBody.rows.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = getColumnCount(table);
    cell.textContent = "No current or upcoming entries.";
    row.append(cell);
    mainBody.append(row);
  }
};

const renderClassScheduleTable = ({ grade, section, tableEl }) => {
  if (!grade || !section || !tableEl) {
    return;
  }

  getScheduleData()
    .then((data) => {
      const matches = data.filter(
        (entry) =>
          String(entry.Grade) === String(grade) &&
          String(entry.Section) === String(section)
      );

      if (matches.length === 0) {
        renderEmptyRow(tableEl);
      } else {
        renderScheduleRows(tableEl, matches);
      }

      tableEl.dataset.rendered = "true";
      document.dispatchEvent(
        new CustomEvent("class-schedule-rendered", {
          detail: { table: tableEl },
        })
      );
    })
    .catch(() => {
      renderEmptyRow(tableEl);
    });
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".class-schedule-table").forEach((table) => {
    renderClassScheduleTable({
      grade: table.dataset.grade,
      section: table.dataset.section,
      tableEl: table,
    });
  });
});
