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
  const endLabel = document.getElementById("block-end");
  const classView = document.querySelector(".class-view");
  const fullscreenToggle = document.getElementById("fullscreen-toggle");
  const timerToggle = document.getElementById("timer-toggle");
  const timerDialog = document.getElementById("timer-dialog");
  const timerForm = document.getElementById("timer-form");
  const timerCancel = document.getElementById("timer-cancel");
  const timerMinutes = document.getElementById("timer-minutes");
  const timerSeconds = document.getElementById("timer-seconds");
  const timerError = document.getElementById("timer-error");
  const timerVisual = document.getElementById("timer-visual");
  const timerDuration = document.getElementById("timer-duration");
  let entries = null;
  let loadedDate = "";
  let timerState = null;
  const timerController = new window.CountdownTimer.Controller((snapshot) => {
    timerState = snapshot.state === "idle" ? null : snapshot;
    const position = `${snapshot.progress * 100}%`;
    timerVisual.style.setProperty("--progress", position);
    timerVisual.style.setProperty("--progress-turn", String(snapshot.progress));
    timerVisual.classList.toggle("timer-alarm", snapshot.state === "complete");
  });
  const periodStateClasses = ["period-between-classes", "period-recess", "period-lunch"];

  function setPeriodState(state) {
    visual.classList.remove(...periodStateClasses);
    if (state) visual.classList.add(`period-${state}`);
    visual.dataset.periodState = state || "general";
  }

  function scheduledPeriodState(entry) {
    const name = (entry?.name || "").trim().toLowerCase();
    if (name === "lunch") return "lunch";
    if (name === "break" || name === "recess") return "recess";
    return null;
  }

  function updateFullscreenControl() {
    const isFullscreen = document.fullscreenElement === classView;
    fullscreenToggle.textContent = isFullscreen ? "Exit Fullscreen" : "Fullscreen";
    fullscreenToggle.setAttribute("aria-pressed", String(isFullscreen));
  }

  if (document.fullscreenEnabled && classView.requestFullscreen && document.exitFullscreen) {
    fullscreenToggle.addEventListener("click", async () => {
      const exitingFullscreen = document.fullscreenElement === classView;
      fullscreenToggle.disabled = true;
      try {
        if (exitingFullscreen) {
          await document.exitFullscreen();
        } else {
          await classView.requestFullscreen();
        }
      } catch (error) {
        console.error(`Unable to ${exitingFullscreen ? "exit" : "enter"} fullscreen.`, error);
        if (!exitingFullscreen) fullscreenToggle.hidden = true;
        updateFullscreenControl();
      } finally {
        fullscreenToggle.disabled = false;
      }
    });
    document.addEventListener("fullscreenchange", updateFullscreenControl);
    updateFullscreenControl();
  } else {
    fullscreenToggle.hidden = true;
  }

  const returnPage = origin === "schedule-teacher" ? "schedule-teacher.html" : "schedule.html";
  returnLink.href = `./${returnPage}`;
  returnLink.textContent = `\u2190 ${origin === "schedule-teacher" ? "Schedule" : "Schedule"}`;
  sourceFrame.src = `./${returnPage}`;

  function closeTimer() {
    timerController.reset();
    timerState = null;
    classView.classList.remove("timer-mode");
    timerVisual.hidden = true;
    visual.hidden = false;
    timerVisual.style.setProperty("--progress", "0%");
    timerVisual.style.setProperty("--progress-turn", "0");
    timerDuration.textContent = "";
    timerForm.reset();
    timerError.hidden = true;
    timerToggle.textContent = "Timer";
    timerToggle.setAttribute("aria-pressed", "false");
    update();
  }

  function openTimerDialog() {
    timerError.hidden = true;
    timerDialog.showModal();
    timerMinutes.select();
  }

  timerToggle.addEventListener("click", () => {
    if (timerState) closeTimer();
    else openTimerDialog();
  });
  timerCancel.addEventListener("click", () => timerDialog.close());
  timerForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const durationMs = window.CountdownTimer.durationFromFields(timerMinutes.value, timerSeconds.value);
    if (!durationMs) {
      timerError.hidden = false;
      return;
    }
    timerDuration.textContent = window.CountdownTimer.formatTime(durationMs);
    timerToggle.textContent = "Close Timer";
    timerToggle.setAttribute("aria-pressed", "true");
    classView.classList.add("timer-mode");
    visual.hidden = true;
    timerVisual.hidden = false;
    timerDialog.close();
    timerController.start(durationMs);
  });

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

  function showNextActivity(entry) {
    if (!entry) {
      nextActivity.textContent = "";
      nextActivity.hidden = true;
      return;
    }
    nextActivity.textContent = `Next: ${entry.name} at ${displayTime(entry.start)}`;
    nextActivity.hidden = false;
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
    }).filter(Boolean).sort((first, second) => first.start - second.start);
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
    endLabel.textContent = displayTime(end);
    const position = `${progress * 100}%`;
    visual.style.setProperty("--progress", position);
    visual.style.setProperty("--progress-turn", String(progress));
  }

  function noSchedule(message) {
    setPeriodState(null);
    title.textContent = message;
    cycleLabel.textContent = "";
    countdown.textContent = "";
    showNextActivity(null);
    visual.hidden = true;
  }

  function update() {
    const now = new Date();
    clock.textContent = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
    if (timerState) return;
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
    const currentIndex = entries.findIndex((entry) => nowMinutes >= entry.start && nowMinutes < entry.end);
    const current = entries[currentIndex];
    if (current) {
      const periodState = scheduledPeriodState(current);
      setPeriodState(periodState);
      title.textContent = current.name;
      const nextEntry = periodState ? entries[currentIndex + 1] : null;
      showNextActivity(nextEntry);
      countdown.textContent = `${durationText((current.end - nowMinutes) * 60)} remaining`;
      showVisual(current.start, current.end, nowMinutes);
      return;
    }

    const upcomingIndex = entries.findIndex((entry) => entry.start > nowMinutes);
    const upcoming = entries[upcomingIndex];
    if (upcoming) {
      const previous = upcomingIndex > 0 ? entries[upcomingIndex - 1] : null;
      const gapMinutes = previous ? upcoming.start - previous.end : null;
      const isFiveMinuteTransition = previous
        && nowMinutes >= previous.end
        && gapMinutes >= 4.5
        && gapMinutes <= 5.5;
      setPeriodState(isFiveMinuteTransition ? "between-classes" : null);
      title.textContent = isFiveMinuteTransition ? "Between classes" : previous ? "Between activities" : "Before classes";
      showNextActivity(upcoming);
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
  window.setInterval(update, 100);
  document.addEventListener("visibilitychange", update);
  window.addEventListener("focus", update);
})();
