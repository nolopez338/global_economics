"use strict";
function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = "";
  let quoted = false;

  for (let index = 0; index < text.length; index++) {
    const character = text[index];
    if (quoted && character === '"' && text[index + 1] === '"') {
      value += '"';
      index++;
    } else if (character === '"') {
      quoted = !quoted;
    } else if (!quoted && character === ",") {
      row.push(value);
      value = "";
    } else if (!quoted && (character === "\n" || character === "\r")) {
      if (character === "\r" && text[index + 1] === "\n") index++;
      row.push(value);
      if (row.some(cell => cell !== "")) rows.push(row);
      row = [];
      value = "";
    } else {
      value += character;
    }
  }
  if (quoted) throw new Error("CSV contains an unterminated quoted field");
  if (value || row.length) {
    row.push(value);
    rows.push(row);
  }
  return rows;
}

function stringifyCsv(rows) {
  return rows.map(row => row.map(value => {
    const s = value == null ? "" : String(value);
    return /[",\r\n]/.test(s) ? '"' + s.replaceAll('"', '""') + '"' : s;
  }).join(",")).join("\n") + "\n";
}
module.exports = { parseCsv, stringifyCsv };
