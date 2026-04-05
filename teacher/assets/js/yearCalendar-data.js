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

if (typeof module !== "undefined" && module.exports) {
  module.exports = { calendar2026, getWeekday2026 };
}