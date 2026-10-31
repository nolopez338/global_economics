/*
  Purpose:
  Provides class-level reference data used by class schedule pages.

  Responsibilities:
  - Exposes student list document links per class via window.CLASS_STUDENT_LISTS
  - Exposes per-class notes collections via window.CLASS_NOTES
  - Serves as global input data for class-page rendering and related UI sections
*/
window.CLASS_METADATA = {
  "10SEMINAR": {
    name: "Seminar",
    shortLabel: "10S",
  },
  "10A": { coordinator: "Julian Franco" },
  "10B": { coordinator: "Carol Muñoz" },
  "10C": { coordinator: "Johan Rincón" },
  "10D": { coordinator: "David Amaya" },
  "10E": { coordinator: "Iván Cárdenas" },
  "11A": { coordinator: "Diego Bernal" },
  "11B": { coordinator: "José Alexander Hurtado" },
  "11C": { coordinator: "Alexandra Rodríguez" },
  "11D": { coordinator: "Ángela González" },
  "11E": { coordinator: "Jhon Jairo Gélvez" },
};

window.CLASS_STUDENT_LISTS = {
  "10SEMINAR": {
    students: [],
  },
  "10A": {
    pdfUrl:
      "../assets/pdf/Decimo-A.pdf",
    students: [],
  },
  "10B": {
    pdfUrl:
      "../assets/pdf/Decimo-B.pdf",
    students: [],
  },
  "10C": {
    pdfUrl:
      "../assets/pdf/Decimo-C.pdf",
    students: [],
  },
  "10D": {
    pdfUrl:
      "../assets/pdf/Decimo-D.pdf",
    students: [],
  },
  "10E": {
    pdfUrl:
      "../assets/pdf/Decimo-E.pdf",
    students: [],
  },
  "11A": {
    pdfUrl:
      "../assets/pdf/Once-A.pdf",
    students: [],
  },
  "11B": {
    pdfUrl:
      "../assets/pdf/Once-B.pdf",
    students: [],
  },
  "11C": {
    pdfUrl:
      "../assets/pdf/Once-C.pdf",
    students: [],
  },
  "11D": {
    pdfUrl:
      "../assets/pdf/Once-D.pdf",
    students: [],
    students: [],
  },
  "11E": {
    pdfUrl:
      "../assets/pdf/Once-E.pdf",
    students: [],
  },
};

window.CLASS_NOTES = {
  "10SEMINAR": [],
  "10A": [],
  "10B": [],
  "10C": [],
  "10D": [],
  "10E": [],
  "11A": [],
  "11B": [],
  "11C": [],
  "11D": [],
  "11E": [],
};
