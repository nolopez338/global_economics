(() => {
  "use strict";

  const practiceData = {
    // Define label dimensions here. Keep "name" first; add or remove up to three optional labels.
    labelDefinitions: [
      { key: "name", label: "Problem" },
      { key: "criterion", label: "Criterion" }
    ],

    // Add problems here. Each problem must provide one value for every label defined above.
    problems: [
      {
        id: "problem-1",
        labels: {
          name: "Example 1 (C1): How to Structure a Complete Response",
          criterion: "C1"
        },
        descriptionHtml: String.raw`
          <p><strong>Page title pattern:</strong> Start with the topic and model type, for example <em>Continuous Probability Models: Uniform and Piecewise Densities</em>.</p>
          <p><strong>Problem description pattern:</strong> Give a real context, define the random variable, and state support. Example: let $X$ be waiting time in minutes for local delivery with support $0\le X\le10$.</p>
          <p><strong>Why this section exists:</strong> It lets any reader understand the scenario before seeing formulas.</p>
        `,
        // Add, remove, or reorder solution subsections in this array; titles stay paired with content.
        solutionSections: [
          {
            title: "Questions/tasks",
            contentHtml: String.raw`
              <ol>
                <li>State the model and support clearly.</li>
                <li>Compute at least one requested probability.</li>
                <li>Interpret the result using area under the density graph.</li>
              </ol>
              <p>This question pattern ensures each criterion has observable evidence.</p>
            `
          },
          {
            title: "C1 solution layout",
            contentHtml: String.raw`
              <p><strong>Step 1 (summary):</strong> Identify variable, support, and model assumptions in one short paragraph.</p>
              <p><strong>Step 2 (setup):</strong> Rewrite the task as symbolic events such as $P(2\le X\le7)$.</p>
              <p><strong>Step 3 (link ahead):</strong> State which later section will contain calculations and which will contain interpretation.</p>
            `
          },
          {
            title: "Subsection organization guide",
            contentHtml: String.raw`
              <p>Reusable order for every problem card:</p>
              <ol>
                <li>Problem description</li>
                <li>Questions/tasks</li>
                <li>C1 summary block</li>
                <li>C2 Calculations block</li>
                <li>C2 Interpretation block with graph(s) when needed</li>
              </ol>
              <p>Keeping this sequence consistent helps future editors replace content quickly without changing page architecture.</p>
            `
          }
        ]
      },
      {
        id: "problem-2",
        labels: {
          name: "Example 2 (C2 Calculations): Uniform Density Computations",
          criterion: "C2 Calculations"
        },
        descriptionHtml: String.raw`
          <p>Let waiting time be modeled by $X \sim \text{Uniform}(0,10)$.</p>
          <p>Use the model to find the density function and calculate $P(2 \le X \le 7)$.</p>
        `,
        solutionSections: [
          {
            title: "C2 Calculations",
            contentHtml: String.raw`
              <p>For $X \sim \text{Uniform}(0,10)$, the constant density is $f(x)=\frac{1}{10}$ on the support.</p>
              $$
              f(x)=
              \begin{cases}
              \frac{1}{10}, & 0 \le x \le 10 \\
              0, & \text{otherwise}
              \end{cases}
              $$
              <p>Now compute the event probability:</p>
              <p>$P(2 \le X \le 7)=\frac{7-2}{10}=\frac{5}{10}=0.5$.</p>
              <p>Integral form (same result):</p>
              $$
              P(2 \le X \le 7)=\int_{2}^{7} \frac{1}{10}\,dx
              =\frac{1}{10}(7-2)=0.5.
              $$
              <p>Complement example for practice:</p>
              $$
              P(X>7)=1-P(X\le7)=1-\frac{7}{10}=0.3.
              $$
            `
          }
        ]
      },
      {
        id: "problem-3",
        labels: {
          name: "Example 3 (C2 Interpretation): Reading Linear and Piecewise Density Graphs",
          criterion: "C2 Interpretation"
        },
        descriptionHtml: String.raw`
          <p>Use the two graphs below as interpretation examples for continuous probability models.</p>
          <p>In each graph, the light blue region is full support and the darker region marks a target interval whose probability is read as area under the density curve.</p>
        `,
        solutionSections: [
          {
            title: "C2 Interpretation with HTML-rendered graphs",
            contentHtml: String.raw`
              <div class="graph-gallery">
                <article class="graph-card">
                  <h4>Linear density graph</h4>
                  <div id="linear-density-graph" class="probability-graph" data-graph-label="Linear probability density graph with shaded support and highlighted interval"></div>
                  <p>
                    The support is $[0,10]$, shown by the light shaded region. The darker region highlights $2\le X\le7$.
                    Probability equals area under the red density curve above that darker interval; it is not determined by width alone because density height changes with $x$.
                  </p>
                </article>

                <article class="graph-card">
                  <h4>Piecewise density graph</h4>
                  <div id="piecewise-density-graph" class="probability-graph" data-graph-label="Piecewise probability density graph with shaded support and highlighted interval"></div>
                  <p>
                    The light shading marks the support $[0,10]$. The darker band marks $3\le X\le7$, where probability is the sum of areas from each piece of the red step-like curve.
                    Unlike the linear model, this piecewise graph has constant height on subintervals with jumps at breakpoints, so interpretation must split the interval at those breakpoints.
                  </p>
                </article>
              </div>
            `
          }
        ]
      }
    ]
  };

  function validateData(data) {
    if (!Array.isArray(data.labelDefinitions) || data.labelDefinitions.length < 1 || data.labelDefinitions.length > 4) {
      throw new Error("Practice data must define between one and four label dimensions.");
    }
    if (data.labelDefinitions[0]?.key !== "name") {
      throw new Error('The first practice label must use the key "name".');
    }

    const keys = data.labelDefinitions.map(({ key, label }) => {
      if (typeof key !== "string" || !key.trim() || typeof label !== "string" || !label.trim()) {
        throw new Error("Every practice label definition needs a non-empty key and label.");
      }
      return key;
    });
    if (new Set(keys).size !== keys.length) {
      throw new Error("Practice label keys must be unique.");
    }
    if (!Array.isArray(data.problems)) {
      throw new Error("Practice problems must be an array.");
    }

    const ids = new Set();
    const names = new Set();
    data.problems.forEach((problem, problemIndex) => {
      const prefix = `Problem ${problemIndex + 1}`;
      if (!problem || typeof problem.id !== "string" || !problem.id.trim() || ids.has(problem.id)) {
        throw new Error(`${prefix} must have a unique, non-empty ID.`);
      }
      ids.add(problem.id);
      if (!problem.labels || typeof problem.labels !== "object" || Array.isArray(problem.labels)) {
        throw new Error(`${prefix} must provide a labels object.`);
      }
      const suppliedKeys = Object.keys(problem.labels);
      if (suppliedKeys.length !== keys.length || keys.some((key) => !suppliedKeys.includes(key))) {
        throw new Error(`${prefix} must provide exactly one value for every configured label.`);
      }
      keys.forEach((key) => {
        if (typeof problem.labels[key] !== "string" || !problem.labels[key].trim()) {
          throw new Error(`${prefix} has an empty or invalid "${key}" label.`);
        }
      });
      if (names.has(problem.labels.name)) {
        throw new Error(`Problem names must be unique: "${problem.labels.name}".`);
      }
      names.add(problem.labels.name);
      if (typeof problem.descriptionHtml !== "string") {
        throw new Error(`${prefix} must provide descriptionHtml.`);
      }
      if (!Array.isArray(problem.solutionSections)) {
        throw new Error(`${prefix} solutionSections must be an ordered array.`);
      }
      problem.solutionSections.forEach((section, sectionIndex) => {
        if (!section || typeof section.title !== "string" || !section.title.trim()
          || typeof section.contentHtml !== "string" || !section.contentHtml.trim()) {
          throw new Error(`${prefix}, solution subsection ${sectionIndex + 1}, needs both a title and content.`);
        }
      });
    });
  }

  const escapeHtml = (value) => String(value).replace(/[&<>"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"
  })[character]);

  const uniqueValues = (problems, key) => [...new Set(problems.map((problem) => problem.labels[key]))];

  function allOptionText(label) {
    const lowerLabel = label.toLowerCase();
    if (lowerLabel.endsWith("y")) return `All ${lowerLabel.slice(0, -1)}ies`;
    return `All ${lowerLabel}s`;
  }

  function initializePracticePage() {
    const controls = document.getElementById("practice-selector-controls");
    const status = document.getElementById("practice-selector-status");
    const region = document.getElementById("selected-problem");
    if (!controls || !status || !region) return;

    try {
      validateData(practiceData);
    } catch (error) {
      console.error(error);
      controls.replaceChildren();
      status.textContent = `Practice data error: ${error.message}`;
      region.hidden = true;
      return;
    }

    if (practiceData.problems.length === 0) {
      status.textContent = "No practice problems are available.";
      region.hidden = true;
    }

    const selects = new Map();
    practiceData.labelDefinitions.forEach((definition, index) => {
      const field = document.createElement("div");
      field.className = "practice-selector__field";
      const label = document.createElement("label");
      const select = document.createElement("select");
      select.id = `practice-filter-${definition.key}`;
      select.dataset.labelKey = definition.key;
      label.htmlFor = select.id;
      label.textContent = definition.label;

      if (index === 0) {
        select.add(new Option("Select a problem", ""));
      } else {
        select.add(new Option(allOptionText(definition.label), ""));
        uniqueValues(practiceData.problems, definition.key).forEach((value) => select.add(new Option(value, value)));
      }
      field.append(label, select);
      controls.append(field);
      selects.set(definition.key, select);
    });

    const nameSelect = selects.get("name");

    function matchingProblems() {
      return practiceData.problems.filter((problem) => practiceData.labelDefinitions.slice(1).every(({ key }) => {
        const selectedValue = selects.get(key).value;
        return !selectedValue || problem.labels[key] === selectedValue;
      }));
    }

    function renderGraphs(problem) {
      if (problem.id !== "problem-3" || !window.MathRender?.renderProbabilityGraph) return;
      window.MathRender.renderProbabilityGraph(
        region.querySelector("#linear-density-graph"),
        (x) => 0.04 + 0.012 * x,
        [0, 10],
        [2, 7]
      );
      window.MathRender.renderProbabilityGraph(
        region.querySelector("#piecewise-density-graph"),
        (x) => x < 4 ? 0.08 : x < 7 ? 0.16 : 1 / 15,
        [0, 10],
        [3, 7]
      );
    }

    function renderProblem(problem) {
      const metadata = practiceData.labelDefinitions.slice(1).map(({ key, label }) =>
        `<li><strong>${escapeHtml(label)}:</strong> ${escapeHtml(problem.labels[key])}</li>`
      ).join("");
      const contents = problem.solutionSections.map((section, index) =>
        `<li><a href="#${problem.id}-solution-${index + 1}">${escapeHtml(section.title)}</a></li>`
      ).join("");
      const sections = problem.solutionSections.map((section, index) => {
        const sectionId = `${problem.id}-solution-${index + 1}`;
        return `
          <div class="subsection-minimize collapsed" data-region="subsection">
            <button class="subsection-toggle" type="button" aria-expanded="false" id="${sectionId}-toggle" aria-controls="${sectionId}">
              <span class="toggle-label">${escapeHtml(section.title)}</span><span class="toggle-icon" aria-hidden="true">+</span>
            </button>
            <div class="subsection-content" id="${sectionId}" role="region" aria-labelledby="${sectionId}-toggle">
              <div class="content-block">${section.contentHtml}</div>
              <div class="subsection-footer"><a class="subsection-back-link" href="#${problem.id}-solution-list" aria-label="Back to solution contents">↑</a></div>
            </div>
          </div>`;
      }).join("");

      region.id = problem.id;
      region.innerHTML = `
        <h2>${escapeHtml(problem.labels.name)}</h2>
        ${metadata ? `<ul class="practice-problem__metadata" aria-label="Problem properties">${metadata}</ul>` : ""}
        <div class="example">
          <h3>Problem description</h3>
          <div class="content-block">${problem.descriptionHtml}</div>
          <nav class="practice-problem__contents" aria-label="Solution contents">
            <h3 id="${problem.id}-solution-list">Solution sections</h3>
            <ol>${contents}</ol>
          </nav>
          ${sections}
        </div>
        <div class="back-to-top"><a class="back-to-top-button" href="#practice-selector"><span class="back-to-top-icon" aria-hidden="true">↑</span>Back to Problem Selector</a></div>`;
      region.hidden = false;
      renderGraphs(problem);
      if (window.MathJax?.typesetPromise) {
        window.MathJax.typesetPromise([region]).catch((error) => console.error("MathJax typesetting failed:", error));
      }
      status.textContent = `${problem.labels.name} selected.`;
    }

    function hideProblem() {
      region.replaceChildren();
      region.id = "selected-problem";
      region.hidden = true;
    }

    function updateNameOptions() {
      const previousName = nameSelect.value;
      const matches = matchingProblems();
      nameSelect.replaceChildren(new Option(matches.length ? "Select a problem" : "No matching problems", ""));
      nameSelect.options[0].disabled = matches.length === 0;
      matches.forEach((problem) => nameSelect.add(new Option(problem.labels.name, problem.id)));

      const selectedProblem = matches.find((problem) => problem.id === previousName);
      if (selectedProblem) {
        nameSelect.value = previousName;
      } else {
        nameSelect.value = "";
        hideProblem();
      }
      status.textContent = matches.length ? "Select a problem to display it." : "No matching problems.";
    }

    practiceData.labelDefinitions.slice(1).forEach(({ key }) => {
      selects.get(key).addEventListener("change", updateNameOptions);
    });
    nameSelect.addEventListener("change", () => {
      const problem = practiceData.problems.find(({ id }) => id === nameSelect.value);
      if (problem && matchingProblems().includes(problem)) renderProblem(problem);
      else {
        hideProblem();
        status.textContent = "Select a problem to display it.";
      }
    });
    region.addEventListener("click", (event) => {
      const button = event.target.closest(".subsection-toggle");
      if (!button || !region.contains(button)) return;
      const subsection = button.closest(".subsection-minimize");
      const expanded = button.getAttribute("aria-expanded") !== "true";
      button.setAttribute("aria-expanded", String(expanded));
      button.querySelector(".toggle-icon").textContent = expanded ? "−" : "+";
      subsection.classList.toggle("collapsed", !expanded);
    });

    updateNameOptions();
  }

  initializePracticePage();
})();
