/*
 * Unified academic-calendar data and lookup utilities.
 *
 * A calendar year is the numbered January-to-December year stored in the
 * year-indexed registries below. The 2026-2027 academic year is a separate
 * interpretation spanning August 2026 through June 2027. Terms are inclusive
 * date ranges within that academic year. Cycle day is the scheduled day value
 * stored for a date; cycle number is generated chronologically across both
 * calendar years using the existing progression rule.
 */

const WEEKDAY_CODES = ["mo", "tu", "we", "th", "fr", "sa", "su"];

const MONTH_NAMES = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];

const calendar2026days = {
  year: 2026,
  weekdays: ["mo", "tu", "we", "th", "fr", "sa", "su"],
  months: [
    {
      month: 8,
      name: "August",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, 1, 2, 3, null, null],
        [null, 4, 5, 6, 1, null, null],
        [2, 3, 4, 5, 6, null, null],
        [1, null, null, null, null, null, null]
      ]
    },
    {
      month: 9,
      name: "September",
      weeks: [
        [null, 2, 3, 4, 5, null, null],
        [6, 1, 2, 3, 4, null, null],
        [5, 6, 1, 2, 3, null, null],
        [4, 5, 6, 1, 2, null, null],
        [3, 4, 5, null, null, null, null]
      ]
    },
    {
      month: 10,
      name: "October",
      weeks: [
        [null, null, null, 6, 1, null, null],
        [null, null, null, null, null, null, null],
        [null, 2, 3, 4, 5, null, null],
        [6, 1, 2, 3, 4, null, null],
        [5, 6, 1, 2, 3, null, null]
      ]
    },
    {
      month: 11,
      name: "November",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, 4, 5, 6, null, null, null],
        [1, 2, 3, 4, 5, null, null],
        [null, 6, 1, 2, null, null, null],
        [3, 4, 5, 6, 1, null, null],
        [2, null, null, null, null, null, null]
      ]
    },
    {
      month: 12,
      name: "December",
      weeks: [
        [null, 3, 4, 5, 6, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null]
      ]
    }
  ]
};

const calendar2027days = {
  year: 2027,
  weekdays: ["mo", "tu", "we", "th", "fr", "sa", "su"],
  months: [
    {
      month: 1,
      name: "January",
      weeks: [
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, 1, 2, 3, null, null],
        [4, 5, 6, 1, 2, null, null],
        [3, 4, 5, 6, 1, null, null]
      ]
    },
    {
      month: 2,
      name: "February",
      weeks: [
        [2, 3, 4, 5, 6, null, null],
        [1, 2, 3, 4, 5, null, null],
        [6, 1, 2, 3, 4, null, null],
        [5, 6, 1, 2, 3, null, null]
      ]
    },
    {
      month: 3,
      name: "March",
      weeks: [
        [4, 5, 6, 1, 2, null, null],
        [3, 4, 5, 6, null, null, null],
        [1, 2, 3, 4, 5, null, null],
        [null, null, null, null, null, null, null],
        [6, 1, 2, null, null, null, null]
      ]
    },
    {
      month: 4,
      name: "April",
      weeks: [
        [null, null, null, 3, null, null, null],
        [4, 5, 6, 1, 2, null, null],
        [3, 4, 5, 6, 1, null, null],
        [2, 3, 4, 5, 6, null, null],
        [1, 2, 3, 4, 5, null, null]
      ]
    },
    {
      month: 5,
      name: "May",
      weeks: [
        [null, null, null, null, null, null, null],
        [6, 1, 2, 3, 4, null, null],
        [null, 5, 6, 1, 2, null, null],
        [null, 3, 4, 5, 6, null, null],
        [1, 2, 3, 4, 5, null, null],
        [null, null, null, null, null, null, null]
      ]
    },
    {
      month: 6,
      name: "June",
      weeks: [
        [null, 6, 1, 2, 3, null, null],
        [null, 4, 5, 6, 1, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null]
      ]
    }
  ]
};

