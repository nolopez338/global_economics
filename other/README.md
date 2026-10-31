# Standalone and Experimental Content

Publication status for the content in this directory is **unconfirmed**. No
tracked root navigation or deployment manifest identifies these paths as public
entry points, so their physical paths are intentionally unchanged.

- `cambridge/grade3_heatmap_dashboard.html` is a standalone Cambridge Grade 3
  assessment heatmap. Its CSS, JavaScript, and data are colocated. Validate the
  data/dashboard contract with:

  ```bash
  node other/cambridge/validate_grade3_heatmap_data.js
  ```

- `Test Basic/` and `Test Codex/` contain manual browser quiz experiments. The
  word “Test” is part of their historical names; these files are not an
  automated test suite and no test runner consumes them.
- `src/pages/g9-t3-correlation-coefficient.html` is a standalone Grade 9 page.
  It is not linked from the root student hub in the current checkout.

Do not relocate these paths until their external consumers and public URLs are
known. Serve them from the repository root with `python3 -m http.server 8000`
when performing manual browser checks.
