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

  function formatTimeRemaining(milliseconds) {
    if (!Number.isFinite(milliseconds)) {
      return "Invalid date";
    }

    if (milliseconds <= 0) {
      return "Overdue";
    }

    var totalSeconds = Math.floor(milliseconds / 1000);
    var days = Math.floor(totalSeconds / 86400);
    var hours = Math.floor((totalSeconds % 86400) / 3600);
    var minutes = Math.floor((totalSeconds % 3600) / 60);
    var seconds = totalSeconds % 60;

    return days + "d " + hours + "h " + minutes + "m " + seconds + "s";
  }

  function updateTaskCountdowns() {
    var now = Date.now();

    document.querySelectorAll("[data-task-deadline]").forEach(function (countdown) {
      var remaining = Number(countdown.dataset.taskDeadline) - now;
      countdown.textContent = formatTimeRemaining(remaining);
      countdown.classList.toggle("overdue", remaining <= 0);
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
      dueDateInput.value = task.dueDate || "";
      dueDateInput.placeholder = "YYYY-MM-DDTHH:mm:ss-05:00";
      dueDateInput.setAttribute("aria-label", "Task " + (index + 1) + " due date");
      countdownCell.className = "task-countdown";
      countdownCell.dataset.taskDeadline = String(dueDate.getTime());
      removeButton.className = "task-editor-button task-remove-button";
      removeButton.type = "button";
      removeButton.textContent = "Remove";
      removeButton.setAttribute("aria-label", "Remove task " + (index + 1));

      descriptionInput.addEventListener("input", function () {
        task.description = descriptionInput.value;
        markUnsaved();
      });
      dueDateInput.addEventListener("input", function () {
        task.dueDate = dueDateInput.value;
        countdownCell.dataset.taskDeadline = String(new Date(task.dueDate).getTime());
        updateTaskCountdowns();
        markUnsaved();
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
