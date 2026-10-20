(function () {
  var params = new URLSearchParams(window.location.search);
  document.querySelector(".back-link").href = "magis.html" + (params.size ? "?" + params.toString() : "");
  var tasksTableBody = document.getElementById("tasks-table-body");
  var tasksEmpty = document.getElementById("tasks-empty");
  var tasksTable = tasksTableBody.closest("table");
  var connectButton = document.getElementById("connect-repository");
  var addTaskButton = document.getElementById("add-task");
  var saveButton = document.getElementById("save-tasks");
  var saveStatus = document.getElementById("task-save-status");
  var tasks = Array.isArray(window.magisTasks) ? window.magisTasks.map(function (task) {
    return Object.assign({}, task);
  }) : [];
  var tasksFileHandle = null;
  var hasUnsavedChanges = false;
  var isSaving = false;
  var revision = 0;
  var activePicker = null;
  var bogotaFormatter = new Intl.DateTimeFormat("en-GB", {
    timeZone: "America/Bogota", year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", hourCycle: "h23"
  });

  function dateParts(value) {
    var date = new Date(value);
    if (!value || !Number.isFinite(date.getTime())) return null;
    var parts = {};
    bogotaFormatter.formatToParts(date).forEach(function (part) { parts[part.type] = part.value; });
    return parts;
  }

  function displayDueDate(value) {
    var parts = dateParts(value);
    return parts ? parts.day + "/" + parts.month + "/" + parts.year + " " + parts.hour + ":" + parts.minute + " (Bogotá)" : "";
  }

  function closePicker() {
    if (!activePicker) return;
    var picker = activePicker;
    activePicker = null;
    picker.input.setAttribute("aria-expanded", "false");
    picker.dialog.close();
    picker.dialog.remove();
    if (picker.input.isConnected) picker.input.focus();
  }

  function openPicker(task, input, countdown) {
    closePicker();
    var today = dateParts(new Date().toISOString());
    // UTC is used only for calendar arithmetic; confirmed wall times get Bogotá's explicit offset.
    var month = new Date(Date.UTC(Number(today.year), Number(today.month) - 1, 1));
    var existing = dateParts(task.dueDate);
    var selected = null;
    var dialog = document.createElement("dialog");
    dialog.className = "task-date-picker";
    dialog.id = "task-date-picker";
    dialog.setAttribute("aria-labelledby", "task-picker-title");
    activePicker = { dialog: dialog, input: input };
    input.setAttribute("aria-expanded", "true");
    document.body.appendChild(dialog);

    function button(label, action, ariaLabel) {
      var element = document.createElement("button");
      element.type = "button";
      element.textContent = label;
      if (ariaLabel) element.setAttribute("aria-label", ariaLabel);
      element.addEventListener("click", action);
      return element;
    }
    function key(date) { return date.toISOString().slice(0, 10); }
    function apply(hour, minute) {
      if (!tasks.includes(task) || !input.isConnected) { closePicker(); return; }
      var value = selected + "T" + hour + ":" + minute + ":00-05:00";
      if (task.dueDate !== value) {
        task.dueDate = value;
        input.value = displayDueDate(value);
        countdown.dataset.taskDeadline = String(new Date(value).getTime());
        updateTaskCountdowns();
        markUnsaved();
      }
      closePicker();
    }
    function heading(text) {
      var title = document.createElement("h2");
      title.id = "task-picker-title";
      title.textContent = text;
      return title;
    }
    function showTime() {
      dialog.replaceChildren(heading("Set time for " + selected));
      var fields = document.createElement("div");
      fields.className = "task-picker-time";
      function field(label, max, value) {
        var wrapper = document.createElement("label");
        wrapper.textContent = label;
        var control = document.createElement("input");
        control.type = "number";
        control.min = "0";
        control.max = String(max);
        control.step = "1";
        control.required = true;
        control.value = value;
        wrapper.appendChild(control);
        fields.appendChild(wrapper);
        return control;
      }
      var hour = field("Hour (00–23)", 23, "23");
      var minute = field("Minute (00–59)", 59, "59");
      var note = document.createElement("p");
      note.textContent = "24-hour time · America/Bogota (UTC−05:00)";
      dialog.append(fields, note, button("Back to calendar", function () { showCalendar(); focusDay(selected); }), button("Confirm time", function () {
        if (!hour.reportValidity() || !minute.reportValidity()) return;
        apply(String(Number(hour.value)).padStart(2, "0"), String(Number(minute.value)).padStart(2, "0"));
      }), button("Cancel", closePicker));
      hour.focus();
    }
    function focusDay(value) {
      var target = dialog.querySelector('[data-date="' + value + '"]');
      if (target) target.focus();
    }
    function showCalendar(focusDate) {
      var year = month.getUTCFullYear();
      var monthIndex = month.getUTCMonth();
      var title = heading(new Intl.DateTimeFormat("en", { month: "long", year: "numeric", timeZone: "UTC" }).format(month));
      title.setAttribute("aria-live", "polite");
      var nav = document.createElement("div");
      nav.className = "task-picker-navigation";
      function navigate(delta) {
        month.setUTCMonth(month.getUTCMonth() + delta);
        showCalendar();
        dialog.querySelector(delta < 0 ? '[aria-label="Previous month"]' : '[aria-label="Next month"]').focus();
      }
      nav.append(button("‹", function () { navigate(-1); }, "Previous month"), title, button("›", function () { navigate(1); }, "Next month"));
      var grid = document.createElement("table");
      grid.className = "task-picker-calendar";
      grid.setAttribute("role", "grid");
      grid.setAttribute("aria-labelledby", title.id);
      var head = grid.createTHead().insertRow();
      ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].forEach(function (name) {
        var cell = document.createElement("th"); cell.scope = "col"; cell.textContent = name.slice(0, 2); cell.setAttribute("aria-label", name); head.appendChild(cell);
      });
      var body = grid.createTBody();
      var offset = month.getUTCDay();
      var length = new Date(Date.UTC(year, monthIndex + 1, 0)).getUTCDate();
      var existingKey = existing ? existing.year + "-" + existing.month + "-" + existing.day : "";
      var tabDate = focusDate || (selected && selected.slice(0, 7) === key(month).slice(0, 7) ? selected : existingKey.slice(0, 7) === key(month).slice(0, 7) ? existingKey : key(month));
      for (var slot = 0; slot < Math.ceil((offset + length) / 7) * 7; slot++) {
        if (slot % 7 === 0) var row = body.insertRow();
        var cell = row.insertCell();
        var day = slot - offset + 1;
        if (day < 1 || day > length) continue;
        (function (date, cell) {
          var value = key(date);
          var dayButton = button(String(date.getUTCDate()), function () { selected = value; showCalendar(value); focusDay(value); });
          dayButton.dataset.date = value;
          dayButton.tabIndex = value === tabDate ? 0 : -1;
          dayButton.setAttribute("aria-label", value + (value === existingKey ? ", current due date" : ""));
          cell.setAttribute("aria-selected", String(value === selected));
          dayButton.classList.toggle("is-existing", value === existingKey);
          dayButton.classList.toggle("is-selected", value === selected);
          dayButton.addEventListener("keydown", function (event) {
            var delta = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7, Home: -date.getUTCDay(), End: 6 - date.getUTCDay() }[event.key];
            var next = new Date(date);
            if (delta !== undefined) next.setUTCDate(next.getUTCDate() + delta);
            else if (event.key === "PageUp" || event.key === "PageDown") {
              next.setUTCDate(1);
              next.setUTCMonth(next.getUTCMonth() + (event.key === "PageUp" ? -1 : 1));
              next.setUTCDate(Math.min(date.getUTCDate(), new Date(Date.UTC(next.getUTCFullYear(), next.getUTCMonth() + 1, 0)).getUTCDate()));
            } else return;
            event.preventDefault();
            month = new Date(Date.UTC(next.getUTCFullYear(), next.getUTCMonth(), 1));
            showCalendar(key(next)); focusDay(key(next));
          });
          cell.appendChild(dayButton);
        })(new Date(Date.UTC(year, monthIndex, day)), cell);
      }
      var help = document.createElement("p");
      help.className = "task-picker-help";
      help.textContent = "Use arrow keys to move by day or week; Page Up/Down changes month. Select a day with Enter or Space. Dates and times use Bogotá time.";
      dialog.replaceChildren(nav, grid, help);
      if (selected) {
        var draft = document.createElement("p"); draft.textContent = "Selected: " + selected;
        dialog.append(draft, button("Confirm", function () { apply("23", "59"); }), button("Set Time", showTime));
      }
      dialog.appendChild(button("Cancel", closePicker));
    }
    dialog.addEventListener("cancel", function (event) { event.preventDefault(); closePicker(); });
    dialog.addEventListener("click", function (event) {
      var bounds = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) closePicker();
    });
    showCalendar();
    dialog.showModal();
    dialog.querySelector('[tabindex="0"]').focus();
  }

  function formatTimeRemaining(milliseconds) {
    if (!Number.isFinite(milliseconds)) {
      return "Invalid date";
    }

    var totalHours = Math.floor(Math.abs(milliseconds) / 3600000);
    var days = Math.floor(totalHours / 24);
    var hours = totalHours % 24;
    var duration = (days ? days + "d " : "") + hours + "h";

    return (milliseconds <= 0 ? "Overdue by " : "") + duration;
  }

  function updateTaskCountdowns() {
    var now = Date.now();

    document.querySelectorAll("[data-task-deadline]").forEach(function (countdown) {
      var remaining = Number(countdown.dataset.taskDeadline) - now;
      var overdue = Number.isFinite(remaining) && remaining <= 0;
      countdown.querySelector(".task-countdown-text").textContent = formatTimeRemaining(remaining);
      countdown.querySelector(".task-postpone-button").hidden = !overdue;
      countdown.classList.toggle("overdue", overdue);
    });
  }

  function setSaveStatus(message, state) {
    saveStatus.textContent = message;
    saveStatus.dataset.state = state || "info";
  }

  function markUnsaved() {
    revision += 1;
    hasUnsavedChanges = true;
    saveButton.disabled = !tasksFileHandle || isSaving;
    document.getElementById("task-dirty-status").hidden = false;
    setSaveStatus("Unsaved changes. Save before leaving.", "warning");
  }

  function renderTasks() {
    closePicker();
    tasksTableBody.replaceChildren();
    tasksEmpty.hidden = tasks.length !== 0;
    tasksTable.hidden = tasks.length === 0;

    tasks.forEach(function (task, index) {
      var dueDate = new Date(task.dueDate);
      var row = document.createElement("tr");
      var positionCell = document.createElement("td");
      var descriptionCell = document.createElement("td");
      var dueDateCell = document.createElement("td");
      var countdownCell = document.createElement("td");
      var countdownText = document.createElement("span");
      var postponeButton = document.createElement("button");
      var actionCell = document.createElement("td");
      var descriptionInput = document.createElement("input");
      var dueDateInput = document.createElement("input");
      var removeButton = document.createElement("button");

      positionCell.className = "task-position";
      positionCell.textContent = String(index + 1);
      descriptionInput.className = "task-editor-input";
      descriptionInput.type = "text";
      descriptionInput.value = task.description || "";
      descriptionInput.setAttribute("aria-label", "Task " + (index + 1) + " description");
      dueDateInput.className = "task-editor-input";
      dueDateInput.type = "text";
      dueDateInput.value = displayDueDate(task.dueDate);
      dueDateInput.placeholder = "Choose due date";
      dueDateInput.readOnly = true;
      dueDateInput.setAttribute("aria-haspopup", "dialog");
      dueDateInput.setAttribute("aria-expanded", "false");
      dueDateInput.setAttribute("aria-controls", "task-date-picker");
      dueDateInput.setAttribute("aria-label", "Task " + (index + 1) + " due date");
      countdownCell.className = "task-countdown";
      countdownCell.dataset.taskDeadline = String(dueDate.getTime());
      countdownText.className = "task-countdown-text";
      postponeButton.className = "task-editor-button task-postpone-button";
      postponeButton.type = "button";
      postponeButton.textContent = "Postpone";
      postponeButton.hidden = true;
      postponeButton.setAttribute("aria-label", "Postpone task " + (index + 1) + " by 24 hours");
      countdownCell.append(countdownText, postponeButton);
      removeButton.className = "task-editor-button task-remove-button";
      removeButton.type = "button";
      removeButton.textContent = "Remove";
      removeButton.setAttribute("aria-label", "Remove task " + (index + 1));

      descriptionInput.addEventListener("input", function () {
        task.description = descriptionInput.value;
        markUnsaved();
      });
      dueDateInput.addEventListener("click", function () { openPicker(task, dueDateInput, countdownCell); });
      postponeButton.addEventListener("click", function () {
        var deadline = new Date(task.dueDate).getTime();
        if (!Number.isFinite(deadline) || deadline > Date.now()) return;
        // Shift the existing instant, then serialize its wall time at UTC−05:00.
        var postponed = deadline + 86400000;
        var wallTime = new Date(postponed - 5 * 3600000);
        if (!Number.isFinite(wallTime.getTime())) return;
        task.dueDate = wallTime.toISOString().replace(/(?:\.000)?Z$/, "-05:00");
        dueDateInput.value = displayDueDate(task.dueDate);
        countdownCell.dataset.taskDeadline = String(postponed);
        updateTaskCountdowns();
        markUnsaved();
      });
      dueDateInput.addEventListener("keydown", function (event) {
        if (["Enter", " ", "ArrowDown"].includes(event.key)) {
          event.preventDefault();
          openPicker(task, dueDateInput, countdownCell);
        }
      });
      removeButton.addEventListener("click", function () {
        tasks.splice(index, 1);
        renderTasks();
        markUnsaved();
      });

      descriptionCell.appendChild(descriptionInput);
      dueDateCell.appendChild(dueDateInput);
      actionCell.appendChild(removeButton);
      row.append(positionCell, descriptionCell, dueDateCell, countdownCell, actionCell);
      tasksTableBody.appendChild(row);
    });

    updateTaskCountdowns();
  }

  async function locateTasksFile(repositoryHandle) {
    var teacherDirectory = await repositoryHandle.getDirectoryHandle("teacher");
    var assetsDirectory = await teacherDirectory.getDirectoryHandle("assets");
    var javascriptDirectory = await assetsDirectory.getDirectoryHandle("js");
    var databasesDirectory = await javascriptDirectory.getDirectoryHandle("databases");
    return databasesDirectory.getFileHandle("teacher-tasks.js");
  }

  function serializeTasks() {
    return "window.magisTasks = " + JSON.stringify(tasks, null, 2) + ";\n";
  }

  connectButton.addEventListener("click", async function () {
    if (typeof window.showDirectoryPicker !== "function") {
      setSaveStatus("Local editing requires Chrome or Edge with File System Access API support (on HTTPS or localhost).", "error");
      return;
    }

    connectButton.disabled = true;
    setSaveStatus("Select the repository root folder.", "info");
    try {
      var repositoryHandle = await window.showDirectoryPicker({ mode: "readwrite" });
      tasksFileHandle = await locateTasksFile(repositoryHandle);
      connectButton.textContent = "Repository Connected";
      saveButton.disabled = !hasUnsavedChanges;
      setSaveStatus("Repository connected successfully." + (hasUnsavedChanges ? " You have unsaved changes." : " No unsaved changes."), "success");
    } catch (error) {
      if (error.name === "AbortError") {
        setSaveStatus("Repository connection cancelled.", "info");
      } else if (error.name === "NotFoundError" || error.name === "TypeMismatchError") {
        setSaveStatus("Incorrect repository folder: select the root containing teacher/assets/js/databases/teacher-tasks.js.", "error");
      } else {
        setSaveStatus("Repository connection failed: " + error.message, "error");
      }
    } finally {
      connectButton.disabled = false;
    }
  });

  addTaskButton.addEventListener("click", function () {
    tasks.push({ description: "", dueDate: "" });
    renderTasks();
    markUnsaved();
  });

  saveButton.addEventListener("click", async function () {
    if (!tasksFileHandle || !hasUnsavedChanges || isSaving) {
      return;
    }

    isSaving = true;
    saveButton.disabled = true;
    connectButton.disabled = true;
    var savedRevision = revision;
    var savedTasks = tasks.map(function (task) { return Object.assign({}, task); });
    var serializedTasks = serializeTasks();
    setSaveStatus("Saving changes…", "info");
    var writable;
    try {
      writable = await tasksFileHandle.createWritable();
      await writable.write(serializedTasks);
      await writable.close();
      window.magisTasks = savedTasks;
      hasUnsavedChanges = revision !== savedRevision;
      document.getElementById("task-dirty-status").hidden = !hasUnsavedChanges;
      setSaveStatus(hasUnsavedChanges ? "Changes saved successfully. Newer edits remain unsaved." : "Changes saved successfully to teacher-tasks.js.", hasUnsavedChanges ? "warning" : "success");
    } catch (error) {
      if (writable) {
        await writable.abort().catch(function () {});
      }
      setSaveStatus("Save failed: " + error.message + ". Changes remain unsaved.", "error");
    } finally {
      isSaving = false;
      connectButton.disabled = false;
      saveButton.disabled = !hasUnsavedChanges;
    }
  });

  window.addEventListener("beforeunload", function (event) {
    if (hasUnsavedChanges) {
      event.preventDefault();
      event.returnValue = "";
    }
  });

  if (typeof window.showDirectoryPicker !== "function") {
    connectButton.disabled = true;
    setSaveStatus("Local editing requires Chrome or Edge with File System Access API support (on HTTPS or localhost).", "error");
  }

  renderTasks();
  window.setInterval(updateTaskCountdowns, 1000);
})();
