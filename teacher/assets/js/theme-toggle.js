(function () {
  const STORAGE_KEY = "scheduleTeacherTheme";
  const body = document.body;
  const toggle = document.querySelector("#dark-mode-toggle");

  if (!toggle || !body) {
    return;
  }

  const applyTheme = (theme) => {
    const isDark = theme === "dark";
    body.classList.toggle("dark-theme", isDark);
    toggle.checked = isDark;
  };

  const savedTheme = localStorage.getItem(STORAGE_KEY);
  applyTheme(savedTheme === "dark" ? "dark" : "light");

  toggle.addEventListener("change", () => {
    const theme = toggle.checked ? "dark" : "light";
    applyTheme(theme);
    localStorage.setItem(STORAGE_KEY, theme);
  });
}());
