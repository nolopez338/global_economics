(function () {
  "use strict";
  const page = document.getElementById("exam-page");
  const label = document.getElementById("timer-label");
  const value = document.getElementById("timer-value");
  const digits = value.querySelector(".timer-digits");
  const toggle = document.getElementById("fullscreen-toggle");
  const fullscreenIcon = toggle.querySelector("svg path");
  const message = document.getElementById("fullscreen-message");

  function update() {
    const state = window.SchoolDayTimer?.countdownAt(new Date()) || {
      label: "Calendar unavailable", remaining: "", remainingSeconds: null
    };
    label.textContent = state.label;
    digits.textContent = state.remaining;
    value.hidden = !state.remaining;
    // Recompute from raw seconds on every tick, including target/calendar changes.
    const active = !value.hidden && Number.isFinite(state.remainingSeconds);
    if (active) {
      value.dataset.urgency = state.remainingSeconds > 1200 ? "green"
        : state.remainingSeconds >= 300 ? "yellow" : "red";
    } else {
      delete value.dataset.urgency;
    }
    value.classList.toggle("is-urgent", active && state.remainingSeconds < 60);
  }

  function syncFullscreen() {
    const active = document.fullscreenElement === page;
    const name = active ? "Exit fullscreen" : "Enter fullscreen";
    fullscreenIcon.setAttribute("d", active
      ? "M3 8h5V3m8 0v5h5M8 21v-5H3m18 0h-5v5"
      : "M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5");
    toggle.setAttribute("aria-label", name);
    toggle.title = name;
    toggle.setAttribute("aria-pressed", String(active));
  }

  if (document.fullscreenEnabled && page.requestFullscreen && document.exitFullscreen) {
    toggle.hidden = false;
    toggle.addEventListener("click", async () => {
      toggle.disabled = true;
      message.hidden = true;
      try {
        if (document.fullscreenElement === page) await document.exitFullscreen();
        else await page.requestFullscreen();
      } catch {
        message.textContent = "Fullscreen unavailable. Use your browser’s fullscreen option.";
        message.hidden = false;
      } finally {
        toggle.disabled = false;
        syncFullscreen();
      }
    });
    document.addEventListener("fullscreenchange", syncFullscreen);
    syncFullscreen();
  }

  update();
  window.setInterval(update, 250);
  window.addEventListener("focus", update);
  document.addEventListener("visibilitychange", update);
})();