const calendar2026 = {
  year: 2026,
  weekdays: ["mo", "tu", "we", "th", "fr", "sa", "su"],
  months: [
    {
      month: 8,
      name: "August",
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
      month: 9,
      name: "September",
      weeks: [
        [null, 1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10, 11, 12, 13],
        [14, 15, 16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25, 26, 27],
        [28, 29, 30, null, null, null, null]
      ]
    },
    {
      month: 10,
      name: "October",
      weeks: [
        [null, null, null, 1, 2, 3, 4],
        [5, 6, 7, 8, 9, 10, 11],
        [12, 13, 14, 15, 16, 17, 18],
        [19, 20, 21, 22, 23, 24, 25],
        [26, 27, 28, 29, 30, 31, null]
      ]
    },
    {
      month: 11,
      name: "November",
      weeks: [
        [null, null, null, null, null, null, 1],
        [2, 3, 4, 5, 6, 7, 8],
        [9, 10, 11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20, 21, 22],
        [23, 24, 25, 26, 27, 28, 29],
        [30, null, null, null, null, null, null]
      ]
    },
    {
      month: 12,
      name: "December",
      weeks: [
        [null, 1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10, 11, 12, 13],
        [14, 15, 16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25, 26, 27],
        [28, 29, 30, 31, null, null, null]
      ]
    }
  ]
};

const holidays2026 = [
  { date: "2026-08-07", name: "Batalla de Boyacá" },
  { date: "2026-08-15", name: "Asunción de la Virgen" },
  { date: "2026-10-19", name: "Día de la Raza" },
  { date: "2026-11-01", name: "Todos los Santos" },
  { date: "2026-11-16", name: "Independencia de Cartagena" },
  { date: "2026-12-08", name: "Inmaculada Concepción" },
  { date: "2026-12-25", name: "Navidad" }
];

const calendar2027 = {
  year: 2027,
  weekdays: ["mo", "tu", "we", "th", "fr", "sa", "su"],
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
    }
  ]
};

const holidays2027 = [
  { date: "2027-01-01", name: "Año Nuevo" },
  { date: "2027-01-11", name: "Reyes Magos" },
  { date: "2027-03-22", name: "San José" },
  { date: "2027-03-25", name: "Jueves Santo" },
  { date: "2027-03-26", name: "Viernes Santo" },
  { date: "2027-05-01", name: "Día del Trabajo" },
  { date: "2027-05-10", name: "Ascensión" },
  { date: "2027-05-31", name: "Corpus Christi" },
  { date: "2027-06-07", name: "Sagrado Corazón de Jesús" }
];

/*
 * Academic-year configuration uses month-level calendar boundaries. This does
 * not claim that August 1 or June 30 is an exact school start or end date.
 * Term boundaries, unlike the academic-year boundaries, are exact dates.
 */
const academicYearConfig = {
  academicYear: "2026-2027",
  firstMonth: { calendarYear: 2026, month: 8 },
  lastMonth: { calendarYear: 2027, month: 6 },
  terms: [
    {
      name: "Term 1",
      startDate: "2026-08-10",
      endDate: "2026-11-07"
    },
    {
      name: "Term 2",
      startDate: "2026-11-08",
      endDate: "2027-03-13"
    },
    {
      name: "Term 3",
      startDate: "2027-03-14",
      endDate: "2027-05-11"
    }
  ]
};

const academicYearRegistry = {
  [academicYearConfig.academicYear]: academicYearConfig
};

/* Calendar-year storage remains independent of academic-year interpretation. */
const calendarRegistry = {
  2026: calendar2026,
  2027: calendar2027
};

const cycleDayRegistry = {
  2026: calendar2026days,
  2027: calendar2027days
};

const holidayRegistry = {
  2026: holidays2026,
  2027: holidays2027
};

