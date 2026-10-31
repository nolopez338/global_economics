# Student database

`students.json` contains 224 students for school year 2026–2027, extracted from the ten class rosters in `teacher/assets/pdf/` (`Decimo-A.pdf` through `Decimo-E.pdf` and `Once-A.pdf` through `Once-E.pdf`).

Each entry in `students` has:

| Field | Meaning |
| --- | --- |
| `student_id` | Student number printed in the roster, stored as text. |
| `name` | Full name in the source's surname-first order. Original capitalization, spelling, and accents are preserved; wrapped lines are joined with spaces. |
| `grade` | Numeric school grade: 10 or 11. |
| `section` | Class section: A–E. Combine with grade for a class label such as `10A`. |

The top-level `school_year` and `name_order` fields describe the whole database. Grades refer to school levels, not academic scores. Names are not split into given names and surnames because compound names wrap inconsistently in the source.

Group coordinators labelled “Acompañante de grupo” are excluded.

| Class | Students |
| --- | ---: |
| 10A | 21 |
| 10B | 23 |
| 10C | 22 |
| 10D | 20 |
| 10E | 22 |
| 11A | 23 |
| 11B | 23 |
| 11C | 22 |
| 11D | 24 |
| 11E | 24 |
| **Total** | **224** |

Validation checked that every student number has exactly one record, every name word below the student numbers was captured once, class counts match the rosters, and student IDs and full names are unique.
