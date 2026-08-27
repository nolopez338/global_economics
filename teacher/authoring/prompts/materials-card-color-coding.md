# Implementation prompt: color-code material cards by category

Use the following prompt to update the materials page implementation.

---

Update `teacher/pages/materials.html` and its supporting materials workflow so every material card is assigned to exactly one of four explicit categories and receives a consistent, accessible color treatment:

| Stored category value | User-facing label | Color family | Suggested light-theme accent | Suggested dark-theme accent |
| --- | --- | --- | --- | --- |
| `slides` | Slides | Blue | `#2563eb` | `#60a5fa` |
| `classroom-activities` | Classroom activities | Green | `#15803d` | `#4ade80` |
| `practice-activities` | Practice activities | Amber | `#b45309` | `#fbbf24` |
| `extra-resources` | Extra resources | Purple | `#7e22ce` | `#c084fc` |

## First inspect the existing workflow

Before editing, review these files and preserve their current dated and base-catalog behavior:

- `teacher/pages/materials.html`
- `teacher/assets/js/materials-page.js`
- `teacher/assets/js/materials-validation.js`
- `teacher/assets/js/databases/materials-data.js`
- `teacher/assets/js/databases/materials-data-base.js`
- `teacher/authoring/validate-materials-data.js`
- `teacher/authoring/tests/materials-workflow.test.js`
- `assets/css/schedule.css`, especially the existing `.class-grid`, `.class-card`, `.class-icon`, and dark-theme rules

Do not replace the safe DOM construction with `innerHTML`, and do not change URL/query behavior, record lookup, grouping, external-link safety, empty states, or invalid-record isolation.

## Data-model and database migration

Add a required `Category` property to every object inside every `Materials` array in both manually maintained database files. The only accepted values are the four stored values in the table above. Example:

```js
{
  "Acronym": "C2S",
  "Name": "Slide for C2",
  "Hyperlink": "https://example.com/slides",
  "Category": "slides"
}
```

Treat `Category` as semantic data, not as a raw color value: do **not** store hex codes, CSS class names, or presentation tokens in the database. Migrate all existing material objects in both databases. Use the resource's purpose—not merely its acronym—to select the category. Map slides/presentations to `slides`, activities intended for use during class to `classroom-activities`, independent exercises/practice to `practice-activities`, and outlines, references, supplementary content, or other supporting links to `extra-resources`. If an existing generic item such as “Class material” is genuinely ambiguous, inspect its hyperlink/target and surrounding class context; do not silently guess from an acronym alone.

Update `teacher/assets/js/materials-validation.js` so:

- `Category` is a required material field.
- It must be a string equal to one of the four canonical stored values.
- Missing, misspelled, differently cased, or unknown values invalidate that material/record with a useful validation error.
- The allowed category list is defined once and exported by the validation API so the renderer/tests do not duplicate the contract unnecessarily.
- Existing warnings for truly unknown properties and all existing validations continue to work.

This repository uses JavaScript files as its material databases, so no SQL/schema migration is needed. The required database change is the complete update of both `materials-data.js` and `materials-data-base.js` described above.

## Rendering and visual design

Update the renderer to derive a controlled modifier class from the validated `Category` value (for example, `material-card--slides`). Never concatenate unvalidated arbitrary database text into a class name. Apply the category treatment to every card in both dated and base-catalog modes.

Add a compact legend near the top of the page that shows all four category labels and their corresponding swatches. The legend should be visible in both rendering modes, remain useful when a result happens to contain only some categories, and use semantic/list markup with an accessible label.

Each card must communicate its category without relying on color alone:

- Include a visible category label or badge using the user-facing label from the table.
- Preserve the acronym and material name.
- Include the category in the link's accessible name, while keeping the class/date context currently supplied by the renderer.
- Use the category color as an accent (for example border, icon/badge, or top stripe), not as a large saturated text background.

Keep colors centralized as CSS custom properties in `teacher/pages/materials.html` or the appropriate shared stylesheet. Provide coordinated light- and dark-theme values. Ensure readable text/background contrast, visible keyboard focus, and a treatment that still makes sense under high-contrast/forced-colors settings. Do not use four near-identical colors, and do not override the current card hover/focus behavior in a way that reduces usability. Preserve the responsive grid.

## Tests and acceptance criteria

Expand `teacher/authoring/tests/materials-workflow.test.js` and its lightweight DOM fixture as needed. At minimum, test that:

1. Each of the four canonical categories validates.
2. A missing or unknown category fails validation.
3. An unrelated extra property still produces a warning rather than being confused with `Category`.
4. Every material in both database files has a valid category and both complete databases pass the audit.
5. Dated-mode cards and base-catalog cards receive the expected controlled category modifier class.
6. Cards render a visible user-facing category label and include the category in their accessible link name.
7. The four-item legend renders with all category labels.
8. Existing request validation, headings, safe external links, grouping, empty states, ambiguity handling, and malformed-record isolation remain covered and passing.

Run at least:

```bash
node --test teacher/authoring/tests/materials-workflow.test.js
node teacher/authoring/validate-materials-data.js
```

Also inspect the page in light and dark themes at a representative dated URL and in base mode. Verify a narrow viewport, keyboard focus, the four legend/card treatments, and that category meaning remains visible without color. Do not finish with partial migration, validator warnings for `Category`, hard-coded acronym-to-color logic, or visual changes without regression tests.

---