function formatDateParts(year, month, day) {
  return `${String(year).padStart(4, "0")}-${String(month).padStart(
    2,
    "0"
  )}-${String(day).padStart(2, "0")}`;
}

function assertCalendarYear(year) {
  if (!Number.isInteger(year)) {
    throw new TypeError("Calendar year must be an integer");
  }
}

function assertValidDateParts(year, month, day) {
  if (
    !Number.isInteger(year) ||
    !Number.isInteger(month) ||
    !Number.isInteger(day)
  ) {
    throw new TypeError("Calendar year, month, and day must be integers");
  }

  const candidate = new Date(0);
  candidate.setUTCHours(0, 0, 0, 0);
  candidate.setUTCFullYear(year, month - 1, day);

  if (
    month < 1 ||
    month > 12 ||
    day < 1 ||
    candidate.getUTCFullYear() !== year ||
    candidate.getUTCMonth() + 1 !== month ||
    candidate.getUTCDate() !== day
  ) {
    throw new RangeError(
      `Invalid calendar date: ${formatDateParts(year, month, day)}`
    );
  }
}

function parseDateInput(date) {
  if (typeof date === "string") {
    const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(date);

    if (!match) {
      throw new TypeError("Date string must use the YYYY-MM-DD format");
    }

    const calendarYear = Number(match[1]);
    const month = Number(match[2]);
    const day = Number(match[3]);

    assertValidDateParts(calendarYear, month, day);

    return {
      normalizedDate: formatDateParts(calendarYear, month, day),
      calendarYear,
      month,
      day
    };
  }

  if (date instanceof Date) {
    if (Number.isNaN(date.getTime())) {
      throw new RangeError("Invalid Date object");
    }

    /*
     * Date objects use UTC fields so construction from an ISO date-only string
     * cannot shift the resulting calendar date.
     */
    const calendarYear = date.getUTCFullYear();
    const month = date.getUTCMonth() + 1;
    const day = date.getUTCDate();

    return {
      normalizedDate: formatDateParts(calendarYear, month, day),
      calendarYear,
      month,
      day
    };
  }

  throw new TypeError("Date must be a YYYY-MM-DD string or a Date object");
}

function normalizeDate(date) {
  return parseDateInput(date).normalizedDate;
}

function resolveMonthNumber(month) {
  if (typeof month === "number") {
    if (!Number.isInteger(month) || month < 1 || month > 12) {
      throw new RangeError("Month must be an integer from 1 through 12");
    }

    return month;
  }

  if (typeof month === "string") {
    const normalizedMonth = month.trim().toLowerCase();
    const monthIndex = MONTH_NAMES.findIndex(
      monthName => monthName.toLowerCase() === normalizedMonth
    );

    if (monthIndex === -1) {
      throw new RangeError(`Unknown month name: ${month}`);
    }

    return monthIndex + 1;
  }

  throw new TypeError("Month must be a number or an English month name");
}

function getCalendarData(year) {
  assertCalendarYear(year);

  const calendarData = calendarRegistry[year];

  if (!calendarData) {
    throw new RangeError(`Unsupported calendar year: ${year}`);
  }

  return calendarData;
}

function getMonthData(year, month) {
  const calendarData = getCalendarData(year);
  const monthNumber = resolveMonthNumber(month);
  const monthIndex = calendarData.months.findIndex(
    monthData => monthData.month === monthNumber
  );

  if (monthIndex === -1) {
    throw new RangeError(
      `Calendar data unavailable for ${year}-${String(monthNumber).padStart(
        2,
        "0"
      )} (${MONTH_NAMES[monthNumber - 1]})`
    );
  }

  return {
    monthIndex,
    monthData: calendarData.months[monthIndex]
  };
}

