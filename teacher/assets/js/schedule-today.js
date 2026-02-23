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

  // Highlight the first matching date row.
  for (const row of rows) {
    const dateCell = row.cells[dateColumnIndex];
    if (!dateCell) {
      continue;
    }

    const rowDate = dateCell.textContent.trim();
    if (rowDate !== todayISO) {
      continue;
    }

    row.classList.add("today-row");
    return;
  }

  const columnCount =
    table.tHead?.rows[0]?.cells.length ?? rows[0]?.cells.length ?? 1;
  const todayRow = buildTodayIndicatorRow(columnCount);

  let insertionReferenceRow = null;
  for (const row of rows) {
    const dateCell = row.cells[dateColumnIndex];
    if (!dateCell) {
      continue;
    }

    const rowDate = dateCell.textContent.trim();
    if (rowDate > todayISO) {
      insertionReferenceRow = row;
      break;
    }
  }

  if (insertionReferenceRow) {
    body.insertBefore(todayRow, insertionReferenceRow);
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
