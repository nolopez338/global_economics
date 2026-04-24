/*
  Purpose:
  Defines the academic calendar structure used by the yearly calendar views.

  Responsibilities:
  - Provides month-by-month week matrices and weekday mapping for 2026
  - Supplies calendar metadata consumed by calendar rendering components
  - Acts as a static data source rather than executing page interaction logic
*/
const calendar2026days = {
  year: 2026,
  weekdays: ["su", "mo", "tu", "we", "th", "fr", "sa"],
  months: [
    {
      month: 1,
      name: "January",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, 3,    4,    5,    1,    null],
        [null, 2,    3,    4,    5,    1,    null],
        [null, 2,    3,    4,    5,    1,    null]
      ]
    },
    {
      month: 2,
      name: "February",
      weeks: [
        [null, 2, 3, 4, 5, 1, null],
        [null, 2, 3, 4, 5, 1, null],
        [null, 2, 3, 4, 5, 1, null],
        [null, 2, 3, 4, 5, 1, null]
      ]
    },
    {
      month: 3,
      name: "March",
      weeks: [
        [null, 2,    3,    4,    5,    1,    null],
        [null, 2,    3,    4,    5,    null, null],
        [null, 1,    2,    3,    4,    5,    null],
        [null, null, 1,    2,    3,    null, null],
        [null, null, null, null, null, null, null]
      ]
    },
    {
      month: 4,
      name: "April",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, 4,    5,    1,    2,    3,    null],
        [null, 4,    5,    1,    2,    3,    null],
        [null, 4,    5,    1,    2,    3,    null],
        [null, 4,    5,    1,    2,    null, null]
      ]
    },
    {
      month: 5,
      name: "May",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, 3,    4,    5,    1,    2,    null],
        [null, 3,    4,    5,    1,    null, null],
        [null, null, 2,    3,    4,    5,    null],
        [null, 1,    2,    3,    4,    5,    null],
        [null, null, null, null, null, null, null]
      ]
    },
    {
      month: 6,
      name: "June",
      weeks: [
        [null, 1,    2,    3,    4,    5,    null],
        [null, null, 1,    2,    3,    4,    null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null]
      ]
    },
    {
      month: 7,
      name: "July",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null]
      ]
    },
    {
      month: 8,
      name: "August",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null]
      ]
    },
    {
      month: 9,
      name: "September",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null]
      ]
    },
    {
      month: 10,
      name: "October",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null]
      ]
    },
    {
      month: 11,
      name: "November",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null]
      ]
    },
    {
      month: 12,
      name: "December",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null]
      ]
    }
  ]
};

const calendar2026cycle = (() => {
  const cycleMonths = calendar2026days.months.map(month => ({
    month: month.month,
    name: month.name,
    weeks: month.weeks.map(week => week.map(day => (day === null ? null : 0)))
  }));

  let currentCycle = 3;
  let previousCycleDay = null;

  for (let monthIndex = 0; monthIndex < calendar2026days.months.length; monthIndex++) {
    const month = calendar2026days.months[monthIndex];
    for (let weekIndex = 0; weekIndex < month.weeks.length; weekIndex++) {
      const week = month.weeks[weekIndex];
      for (let weekdayIndex = 0; weekdayIndex < week.length; weekdayIndex++) {
        const cycleDay = week[weekdayIndex];

        if (cycleDay === null) {
          continue;
        }

        if (previousCycleDay === 5 && cycleDay === 1) {
          currentCycle = (currentCycle % 11) + 1;
        }

        cycleMonths[monthIndex].weeks[weekIndex][weekdayIndex] = currentCycle;
        previousCycleDay = cycleDay;
      }
    }
  }

  return {
    year: 2026,
    weekdays: ["su", "mo", "tu", "we", "th", "fr", "sa"],
    months: cycleMonths
  };
})();

