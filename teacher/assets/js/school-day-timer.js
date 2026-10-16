(function () {
  "use strict";
  function toMinutes(value) {
    const [hours, minutes] = value.split(":").map(Number);
    return hours * 60 + minutes;
  }
      const periods = [
        ["Contact", "06:45", "07:00"],
        ["1st Hour", "07:05", "07:55"],
        ["2nd Hour", "08:00", "08:50"],
        ["3rd Hour", "08:55", "09:45"],
        ["Break", "09:45", "10:15"],
        ["4th Hour", "10:15", "11:05"],
        ["5th Hour", "11:10", "12:00"],
        ["6th Hour", "12:05", "12:55"],
        ["Lunch", "12:55", "13:55"],
        ["7th Hour", "13:55", "14:45"],
        ["Pause", "14:45", "15:00"],
        ["Final Hour", "15:00", "16:00"]
      ].map(([name, startText, endText]) => ({
        name, startText, endText,
        start: toMinutes(startText),
        end: toMinutes(endText)
      }));
  function progress(start, end, nowMinutes) {
    return Math.max(0, Math.min(1, (nowMinutes - start) / (end - start)));
  }
  window.SchoolDayTimer = { periods, progress };
})();
