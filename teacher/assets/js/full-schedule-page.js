/*
  Loaded after class-page/schedule scripts so this adapter can replace the single-class
  markup and render the combined table while still allowing schedule-today.js to run.
*/
(() => {
  const parseClassId = (rawClassId) => {
    const classId = String(rawClassId || "").trim().toUpperCase();
    const match = classId.match(/^(\d+)([A-Z])$/);

    if (!match) {
      return {
        class_id: classId,
        grade: "",
        group: "",
      };
    }

    return {
      class_id: classId,
      grade: match[1],
      group: match[2],
    };
  };

  const toClassId = (entry) => {
    if (entry?.class_id) {
      return String(entry.class_id).trim().toUpperCase();
    }

    const grade = entry?.Grade ?? entry?.grade ?? "";
    const group = entry?.Section ?? entry?.Group ?? entry?.group ?? "";
    return `${grade}${group}`.trim().toUpperCase();
  };

  const toTimestamp = (dateValue) => {
    if (!dateValue) {
      return Number.POSITIVE_INFINITY;
    }

    const [year, month, day] = String(dateValue).split("/");
    const asDate = new Date(Number(year), Number(month) - 1, Number(day));
    const time = asDate.getTime();

    return Number.isNaN(time) ? Number.POSITIVE_INFINITY : time;
  };

  const classSlotSortValue = (slotValue) => {
    const slot = String(slotValue || "").trim();
    const match = slot.match(/^(\d+)-(\d+)$/);
    if (match) {
      return Number(match[1]) * 100 + Number(match[2]);
    }

    return Number.POSITIVE_INFINITY;
  };

  const flattenScheduleData = (sourceData) => {
    const flatEntries = [];

    if (Array.isArray(sourceData)) {
      sourceData.forEach((entry, index) => {
        const class_id = toClassId(entry);
        const { grade, group } = parseClassId(class_id);
        flatEntries.push({
          ...entry,
          class_id,
          grade,
          group,
          __sourceIndex: index,
        });
      });
      return flatEntries;
    }

    if (sourceData && typeof sourceData === "object") {
      Object.keys(sourceData).forEach((classKey) => {
        const entries = sourceData[classKey];
        if (!Array.isArray(entries)) {
          return;
        }

        entries.forEach((entry, index) => {
          const class_id = toClassId({ ...entry, class_id: classKey });
          const { grade, group } = parseClassId(class_id);
          flatEntries.push({
            ...entry,
            class_id,
            grade,
            group,
            __sourceIndex: index,
          });
        });
      });
    }

    return flatEntries;
  };

  const sortCombinedData = (entries) => {
    return [...entries].sort((a, b) => {
      const dateDiff = toTimestamp(a.Date) - toTimestamp(b.Date);
      if (dateDiff !== 0) {
        return dateDiff;
      }

      const slotDiff = classSlotSortValue(a["Class #"]) - classSlotSortValue(b["Class #"]);
      if (slotDiff !== 0) {
        return slotDiff;
      }

      const classDiff = String(a.class_id).localeCompare(String(b.class_id));
      if (classDiff !== 0) {
        return classDiff;
      }

      return (a.__sourceIndex ?? 0) - (b.__sourceIndex ?? 0);
    });
  };

  const formatScheduleDate = (value) => {
    const [year, month, day] = String(value || "").split("/");
    if (!year || !month || !day) {
      return value || "";
    }

    return `${year} / ${month} / ${day}`;
  };

  const createBreadcrumbs = () => {
    const wrapper = document.createElement("div");
    wrapper.className = "breadcrumbs";

    const link = document.createElement("a");
    link.className = "back-link";
    link.href = "../schedule.html";
    link.setAttribute("aria-label", "Back to the main schedule");
    link.textContent = "← Back to Schedule";

    wrapper.append(link);
    return wrapper;
  };

  const createNotesSection = () => {
    const section = document.createElement("section");
    section.className = "page-card";
    section.setAttribute("aria-label", "Full schedule notes");

    const heading = document.createElement("h2");
    heading.textContent = "Notes";

    const text = document.createElement("p");
    text.textContent =
      "This page aggregates schedule entries for all classes in a single calendar table.";

    section.append(heading, text);
    return section;
  };

  const createCalendarSection = (entries) => {
    const calendarSection = document.createElement("section");
    calendarSection.className = "page-card";
    calendarSection.setAttribute("aria-label", "Full schedule calendar");

    const heading = document.createElement("h2");
    heading.textContent = "Class Calendar";

    const tableWrap = document.createElement("div");
    tableWrap.className = "table-wrap";

    const table = document.createElement("table");
    table.className = "class-schedule-table";

    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");

    [
      "Grade",
      "Group",
      "Class #",
      "Date",
      "Weekday",
      "Day",
      "Description",
      "Material",
    ].forEach((label) => {
      const th = document.createElement("th");
      th.textContent = label;
      headerRow.append(th);
    });

    thead.append(headerRow);
    table.append(thead);

    const tbody = document.createElement("tbody");

    if (entries.length === 0) {
      const row = document.createElement("tr");
      const cell = document.createElement("td");
      cell.colSpan = 8;
      cell.textContent = "No scheduled entries.";
      row.append(cell);
      tbody.append(row);
    } else {
      entries.forEach((entry) => {
        const row = document.createElement("tr");
        row.dataset.date = entry.Date || "";
        row.dataset.weekday = entry.Weekday || "";
        row.dataset.description = entry.Description || "";
        row.dataset.classId = entry.class_id || "";
        if (entry.Summary) {
          row.dataset.summary = entry.Summary;
          row.dataset.title = entry.Summary;
        }

        const gradeCell = document.createElement("td");
        gradeCell.textContent = entry.grade;

        const groupCell = document.createElement("td");
        groupCell.textContent = entry.group;

        const classCell = document.createElement("th");
        classCell.scope = "row";
        classCell.textContent = entry["Class #"] || "";

        const dateCell = document.createElement("td");
        dateCell.textContent = formatScheduleDate(entry.Date);

        const weekdayCell = document.createElement("td");
        weekdayCell.textContent = entry.Weekday || "";

        const dayCell = document.createElement("td");
        dayCell.textContent = entry.Day ?? "";

        const descriptionCell = document.createElement("td");
        descriptionCell.textContent = entry.Description || "";

        const materialCell = document.createElement("td");
        materialCell.textContent = entry.Material || "";

        row.append(
          gradeCell,
          groupCell,
          classCell,
          dateCell,
          weekdayCell,
          dayCell,
          descriptionCell,
          materialCell
        );

        tbody.append(row);
      });
    }

    table.append(tbody);
    tableWrap.append(table);
    calendarSection.append(heading, tableWrap);

    return { calendarSection, table };
  };

  const renderFullSchedulePage = () => {
    const container = document.querySelector("#class-page");
    if (!container) {
      return;
    }

    const flattenedData = flattenScheduleData(window.SCHEDULE_DATA);
    const combinedSchedule = sortCombinedData(flattenedData);

    const header = document.createElement("header");
    const textWrapper = document.createElement("div");
    const title = document.createElement("h1");
    title.textContent = "Full Schedule";
    textWrapper.append(title);
    header.append(textWrapper);

    const { calendarSection, table } = createCalendarSection(combinedSchedule);

    container.innerHTML = "";
    container.append(
      createBreadcrumbs(),
      header,
      createNotesSection(),
      calendarSection,
      createBreadcrumbs()
    );

    table.dataset.rendered = "true";
    document.dispatchEvent(
      new CustomEvent("class-schedule-rendered", {
        detail: { table },
      })
    );
  };

  renderFullSchedulePage();
})();