const calendar2026 = {
  year: 2026,
  weekdays: ["su", "mo", "tu", "we", "th", "fr", "sa"],
  months: [
    {
      month: 1,
      name: "January",
      weeks: [
        [null, null, null, null, 1, 2, 3],
        [4, 5, 6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15, 16, 17],
        [18, 19, 20, 21, 22, 23, 24],
        [25, 26, 27, 28, 29, 30, 31]
      ]
    },
    {
      month: 2,
      name: "February",
      weeks: [
        [1, 2, 3, 4, 5, 6, 7],
        [8, 9, 10, 11, 12, 13, 14],
        [15, 16, 17, 18, 19, 20, 21],
        [22, 23, 24, 25, 26, 27, 28]
      ]
    },
    {
      month: 3,
      name: "March",
      weeks: [
        [1, 2, 3, 4, 5, 6, 7],
        [8, 9, 10, 11, 12, 13, 14],
        [15, 16, 17, 18, 19, 20, 21],
        [22, 23, 24, 25, 26, 27, 28],
        [29, 30, 31, null, null, null, null]
      ]
    },
    {
      month: 4,
      name: "April",
      weeks: [
        [null, null, null, 1, 2, 3, 4],
        [5, 6, 7, 8, 9, 10, 11],
        [12, 13, 14, 15, 16, 17, 18],
        [19, 20, 21, 22, 23, 24, 25],
        [26, 27, 28, 29, 30, null, null]
      ]
    },
    {
      month: 5,
      name: "May",
      weeks: [
        [null, null, null, null, null, 1, 2],
        [3, 4, 5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14, 15, 16],
        [17, 18, 19, 20, 21, 22, 23],
        [24, 25, 26, 27, 28, 29, 30],
        [31, null, null, null, null, null, null]
      ]
    },
    {
      month: 6,
      name: "June",
      weeks: [
        [null, 1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10, 11, 12, 13],
        [14, 15, 16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25, 26, 27],
        [28, 29, 30, null, null, null, null]
      ]
    },
    {
      month: 7,
      name: "July",
      weeks: [
        [null, null, null, 1, 2, 3, 4],
        [5, 6, 7, 8, 9, 10, 11],
        [12, 13, 14, 15, 16, 17, 18],
        [19, 20, 21, 22, 23, 24, 25],
        [26, 27, 28, 29, 30, 31, null]
      ]
    },
    {
      month: 8,
      name: "August",
      weeks: [
        [null, null, null, null, null, null, 1],
        [2, 3, 4, 5, 6, 7, 8],
        [9, 10, 11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20, 21, 22],
        [23, 24, 25, 26, 27, 28, 29],
        [30, 31, null, null, null, null, null]
      ]
    },
    {
      month: 9,
      name: "September",
      weeks: [
        [null, null, 1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10, 11, 12],
        [13, 14, 15, 16, 17, 18, 19],
        [20, 21, 22, 23, 24, 25, 26],
        [27, 28, 29, 30, null, null, null]
      ]
    },
    {
      month: 10,
      name: "October",
      weeks: [
        [null, null, null, null, 1, 2, 3],
        [4, 5, 6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15, 16, 17],
        [18, 19, 20, 21, 22, 23, 24],
        [25, 26, 27, 28, 29, 30, 31]
      ]
    },
    {
      month: 11,
      name: "November",
      weeks: [
        [1, 2, 3, 4, 5, 6, 7],
        [8, 9, 10, 11, 12, 13, 14],
        [15, 16, 17, 18, 19, 20, 21],
        [22, 23, 24, 25, 26, 27, 28],
        [29, 30, null, null, null, null, null]
      ]
    },
    {
      month: 12,
      name: "December",
      weeks: [
        [null, null, 1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10, 11, 12],
        [13, 14, 15, 16, 17, 18, 19],
        [20, 21, 22, 23, 24, 25, 26],
        [27, 28, 29, 30, 31, null, null]
      ]
    }
  ]
};

