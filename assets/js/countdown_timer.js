/* Shared timestamp-based countdown controller and floating mind-map timer. */
(function () {
  "use strict";

  const clamp = (value, minimum, maximum) => Math.min(maximum, Math.max(minimum, value));

  function formatTime(milliseconds) {
    const total = Math.max(0, Math.ceil(milliseconds / 1000));
    const hours = Math.floor(total / 3600);
    const minutes = Math.floor((total % 3600) / 60);
    const seconds = total % 60;
    return `${hours ? `${hours}:` : ""}${hours ? String(minutes).padStart(2, "0") : minutes}:${String(seconds).padStart(2, "0")}`;
  }

  function durationFromFields(minutes, seconds) {
    const minuteValue = Number(minutes);
    const secondValue = Number(seconds);
    if (!Number.isInteger(minuteValue) || !Number.isInteger(secondValue)
      || minuteValue < 0 || minuteValue > 999 || secondValue < 0 || secondValue > 59) return null;
    const milliseconds = (minuteValue * 60 + secondValue) * 1000;
    return milliseconds > 0 ? milliseconds : null;
  }

  class Controller {
    constructor(onChange) {
      this.onChange = typeof onChange === "function" ? onChange : function () {};
      this.state = "idle";
      this.durationMs = 0;
      this.remainingMs = 0;
      this.endsAt = 0;
      this.updateInterval = null;
      this.alarmInterval = null;
      this.audioContext = null;
      this.sync = this.sync.bind(this);
      document.addEventListener("visibilitychange", this.sync);
      window.addEventListener("focus", this.sync);
    }

    snapshot(now = Date.now()) {
      const remainingMs = this.state === "running" ? Math.max(0, this.endsAt - now) : this.remainingMs;
      const elapsedMs = this.durationMs ? this.durationMs - remainingMs : 0;
      return { state: this.state, durationMs: this.durationMs, remainingMs, progress: this.durationMs ? clamp(elapsedMs / this.durationMs, 0, 1) : 0 };
    }

    emit() { this.onChange(this.snapshot()); }

    prepareAudio() {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;
      this.audioContext ||= new AudioContext();
      this.audioContext.resume();
    }

    alarmPulse() {
      if (!this.audioContext) return;
      const oscillator = this.audioContext.createOscillator();
      const gain = this.audioContext.createGain();
      oscillator.type = "square";
      oscillator.frequency.value = 880;
      gain.gain.setValueAtTime(0.16, this.audioContext.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + 0.35);
      oscillator.connect(gain).connect(this.audioContext.destination);
      oscillator.start();
      oscillator.stop(this.audioContext.currentTime + 0.35);
    }

    beginAlarm() {
      if (this.alarmInterval) return;
      this.alarmPulse();
      this.alarmInterval = window.setInterval(() => this.alarmPulse(), 600);
    }

    stopAlarm() {
      if (this.alarmInterval) window.clearInterval(this.alarmInterval);
      this.alarmInterval = null;
    }

    start(durationMs) {
      if (!Number.isFinite(durationMs) || durationMs <= 0) return false;
      this.stopAlarm();
      this.prepareAudio();
      this.durationMs = durationMs;
      this.remainingMs = durationMs;
      this.endsAt = Date.now() + durationMs;
      this.state = "running";
      if (!this.updateInterval) this.updateInterval = window.setInterval(this.sync, 100);
      this.sync();
      return true;
    }

    sync() {
      if (this.state !== "running") { this.emit(); return; }
      this.remainingMs = Math.max(0, this.endsAt - Date.now());
      if (!this.remainingMs) {
        this.state = "complete";
        window.clearInterval(this.updateInterval);
        this.updateInterval = null;
        this.beginAlarm();
      }
      this.emit();
    }

    stop() {
      if (this.state === "running") this.remainingMs = Math.max(0, this.endsAt - Date.now());
      this.stopAlarm();
      window.clearInterval(this.updateInterval);
      this.updateInterval = null;
      if (this.state !== "idle") this.state = "stopped";
      this.emit();
    }

    reset() {
      this.stopAlarm();
      window.clearInterval(this.updateInterval);
      this.updateInterval = null;
      this.state = "idle";
      this.durationMs = 0;
      this.remainingMs = 0;
      this.endsAt = 0;
      this.emit();
    }

    destroy() {
      this.reset();
      document.removeEventListener("visibilitychange", this.sync);
      window.removeEventListener("focus", this.sync);
      if (this.audioContext) this.audioContext.close();
      this.audioContext = null;
    }
  }

  function floatingMarkup() {
    return `<button class="countdown-launcher" type="button" aria-label="Open countdown timer" title="Open countdown timer"><span aria-hidden="true">⏱</span></button>
      <section class="countdown-window" role="dialog" aria-label="Countdown timer" hidden>
        <header class="countdown-titlebar">
          <strong>Countdown timer</strong><span class="countdown-title-time" aria-hidden="true"></span>
          <button class="countdown-icon countdown-minimize" type="button" aria-label="Minimize countdown timer" title="Minimize"><span aria-hidden="true">⌄</span></button>
          <button class="countdown-icon countdown-close" type="button" aria-label="Close and reset countdown timer" title="Close timer"><span aria-hidden="true">×</span></button>
        </header>
        <div class="countdown-content">
          <form class="countdown-form">
            <div class="countdown-fields">
              <label>Minutes<input class="countdown-minutes" type="number" min="0" max="999" value="5" inputmode="numeric"></label>
              <label>Seconds<input class="countdown-seconds" type="number" min="0" max="59" value="0" inputmode="numeric"></label>
            </div>
            <p class="countdown-error" role="alert" hidden>Enter a valid timer longer than zero seconds.</p>
            <button class="countdown-start" type="submit">Start</button>
          </form>
          <output class="countdown-display" aria-live="off">5:00</output>
          <p class="countdown-status" role="status" aria-live="polite">Ready</p>
          <div class="countdown-actions">
            <button class="countdown-stop" type="button" disabled>Stop</button>
            <button class="countdown-reset" type="button">Reset</button>
          </div>
        </div>
        ${["n","ne","e","se","s","sw","w","nw"].map((edge) => `<span class="countdown-resize countdown-resize--${edge}" data-resize="${edge}" aria-hidden="true"></span>`).join("")}
      </section>`;
  }

  function mountFloating(root) {
    if (!root || root.querySelector(":scope > .countdown-launcher")) return null;
    const host = document.createElement("div");
    host.className = "countdown-timer-host";
    host.setAttribute("data-mind-map-interactive", "");
    host.innerHTML = floatingMarkup();
    root.append(host);
    const launcher = host.querySelector(".countdown-launcher");
    const popup = host.querySelector(".countdown-window");
    const titlebar = host.querySelector(".countdown-titlebar");
    const titleTime = host.querySelector(".countdown-title-time");
    const form = host.querySelector(".countdown-form");
    const minutes = host.querySelector(".countdown-minutes");
    const seconds = host.querySelector(".countdown-seconds");
    const error = host.querySelector(".countdown-error");
    const display = host.querySelector(".countdown-display");
    const status = host.querySelector(".countdown-status");
    const stop = host.querySelector(".countdown-stop");
    let minimized = false;
    let lastAnnouncedSecond = null;
    let lastState = null;

    const controller = new Controller((snapshot) => {
      const text = formatTime(snapshot.remainingMs);
      display.textContent = text;
      titleTime.textContent = snapshot.state === "idle" ? "" : text;
      popup.dataset.timerState = snapshot.state;
      stop.disabled = snapshot.state !== "running";
      const labels = { idle: "Ready", running: "Timer running", stopped: "Timer stopped", complete: "Time is up" };
      const second = Math.ceil(snapshot.remainingMs / 1000);
      if (snapshot.state !== lastState) {
        status.textContent = labels[snapshot.state];
        lastState = snapshot.state;
      }
      if (snapshot.state === "running" && second !== lastAnnouncedSecond && (second % 10 === 0 || second <= 5)) {
        status.textContent = `${text} remaining`;
        lastAnnouncedSecond = second;
      }
    });

    function constrain() {
      if (popup.hidden) return;
      const margin = 8;
      const width = Math.min(popup.offsetWidth, window.innerWidth - margin * 2);
      const height = Math.min(popup.offsetHeight, window.innerHeight - margin * 2);
      popup.style.width = `${width}px`;
      if (!minimized) popup.style.height = `${height}px`;
      popup.style.left = `${clamp(parseFloat(popup.style.left) || window.innerWidth - width - 24, margin, window.innerWidth - width - margin)}px`;
      popup.style.top = `${clamp(parseFloat(popup.style.top) || window.innerHeight - height - 80, margin, window.innerHeight - height - margin)}px`;
    }

    function open() {
      popup.hidden = false;
      launcher.setAttribute("aria-expanded", "true");
      constrain();
      (minimized ? host.querySelector(".countdown-minimize") : minutes).focus();
    }

    launcher.setAttribute("aria-expanded", "false");
    launcher.addEventListener("click", open);
    host.querySelector(".countdown-close").addEventListener("click", () => {
      controller.reset(); form.reset(); display.textContent = "5:00"; error.hidden = true; minimized = false;
      popup.classList.remove("is-minimized"); popup.hidden = true;
      launcher.setAttribute("aria-expanded", "false"); launcher.focus();
    });
    host.querySelector(".countdown-minimize").addEventListener("click", (event) => {
      minimized = !minimized; popup.classList.toggle("is-minimized", minimized);
      event.currentTarget.setAttribute("aria-label", minimized ? "Restore countdown timer" : "Minimize countdown timer");
      event.currentTarget.title = minimized ? "Restore" : "Minimize"; constrain();
    });
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const duration = durationFromFields(minutes.value, seconds.value);
      error.hidden = Boolean(duration);
      if (duration) controller.start(duration);
    });
    stop.addEventListener("click", () => controller.stop());
    host.querySelector(".countdown-reset").addEventListener("click", () => {
      controller.reset(); form.reset(); display.textContent = "5:00"; error.hidden = true; minutes.focus();
    });

    let operation = null;
    function startPointer(event, resize) {
      if (event.button !== undefined && event.button !== 0) return;
      if (!resize && event.target.closest("button, input, label, [data-resize]")) return;
      const rect = popup.getBoundingClientRect();
      operation = { id: event.pointerId, resize, x: event.clientX, y: event.clientY, left: rect.left, top: rect.top, width: rect.width, height: rect.height };
      event.currentTarget.setPointerCapture(event.pointerId);
      document.documentElement.classList.add("countdown-pointer-active");
      event.preventDefault();
    }
    titlebar.addEventListener("pointerdown", (event) => startPointer(event, ""));
    host.querySelectorAll("[data-resize]").forEach((handle) => handle.addEventListener("pointerdown", (event) => startPointer(event, handle.dataset.resize)));
    host.addEventListener("pointermove", (event) => {
      if (!operation || operation.id !== event.pointerId) return;
      const dx = event.clientX - operation.x; const dy = event.clientY - operation.y;
      if (!operation.resize) { popup.style.left = `${operation.left + dx}px`; popup.style.top = `${operation.top + dy}px`; }
      else {
        const edge = operation.resize; let left = operation.left; let top = operation.top;
        let width = operation.width + (edge.includes("e") ? dx : edge.includes("w") ? -dx : 0);
        let height = operation.height + (edge.includes("s") ? dy : edge.includes("n") ? -dy : 0);
        width = clamp(width, 280, window.innerWidth - 16); height = clamp(height, 250, window.innerHeight - 16);
        if (edge.includes("w")) left = operation.left + operation.width - width;
        if (edge.includes("n")) top = operation.top + operation.height - height;
        popup.style.cssText += `;left:${left}px;top:${top}px;width:${width}px;height:${height}px`;
      }
      constrain();
    });
    const endPointer = (event) => { if (operation?.id === event.pointerId) { operation = null; document.documentElement.classList.remove("countdown-pointer-active"); constrain(); } };
    host.addEventListener("pointerup", endPointer); host.addEventListener("pointercancel", endPointer);
    window.addEventListener("resize", constrain);
    document.addEventListener("fullscreenchange", () => window.requestAnimationFrame(constrain));
    return controller;
  }

  window.CountdownTimer = { Controller, formatTime, durationFromFields, mountFloating };
  document.querySelectorAll("[data-mind-map-presentation]").forEach(mountFloating);
})();
