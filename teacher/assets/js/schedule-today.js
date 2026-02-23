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

const normalizeDateString = (raw) => {
  if (!raw) {
    return null;
  }

  const match = raw.trim().match(/^(\d{4})[-\/](\d{2})[-\/](\d{2})$/);
  if (!match) {
    return null;
  }

  const [, year, month, day] = match;
  return `${year}-${month}-${day}`;
};

const applyTodayMarker = (table) => {
  const body = table.tBodies[0];
  if (!body) {
    return;
  }

  body.querySelectorAll(".today-indicator-row").forEach((row) => row.remove());
  body.querySelectorAll(".today-row").forEach((row) => row.classList.remove("today-row"));

  const rows = Array.from(body.rows);
  if (rows.length === 0) {
    return;
  }

  const headerCells = Array.from(table.tHead?.rows[0]?.cells ?? []);
  const detectedDateColumnIndex = headerCells.findIndex(
    (cell) => cell.textContent.trim().toLowerCase() === "date"
  );
  const dateColumnIndex = detectedDateColumnIndex >= 0 ? detectedDateColumnIndex : 1;

  // Compute today in local time using ISO format for reliable comparison.
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, "0");
  const dd = String(today.getDate()).padStart(2, "0");
  const todayISO = `${yyyy}-${mm}-${dd}`;

  const columnCount =
    table.tHead?.rows[0]?.cells.length ?? rows[0]?.cells.length ?? 1;

  let hasParseableDate = false;
  let firstGreaterDateRow = null;

  for (const row of rows) {
    const dateCell = row.cells[dateColumnIndex];
    if (!dateCell) {
      continue;
    }

    const rowDateNormalized = normalizeDateString(dateCell.textContent);
    if (!rowDateNormalized) {
      continue;
    }

    hasParseableDate = true;

    if (rowDateNormalized === todayISO) {
      row.classList.add("today-row");
      return;
    }

    if (!firstGreaterDateRow && rowDateNormalized > todayISO) {
      firstGreaterDateRow = row;
    }
  }

  if (!hasParseableDate) {
    return;
  }

  const todayRow = buildTodayIndicatorRow(columnCount);
  if (firstGreaterDateRow) {
    body.insertBefore(todayRow, firstGreaterDateRow);
    return;
  }

  body.append(todayRow);
};

const applyTodayMarkers = () => {
  document
    .querySelectorAll(".class-schedule-table")
    .forEach((table) => applyTodayMarker(table));
};

document.addEventListener("class-schedule-rendered", (event) => {
  const table = event.detail?.table;
  if (table) {
    applyTodayMarker(table);
  }
});

document.addEventListener("DOMContentLoaded", () => {
  applyTodayMarkers();
});
