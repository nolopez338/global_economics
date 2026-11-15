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
  function durationText(seconds) {
    const safe = Math.max(0, Math.ceil(seconds));
    const hours = Math.floor(safe / 3600);
    const minutes = Math.floor((safe % 3600) / 60);
    const remainder = safe % 60;
    return `${hours ? `${hours}:` : ""}${String(minutes).padStart(hours ? 2 : 1, "0")}:${String(remainder).padStart(2, "0")}`;
  }

  // Local date fields match the classroom clock, not the calendar's UTC Date API.
  function countdownAt(now, calendar = window.academicCalendar) {
    const dateKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;
    if (now.getDay() === 0 || now.getDay() === 6) {
      return { label: "Weekend · no school", remaining: "" };
    }
    let info;
    try {
      info = calendar?.getAcademicDateInfo(dateKey);
    } catch {
      // Missing or failed calendar lookups must never produce a countdown.
    }
    if (!info || info.isHoliday == null) {
      return { label: "Calendar unavailable", remaining: "" };
    }
    if (info.isHoliday) return { label: "School holiday", remaining: "" };
    if (!Number.isInteger(info.cycleDay) || info.cycleDay < 1 || info.cycleDay > 6) {
      return { label: "Not a school day", remaining: "" };
    }
    const minutes = now.getHours() * 60 + now.getMinutes() + now.getSeconds() / 60 + now.getMilliseconds() / 60000;
    const current = periods.find(period => minutes >= period.start && minutes < period.end);
    const upcoming = periods.find(period => minutes < period.start);
    if (current) {
      return { label: `${current.name} ends in`, remaining: durationText((current.end - minutes) * 60) };
    }
    if (upcoming) {
      return { label: `${upcoming.name} starts in`, remaining: durationText((upcoming.start - minutes) * 60) };
    }
    return { label: "School day ended", remaining: "" };
  }

  window.SchoolDayTimer = { periods, progress, durationText, countdownAt };
})();
