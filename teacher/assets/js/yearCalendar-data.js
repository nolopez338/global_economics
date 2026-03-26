const MONTH_NAMES = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
];

const WEEKDAY_NAMES = [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday'
];

function pad2(value) {
  return String(value).padStart(2, '0');
}

function getDayOfYear(date) {
  const startOfYear = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
  const diffInMs = date.getTime() - startOfYear.getTime();
  return Math.floor(diffInMs / 86400000) + 1;
}

function getISOWeekNumber(date) {
  const target = new Date(Date.UTC(
    date.getUTCFullYear(),
    date.getUTCMonth(),
    date.getUTCDate()
  ));

  const isoWeekday = target.getUTCDay() === 0 ? 7 : target.getUTCDay();
  target.setUTCDate(target.getUTCDate() + 4 - isoWeekday);

  const isoYearStart = new Date(Date.UTC(target.getUTCFullYear(), 0, 1));
  const diffInDays = Math.floor((target.getTime() - isoYearStart.getTime()) / 86400000);

  return Math.floor(diffInDays / 7) + 1;
}

function createCalendar2026() {
  const data = [];
  const current = new Date(Date.UTC(2026, 0, 1));
  const end = new Date(Date.UTC(2026, 11, 31));

  while (current <= end) {
    const year = current.getUTCFullYear();
    const month = current.getUTCMonth() + 1;
    const day = current.getUTCDate();
    const jsWeekday = current.getUTCDay();
    const weekday = jsWeekday === 0 ? 7 : jsWeekday;

    data.push({
      date: `${year}-${pad2(month)}-${pad2(day)}`,
      year,
      month,
      monthName: MONTH_NAMES[month - 1],
      day,
      weekday,
      weekdayName: WEEKDAY_NAMES[jsWeekday],
      dayOfYear: getDayOfYear(current),
      weekOfYear: getISOWeekNumber(current),
      quarter: Math.ceil(month / 3),
      semester: month <= 6 ? 1 : 2,
      isWeekend: weekday >= 6
    });

    current.setUTCDate(current.getUTCDate() + 1);
  }

  return data;
}

const calendar2026 = createCalendar2026();

export { calendar2026 };
export default calendar2026;