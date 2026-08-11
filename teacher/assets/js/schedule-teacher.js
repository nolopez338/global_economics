/* Enhances the teacher's six-day schedule with calendar-driven state. */
(function () {
  const scheduleDays = Array.from(document.querySelectorAll(".rotation-day[data-cycle-day]"));
  const toggle = document.querySelector(".collapsible-toggle");
  const panel = document.getElementById("class-pages-panel");
  const icon = toggle?.querySelector(".collapsible-icon");
  let displayedLocalDate = null;

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
    const match = href && href.match(/^pages\/class_schedules\/(\d{2})([A-E])\.html$/i);
    if (match) {
      link.setAttribute(
        "href",
        `pages/class.html?grade=${match[1]}&section=${match[2].toUpperCase()}&mode=teacher&origin=schedule-teacher`
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

    scheduleDays.forEach((day) => {
      const isActive = Number(day.dataset.cycleDay) === cycleDay;
      day.classList.toggle("is-active", isActive);
      if (isActive) {
        day.setAttribute("aria-current", "date");
      } else {
        day.removeAttribute("aria-current");
      }
    });
  }

  function refreshAfterDateChange() {
    const now = new Date();
    if (formatLocalDate(now) !== displayedLocalDate) {
      updateActiveScheduleDay(now);
    }
  }

  updateActiveScheduleDay();
  window.setInterval(refreshAfterDateChange, 60000);
  document.addEventListener("visibilitychange", refreshAfterDateChange);
  window.addEventListener("focus", refreshAfterDateChange);

  window.updateTeacherScheduleDay = updateActiveScheduleDay;
})();
