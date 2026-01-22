const buildClassKey = (grade, section) => {
  if (!grade || !section) {
    return "";
  }

  return `${grade}${String(section).toUpperCase()}`;
};

const getClassMetadata = () => {
  const container = document.querySelector("#class-page");
  if (!container) {
    return null;
  }

  const grade = container.dataset.grade || "";
  const section = container.dataset.section || "";
  const classKey = buildClassKey(grade, section);

  return {
    container,
    grade,
    section: String(section).toUpperCase(),
    classKey,
  };
};

const createBreadcrumbs = (classKey, subtitle) => {
  const wrapper = document.createElement("div");
  wrapper.className = "breadcrumbs";

  const link = document.createElement("a");
  link.className = "back-link";
  link.href = "../schedule.html";
  link.setAttribute("aria-label", "Back to the main schedule");
  link.textContent = "← Back to Schedule";

  const sub = document.createElement("span");
  sub.className = "sub";
  sub.textContent = subtitle || `Class ${classKey} overview`;

  wrapper.append(link, sub);
  return wrapper;
};

const createHeader = (classKey) => {
  const header = document.createElement("header");
  const textWrapper = document.createElement("div");

  const title = document.createElement("h1");
  title.textContent = `Schedule ${classKey}`;

  const subtitle = document.createElement("p");
  subtitle.className = "sub";
  subtitle.textContent = `Placeholder schedule page for class ${classKey}. Update with class-specific details when ready.`;

  textWrapper.append(title, subtitle);
  header.append(textWrapper);

  return header;
};

const createNotesSection = (classKey, studentList, classNotes) => {
  const section = document.createElement("section");
  section.className = "page-card";
  section.setAttribute("aria-label", `Class ${classKey} description`);

  const heading = document.createElement("h2");
  heading.textContent = `Class ${classKey} Notes`;

  const notesContent = document.createElement("div");
  if (!classNotes || classNotes.length === 0) {
    const placeholder = document.createElement("p");
    placeholder.className = "placeholder";
    placeholder.textContent = "No class notes have been added yet.";
    notesContent.append(placeholder);
  } else {
    classNotes.forEach((note) => {
      const noteBlock = document.createElement("div");
      noteBlock.className = "notes-entry";

      const noteTitle = document.createElement("h3");
      noteTitle.textContent = note.title || "Class note";
      noteBlock.append(noteTitle);

      if (note.date) {
        const dateText = document.createElement("p");
        dateText.className = "sub";
        dateText.textContent = note.date;
        noteBlock.append(dateText);
      }

      if (Array.isArray(note.items) && note.items.length > 0) {
        const list = document.createElement("ul");
        note.items.forEach((item) => {
          const listItem = document.createElement("li");
          listItem.textContent = item;
          list.append(listItem);
        });
        noteBlock.append(list);
      }

      if (Array.isArray(note.links) && note.links.length > 0) {
        const linkList = document.createElement("ul");
        note.links.forEach((link) => {
          if (!link?.url) {
            return;
          }
          const listItem = document.createElement("li");
          const anchor = document.createElement("a");
          anchor.href = link.url;
          anchor.target = "_blank";
          anchor.rel = "noopener noreferrer";
          anchor.textContent = link.label || link.url;
          listItem.append(anchor);
          linkList.append(listItem);
        });
        noteBlock.append(linkList);
      }

      notesContent.append(noteBlock);
    });
  }

  const studentSubsection = document.createElement("div");
  studentSubsection.className = "notes-subsection";

  const studentHeading = document.createElement("h3");
  studentHeading.textContent = "Student list";

  studentSubsection.append(studentHeading);

  if (studentList?.pdfUrl) {
    const pdfParagraph = document.createElement("p");
    const pdfLink = document.createElement("a");
    pdfLink.href = studentList.pdfUrl;
    pdfLink.target = "_blank";
    pdfLink.rel = "noopener noreferrer";
    pdfLink.textContent = "View student list PDF";
    pdfParagraph.append(pdfLink);
    studentSubsection.append(pdfParagraph);
  }

  if (!studentList?.students || studentList.students.length === 0) {
    const emptyStudents = document.createElement("p");
    emptyStudents.className = "placeholder";
    emptyStudents.textContent = "No student names are listed yet.";
    studentSubsection.append(emptyStudents);
  } else {
    const list = document.createElement("ul");
    studentList.students.forEach((student) => {
      if (!student?.name) {
        return;
      }

      const listItem = document.createElement("li");
      listItem.textContent = student.name;
      list.append(listItem);
    });

    if (list.children.length > 0) {
      studentSubsection.append(list);
    } else {
      const emptyStudents = document.createElement("p");
      emptyStudents.className = "placeholder";
      emptyStudents.textContent = "No student names are listed yet.";
      studentSubsection.append(emptyStudents);
    }
  }

  section.append(heading, notesContent, studentSubsection);
  return section;
};

const createCalendarSection = (classKey, grade, section) => {
  const calendarSection = document.createElement("section");
  calendarSection.className = "page-card";
  calendarSection.setAttribute("aria-label", `Class ${classKey} calendar`);

  const heading = document.createElement("h2");
  heading.textContent = "Class Calendar";

  const tableWrap = document.createElement("div");
  tableWrap.className = "table-wrap";

  const table = document.createElement("table");
  table.className = "class-schedule-table";
  table.dataset.grade = grade;
  table.dataset.section = section;

  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");

  ["Class #", "Date", "Weekday", "Day", "Description", "Material"].forEach(
    (label) => {
      const th = document.createElement("th");
      th.textContent = label;
      headerRow.append(th);
    }
  );

  thead.append(headerRow);
  table.append(thead);
  table.append(document.createElement("tbody"));
  tableWrap.append(table);

  calendarSection.append(heading, tableWrap);
  return calendarSection;
};

const renderClassPage = () => {
  const metadata = getClassMetadata();
  if (!metadata) {
    return;
  }

  const { container, classKey, grade, section } = metadata;

  const studentLists = window.CLASS_STUDENT_LISTS || {};
  const classNotes = window.CLASS_NOTES || {};

  const studentList = studentLists[classKey];
  const notes = classNotes[classKey];

  document.title = `Schedule ${classKey}`;
  container.innerHTML = "";

  container.append(
    createBreadcrumbs(classKey, `Class ${classKey} overview`),
    createHeader(classKey),
    createNotesSection(classKey, studentList, notes),
    createCalendarSection(classKey, grade, section),
    createBreadcrumbs(classKey, "Return to the full weekly schedule.")
  );
};

renderClassPage();