function getDatePosition(year, month, day) {
  assertCalendarYear(year);

  const monthNumber = resolveMonthNumber(month);

  assertValidDateParts(year, monthNumber, day);

  const { monthIndex, monthData } = getMonthData(year, monthNumber);

  for (let weekIndex = 0; weekIndex < monthData.weeks.length; weekIndex++) {
    const weekdayIndex = monthData.weeks[weekIndex].indexOf(day);

    if (weekdayIndex !== -1) {
      return {
        monthIndex,
        weekIndex,
        weekdayIndex
      };
    }
  }

  throw new RangeError(
    `Calendar position unavailable for ${formatDateParts(
      year,
      monthNumber,
      day
    )}`
  );
}

function getWeekday(year, month, day) {
  const { weekdayIndex } = getDatePosition(year, month, day);

  return getCalendarData(year).weekdays[weekdayIndex];
}

function getAcademicYearConfig(academicYear) {
  if (typeof academicYear !== "string" || !academicYear.trim()) {
    throw new TypeError("Academic year must be a non-empty string");
  }

  const config = academicYearRegistry[academicYear];

  if (!config) {
    throw new RangeError(`Unknown academic year: ${academicYear}`);
  }

  return config;
}

function getAcademicMonthSequence(config) {
  const sequence = [];

  let calendarYear = config.firstMonth.calendarYear;
  let month = config.firstMonth.month;

  const finalValue =
    config.lastMonth.calendarYear * 12 + config.lastMonth.month;

  while (calendarYear * 12 + month <= finalValue) {
    sequence.push({ calendarYear, month });

    month++;

    if (month === 13) {
      calendarYear++;
      month = 1;
    }
  }

  return sequence;
}

function generateAcademicCycleNumbers(config) {
  const generatedRegistry = {};

  let currentCycle = 1;
  let previousCycleDay = null;

  for (const { calendarYear, month } of getAcademicMonthSequence(config)) {
    const calendarData = calendarRegistry[calendarYear];
    const cycleDayData = cycleDayRegistry[calendarYear];

    if (!calendarData || !cycleDayData) {
      throw new Error(
        `Missing registered calendar or cycle-day data for ${calendarYear}`
      );
    }

    const calendarMonth = calendarData.months.find(
      item => item.month === month
    );

    const cycleDayMonth = cycleDayData.months.find(
      item => item.month === month
    );

    if (!calendarMonth || !cycleDayMonth) {
      throw new Error(
        `Missing registered calendar or cycle-day month for ${calendarYear}-${String(
          month
        ).padStart(2, "0")}`
      );
    }

    if (!generatedRegistry[calendarYear]) {
      generatedRegistry[calendarYear] = {
        year: calendarYear,
        weekdays: calendarData.weekdays.slice(),
        months: []
      };
    }

    const generatedMonth = {
      month: cycleDayMonth.month,
      name: cycleDayMonth.name,
      weeks: cycleDayMonth.weeks.map(week => week.map(() => null))
    };

    for (
      let weekIndex = 0;
      weekIndex < cycleDayMonth.weeks.length;
      weekIndex++
    ) {
      const week = cycleDayMonth.weeks[weekIndex];

      if (
        !calendarMonth.weeks[weekIndex] ||
        calendarMonth.weeks[weekIndex].length !== week.length
      ) {
        throw new Error(
          `Calendar and cycle-day matrices are misaligned for ${calendarYear}-${String(
            month
          ).padStart(2, "0")}`
        );
      }

      for (
        let weekdayIndex = 0;
        weekdayIndex < week.length;
        weekdayIndex++
      ) {
        const cycleDay = week[weekdayIndex];

        if (cycleDay === null) {
          continue;
        }

        /*
         * Preserve the established progression rule and the cycle-number
         * sequence from 1 through 11.
         */
        if (previousCycleDay === 5 && cycleDay === 1) {
          currentCycle = (currentCycle % 11) + 1;
        }

        generatedMonth.weeks[weekIndex][weekdayIndex] = currentCycle;
        previousCycleDay = cycleDay;
      }
    }

    generatedRegistry[calendarYear].months.push(generatedMonth);
  }

  return generatedRegistry;
}