const holidays2026 = [
  { date: "2026-01-01", name: "Año Nuevo" },
  { date: "2026-01-06", name: "Reyes Magos" },
  { date: "2026-03-23", name: "San José" },
  { date: "2026-04-02", name: "Jueves Santo" },
  { date: "2026-04-03", name: "Viernes Santo" },
  { date: "2026-04-05", name: "Domingo de Resurrección" },
  { date: "2026-05-01", name: "Día del Trabajo" },
  { date: "2026-05-18", name: "Ascensión" },
  { date: "2026-06-08", name: "Corpus Christi" },
  { date: "2026-07-06", name: "San Pedro y San Pablo" },
  { date: "2026-07-20", name: "Independencia de Colombia" },
  { date: "2026-08-07", name: "Batalla de Boyacá" },
  { date: "2026-08-15", name: "Asunción de la Virgen" },
  { date: "2026-10-19", name: "Día de la Raza" },
  { date: "2026-11-01", name: "Todos los Santos" },
  { date: "2026-11-16", name: "Independencia de Cartagena" },
  { date: "2026-12-08", name: "Inmaculada Concepción" },
  { date: "2026-12-25", name: "Navidad" }
];

function getWeekday2026(month, day) {
  let monthData;

  if (typeof month === "number") {
    monthData = calendar2026.months.find(m => m.month === month);
  } else if (typeof month === "string") {
    const normalizedMonth = month.trim().toLowerCase();
    monthData = calendar2026.months.find(
      m => m.name.toLowerCase() === normalizedMonth
    );
  } else {
    throw new Error("Month must be a number or a string");
  }

  if (!monthData) {
    throw new Error("Invalid month");
  }

  for (const week of monthData.weeks) {
    const weekdayIndex = week.indexOf(day);
    if (weekdayIndex !== -1) {
      return calendar2026.weekdays[weekdayIndex];
    }
  }

  throw new Error("Invalid day for the given month");
}

function getCycleDay2026(month, day) {
  let monthData;
  let monthIndex;

  if (typeof month === "number") {
    monthIndex = calendar2026.months.findIndex(m => m.month === month);
    monthData = calendar2026.months[monthIndex];
  } else if (typeof month === "string") {
    const normalizedMonth = month.trim().toLowerCase();
    monthIndex = calendar2026.months.findIndex(
      m => m.name.toLowerCase() === normalizedMonth
    );
    monthData = calendar2026.months[monthIndex];
  } else {
    throw new Error("Month must be a number or a string");
  }

  if (!monthData) {
    throw new Error("Invalid month");
  }

  for (let weekIndex = 0; weekIndex < monthData.weeks.length; weekIndex++) {
    const weekdayIndex = monthData.weeks[weekIndex].indexOf(day);
    if (weekdayIndex !== -1) {
      return calendar2026days.months[monthIndex].weeks[weekIndex][weekdayIndex];
    }
  }

  throw new Error("Invalid day for the given month");
}

function getCycleNumber2026(month, day) {
  let monthData;
  let monthIndex;

  if (typeof month === "number") {
    monthIndex = calendar2026.months.findIndex(m => m.month === month);
    monthData = calendar2026.months[monthIndex];
  } else if (typeof month === "string") {
    const normalizedMonth = month.trim().toLowerCase();
    monthIndex = calendar2026.months.findIndex(
      m => m.name.toLowerCase() === normalizedMonth
    );
    monthData = calendar2026.months[monthIndex];
  } else {
    throw new Error("Month must be a number or a string");
  }

  if (!monthData) {
    throw new Error("Invalid month");
  }

  for (let weekIndex = 0; weekIndex < monthData.weeks.length; weekIndex++) {
    const weekdayIndex = monthData.weeks[weekIndex].indexOf(day);
    if (weekdayIndex !== -1) {
      return calendar2026cycle.months[monthIndex].weeks[weekIndex][weekdayIndex];
    }
  }

  throw new Error("Invalid day for the given month");
}


if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    calendar2026days,
    calendar2026cycle,
    calendar2026,
    holidays2026,
    getWeekday2026,
    getCycleDay2026,
    getCycleNumber2026
  };
}
