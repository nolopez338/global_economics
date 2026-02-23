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
  const body = table.tBodies[0] ?? table.createTBody();
  body.innerHTML = "";

  entries.forEach((entry) => {
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
  });
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
