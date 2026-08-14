(() => {
  "use strict";

  const escapeHtml = (value) => String(value).replace(/[&<>"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"
  })[character]);

  function valuesFor(problem, key) {
    const value = problem.labels?.[key] ?? problem[key];
    if (value === undefined || value === null || value === "") return [];
    return Array.isArray(value) ? value : [value];
  }

  function initialize() {
    const data = window.practiceData;
    const controls = document.getElementById("practice-selector-controls");
    const status = document.getElementById("practice-selector-status");
    const region = document.getElementById("selected-problem");
    if (!data || !controls || !status || !region) return;

    const selectors = data.selectors || [];
    if (!Array.isArray(selectors) || selectors.length > 5 || !Array.isArray(data.problems)) {
      status.textContent = "Practice data is not configured correctly.";
      return;
    }

    const selected = new Map(selectors.map(({ key }) => [key, new Set()]));
    const summaries = new Map();
    controls.classList.toggle("practice-selector__controls--problem-only", selectors.length === 0);

    function configuredOptions(selector) {
      if (selector.options) return selector.options;
      return [...new Set(data.problems.flatMap((problem) => valuesFor(problem, selector.key)))];
    }

    selectors.forEach((selector, index) => {
      const details = document.createElement("details");
      details.className = "practice-multiselect practice-selector__field";
      const summary = document.createElement("summary");
      summary.id = `practice-filter-${index}-summary`;
      summary.setAttribute("aria-expanded", "false");
      const label = document.createElement("span");
      label.className = "practice-multiselect__label";
      label.textContent = selector.label;
      const value = document.createElement("span");
      value.className = "practice-multiselect__value";
      value.textContent = "Any";
      summary.append(label, value);
      summaries.set(selector.key, summary);

      const menu = document.createElement("div");
      menu.className = "practice-multiselect__menu";
      menu.setAttribute("role", "group");
      menu.setAttribute("aria-labelledby", summary.id);
      configuredOptions(selector).forEach((option) => {
        const row = document.createElement("label");
        row.className = "practice-multiselect__option";
        const input = document.createElement("input");
        input.type = "checkbox";
        input.value = option;
        input.dataset.filterKey = selector.key;
        const text = document.createElement("span");
        text.textContent = selector.descriptions?.[option]
          ? `${option} — ${selector.descriptions[option]}` : option;
        row.append(input, text);
        menu.append(row);
      });
      details.addEventListener("toggle", () => {
        summary.setAttribute("aria-expanded", String(details.open));
        if (details.open) controls.querySelectorAll(".practice-multiselect[open]").forEach((other) => {
          if (other !== details) other.open = false;
        });
      });
      details.append(summary, menu);
      controls.append(details);
    });

    const problemField = document.createElement("div");
    problemField.className = "practice-selector__field practice-selector__problem";
    const problemLabel = document.createElement("label");
    problemLabel.htmlFor = "practice-problem-select";
    problemLabel.textContent = "Problem";
    const problemSelect = document.createElement("select");
    problemSelect.id = "practice-problem-select";
    problemField.append(problemLabel, problemSelect);
    controls.append(problemField);

    const clear = document.createElement("button");
    clear.type = "button";
    clear.className = "practice-selector__clear";
    clear.textContent = "Clear all filters";
    clear.hidden = selectors.length === 0;
    controls.after(clear);

    function matchingProblems() {
      return data.problems.filter((problem) => selectors.every(({ key }) => {
        const wanted = selected.get(key);
        return wanted.size === 0 || valuesFor(problem, key).some((value) => wanted.has(value));
      }));
    }

    function hideProblem() {
      region.replaceChildren();
      region.hidden = true;
    }

    function typeset(element) {
      if (!window.MathJax?.typesetPromise) return;
      if (window.MathJax.typesetClear) window.MathJax.typesetClear([element]);
      window.MathJax.typesetPromise([element]).catch((error) =>
        console.error("MathJax typesetting failed:", error));
    }

    function renderProblem(problem) {
      const metadata = selectors.map(({ key, label }) => {
        const values = valuesFor(problem, key);
        return values.length
          ? `<li><strong>${escapeHtml(label)}:</strong> ${values.map(escapeHtml).join(", ")}</li>` : "";
      }).join("");
      const solutionId = `${problem.id}-solution`;
      const sections = problem.solutionSections.map((section) =>
        `<section class="practice-solution__section"><h4>${escapeHtml(section.title)}</h4><div class="content-block">${section.contentHtml}</div></section>`
      ).join("");
      region.innerHTML = `<h2>${escapeHtml(problem.labels?.name ?? problem.name)}</h2>
        ${metadata ? `<ul class="practice-problem__metadata" aria-label="Problem properties">${metadata}</ul>` : ""}
        <div class="example"><h3>Problem description</h3><div class="content-block">${problem.descriptionHtml}</div></div>
        <div class="subsection-minimize collapsed practice-solution" data-region="subsection">
          <button class="subsection-toggle" type="button" aria-expanded="false" aria-controls="${solutionId}">
            <span class="toggle-label">Solution</span><span class="toggle-icon" aria-hidden="true">+</span>
          </button>
          <div class="subsection-content" id="${solutionId}" role="region">${sections}</div>
        </div>`;
      region.hidden = false;
      typeset(region);
      status.textContent = `${problem.labels?.name ?? problem.name} selected.`;
    }

    function updateProblems() {
      selectors.forEach(({ key }) => {
        const values = [...selected.get(key)];
        summaries.get(key).querySelector(".practice-multiselect__value").textContent = values.length ? values.join(", ") : "Any";
      });
      const previous = problemSelect.value;
      const matches = matchingProblems();
      problemSelect.replaceChildren(new Option(matches.length ? "Choose a problem" : "No matching problems", ""));
      problemSelect.options[0].disabled = matches.length === 0;
      const ids = new Set();
      matches.forEach((problem) => {
        if (!ids.has(problem.id)) problemSelect.add(new Option(problem.labels?.name ?? problem.name, problem.id));
        ids.add(problem.id);
      });
      if (matches.some(({ id }) => id === previous)) problemSelect.value = previous;
      else hideProblem();
      status.textContent = matches.length
        ? `${matches.length} problem${matches.length === 1 ? "" : "s"} available. Choose a problem to display it.`
        : "No matching problems.";
    }

    controls.addEventListener("change", (event) => {
      if (!event.target.matches('input[type="checkbox"]')) return;
      const values = selected.get(event.target.dataset.filterKey);
      event.target.checked ? values.add(event.target.value) : values.delete(event.target.value);
      updateProblems();
    });
    problemSelect.addEventListener("change", () => {
      const problem = matchingProblems().find(({ id }) => id === problemSelect.value);
      if (problem) renderProblem(problem);
      else hideProblem();
    });
    clear.addEventListener("click", () => {
      selected.forEach((values) => values.clear());
      controls.querySelectorAll('input[type="checkbox"]').forEach((input) => { input.checked = false; });
      updateProblems();
    });
    region.addEventListener("click", (event) => {
      const button = event.target.closest(".subsection-toggle");
      if (!button) return;
      const expanded = button.getAttribute("aria-expanded") !== "true";
      button.setAttribute("aria-expanded", String(expanded));
      button.querySelector(".toggle-icon").textContent = expanded ? "−" : "+";
      button.closest(".subsection-minimize").classList.toggle("collapsed", !expanded);
    });
    document.addEventListener("click", (event) => {
      if (!event.target.closest(".practice-multiselect")) controls.querySelectorAll(".practice-multiselect[open]").forEach((details) => { details.open = false; });
    });
    updateProblems();
  }

  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", initialize) : initialize();
})();
