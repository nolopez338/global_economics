const formatScheduleDate = (value) => {
  const normalizedDate = normalizeScheduleDate(value);
  if (!normalizedDate) {
    return value;
  }

  const [year, month, day] = normalizedDate.split("-");
  return `${year} / ${month} / ${day}`;
};

const getScheduleData = () => {
  if (Array.isArray(window.SCHEDULE_DATA)) {
    return Promise.resolve(window.SCHEDULE_DATA);
  }

  return Promise.resolve([]);
};

const normalizeOrigin = (origin) =>
  origin === "schedule-teacher" ? "schedule-teacher" : "schedule";

const isNonEmptyValue = (value) =>
  value !== undefined && value !== null && String(value).trim() !== "";

const getMaterialValue = (entry, origin) => {
  if (normalizeOrigin(origin) === "schedule-teacher") {
    if (isNonEmptyValue(entry["Material teacher"])) {
      return entry["Material teacher"];
    }
  }

  return entry.Material || "";
};

const getColumnCount = (table) =>
  table.tHead?.rows[0]?.cells.length ?? 1;

const normalizeScheduleDate = (raw) => {
  if (!raw) {
    return null;
  }

  const match = String(raw)
    .trim()
    .match(/^(\d{4})\s*(?:[-\/]|\s\/\s)\s*(\d{1,2})\s*(?:[-\/]|\s\/\s)\s*(\d{1,2})$/);
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
  const origin = normalizeOrigin(
    table.dataset.origin ||
      document.querySelector("#class-page")?.dataset.origin ||
      "schedule"
  );

  table.querySelectorAll("tbody").forEach((body) => body.remove());

  const mainBody = table.createTBody();

  const todayISO = getTodayISODate();
  const classifiedEntries = entries.map((entry) => {
    const normalizedDate = normalizeScheduleDate(entry.Date);
    return {
      entry,
      normalizedDate,
      isPast: Boolean(normalizedDate && normalizedDate < todayISO),
    };
  });

  const uniquePastDates = Array.from(
    new Set(
      classifiedEntries
        .filter((item) => item.isPast)
        .map((item) => item.normalizedDate)
    )
  ).sort();

  const olderPastDates = new Set(
    uniquePastDates.length > 2
      ? uniquePastDates.slice(0, uniquePastDates.length - 2)
      : []
  );

  const olderPastEntries = [];
  const visibleEntries = [];

  classifiedEntries.forEach((item) => {
    if (item.isPast && olderPastDates.has(item.normalizedDate)) {
      olderPastEntries.push(item.entry);
      return;
    }

    visibleEntries.push(item.entry);
  });

  const appendEntryRow = (entry, body) => {
    const row = document.createElement("tr");
    const material = getMaterialValue(entry, origin);
    row.dataset.date = entry.Date;
    row.dataset.weekday = entry.Weekday;
    row.dataset.description = entry.Description;
    row.dataset.material = material;
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
    materialCell.textContent = material;

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

  if (olderPastEntries.length > 0) {
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

    const pastRows = olderPastEntries.map((entry, index) => {
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

  visibleEntries.forEach((entry) => appendEntryRow(entry, mainBody));

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
