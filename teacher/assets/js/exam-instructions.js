(function () {
  "use strict";
  const page = document.getElementById("exam-page");
  const label = document.getElementById("timer-label");
  const value = document.getElementById("timer-value");
  const toggle = document.getElementById("fullscreen-toggle");
  const message = document.getElementById("fullscreen-message");

  function update() {
    const state = window.SchoolDayTimer?.countdownAt(new Date()) || {
      label: "Calendar unavailable", remaining: ""
    };
    label.textContent = state.label;
    value.textContent = state.remaining;
    value.hidden = !state.remaining;
  }

  function syncFullscreen() {
    const active = document.fullscreenElement === page;
    toggle.textContent = active ? "Exit fullscreen" : "Fullscreen";
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
