    const scheduleRenderedEventName = "class-schedule-rendered";

    const triggerScheduleRendered = () => {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          document.dispatchEvent(new Event(scheduleRenderedEventName));
        });
      });
    };

    triggerScheduleRendered();

    const isTeacherPage = window.location.pathname.endsWith("/schedule-teacher.html");
    const scheduleMode = isTeacherPage ? "teacher" : "public";
    const scheduleOrigin = isTeacherPage ? "schedule-teacher" : "schedule";

    const updateSharedLinks = (origin, teacherAccess) => {
      const calendarLink = document.querySelector('.back-link[href*="general_calendar.html"]');
      if (calendarLink) {
        calendarLink.setAttribute("href", `./assets/html/general_calendar.html?origin=${origin}`);
      }

      document.querySelectorAll('a.class-link[href^="pages/magis.html"]').forEach((link) => {
        link.setAttribute("href", teacherAccess ? "pages/magis.html?access=teacher" : "pages/magis.html");
      });
    };

    updateSharedLinks(scheduleOrigin, isTeacherPage);

    const updateClassLinks = (mode, origin) => {
      const links = document.querySelectorAll("a.class-link, a.class-card");
      links.forEach((link) => {
        const href = link.getAttribute("href");
        const match = href && href.match(/^pages\/class_schedules\/(\d{2})([A-E])\.html$/i);
        if (!match) {
          return;
        }
        const grade = match[1];
        const section = match[2].toUpperCase();
        link.setAttribute("href", `pages/class.html?grade=${grade}&section=${section}&mode=${mode}&origin=${origin}`);
      });
    };

    updateClassLinks(scheduleMode, scheduleOrigin);

    const toggle = document.querySelector(".collapsible-toggle");
    const panel = document.getElementById("class-pages-panel");
    const icon = toggle?.querySelector(".collapsible-icon");

    if (toggle && panel && icon) {
      toggle.addEventListener("click", () => {
        const isExpanded = toggle.getAttribute("aria-expanded") === "true";
        toggle.setAttribute("aria-expanded", String(!isExpanded));
        panel.hidden = isExpanded;
        icon.textContent = isExpanded ? "+" : "−";
      });
    }

    const weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    const storageKey = "scheduleDay1Weekday";
    const weekdayViewKey = "scheduleWeekdayView";
    const weekSummaryKey = "scheduleWeekSummaries";
    const weekdayHeader = document.getElementById("weekday-header");
    const weekdayButtons = Array.from(document.querySelectorAll(".weekday-button"));
    const weekdayMenu = document.getElementById("weekday-menu");
    const weekdayMenuItems = weekdayMenu ? Array.from(weekdayMenu.querySelectorAll("button[data-weekday]")) : [];
    const weekdayViewToggle = document.getElementById("weekday-view-toggle");
    const weekdayViewIndicator = weekdayViewToggle?.querySelector(".view-toggle-text");
    const plainStyleToggle = document.getElementById("plain-style-toggle");
    const plainStyleIndicator = plainStyleToggle?.querySelector(".view-toggle-text");
    const weekSummaryToggle = document.getElementById("week-summary-toggle");
    const weekSummaryIndicator = weekSummaryToggle?.querySelector(".view-toggle-text");
    const scheduleTable = document.querySelector(".table-wrap table");
    const scheduleWrap = document.querySelector(".schedule-table-wrap");
    const currentTimeOverlay = document.querySelector(".current-time-overlay");
    const currentTimeLine = document.querySelector(".current-time-line");
    const currentTimeLabel = document.querySelector(".current-time-label");
    const originalBackgrounds = new Map();
    let lastTrigger = null;
    let isWeekdayView = false;
    let isPlainStyle = false;
    let isWeekSummaryEnabled = false;
    let cachedClassEntries = null;

    const setExpandedState = (isExpanded) => {
      weekdayButtons.forEach((button) => {
        button.setAttribute("aria-expanded", String(isExpanded));
      });
    };

    const updateWeekdayLabels = (day1Label) => {
      const offset = Math.max(0, weekdays.indexOf(day1Label));
      weekdayButtons.forEach((button, index) => {
        const label = weekdays[(offset + index) % weekdays.length];
        button.textContent = label;
      });
    };

    const storeWeekday = (day1Label) => {
      try {
        localStorage.setItem(storageKey, day1Label);
      } catch (error) {
        console.error("Unable to store weekday selection.", error);
      }
    };

    const getStoredWeekday = () => {
      try {
        return localStorage.getItem(storageKey);
      } catch (error) {
        console.error("Unable to read weekday selection.", error);
        return null;
      }
    };

    const applyWeekdaySelection = (day1Label) => {
      if (!weekdays.includes(day1Label)) {
        return;
      }
      updateWeekdayLabels(day1Label);
      storeWeekday(day1Label);
      if (isWeekdayView) {
        applyColumnOrder("weekday");
      }
      refreshScheduleView();
    };

    const positionMenu = () => {
      if (!weekdayMenu || !weekdayHeader) {
        return;
      }
      const rect = weekdayHeader.getBoundingClientRect();
      const top = rect.bottom + 4;
      const left = rect.left;
      weekdayMenu.style.top = `${top}px`;
      weekdayMenu.style.left = `${left}px`;
    };

    const openMenu = (trigger) => {
      if (!weekdayMenu) {
        return;
      }
      lastTrigger = trigger || document.activeElement;
      positionMenu();
      weekdayMenu.hidden = false;
      weekdayMenu.setAttribute("aria-hidden", "false");
      setExpandedState(true);
      const firstItem = weekdayMenuItems[0];
      if (firstItem) {
        firstItem.focus();
      }
    };

    const closeMenu = () => {
      if (!weekdayMenu) {
        return;
      }
      weekdayMenu.hidden = true;
      weekdayMenu.setAttribute("aria-hidden", "true");
      setExpandedState(false);
      if (lastTrigger && typeof lastTrigger.focus === "function") {
        lastTrigger.focus();
      }
    };

    if (weekdayHeader && weekdayMenu) {
      weekdayHeader.addEventListener("click", (event) => {
        const targetButton = event.target.closest(".weekday-button");
        if (targetButton) {
          openMenu(targetButton);
          return;
        }
        openMenu(weekdayButtons[0]);
      });

      weekdayButtons.forEach((button) => {
        button.addEventListener("keydown", (event) => {
          if (event.key === "Escape") {
            closeMenu();
          }
        });
      });

      weekdayMenuItems.forEach((item) => {
        item.addEventListener("click", () => {
          const selection = item.getAttribute("data-weekday");
          if (selection) {
            applyWeekdaySelection(selection);
          }
          closeMenu();
        });
      });

      weekdayMenu.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
          event.preventDefault();
          closeMenu();
        }
      });

      document.addEventListener("click", (event) => {
        if (!weekdayMenu.hidden) {
          const target = event.target;
          if (!weekdayMenu.contains(target) && !weekdayHeader.contains(target)) {
            closeMenu();
          }
        }
      });

      window.addEventListener("resize", () => {
        if (!weekdayMenu.hidden) {
          positionMenu();
        }
      });
    }

    const initialWeekday = getStoredWeekday();
    if (initialWeekday && weekdays.includes(initialWeekday)) {
      updateWeekdayLabels(initialWeekday);
    } else {
      updateWeekdayLabels(weekdays[0]);
    }

    const ensureDayColumnAttributes = () => {
      if (!scheduleTable) {
        return;
      }
      const rows = scheduleTable.querySelectorAll("tr");
      rows.forEach((row) => {
        const cells = Array.from(row.children);
        cells.slice(1).forEach((cell, index) => {
          if (!cell.hasAttribute("data-day-column")) {
            cell.setAttribute("data-day-column", String(index));
          }
        });
      });
    };

    const getWeekdayOrder = () => {
      const orderMap = new Map();
      weekdayButtons.forEach((button) => {
        const label = button.textContent?.trim();
        const columnCell = button.closest("[data-day-column]");
        const dayColumn = columnCell ? Number(columnCell.getAttribute("data-day-column")) : NaN;
        if (label && !Number.isNaN(dayColumn)) {
          orderMap.set(label, dayColumn);
        }
      });
      const ordered = weekdays.map((label) => orderMap.get(label));
      if (ordered.some((value) => typeof value !== "number" || Number.isNaN(value))) {
        return [0, 1, 2, 3, 4];
      }
      return ordered;
    };

    const reorderRow = (row, order) => {
      const cells = Array.from(row.children);
      const timeCell = cells[0];
      if (!timeCell) {
        return;
      }
      const dayCells = cells.slice(1);
      const cellMap = new Map();
      dayCells.forEach((cell) => {
        const index = Number(cell.getAttribute("data-day-column"));
        if (!Number.isNaN(index)) {
          cellMap.set(index, cell);
        }
      });
      const fragment = document.createDocumentFragment();
      fragment.appendChild(timeCell);
      order.forEach((index) => {
        const cell = cellMap.get(index);
        if (cell) {
          fragment.appendChild(cell);
        }
      });
      row.appendChild(fragment);
    };

    const applyColumnOrder = (mode) => {
      if (!scheduleTable) {
        return;
      }
      const order = mode === "weekday" ? getWeekdayOrder() : [0, 1, 2, 3, 4];
      const rows = scheduleTable.querySelectorAll("tr");
      rows.forEach((row) => reorderRow(row, order));
    };

    const setToggleState = (enabled) => {
      if (!weekdayViewToggle || !weekdayViewIndicator) {
        return;
      }
      isWeekdayView = Boolean(enabled);
      weekdayViewToggle.setAttribute("aria-checked", String(isWeekdayView));
      weekdayViewIndicator.textContent = isWeekdayView ? "On" : "Off";
      applyColumnOrder(isWeekdayView ? "weekday" : "day");
      refreshScheduleView();
      try {
        localStorage.setItem(weekdayViewKey, String(isWeekdayView));
      } catch (error) {
        console.error("Unable to store weekday view selection.", error);
      }
    };

    const setPlainStyleState = (enabled) => {
      if (!plainStyleToggle || !plainStyleIndicator || !scheduleWrap) {
        return;
      }
      isPlainStyle = Boolean(enabled);
      plainStyleToggle.setAttribute("aria-checked", String(isPlainStyle));
      plainStyleIndicator.textContent = isPlainStyle ? "On" : "Off";
      scheduleWrap.classList.toggle("plain-style", isPlainStyle);
      refreshScheduleView();
    };

    const getStoredView = () => {
      try {
        return localStorage.getItem(weekdayViewKey);
      } catch (error) {
        console.error("Unable to read weekday view selection.", error);
        return null;
      }
    };

    ensureDayColumnAttributes();
    const storedView = getStoredView();
    setToggleState(storedView === "true");

    if (weekdayViewToggle) {
      weekdayViewToggle.addEventListener("click", () => {
        setToggleState(!isWeekdayView);
      });

      weekdayViewToggle.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          setToggleState(!isWeekdayView);
        }
      });
    }

    if (plainStyleToggle) {
      plainStyleToggle.addEventListener("click", () => {
        setPlainStyleState(!isPlainStyle);
      });

      plainStyleToggle.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          setPlainStyleState(!isPlainStyle);
        }
      });
    }

    const getStoredSummaryPreference = () => {
      try {
        return localStorage.getItem(weekSummaryKey);
      } catch (error) {
        console.error("Unable to read week summary selection.", error);
        return null;
      }
    };

    const parseISODate = (value) => {
      if (!value) {
        return null;
      }
      const [year, month, day] = value.split("-").map(Number);
      if (Number.isNaN(year) || Number.isNaN(month) || Number.isNaN(day)) {
        return null;
      }
      const date = new Date(year, month - 1, day);
      if (Number.isNaN(date.getTime())) {
        return null;
      }
      date.setHours(0, 0, 0, 0);
      return date;
    };

    const getClassPageLinks = () => {
      const linkElements = Array.from(document.querySelectorAll(".class-grid .class-card"));
      return linkElements
        .map((link) => {
          const href = link.getAttribute("href");
          const label = link.textContent?.trim();
          return href && label ? { href, classId: label } : null;
        })
        .filter(Boolean);
    };

    const buildClassEntriesFromDocument = (doc, fallbackClassId) => {
      const rows = Array.from(doc.querySelectorAll("tr[data-class-id][data-date][data-weekday][data-session]"));
      return rows
        .map((row) => {
          const {
            classId,
            date: dateText,
            weekday,
            session,
            title,
            description,
          } = row.dataset;
          const parsedDate = parseISODate(dateText);
          if (!classId && !fallbackClassId) {
            return null;
          }
          if (!parsedDate || !weekday || !session) {
            return null;
          }
          return {
            classId: classId || fallbackClassId,
            date: parsedDate,
            weekday,
            session,
            title,
            description,
          };
        })
        .filter(Boolean);
    };

    const loadClassEntries = async () => {
      if (cachedClassEntries) {
        return cachedClassEntries;
      }
      const classPages = getClassPageLinks();
      if (classPages.length === 0) {
        cachedClassEntries = [];
        return cachedClassEntries;
      }
      const entries = [];
      await Promise.all(
        classPages.map(async ({ href, classId }) => {
          try {
            const response = await fetch(href);
            if (!response.ok) {
              return;
            }
            const html = await response.text();
            const doc = new DOMParser().parseFromString(html, "text/html");
            entries.push(...buildClassEntriesFromDocument(doc, classId));
          } catch (error) {
            return;
          }
        })
      );
      cachedClassEntries = entries;
      return entries;
    };

    const clearWeekSummaries = () => {
      if (!scheduleTable) {
        return;
      }
      scheduleTable.querySelectorAll(".week-summary").forEach((summary) => summary.remove());
    };

    const normalizeDateKey = (date) => {
      if (!date) {
        return null;
      }
      return date.toISOString().split("T")[0];
    };

    const parseDisplayDate = (value) => {
      if (!value) {
        return null;
      }
      const trimmed = value.trim();
      const match = trimmed.match(/(\d{4})\s*([/-])\s*(\d{1,2})\s*[/-]\s*(\d{1,2})/);
      if (!match) {
        return null;
      }
      const [, yearText, separator, part1Text, part2Text] = match;
      const year = Number(yearText);
      let month = Number(part1Text);
      let day = Number(part2Text);
      if (separator === "/") {
        day = Number(part1Text);
        month = Number(part2Text);
      }
      if (Number.isNaN(year) || Number.isNaN(month) || Number.isNaN(day)) {
        return null;
      }
      const date = new Date(year, month - 1, day);
      if (Number.isNaN(date.getTime())) {
        return null;
      }
      date.setHours(0, 0, 0, 0);
      return date;
    };

    const findDateInText = (text) => {
      if (!text) {
        return null;
      }
      const match = text.match(/\d{4}\s*[/-]\s*\d{1,2}\s*[/-]\s*\d{1,2}/);
      return match ? parseDisplayDate(match[0]) : null;
    };

    const getDateFromElement = (element) => {
      if (!element) {
        return null;
      }
      const dataDate = element.getAttribute("data-date");
      if (dataDate) {
        return parseISODate(dataDate) || parseDisplayDate(dataDate);
      }
      if (element.tagName === "TIME") {
        const datetime = element.getAttribute("datetime");
        if (datetime) {
          return parseISODate(datetime) || parseDisplayDate(datetime);
        }
      }
      return findDateInText(element.textContent);
    };

    const getDateForCell = (cell) => {
      if (!cell) {
        return null;
      }
      const directDate = getDateFromElement(cell);
      if (directDate) {
        return directDate;
      }
      const dateElement = cell.querySelector("[data-date], time[datetime]");
      const elementDate = getDateFromElement(dateElement);
      if (elementDate) {
        return elementDate;
      }
      const columnIndex = Number(cell.getAttribute("data-day-column"));
      if (Number.isNaN(columnIndex)) {
        return null;
      }
      const headerCells = scheduleTable?.querySelectorAll("thead th[data-day-column]") ?? [];
      const headerCell = Array.from(headerCells).find(
        (header) => Number(header.getAttribute("data-day-column")) === columnIndex
      );
      return getDateFromElement(headerCell);
    };

    const buildSummaryText = (description) => {
      if (!description) {
        return "No Activity";
      }
      const trimmed = description.trim();
      if (!trimmed) {
        return "No Activity";
      }
      const sentenceMatch = trimmed.match(/[^.!?]+[.!?]?/);
      return sentenceMatch ? sentenceMatch[0].trim() : trimmed;
    };

    const buildEntryKey = (classId, session, date) => {
      const dateKey = normalizeDateKey(date);
      if (!classId || !session || !dateKey) {
        return null;
      }
      return `${classId}-${session}-${dateKey}`;
    };

    const renderWeekSummaries = async () => {
      if (!isWeekSummaryEnabled) {
        clearWeekSummaries();
        return;
      }
      if (!scheduleTable) {
        return;
      }
      clearWeekSummaries();
      const entries = await loadClassEntries();
      const entryIndex = new Map();
      entries.forEach((entry) => {
        const key = buildEntryKey(entry.classId, entry.session, entry.date);
        if (key && !entryIndex.has(key)) {
          entryIndex.set(key, entry);
        }
      });
      scheduleTable.querySelectorAll("tbody td").forEach((cell) => {
        const link = cell.querySelector(".class-link");
        const block = link?.querySelector(".block");
        if (!link || !block) {
          return;
        }
        const label = block.textContent?.trim() ?? "";
        const [classId, session] = label.split("-").map((part) => part.trim());
        if (!classId || !session) {
          return;
        }
        const cellDate = getDateForCell(cell);
        const entryKey = buildEntryKey(classId, session, cellDate);
        const entry = entryKey ? entryIndex.get(entryKey) : null;
        const summaryText = buildSummaryText(entry?.description);
        const summary = document.createElement("div");
        summary.className = "week-summary";
        summary.textContent = summaryText;
        link.after(summary);
      });
    };

    const setWeekSummaryState = async (enabled) => {
      if (!weekSummaryToggle || !weekSummaryIndicator) {
        return;
      }
      isWeekSummaryEnabled = enabled;
      weekSummaryToggle.setAttribute("aria-checked", String(enabled));
      weekSummaryIndicator.textContent = enabled ? "On" : "Off";
      if (enabled) {
        await renderWeekSummaries();
      } else {
        clearWeekSummaries();
      }
      try {
        localStorage.setItem(weekSummaryKey, String(enabled));
      } catch (error) {
        console.error("Unable to store week summary selection.", error);
      }
    };

    function refreshWeekSummaries() {
      if (!isWeekSummaryEnabled) {
        return;
      }
      renderWeekSummaries();
    }

    function refreshScheduleView() {
      updateTodayColumnHighlight();
      updateCurrentTimeLine();
      refreshWeekSummaries();
    }

    const storedSummaryPreference = getStoredSummaryPreference();
    setWeekSummaryState(storedSummaryPreference === "true");

    if (weekSummaryToggle) {
      weekSummaryToggle.addEventListener("click", () => {
        setWeekSummaryState(!isWeekSummaryEnabled);
      });

      weekSummaryToggle.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          setWeekSummaryState(!isWeekSummaryEnabled);
        }
      });
    }

    function clearTodayColumnHighlight() {
      if (!scheduleTable) {
        return;
      }
      scheduleTable.querySelectorAll(".today-highlighted").forEach((cell) => {
        const stored = originalBackgrounds.get(cell);
        if (stored) {
          if (stored.background) {
            cell.style.background = stored.background;
          } else {
            cell.style.removeProperty("background");
          }
          if (stored.backgroundColor) {
            cell.style.backgroundColor = stored.backgroundColor;
          } else {
            cell.style.removeProperty("background-color");
          }
          originalBackgrounds.delete(cell);
        } else {
          cell.style.removeProperty("background");
          cell.style.removeProperty("background-color");
        }
        cell.style.removeProperty("--today-highlight-fill");
        cell.classList.remove("today-highlighted");
      });
    }

    function extractColor(value) {
      if (!value) {
        return null;
      }
      const match = value.match(/rgba?\([^)]+\)|#[0-9a-fA-F]{3,8}/);
      return match ? match[0] : null;
    }

    function parseColor(color) {
      if (!color) {
        return null;
      }
      const rgbMatch = color.match(/rgba?\(([^)]+)\)/);
      if (rgbMatch) {
        const parts = rgbMatch[1].match(/[\d.]+/g)?.map(Number) ?? [];
        if (parts.length >= 3) {
          return {
            r: parts[0],
            g: parts[1],
            b: parts[2],
            a: parts.length > 3 ? parts[3] : 1,
          };
        }
      }
      const hexMatch = color.match(/#([0-9a-fA-F]{3,8})/);
      if (hexMatch) {
        const hex = hexMatch[1];
        const expand = (value) => value.split("").map((char) => char + char).join("");
        const normalized = hex.length === 3 || hex.length === 4 ? expand(hex) : hex;
        const hasAlpha = normalized.length === 8;
        const int = parseInt(normalized, 16);
        const r = (int >> (hasAlpha ? 24 : 16)) & 255;
        const g = (int >> (hasAlpha ? 16 : 8)) & 255;
        const b = (int >> (hasAlpha ? 8 : 0)) & 255;
        const a = hasAlpha ? (int & 255) / 255 : 1;
        return { r, g, b, a };
      }
      return null;
    }

    function lightenColor(color, amount = 0.35) {
      const parsed = parseColor(color);
      if (!parsed) {
        return null;
      }
      const blend = (value) => Math.round(value + (255 - value) * amount);
      return `rgba(${blend(parsed.r)}, ${blend(parsed.g)}, ${blend(parsed.b)}, ${parsed.a})`;
    }

    function resolveTodayHighlightBaseColor() {
      if (scheduleWrap) {
        const base = getComputedStyle(scheduleWrap).getPropertyValue("--today-highlight-base").trim();
        if (base) {
          return base;
        }
      }
      const sampleCell = scheduleTable?.querySelector("td, th");
      if (!sampleCell) {
        return null;
      }
      const styles = getComputedStyle(sampleCell);
      return (
        extractColor(styles.boxShadow) ||
        extractColor(styles.outlineColor) ||
        extractColor(styles.borderColor)
      );
    }

    function getTodayWeekdayLabel() {
      const todayIndex = new Date().getDay();
      if (todayIndex === 0 || todayIndex === 6) {
        return null;
      }
      return weekdays[todayIndex - 1];
    }

    function findColumnIndexForWeekday(weekdayLabel) {
      if (!weekdayLabel) {
        return null;
      }
      if (isWeekdayView) {
        const matchingButton = weekdayButtons.find(
          (button) => button.textContent?.trim() === weekdayLabel
        );
        if (matchingButton) {
          const headerCell = matchingButton.closest("[data-day-column]");
          const columnIndex = headerCell?.getAttribute("data-day-column");
          return columnIndex !== null && columnIndex !== undefined ? Number(columnIndex) : null;
        }
      }
      const dayIndex = weekdayButtons.findIndex(
        (button) => button.textContent?.trim() === weekdayLabel
      );
      return dayIndex >= 0 ? dayIndex : null;
    }

    function updateTodayColumnHighlight() {
      if (!scheduleTable) {
        return;
      }
      if (isPlainStyle) {
        clearTodayColumnHighlight();
        return;
      }
      const todayLabel = getTodayWeekdayLabel();
      const columnIndex = findColumnIndexForWeekday(todayLabel);
      clearTodayColumnHighlight();
      if (columnIndex === null || Number.isNaN(columnIndex)) {
        return;
      }
      const baseColor = resolveTodayHighlightBaseColor();
      const fillColor = baseColor ? lightenColor(baseColor) : null;
      if (!fillColor) {
        return;
      }
      const highlightOverrides = [
        { start: 6 * 60 + 45, end: 7 * 60 + 5, color: "rgba(116, 101, 173, 0.85)" },
        { start: 9 * 60 + 35, end: 10 * 60 + 5, color: "rgba(44, 149, 62, 0.85)" },
        { start: 12 * 60 + 50, end: 13 * 60 + 50, color: "rgba(44, 149, 62, 0.85)" },
        { start: 14 * 60 + 45, end: 15 * 60 + 0, color: "rgba(116, 101, 173, 0.85)" },
      ];
      scheduleTable
        .querySelectorAll(`[data-day-column="${columnIndex}"]`)
        .forEach((cell) => {
          if (!originalBackgrounds.has(cell)) {
            originalBackgrounds.set(cell, {
              background: cell.style.background,
              backgroundColor: cell.style.backgroundColor,
            });
          }
          const row = cell.closest("tr");
          const timeCell = row?.querySelector("th[scope='row']");
          const range = parseTimeRange(timeCell?.textContent?.trim());
          const override = range
            ? highlightOverrides.find((item) => item.start === range.start && item.end === range.end)
            : null;
          const cellFill = override ? override.color : fillColor;
          cell.style.backgroundColor = cellFill;
          cell.style.setProperty("--today-highlight-fill", cellFill);
          cell.classList.add("today-highlighted");
        });
    }

    function parseTimeRange(text) {
      if (!text) {
        return null;
      }
      const [startText, endText] = text.split("-").map((part) => part.trim());
      const toMinutes = (value) => {
        const [hours, minutes] = value.split(":").map(Number);
        if (Number.isNaN(hours) || Number.isNaN(minutes)) {
          return null;
        }
        return hours * 60 + minutes;
      };
      const start = toMinutes(startText);
      const end = toMinutes(endText);
      if (start === null || end === null || end <= start) {
        return null;
      }
      return { start, end };
    }

    function updateCurrentTimeLine() {
      if (!scheduleTable || !scheduleWrap || !currentTimeOverlay || !currentTimeLine) {
        return;
      }
      if (isPlainStyle) {
        currentTimeOverlay.hidden = true;
        return;
      }
      const now = new Date();
      const nowMinutes = now.getHours() * 60 + now.getMinutes();
      const rows = Array.from(scheduleTable.querySelectorAll("tbody tr"));
      const matchingRow = rows.find((row) => {
        const timeCell = row.querySelector("th[scope='row']");
        const range = parseTimeRange(timeCell?.textContent?.trim());
        return range ? nowMinutes >= range.start && nowMinutes <= range.end : false;
      });

      if (!matchingRow) {
        currentTimeOverlay.hidden = true;
        return;
      }

      const timeCell = matchingRow.querySelector("th[scope='row']");
      const range = parseTimeRange(timeCell?.textContent?.trim());
      if (!range) {
        currentTimeOverlay.hidden = true;
        return;
      }
      const fraction = (nowMinutes - range.start) / (range.end - range.start);
      const wrapRect = scheduleWrap.getBoundingClientRect();
      const rowRect = matchingRow.getBoundingClientRect();
      const timeCellRect = timeCell?.getBoundingClientRect();
      const leftOffset = timeCellRect ? timeCellRect.right - wrapRect.left : 0;
      const rowTop = rowRect.top - wrapRect.top;
      const top = rowTop + rowRect.height * fraction;
      const width = wrapRect.width - leftOffset;

      currentTimeOverlay.hidden = false;
      currentTimeLine.style.left = `${leftOffset}px`;
      currentTimeLine.style.width = `${width}px`;
      currentTimeLine.style.top = `${top}px`;
      if (currentTimeLabel) {
        currentTimeLabel.textContent = now.toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        });
      }
    }

    document.addEventListener(scheduleRenderedEventName, () => {
      refreshScheduleView();
    });

    refreshScheduleView();
    setInterval(updateCurrentTimeLine, 30000);
    window.addEventListener("resize", refreshScheduleView);
