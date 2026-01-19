const parseScheduleDate = (text) => {
  if (!text) {
    return null;
  }

  const parts = text
    .split("/")
    .map((part) => part.trim())
    .filter(Boolean);

  if (parts.length < 3) {
    return null;
  }

  const [yearPart, dayPart, monthPart] = parts;
  const year = Number.parseInt(yearPart, 10);
  const day = Number.parseInt(dayPart, 10);
  const month = Number.parseInt(monthPart, 10);

  if (Number.isNaN(year) || Number.isNaN(day) || Number.isNaN(month)) {
    return null;
  }

  const date = new Date(year, month - 1, day);
  if (Number.isNaN(date.getTime())) {
    return null;
  }

  date.setHours(0, 0, 0, 0);
  return date;
};

const buildTodayIndicatorRow = (columnCount) => {
  const row = document.createElement("tr");
  row.className = "today-indicator-row";

  const cell = document.createElement("td");
  cell.colSpan = columnCount;

  const indicator = document.createElement("div");
  indicator.className = "today-indicator";

  const label = document.createElement("span");
  label.textContent = "Today";

  indicator.append(label);
  cell.append(indicator);
  row.append(cell);

  return row;
};

const applyTodayMarker = (table) => {
  const body = table.tBodies[0];
  if (!body) {
    return;
  }

  body.querySelectorAll(".today-indicator-row").forEach((row) => row.remove());
  body.querySelectorAll(".today-row").forEach((row) => row.classList.remove("today-row"));

  const rows = Array.from(body.rows);
  const dateRows = rows
    .map((row) => {
      const dateCell = row.querySelector("td:nth-child(2)");
      const date = parseScheduleDate(dateCell?.textContent ?? "");

      return date ? { row, date } : null;
    })
    .filter(Boolean);

  if (dateRows.length === 0) {
    return;
  }

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const todayRows = dateRows.filter(({ date }) => date.getTime() === today.getTime());
  if (todayRows.length > 0) {
    todayRows.forEach(({ row }) => row.classList.add("today-row"));
    return;
  }

  const futureRow = dateRows.find(({ date }) => date.getTime() > today.getTime());
  const columnCount =
    table.tHead?.rows[0]?.cells.length ?? rows[0]?.cells.length ?? 1;
  const indicatorRow = buildTodayIndicatorRow(columnCount);

  if (futureRow) {
    body.insertBefore(indicatorRow, futureRow.row);
    return;
  }

  body.append(indicatorRow);
};

document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll(".class-schedule-table")
    .forEach((table) => applyTodayMarker(table));
});
