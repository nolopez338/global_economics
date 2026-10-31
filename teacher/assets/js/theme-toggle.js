(function () {
  var STORAGE_KEY = "scheduleTeacherTheme";
  var TOGGLE_SELECTOR = "#dark-mode-toggle";
  var LISTENER_FLAG = "themeToggleBound";

  function getStoredTheme() {
    try {
      return localStorage.getItem(STORAGE_KEY) === "dark" ? "dark" : "light";
    } catch (error) {
      return "light";
    }
  }

  function setStoredTheme(theme) {
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (error) {
      // Ignore storage failures (private mode/restrictions)
    }
  }

  function applyTheme(theme) {
    if (!document.body) {
      return;
    }

    var isDark = theme === "dark";
    document.body.classList.toggle("dark-theme", isDark);

    var toggle = document.querySelector(TOGGLE_SELECTOR);
    if (toggle) {
      toggle.checked = isDark;
    }
  }

  function bindToggle() {
    var toggle = document.querySelector(TOGGLE_SELECTOR);
    if (!toggle || toggle.dataset[LISTENER_FLAG] === "true") {
      return;
    }

    toggle.addEventListener("change", function () {
      var nextTheme = toggle.checked ? "dark" : "light";
      applyTheme(nextTheme);
      setStoredTheme(nextTheme);
    });

    toggle.dataset[LISTENER_FLAG] = "true";
    toggle.checked = getStoredTheme() === "dark";
  }

  function initializeThemeToggle() {
    var theme = getStoredTheme();
    applyTheme(theme);
    bindToggle();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeThemeToggle, { once: true });
  } else {
    initializeThemeToggle();
  }
}());
