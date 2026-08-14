/* Projector-friendly view of the current entry in the existing schedule table. */
(function () {
  const params = new URLSearchParams(window.location.search);
  const origin = params.get("origin") === "schedule-teacher" ? "schedule-teacher" : "schedule";
  const sourceFrame = document.getElementById("schedule-source");
  const returnLink = document.getElementById("return-link");
  const title = document.getElementById("activity-title");
  const clock = document.getElementById("live-clock");
  const cycleLabel = document.getElementById("cycle-label");
  const countdown = document.getElementById("countdown");
  const nextActivity = document.getElementById("next-activity");
  const visual = document.getElementById("block-visual");
  const startLabel = document.getElementById("block-start");
  const endLabel = document.getElementById("block-end");
  const line = document.getElementById("time-line");
  const lineTime = document.getElementById("line-time");
  const elapsedFill = document.getElementById("elapsed-fill");
  const classView = document.querySelector(".class-view");
  const fullscreenToggle = document.getElementById("fullscreen-toggle");
  let entries = null;
  let loadedDate = "";

  function updateFullscreenControl() {
    const isFullscreen = document.fullscreenElement === classView;
    fullscreenToggle.textContent = isFullscreen ? "Exit Fullscreen" : "Fullscreen";
    fullscreenToggle.setAttribute("aria-pressed", String(isFullscreen));
  }

  if (classView.requestFullscreen) {
    fullscreenToggle.addEventListener("click", () => {
      if (document.fullscreenElement === classView) {
        document.exitFullscreen();
      } else {
        classView.requestFullscreen();
      }
    });
    document.addEventListener("fullscreenchange", updateFullscreenControl);
    updateFullscreenControl();
  } else {
    fullscreenToggle.hidden = true;
  }

  const returnPage = origin === "schedule-teacher" ? "schedule-teacher.html" : "schedule.html";
  returnLink.href = `./${returnPage}`;
  returnLink.textContent = `\u2190 ${origin === "schedule-teacher" ? "Teacher schedule" : "Schedule"}`;
  sourceFrame.src = `./${returnPage}`;

  function localDate(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
  }

  function parseMinutes(value) {
    const parts = value.trim().split(":").map(Number);
    return parts.length === 2 && parts.every(Number.isFinite) ? parts[0] * 60 + parts[1] : null;
  }

  function displayTime(totalMinutes) {
    const hours = Math.floor(totalMinutes / 60);
    const minutes = Math.floor(totalMinutes % 60);
    const suffix = hours >= 12 ? "PM" : "AM";
    return `${hours % 12 || 12}:${String(minutes).padStart(2, "0")} ${suffix}`;
  }

  function activityForCell(cell) {
    if (!cell || cell.classList.contains("empty") || cell.textContent.trim() === "\u2014") {
      return "Free Period";
    }
    const explicitActivity = cell.dataset.activity;
    if (explicitActivity) return explicitActivity;
    const parts = Array.from(cell.querySelectorAll("strong, .block"))
      .map((node) => node.textContent.trim()).filter(Boolean);
    return parts.length ? parts.join(" - ") : cell.textContent.trim() || "Free Period";
  }

  function readEntries(cycleDay) {
    const doc = sourceFrame.contentDocument;
    const rows = Array.from(doc?.querySelectorAll(".rotation-schedule tbody tr") || []);
    return rows.map((row) => {
      const rangeText = row.querySelector("th time")?.textContent || "";
      const parts = rangeText.split("-").map(parseMinutes);
      if (parts.length !== 2 || parts.some((part) => part === null) || parts[1] <= parts[0]) return null;
      const cell = row.querySelector(`[data-cycle-day="${cycleDay}"]`) || row.cells[cycleDay];
      const name = row.querySelector("th")?.dataset.activity || activityForCell(cell);
      return { start: parts[0], end: parts[1], name };
    }).filter(Boolean);
  }

  function durationText(seconds) {
    const safe = Math.max(0, Math.ceil(seconds));
    const hours = Math.floor(safe / 3600);
    const minutes = Math.floor((safe % 3600) / 60);
    const secs = safe % 60;
    return `${hours ? `${hours}:` : ""}${String(minutes).padStart(hours ? 2 : 1, "0")}:${String(secs).padStart(2, "0")}`;
  }

  function showVisual(start, end, nowMinutes) {
    const progress = Math.max(0, Math.min(1, (nowMinutes - start) / (end - start)));
    visual.hidden = false;
    startLabel.textContent = displayTime(start);
    endLabel.textContent = displayTime(end);
    const position = `${progress * 100}%`;
    line.style.top = position;
    elapsedFill.style.height = position;
  }

  function noSchedule(message) {
    title.textContent = message;
    cycleLabel.textContent = "";
    countdown.textContent = "";
    nextActivity.hidden = true;
    visual.hidden = true;
  }

  function update() {
    const now = new Date();
    clock.textContent = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
    lineTime.textContent = clock.textContent;
    const dateKey = localDate(now);
    const info = window.academicCalendar?.getAcademicDateInfo(dateKey);
    const cycleDay = info?.cycleDay;

    if (dateKey !== loadedDate) {
      loadedDate = dateKey;
      entries = null;
    }
    if (now.getDay() === 0 || now.getDay() === 6 || info?.isHoliday || !Number.isInteger(cycleDay) || cycleDay < 1 || cycleDay > 6) {
      noSchedule("No scheduled classes today");
      return;
    }
    if (!entries) entries = readEntries(cycleDay);
    if (!entries.length) {
      noSchedule("No scheduled classes today");
      return;
    }

    cycleLabel.textContent = `Academic cycle day ${cycleDay}`;
    const nowMinutes = now.getHours() * 60 + now.getMinutes() + now.getSeconds() / 60 + now.getMilliseconds() / 60000;
    const current = entries.find((entry) => nowMinutes >= entry.start && nowMinutes < entry.end);
    if (current) {
      title.textContent = current.name;
      nextActivity.hidden = true;
      countdown.textContent = `${durationText((current.end - nowMinutes) * 60)} remaining`;
      showVisual(current.start, current.end, nowMinutes);
      return;
    }

    const upcoming = entries.find((entry) => entry.start > nowMinutes);
    if (upcoming) {
      const previous = [...entries].reverse().find((entry) => entry.end <= nowMinutes);
      title.textContent = previous ? "Between classes" : "Before classes";
      nextActivity.textContent = `Next: ${upcoming.name} at ${displayTime(upcoming.start)}`;
      nextActivity.hidden = false;
      countdown.textContent = `${durationText((upcoming.start - nowMinutes) * 60)} until start`;
      showVisual(previous?.end ?? 0, upcoming.start, nowMinutes);
      return;
    }
    noSchedule("Schedule finished for today");
    cycleLabel.textContent = `Academic cycle day ${cycleDay}`;
  }

  sourceFrame.addEventListener("load", () => {
    entries = null;
    update();
  });
  update();
  window.setInterval(update, 250);
  document.addEventListener("visibilitychange", update);
  window.addEventListener("focus", update);
})();
