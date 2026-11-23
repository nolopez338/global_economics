"use strict";
const calendar = require("../assets/js/databases/year-calendar-data.js");
const meetingDays = {
  "10A": [1, 3], "10B": [3, 4], "10C": [1, 5], "10D": [4, 6], "10E": [1, 5],
  "10Seminar": [4],
  "11A": [1, 3], "11B": [2, 3], "11C": [1, 6], "11D": [3, 5], "11E": [1, 6]
};
const weekdayNames = {
  mo: "Monday", tu: "Tuesday", we: "Wednesday", th: "Thursday",
  fr: "Friday", sa: "Saturday", su: "Sunday"
};


function validateCalendar(records) {
  const fail = message => { throw new Error(`schedule.csv: ${message}`); };
  const expectedKeys = new Set();
  for (const [classId, days] of Object.entries(meetingDays)) {
    for (const yearData of Object.values(calendar.cycleDayRegistry)) {
      for (const monthData of yearData.months) {
        const calendarMonth = calendar.calendarRegistry[yearData.year].months.find(item => item.month === monthData.month);
        monthData.weeks.forEach((week, weekIndex) => week.forEach((cycleDay, weekdayIndex) => {
          if (!days.includes(cycleDay)) return;
          const day = calendarMonth.weeks[weekIndex][weekdayIndex];
          const isoDate = `${yearData.year}-${String(monthData.month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
          expectedKeys.add(`${classId}|${isoDate}`);
        }));
      }
    }
  }

  const actualKeys = new Set();
  for (const [index, record] of records.entries()) {
    const rowNumber = index + 2;
    const classId = `${record.Grade}${record.Section}`;
    const days = meetingDays[classId];
    if (!days) fail(`row ${rowNumber} has unsupported class ${classId}`);
    const dateMatch = /^(\d{4}) \/ (\d{2}) \/ (\d{2})$/.exec(record.Date);
    if (!dateMatch) fail(`row ${rowNumber} has invalid Date format`);
    const isoDate = `${dateMatch[1]}-${dateMatch[2]}-${dateMatch[3]}`;
    const info = calendar.getAcademicDateInfo(isoDate);
    const meetingNumber = days.indexOf(info.cycleDay) + 1;
    if (!meetingNumber) fail(`row ${rowNumber} is not a meeting day for ${classId}`);
    const expectedClassNumber = `${info.cycleNumber}-${meetingNumber}`;
    const expectedTerm = info.term === null ? null : Number(info.term.slice(-1));
    if (record["Class #"] !== expectedClassNumber) fail(`row ${rowNumber} Class # must be ${expectedClassNumber}`);
    if (record.Term !== expectedTerm) fail(`row ${rowNumber} Term must be ${expectedTerm}`);
    if (record.Weekday !== weekdayNames[info.weekday]) fail(`row ${rowNumber} Weekday is incorrect`);
    if (record.Day !== info.cycleDay) fail(`row ${rowNumber} Day must be ${info.cycleDay}`);

    const key = `${classId}|${isoDate}`;
    if (actualKeys.has(key)) fail(`row ${rowNumber} duplicates ${key}`);
    actualKeys.add(key);
  }

  const missing = [...expectedKeys].filter(key => !actualKeys.has(key));
  const unexpected = [...actualKeys].filter(key => !expectedKeys.has(key));
  if (missing.length || unexpected.length) {
    fail(`meeting coverage differs (missing ${missing.length}, unexpected ${unexpected.length})`);
  }

  const sorted = [...records].sort((left, right) =>
    left.Grade - right.Grade || left.Section.localeCompare(right.Section) || left.Date.localeCompare(right.Date)
  );
  if (JSON.stringify(records) !== JSON.stringify(sorted)) fail("records are not ordered by grade, section, and date");

}
module.exports = validateCalendar;
