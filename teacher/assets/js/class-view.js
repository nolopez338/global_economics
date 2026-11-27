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
  const minimalToggle = document.getElementById("minimal-toggle");
  const pageFullscreenToggle = document.getElementById("page-fullscreen-toggle");
  const resizeButtons = ["resize-clock", "resize-minimal", "resize-page"].map((id) => document.getElementById(id));
  const presentationToolbar = document.querySelector(".presentation-toolbar");
  const presentationExit = document.getElementById("presentation-exit");
  const presentationMessage = document.getElementById("presentation-message");
  const blockRemaining = document.getElementById("block-remaining");
  const timerRemaining = document.getElementById("timer-remaining");
  const timerToggle = document.getElementById("timer-toggle");
  const timerDialog = document.getElementById("timer-dialog");
  const timerForm = document.getElementById("timer-form");
  const timerCancel = document.getElementById("timer-cancel");
  const timerMinutes = document.getElementById("timer-minutes");
  const timerSeconds = document.getElementById("timer-seconds");
  const timerError = document.getElementById("timer-error");
  const timerVisual = document.getElementById("timer-visual");
  const timerDuration = document.getElementById("timer-duration");
  const presentationHours = document.querySelectorAll(".presentation-hour");
  let entries = null;
  let loadedDate = "";
  let timerState = null;
  const timerController = new window.CountdownTimer.Controller((snapshot) => {
    timerState = snapshot.state === "idle" ? null : snapshot;
    const position = `${snapshot.progress * 100}%`;
    timerVisual.style.setProperty("--progress", position);
    timerVisual.style.setProperty("--progress-turn", String(snapshot.progress));
    timerVisual.classList.toggle("timer-alarm", snapshot.state === "complete");
    timerRemaining.textContent = window.CountdownTimer.formatTime(snapshot.remainingMs);
  });
  const periodStateClasses = ["period-between-classes", "period-recess", "period-lunch"];

  let presentation = "page";
  let lastFullscreen = document.fullscreenElement;
  let presentationBusy = false;
  let returnControl = fullscreenToggle;
  let pendingFocus = null;

  function describeButton(button, label, pressed) {
    button.title = label;
    button.setAttribute("aria-label", label);
    button.setAttribute("aria-pressed", String(pressed));
  }

  function updatePresentationControls() {
    const clockFullscreen = document.fullscreenElement === classView;
    const pageFullscreen = document.fullscreenElement === document.documentElement;
    describeButton(fullscreenToggle, `Presentation 1: ${clockFullscreen ? "exit fullscreen clock" : "fullscreen the clock"}`, clockFullscreen);
    describeButton(minimalToggle, `Presentation 2: ${presentation === "minimal" ? "exit minimal clock" : "show the minimal clock (windowed)"}`, presentation === "minimal");
    describeButton(pageFullscreenToggle, `Presentation 3: ${pageFullscreen ? "exit whole-page fullscreen" : "fullscreen the whole page"}`, pageFullscreen);
    resizeButtons.forEach((button, index) => {
      const active = classView.classList.contains("window-fit") && presentation === ["clock", "minimal", "page"][index];
      const name = ["the clock", "the minimal clock", "the whole page"][index];
      describeButton(button, `Resize ${index + 1}: show ${name} and fit this browser window`, active);
    });
  }

  function setPresentation(mode, { fit = false, focus = true, active = mode !== "page" || fit } = {}) {
    presentation = mode;
    classView.classList.toggle("minimal-mode", mode === "minimal");
    classView.classList.toggle("clock-mode", mode === "clock");
    classView.classList.toggle("window-fit", fit);
    classView.classList.toggle("presentation-active", active);
    presentationToolbar.hidden = !active;
    if (active && timerDialog.open) timerDialog.close();
    [visual, timerVisual].forEach((circle) => {
      if (mode === "minimal") {
        circle.setAttribute("role", "button");
        circle.tabIndex = 0;
        circle.setAttribute("aria-label", "Exit minimal mode (click or press Enter, Space, or Escape)");
        circle.setAttribute("aria-describedby", circle === visual ? "block-remaining" : "timer-remaining");
      } else {
        circle.removeAttribute("role");
        circle.removeAttribute("tabindex");
        circle.removeAttribute("aria-describedby");
        circle.setAttribute("aria-label", circle === visual ? "Current schedule block" : "Countdown timer");
      }
    });
    updatePresentationControls();
    if (!focus) return;
    if (active) {
      pendingFocus = presentationExit;
    } else {
      pendingFocus = returnControl;
    }
    if (!presentationBusy) {
      pendingFocus.focus({ preventScroll: true });
      pendingFocus = null;
    }
  }

  function announce(message) {
    presentationMessage.textContent = message;
  }

  async function leaveFullscreen() {
    if (document.fullscreenElement) {
      if (!document.exitFullscreen) throw new Error("Fullscreen exit is unavailable");
      await document.exitFullscreen();
      if (document.fullscreenElement) throw new Error("Browser did not exit fullscreen");
    }
  }

  // Serialize presentation changes, but never touch the timer or schedule state.
  async function changePresentation(action) {
    if (presentationBusy) return;
    presentationBusy = true;
    const buttons = [fullscreenToggle, minimalToggle, pageFullscreenToggle, ...resizeButtons, presentationExit];
    buttons.forEach((button) => { button.disabled = true; });
    try {
      await action();
    } catch (error) {
      announce("The browser could not change presentation. Exit fullscreen and try again.");
      console.warn("Unable to change presentation.", error);
    } finally {
      buttons.forEach((button) => { button.disabled = false; });
      presentationBusy = false;
      updatePresentationControls();
      if (pendingFocus) {
        pendingFocus.focus({ preventScroll: true });
        pendingFocus = null;
      }
    }
  }

  async function returnToPage() {
    await leaveFullscreen();
    announce("");
    setPresentation("page");
  }

  minimalToggle.addEventListener("click", () => changePresentation(async () => {
    const mode = presentation === "minimal" ? "page" : "minimal";
    await leaveFullscreen();
    returnControl = minimalToggle;
    announce("");
    setPresentation(mode);
  }));
  presentationExit.addEventListener("click", () => changePresentation(returnToPage));
  [visual, timerVisual].forEach((circle) => {
    circle.addEventListener("click", () => {
      if (presentation === "minimal") changePresentation(returnToPage);
    });
    circle.addEventListener("keydown", (event) => {
      if (presentation === "minimal" && (event.key === "Enter" || event.key === " ")) {
        event.preventDefault();
        changePresentation(returnToPage);
      }
    });
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !timerDialog.open && classView.classList.contains("presentation-active")) {
      event.preventDefault();
      changePresentation(returnToPage);
    }
  });

  async function toggleFullscreen(target, mode, button) {
    if (document.fullscreenElement === target) {
      await returnToPage();
      return;
    }
    await leaveFullscreen();
    returnControl = button;
    announce("");
    const keepFit = mode === "page" && presentation === "page" && classView.classList.contains("window-fit");
    setPresentation(mode, { fit: keepFit, active: true });
    if (!document.fullscreenEnabled || !target.requestFullscreen) {
      announce("Fullscreen is unavailable in this browser. The presentation is ready in this window.");
      return;
    }
    try {
      await target.requestFullscreen();
    } catch (error) {
      announce("Fullscreen was blocked by the browser. The presentation is ready in this window.");
      console.warn("Unable to enter fullscreen.", error);
    }
  }

  fullscreenToggle.addEventListener("click", () => changePresentation(() => toggleFullscreen(classView, "clock", fullscreenToggle)));
  pageFullscreenToggle.addEventListener("click", () => changePresentation(() => toggleFullscreen(document.documentElement, "page", pageFullscreenToggle)));
  document.addEventListener("fullscreenchange", () => {
    const current = document.fullscreenElement;
    // Native Escape/browser exit must also restore the toolbar and keyboard focus.
    if (lastFullscreen && !current && classView.classList.contains("presentation-active")) {
      setPresentation("page");
    }
    lastFullscreen = current;
    updatePresentationControls();
  });

  function windowDimensions() {
    return { width: window.outerWidth, height: window.outerHeight, innerWidth: window.innerWidth, innerHeight: window.innerHeight };
  }

  const nextPaint = () => new Promise((resolve) => window.requestAnimationFrame(resolve));
  const delay = (ms) => new Promise((resolve) => window.setTimeout(resolve, ms));

  async function fitWindow(mode, index) {
    await leaveFullscreen();
    // Fullscreen exit can restore window chrome asynchronously.
    await nextPaint();
    await nextPaint();
    returnControl = resizeButtons[index];
    setPresentation(mode, { fit: true });
    const manualMessage = "Browser requires manual window resizing. Resize this window to fit.";
    // Reserve room for the final feedback without prematurely claiming failure.
    announce("Fitting this window. If the browser blocks resizing, resize this window manually.");
    const before = windowDimensions();
    const chromeWidth = Math.max(0, before.width - before.innerWidth);
    const chromeHeight = Math.max(0, before.height - before.innerHeight);
    const maxWidth = Math.max(1, (screen.availWidth || before.width) - chromeWidth);
    const maxHeight = Math.max(1, (screen.availHeight || before.height) - chromeHeight);
    const preferredWidth = { clock: 360, minimal: 248, page: 640 }[mode];
    let clockSize = mode === "minimal" ? 192 : 288;
    classView.style.setProperty("--fit-width", `${Math.min(preferredWidth, maxWidth)}px`);
    classView.style.setProperty("--fit-clock-size", `${clockSize}px`);
    classView.classList.add("measuring-fit");
    let bounds;
    let contentWidth;
    try {
      bounds = classView.getBoundingClientRect();
      // One bounded correction for short screens, with a readable clock floor.
      if (bounds.height > maxHeight) {
        clockSize = Math.max(160, clockSize - (bounds.height - maxHeight));
        classView.style.setProperty("--fit-clock-size", `${clockSize}px`);
        bounds = classView.getBoundingClientRect();
      }
      contentWidth = Math.max(bounds.width, classView.scrollWidth);
    } finally {
      classView.classList.remove("measuring-fit");
    }
    const targetWidth = Math.ceil(Math.min(maxWidth, contentWidth) + chromeWidth);
    const targetHeight = Math.ceil(Math.min(maxHeight, bounds.height) + chromeHeight);
    try {
      if (!window.resizeTo) throw new Error("Window resizing is unavailable");
      window.resizeTo(targetWidth, targetHeight);
    } catch (error) {
      // Ordinary browser windows often reject this silently instead of throwing.
      console.info("Window resizing was unavailable.", error);
    }
    // Wait for native geometry to settle, without resizing again or binding a loop.
    await delay(350);
    let after = windowDimensions();
    if (after.width === before.width && after.height === before.height) {
      await delay(350);
      after = windowDimensions();
    }
    const nearTarget = Math.abs(after.width - targetWidth) <= 8 && Math.abs(after.height - targetHeight) <= 8;
    const changed = Math.abs(after.width - before.width) > 2 || Math.abs(after.height - before.height) > 2;
    const viewportChanged = Math.abs(after.innerWidth - before.innerWidth) > 2 || Math.abs(after.innerHeight - before.innerHeight) > 2;
    const fits = classView.scrollWidth <= after.innerWidth + 1 && classView.getBoundingClientRect().height <= after.innerHeight + 1;
    if ((changed && viewportChanged && fits) || (nearTarget && fits)) {
      announce(changed ? `Window fitted to presentation ${index + 1}.` : `Window already fits presentation ${index + 1}.`);
    } else {
      announce(changed ? "Browser limited window resizing. Resize this window manually to fit." : manualMessage);
    }
  }

  resizeButtons.forEach((button, index) => button.addEventListener("click", () => changePresentation(() => fitWindow(["clock", "minimal", "page"][index], index))));
  updatePresentationControls();

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

  const returnPage = origin === "schedule-teacher" ? "schedule-teacher.html" : "schedule.html";
  returnLink.href = `../${returnPage}`;
  sourceFrame.src = `../${returnPage}`;

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
    timerToggle.title = "Set countdown timer";
    timerToggle.setAttribute("aria-label", timerToggle.title);
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
    timerToggle.title = "Close countdown timer and return to the schedule";
    timerToggle.setAttribute("aria-label", timerToggle.title);
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
    blockRemaining.textContent = durationText((end - nowMinutes) * 60);
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
    const hour = String(now.getHours() % 12 || 12);
    presentationHours.forEach((label) => {
      if (label.textContent !== hour) label.textContent = hour;
    });
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
