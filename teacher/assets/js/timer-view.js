(function () {
  "use strict";

  const page = document.getElementById("timer-page");
  if (!page) return;
  const { periods: schedule, progress: periodProgress } = window.SchoolDayTimer;
  const clock = page.querySelector("#live-clock");
  const dateLabel = page.querySelector("#current-date");
  const cycleLabel = page.querySelector("#cycle-label");
  const title = page.querySelector("#period-title");
  const range = page.querySelector("#period-range");
  const nextPeriod = page.querySelector("#next-period");
  const countdown = page.querySelector("#countdown");
  const visual = page.querySelector("#period-visual");
  const endLabel = page.querySelector("#period-end");
  const scheduleList = page.querySelector("#schedule-list");
  const fullscreenToggle = page.querySelector("#fullscreen-toggle");
  let lastDateKey = "";

  function localDateKey(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
  }

  function durationText(seconds) {
    const safe = Math.max(0, Math.ceil(seconds));
    const hours = Math.floor(safe / 3600);
    const minutes = Math.floor((safe % 3600) / 60);
    const remainder = safe % 60;
    return `${hours ? `${hours}:` : ""}${String(minutes).padStart(hours ? 2 : 1, "0")}:${String(remainder).padStart(2, "0")}`;
  }

  function renderSchedule() {
    schedule.forEach((period, index) => {
      const item = document.createElement("li");
      item.className = "schedule-item";
      item.dataset.periodIndex = String(index);
      const name = document.createElement("span");
      name.textContent = period.name;
      const time = document.createElement("time");
      time.textContent = `${period.startText}–${period.endText}`;
      item.append(name, time);
      scheduleList.append(item);
    });
  }

  function highlightPeriod(index) {
    scheduleList.querySelectorAll(".schedule-item").forEach((item, itemIndex) => {
      const active = itemIndex === index;
      item.classList.toggle("active", active);
      if (active) item.setAttribute("aria-current", "true");
      else item.removeAttribute("aria-current");
    });
  }

  function setPeriodState(name) {
    visual.classList.remove("period-between-classes", "period-recess", "period-lunch");
    let state = null;
    if (name === "Break" || name === "Pause") state = "recess";
    if (name === "Lunch") state = "lunch";
    if (state) visual.classList.add(`period-${state}`);
    visual.dataset.periodState = state || "general";
  }

  function setNext(period) {
    nextPeriod.textContent = period ? `Next: ${period.name} at ${period.startText}` : "";
    nextPeriod.hidden = !period;
  }

  function showProgress(start, end, nowMinutes, label) {
    const progress = periodProgress(start, end, nowMinutes);
    visual.hidden = false;
    endLabel.textContent = label;
    visual.style.setProperty("--progress", `${progress * 100}%`);
    visual.style.setProperty("--progress-turn", String(progress));
  }

  function showNoSchedule(message, detail) {
    title.textContent = message;
    range.textContent = detail || "";
    countdown.textContent = "";
    setNext(null);
    setPeriodState(null);
    highlightPeriod(-1);
    visual.hidden = true;
  }

  function updateCalendarLabel(info) {
    if (Number.isInteger(info?.cycleDay)) {
      cycleLabel.textContent = `Cycle day ${info.cycleDay}`;
    } else {
      cycleLabel.textContent = "No school day";
    }
  }

  function update(now = new Date()) {
    clock.dateTime = now.toISOString();
    clock.textContent = now.toLocaleTimeString([], {
      hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false
    });
    const dateKey = localDateKey(now);
    if (dateKey !== lastDateKey) {
      lastDateKey = dateKey;
      dateLabel.dateTime = dateKey;
      dateLabel.textContent = now.toLocaleDateString([], {
        weekday: "long", year: "numeric", month: "long", day: "numeric"
      });
    }

    let info = null;
    try {
      info = window.academicCalendar?.getAcademicDateInfo(dateKey) || null;
    } catch (error) {
      console.warn("School calendar data is unavailable for this date.", error);
    }

    const weekend = now.getDay() === 0 || now.getDay() === 6;
    const validCycleDay = Number.isInteger(info?.cycleDay) && info.cycleDay >= 1 && info.cycleDay <= 6;
    if (weekend) {
      cycleLabel.textContent = "Weekend";
      showNoSchedule("No active school schedule", "The school-day timer resumes on a scheduled school day.");
      return;
    }
    if (info?.isHoliday) {
      cycleLabel.textContent = info.holiday?.name || "School holiday";
      showNoSchedule("No active school schedule", "Today is a non-school day.");
      return;
    }
    if (!validCycleDay) {
      cycleLabel.textContent = info ? "No school day" : "Calendar unavailable";
      showNoSchedule("No active school schedule", info ? "Today is not listed as a school day." : "School calendar data is unavailable.");
      return;
    }

    updateCalendarLabel(info);
    const nowMinutes = now.getHours() * 60 + now.getMinutes() + now.getSeconds() / 60 + now.getMilliseconds() / 60000;
    const currentIndex = schedule.findIndex((period) => nowMinutes >= period.start && nowMinutes < period.end);
    if (currentIndex !== -1) {
      const current = schedule[currentIndex];
      title.textContent = current.name;
      range.textContent = `${current.startText}–${current.endText}`;
      countdown.textContent = `${durationText((current.end - nowMinutes) * 60)} remaining`;
      setNext(schedule[currentIndex + 1]);
      setPeriodState(current.name);
      highlightPeriod(currentIndex);
      showProgress(current.start, current.end, nowMinutes, current.endText);
      return;
    }

    const upcomingIndex = schedule.findIndex((period) => period.start > nowMinutes);
    if (upcomingIndex !== -1) {
      const upcoming = schedule[upcomingIndex];
      const previous = schedule[upcomingIndex - 1];
      title.textContent = previous ? "Between periods" : "School day begins soon";
      range.textContent = previous ? "Unscheduled transition" : "Before Contact";
      countdown.textContent = `${durationText((upcoming.start - nowMinutes) * 60)} until ${upcoming.name}`;
      setNext(upcoming);
      setPeriodState(null);
      visual.classList.add("period-between-classes");
      visual.dataset.periodState = "between-classes";
      highlightPeriod(-1);
      showProgress(previous?.end ?? 0, upcoming.start, nowMinutes, upcoming.startText);
      return;
    }

    showNoSchedule("School schedule ended", "Final Hour ended at 16:00.");
    cycleLabel.textContent = `Cycle day ${info.cycleDay}`;
  }

  function updateFullscreenControl() {
    const active = document.fullscreenElement === page;
    fullscreenToggle.textContent = active ? "Exit Fullscreen" : "Fullscreen";
    fullscreenToggle.setAttribute("aria-pressed", String(active));
  }

  if (document.fullscreenEnabled && page.requestFullscreen && document.exitFullscreen) {
    fullscreenToggle.addEventListener("click", async () => {
      fullscreenToggle.disabled = true;
      try {
        if (document.fullscreenElement === page) await document.exitFullscreen();
        else await page.requestFullscreen();
      } catch (error) {
        console.error("Unable to change fullscreen mode.", error);
      } finally {
        fullscreenToggle.disabled = false;
      }
    });
    document.addEventListener("fullscreenchange", updateFullscreenControl);
  } else {
    fullscreenToggle.hidden = true;
  }
  // Keep the existing teacher theme preference, but own all timer UI handling.
  const themeToggle = page.querySelector("#dark-mode-toggle");
  const themeKey = "scheduleTeacherTheme";
  function applyTimerTheme(dark) {
    page.dataset.theme = dark ? "dark" : "light";
    themeToggle.checked = dark;
  }
  try {
    applyTimerTheme(localStorage.getItem(themeKey) === "dark");
  } catch {
    applyTimerTheme(false);
  }
  themeToggle.addEventListener("change", () => {
    applyTimerTheme(themeToggle.checked);
    try {
      localStorage.setItem(themeKey, themeToggle.checked ? "dark" : "light");
    } catch {
      // The timer remains usable when browser storage is unavailable.
    }
  });

  renderSchedule();
  update();
  window.setInterval(update, 250);
  document.addEventListener("visibilitychange", () => update());
  window.addEventListener("focus", () => update());
})();