/*
 * Cycle numbers are generated once in chronological academic-year order:
 * August–December 2026 followed by January–June 2027.
 */
const cycleNumberRegistry = generateAcademicCycleNumbers(academicYearConfig);

const calendar2026cycle = cycleNumberRegistry[2026];
const calendar2027cycle = cycleNumberRegistry[2027];

function getRegisteredMatrixValue(
  registry,
  year,
  month,
  day,
  dataLabel
) {
  const monthNumber = resolveMonthNumber(month);
  const { weekIndex, weekdayIndex } = getDatePosition(
    year,
    monthNumber,
    day
  );

  const yearData = registry[year];

  if (!yearData) {
    throw new RangeError(
      `${dataLabel} data unavailable for calendar year ${year}`
    );
  }

  const monthData = yearData.months.find(
    item => item.month === monthNumber
  );

  if (!monthData) {
    throw new RangeError(
      `${dataLabel} data unavailable for ${year}-${String(
        monthNumber
      ).padStart(2, "0")}`
    );
  }

  if (
    !monthData.weeks[weekIndex] ||
    weekdayIndex >= monthData.weeks[weekIndex].length
  ) {
    throw new Error(
      `${dataLabel} matrix is misaligned for ${formatDateParts(
        year,
        monthNumber,
        day
      )}`
    );
  }

  return monthData.weeks[weekIndex][weekdayIndex];
}

function getCycleDay(year, month, day) {
  return getRegisteredMatrixValue(
    cycleDayRegistry,
    year,
    month,
    day,
    "Cycle-day"
  );
}

function getCycleNumber(year, month, day) {
  return getRegisteredMatrixValue(
    cycleNumberRegistry,
    year,
    month,
    day,
    "Cycle-number"
  );
}

function getAcademicMonthData(academicYear, month, calendarYear) {
  const config = getAcademicYearConfig(academicYear);
  const monthNumber = resolveMonthNumber(month);

  if (calendarYear !== undefined) {
    assertCalendarYear(calendarYear);
  }

  const matchingMonths = getAcademicMonthSequence(config).filter(
    item =>
      item.month === monthNumber &&
      (calendarYear === undefined || item.calendarYear === calendarYear)
  );

  if (matchingMonths.length === 0) {
    const yearDescription =
      calendarYear === undefined ? "" : ` in ${calendarYear}`;

    throw new RangeError(
      `${MONTH_NAMES[monthNumber - 1]}${yearDescription} is not part of academic year ${academicYear}`
    );
  }

  if (matchingMonths.length > 1) {
    throw new RangeError(
      `Calendar year is required to disambiguate ${
        MONTH_NAMES[monthNumber - 1]
      } in academic year ${academicYear}`
    );
  }

  const selected = matchingMonths[0];

  const { monthIndex, monthData } = getMonthData(
    selected.calendarYear,
    selected.month
  );

  return {
    academicYear,
    calendarYear: selected.calendarYear,
    monthIndex,
    monthData
  };
}

function findAcademicYearConfig(calendarYear, month) {
  const value = calendarYear * 12 + month;

  return (
    Object.values(academicYearRegistry).find(config => {
      const firstValue =
        config.firstMonth.calendarYear * 12 + config.firstMonth.month;

      const lastValue =
        config.lastMonth.calendarYear * 12 + config.lastMonth.month;

      return value >= firstValue && value <= lastValue;
    }) || null
  );
}

function getAcademicYear(date) {
  const { calendarYear, month } = parseDateInput(date);
  const config = findAcademicYearConfig(calendarYear, month);

  return config ? config.academicYear : null;
}

function isDateInAcademicYear(date) {
  return getAcademicYear(date) !== null;
}

function getTerm(date) {
  const {
    normalizedDate,
    calendarYear,
    month
  } = parseDateInput(date);

  const config = findAcademicYearConfig(calendarYear, month);

  if (!config) {
    return null;
  }

  const term = config.terms.find(
    item =>
      normalizedDate >= item.startDate &&
      normalizedDate <= item.endDate
  );

  return term ? term.name : null;
}

