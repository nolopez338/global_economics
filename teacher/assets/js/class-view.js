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
  let alarmInterval = null;
  let audioContext = null;

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
  returnLink.textContent = `\u2190 ${origin === "schedule-teacher" ? "Teacher schedule" : "Schedule"}`;
  sourceFrame.src = `./${returnPage}`;

  function timerText(totalSeconds) {
    const safe = Math.max(0, Math.ceil(totalSeconds));
    const hours = Math.floor(safe / 3600);
    const minutes = Math.floor((safe % 3600) / 60);
    const seconds = safe % 60;
    return `${hours ? `${hours}:` : ""}${hours ? String(minutes).padStart(2, "0") : minutes}:${String(seconds).padStart(2, "0")}`;
  }

  function soundAlarmPulse() {
    if (!audioContext) return;
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();
    oscillator.type = "square";
    oscillator.frequency.value = 880;
    gain.gain.setValueAtTime(0.16, audioContext.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.35);
    oscillator.connect(gain).connect(audioContext.destination);
    oscillator.start();
    oscillator.stop(audioContext.currentTime + 0.35);
  }

  function beginAlarm() {
    if (alarmInterval) return;
    timerVisual.classList.add("timer-alarm");
    soundAlarmPulse();
    alarmInterval = window.setInterval(soundAlarmPulse, 600);
  }

  function stopAlarm() {
    window.clearInterval(alarmInterval);
    alarmInterval = null;
    timerVisual.classList.remove("timer-alarm");
  }

  function closeTimer() {
    stopAlarm();
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
    const durationMs = (Number(timerMinutes.value) * 60 + Number(timerSeconds.value)) * 1000;
    if (!Number.isFinite(durationMs) || durationMs <= 0) {
      timerError.hidden = false;
      return;
    }
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (AudioContext) {
      audioContext ||= new AudioContext();
      audioContext.resume();
    }
    const startedAt = Date.now();
    timerState = { startedAt, durationMs };
    timerDuration.textContent = timerText(durationMs / 1000);
    timerToggle.textContent = "Close Timer";
    timerToggle.setAttribute("aria-pressed", "true");
    classView.classList.add("timer-mode");
    visual.hidden = true;
    timerVisual.hidden = false;
    timerDialog.close();
    updateTimer(startedAt);
  });

  function updateTimer(timestamp = Date.now()) {
    if (!timerState) return;
    const elapsed = Math.max(0, timestamp - timerState.startedAt);
    const progress = Math.min(1, elapsed / timerState.durationMs);
    const position = `${progress * 100}%`;
    timerVisual.style.setProperty("--progress", position);
    timerVisual.style.setProperty("--progress-turn", String(progress));
    if (progress >= 1) beginAlarm();
  }

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
    endLabel.textContent = displayTime(end);
    const position = `${progress * 100}%`;
    visual.style.setProperty("--progress", position);
    visual.style.setProperty("--progress-turn", String(progress));
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
    if (timerState) {
      updateTimer(now.getTime());
      return;
    }
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
  window.setInterval(update, 100);
  document.addEventListener("visibilitychange", update);
  window.addEventListener("focus", update);
})();
