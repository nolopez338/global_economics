/* Enhances the teacher's six-day schedule with calendar-driven state. */
(function () {
  const scheduleTable = document.querySelector(".rotation-schedule table");
  const scheduleWrap = document.querySelector(".rotation-schedule .schedule-table-wrap");
  const currentTimeOverlay = scheduleWrap?.querySelector(".current-time-overlay");
  const currentTimeLine = currentTimeOverlay?.querySelector(".current-time-line");
  const currentTimeLabel = currentTimeLine?.querySelector(".current-time-label");
  const columnToggle = document.querySelector(".schedule-column-toggle");
  const mobileScheduleQuery = window.matchMedia("(max-width: 600px)");
  const toggle = document.querySelector(".collapsible-toggle");
  const panel = document.getElementById("class-pages-panel");
  const icon = toggle?.querySelector(".collapsible-icon");
  let displayedLocalDate = null;
  let activeCycleDay = null;
  let mobileScheduleExpanded = false;

  if (toggle && panel && icon) {
    toggle.addEventListener("click", () => {
      const isExpanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!isExpanded));
      panel.hidden = isExpanded;
      icon.textContent = isExpanded ? "+" : "−";
    });
  }

  document.querySelectorAll("a.class-card").forEach((link) => {
    const href = link.getAttribute("href");
    const match = href && href.match(/^pages\/class_schedules\/(\d{2})([A-E]|Seminars)\.html$/i);
    if (match) {
      const section = match[2].toLowerCase() === "seminars"
        ? "Seminar"
        : match[2].toUpperCase();
      link.setAttribute(
        "href",
        `pages/class.html?grade=${match[1]}&section=${section}&mode=teacher&origin=schedule-teacher`
      );
    }
  });

  function formatLocalDate(date) {
    return [
      date.getFullYear(),
      String(date.getMonth() + 1).padStart(2, "0"),
      String(date.getDate()).padStart(2, "0")
    ].join("-");
  }

  function updateActiveScheduleDay(now = new Date()) {
    const localDate = formatLocalDate(now);
    displayedLocalDate = localDate;
    let cycleDay = null;

    if (window.academicCalendar) {
      cycleDay = window.academicCalendar.getAcademicDateInfo(localDate).cycleDay;
    }

    if (!Number.isInteger(cycleDay) || cycleDay < 1 || cycleDay > 6) {
      cycleDay = null;
    }
    activeCycleDay = cycleDay;

    scheduleTable?.querySelectorAll("[data-cycle-day]").forEach((cell) => {
      const isActive = Number(cell.dataset.cycleDay) === cycleDay;
      const isDayHeader = cell.classList.contains("rotation-day");
      cell.classList.toggle("is-active-cycle-day", isActive);
      if (isActive && isDayHeader) {
        cell.setAttribute("aria-current", "date");
      } else {
        cell.removeAttribute("aria-current");
      }
    });
    updateMobileScheduleColumns();
  }

  function updateMobileScheduleColumns() {
    if (!scheduleTable || !columnToggle) {
      return;
    }

    const isMobile = mobileScheduleQuery.matches;
    const showCompleteSchedule = !isMobile || mobileScheduleExpanded;
    const visibleCycleDays = activeCycleDay === 6
      ? [1, 6]
      : [activeCycleDay ?? 1, activeCycleDay ? activeCycleDay + 1 : 2];

    scheduleTable.classList.toggle("is-mobile-collapsed", isMobile && !mobileScheduleExpanded);
    scheduleTable.classList.toggle("is-mobile-expanded", isMobile && mobileScheduleExpanded);
    scheduleTable.querySelectorAll("[data-cycle-day]").forEach((cell) => {
      cell.classList.toggle(
        "mobile-cycle-visible",
        visibleCycleDays.includes(Number(cell.dataset.cycleDay))
      );
    });

    columnToggle.setAttribute("aria-expanded", String(showCompleteSchedule));
    columnToggle.textContent = showCompleteSchedule
      ? "Mostrar horario reducido"
      : "Mostrar horario completo";
    window.requestAnimationFrame(() => updateCurrentTimeLine());
  }

  function assignCycleDayColumns() {
    if (!scheduleTable) {
      return;
    }

    const occupiedUntilRow = [];
    Array.from(scheduleTable.rows).forEach((row, rowIndex) => {
      let columnIndex = 0;
      Array.from(row.cells).forEach((cell) => {
        while ((occupiedUntilRow[columnIndex] ?? 0) > rowIndex) {
          columnIndex += 1;
        }

        if (columnIndex >= 1 && columnIndex <= 6) {
          cell.dataset.cycleDay = String(columnIndex);
        }

        const rowSpan = Math.max(1, cell.rowSpan || 1);
        const colSpan = Math.max(1, cell.colSpan || 1);
        for (let offset = 0; offset < colSpan; offset += 1) {
          occupiedUntilRow[columnIndex + offset] = rowIndex + rowSpan;
        }
        columnIndex += colSpan;
      });
    });
  }

  function parseTimeRange(text) {
    if (!text) {
      return null;
    }
    const [startText, endText] = text.split("-").map((part) => part.trim());
    const toMinutes = (value) => {
      const [hours, minutes] = value.split(":").map(Number);
      return Number.isFinite(hours) && Number.isFinite(minutes) ? hours * 60 + minutes : null;
    };
    const start = toMinutes(startText);
    const end = toMinutes(endText);
    return start !== null && end !== null && end > start ? { start, end } : null;
  }

  function updateCurrentTimeLine(now = new Date()) {
    if (!scheduleTable || !scheduleWrap || !currentTimeOverlay || !currentTimeLine) {
      return;
    }

    const nowMinutes = now.getHours() * 60 + now.getMinutes() + now.getSeconds() / 60;
    const rows = Array.from(scheduleTable.tBodies[0]?.rows ?? []);
    const intervals = rows.map((row) => {
      const timeCell = row.querySelector("th[scope='row']");
      return {
        row,
        timeCell,
        range: parseTimeRange(timeCell?.querySelector("time")?.textContent)
      };
    }).filter((interval) => interval.timeCell && interval.range);
    const matchingInterval = intervals.find(({ range }) => (
      nowMinutes >= range.start && nowMinutes <= range.end
    ));
    const gapIndex = matchingInterval ? -1 : intervals.findIndex(({ range }, index) => {
      const nextRange = intervals[index + 1]?.range;
      return nextRange && nowMinutes > range.end && nowMinutes < nextRange.start;
    });

    if (!matchingInterval && gapIndex === -1) {
      currentTimeOverlay.hidden = true;
      currentTimeLine.classList.remove("is-unshown-gap");
      return;
    }

    const wrapRect = scheduleWrap.getBoundingClientRect();
    const activeInterval = matchingInterval ?? intervals[gapIndex];
    const rowRect = activeInterval.row.getBoundingClientRect();
    const timeCellRect = activeInterval.timeCell.getBoundingClientRect();
    const leftOffset = timeCellRect.right - wrapRect.left;
    const isUnshownGap = gapIndex !== -1;
    const topOffset = isUnshownGap
      ? intervals[gapIndex + 1].row.getBoundingClientRect().top - wrapRect.top
      : rowRect.top - wrapRect.top
        + rowRect.height * ((nowMinutes - activeInterval.range.start)
          / (activeInterval.range.end - activeInterval.range.start));

    currentTimeOverlay.hidden = false;
    currentTimeLine.classList.toggle("is-unshown-gap", isUnshownGap);
    currentTimeLine.style.left = `${leftOffset}px`;
    currentTimeLine.style.width = `${wrapRect.width - leftOffset}px`;
    currentTimeLine.style.top = `${topOffset}px`;
    if (currentTimeLabel) {
      currentTimeLabel.textContent = now.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
      });
    }
  }

  function refreshAfterDateChange() {
    const now = new Date();
    if (formatLocalDate(now) !== displayedLocalDate) {
      updateActiveScheduleDay(now);
    }
  }

  assignCycleDayColumns();
  columnToggle?.addEventListener("click", () => {
    mobileScheduleExpanded = !mobileScheduleExpanded;
    updateMobileScheduleColumns();
  });
  mobileScheduleQuery.addEventListener("change", updateMobileScheduleColumns);
  updateActiveScheduleDay();
  updateCurrentTimeLine();
  window.setInterval(refreshAfterDateChange, 60000);
  window.setInterval(updateCurrentTimeLine, 30000);
  document.addEventListener("visibilitychange", refreshAfterDateChange);
  window.addEventListener("focus", refreshAfterDateChange);
  window.addEventListener("resize", updateCurrentTimeLine);

  window.updateTeacherScheduleDay = updateActiveScheduleDay;
  window.updateTeacherScheduleTime = updateCurrentTimeLine;
})();