function getHolidayForDate(normalizedDate, calendarYear) {
  const holidays = holidayRegistry[calendarYear];

  return holidays
    ? holidays.find(item => item.date === normalizedDate) || null
    : null;
}

function getWeekdayFromDateParts(calendarYear, month, day) {
  const candidate = new Date(0);

  candidate.setUTCHours(0, 0, 0, 0);
  candidate.setUTCFullYear(calendarYear, month - 1, day);

  return WEEKDAY_CODES[(candidate.getUTCDay() + 6) % 7];
}

function hasRegisteredMonth(registry, calendarYear, month) {
  return Boolean(
    registry[calendarYear] &&
      registry[calendarYear].months.some(item => item.month === month)
  );
}

function getAcademicDateInfo(date) {
  const {
    normalizedDate,
    calendarYear,
    month,
    day
  } = parseDateInput(date);

  const config = findAcademicYearConfig(calendarYear, month);

  const hasCalendarMonth = hasRegisteredMonth(
    calendarRegistry,
    calendarYear,
    month
  );

  const hasCycleDayMonth = hasRegisteredMonth(
    cycleDayRegistry,
    calendarYear,
    month
  );

  const hasCycleNumberMonth = hasRegisteredMonth(
    cycleNumberRegistry,
    calendarYear,
    month
  );

  const holiday = getHolidayForDate(normalizedDate, calendarYear);

  const hasHolidayData = Object.prototype.hasOwnProperty.call(
    holidayRegistry,
    calendarYear
  );

  return {
    normalizedDate,
    academicYear: config ? config.academicYear : null,
    calendarYear,
    month,
    day,
    weekday: hasCalendarMonth
      ? getWeekday(calendarYear, month, day)
      : getWeekdayFromDateParts(calendarYear, month, day),
    term: getTerm(normalizedDate),
    cycleDay:
      hasCalendarMonth && hasCycleDayMonth
        ? getCycleDay(calendarYear, month, day)
        : null,
    cycleNumber:
      hasCalendarMonth && hasCycleNumberMonth
        ? getCycleNumber(calendarYear, month, day)
        : null,
    isHoliday: hasHolidayData ? holiday !== null : null,
    holiday: holiday ? { ...holiday } : null
  };
}

/*
 * Thin compatibility wrappers preserve existing 2026 browser and CommonJS
 * consumers while delegating all lookup logic to the generic functions.
 */
function getMonthData2026(month) {
  return getMonthData(2026, month);
}

function getDatePosition2026(month, day) {
  return getDatePosition(2026, month, day);
}

function getWeekday2026(month, day) {
  return getWeekday(2026, month, day);
}

function getCycleDay2026(month, day) {
  return getCycleDay(2026, month, day);
}

function getCycleNumber2026(month, day) {
  return getCycleNumber(2026, month, day);
}

const academicCalendarExports = {
  academicYearConfig,
  academicYearRegistry,
  calendarRegistry,
  cycleDayRegistry,
  cycleNumberRegistry,
  holidayRegistry,

  calendar2026days,
  calendar2027days,
  calendar2026cycle,
  calendar2027cycle,
  calendar2026,
  calendar2027,
  holidays2026,
  holidays2027,

  normalizeDate,
  getCalendarData,
  getMonthData,
  getDatePosition,
  getWeekday,
  getCycleDay,
  getCycleNumber,
  getAcademicYear,
  isDateInAcademicYear,
  getTerm,
  getAcademicMonthData,
  getAcademicDateInfo,

  getMonthData2026,
  getDatePosition2026,
  getWeekday2026,
  getCycleDay2026,
  getCycleNumber2026
};

if (typeof window !== "undefined") {
  window.academicCalendar = academicCalendarExports;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = academicCalendarExports;
}